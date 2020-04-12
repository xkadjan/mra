"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: The code is not compliant with Python 3.x, hence it will throw errors on print method without '()'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

DESCRIPTION:
The script exports dws and arm data to the csv. The script exports time slices of the dws and arm selected by time lists.
The inputs for the scripts are:
wgs_ref
wgs_ref2
dir - directory where are processed and exported files,i.e. c:/userpath/processed
dwsname - name of the dws exported and processed file .csv
armname - name of the arm exported and processed file .csv
hallname - name of the dws file where is hall position measured statically .csv

USAGE:
in the configuration file configs.ini fill in the options in these formats:

in the section 'global':
dir = path to the directory where are all the files to be exported and sliced
wgs_ref = [[lat,lon,height]]
wgs_ref2 = [[lat,lon,height]]

in the section 'dws_arm_evaluation':
dir = path to the directory where are all the files exported and sliced
dwsname = name of the dws file.csv , e.g. DWS_46205_46293.7.csv
armname = name of the arm file.csv
hallname = name of the hall file.csv

RUNNING THE SCRIPT:
OPTION #1:
Run the script from the python command prompt as follows:
python <path to the view_raw_data.py> <path to the configs file>
example:
python c:\\Users\\mpavelka\\Documents\\MiscTests\\SCALA_SCANPOINT_VALIDATION\\Python\\dws_arm_evaluation.py c:\\Users\\mpavelka\\Documents\\MiscTests\\hodnoceniGNSSproMarka\\12112017\\valid_data\\configs.ini

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
# dir = r"c:\Users\mpavelka\Documents\MiscTests\hodnoceni GNSS pro Marka\12112017\valid_data\Processed"
# hallname = r"DWS_hall40600_45500.csv"
# dwsname = r"DWS_46205_46293.7.csv" #r"DataSlice_39700_39950.csv"
# armname = r"Arm_Data1F003_46205_46293.7_processed.csv"
# wgs_ref = np.array([[50.2348548388889,14.9123327444444,242.877]])
# wgs_ref2 = np.array([[50.2349479305556,14.9120706958333,243.003]])
"""

import dws_arm_helper as dah
import numpy as np
import os
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

wgs_ref = np.array(json.loads(config.get('global','wgs_ref')))
wgs_ref2 = np.array(json.loads(config.get('global','wgs_ref2')))
dir = config.get('dws_arm_evaluation','dir')
dwsname = config.get('dws_arm_evaluation','dwsname')
armname = config.get('dws_arm_evaluation','armname')
hallname = config.get('dws_arm_evaluation','hallname')
dwspath = os.path.join(dir,hallname)


heading = dah.bearing(wgs_ref,wgs_ref2)

dah.dws_arm_static_evaluation(dwspath,wgs_ref,wgs_ref2,verbose=True)
dah.dws_arm_dynamic_evaluation(dir,dwsname,armname,heading=heading,plotting=True,verbose=True)