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

class Evaluator:

    def __init__(self):
        self.bounds_speed = [0,1,2.5,4,5.5,7,8.5,10]
        self.bounds_acc = [-4,-3,-2,-1,0,1,2]
        self.labels_speed = self.get_labels(self.bounds_speed,'m/s')
        self.labels_acc = self.get_labels(self.bounds_acc,'m/s²')
        self.labels_rtk = ['dewesoft']
        self.results = pd.DataFrame()
        self.results_dewesoft = pd.DataFrame()

    def get_labels(self,bounds,unit):
        labels = []
        for box in range(1,len(bounds)):
            labels.append(str(bounds[box-1]) + ' - ' + str(bounds[box]) + ' ' + unit)
        return labels

    def get_deviations(self,rtk_list):
        self.dewesoft = self.calculate_deviations(rtk_list[0])

    def calculate_deviations(self,df):
        df['diff_east'] = df.rtk_east - df.arm_east
        df['diff_north'] = df.rtk_north - df.arm_north
        df['deviation'] = np.sqrt(df['diff_east']**2 + df['diff_north']**2)
        df['azimuth'] = np.rad2deg(np.arctan(df['diff_east']/df['diff_north']))
        return df.drop(columns=[col for col in df.columns.tolist() if "Unnamed" in col])

    def filter_fix(self):
        self.dewesoft = self.dewesoft[self.dewesoft.status == 7]

    def filter_sigma(self):
        self.dewesoft = self.dewesoft[self.dewesoft.deviation < (3 * self.get_precision(self.dewesoft))]

    def get_make_boxes(self):
        self.dewesoft_by_speed = self.get_boxes(self.dewesoft,'cvl_speed',self.bounds_speed,'dewesoft')
        self.dewesoft_by_acc = self.get_boxes(self.dewesoft,'cvl_acc',self.bounds_acc,'dewesoft')

    def get_boxes(self,rtk,filter_by,bounds,label):
        boxes = []
        for box in range(1,len(bounds)):
            df = rtk[(rtk[filter_by] > bounds[box-1]) & (rtk[filter_by] <= bounds[box])]
            boxes.append(df)
            print(label + ' by ' + filter_by + ': ' + str(bounds[box-1]) + ' - ' + str(bounds[box]) + '.....' + str(len(df)))
        return boxes

    def get_results(self,only_fix):
        rtks = [self.dewesoft]
        self.evaluate(rtks,"WHOLE",only_fix)

        for speed in range(len(self.labels_speed)):
            rtks = [self.dewesoft_by_speed[speed]]
            self.evaluate(rtks,self.labels_speed[speed],only_fix)

        for acc in range(len(self.labels_acc)):
            rtks = [self.dewesoft_by_acc[acc]]
            self.evaluate(rtks,self.labels_acc[acc],only_fix)

        self.get_rtks_results()

    def evaluate(self,rtks,label,only_fix):
        results = pd.DataFrame(index=self.labels_rtk)
        samples,µ_err,µ_err_east,µ_err_north,σ_err,RMS_err,CEP_err,SSR_err = [],[],[],[],[],[],[],[]

        for rtk in rtks: samples.append(self.get_samples(rtk))
        for rtk in rtks: µ_err.append(self.get_accuracy(rtk.deviation))
        for rtk in rtks: µ_err_east.append(self.get_accuracy(rtk.diff_east))
        for rtk in rtks: µ_err_north.append(self.get_accuracy(rtk.diff_north))
        for rtk in rtks: σ_err.append(self.get_precision(rtk))
        for rtk in rtks: RMS_err.append(self.get_rms(rtk))
        for rtk in rtks: CEP_err.append(self.get_cep(rtk))
        if not only_fix:
            for rtk in rtks: SSR_err.append(self.get_ssr(rtk))

        results.insert(results.columns.size,'set',label)
        results.insert(results.columns.size,'samples',samples)
        results.insert(results.columns.size,'µ_err',µ_err)
        results.insert(results.columns.size,'µ_err_east',µ_err)
        results.insert(results.columns.size,'µ_err_north',µ_err)
        results.insert(results.columns.size,'σ_err',σ_err)
        results.insert(results.columns.size,'RMS_err',RMS_err)
#        results.insert(results.columns.size,'CEP_err',CEP_err)
        if not only_fix:
            results.insert(results.columns.size,'SSR_err',SSR_err)

        self.results = self.results.append(results)
        print('-'*60 + '\n' + str(label) + ': \n', results)

    def get_samples(self,rtk):
        # Samples (samples) – number of samples
        return len(rtk)

    def get_accuracy (self,rtk):
        # Accuracy (µerr) – sample mean of deviations from reference point (error offset)
        return float(rtk.mean())

    def get_precision(self,rtk):
        # Precision (σerr) – standard deviation of error (stability of positioning)
        return float(np.sqrt(rtk.deviation.std()))

    def get_rms(self,rtk):
        # RMS error (RMSerr) – value specified by the manufacturer (metric emphasizing large errors)
        return float(np.sqrt(rtk.deviation.pow(2).mean()))

    def get_cep(self,rtk):
        # CEP
        return 0

    def get_ssr(self,rtk):
        # System status ratio (SSR) – ability of the system to solve the problem of ambiguity integer phases
        if len(rtk) == 0:
            SSR = '-'
        else:
            SSR = float(len(rtk.status[rtk.status == 4])/len(rtk)*100)
        return SSR

    def get_rtks_results(self):
        self.results_dewesoft = self.results[self.results.index == 'dewesoft']

    def csv_print(self,csv_dir,new_preproccess):
        if new_preproccess:
            self.dewesoft.to_csv(os.path.join(csv_dir, 'dewesoft_whole.csv'))
        self.results_dewesoft.to_csv(os.path.join(csv_dir, 'results_dewesoft.csv'))
