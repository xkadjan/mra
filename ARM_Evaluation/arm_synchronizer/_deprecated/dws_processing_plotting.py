# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 10:25:24 2019

@author: xkadj
"""
import matplotlib.pyplot as plt

def plot_map(dewesoft):
    plt.figure(num=1, figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
    plt.plot(dewesoft.east, dewesoft.north, 'r', marker=".", linewidth=0.1, alpha=0.4, label='dewesoft')
    plt.title('Map of horizontal positions', size=12, loc='left')
    plt.xlabel('distance to North [m]',size=10)
    plt.ylabel('distance to East [m]',size=10)
#    plt.set_minor_formatter(FormatStrFormatter("%.2f"))
#    plt.majorticks_on()
    plt.minorticks_on()
    plt.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
    plt.axes().set_aspect('equal', 'datalim')
    plt.style.use('seaborn-paper')
    plt.grid(True)
    plt.legend(loc=1)
    plt.tight_layout()
    plt.show()
    
def plot_status(dewesoft):
    plt.figure(num=2, figsize=[12, 2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
    plt.plot(dewesoft.utc_time, dewesoft.status_gnss, 'g', marker=".", linewidth=0.2, alpha=0.4, label='status_gnss')
    plt.plot(dewesoft.utc_time, dewesoft.status_sys, 'r', marker=".", linewidth=0.2, alpha=0.4, label='status_sys')
#    plt.plot(dewesoft.utc_time, dewesoft.time_dev, 'y', marker=".", linewidth=0.2, alpha=0.4, label='time deviation (utc-log)')
    plt.title('System/GNSS status profile', size=12, loc='left')
    plt.xlabel('time of day [s]',size=10)
    plt.ylabel('System/GNSS status [-]',size=10)
    #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
    #plt.majorticks_on()
    plt.minorticks_on()
    plt.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
    #plt.axes().set_aspect('equal', 'datalim')
    plt.grid(True)
    plt.legend(loc=1)
    plt.tight_layout()
    plt.show()
    
def plot_height(dewesoft):
    plt.figure(num=3, figsize=[12, 2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
    plt.plot(dewesoft.utc_time, dewesoft.up, 'r', marker=".", linewidth=0.2, alpha=0.4, label='height')
    plt.title('Height profile', size=12, loc='left')
    plt.xlabel('time of day [s]',size=10)
    plt.ylabel('height profile [m]',size=10)
    #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
    #plt.majorticks_on()
    plt.minorticks_on()
    plt.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
    #plt.axes().set_aspect('equal', 'datalim')
    plt.grid(True)
    plt.legend(loc=1)
    plt.tight_layout()
    plt.show()
    
def plot_speed(dewesoft):
    plt.figure(num=4, figsize=[12, 2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
    plt.plot(dewesoft.utc_time, dewesoft.raw_speed, 'r', marker=".", linewidth=0.2, alpha=0.4, label='speed')
    plt.title('Speed profile (raw)', size=12, loc='left')
    plt.xlabel('time of day [s]',size=10)
    plt.ylabel('speed [kph]',size=10)
    #plt.set_minor_formatter(FormatStrFormatter("%.2f"))
    #plt.majorticks_on()
    plt.minorticks_on()
    plt.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
    #plt.axes().set_aspect('equal', 'datalim')
    plt.grid(True)
    plt.legend(loc=1)
    plt.tight_layout()
    plt.show()