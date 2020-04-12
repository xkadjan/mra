# -*- coding: utf-8 -*-
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: The code is not compliant with Python 3.x, hence it will throw errors on print method without '()'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

DESCRIPTION:
The script plots X coordinates of ASC processed data and Dewesoft processed data
The inputs for the script are:
wgs_ref
wgs_ref2
dir - path to the directory where are raw data of dewesoft and arm

USAGE:
place all ASC files and Dewesoft files into one parent folder
in the configs.ini file fill in 'global' options, those are wgs_ref and wgs_ref2 and path to the directory
of the raw data of dewesoft and arm

The format of the 'global' section is:
dir = path to the directory where are raw data of dewesoft and arm
wgs_ref = [[lat,lon,height]]
wgs_ref2 = [[lat,lon,height]]

RUNNING THE SCRIPT:
OPTION #1:
Run the script from the python command prompt as follows:
python <path to the view_raw_data.py> <path to the configs file>
example:
python c:\\Users\\mpavelka\\Documents\\MiscTests\\SCALA_SCANPOINT_VALIDATION\\Python\\view_raw_data.py c:\\Users\\mpavelka\\Documents\\MiscTests\\hodnoceniGNSSproMarka\\12112017\\valid_data\\configs.ini

OPTION #2:
running from the IDE, spyder,pycharm, etc.
A] in Spyder:
1. go to tab run, click on configure
2. check the 'Command lines option' box
3. Enter the path to the configs.ini file to the text field next to the checked box
4. Run from the IDE

B] in pycharm:
1. go to tab run and click on edit configurations
2. into the field 'Script parameters' enter the path to configs.ini file
3. Run from the IDE

TEST DATA:
dir = r"c:\\Users\\mpavelka\\Documents\\MiscTests\\hodnoceniGNSSproMarka\\12112017\\valid_data"
wgs_ref = np.array([[50.2348548388889,14.9123327444444,242.877]])
wgs_ref2 = np.array([[50.2349479305556,14.9120706958333,243.003]])

"""

import numpy as np
import configparser
import dws_arm_helper as dah
import json
import sys

if len(sys.argv) > 1:
    cf = sys.argv[1]
    print(cf)
else:
    cf = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt Arm\SWskripty\ARM_Soft\ARM_Soft v4.00\ARM_Evaluation\arm_evaluation_v4\configs.ini"

config = configparser.ConfigParser()
config.read(cf)

wgs_ref = np.array(json.loads(config.get('global','wgs_ref')))
wgs_ref2 = np.array(json.loads(config.get('global','wgs_ref2')))
dir = config.get('global','dir')

ENC_resolution,Radius,arm,sensorPPS,sensorPPSuError,sensorHALL,sensorENC,armPositions = dah.view_raw_data(dir,wgs_ref,wgs_ref2)
