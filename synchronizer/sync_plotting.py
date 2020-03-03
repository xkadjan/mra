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
    def __init__(self, arm, rtk):
        self.arm = arm
#        self.rtk = rtk
        self.fig_1, self.ax_1 = plt.subplots(num=301,figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r')
        self.fig_2, self.ax_2 = plt.subplots(num=302,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
        self.fig_3, self.ax_3 = plt.subplots(num=303,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
        self.fig_4, self.ax_4 = plt.subplots(num=304,figsize=[12.2, 3], dpi=100, facecolor='w', edgecolor='r')
    
    def plot_arm(self,data,signal_name,color): 
        self.plot_EN(data, signal_name, color)
        self.plot_utcE(data, signal_name, color)
        self.plot_utcSpeed(data, signal_name, color)
        
    def plot_rtk(self,rtk,signal_name,color):
        self.plot_EN(rtk, signal_name, color)
        self.plot_utcE(rtk, signal_name, color)
        self.plot_utcStatus(rtk, signal_name, color)
    
    def plot_marks(self):
        bold = 1
        self.plot_MARK(self.fig_2, self.ax_2, self.arm.arm_badhalls,'arm_badhalls','y',bold,[self.arm.arm_20hz.east.min()-0.5,self.arm.arm_20hz.east.max()+0.5])
        self.plot_MARK(self.fig_4, self.ax_4, self.arm.arm_badhalls,'arm_badhalls','y',bold,[-10,10])
        
        self.plot_MARK(self.fig_2, self.ax_2, self.arm.arm_halls,'arm_halls','k',bold,[self.arm.arm_20hz.east.min()-0.5,self.arm.arm_20hz.east.max()+0.5])
        self.plot_MARK(self.fig_4, self.ax_4, self.arm.arm_halls,'arm_halls','k',bold,[-10,10])
        
        if len(self.arm.arm_peaks): self.plot_MARK(self.fig_2, self.ax_2, self.arm.arm_peaks,'arm_peaks','r',bold+1,[self.arm.arm_20hz.east.min()-1,self.arm.arm_20hz.east.max()+1])
        if len(self.arm.arm_peaks): self.plot_MARK(self.fig_4, self.ax_4, self.arm.arm_peaks,'arm_peaks','r',bold+1,self.arm.arm_peaks.raw_speed_diff)
        
        self.plot_bad_circles(self.arm.circle_bad)
        
    def plot_MARK(self,fig, ax, marks, mark_type, rcv_color, bold, bounds):
        if len(bounds) == 2:
            ax.plot([marks.utc_time, marks.utc_time], [bounds[0],bounds[1]], rcv_color, linestyle='--', linewidth=bold, alpha=0.6)
        else:
            ax.plot(marks.utc_time, np.zeros(len(marks.utc_time)), rcv_color, linewidth=0, marker='o', markersize=5, alpha=0.8)
        fig.show()

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
        self.ax_4.plot(points_DF.utc_time, points_DF.raw_speed, rcv_color, marker=".", linewidth=0.2, alpha=1, markersize=1, label='raw_speed')
        self.ax_4.plot(points_DF.utc_time, points_DF.raw_acc, 'b', marker=".", linewidth=0.2, alpha=1, markersize=1, label='raw_acc')
        self.ax_4.set_title('Speed and acceleration in time', size=12, loc='left')
        self.ax_4.set_xlabel('time of day [s]',size=10)
        self.ax_4.set_ylabel('speed [mps] / acceleration [mps-1]',size=10)
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
