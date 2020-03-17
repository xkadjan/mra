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
        self.ENC_resolution = 2500 # [-]
        self.enc_tol = 3           # [-]
        self.badhall_tol = 3       # [s]
        self.seconds_to_drop = 100 # [s]
        
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

    def get_files(self,dir,signal,prefix):
        files = os.listdir(dir)
        csvs = [i for i in files if '.csv' in i]
        csvs = [i for i in csvs if not i.find(signal)]
        csvs_paths = [os.path.join(dir, name) for name in csvs]
        csvs_paths = [i for i in csvs_paths if prefix in i]
        return csvs_paths
     
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
        print(' - arm 20hz loading done, ' + str(len(arm)) + ' points')
#            arm_output.to_csv(os.path.join(output_dir, file.split('\\')[-1][:-4]+'_enu.csv'))

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
                    circle_bad.append([row,arm_halls_enc[row],error,arm_halls_time[row-1],arm_halls_time[row]])
                else:
                    circle_good.append([row,arm_halls_enc[row],error,arm_halls_time[row-1],arm_halls_time[row]])
            else:
                circle_good.append([row,arm_halls_enc[row],-1,arm_halls_time[row-1],arm_halls_time[row]])        
        self.circle_good = pd.DataFrame(circle_good,columns=["row","enc","error","time_start","time_end"])
        self.circle_bad = pd.DataFrame(circle_bad,columns=["row","enc","error","time_start","time_end"])
        
        print('circle_good: ' + str(len(self.circle_good)))
        print('circle_bad: ' + str(len(self.circle_bad)))
        
        self.drop_last_badhalls()
        
    def drop_last_badhalls(self):       
        badhalls_index = self.arm_badhalls.index.astype(int).tolist()
        badhalls_index = [i - 1 for i,x in enumerate(badhalls_index) if x == 0]
        badhalls_last = self.arm_badhalls.iloc[badhalls_index]
        gap_after_last_good = self.circle_good[self.circle_good.error == -1]

        for i in range(len(badhalls_last)):
            if badhalls_last.utc_time.iloc[i] > gap_after_last_good.time_start.iloc[i] + self.badhall_tol: 
                last_to_drop = gap_after_last_good.iloc[i]
                last_to_drop.time_end = last_to_drop.time_start + self.seconds_to_drop
                self.circle_bad = self.circle_bad.append(last_to_drop)
        self.circle_bad = self.circle_bad.reset_index()
    
    def add_meas_num(self,arm_halls):
        measurement, meas = 0, []
        for i,hall in arm_halls.iterrows():
            if hall['index'] == 0:
                print(hall.hall_index)
                measurement += 1
            meas.append(measurement)
        arm_halls.insert(2,'meas',meas)
        return arm_halls


class RtkParser:
    
    def __init__(self,dir_rtk,fixed_height):
        self.fixed_height = fixed_height
        self.dir_rtk = dir_rtk
        self.rtk_folders = os.listdir(dir_rtk)  
        self.novatel = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.tersus = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.ashtech = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.ublox = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])       
        
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
                rtk = pd.DataFrame(transpos.get_points(sentences)).astype(float)
                rtk.columns = ['utc_time','lat','lon','status']
                rtk["height"] = self.fixed_height              
                rtk.insert(len(rtk.count()), 'lat_in_rad', rtk.lat*np.pi/180, allow_duplicates=False)
                rtk.insert(len(rtk.count()), 'lon_in_rad', rtk.lon*np.pi/180, allow_duplicates=False)               
                xyz = transpos.wgs2xyz(rtk[['lat_in_rad','lon_in_rad','height']].values)
                enu = transpos.xyz2enu(xyz,wgs_ref)               
                rtk["east"], rtk["north"], rtk["up"] = enu.T[0], enu.T[1], enu.T[2]
                rtk = rtk[["utc_time","lat","lon","height","east","north","up",'status']]                              
                print(' - rtk loading done, ' + str(len(rtk)) + ' points')               
                return rtk
                      
# =============================================================================
#  DEFINITIONS       
# =============================================================================
dir_rtk = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\RTK\TO_PROCESS"
dir_arm = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\arm_converted_200309"
#dir_arm = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\TO_PROCESS"

output_dir = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\enu"
output_dir = os.path.join(dir_arm,'output')

wgs_ref = [50.07478605085059,14.52025289904692,286.6000000000184]
fixed_height = 235.58

prefix = 'auto'        
# =============================================================================
# MAIN:
# =============================================================================
arm = ArmParser(dir_arm,prefix)
arm.parse_slices()
arm.get_bad_cicles()

rtk = RtkParser(dir_rtk,fixed_height)
rtk.parse_slices(prefix) 
#rtk = []

# =============================================================================
#    PLOTTING:
# =============================================================================
pltr = plot.Plotter(arm, rtk)

pltr.plot_arm(arm.arm_async,'arm_async','k')
pltr.plot_arm(arm.arm_20hz,'arm_20hz','r')
pltr.plot_marks()

#pltr.plot_rtk(rtk.novatel,'novatel',"g")
#pltr.plot_rtk(rtk.tersus,'tersus',"y")
#pltr.plot_rtk(rtk.ashtech,'ashtech',"b")
#pltr.plot_rtk(rtk.ublox,'ublox',"m")
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