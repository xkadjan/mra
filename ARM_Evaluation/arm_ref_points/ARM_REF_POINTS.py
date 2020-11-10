# -*- coding: utf-8 -*-
"""
@author: xkadj
"""
import pandas as pd
import configargparse

def configArgParser():
    description = '   Measurement Robotic Arm (MRA), The MIT License (MIT), Copyright (c) 2019 CULS Prague TF\ndeveloped by: Jan Kaderabek\n'
    parser = configargparse.ArgParser(default_config_files=['config.ini'], description=description)
    parser.add('-cpp', '--center_point_path', type=str, help='path to log of reference center point')
    parser.add('-hpp', '--hall_point_path', type=str, help='path to log of reference center point')
    args = parser.parse()
    return args

def get_coordinate(coor):
    return (coor/100).astype(int) + ((coor/100) - (coor/100).astype(int)) / .6

args = configArgParser()

GPGGA_header = ['prefix','utc_time','latitude','lat_postfix','longitude','long_postfix',
                'status','nos','hdop','height','height_unit','msl','msl_unit','age','base','checksum']

raw_center = pd.read_csv(args.center_point_path,skiprows=1,names=GPGGA_header)
raw_center = raw_center[raw_center.prefix == '$GPGGA']
raw_center = raw_center[raw_center.status == 4]

center = [get_coordinate(raw_center.latitude.astype(float)).mean(),
          get_coordinate(raw_center.longitude.astype(float)).mean(),
          raw_center.height.astype(float).mean()]

print('averaged center reference point:\n', center)

raw_hall = pd.read_csv(args.hall_point_path,skiprows=1,names=GPGGA_header)
raw_hall = raw_hall[raw_hall.prefix == '$GPGGA']
raw_hall = raw_hall[raw_hall.status == 4]

hall = [get_coordinate(raw_hall.latitude.astype(float)).mean(),
          get_coordinate(raw_hall.longitude.astype(float)).mean(),
          raw_hall.height.astype(float).mean()]

print('averaged hall reference point:\n', hall)

