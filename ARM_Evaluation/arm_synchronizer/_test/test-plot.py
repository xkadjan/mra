# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:13:33 2020

@author: xkadj
"""
# definitions for the axes

import matplotlib.pyplot as plt
#import matplotlib.patches as patches
from matplotlib.colors import LogNorm
#from matplotlib.lines import Line2D
#import numpy as np
#import seaborn as sb

rtk = dewesoft
bins = 200
max_hist = 100
label = 'Dewesoft - rychlost'

data,label,x_value = dws_e.dewesoft,'Dewesoft','speed [m/s]'

g = sb.lmplot('cvl_' + x_value.split(' ')[0],'deviation',data,scatter_kws={"s": 2, "alpha": 0.3},legend=True)
g = (g.set_axis_labels(x_value,'deviation [m]')
.set(xlim=(0, 10), ylim=(0, 0.3),xticks=[0,2,4,6,8,10], yticks=[0,0.05,0.1,0.15])
.fig.subplots_adjust(wspace=.02))

#x,y = rtk.diff_east, rtk.diff_north
#left, width = 0.1, 0.75
#bottom, height = 0.07, 0.72
#spacing = 0.005
#bins = bins#200
#max_hist = max_hist
#lim = 0.5
#color = 'w'
#
#rect_scatter = [left, bottom, width, height]
#rect_histx = [left, bottom + height + spacing, width, 0.1]
#rect_histy = [left + width + spacing, bottom, 0.1, height]
#
## start with a rectangular Figure
#plt.figure(figsize=(8, 8),facecolor='whitesmoke', edgecolor='r')
#
## 2D hist
#ax_1 = plt.axes(rect_scatter)
#ax_1.hist2d(x, y, bins=bins, cmap=plt.cm.gist_heat,norm=LogNorm(),alpha=1)
#ax_1.set_xlabel('deviation to North [m]',size=20)
#ax_1.set_ylabel('deviation to East [m]',size=20)
#ax_1.set_xlim([-lim,lim])
#ax_1.set_ylim([-lim,lim])
#ax_1.minorticks_on()
#ax_1.tick_params(axis='both',which='major',length=5,width=1,labelsize=0)
#ax_1.set_aspect('equal', 'datalim')
#ax_1.grid(True)
#
##data = np.arange(100, 0, -1).reshape(10, 10)
##im = ax_1.imshow(data, cmap='gist_earth')
##cax = ax_1.add_axes([0.27, 0.8, 0.5, 0.05])
##ax_1.colorbar(im, cax=cax, orientation='horizontal')
#
## Hist x
#ax_histx = plt.axes(rect_histx)
#ax_histx.hist(x, bins=bins, color='k',density = True)
##ax_histx.set_ylabel('Number of \nsamles [-]',size=10)
#ax_histx.set_ylim([0,max_hist])
#ax_histx.set_xlim(ax_1.get_xlim())
#ax_histx.minorticks_on()
#ax_histx.tick_params(axis='y',which='major',length=10,width=1,labelsize=20)
#ax_histx.tick_params(axis='x',which='major',length=10,width=1,labelsize=20)
#ax_histx.grid(True)
#
## Hist y
#ax_histy = plt.axes(rect_histy)
#ax_histy.hist(y, bins=bins, color='k', density = True, orientation='horizontal')
##ax_histy.set_xlabel('Number \n    [-]',size=10)
#ax_histy.set_xlim([0,max_hist])
#ax_histy.set_ylim(ax_1.get_ylim())
#ax_histy.minorticks_on()
#ax_histy.tick_params(axis='y',which='major',length=10,width=1,labelsize=20)
#ax_histy.tick_params(axis='x',which='major',length=10,width=1,labelsize=20)
#ax_histy.grid(True)
#
##plt.tight_layout()
#ax_1.set_facecolor(color)
#ax_histx.set_facecolor(color)
#ax_histy.set_facecolor(color)
#plt.show()
#
#title = 'Horizontal positions deviations\n' + label
#ax_histx.set_title(title, size=24, loc='left')
#plt.title('Density of \n[%]', size=20, loc='left')