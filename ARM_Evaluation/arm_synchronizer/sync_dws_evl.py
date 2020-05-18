# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:18:46 2020

@author: xkadj
"""
import os
import pandas as pd
import numpy as np

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
            for speed in range(len(self.labels_speed)):
                filename = 'dewesoft_speed_from' + str(self.bounds_speed[speed]) + 'to' + str(self.bounds_speed[speed]) + 'mps.csv'
                self.dewesoft_by_speed[speed].to_csv(os.path.join(csv_dir, filename))
            for acc in range(len(self.labels_acc)):
                filename = 'dewesoft_acc_from' + str(self.bounds_acc[acc]) + 'to' + str(self.bounds_acc[acc]) + 'mps-1.csv'
                self.dewesoft_by_acc[acc].to_csv(os.path.join(csv_dir, filename))
        self.results_dewesoft.to_csv(os.path.join(csv_dir, 'results_dewesoft.csv'))
