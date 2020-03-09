# -*- coding: utf-8 -*-
import os
import numpy as np
import arm_processor as proc
import arm_plotter as plt


wgs_ref = np.array([[50.07478605085059,14.52025289904692,286.6000000000184]]) #RTK-VRS
wgs_ref2 = np.array([[50.07508285962353,14.52026554104843,286.6000000000574]])#RTK-VRS
#wgs_ref = np.array([[50.074786356011245, 14.520253133476757, 235.338018326546376]]) #novatel(DGPS-Nov) -etrs
#wgs_ref2 = np.array([[50.075083143026525, 14.520265843926168, 235.323186840645207]])#novatel(DGPS-Nov) -etrs
#wgs_ref = np.array([[50.074791265189710, 14.520261214076397, 235.331443161528682]]) #novatel(DGPS-Nov) -wgs
#wgs_ref2 = np.array([[50.075088052669322, 14.520273966117056, 235.310573094985472]])#novatel(DGPS-Nov) -wgs

ENC_resolution = 2500
Radius = 3 
artifical_angle_offset = 15#novatel-rtk
#artifical_angle_offset = 15#dewesoft-valeo
#artifical_angle_offset = 8.7#novatel-valeo(corrected)
#artifical_angle_offset = 5#novatel-valeo

rate_hz = 20
dir = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\TO_PROCESS\used"
#dir = r"C:\Users\xkadj\OneDrive\valeo\191114_ARM_DEWESOFT_NOVATEL\arm_data\TO_PROCESS"

folders_list = [x[0] for x in os.walk(dir)]
f = 20
error_files = []
for measurement_dir in folders_list[1:]:
    if "unused" in measurement_dir: continue
    measurement_name = measurement_dir.split('\\')[-1]
    print(" - folder name: " + str(measurement_name))
    files = os.listdir(measurement_dir)
    
    ascs = [s for s in files if 'ASC' in s]
    ascfilepaths = [os.path.join(dir, measurement_name, name) for name in ascs]
    
    ff = f + 5
    for arm_path in ascfilepaths:
#        try:
        armproc = proc.Arm_Processor(arm_path,wgs_ref,wgs_ref2,ENC_resolution,Radius,artifical_angle_offset,rate_hz)
        sensorPPS,sensorHALL,sensorHALL_orig,sensorENC,sensorPPSuError,fixtimestring = armproc.arm_processor()

        arm_final = armproc._arm_data
        arm_synced = armproc.arm_synced
        title = measurement_name + "_" + str(fixtimestring) + "_" +  os.path.basename(arm_path)           
        
        arm_final_print = arm_final.drop(columns=['ENCnumber','EventTime','ENCangle'])
        path = str(os.path.join(dir, 'async_' + title[:-4] + '.csv'))
        arm_final_print.to_csv(path)
#        print(" - created file: " + path)
        
        path = str(os.path.join(dir, str(rate_hz) + 'hz_' + title[:-4] + '.csv'))
        arm_synced.to_csv(path)
#        print(" - created file: " + path)
        
        peaks = proc.peak_detector(arm_synced)
        path = str(os.path.join(dir, 'peaks_' + title[:-4] + '.csv'))
        peaks.to_csv(path)
#        print(" - created file: " + path)
        
        halls = proc.get_halls(sensorHALL)
        path = str(os.path.join(dir, 'halls_' + title[:-4] + '.csv'))
        halls.to_csv(path)
#        print(" - created file: " + path)
        
        badhalls = proc.get_halls_orig(sensorHALL_orig)
        path = str(os.path.join(dir, 'badhalls_' + title[:-4] + '.csv'))
        badhalls.to_csv(path)
#        print(" - created file: " + path)
        
        ff += 1
#        plt.arm_plot(f,ff,arm_final,arm_synced,sensorHALL,sensorHALL_orig,sensorENC,title,dir,peaks)
        print(" - ARM_CONVERTOR - done")          
#        except:
#            print(" - an exception occurred")
#            print(" - the file " + str(arm_path) + " was not posible to convert!")
#            error_files.append(arm_path)
    print(" -" * 50)
    f += 20 #pocet grafu
print(" - error files: " + str(error_files))