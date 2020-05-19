# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:51:05 2020

@author: xkadj
"""

import matplotlib.pyplot as plt
#dev = evl.novatel.deviation
#speed = evl.novatel.cvl_speed
label = 'Novatel PwrPak7'
#fig, ax = plt.subplots(figsize=[10, 10], dpi=100, facecolor='w', edgecolor='r')
#
#ax.scatter(speed,dev, s=1, color='C7')
#ax.set_title(label + ' - dependence of deviation on speed', size=10, loc='left')
#ax.set_xlabel('speed [m/s]',size=10)
#ax.set_ylabel('deviation [m]',size=10)
##ax.set_xlim([0,0.5])
##ax.set_ylim([0,30])
#ax.minorticks_on()
#ax.tick_params(axis='y',which='major',length=10,width=1,labelsize=10)
#ax.tick_params(axis='x',which='major',length=10,width=1,labelsize=10)
#ax.grid(True)
#fig.tight_layout()

x_value = 'speed [m/s]'
data = evl.novatel

g = sb.lmplot('cvl_speed','deviation',data,scatter_kws={"s": 1, "alpha": 0.3},legend=True)
g = (g.set_axis_labels(x_value,'deviation [m]')
        .set(xlim=(0, 10), ylim=(0, 0.3),xticks=[0,2,4,6,8,10], yticks=[0,0.1,0.2,0.3])
        .fig.subplots_adjust(wspace=.02))