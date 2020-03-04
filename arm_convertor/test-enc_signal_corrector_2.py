# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 15:55:49 2019

@author: xkadj
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
            speed_corr[point-1]  = polynomial(enc.iloc[point].time)
    enc["speed_corr"] = speed_corr
    
    enc["dist_corr_diff"] = enc.speed_corr * enc.time_diff       #[m]
    enc["num_corr_diff"] = enc.dist_corr_diff / distance         #[-]   
#    enc["num_corr_diff_round"] = round(enc.num_corr_diff)        #[-] 
    enc["num_corr_diff_round"] = round(enc.num_corr_diff)        #[-] 
    
    clockwise = np.mean(enc["speed_cvl"]) > 0
    diff = enc.num_corr_diff_round.tolist()
    diff[0] = 0
    for sample in range(1,len(diff)):
        diff[sample] = diff[sample] + diff[sample-1]
    enc["num_corr_sum"] = diff
    
    enc["num"] = enc.num.iloc[0] + enc.num_corr_sum * (((clockwise*-1)+0.5)*2)
    
    return enc

def slice_enc(enc,outsiders,start,stop):
    enc = enc.where(enc.time >= start).where(enc.time <= stop).dropna()
#    enc = enc.iloc[start:stop]
    start_outsiders = enc.time.iloc[0]
    stop_outsiders = enc.time.iloc[-1]    
    outsiders = outsiders.where(outsiders.time >= start_outsiders).where(outsiders.time <= stop_outsiders).dropna()
    return enc,outsiders

def replace_times(enc):
    bad_times = enc.loc[(np.array(enc.index[abs(enc.round_diff)>0.01])-1).tolist()]
    bad_times["time_diff_corr"] = (bad_times.num_corr_diff_round / bad_times.num_corr_diff * bad_times.time_diff) - bad_times.time_diff
    bad_times["time"] = bad_times.time + bad_times.time_diff_corr
    
    times = np.array([enc.index.tolist(),enc.time]).T
    times_corr = np.array([bad_times.index.tolist(),bad_times.time]).T
    
    for corr in range(len(times_corr)):
        for orig in range(len(times)):
            if times_corr[corr][0] == times[orig][0]:
                times[orig][1] = times_corr[corr][1]
    
    enc["time"] = pd.Series(times.T[1],index=times.T[0].astype(int))
    return enc

# =============================================================================
# INIT
# =============================================================================
#
#def ENC_signal_corrector(sensorENC):
    
radius = 3
points = 2500
circle = 2 * np.pi * radius
distance = circle / points

kernel_size = 5
atol = 0.05

plot_num = 6
bounds = [0,999999]
#bounds = [127.1,127.8]

means, acc = 1, 0
# =============================================================================
# MAIN
# =============================================================================
#enc = pd.DataFrame(sensorENC[["ENCnum","ENCtime"]])

enc = sensorENC
#    enc = pd.read_csv('encoder_raw.csv', sep=',', engine='python')
enc = pd.DataFrame({'time': enc.ENCtime,
                    'num': enc.ENCnum})
    
enc["num_original"] = enc.num
enc["num_diff"] = enc.num.diff()

enc["time"] = enc.time / 1000000                            #[s]
enc["time_diff"] = enc.time.diff()                          #[s]
enc = enc.dropna()

enc["dist_diff"] = abs(enc.num_diff) * distance             #[m]   
enc["dist_diff"] = enc.num_diff * distance                  #[m]       
enc["speed"] = enc.dist_diff / enc.time_diff                #[m/s]

kernel = (np.ones(kernel_size)/kernel_size).tolist()
cvl = np.zeros(len(enc))
#    cvl[int((kernel_size-kernel_size%2)/2+1):-int((kernel_size-kernel_size%2)/2-1)] = np.convolve(enc.speed, kernel, mode='valid')
cvl[int((kernel_size-kernel_size%2)/2):-int((kernel_size-kernel_size%2)/2)] = np.convolve(enc.speed, kernel, mode='valid')
enc["speed_cvl"] = cvl

#if acc == 1:
#    enc["speed_diff"] = enc.speed_cvl.diff()
#    enc = enc.dropna()
#    enc["acc"] = enc.speed_diff / enc.time_diff             #[m/s-2]

enc["outsider"] = ~np.isclose(enc.speed, enc.speed_cvl, atol=atol)
outsiders = enc.where(enc.outsider).dropna()

err_clusters = get_clusters(outsiders,enc)
bound_points = enc.loc[np.concatenate((err_clusters), axis=0)]
enc = fix_enc(enc,err_clusters,distance)

enc_copy = enc.copy(deep=True)

enc["round_diff"] = enc.num_corr_diff - enc.num_corr_diff_round
enc = replace_times(enc)

# =============================================================================
enc_f = enc[["time","num"]]
enc_f["num_diff"] = enc_f.num.diff()

enc_f["time"] = enc_f.time                                   #[s]
enc_f["time_diff"] = enc_f.time.diff()                       #[s]
enc_f = enc_f.dropna()

enc_f["dist_diff"] = abs(enc_f.num_diff) * distance          #[m]   
enc_f["dist_diff"] = enc_f.num_diff * distance               #[m]       
enc_f["speed"] = enc_f.dist_diff / enc_f.time_diff           #[m/s]



#enc_f["time"] = enc_f.time * 1000000
#enc["time"] = enc.time * 1000000
#outsiders["time"] = outsiders.time * 1000000
#bound_points["time"] = bound_points.time * 1000000
#    return enc_f[["time","num"]]
#
#
#
#
##num_corr = np.zeros(len(enc))
##num_corr[0] = enc.num.iloc[0]
##actual_enc = num_corr[0]
##for row in range(1,len(num_corr)):
##    actual_enc = actual_enc + enc.num_corr_diff.iloc[row]
##    num_corr[row] = actual_enc
##enc["num_corr"] = num_corr
##
##zero_diffcorr = enc.where(enc.num_corr_diff == 0).dropna().index
##enc_droped = enc.drop(zero_diffcorr)
#
##print(" - encoder signal corrector result: " + str(len(outsiders)) + " corrected / " + str(len(zero_ENCdiffcorr)) + " dropped samples")
##
###    return ENC_analysis, outsiders
#
# =============================================================================
# PLOT:
# =============================================================================

enc_OLD,outsiders_OLD = enc,outsiders
#enc,outsiders = slice_enc(enc,outsiders,bounds[0],bounds[1])

# =============================================================================
# speed
# =============================================================================
import matplotlib.ticker as ticker
from matplotlib import rcParams
import matplotlib.patches as patches

fig, ax = plt.subplots(num=plot_num,figsize=[12.2, 3])
rcParams["font.family"] = "Arial"

#plt.title('Instant speed of MRA',fontsize=16,fontweight="bold",loc='left')
if acc == 1: ax.plot(enc.time, enc.acc, '.y',linestyle='dashed',linewidth=0.5, markersize=2, label = 'Acceleration speed of MRA [mps-2]')
ax.plot(enc.time, enc.speed, '.g',linestyle='dashed',linewidth=0.5, markersize=4)


#if means == 1:ax.plot(enc.time, enc.speed_means, '.c',linestyle='dashed',linewidth=0.5, markersize=2)
ax.plot(enc.time, enc.speed_cvl, '.r',linestyle='dashed',linewidth=0.5, markersize=2)
ax.plot(outsiders.time, outsiders.speed, 'or', markersize=5)
ax.plot(bound_points.time, bound_points.speed, 'ob', markersize=5)
ax.plot(enc.time, enc.speed_corr, '.k',linestyle='dashed',linewidth=0.5, markersize=4)

        

ax.plot(enc_f.time, enc_f.speed, '.c',linestyle='dashed',linewidth=0.5, markersize=4)
#ax.plot(enc.time, enc.round_diff, '.m',linestyle='dashed',linewidth=0.5, markersize=4)
                 

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
                 
#rect = patches.Rectangle((50,100),40,30,linewidth=20,edgecolor='r')#,facecolor='none')
#ax.add_patch(rect)
#plt.show()         
                 


