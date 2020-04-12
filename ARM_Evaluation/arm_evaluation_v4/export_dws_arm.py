# -*- coding: utf-8 -*-
"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: The code is not compliant with Python 3.x, hence it will throw errors on print method without '()'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

DESCRIPTION:
The script exports dws and arm data to the csv. The script exports time slices of the dws and arm selected by time lists.
The inputs for the script are:
wgs_ref
wgs_ref2
dir - path to the raw data which are supposed to be processed and exported
time_list - list of lists of start and stop of the time slices
hall_time_list - list of start and stop of the time slice where is hall position measured

USAGE:
in the configuration file configs.ini fill in the options in these formats:

in the section 'global':
dir = path to the directory where are saved all the files to be exported and sliced
wgs_ref = [[lat,lon,height]]
wgs_ref2 = [[lat,lon,height]]

in the section 'export_dws_arm':
time_list = [[start1,stop1],[start2,stop2],...,[startx,stopx]]
hall_time_list [start,stop]

RUNNING THE SCRIPT:
OPTION #1:
Run the script from the python command prompt as follows:
python <path to the view_raw_data.py> <path to the configs file>
example:
python c:\\Users\\mpavelka\\Documents\\MiscTests\\SCALA_SCANPOINT_VALIDATION\\Python\\export_dws_arm.py c:\\Users\\mpavelka\\Documents\\MiscTests\\hodnoceniGNSSproMarka\\12112017\\valid_data\\configs.ini

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
# dir = r"c:\Users\mpavelka\Documents\MiscTests\hodnoceni GNSS pro Marka\12112017\valid_data"
# wgs_ref = np.array([[50.2348548388889,14.9123327444444,242.877]])
# wgs_ref2 = np.array([[50.2349479305556,14.9120706958333,243.003]])
# time_list = [[39700,39950],[46205,46293.7],[46550,46750]]#[[40600,45500]]#[[39700,39950],[46550,46750]]
# hall_time_list = [40600,45500]
"""

import numpy as np
import dws_arm_helper as dah
import configparser
import json
import sys

if len(sys.argv) > 1:
    cf = sys.argv[1]
    print(cf)
else:
    cf = r"c:\Users\mpavelka\Documents\MiscTests\hodnoceniGNSSproMarka\12112017\valid_data\configs.ini"

config = configparser.ConfigParser()
config.read(cf)

time_list = json.loads(config.get("export_dws_arm","time_list"))
hall_time_list = json.loads(config.get("export_dws_arm","hall_time_list"))
wgs_ref = np.array(json.loads(config.get('global','wgs_ref')))
wgs_ref2 = np.array(json.loads(config.get('global','wgs_ref2')))
dir = config.get('global','dir')

dah.export_dws_arm(dir,wgs_ref,wgs_ref2,time_list,hall_time_list)
