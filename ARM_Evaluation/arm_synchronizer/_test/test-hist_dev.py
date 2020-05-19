# -*- coding: utf-8 -*-
"""
Created on Mon May 11 16:07:59 2020

@author: xkadj
"""

import matplotlib.pyplot as plt
dev = evl.ublox.deviation
label = 'Novatel PwrPak7'
bins = 50

fig, ax = plt.subplots(figsize=[10, 3], dpi=100, facecolor='w', edgecolor='r')

#ax.figure(figsize=(8, 3),facecolor='whitesmoke', edgecolor='r')
ax.hist(dev, bins=bins, density =True, color='b')
ax.set_title(label + ' - density of horizontal deviations from MRA', size=10, loc='left')
ax.set_xlabel('deviation [m]',size=10)
ax.set_ylabel('density [%]',size=10)

ax.set_xlim([0,0.5])
ax.set_ylim([0,30])
ax.minorticks_on()
ax.tick_params(axis='y',which='major',length=10,width=1,labelsize=10)
ax.tick_params(axis='x',which='major',length=10,width=1,labelsize=10)
ax.grid(True)
fig.tight_layout()