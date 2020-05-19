# -*- coding: utf-8 -*-
import os
import numpy as np
import arm_processor as proc
import arm_plotter as plt
import configargparse

def configArgParser():
    description = '   Measurement Robotic Arm (MRA), The MIT License (MIT), Copyright (c) 2019 CULS Prague TF\nprogrammed by: Jan Kaderabek\n'
    parser = configargparse.ArgParser(default_config_files=['config.ini'], description=description)

    # Arguments below are defaultly reading from configfile
    parser.add('-p', '--data_path', type=str, help='path of MRA and sensors data')
    parser.add('-ref','--wgs_ref', type=lambda x: list(map(float,(str(x).split(',')))), help='reference point in center of rotation (in WGS84)')
    parser.add('-ref_2','--wgs_ref_2', type=lambda x: list(map(float,(str(x).split(',')))), help='reference point on line between center and hall signal (in WGS84)')
    parser.add('--resolution', type=int, help='MRA incremetar encoder resolution')
    parser.add('--radius', type=float, help='radius of MRA')
    parser.add('--angle_offset', type=float, help='angle antenna offset')
    parser.add('--rate_hz', type=int, help='required frequence of interpolation')
    parser.add('--enc_tol', type=int, help='tolerance of bad encoder ticks for Hall signal corrector')
    args = parser.parse()
    return args

args = configArgParser()

dir_rtk = os.path.join(args.data_path,'dewesoft_converted')
wgs_ref = np.array([args.wgs_ref]) #RTK-VRS
wgs_ref2 = np.array([args.wgs_ref_2])#RTK-VRS

ENC_resolution = args.resolution
Radius = args.radius
artifical_angle_offset = args.angle_offset
rate_hz = args.rate_hz
enc_tol = args.enc_tol
dir = os.path.join(args.data_path,'arm_raw')
output_dir = os.path.join(args.data_path,'arm_converted')

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
        try:
            armproc = proc.Arm_Processor(arm_path,wgs_ref,wgs_ref2,ENC_resolution,Radius,artifical_angle_offset,rate_hz,enc_tol)
            sensorPPS,sensorHALL,sensorHALL_orig,sensorENC,sensorPPSuError,fixtimestring = armproc.arm_processor()

            arm_final = armproc._arm_data
            arm_synced = armproc.arm_synced
            title = measurement_name + "_" + str(fixtimestring) + "_" +  os.path.basename(arm_path)

            arm_final_print = arm_final.drop(columns=['ENCnumber','EventTime','ENCangle'])
            path = os.path.join(output_dir, 'async_' + title[:-4] + '.csv')
            arm_final_print.to_csv(path)

            path = os.path.join(output_dir, str(rate_hz) + 'hz_' + title[:-4] + '.csv')
            arm_synced.to_csv(path)

            peaks = proc.peak_detector(arm_synced)
            path = os.path.join(output_dir, 'peaks_' + title[:-4] + '.csv')
            peaks.to_csv(path)

            halls = proc.get_halls(sensorHALL)
            path = os.path.join(output_dir, 'halls_' + title[:-4] + '.csv')
            halls.to_csv(path)

            badhalls = proc.get_halls_orig(sensorHALL_orig)
            path = os.path.join(output_dir, 'badhalls_' + title[:-4] + '.csv')
            badhalls.to_csv(path)

            ff += 1
            #plt.arm_plot(f,ff,arm_final,arm_synced,sensorHALL,sensorHALL_orig,sensorENC,title,dir,peaks)

        except:
            print(" - an exception occurred")
            print(" - the file " + str(arm_path) + " was not posible to convert!")
            error_files.append(arm_path)
        print(" - ARM_CONVERTOR - done")
    print(" -" * 50)
    f += 20 #pocet grafu
print(" - error files: " + str(error_files))