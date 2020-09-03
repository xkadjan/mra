# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 10:25:24 2019

@author: xkadj
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sb
import os

class Plotter:
#    ax: https://matplotlib.org/api/axes_api.html
    def __init__(self,new_preproccess,only_fix,csv_dir):
        self.only_fix = only_fix
        self.csv_dir = csv_dir
        if new_preproccess:
            self.fig_1, self.ax_1 = plt.subplots(num=301,figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r')
            self.fig_2, self.ax_2 = plt.subplots(num=302,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
            self.fig_3, self.ax_3 = plt.subplots(num=303,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
            self.fig_4, self.ax_4 = plt.subplots(num=304,figsize=[12.2, 5], dpi=100, facecolor='w', edgecolor='r')

        self.fig_41, self.ax_41 = plt.subplots(num=401,figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r')
        self.fig_42, self.ax_42 = plt.subplots(num=402,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
        self.fig_43, self.ax_43 = plt.subplots(num=403,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')

        self.count_hist = 500

    def plot_arm(self,data,signal_name,color):
        self.plot_EN(data, signal_name, color)
        self.plot_utcE(data, signal_name, color)
        self.plot_utcSpeed(data, signal_name, color)

    def plot_rtk(self,rtk,signal_name,color):
        self.plot_EN(rtk, signal_name, color)
        self.plot_utcE(rtk, signal_name, color)
        self.plot_utcStatus(rtk, signal_name, color)

    def plot_devs(self,rtk,signal_name,color):
        self.plot_devs_EN(rtk, signal_name, color)
        self.plot_devs_utcE(rtk, signal_name, color)
        self.plot_devs_utcN(rtk, signal_name, color)

    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def plot_marks(self,arm):
        bold = 1
        self.plot_MARK(self.fig_2, self.ax_2, arm.arm_badhalls,'arm_badhalls','y',bold,[arm.arm_20hz.east.min()-0.5,arm.arm_20hz.east.max()+0.5],'arm_badhall')
        # self.plot_MARK(self.fig_4, self.ax_4, arm.arm_badhalls,'arm_badhalls','y',bold,[-10,10],'arm_badhall')

        self.plot_MARK(self.fig_2, self.ax_2, arm.arm_halls,'arm_halls','k',bold,[arm.arm_20hz.east.min()-0.5,arm.arm_20hz.east.max()+0.5],'arm_hall')
        self.plot_MARK(self.fig_4, self.ax_4, arm.arm_halls,'arm_halls','k',bold,[-10,10],'arm_hall')

        if len(arm.arm_peaks): self.plot_MARK(self.fig_2, self.ax_2, arm.arm_peaks,'arm_peaks','r',bold+1,[arm.arm_20hz.east.min()-1,arm.arm_20hz.east.max()+1],'arm_peak')
        if len(arm.arm_peaks): self.plot_MARK(self.fig_4, self.ax_4, arm.arm_peaks,'arm_peaks','r',bold+1,arm.arm_peaks.raw_speed_diff,'arm_peak')

        self.plot_bad_circles(arm.circle_bad)

    def plot_MARK(self,fig, ax, marks, mark_type, rcv_color, bold, bounds, label):
        if len(bounds) == 2:
            ax.plot([marks.utc_time, marks.utc_time], [bounds[0],bounds[1]], rcv_color, linestyle='--', linewidth=bold, alpha=0.6, label=label)
        else:
            ax.plot(marks.utc_time, np.zeros(len(marks.utc_time)), rcv_color, linewidth=0, marker='o', markersize=5, alpha=0.8, label=label)
        fig.show()

    def plot_bad_circles(self,circle_bad):
        for circle in range(len(circle_bad)):
            rect = patches.Rectangle((circle_bad.time_start[circle],-3.5),circle_bad.time_end[circle]-circle_bad.time_start[circle],
                                     7,linewidth=None,color='r',alpha=0.2)#,facecolor='none')
            self.ax_2.add_patch(rect)
            self.fig_2.show()

        for circle in range(len(circle_bad)):
            rect = patches.Rectangle((circle_bad.time_start[circle],-10),circle_bad.time_end[circle]-circle_bad.time_start[circle],
                                     20,linewidth=None,color='r',alpha=0.4)#,facecolor='none')
            self.ax_4.add_patch(rect)
            self.fig_4.show()

    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def plot_EN(self,points_DF, rcv_name, rcv_color):
        self.ax_1.plot(points_DF.east, points_DF.north, rcv_color, marker=".", linewidth=0.1, alpha=0.2,label=rcv_name)
        self.ax_1.set_title('Map of positions', size=12, loc='left')
        self.ax_1.set_xlabel('distance to North [m]',size=10)
        self.ax_1.set_ylabel('distance to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_1.minorticks_on()
        self.ax_1.tick_params(axis='both',which='major',length=10,width=1,labelsize=10)
        self.ax_1.set_aspect('equal', 'datalim')
    #    plt.style.use('seaborn-paper')
        self.ax_1.grid(True)
        self.ax_1.legend(loc=1)
        self.fig_1.tight_layout()
        self.fig_1.set_facecolor('whitesmoke')
        self.fig_1.show()

    def plot_utcE(self,points_DF, rcv_name, rcv_color):
        self.ax_2.plot(points_DF.utc_time, points_DF.east, rcv_color, marker=".", linewidth=1, markersize=4, alpha=0.4, label=rcv_name)
        self.ax_2.set_title('Positions in time', size=12, loc='left')
        self.ax_2.set_xlabel('time of day [s]',size=10)
        self.ax_2.set_ylabel('distance to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_2.minorticks_on()
        self.ax_2.tick_params(axis='both',which='major',length=10,width=1,labelsize=10)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_2.grid(True)
        self.ax_2.legend(loc=1)
        self.fig_2.tight_layout()
        self.fig_2.set_facecolor('whitesmoke')
        self.fig_2.show()
        custom_lines = [Line2D([0], [0], color='b', marker=".", linewidth=0.3, alpha=1, markersize=1.5),
                        Line2D([0], [0], color='r', marker=".", linewidth=0.3, alpha=1, markersize=1.5),
                        Line2D([0], [0], color='y', marker='|', linestyle='--', linewidth=1, alpha=0.6),
                        Line2D([0], [0], color='k', marker='|', linestyle='--', linewidth=1, alpha=0.6),
                        patches.Rectangle((0,0),1,1, color='r', alpha=0.2)]
        self.ax_2.legend(custom_lines, ['dewesoft', 'arm','hall_bad','hall_correct','removed_period'],loc=1)

    def plot_utcStatus(self,points_DF, rcv_name, rcv_color):
        self.ax_3.plot(points_DF.utc_time, points_DF.status, rcv_color, marker="|", linewidth=0.2, alpha=0.4, label=rcv_name)
#        self.ax_2.plot(points_DF.utc_time, points_DF.status, rcv_color, marker="|", linewidth=0.2, alpha=0.4, label=rcv_name)
        self.ax_3.set_title('RTK correction in time', size=12, loc='left')
        self.ax_3.set_xlabel('time of day [s]',size=10)
        self.ax_3.set_ylabel('RTK status [-]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_3.minorticks_on()
        self.ax_3.tick_params(axis='both',which='major',length=10,width=1,labelsize=10)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_3.grid(True)
        self.ax_3.legend(loc=1)
        self.fig_3.tight_layout()
    #    plt.axis([points_DF.utc_time.min()-100, points_DF.utc_time.max()+100, -1, 1])
        self.fig_3.set_facecolor('whitesmoke')
        self.fig_3.show()

    def plot_utcSpeed(self,points_DF, rcv_name, rcv_color):
        self.ax_4.plot(points_DF.utc_time, points_DF.raw_speed, 'darksalmon', marker=".", linewidth=1, alpha=1, markersize=2, label='raw_speed[m/s]')
        self.ax_4.plot(points_DF.utc_time, points_DF.raw_acc, 'skyblue', marker=".", linewidth=1, alpha=1, markersize=2, label='raw_acc[m/s-2]')
        self.ax_4.plot(points_DF.utc_time, points_DF.cvl_speed, '-r', marker=".", linewidth=1, alpha=1, markersize=2, label='filtered_speed[m/s]')
        self.ax_4.plot(points_DF.utc_time, points_DF.cvl_acc, '-b', marker=".", linewidth=1, alpha=1, markersize=2, label='filtered_acc[m/s-2]')
        self.ax_4.set_title('Speed and acceleration in time', size=14, loc='left')
        self.ax_4.set_xlabel('time of day [s]',size=12)
        self.ax_4.set_ylabel('speed [mps] / acceleration [mps-2]',size=12)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_4.minorticks_on()
        self.ax_4.tick_params(axis='both',which='major',length=10,width=1,labelsize=12)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_4.grid(True)
        self.ax_4.legend(loc=1)
        self.ax_4.set_ylim([-10,10])
        self.ax_4.set_xlim([60585,60655])

        self.fig_4.tight_layout()
    #    plt.axis([points_DF.utc_time.min()-100, points_DF.utc_time.max()+100, -6, 10])
        self.fig_4.set_facecolor('whitesmoke')
        self.fig_4.show()
        custom_lines = [Line2D([0], [0], color='darksalmon', marker=".", linewidth=1, alpha=1, markersize=2),
                        Line2D([0], [0], color='skyblue', marker=".", linewidth=1, alpha=1, markersize=2),
                        Line2D([0], [0], color='r', marker=".", linewidth=1, alpha=1, markersize=2),
                        Line2D([0], [0], color='b', marker=".", linewidth=1, alpha=1, markersize=2),
                        # Line2D([0], [0], color='y', marker='|', linestyle='--', linewidth=1, alpha=0.6),
                        Line2D([0], [0], color='k', marker='|', linestyle='--', linewidth=1, alpha=0.6)]#,
                        # patches.Rectangle((0,0),1,1, color='r', alpha=0.4)]
        # self.ax_4.legend(custom_lines, ['raw_speed','raw_acc', 'cvl_speed', 'cvl_acc','hall_bad','hall_correct','removed_period'],loc=1)
        self.ax_4.legend(custom_lines, [r'$v_{r}$',r'$a_{r}$', r'$v_{f}$', r'$a_{f}$',r'$t_{h}$',],loc=1)

    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def plot_devs_EN(self,points_DF, rcv_name, rcv_color):
        self.ax_41.plot(points_DF.diff_east, points_DF.diff_north, rcv_color, marker=".", linewidth=0.1, alpha=0.4)
        self.ax_41.set_title('Map of horizontal positions', size=12, loc='left')
        self.ax_41.set_xlabel('distance to North [m]',size=10)
        self.ax_41.set_ylabel('distance to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_41.minorticks_on()
        self.ax_41.tick_params(axis='both',which='major',length=10,width=1,labelsize=10)
        self.ax_41.set_aspect('equal', 'datalim')
    #    plt.style.use('seaborn-paper')
        self.ax_41.grid(True)
        self.ax_41.legend(loc=1)
        self.fig_41.tight_layout()
        self.fig_41.set_facecolor('whitesmoke')
        self.fig_41.show()

    def plot_devs_utcE(self,points_DF, rcv_name, rcv_color):
        self.ax_42.plot(points_DF.utc_time, points_DF.diff_east, rcv_color, marker=".", linewidth=1, markersize=4, alpha=0.4, label=rcv_name)
        self.ax_42.set_title('Deviation in time', size=12, loc='left')
        self.ax_42.set_xlabel('time of day [s]',size=10)
        self.ax_42.set_ylabel('deviation to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_42.minorticks_on()
        self.ax_42.tick_params(axis='both',which='major',length=10,width=1,labelsize=10)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_42.grid(True)
        self.ax_42.legend(loc=1)
        self.fig_42.tight_layout()
        self.fig_42.set_facecolor('whitesmoke')
        self.fig_42.show()

    def plot_devs_utcN(self,points_DF, rcv_name, rcv_color):
        self.ax_43.plot(points_DF.utc_time, points_DF.diff_north, rcv_color, marker=".", linewidth=1, markersize=4, alpha=0.4, label=rcv_name)
        self.ax_43.set_title('Deviation in time', size=12, loc='left')
        self.ax_43.set_xlabel('time of day [s]',size=10)
        self.ax_43.set_ylabel('deviation to North [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_43.minorticks_on()
        self.ax_43.tick_params(axis='both',which='major',length=10,width=1,labelsize=10)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_43.grid(True)
        self.ax_43.legend(loc=1)
        self.fig_43.tight_layout()
        self.fig_43.set_facecolor('whitesmoke')
        self.fig_43.show()

    def plot_hist(self,rtk,label,results):
        # definitions for the axes
        x,y = rtk.diff_north, rtk.diff_east
        left, width = 0.1, 0.75
        bottom, height = 0.07, 0.72
        spacing = 0.005
        # bins = bins#200
        # max_hist = max_hist
        if self.only_fix:
            bins = 1000
            max_hist = 7500
            lim = 0.6
            lim_xy = 0.6
        else:
            if ('Novatel' in label) or ('Tersus' in label):
                bins = 1500
                max_hist = 7500
                lim = 1.5
                lim_xy = 1.5
            else:
                bins = 6500
                max_hist = 7500
                lim = 10
                lim_xy = 10

        color = 'w'

        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom + height + spacing, width, 0.1]
        rect_histy = [left + width + spacing, bottom, 0.1, height]

        # start with a rectangular Figure
        fig = plt.figure(num=self.count_hist,figsize=(8, 8),facecolor='whitesmoke', edgecolor='r')
        self.count_hist += 1
#        fig.show()

        # 2D hist
        ax_1 = plt.axes(rect_scatter)
        ax_1.hist2d(x, y, bins=bins, range=[[-lim_xy,lim_xy],[-lim_xy,lim_xy]], cmap=plt.cm.gist_heat,norm=LogNorm(),alpha=1)
        ax_1.set_xlabel('deviation to East [m]',size=14)
        ax_1.set_ylabel('deviation to North [m]',size=14)
        ax_1.set_xlim([-lim,lim])
        ax_1.set_ylim([-lim,lim])
        ax_1.minorticks_on()
        ax_1.tick_params(axis='both',which='major',length=5,width=1,labelsize=0)
        ax_1.set_aspect('equal', 'datalim')
        ax_1.grid(True)

        # Hist x
        ax_histx = plt.axes(rect_histx)
        ax_histx.hist(x, bins=bins, color='k', range=[-lim_xy,lim_xy])
        #ax_histx.set_ylabel('Number of \nsamles [-]',size=10)
        ax_histx.set_ylim([0,max_hist])
        ax_histx.set_xlim(ax_1.get_xlim())
        # ax_histx.set_xlim(lim)
        ax_histx.minorticks_on()
        ax_histx.tick_params(axis='y',which='major',length=10,width=1,labelsize=14)
        ax_histx.tick_params(axis='x',which='major',length=10,width=1,labelsize=14)
        ax_histx.grid(True)

        # Hist y
        ax_histy = plt.axes(rect_histy)
        ax_histy.hist(y, bins=bins, color='k', range=[-lim_xy,lim_xy], orientation='horizontal')
        #ax_histy.set_xlabel('Number \n    [-]',size=10)
        ax_histy.set_xlim([0,max_hist])
        ax_histy.set_ylim(ax_1.get_ylim())
        # ax_histy.set_ylim(lim)
        ax_histy.minorticks_on()
        ax_histy.tick_params(axis='y',which='major',length=10,width=1,labelsize=14)
        ax_histy.tick_params(axis='x',which='major',length=10,width=1,labelsize=14)
        ax_histy.grid(True)

        #plt.tight_layout()
        ax_1.set_facecolor(color)
        ax_histx.set_facecolor(color)
        ax_histy.set_facecolor(color)


        # title = 'Horizontal positions deviations\n' + label#.split(' - ')[1]
        title = label
        ax_histx.set_title(title, size=16, loc='left')
        plt.title('Samples\n[-]', size=14, loc='left')
        # plt.show()
        fig.savefig(os.path.join(self.csv_dir, 'position_onlyfix-' + str(self.only_fix) + '_' + label + '.jpg'))

    def plot_hist_dev(self,dev,label,results,measurement):
        if self.only_fix:
            bins = 2000
            xmax = 5
        else:
            bins = 2000
            xmax = 40
        fig, ax = plt.subplots(figsize=[10, 3], dpi=100, facecolor='w', edgecolor='r')
        ax.hist(dev, bins=bins, range=[0,xmax], density =True, color='C7')
        # title = 'Density of horizontal deviations from MRA - ' + label
        title = label
        # title = title + '\n µ_err = ' + '%.2f'%(results['µ_err']*100) + ' cm'
        # title = title + '; s_err = ' + '%.2f'%(results['s_err']*100) + ' cm'
        # title = title + '; RMS_err = ' + '%.2f'%(results['RMS_err']*100) + ' cm'
        # ax.set_title(title, size=14, loc='left')
        ax.set_title(label + ' - ' + measurement, size=14, loc='left')
        ax.plot([results['µ_err'],results['µ_err']],[0,35],color='y')
        ax.plot([results['s_err'],results['s_err']],[0,35],color='g')
        ax.plot([results['RMS_err'],results['RMS_err']],[0,35],color='b')
        ax.set_xlabel('deviation [m]',size=12)
        ax.set_ylabel('density [%]',size=12)
        if self.only_fix:
            ax.set_xlim([0,0.7])
            ax.set_ylim([0,35])
            # ax.set_ylim([0.001,100])
            # ax.set_yscale("log",basey=10,subsy=[2,3,4,5,6,7,8,9])
        else:
            ax.set_xlim([0.001,100])
            ax.set_xscale("log",basex=10,subsx=[2,3,4,5,6,7,8,9])
            ax.set_ylim([0.001,100])
            ax.set_yscale("log",basey=10,subsy=[2,3,4,5,6,7,8,9])
            ax.set_yticks((0.001,0.01,0.1,1,10,100))
            # ax.set_yticklabels([0.001,0.01,0.1,1,10])
        ax.minorticks_on()
        ax.tick_params(axis='y',which='major',length=10,width=1,labelsize=14)
        ax.tick_params(axis='x',which='major',length=10,width=1,labelsize=14)
        ax.grid(True)
        fig.tight_layout()

        custom_lines = [patches.Rectangle((0,0),1,1, color='C7'),
                        Line2D([0], [0], color='y'),
                        Line2D([0], [0], color='g'),
                        Line2D([0], [0], color='b')]
        ax.legend(custom_lines, [r'$density$', r'$µ_{err}$', r'$s_{err}$', r'$RMS_{err}$'], prop={'weight':'bold'}, loc=1)
        # fig.show()
        fig.savefig(os.path.join(self.csv_dir, 'deviation_onlyfix-' + str(self.only_fix) + '_' + label + '.jpg'))

    def plot_correlation(self,x_value,dev,label,x_value_name):
        fig, ax = plt.subplots(figsize=[10, 10], dpi=100, facecolor='w', edgecolor='r')
        ax.scatter(x_value,dev, s=1, color='C7')
        ax.set_title(label + ' - dependence of deviation on ' + x_value_name.split('[')[0], size=10, loc='left')
        ax.set_xlabel(x_value_name,size=10)
        ax.set_ylabel('deviation [m]',size=10)
        ax.minorticks_on()
        ax.tick_params(axis='y',which='major',length=10,width=1,labelsize=10)
        ax.tick_params(axis='x',which='major',length=10,width=1,labelsize=10)
        ax.grid(True)
        fig.tight_layout()

    def plot_pearsoncorr(self,pearsoncorr,label):
        fig, ax = plt.subplots(figsize=[10, 5], dpi=100, facecolor='w', edgecolor='r')
        sb.heatmap(pearsoncorr,
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            cmap='RdBu_r',
            annot=True,
            linewidth=0.5,
            square=False)
        ax.set_title(label + ' - pearsons correlations', size=10, loc='left')
        fig.tight_layout()
        fig.savefig(os.path.join(self.csv_dir, 'pearson_onlyfix-' + str(self.only_fix) + '_' + label + '.jpg'))

    def plot_lmplot(self,data,label,x_value):
        g = sb.lmplot('cvl_' + x_value.split(' ')[0],'deviation',data,scatter_kws={"s": 2, "alpha": 0.3},legend=True)
        g = (g.set_axis_labels(x_value,'deviation [m]')
        .set(xlim=(0, 10), ylim=(0, 0.3),xticks=[0,2,4,6,8,10], yticks=[0,0.05,0.1,0.15])
        .fig.subplots_adjust(wspace=.02))

    def plot_boxplot(self,data,label,mode,measurement):
        if mode == 'status':
            data_1 = np.array(data.deviation[data.status == 4])
            data_2 = np.array(data.deviation[data.status == 5])
            data_3 = np.array(data.deviation[data.status == 2])
        elif mode == 'phase':
            data_1 = np.array(data[0].deviation)
            data_2 = np.array(data[1].deviation)
            data_3 = np.array(data[2].deviation)
        data = [data_1, data_2, data_3]

        fig = plt.figure(figsize =(10, 2),facecolor='w', edgecolor='r',dpi=100)
        ax = fig.add_subplot(111)

        # Creating axes instance
        bp = ax.boxplot(data,vert = False)

        for cap in bp['caps']:
            cap.set(color ='r',
                    linewidth = 1)

        for median in bp['medians']:
            median.set(color ='red',
                        linewidth = 1)

        for flier in bp['fliers']:
            flier.set(marker ='o',
                      markersize = 0.2,
                      color ='k',
                      alpha = 0.2)

        if mode == 'status':
            ax.set_yticklabels(['fix', 'float','gnss'])
        elif mode == 'phase':
            ax.set_yticklabels(['ramp', 'constant speed','deceleration'])
        ax.set_xlabel('deviation [m]',size=12)
        ax.grid(True)

        ax.set_xlim([0.00007,60])
        ax.set_xscale("log",basex=10,subsx=[0,1,2,3,4,5,6,7,8,9])

        # Adding title
        ax.set_title(label + ' - ' + measurement, size=14, loc='left')
        plt.tight_layout()

        # Removing top axes and right axes
        # ticks
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        # show plot
        # plt.show(bp)
        fig.savefig(os.path.join(self.csv_dir, 'deviations-state_' + (measurement) + '_' + mode + '_' + label + '.jpg'))

    def plot_acc_density(self,arm_20hz):
        fig, ax = plt.subplots(figsize=[5,5], dpi=100, facecolor='w', edgecolor='r')
        ax.hist(arm_20hz.cvl_acc, bins=500, range=[arm_20hz.cvl_acc.min(),arm_20hz.cvl_acc.max()], density =True, color='C7')
        title = 'Acceleration density'
        ax.set_title(title, size=14, loc='left')
        ax.set_xlabel('acceleration [m*s-2]',size=12)
        ax.set_ylabel('density [%]',size=12)

        ax.set_xlim([-4,2])
        ax.set_ylim([0.001,10])
        ax.set_yscale("log",basey=10,subsy=[2,3,4,5,6,7,8,9])

        ax.minorticks_on()
        ax.tick_params(axis='y',which='major',length=10,width=1,labelsize=12)
        ax.tick_params(axis='x',which='major',length=10,width=1,labelsize=11)
        ax.grid(True)
        fig.tight_layout()

        fig.savefig(os.path.join(self.csv_dir, 'density-acc+speed.jpg'))

