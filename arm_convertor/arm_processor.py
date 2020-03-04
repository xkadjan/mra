#import os
import numpy as np
import pandas as pd
import hall_signal_corrector as hf
import enc_signal_corrector_2 as ef
import math
import ctypes
    
class Arm_Processor(object):
    def __init__(self,arm_path,wgs_ref1,wgs_ref2,ENC_resolution,Radius,artifical_angle_offset,rate_hz,time_lists=[[0,0]]):
        heading = self.bearing(wgs_ref1, wgs_ref2)
        self.ARMPATH = arm_path
        self.PHASE = np.deg2rad(360 - heading + 90)
        self.RADIUS = Radius
        self.COR = [0,0]
        self._time_list = time_lists
        self._arm_data = None
        self._hall_times = None
        self._owntime = None
        self.ENC_resolution = 2500
        self.artifical_angle_offset = artifical_angle_offset
        self.rate_hz = rate_hz
        self.arm_synced = None
        self.direction = None

    def bearing(self,wgs_1,wgs_2):
        lat1 = wgs_1[0,0]
        lat2 = wgs_2[0,0]
        lon1 = wgs_1[0,1]
        lon2 = wgs_2[0,1]
        dlon = np.deg2rad(lon2 - lon1)
    
        bearing = np.arctan((np.sin(dlon) * np.cos(np.deg2rad(lat2))) / (np.cos(np.deg2rad(lat1)) * np.sin(np.deg2rad(lat2)) - np.sin(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.cos(dlon)))
        return 360 + bearing * 180 / np.pi

    def arm_extractor(self):
        data = pd.read_fwf(self.ARMPATH,
                           widths=[10, 1, 1, 2, 4, 7, 2, 1, 1, 1, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
                           skiprows=4, header=None, skipfooter=2)
        data.drop(labels=[1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25], axis=1, inplace=True)
        data.rename(
            columns={0: 'Log_Time', 4: 'ID', 10: 'Bytes', 12: 1, 14: 2, 16: 3, 18: 4, 20: 5, 22: 6, 24: 7, 26: 8},
            inplace=True)
        try:
            dropers = data.index[data.ID == '768'].tolist()
        except Exception:
            dropers = data.index[data.ID == 768].tolist()
        if dropers:
            data.drop(data.index[dropers[0]:], inplace=True)
        data = data.fillna(value=0)
        data.ID = data.ID.astype('int')
        cols_to_check = ['Bytes', 1, 2, 3, 4, 5, 6, 7, 8]
        for col in cols_to_check:
            if not isinstance(data[col].iloc[6], float):
                data[col] = data[col].astype(float)
        return data

    def Byte4_converter(self,c1, c2, c3, c4):
        return c1 * 16777216 + c2 * 65536 + c3 * 256 + c4

    def Bytes2dec(self,b1, b2, b3, b4):
        bn1 = int(b4) << 24
        bn2 = int(b3) << 16
        bn3 = int(b2) << 8
        bn4 = int(b1)
        n = bn1 | bn2 | bn3 | bn4
        bn = bin(n)
        e = int(bn[2:10], 2) - 127
        mantissa = (int(bn[10:], 2)) / 2. ** 23
        return (1 + mantissa) * 2 ** e

    def DetaTime2sec(self,hr, min, sec, milis=0):
        return hr * 3600 + min * 60 + sec + milis / 1000
    
    def to_signed(self,ENCnum):  
        for row in range(len(ENCnum)):
            ENCnum[row] = ctypes.c_long(int(ENCnum[row])).value
        return ENCnum

    def parse_nmea(self,data,msgID):
        nmeacode = data[data.ID == 1024]
        nmeatime = nmeacode.iloc[0] - 48
        data_out = (nmeatime[1] * 10 + nmeatime[2]) * 3600 + (nmeatime[3] * 10 + nmeatime[4]) * 60 + nmeatime[5] * 10 + nmeatime[6]
        data_out_string = nmeatime[1]*100000 + nmeatime[2]*10000 + nmeatime[3]*1000 + nmeatime[4]*100 + nmeatime[5]*10 + nmeatime[6]
        return data_out,data_out_string
    
    def parse_sensor_data(self, arm, time_ID, num_ID):
        arm_raw_arr = arm.as_matrix()
        sensor = []
        pair = np.array([np.nan,np.nan])
        for arm_row in range(len(arm_raw_arr)):
            msg_ID = arm.iloc[arm_row,1]
            if msg_ID == time_ID: #kdyz je to cas
                msg = arm_raw_arr[arm_row,3:7]
                pair[0] = self.Byte4_converter(msg[0],msg[1],msg[2],msg[3])
            elif msg_ID == num_ID: #kdyz je to increment
                if not np.isnan(pair)[0]:
                    msg = arm_raw_arr[arm_row,3:7]
                    pair[1] = self.Byte4_converter(msg[0],msg[1],msg[2],msg[3])
                    sensor.append([pair[1],pair[0]])
                    pair = np.array([np.nan,np.nan])
        sensor = pd.DataFrame(sensor)
        return sensor
    
    def arm_parser(self,arm):
        print (" - processing: " + str(self.ARMPATH))
        fixtimesec,fixtimestring = self.parse_nmea(arm, 1024)     
        sensorPPS = self.parse_sensor_data(arm, 1025, 1026)
        sensorPPS.columns = ['PPSnum', 'PPStime']
        print(" - PPS parsing - done" )        
        sensorHALL = self.parse_sensor_data(arm, 1040, 1041)
        sensorHALL.columns = ['HALLnum', 'HALLtime']
        print(" - HALL parsing - done" )        
        sensorENC = self.parse_sensor_data(arm, 1056, 1057)
        sensorENC.columns = ['ENCnum', 'ENCtime']
        print(" - ENC parsing - done" )
        return fixtimesec,fixtimestring,sensorPPS,sensorHALL,sensorENC
    
    def get_time_err(self,sensorPPS):
        ppsTdif = sensorPPS.PPStime.sub(sensorPPS.PPStime.shift(), fill_value=0)
        ppsNdif = sensorPPS.PPSnum.sub(sensorPPS.PPSnum.shift(), fill_value=0)
        relative_pps_time = (ppsNdif * 1000000 - ppsTdif) / ppsNdif
        relative_pps_time[0] = 'NaN'
        sensorPPS['RelPPStime'] = relative_pps_time
        sensorPPSuFixTime = sensorPPS.PPStime[0]
        sensorPPS = sensorPPS.where((sensorPPS.RelPPStime < 50) & (sensorPPS.RelPPStime > -50))
        sensorPPS = sensorPPS.dropna()
        sensorPPSuError = sensorPPS.RelPPStime[2:len(relative_pps_time)].mean()
        print(" - sensorPPSuFixTime",sensorPPSuFixTime)
        print(" - sensorPPSuError",sensorPPSuError)
        return sensorPPS, sensorPPSuError, sensorPPSuFixTime
    
    def enc_per_circle(self,sensorENC):
        enc_per_round = pd.DataFrame(sensorENC[[7,9]])
        enc_per_round.rename(columns={7: 'hall', 9: 'enc'},inplace=True)
#        enc_per_round['enc'] = enc_per_round.enc + 1                    # maybe this woks with one direction 
        enc_per_round['hall_diff'] = enc_per_round.hall.diff().shift(-1)
        enc_per_round.enc = (enc_per_round.enc % self.ENC_resolution).astype(int)
        
        first_circle = enc_per_round.enc.where(enc_per_round.hall == 0).dropna()
        first_circle = max(abs(first_circle.drop(first_circle.index[0]) - self.ENC_resolution))
        first_circle = pd.DataFrame({"hall":[0],"enc":[first_circle],"hall_diff":[1]})        
        enc_per_round = enc_per_round.append(first_circle).sort_index()
        
        enc_per_round = enc_per_round.where(enc_per_round.hall_diff != 0).dropna()
        enc_per_round = enc_per_round.drop(enc_per_round.index[1])
        
        errors = enc_per_round.enc.tolist()
        for error in range(len(errors)): 
            if errors[error] > self.ENC_resolution/2: errors[error] = errors[error] - self.ENC_resolution
        enc_per_round.enc = errors
       
        return enc_per_round.enc.reset_index().enc

    def arm_processor(self):
        arm = self.arm_extractor()         # load ASC data file
        fixtimesec,fixtimestring,sensorPPS,sensorHALL,sensorENC = self.arm_parser(arm)
        sensorPPS, sensorPPSuError, sensorPPSuFixTime = self.get_time_err(sensorPPS)
        sensorHALL = sensorHALL.dropna()
        sensorENC = sensorENC.dropna()               
        sensorENC["ENCnum"] = self.to_signed(sensorENC.ENCnum.tolist())

        sensorENC = ef.ENC_signal_corrector(sensorENC)
        sensorENC.rename({'time': 'ENCtime',
                          'num': 'ENCnum'}, axis=1, inplace=True)
    
        self.direction = sum(sensorENC.ENCnum.diff().dropna()) > 0
#                   
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::       
        sensorHALL[2] = sensorHALL.HALLtime - sensorPPSuFixTime
        sensorHALL[3] = sensorHALL[2] / 1000000
        sensorHALL[4] = np.floor(sensorPPSuError * sensorHALL[3].apply(np.floor))
        sensorHALL[5] = sensorHALL[2] + (sensorHALL[4])
        sensorHALL[6] = sensorHALL[5] / 1000000
        sensorHALL[8] = fixtimesec + sensorHALL[6]

        sensorENC[2] = sensorENC.ENCtime - sensorPPSuFixTime
        sensorENC[3] = sensorENC[2] / 1000000
        sensorENC[4] = np.floor(sensorPPSuError * sensorENC[3].apply(np.floor))
        sensorENC[5] = sensorENC[2] + (sensorENC[4])
        sensorENC[6] = sensorENC[5] / 1000000
        
        sensorHALL, sensorHALL_orig = hf.hall_filter(self.ENC_resolution,sensorHALL,sensorENC)
        sensorHALL = sensorHALL.reset_index()

        lensENC = len(sensorENC)
        lensHALL = len(sensorHALL)

        cirnums = []
        for i in range(lensENC):
            numOfCircle = 0
            for j in range(lensHALL):
                if sensorENC[6].iloc[i] > sensorHALL[6].iloc[j]:
                    numOfCircle += 1
            cirnums.append(numOfCircle)
        sensorENC[7] = cirnums
        
        units = []
        for i in range(lensHALL):
            numOfUnit = 0
            for j in range(lensENC):
                if sensorHALL.HALLnum[i] == sensorENC[7].iloc[j]:
                    numOfUnit += 1
            units.append(numOfUnit)
        sensorHALL[7] = units

        numOfDegree = 0
        numOfDegreeMem = 0
        col8 = [0]
        col9 = [0]
        for i in range(1, lensENC):
            if sensorENC[7].iloc[i] > sensorENC[7].iloc[i - 1]:
                numOfDegree = 1
                col9.append(sensorENC.ENCnum.iloc[i] - sensorENC.ENCnum.iloc[i - 1])
                numOfDegreeMem = sensorENC.ENCnum.iloc[i - 1]
            else:
                numOfDegree += 1
                col9.append(sensorENC.ENCnum.iloc[i] - numOfDegreeMem)
            col8.append(numOfDegree)
        sensorENC[8] = col8
        sensorENC[9] = col9      
        sensorENC.drop(sensorENC[sensorENC['ENCnum'] == 0 ].index , inplace=True)
        
        sensorHALL['enc_err'] = self.enc_per_circle(sensorENC).astype(int)

        mask = sensorENC[7] == 0
        lastoff = sensorENC.loc[mask, [9]]
        if not self.direction: lastoff = lastoff + 2*self.ENC_resolution
        if not lastoff.empty: sensorENC.loc[mask, [9]] = sensorENC.loc[mask, [9]] + self.ENC_resolution - lastoff.iloc[len(lastoff) - 1]
        sensorENC[10] = (sensorENC[9] * 360 / self.ENC_resolution) % 360        
        sensorENC[10] = sensorENC[10] + self.artifical_angle_offset                      # <- artifical offset        
        sensorENC[11] = np.radians(sensorENC[10])
        sensorENC[12] = self.RADIUS * -np.cos(sensorENC[11] + self.PHASE)
        sensorENC[13] = self.RADIUS * -np.sin(sensorENC[11] + self.PHASE)
      
        sensorENC = sensorENC[1:]
               
        armPositions = pd.DataFrame(sensorENC[['ENCnum', 6, 10, 11, 12, 13]])
        armPositions.rename(
            columns={'ENCnum': 'ENCnumber', 6: 'EventTime', 10: 'ENCangle', 11: 'ENCangle_rad', 12: 'Xarm', 13: 'Yarm'},
            inplace=True)
        armPositions['Time'] = sensorENC[6] + fixtimesec
        sensorPPS['Time'] = (sensorPPS['PPStime'] - sensorPPSuFixTime)/1000000 + fixtimesec

        colnames = armPositions.columns.tolist()
        colnames.pop(colnames.index('Time'))
        colnames.insert(0, 'Time')
        armPositions = armPositions[colnames]
               
        self._hall_times = sensorHALL[8]
        self._arm_data = armPositions
        
        self.arm_synced = self.downsampling(armPositions[['Time', 'ENCangle']])
        
        self.arm_synced['ENCangle_rad'] = np.radians(self.arm_synced['ENCangle'])
        self.arm_synced['Xarm'] = self.RADIUS * -np.cos(self.arm_synced['ENCangle_rad'] + self.PHASE)
        self.arm_synced['Yarm'] = self.RADIUS * -np.sin(self.arm_synced['ENCangle_rad'] + self.PHASE)
        
        self.arm_synced["raw_speed"] = ((self.arm_synced.Xarm.diff().pow(2) + self.arm_synced.Yarm.diff().pow(2)).pow(1/2) / self.arm_synced.Time.diff()).fillna(0) * 3.6
                      
#        return sensorPPS,sensorHALL,sensorHALL_orig,sensorENC,sensorPPSuError,fixtimestring,ENC_analysis,outsiders
        return sensorPPS,sensorHALL,sensorHALL_orig,sensorENC,sensorPPSuError,fixtimestring
    
    def downsampling(self,arm_asynchr):
        start_time = math.ceil(arm_asynchr.Time.min() * self.rate_hz) / self.rate_hz
        stop_time = math.floor(arm_asynchr.Time.max() * self.rate_hz) / self.rate_hz
        print(" - raw samples (starttime,stoptime,number):",arm_asynchr.Time.min(),arm_asynchr.Time.max(),len(arm_asynchr))
        
        num_of_samples = round((stop_time - start_time) * self.rate_hz) + 1
        sampled_time = np.linspace(start_time, stop_time, num=num_of_samples)
        print(" - new samples (starttime,stoptime,number):",start_time,stop_time,num_of_samples)
        
        sampled_angle = self.interpolate_angle(arm_asynchr,sampled_time)

        arm_synced = pd.DataFrame(np.vstack((sampled_time,sampled_angle)).T)
        arm_synced.rename(columns={0: 'Time', 1: 'ENCangle'},inplace=True)
        
#        tck = interpolate.splrep(arm_asynchr.Time, arm_asynchr.ENCangle_rad, s=0)
#        sampled_angles = interpolate.splev(sampled_time, tck, der=0)
#        
#        arm_synced = pd.DataFrame(np.vstack((sampled_time,sampled_angles)).T)
#        arm_synced.rename(columns={0: 'Time', 1: 'ENCangle_rad'},inplace=True)
#        
##        arm_synced['ENCangle_rad'] = self.get_median_filtered(arm_synced.ENCangle_rad)  
#        arm_synced['ENCangle_rad'], mask = self.get_median_filtered(arm_synced.ENCangle_rad)
##        arm_synced = arm_synced.drop(np.where(mask)[0].tolist())
        return arm_synced
    
    def interpolate_angle(self, arm_asynchr, sampled_time):
        arm_asynchr_time_np = np.array(arm_asynchr.Time)
        arm_asynchr_angle_np = np.array(arm_asynchr.ENCangle)
        num_of_resampled = len(sampled_time)
        time_pairs_list,angle_pairs_list = [],[]
        for sample in range(num_of_resampled):
            time_diff = arm_asynchr_time_np - sampled_time[sample]
            index_diff = np.argmin(abs(time_diff))  
            nearest_diff_value = time_diff[index_diff]
            if nearest_diff_value > 0: index_diff -= 1
            time_pairs_list.append([arm_asynchr_time_np[index_diff], arm_asynchr_time_np[index_diff+1]])
            angle_pairs_list.append([arm_asynchr_angle_np[index_diff], arm_asynchr_angle_np[index_diff+1]])
            
        for sample in range(len(angle_pairs_list)):     # corrector of peaks caused by hall 
            angle_diff = angle_pairs_list[sample][1]-angle_pairs_list[sample][0]
            if not abs(angle_diff) < 360 - 1:
                if angle_diff > 0:
                    angle_pairs_list[sample][1] = angle_pairs_list[sample][1] - 360
                else:
                    angle_pairs_list[sample][1] = angle_pairs_list[sample][1] + 360
        
        sampled_angle = []
        for sample in range(num_of_resampled):
            ratio = (sampled_time[sample] - time_pairs_list[sample][0]) / (time_pairs_list[sample][1] - time_pairs_list[sample][0])   
            sampled_angle.append(((angle_pairs_list[sample][1]-angle_pairs_list[sample][0]) * ratio) + angle_pairs_list[sample][0])
        sampled_angle = np.array(sampled_angle)
           
        return sampled_angle
    
#    def get_median_filtered(self,signal, threshold=3):
#        signal = signal.copy()
#        difference = np.abs(signal - np.median(signal))
#        median_difference = np.median(difference)
#        if median_difference == 0:
#            s = 0
#        else:
#            s = difference / float(median_difference)
#        mask = s > threshold
#        signal[mask] = np.median(signal)
#        return signal, mask
        
def peak_detector(arm_synced):        
    speed_diff = arm_synced.raw_speed.diff()
    peaks = []
    for sample in range(len(speed_diff)):
        if abs(speed_diff[sample]) > 4:
            peaks.append([sample,arm_synced.Time[sample],speed_diff[sample]])
    return pd.DataFrame(peaks,columns=['sample_index', 'utc_time', 'raw_speed_diff'])

def get_halls(sensorHALL):
    halls = pd.DataFrame(sensorHALL[["HALLnum",8,'enc_err']])
    halls.columns = ["hall_index","utc_time","enc_err"]  
    return halls   

def get_halls_orig(sensorHALL_orig):
    halls = pd.DataFrame(sensorHALL_orig[["HALLnum",8]])
    halls[7]=0
    halls.columns = ["hall_index","utc_time","enc_err"]  
    return halls       

# =============================================================================
# # todo:  
# #   - rename colls in sensorENC!         
# #   - time correction distribution to whole sec
# =============================================================================
