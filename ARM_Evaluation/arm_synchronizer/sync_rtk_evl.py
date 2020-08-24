# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:02:34 2020

@author: xkadj
"""

import os
import pandas as pd
import numpy as np

class Evaluator:

    def __init__(self):
        self.bounds_speed = [0,1,2.5,4,5.5,7,8.5,10]
        # self.bounds_acc = [-4,-3,-2,-1,0,1,2]
        self.bounds_acc = [-4,-0.2,0.4,2]
        self.labels_speed = self.get_labels(self.bounds_speed,'m/s')
        self.labels_acc = self.get_labels(self.bounds_acc,'m/s²')
        self.labels_rtk = ['novatel', 'tersus', 'ashtech', 'ublox']
        self.results = pd.DataFrame()
        self.results_novatel = pd.DataFrame()
        self.results_tersus = pd.DataFrame()
        self.results_ashtech = pd.DataFrame()
        self.results_ublox = pd.DataFrame()

    def get_deviations(self,rtk_list):
        self.novatel = self.calculate_deviations(rtk_list[0])
        self.tersus = self.calculate_deviations(rtk_list[1])
        self.ashtech = self.calculate_deviations(rtk_list[2])
        self.ublox = self.calculate_deviations(rtk_list[3])

        # Make backup
        self.novatel_unsliced = self.novatel
        self.tersus_unsliced = self.tersus
        self.ashtech_unsliced = self.ashtech
        self.ublox_unsliced = self.ublox

    def filter_fix(self):
        self.novatel = self.novatel[self.novatel.status == 4]
        self.tersus = self.tersus[self.tersus.status == 4]
        self.ashtech = self.ashtech[self.ashtech.status == 4]
        self.ublox = self.ublox[self.ublox.status == 4]

    def filter_sigma(self):
        self.novatel = self.make_sigma_filter(self.novatel,3)
        self.tersus = self.make_sigma_filter(self.tersus,3)
        self.ashtech = self.make_sigma_filter(self.ashtech,3)
        self.ublox = self.make_sigma_filter(self.ublox,3)

    def make_sigma_filter(self,rtk,multiplier):
        # n = len(rtk.index)
        # mean = self.get_accuracy(rtk.deviation)


        mean = self.get_accuracy(rtk.deviation)
        std = self.get_sigma(rtk)
        rtk = rtk[rtk.deviation < mean + multiplier * std]
        rtk = rtk[rtk.deviation > mean - multiplier * std]
        return rtk

    def get_make_boxes(self):
        self.novatel_by_speed = self.get_boxes(self.novatel,'cvl_speed',self.bounds_speed,'novatel')
        self.tersus_by_speed = self.get_boxes(self.tersus,'cvl_speed',self.bounds_speed,'tersus')
        self.ashtech_by_speed = self.get_boxes(self.ashtech,'cvl_speed',self.bounds_speed,'ashtech')
        self.ublox_by_speed = self.get_boxes(self.ublox,'cvl_speed',self.bounds_speed,'ublox')

        self.novatel_by_acc = self.get_boxes(self.novatel,'cvl_acc',self.bounds_acc,'novatel')
        self.tersus_by_acc = self.get_boxes(self.tersus,'cvl_acc',self.bounds_acc,'tersus')
        self.ashtech_by_acc = self.get_boxes(self.ashtech,'cvl_acc',self.bounds_acc,'ashtech')
        self.ublox_by_acc = self.get_boxes(self.ublox,'cvl_acc',self.bounds_acc,'ublox')

    def adjust_status(self):
        self.novatel['status'] = self.make_status_adjust(self.novatel['status'].values.astype(int).tolist())
        self.tersus['status'] = self.make_status_adjust(self.tersus['status'].values.astype(int).tolist())
        self.ashtech['status'] = self.make_status_adjust(self.ashtech['status'].values.astype(int).tolist())
        self.ublox['status'] = self.make_status_adjust(self.ublox['status'].values.astype(int).tolist())

    def make_status_adjust(self,old_status_list):
        status_list = []
        for status in old_status_list:
            if status == 4:
                status_list.append(2)
            elif status == 5:
                status_list.append(1)
            else:
                status_list.append(0)
        return status_list

    def calculate_deviations(self,df):
        df['diff_east'] = df.rtk_east - df.arm_east
        df['diff_north'] = df.rtk_north - df.arm_north
        df['deviation'] = np.sqrt(df['diff_east']**2 + df['diff_north']**2)
        df['azimuth'] = np.rad2deg(np.arctan(df['diff_east']/df['diff_north']))
        return df.drop(columns=[col for col in df.columns.tolist() if "Unnamed" in col])

    def get_boxes(self,rtk,filter_by,bounds,label):
        boxes = []
        for box in range(1,len(bounds)):
            df = rtk[(rtk[filter_by] > bounds[box-1]) & (rtk[filter_by] <= bounds[box])]
            boxes.append(df)
            print(label + ' by ' + filter_by + ': ' + str(bounds[box-1]) + ' - ' + str(bounds[box]) + '.....' + str(len(df)))
        return boxes

    def get_labels(self,bounds,unit):
        labels = []
        for box in range(1,len(bounds)):
            labels.append(str(bounds[box-1]) + ' - ' + str(bounds[box]) + ' ' + unit)
        return labels

    def csv_print(self,csv_dir,new_preproccess):
        if new_preproccess:
            self.novatel_unsliced.to_csv(os.path.join(csv_dir, 'novatel_whole.csv'))
            self.tersus_unsliced.to_csv(os.path.join(csv_dir, 'tersus_whole.csv'))
            self.ashtech_unsliced.to_csv(os.path.join(csv_dir, 'ashtech_whole.csv'))
            self.ublox_unsliced.to_csv(os.path.join(csv_dir, 'ublox_whole.csv'))

        self.results_novatel.to_csv(os.path.join(csv_dir, 'results_novatel.csv'))
        self.results_tersus.to_csv(os.path.join(csv_dir, 'results_tersus.csv'))
        self.results_ashtech.to_csv(os.path.join(csv_dir, 'results_ashtech.csv'))
        self.results_ublox.to_csv(os.path.join(csv_dir, 'results_ublox.csv'))

    def csv_load(self,csv_dir):
        labels_rtk = ['novatel_whole.csv','tersus_whole.csv','ashtech_whole.csv','ublox_whole.csv']
        rtk_list = []
        for rtk_name in labels_rtk:
            rtk_list.append(pd.read_csv(os.path.join(csv_dir, rtk_name), sep=',', engine='python'))
        return rtk_list

    def get_results(self,only_fix):
        rtks = [self.novatel,self.tersus,self.ashtech,self.ublox]
        self.evaluate(rtks,"WHOLE",only_fix)

        for speed in range(len(self.labels_speed)):
            rtks = [self.novatel_by_speed[speed],self.tersus_by_speed[speed],self.ashtech_by_speed[speed],self.ublox_by_speed[speed]]
            self.evaluate(rtks,self.labels_speed[speed],only_fix)

        for acc in range(len(self.labels_acc)):
            rtks = [self.novatel_by_acc[acc],self.tersus_by_acc[acc],self.ashtech_by_acc[acc],self.ublox_by_acc[acc]]
            self.evaluate(rtks,self.labels_acc[acc],only_fix)

        self.get_rtks_results()

    def evaluate(self,rtks,label,only_fix):
        results = pd.DataFrame(index=self.labels_rtk)
        samples,µ_err,µ_err_east,µ_err_north,s_err,RMS_err,CEP_err,SSR_err = [],[],[],[],[],[],[],[]

        for rtk in rtks: samples.append(self.get_samples(rtk))
        for rtk in rtks: µ_err.append(self.get_accuracy(rtk.deviation))
        for rtk in rtks: µ_err_east.append(self.get_accuracy(rtk.diff_east))
        for rtk in rtks: µ_err_north.append(self.get_accuracy(rtk.diff_north))
        for rtk in rtks: s_err.append(self.get_precision(rtk))
        for rtk in rtks: RMS_err.append(self.get_rms(rtk))
        for rtk in rtks: CEP_err.append(self.get_cep(rtk))
        if not only_fix:
            for rtk in rtks: SSR_err.append(self.get_ssr(rtk))

        results.insert(results.columns.size,'set',label)
        results.insert(results.columns.size,'samples',samples)
        results.insert(results.columns.size,'µ_err',µ_err)
        results.insert(results.columns.size,'µ_err_east',µ_err)
        results.insert(results.columns.size,'µ_err_north',µ_err)
        results.insert(results.columns.size,'s_err',s_err)
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
        # Precision (serr) – standard deviation of error (stability of positioning)
        return float(np.sqrt(rtk.deviation.std()))
        # return float(rtk.deviation.std() / np.sqrt(len(rtk.deviation)))

    def get_sigma(self,rtk):
        # -
        return float(rtk.deviation.std())

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
        self.results_novatel = self.results[self.results.index == 'novatel']
        self.results_tersus = self.results[self.results.index == 'tersus']
        self.results_ashtech = self.results[self.results.index == 'ashtech']
        self.results_ublox = self.results[self.results.index == 'ublox']

    def get_correlation(self):
        self.pearsoncorr_novatel = self.novatel.corr(method='pearson')
        self.pearsoncorr_tersus = self.tersus.corr(method='pearson')
        self.pearsoncorr_ashtech = self.ashtech.corr(method='pearson')
        self.pearsoncorr_ublox = self.ublox.corr(method='pearson')

    def abs_acc(self):
        self.novatel["cvl_acc"] = self.novatel["cvl_acc"].abs()
        self.tersus["cvl_acc"] = self.tersus["cvl_acc"].abs()
        self.ashtech["cvl_acc"] = self.novatel["cvl_acc"].abs()
        self.ublox["cvl_acc"] = self.ublox["cvl_acc"].abs()
