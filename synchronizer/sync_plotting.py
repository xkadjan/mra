# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 10:25:24 2019

@author: xkadj
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Plotter:
#    ax: https://matplotlib.org/api/axes_api.html
    def __init__(self,new_preproccess):
        if new_preproccess:
            self.fig_1, self.ax_1 = plt.subplots(num=301,figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r')
            self.fig_2, self.ax_2 = plt.subplots(num=302,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
            self.fig_3, self.ax_3 = plt.subplots(num=303,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
            self.fig_4, self.ax_4 = plt.subplots(num=304,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')

        self.fig_41, self.ax_41 = plt.subplots(num=401,figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r')
        self.fig_42, self.ax_42 = plt.subplots(num=402,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
        self.fig_43, self.ax_43 = plt.subplots(num=403,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')

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
        self.plot_MARK(self.fig_2, self.ax_2, arm.arm_badhalls,'arm_badhalls','y',bold,[arm.arm_20hz.east.min()-0.5,arm.arm_20hz.east.max()+0.5])
        self.plot_MARK(self.fig_4, self.ax_4, arm.arm_badhalls,'arm_badhalls','y',bold,[-10,10])

        self.plot_MARK(self.fig_2, self.ax_2, arm.arm_halls,'arm_halls','k',bold,[arm.arm_20hz.east.min()-0.5,arm.arm_20hz.east.max()+0.5])
        self.plot_MARK(self.fig_4, self.ax_4, arm.arm_halls,'arm_halls','k',bold,[-10,10])

        if len(arm.arm_peaks): self.plot_MARK(self.fig_2, self.ax_2, arm.arm_peaks,'arm_peaks','r',bold+1,[arm.arm_20hz.east.min()-1,arm.arm_20hz.east.max()+1])
        if len(arm.arm_peaks): self.plot_MARK(self.fig_4, self.ax_4, arm.arm_peaks,'arm_peaks','r',bold+1,arm.arm_peaks.raw_speed_diff)

        self.plot_bad_circles(arm.circle_bad)

    def plot_MARK(self,fig, ax, marks, mark_type, rcv_color, bold, bounds):
        if len(bounds) == 2:
            ax.plot([marks.utc_time, marks.utc_time], [bounds[0],bounds[1]], rcv_color, linestyle='--', linewidth=bold, alpha=0.6)
        else:
            ax.plot(marks.utc_time, np.zeros(len(marks.utc_time)), rcv_color, linewidth=0, marker='o', markersize=5, alpha=0.8)
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
        self.ax_1.plot(points_DF.east, points_DF.north, rcv_color, marker=".", linewidth=0.1, alpha=0.4)
        self.ax_1.set_title('Map of horizontal positions', size=12, loc='left')
        self.ax_1.set_xlabel('distance to North [m]',size=10)
        self.ax_1.set_ylabel('distance to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_1.minorticks_on()
        self.ax_1.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
        self.ax_1.set_aspect('equal', 'datalim')
    #    plt.style.use('seaborn-paper')
        self.ax_1.grid(True)
        self.ax_1.legend(loc=1)
        self.fig_1.tight_layout()
        self.fig_1.set_facecolor('whitesmoke')
        self.fig_1.show()

    def plot_utcE(self,points_DF, rcv_name, rcv_color):
        self.ax_2.plot(points_DF.utc_time, points_DF.east, rcv_color, marker=".", linewidth=1, markersize=4, alpha=0.4, label=rcv_name)
        self.ax_2.set_title('Deviation in time', size=12, loc='left')
        self.ax_2.set_xlabel('time of day [s]',size=10)
        self.ax_2.set_ylabel('distance to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_2.minorticks_on()
        self.ax_2.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_2.grid(True)
        self.ax_2.legend(loc=1)
        self.fig_2.tight_layout()
        self.fig_2.set_facecolor('whitesmoke')
        self.fig_2.show()

    def plot_utcStatus(self,points_DF, rcv_name, rcv_color):
        self.ax_3.plot(points_DF.utc_time, points_DF.status, rcv_color, marker="|", linewidth=0.2, alpha=0.4, label=rcv_name)
#        self.ax_2.plot(points_DF.utc_time, points_DF.status, rcv_color, marker="|", linewidth=0.2, alpha=0.4, label=rcv_name)
        self.ax_3.set_title('RTK correction in time', size=12, loc='left')
        self.ax_3.set_xlabel('time of day [s]',size=10)
        self.ax_3.set_ylabel('RTK status [-]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_3.minorticks_on()
        self.ax_3.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_3.grid(True)
        self.ax_3.legend(loc=1)
        self.fig_3.tight_layout()
    #    plt.axis([points_DF.utc_time.min()-100, points_DF.utc_time.max()+100, -1, 1])
        self.fig_3.set_facecolor('whitesmoke')
        self.fig_3.show()

    def plot_utcSpeed(self,points_DF, rcv_name, rcv_color):
        self.ax_4.plot(points_DF.utc_time, points_DF.raw_speed, 'k', marker=".", linewidth=0.3, alpha=0.4, markersize=1.5, label='raw_speed[m/s]')
        self.ax_4.plot(points_DF.utc_time, points_DF.raw_acc, 'k', marker=".", linewidth=0.3, alpha=0.4, markersize=1.5, label='raw_acc[m/s-2]')
        self.ax_4.plot(points_DF.utc_time, points_DF.cvl_speed, '-r', marker=".", linewidth=0.3, alpha=1, markersize=1.5, label='filtered_speed[m/s]')
        self.ax_4.plot(points_DF.utc_time, points_DF.cvl_acc, '-b', marker=".", linewidth=0.3, alpha=1, markersize=1.5, label='filtered_acc[m/s-2]')
        self.ax_4.set_title('Speed and acceleration in time', size=12, loc='left')
        self.ax_4.set_xlabel('time of day [s]',size=10)
        self.ax_4.set_ylabel('speed [mps] / acceleration [mps-2]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_4.minorticks_on()
        self.ax_4.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_4.grid(True)
        self.ax_4.legend(loc=1)
        self.ax_4.set_ylim([-10,10])
        self.fig_4.tight_layout()
    #    plt.axis([points_DF.utc_time.min()-100, points_DF.utc_time.max()+100, -6, 10])
        self.fig_4.set_facecolor('whitesmoke')
        self.fig_4.show()

    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def plot_devs_EN(self,points_DF, rcv_name, rcv_color):
        self.ax_41.plot(points_DF.diff_east, points_DF.diff_north, rcv_color, marker=".", linewidth=0.1, alpha=0.4)
        self.ax_41.set_title('Map of horizontal positions', size=12, loc='left')
        self.ax_41.set_xlabel('distance to North [m]',size=10)
        self.ax_41.set_ylabel('distance to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_41.minorticks_on()
        self.ax_41.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
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
        self.ax_42.set_ylabel('distance to East [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_42.minorticks_on()
        self.ax_42.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
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
        self.ax_43.set_ylabel('distance to North [m]',size=10)
        #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
        #plt.majorticks_on()
        self.ax_43.minorticks_on()
        self.ax_43.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
        #plt.axes().set_aspect('equal', 'datalim')
        self.ax_43.grid(True)
        self.ax_43.legend(loc=1)
        self.fig_43.tight_layout()
        self.fig_43.set_facecolor('whitesmoke')
        self.fig_43.show()

    def plot_hist(self,rtk,bins,label,max_hist,results):
        from matplotlib.colors import LogNorm

        # definitions for the axes
        x,y = rtk.diff_east, rtk.diff_north
        left, width = 0.1, 0.75
        bottom, height = 0.1, 0.75
        spacing = 0.005
        bins = bins#200
        max_hist = max_hist
        lim = 0.5
        color = 'w'

        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom + height + spacing, width, 0.1]
        rect_histy = [left + width + spacing, bottom, 0.1, height]

        # start with a rectangular Figure
        plt.figure(figsize=(8, 8),facecolor='whitesmoke', edgecolor='r')

        # 2D hist
        ax_1 = plt.axes(rect_scatter)
        ax_1.hist2d(x, y, bins=bins, cmap=plt.cm.gist_heat,norm=LogNorm(),alpha=1)
        ax_1.set_xlabel('distance to North [m]',size=12)
        ax_1.set_ylabel('distance to East [m]',size=12)
        ax_1.set_xlim([-lim,lim])
        ax_1.set_ylim([-lim,lim])
        ax_1.minorticks_on()
        ax_1.tick_params(axis='both',which='major',length=5,width=1,labelsize=0)
        ax_1.set_aspect('equal', 'datalim')
        ax_1.grid(True)

        # Hist x
        ax_histx = plt.axes(rect_histx)
        ax_histx.hist(x, bins=bins, color='k')
        #ax_histx.set_ylabel('Number of \nsamles [-]',size=10)
        ax_histx.set_ylim([0,max_hist])
        ax_histx.set_xlim(ax_1.get_xlim())
        ax_histx.minorticks_on()
        ax_histx.tick_params(axis='y',which='major',length=10,width=1,labelsize=14)
        ax_histx.tick_params(axis='x',which='major',length=10,width=1,labelsize=14)
        ax_histx.grid(True)

        # Hist y
        ax_histy = plt.axes(rect_histy)
        ax_histy.hist(y, bins=bins, color='k', orientation='horizontal')
        #ax_histy.set_xlabel('Number of \nsamles [-]',size=10)
        ax_histy.set_xlim([0,max_hist])
        ax_histy.set_ylim(ax_1.get_ylim())
        ax_histy.minorticks_on()
        ax_histy.tick_params(axis='y',which='major',length=10,width=1,labelsize=14)
        ax_histy.tick_params(axis='x',which='major',length=10,width=1,labelsize=14)
        ax_histy.grid(True)


        #plt.tight_layout()
        ax_1.set_facecolor(color)
        ax_histx.set_facecolor(color)
        ax_histy.set_facecolor(color)
        plt.show()
        ax_histx.set_title(label + ' - horizontal deviations from MRA', size=16, loc='left')
        plt.title('Number of \nsamles [-]', size=12, loc='left')

        # Results
        def plot_errors(err,color):
            ax_histx.plot([results[err],results[err]],[0,max_hist],color=color)
            ax_histy.plot([0,max_hist],[results[err],results[err]],color=color)
            ax_histx.plot([-results[err],-results[err]],[0,max_hist],color=color)
            ax_histy.plot([0,max_hist],[-results[err],-results[err]],color=color)
            ax_1.add_artist(plt.Circle((0,0),results[err],fill=False,linestyle='-',color=color,label=err))
        plot_errors('µ_err','y')
        plot_errors('σ_err','g')
        plot_errors('RMS_err','b')

        from matplotlib.lines import Line2D
        custom_lines = [Line2D([0], [0], color='y'),
                Line2D([0], [0], color='g'),
                Line2D([0], [0], color='b')]
        ax_1.legend(custom_lines, ['µ_err', 'σ_err', 'RMS_err'],loc=3)

