# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:06:22 2020

@author: xkadj
"""
import os
import pandas as pd
import numpy as np

import sync_transpositions as transpos

class RtkParser:

    def __init__(self,args):
        self.args = args
        self.wgs_ref = args.wgs_ref
        self.dir_rtk = args.dir_rtk
        self.rtk_folders = os.listdir(self.dir_rtk)
        self.novatel = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.tersus = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.ashtech = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.ublox = pd.DataFrame(columns=["utc_time","lat","lon","height","east","north","up",'status'])
        self.novatel_ref = pd.DataFrame()
        self.tersus_ref = pd.DataFrame()
        self.ashtech_ref = pd.DataFrame()
        self.ublox_ref = pd.DataFrame()

    def parse_slices(self):

        if self.args.prefix == 'all':
            folders = self.rtk_folders
        else:
            folders = [i for i in self.rtk_folders if self.args.prefix in i]

        for folder in folders:
            rtk_txts_paths = self.load_files(folder,'novatel')
            self.novatel = self.novatel.append(self.parse_rtk(rtk_txts_paths))

        for folder in folders:
            rtk_txts_paths = self.load_files(folder,'tersus')
            self.tersus = self.tersus.append(self.parse_rtk(rtk_txts_paths))

        for folder in folders:
            rtk_txts_paths = self.load_files(folder,'ashtech')
            self.ashtech = self.ashtech.append(self.parse_rtk(rtk_txts_paths))

        for folder in folders:
            rtk_txts_paths = self.load_files(folder,'ublox')
            self.ublox = self.ublox.append(self.parse_rtk(rtk_txts_paths))

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
                rtk["height"] = self.wgs_ref[2]
                rtk.insert(len(rtk.count()), 'lat_in_rad', rtk.lat*np.pi/180, allow_duplicates=False)
                rtk.insert(len(rtk.count()), 'lon_in_rad', rtk.lon*np.pi/180, allow_duplicates=False)
                xyz = transpos.wgs2xyz(rtk[['lat_in_rad','lon_in_rad','height']].values)
                enu = transpos.xyz2enu(xyz,self.wgs_ref)
                rtk["east"], rtk["north"], rtk["up"] = enu.T[0], enu.T[1], enu.T[2]
                rtk["raw_speed"] = ((rtk.east.diff().pow(2) + rtk.north.diff().pow(2)).pow(1/2) / rtk.utc_time.diff()).fillna(0)
                rtk["raw_acc"] = (rtk.raw_speed.diff() / rtk.utc_time.diff()).fillna(0)
                rtk["cvl_speed"] = self.convolve_filter(rtk.raw_speed,7)
                rtk["cvl_acc"] = self.convolve_filter(rtk.raw_acc,33)
                rtk = rtk[["utc_time","lat","lon","height","east","north","up",'status',"raw_speed","raw_acc","cvl_speed","cvl_acc"]]
                return rtk
            
    def convolve_filter(self,signal,kernel_size):
        kernel = (np.ones(kernel_size)/kernel_size).tolist()
        cvl = np.zeros(len(signal))
        cvl[int((kernel_size-kernel_size%2)/2):-int((kernel_size-kernel_size%2)/2)] = np.convolve(signal, kernel, mode='valid')
        return cvl
    
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
