# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:55:49 2019

@author: xkadj
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
import matplotlib.patches as patches

def get_clusters(outsiders,enc):
    enc_len = len(enc)
    indexes = pd.Series(outsiders.index)

    clusters = []
    first,last = indexes[0],indexes[0]

    for index in indexes[1:]:
        if last + 1 == index:
            last = index
        else:
            if last >= enc_len:
                clusters.append([first-1,last])
            if first <= 1:
                clusters.append([1,last+1])
            else:
                clusters.append([first-1,last+1])
            first,last = index,index

    return clusters

def fix_enc(enc,err_clusters,distance):
    speed_corr = np.array(enc.speed)
    for cluster in range(len(err_clusters)):
        bound_points_time = [enc.loc[err_clusters[cluster][0]].time,
                             enc.loc[err_clusters[cluster][1]].time]
        bound_points_speed = [enc.loc[err_clusters[cluster][0]].speed,
                              enc.loc[err_clusters[cluster][1]].speed]

        polynomial = np.poly1d(np.polyfit(bound_points_time, bound_points_speed, 1))
        for point in range(err_clusters[cluster][0],err_clusters[cluster][1]-1):
            speed_corr[point]  = polynomial(enc.iloc[point].time)
    enc["speed_corr"] = speed_corr

    enc["dist_corr_diff"] = enc.speed_corr * enc.time_diff       #[m]
    enc["num_corr_diff"] = enc.dist_corr_diff / distance         #[-]
    enc["num_corr_diff_round"] = (enc.num_corr_diff)        #[-]

    diff = enc.num_corr_diff_round.tolist() #sum with firt zero
    diff[0] = 0
    for sample in range(1,len(diff)):
        diff[sample] = diff[sample-1] + diff[sample]
    enc["num_corr_sum"] = diff

    clockwise = np.mean(enc["speed_cvl"]) > 0
    enc["num"] = enc.num.iloc[0] + enc.num_corr_sum * (((clockwise*-1)+0.5)*2)

    return enc

def replace_times(enc):
    enc["round_diff_abs"] = abs(enc.num_corr_diff - enc.num_corr_diff_round)
    enc["round_diff_abs"] = enc.round_diff_abs.shift(periods=-1,fill_value=0)
    bt = enc[enc.round_diff_abs > 0.01]   # renamed: bad_times -> bt

    bt["time"] = bt.time + (bt.num_corr_diff_round / bt.num_corr_diff * bt.time_diff) - bt.time_diff

    times = np.array([enc.index.tolist(), enc.time]).T
    times_corr = np.array([bt.index.tolist(), bt.time]).T

    for corr in range(len(times_corr)):
        for orig in range(len(times)):
            if times_corr[corr][0] == times[orig][0]:
                times[orig][1] = times_corr[corr][1]

    enc["time"] = pd.Series(times.T[1], index=times.T[0].astype(int))

    return enc

def ENC_signal_corrector(sensorENC):
    radius = 3
    points = 2500
    circle = 2 * np.pi * radius
    distance = circle / points
    kernel_size = 15
    atol = 0.05

    enc = pd.DataFrame({'time': sensorENC.ENCtime,'num': sensorENC.ENCnum})

    enc["num_original"] = enc.num
    enc["num_diff"] = enc.num.diff()

    enc["time"] = enc.time / 1000000                            #[s]
    enc["time_diff"] = enc.time.diff()                          #[s]
    enc = enc.dropna()

    enc["dist_diff"] = enc.num_diff * distance                  #[m]
    enc["speed"] = enc.dist_diff / enc.time_diff                #[m/s]

    kernel = (np.ones(kernel_size)/kernel_size).tolist()
    cvl = np.zeros(len(enc))
    cvl[int((kernel_size-kernel_size%2)/2):-int((kernel_size-kernel_size%2)/2)] = np.convolve(enc.speed, kernel, mode='valid')
    enc["speed_cvl"] = cvl

    enc["outsider"] = ~np.isclose(enc.speed, enc.speed_cvl, atol=atol)
    outsiders = enc.where(enc.outsider).dropna()

    err_clusters = get_clusters(outsiders,enc)
    bound_points = enc.loc[np.concatenate((err_clusters), axis=0)]

    enc = fix_enc(enc,err_clusters,distance)
    enc = replace_times(enc)

    # =============================================================================
    enc_f = enc[["time","num"]]
#    enc_f = enc_f[enc_f.num.diff() != 0]  #first ment of errasing of zeros

    enc_f["num_diff"] = enc_f.num.diff()

    enc_f["time"] = enc_f.time                                   #[s]
    enc_f["time_diff"] = enc_f.time.diff()                       #[s]
    enc_f = enc_f.dropna()

    enc_f["dist_diff"] = enc_f.num_diff * distance               #[m]
    enc_f["speed"] = enc_f.dist_diff / enc_f.time_diff           #[m/s]

    enc_f = enc_f[enc_f.num.diff() != 0]   #actual placement of errasing of zeros

    enc_f["time"] = enc_f.time * 1000000
    enc["time"] = enc.time * 1000000
    outsiders["time"] = outsiders.time * 1000000
    bound_points["time"] = bound_points.time * 1000000

    fig, ax = plt.subplots(figsize=[12.2, 3])
    rcParams["font.family"] = "Arial"

#    ax.plot(enc.time, enc.speed, '.g',linestyle='dashed',linewidth=0.5, markersize=4)
    ax.plot(enc.time, enc.speed_cvl, '.r',linestyle='dashed',linewidth=0.5, markersize=2)
    ax.plot(outsiders.time, outsiders.speed, 'or', markersize=5)
    ax.plot(bound_points.time, bound_points.speed, 'ob', markersize=5)
    ax.plot(enc.time, enc.speed_corr, '.k',linestyle='dashed',linewidth=0.5, markersize=4)
    ax.plot(enc_f.time, enc_f.speed, '.c',linestyle='dashed',linewidth=0.5, markersize=4)

    ax.set_xlabel('Time of day [s]',size=8)
    ax.set_ylabel('Instant speed of MRA [m.s$^{-1}$]',size=8,labelpad=2)
    #ax.set_xlim(emit=1, auto=0, xmin=57181, xmax=57227)

    ax.grid(True, color='grey', linestyle=':', linewidth=0.5)
    ax.tick_params(axis='x',which='major',length=10,width=1,labelsize=8)
    ax.tick_params(axis='x',which='major',length=5,width=1,labelsize=8)
    ax.tick_params(axis='y',which='major',length=10,width=1,labelsize=8)
    ax.tick_params(axis='y',which='minor',length=5,width=1,labelsize=8)
    #ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, pos: '%.3f' % x))
    ax.minorticks_on()
    plt.grid(True, color='grey', linestyle=':', linewidth=0.5,which='major')

    plt.tight_layout()
    ax.set_facecolor('#f3f3f3')
#    plt.show()

    return enc_f[["time","num"]]
