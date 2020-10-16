# -*- coding: utf-8 -*-
import os
import arm_processor as proc
import configargparse
import warnings

def configArgParser():
    description = '   Measurement Robotic Arm (MRA), The MIT License (MIT), Copyright (c) 2019 CULS Prague TF\ndeveloped by: Jan Kaderabek\n'
    parser = configargparse.ArgParser(default_config_files=['config.ini'], description=description)
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

def checkFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

warnings.filterwarnings("ignore")

args = configArgParser()
input_dir = args.data_path
output_dir = checkFolder(os.path.join(args.data_path,'arm_converted'))

folders_list = [x[0] for x in os.walk(input_dir)]
error_files = []
for measurement_dir in folders_list[1:]:
    if "unused" in measurement_dir: continue
    measurement_name = measurement_dir.split('\\')[-1]
    print(" - ARM raw data folder: " + str(measurement_name))
    files = os.listdir(measurement_dir)

    ascs = [s for s in files if 'ASC' in s]
    ascfilepaths = [os.path.join(input_dir, measurement_name, name) for name in ascs]

    for arm_path in ascfilepaths:
        try:
            armproc = proc.Arm_Processor(arm_path,args)
            armproc.arm_processor()

            arm_final = armproc.arm_data
            arm_synced = armproc.arm_synced
            title = measurement_name + "_" + str(armproc.fixtimestring) + "_" +  os.path.basename(arm_path)

            arm_final_print = arm_final.drop(columns=['ENCnumber','EventTime','ENCangle'])
            arm_final_print.to_csv(os.path.join(output_dir, 'async_' + title[:-4] + '.csv'))

            arm_synced.to_csv(os.path.join(output_dir, str(args.rate_hz) + 'hz_' + title[:-4] + '.csv'))

            peaks = proc.peak_detector(arm_synced)
            peaks.to_csv(os.path.join(output_dir, 'peaks_' + title[:-4] + '.csv'))

            halls = proc.get_halls(armproc.sensorHALL)
            halls.to_csv(os.path.join(output_dir, 'halls_' + title[:-4] + '.csv'))

            badhalls = proc.get_halls_orig(armproc.sensorHALL_orig)
            badhalls.to_csv(os.path.join(output_dir, 'badhalls_' + title[:-4] + '.csv'))

            print(" - ARM data: " + title + " converting finished")

        except:
            print(" - an exception occurred")
            print(" - the file " + str(arm_path) + " was not posible to convert!")
            error_files.append(arm_path)

        print("-" * 50)

print(" - error files: " + str(error_files))