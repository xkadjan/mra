# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:57:48 2019

@author: xkadj
"""

import os
import numpy as np
import pandas as pd
import sync_transpositions as transpos
import sync_plotting as plot

class ArmParser:

    def __init__(self,dir_arm,prefix):
        self.ENC_resolution = 2500      # [-]
        self.enc_tol = 3                # [-]
        self.badhall_tol = 10           # [s]
        self.speed_drop_tol = 0.1       # [m*s-1]
        self.acc_drop_tol = [0.01,10]   # [m*s-2]
        self.seconds_to_drop = 100      # [s]
        self.seconds_over_hall = 0.1    # [s]
        self.last_len_20hz = 0

        self.arm_20hz_paths = self.get_files(dir_arm,'20hz',prefix)
        self.arm_async_paths = self.get_files(dir_arm,'async',prefix)
        self.arm_badhalls_paths = self.get_files(dir_arm,'badhalls',prefix)
        self.arm_halls_paths = self.get_files(dir_arm,'halls',prefix)
        self.arm_peaks_paths = self.get_files(dir_arm,'peaks',prefix)

        self.arm_20hz = pd.DataFrame(columns=["utc_time","east","north","up","raw_speed","raw_acc"])
        self.arm_async = pd.DataFrame(columns=["utc_time","east","north","up","raw_speed","raw_acc"])
        self.arm_badhalls = pd.DataFrame(columns=['hall_index', 'utc_time', 'enc_err'])
        self.arm_halls = pd.DataFrame(columns=['hall_index', 'utc_time', 'enc_err'])
        self.arm_peaks = pd.DataFrame(columns=['sample_index', 'utc_time', 'raw_speed_diff'])

        self.circle_good = pd.DataFrame(columns=["row","enc","error","time_start","time_end"])
        self.circle_bad = pd.DataFrame(columns=["row","enc","error","time_start","time_end"])

    def get_files(self,dir,signal,prefix):
        files = os.listdir(dir)
        csvs = [i for i in files if '.csv' in i]
        csvs = [i for i in csvs if not i.find(signal)]
        csvs_paths = [os.path.join(dir, name) for name in csvs]
        csvs_paths = [i for i in csvs_paths if prefix in i]
        start_times = [float(i.split('_')[-2]) for i in csvs_paths]
        # Sorting of paths:
        csvs_paths = [[start_times[meas],csvs_paths[meas]] for meas in range(len(csvs_paths))]
        csvs_paths.sort(key=lambda pair: pair[0])
        csvs_paths = [csvs_paths[meas][1] for meas in range(len(csvs_paths))]
        return csvs_paths

    def parse_slices(self):
#        for file in self.arm_async_paths:
#            self.parse_async(file)
        for file in self.arm_20hz_paths:
            self.parse_20hz(file)

        for file in self.arm_badhalls_paths:
            self.parse_badhalls(file)

        for file in self.arm_halls_paths:
            self.parse_halls(file)

        self.arm_halls = self.arm_halls.reset_index()
        self.arm_halls = self.add_meas_num(self.arm_halls)

        for file in self.arm_peaks_paths:
            self.parse_peaks(file)

    def parse_async(self,file):
        arm = pd.read_csv(file, sep=',', engine='python')
        arm = arm[["Time","Xarm","Yarm"]]
        arm = arm.rename(columns={"Time": "utc_time", "Xarm": "east", "Yarm": "north"})
        arm["raw_speed"] = ((arm.east.diff().pow(2) + arm.north.diff().pow(2)).pow(1/2) / arm.utc_time.diff()).fillna(0)
        arm["raw_acc"] = (arm.raw_speed.diff() / arm.utc_time.diff()).fillna(0)
        self.arm_async = self.arm_async.append(arm)
        print(' - arm async loading done, ' + str(len(arm)) + ' points')

    def parse_20hz(self,file):
        arm = pd.read_csv(file, sep=',', engine='python')
        arm = arm[["Time","Xarm","Yarm"]]
        arm = arm.rename(columns={"Time": "utc_time", "Xarm": "east", "Yarm": "north"})
        arm["up"] = 0
        arm["raw_speed"] = ((arm.east.diff().pow(2) + arm.north.diff().pow(2)).pow(1/2) / arm.utc_time.diff()).fillna(0)
        arm["raw_acc"] = (arm.raw_speed.diff() / arm.utc_time.diff()).fillna(0)
        self.arm_20hz = self.arm_20hz.append(arm[["utc_time","east","north","up","raw_speed","raw_acc"]])
        self.last_len_20hz = len(self.arm_20hz)
        print(' - arm 20hz loading done, ' + str(len(arm)) + ' points')

    def parse_badhalls(self,file):
        badhalls = pd.read_csv(file, sep=',', engine='python')
        self.arm_badhalls = self.arm_badhalls.append(badhalls[['hall_index', 'utc_time', 'enc_err']])
        print(' - arm bad halls loading done, ' + str(len(badhalls)) + ' hall signals')

    def parse_halls(self,file):
        halls = pd.read_csv(file, sep=',', engine='python')#.values.tolist()
        self.arm_halls = self.arm_halls.append(halls[['hall_index', 'utc_time', 'enc_err']])
        print(' - arm halls loading done, ' + str(len(halls)) + ' hall signals')

    def parse_peaks(self,file):
        peaks = pd.read_csv(file, sep=',', engine='python')#.values.tolist()
        self.arm_peaks = self.arm_peaks.append(peaks[['sample_index', 'utc_time', 'raw_speed_diff']])
        print(' - arm peaks loading done, ' + str(len(peaks)) + ' peak signals')

    def get_bad_cicles(self):
        arm_halls_index = self.arm_halls['index'].astype(int).tolist()
        arm_halls_enc = self.arm_halls.enc_err.astype(int).tolist()
        arm_halls_time = self.arm_halls.utc_time.tolist()
        circle_bad,circle_good = [],[]
        for row in range(len(arm_halls_index)):
            if arm_halls_index[row] != 0:
                error = abs(arm_halls_enc[row])
                if error >= self.enc_tol:
                    circle_bad.append([row,arm_halls_enc[row],error,arm_halls_time[row-1]-self.seconds_over_hall,arm_halls_time[row]+self.seconds_over_hall])
                else:
                    circle_good.append([row,arm_halls_enc[row],error,arm_halls_time[row-1],arm_halls_time[row]])
            else:
                circle_good.append([row,arm_halls_enc[row],-1,arm_halls_time[row-1],arm_halls_time[row]])
        self.circle_good = pd.DataFrame(circle_good,columns=["row","enc","error","time_start","time_end"])
        self.circle_bad = pd.DataFrame(circle_bad,columns=["row","enc","error","time_start","time_end"])
        self.drop_last_badhalls()

    def drop_last_badhalls(self):
        badhalls_index = self.arm_badhalls.index.astype(int).tolist()
        badhalls_index = [i - 1 for i,x in enumerate(badhalls_index) if x == 0]
        badhalls_last = self.arm_badhalls.iloc[badhalls_index]
        gap_after_last_good = self.circle_good[self.circle_good.error == -1]
        first_points = self.arm_20hz.loc[0]
        first_points['utc_time'].iat[0] = 86400

        for i in range(len(badhalls_last)):
            if badhalls_last.utc_time.iloc[i] > gap_after_last_good.time_start.iloc[i] + self.badhall_tol:
                last_to_drop = gap_after_last_good.iloc[i]
                last_to_drop.time_end = first_points.iloc[i].utc_time    #last_to_drop.time_start + self.seconds_to_drop
                self.circle_bad = self.circle_bad.append(last_to_drop)
        self.circle_bad = self.circle_bad.reset_index()

    def add_meas_num(self,arm_halls):
        measurement, meas = 0, []
        for i,hall in arm_halls.iterrows():
            if hall['index'] == 0:
                measurement += 1
            meas.append(measurement)
        arm_halls.insert(2,'meas',meas)
        return arm_halls

    def print_drop_ratio(self,label):
        drop_ratio = 100 - (len(self.arm_20hz) / self.last_len_20hz * 100)
        self.last_len_20hz = len(arm.arm_20hz)
        print(' - ' + label + ": %.3f" % drop_ratio + ' % of points were dropped')

    def drop_bad_circles(self):
        arm_20hz = self.arm_20hz.reset_index()
        circle_bad = self.circle_bad
        condition = pd.Series()
        for slice_out in range(len(circle_bad)):
            condition = (circle_bad.loc[slice_out].time_start < arm_20hz.utc_time) & (arm_20hz.utc_time < circle_bad.loc[slice_out].time_end) | condition
        self.arm_20hz = arm_20hz.drop(condition.index[condition == True])
        self.print_drop_ratio('drop_bad_circles')

    def drop_zero_speed(self):
        indexes_to_drop = self.arm_20hz.index[abs(self.arm_20hz.cvl_speed) < self.speed_drop_tol]
        self.arm_20hz = self.arm_20hz.drop(indexes_to_drop)
        self.print_drop_ratio('drop_zero_speed')

    def drop_zero_acc(self):
        indexes_to_drop = self.arm_20hz.index[abs(self.arm_20hz.cvl_acc) < self.acc_drop_tol[0]]
        self.arm_20hz = self.arm_20hz.drop(indexes_to_drop)
        self.print_drop_ratio('drop_zero_acc')

    def drop_limit_acc(self):
        indexes_to_drop = self.arm_20hz.index[abs(self.arm_20hz.raw_acc) > self.acc_drop_tol[1]]
        self.arm_20hz = self.arm_20hz.drop(indexes_to_drop)
        self.print_drop_ratio('drop_limit_acc')

    def drop_peaks(self):
        times_to_drop = self.arm_peaks.utc_time.tolist()
        condition = pd.Series()
        for time in times_to_drop:
            condition = (self.arm_20hz.utc_time == time) | condition
        self.arm_20hz = self.arm_20hz.drop(condition.index[condition == True])
        self.print_drop_ratio('drop_peaks')

    def filter_signal(self):
        self.arm_20hz["cvl_speed"] = self.convolve_filter(self.arm_20hz.raw_speed,7)
        self.arm_20hz["cvl_acc"] = self.convolve_filter(self.arm_20hz.raw_acc,33)

    def convolve_filter(self,signal,kernel_size):
        kernel = (np.ones(kernel_size)/kernel_size).tolist()
        cvl = np.zeros(len(signal))
        cvl[int((kernel_size-kernel_size%2)/2):-int((kernel_size-kernel_size%2)/2)] = np.convolve(signal, kernel, mode='valid')
        return cvl

    def slice_times(self,slice_times):
        self.arm_20hz = self.arm_20hz[(self.arm_20hz.utc_time > slice_times[0]) & (self.arm_20hz.utc_time < slice_times[1])]
        self.arm_async = self.arm_async[(self.arm_async.utc_time > slice_times[0]) & (self.arm_async.utc_time < slice_times[1])]
        self.arm_badhalls = self.arm_badhalls[(self.arm_badhalls.utc_time > slice_times[0]) & (self.arm_badhalls.utc_time < slice_times[1])]
        self.arm_halls = self.arm_halls[(self.arm_halls.utc_time > slice_times[0]) & (self.arm_halls.utc_time < slice_times[1])]
        self.arm_peaks = self.arm_peaks[(self.arm_peaks.utc_time > slice_times[0]) & (self.arm_peaks.utc_time < slice_times[1])]

class RtkParser:

    def __init__(self,dir_rtk,fixed_height):
        self.fixed_height = fixed_height
        self.dir_rtk = dir_rtk
        self.rtk_folders = os.listdir(dir_rtk)
        self.novatel = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.tersus = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.ashtech = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.ublox = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.novatel_ref = pd.DataFrame()
        self.tersus_ref = pd.DataFrame()
        self.ashtech_ref = pd.DataFrame()
        self.ublox_ref = pd.DataFrame()

    def parse_slices(self,prefix):

        folders = [i for i in self.rtk_folders if prefix in i]

        for folder in folders:
            rtk_txts_paths = rtk.load_files(folder,'novatel')
            rtk.novatel = self.novatel.append(rtk.parse_rtk(rtk_txts_paths))

        for folder in folders:
            rtk_txts_paths = self.load_files(folder,'tersus')
            rtk.tersus = rtk.tersus.append(rtk.parse_rtk(rtk_txts_paths))

        for folder in folders:
            rtk_txts_paths = self.load_files(folder,'ashtech')
            rtk.ashtech = rtk.ashtech.append(rtk.parse_rtk(rtk_txts_paths))

        for folder in folders:
            rtk_txts_paths = self.load_files(folder,'ublox')
            rtk.ublox = rtk.ublox.append(rtk.parse_rtk(rtk_txts_paths))

    def load_files(self,folder,rtk_type):
        rtk_folder = os.path.join(self.dir_rtk, folder)
        rtk_files = os.listdir(rtk_folder)
        rtk_txts = [i for i in rtk_files if '.txt' in i]
        rtk_txts = [i for i in rtk_files if rtk_type in i]
        rtk_txts_paths = [os.path.join(rtk_folder, name) for name in rtk_txts]
        return rtk_txts_paths

    def parse_rtk(self,rtk_txts_paths):
        for file in rtk_txts_paths:
            f = open(file, "r")
            if f.mode == 'r':
                log = f.read()
                sentences = log.split('$')[1:]
                label = file.split('\\')[-2:]
                rtk = pd.DataFrame(self.get_points(sentences,label)).astype(float)
                rtk.columns = ['utc_time','lat','lon','status']
                rtk["height"] = self.fixed_height
                rtk.insert(len(rtk.count()), 'lat_in_rad', rtk.lat*np.pi/180, allow_duplicates=False)
                rtk.insert(len(rtk.count()), 'lon_in_rad', rtk.lon*np.pi/180, allow_duplicates=False)
                xyz = transpos.wgs2xyz(rtk[['lat_in_rad','lon_in_rad','height']].values)
                enu = transpos.xyz2enu(xyz,wgs_ref)
                rtk["east"], rtk["north"], rtk["up"] = enu.T[0], enu.T[1], enu.T[2]
                rtk = rtk[["utc_time","lat","lon","height","east","north","up",'status']]
                return rtk

    def get_points(self,sentences,label):
        points = []
        error_sentence,incomplete_sentence = [],[]
        for sentence in range(len(sentences)):
            sentences[sentence] = sentences[sentence].replace("GNGGA", "GPGGA")
            sentences[sentence] = sentences[sentence].split(',')
            if 'E' in sentences[sentence] and len(sentences[sentence]) == 15:
                E_index = sentences[sentence].index('E')
                utc = sentences[sentence][E_index-4]
                lat = sentences[sentence][E_index-3]
                lon = sentences[sentence][E_index-1]
                if len(sentences[sentence]) > 5:
                    status = int(sentences[sentence][E_index+1])
                else:
                    status = 6                    # without status
                try:
                    utc = transpos.get_seconds(utc)
                    lat = transpos.get_coordinate(lat)
                    lon = transpos.get_coordinate(lon)
                    parameters = [utc,lat,lon,status]
                    points.append(parameters)
                except:
                    error_sentence.append(sentence+1)
                    continue
            else:
                incomplete_sentence.append(sentence+1)
        drop_ratio = ((len(incomplete_sentence)+len(error_sentence)) / len(points) * 100)
        print(" - " + label[0] + '-'+ label[1].split('_')[1].split('.')[0] + " %.3f" % drop_ratio + ' % of NMEAs were incomplete')
        return points

    def drop_points_wo_arm(self,arm_df):
        self.novatel = self.drop_according_time(self.novatel,arm_df,'novatel')
        self.tersus = self.drop_according_time(self.tersus,arm_df,'tersus')
        self.ashtech = self.drop_according_time(self.ashtech,arm_df,'ashtech')
        self.ublox = self.drop_according_time(self.ublox,arm_df,'ublox')

    def drop_points_wo_rtk(self,arm_df):
        self.novatel_ref = self.drop_according_time(arm_df,self.novatel,'novatel_ref')
        self.tersus_ref = self.drop_according_time(arm_df,self.tersus,'tersus_ref')
        self.ashtech_ref = self.drop_according_time(arm_df,self.ashtech,'ashtech_ref')
        self.ublox_ref = self.drop_according_time(arm_df,self.ublox,'ublox_ref')

    def drop_according_time(self,dropped_df,reference_df,label):
        print(' - points where is no arm reference will be droped from ' + label)
        dropped_df = dropped_df.sort_values(by=['utc_time']).reset_index()
        times_of_arm = reference_df.utc_time.round(2).tolist()
        times_of_rtk = dropped_df.utc_time.round(2).tolist()
        condition = []
        for rtk_row in range(len(times_of_rtk)):
            rtk_time = times_of_rtk[rtk_row]
            for arm_row in range(len(times_of_arm)):
                arm_time = times_of_arm[arm_row]
                if rtk_time <= arm_time:
                    if rtk_time == arm_time:
                        condition.append(False)
                        times_of_arm = times_of_arm[arm_row:]
                    elif rtk_time < arm_time:
                        condition.append(True)
                    break
                if arm_row == len(times_of_arm)-1:
                    condition.append(True)
        condition = pd.Series(condition)
        drop_ratio = (len(condition[condition == True]) / len(condition) * 100)
        print(' - ' + label + ": %.3f" % drop_ratio + ' % of points were dropped')
        return dropped_df.drop(condition.index[condition == True])

    def concate_arm_and_rtks(self):
        novatel = self.concate_dfs(self.novatel_ref,self.novatel)
        tersus = self.concate_dfs(self.tersus_ref,self.tersus)
        ashtech = self.concate_dfs(self.ashtech_ref,self.ashtech)
        ublox = self.concate_dfs(self.ublox_ref,self.ublox)
        return [novatel,tersus,ashtech,ublox]

    def concate_dfs(self,arm_df,rtk_df):
        arm_df = arm_df.drop(columns='level_0').reset_index()[['utc_time','east','north','cvl_speed','cvl_acc']]
        arm_df = arm_df.rename(columns={"east": "arm_east", "north": "arm_north"})
        rtk_df = rtk_df.reset_index()[['east','north','status']]
        rtk_df = rtk_df.rename(columns={"east": "rtk_east", "north": "rtk_north"})
        arm_rtk_df = pd.concat([arm_df, rtk_df], axis=1)
        arm_rtk_df = arm_rtk_df[['utc_time','cvl_speed','cvl_acc','status','arm_east','arm_north','rtk_east','rtk_north']]
        return arm_rtk_df

    def slice_times(self,slice_times):
        self.novatel = self.novatel[(self.novatel.utc_time > slice_times[0]) & (self.novatel.utc_time < slice_times[1])]
        self.tersus = self.tersus[(self.tersus.utc_time > slice_times[0]) & (self.tersus.utc_time < slice_times[1])]
        self.ashtech = self.ashtech[(self.ashtech.utc_time > slice_times[0]) & (self.ashtech.utc_time < slice_times[1])]
        self.ublox = self.ublox[(self.ublox.utc_time > slice_times[0]) & (self.ublox.utc_time < slice_times[1])]

class Evaluator:

    def __init__(self,rtk_list):
        self.novatel = rtk_list[0]
        self.tersus = rtk_list[1]
        self.ashtech = rtk_list[2]
        self.ublox = rtk_list[3]

# =============================================================================
#  DEFINITIONS
# =============================================================================
dir_rtk = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\RTK\TO_PROCESS"
dir_arm = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\arm_converted_200326"
#dir_arm = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\TO_PROCESS"

output_dir = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\enu"
output_dir = os.path.join(dir_arm,'output')

wgs_ref = [50.07478605085059,14.52025289904692,286.6000000000184]
fixed_height = 235.58

prefix = 'ped'

if prefix == 'auto': slice_times = [57800,61500]
if prefix == 'car': slice_times = [71800,76000]
if prefix == 'ped': slice_times = [0,90000]

# =============================================================================
# MAIN:
# =============================================================================
arm = ArmParser(dir_arm,prefix)
arm.parse_slices()
#arm.slice_times(slice_times)
arm.filter_signal()
arm.get_bad_cicles()
arm.drop_bad_circles()
arm.drop_zero_speed()
arm.drop_zero_acc()
arm.drop_limit_acc()
arm.drop_peaks()

rtk = RtkParser(dir_rtk,fixed_height)
rtk.parse_slices(prefix)
#rtk.slice_times(slice_times)
rtk.drop_points_wo_arm(arm.arm_20hz)
rtk.drop_points_wo_rtk(arm.arm_20hz)
rtk_list = rtk.concate_arm_and_rtks()

evl = Evaluator(rtk_list)

#rtk = []

# =============================================================================
#    PLOTTING:
# =============================================================================
pltr = plot.Plotter(arm, rtk)

#pltr.plot_arm(arm.arm_async,'arm_async','k')
pltr.plot_arm(arm.arm_20hz,'arm_20hz','r')
pltr.plot_marks()

pltr.plot_rtk(rtk.novatel,'novatel',"g")
pltr.plot_rtk(rtk.tersus,'tersus',"y")
pltr.plot_rtk(rtk.ashtech,'ashtech',"b")
pltr.plot_rtk(rtk.ublox,'ublox',"m")
##



# =============================================================================
#
# =============================================================================


#
##
##            rtk_output = rtk[["utc_time","east","north","up","status"]]
##            rtk_output.to_csv(os.path.join(output_dir, file.split('\\')[-1][:-4]+'_enu.csv'))
#

### =============================================================================
### DEWESOFT:
### =============================================================================
##dewsoft_files = os.listdir(dir_dewesoft)
##dewesoft_csvs = [i for i in dewsoft_files if 'csv' in i]
##dewesoft_csvs_paths = [os.path.join(dir_dewesoft, name) for name in dewesoft_csvs]
##
###header = ['lat', 'lon', 'height', 'utc_time', 'east_row', 'north_row', 'up_row', 'utc_time_2']
###for file in [novatel_csvs_paths[7]]:
##for file in dewesoft_csvs_paths:
###    dewesoft = pd.read_csv(file, sep=',', names=header , engine='python')#.values.tolist()
##    dewesoft = pd.read_csv(file, sep=';', engine='python')#.values.tolist()
##
###    dewesoft["utc_time"] = dewesoft.utc_time % 86400
##
###    dewesoft.insert(len(dewesoft.count()), 'lat_in_rad', dewesoft.lat*np.pi/180, allow_duplicates=False)
###    dewesoft.insert(len(dewesoft.count()), 'lon_in_rad', dewesoft.lon*np.pi/180, allow_duplicates=False)
###
###    xyz = transpos.wgs2xyz(dewesoft[['lat_in_rad','lon_in_rad','height']].values)
###    enu = transpos.xyz2enu(xyz,wgs_ref)
###
###    dewesoft["east"], dewesoft["north"], dewesoft["up"] = enu.T[0], enu.T[1], enu.T[2]
##    dewesoft = dewesoft[["utc_time","lat","lon","height","east","north","up"]]
##    print(' - dewesoft loading done, ' + str(len(dewesoft)) + ' points')
##
##    dewesoft["east"] = dewesoft.east - 0.59
##    dewesoft["north"] = dewesoft.north - 0.588
##
##    filename = file.split("\\")[-1][:-4]
##    plot.plot_EN(dewesoft, filename, "b")
##    plot.plot_utcE(dewesoft, filename, "b")
#