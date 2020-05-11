import os
import pandas as pd
import numpy as np
import sync_transpositions as transpos

class DwsParser:

    def __init__(self,dir_rtk,wgs_ref):
        self.wgs_ref = wgs_ref
        self.dir_rtk = dir_rtk
        self.dewesoft = pd.DataFrame()
        self.dewesoft_ref = pd.DataFrame()

    def parse_slices(self):
        rtk_txts_paths = self.load_files()
        self.parse_rtk(rtk_txts_paths)
        self.dewesoft = self.make_enu(self.dewesoft)

    def load_files(self):
        rtk_files = os.listdir(self.dir_rtk)
        rtk_txts = [i for i in rtk_files if '.csv' in i]
        rtk_txts_paths = [os.path.join(self.dir_rtk, name) for name in rtk_txts]
        return rtk_txts_paths

    def parse_rtk(self,rtk_txts_paths):
        for file in rtk_txts_paths:
            print(' - loaded: ' + file)
            self.dewesoft = self.dewesoft.append(pd.read_csv(file,delimiter=';',index_col=False).drop(['Unnamed: 0'],axis=1))

    def make_enu(self,rtk):
        rtk["height"] = self.wgs_ref[2]
        rtk["utc_time"] = rtk["utc_time"] - 3600
        rtk = rtk.rename(columns={"status_gnss": "status"})
        rtk.insert(len(rtk.count()), 'lat_in_rad', rtk.lat*np.pi/180, allow_duplicates=False)
        rtk.insert(len(rtk.count()), 'lon_in_rad', rtk.lon*np.pi/180, allow_duplicates=False)
        xyz = transpos.wgs2xyz(rtk[['lat_in_rad','lon_in_rad','height']].values)
        enu = transpos.xyz2enu(xyz,self.wgs_ref)
        rtk["east"], rtk["north"], rtk["up"] = enu.T[0], enu.T[1], enu.T[2]
        rtk = rtk[["utc_time","lat","lon","height","east","north","up",'status']]
        return rtk

    def compensate_offset(self):
        self.dewesoft["east"] = self.dewesoft.east - 0.35
        self.dewesoft["north"] = self.dewesoft.north + 0.94

    def drop_unpaired_points(self,arm_df):
        self.dewesoft = self.drop_according_time(self.dewesoft,arm_df,'dewesoft')
        self.dewesoft_ref = self.drop_according_time(arm_df,self.dewesoft,'dewesoft_ref')

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
        return [self.concate_dfs(self.dewesoft_ref,self.dewesoft)]

    def concate_dfs(self,arm_df,rtk_df):
        arm_df = arm_df.drop(columns='level_0').reset_index()[['utc_time','east','north','cvl_speed','cvl_acc']]
        arm_df = arm_df.rename(columns={"east": "arm_east", "north": "arm_north"})
        rtk_df = rtk_df.reset_index()[['east','north','status']]
        rtk_df = rtk_df.rename(columns={"east": "rtk_east", "north": "rtk_north"})
        arm_rtk_df = pd.concat([arm_df, rtk_df], axis=1)
        arm_rtk_df = arm_rtk_df[['utc_time','cvl_speed','cvl_acc','status','arm_east','arm_north','rtk_east','rtk_north']]
        return arm_rtk_df
