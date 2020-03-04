# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 17:24:42 2019

@author: xkadj
"""
import os
import matplotlib.pyplot as plt

#def arm_plot(f,ff,arm_final,arm_synced,sensorHALL,sensorHALL_orig,sensorENC,title,dir,ENC_analysis,outsiders,peaks):  
def arm_plot(f,ff,arm_final,arm_synced,sensorHALL,sensorHALL_orig,sensorENC,title,dir,peaks):  

    
    plt.figure(num=f, figsize=[12, 6.2], dpi=100, facecolor='w', edgecolor='c').set_facecolor('whitesmoke')
    plt.plot(arm_final.Time, arm_final.Xarm, '.r',linestyle='dashed',linewidth=0.5, markersize=2)
    plt.plot(arm_synced.Time, arm_synced.Xarm, '|g',linestyle='dashed',linewidth=0.5, markersize=5)
    plt.plot([sensorHALL_orig[8],sensorHALL_orig[8]], [-3,3], ':y')
#    plt.plot([sensorHALL[8],sensorHALL[8]], [-3,3], ':b')
    plt.plot([sensorHALL[8],sensorHALL[8]], [-3.2,3.2], ':r')
    plt.xlabel('Time of day [s]',size=10)
    plt.ylabel('X-Axis of Arm [m]',size=10)
    plt.title('x-positions: ' + title)
    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
    plt.minorticks_on()
    plt.tight_layout()
    plt.show() 
    f += 1
    
#    plt.figure(num=f, figsize=[12, 6.2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
#    plt.plot(arm_final.Xarm, arm_final.Yarm, '.r',linestyle='dashed',linewidth=0.5, markersize=2)
#    plt.plot(arm_synced.Xarm, arm_synced.Yarm, '|g',linestyle='dashed',linewidth=0.5, markersize=5)
#    plt.xlabel('X-Axis of Arm [m]',size=10)
#    plt.ylabel('Y-Axis of Arm [m]',size=10)
#    plt.title('positions: ' + title)
#    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
#    plt.minorticks_on()
#    plt.tight_layout()
#    plt.show() 
#    f += 1
    
    plt.figure(num=f, figsize=[12, 6.2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
    plt.plot(arm_synced.Time, arm_synced.raw_speed, '.r',linestyle='dashed',linewidth=0.5, markersize=5)
    
    plt.plot(arm_synced.Time, arm_synced.raw_speed.diff(), '.b',linestyle='dashed',linewidth=0.5, markersize=1)
    plt.plot(arm_synced.Time[peaks.sample_index.tolist()], arm_synced.raw_speed.diff()[peaks.sample_index.tolist()], 'xr', markersize=15)
    
    plt.plot([sensorHALL_orig[8],sensorHALL_orig[8]], [0,40], ':y')
#    plt.plot([sensorHALL[8],sensorHALL[8]], [0,40], ':b')
    plt.plot([sensorHALL[8],sensorHALL[8]], [-5,45], ':r')
    plt.xlabel('Time of day [s]',size=10)
    plt.ylabel('Actual speed [kph]',size=10)
    plt.title('actual speed: ' + title)
    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
    plt.minorticks_on()
    plt.tight_layout()
    plt.show() 
    f += 1
    
##    plt.figure(num=f, figsize=[12, 6.2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
##    plt.plot([sensorHALL[8],sensorHALL[8]], [arm_final.numDiff.min(),arm_final.numDiff.max()], ':k')
##    plt.plot(arm_final.Time, arm_final.numDiff,':.')
##    plt.xlabel('Time of day [s]',size=10)
##    plt.ylabel('Omitted can messages [-]',size=10)
##    plt.title('omitted messages: ' + title)
##    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
##    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
##    plt.minorticks_on()
##    plt.tight_layout()
##    plt.show()
##    f += 1
#    
#    plt.figure(num=f, figsize=[12, 6.2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
#    plt.plot([sensorHALL[8],sensorHALL[8]], [arm_final.ENCangle.min(),arm_final.ENCangle.max()], ':k')
#    plt.plot(arm_final.Time, arm_final.ENCangle,'-|')
#    plt.xlabel('Time of day [s]',size=10)
#    plt.ylabel('Angle [°]',size=10)
#    plt.title('angle: ' + title)
#    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
#    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
#    plt.minorticks_on()
#    plt.tight_layout()
#    plt.show()
#    f += 1
#    
#    plt.figure(num=f, figsize=[12, 6.2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
##    plt.plot([sensorHALL_orig[8],sensorHALL_orig[8]], [sensorENC.ENCnum.min(),sensorENC.ENCnum.max()], ':y')
##    plt.plot([sensorHALL[8],sensorHALL[8]], [sensorENC.ENCnum.min(),sensorENC.ENCnum.max()], ':k')
#    plt.plot(sensorENC.ENCtime,sensorENC.ENCnum, '.g',linestyle='dashed',linewidth=0.5, markersize=2)
#    plt.xlabel('ENCtime [us]',size=10)
#    plt.ylabel('ENCnum [-]',size=10)
#    plt.title('ENCnum: ' + title)
#    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
#    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
#    plt.minorticks_on()
#    plt.tight_layout()
#    plt.show()
#    f += 1
#    
#    plt.figure(num=f, figsize=[12, 6.2], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
#    plt.plot([arm_final.index.min(),arm_final.index.max()],[sensorHALL[8],sensorHALL[8]], ':k')
#    
#    plt.plot(arm_final.index, arm_final.Time, '-|')
#    plt.xlabel('Index [-]',size=10)
#    plt.ylabel('Time of day [s]',size=10)
#    plt.title('time: ' + title)
#    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
#    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
#    plt.minorticks_on()
#    plt.tight_layout()
#    plt.show()
#    
#    f += 1
#    plt.figure(num=ff, figsize=[12, 3], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')
#    plt.plot(ENC_analysis.ENCtime,ENC_analysis.tangents, '.k',linestyle='dashed',linewidth=0.5, markersize=2)
#    #plt.plot(ENC_analysis.ENCtime,ENC_analysis.tan_means, '.b',linestyle='dashed',linewidth=0.5, markersize=2)
#    plt.plot(ENC_analysis.ENCtime,ENC_analysis.tan_corr, '.g',linestyle='dashed',linewidth=0.5, markersize=2)
#    plt.plot(outsiders.ENCtime,outsiders.tangents, 'xr',markersize=10)
#    plt.xlabel('Time of day [s]',size=10)
#    plt.ylabel('tangents [-]',size=10)
#    plt.title('tangents: ' + title)
#    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
#    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
#    plt.minorticks_on()
#    plt.tight_layout()
#    plt.show()
#
#    f -= 4
#   
## =============================================================================
##     OLDER PLOTS
## =============================================================================
##    title = measurement_name + "_" + str(fixtimestring) + "_" +  os.path.basename(arm_path)
##    armPositions.to_csv(os.path.join(dir, title[:-4] + '.csv'))
##    
##    plt.figure(f)
##    plt.plot(Arm.Time, Arm.Xarm, '.r',linestyle='dashed',linewidth=0.5, markersize=2)
##    plt.plot([sensorHALL_orig[8],sensorHALL_orig[8]], [-3,3], ':y')
##    plt.plot([sensorHALL[8],sensorHALL[8]], [-3,3], ':b')
##    plt.xlabel('Time of day [s]',size=10)
##    plt.ylabel('X-Axis of Arm [m]',size=10)
##    plt.title('x-positions: ' + title)
##    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
##    plt.show() 
##    f += 1
##    
###    plt.figure(f)
###    plt.plot(Arm.Time, Arm.mps, '.g',linestyle='dashed',linewidth=0.5, markersize=2)
###    plt.plot([sensorHALL_orig[8],sensorHALL_orig[8]], [0,10], ':y')
###    plt.plot([sensorHALL[8],sensorHALL[8]], [0,10], ':b')
####        plt.plot(armPositions.Time, armPositions.numDiff,':.')
###    plt.xlabel('Time of day [s]',size=10)
###    plt.ylabel('Velocity [m/s]',size=10)
###    plt.title('velocity: ' + title)
###    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
###    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
###    plt.show()
###    f += 1
##    
##    plt.figure(f)
###    plt.plot(Arm.Time, Arm.mps, '.b',linestyle='dashed',linewidth=0.5, markersize=2)
###    plt.plot([sensorHALL_orig[8],sensorHALL_orig[8]], [0,10], ':y')
##    plt.plot([sensorHALL[8],sensorHALL[8]], [0,10], ':k')
##    plt.plot(arm_final.Time, arm_final.numDiff,':.')
##    plt.xlabel('Time of day [s]',size=10)
##    plt.ylabel('Omitted can messages [-]',size=10)
##    plt.title('velocity: ' + title)
##    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
##    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
##    plt.show()
##    f += 1
##    
##    plt.figure(f)
###    plt.plot(Arm.Time, Arm.mps, '.b',linestyle='dashed',linewidth=0.5, markersize=2)
###    plt.plot([sensorHALL_orig[8],sensorHALL_orig[8]], [0,10], ':y')
##    plt.plot([sensorHALL[8],sensorHALL[8]], [0,10], ':k')
##    plt.plot(arm_final.Time, arm_final.ENCangle,'-|',inewidth=0.5, markersize=2)
##    plt.xlabel('Time of day [s]',size=10)
##    plt.ylabel('Omitted can messages [-]',size=10)
##    plt.title('velocity: ' + title)
##    plt.grid(True, color='grey', linestyle=':', linewidth=0.5)
##    plt.legend(fancybox=True, framealpha=0.2,facecolor='y')
##    plt.show()
##    f -= 2