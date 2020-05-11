# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:58:40 2020

@author: xkadj
"""
import os
import pandas as pd
import numpy as np
import scipy

class ArmParser:

    def __init__(self,dir_arm,prefix):
        self.ENC_resolution = 2500      # [-]
        self.enc_tol = 3                # [-]
        self.badhall_tol = 10           # [s]
        self.speed_drop_tol = 0.1       # [m*s-1]
        self.acc_drop_tol = [0.01,10]   # [m*s-2]
        self.peak_drop_tol = 0.1        # [s]
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
        if not prefix == 'all':
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
        self.arm_20hz = self.arm_20hz.reset_index()

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
        self.last_len_20hz = len(self.arm_20hz)
        print(' - ' + label + ": %.3f" % drop_ratio + ' % of points were dropped')

    def drop_bad_circles(self):
        arm_20hz = self.arm_20hz#.reset_index()
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
        indexes_to_drop = self.arm_20hz.index[abs(self.arm_20hz.raw_acc) < self.acc_drop_tol[0]]
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
            condition = ((self.arm_20hz.utc_time > time - self.peak_drop_tol) & (self.arm_20hz.utc_time < time + self.peak_drop_tol)) | condition
        self.arm_20hz = self.arm_20hz.drop(condition.index[condition == True])
        self.print_drop_ratio('drop_peaks')

    def filter_signal(self):
        self.arm_20hz["cvl_speed"] = self.convolve_filter(self.arm_20hz.raw_speed,7)
        self.arm_20hz["cvl_acc"] = self.convolve_filter(self.arm_20hz.raw_acc,33)
#        self.arm_20hz["cvl_speed"] = self.savitzky_golay_filter(self.arm_20hz.raw_speed)
#        self.arm_20hz["cvl_acc"] = self.savitzky_golay_filter(self.arm_20hz.raw_acc)

    def convolve_filter(self,signal,kernel_size):
        kernel = (np.ones(kernel_size)/kernel_size).tolist()
        cvl = np.zeros(len(signal))
        cvl[int((kernel_size-kernel_size%2)/2):-int((kernel_size-kernel_size%2)/2)] = np.convolve(signal, kernel, mode='valid')
        return cvl

    def savitzky_golay_filter(self,signal):
        return scipy.signal.savgol_filter(signal, 51, 3)

    def slice_times(self,slice_times):
        self.arm_20hz = self.arm_20hz[(self.arm_20hz.utc_time > slice_times[0]) & (self.arm_20hz.utc_time < slice_times[1])]
        self.arm_async = self.arm_async[(self.arm_async.utc_time > slice_times[0]) & (self.arm_async.utc_time < slice_times[1])]
        self.arm_badhalls = self.arm_badhalls[(self.arm_badhalls.utc_time > slice_times[0]) & (self.arm_badhalls.utc_time < slice_times[1])]
        self.arm_halls = self.arm_halls[(self.arm_halls.utc_time > slice_times[0]) & (self.arm_halls.utc_time < slice_times[1])]
        self.arm_peaks = self.arm_peaks[(self.arm_peaks.utc_time > slice_times[0]) & (self.arm_peaks.utc_time < slice_times[1])]