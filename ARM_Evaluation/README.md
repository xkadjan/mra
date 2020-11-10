# ARM_Evaluation
This sub-repository contents evaluation codes for determination of results of position sensors properties by MRA method.
If you have 'DATA' folder all outputs are already generated inside it.
If you would like to verify calculations you can install the environment and run evaluation coden according to next steps:

## Installation (recommended steps):
1) clone or download and unzip the 'mra' repository from GitHub (last master version): https://github.com/xkadjan/mra/
2) unzip downloaded 'DATA' archive to 'ARM_Evaluation' folder of your local stored repository
3) install Conda if you don't have it (see: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
4) in terminal go to 'ARM_Evalution' folder and environment for MRA evaluation codes prepare from there:
5) conda create -n mra python=3.7.4
6) conda activate mra
7) pip install -r req.txt

## Running

### Averaging of two surveyed reference points (point of rotation center and point on the line giving absolute angle of MRA circle trajectory):
1) in the same terminal (environment) go to 'arm_ref_points' folder
2) run converting script by: 'python ARM_REF_POINTS.py'
3) after computing the results of averaging reference points are printed to the console

### Converting of MRA raw data to MRA reference trajecory:
1) in the same terminal (environment) go to 'arm_convertor' folder
2) run converting script by: 'python ARM_CONVERTOR.py'
3) after computing MRA reference trajectories and debug events are stored in 'DATA/MRA_converted' folder
* you can adjust converting parameters (e.g. reference points, paths to data, ets.) in text file 'config.ini'

### Evaluation of four RTK receivers by MRA method:
1) in the same terminal (environment) go to 'arm_synchronizer' folder
2) run converting script by: 'python SYNC_ARM-RTK.py'
3) after computing the results of evaluation are printed in console and with images stored in 'DATA/RESULTS' folder 
* you can adjust converting parameters (e.g. 'wholle measurement'/'only fix system state' switcher, reference points, paths to data, ets.) in text file 'config.ini'


********************************************************************************
The MIT License (MIT), Copyright (c) 2020 CULS Prague TF

MRA is platform for verify of the dynamic properties of the Real-Time Kinematic receivers (RTK receivers). 
MRA also can be suitable for verify of other localisation devices.
MRA is not only this software part but whole methodology for creating of reference trajectory described in paper here:
https://dspace.emu.ee/xmlui/bitstream/handle/10492/4809/AR2019_Vol17No4_Matejka.pdf?sequence=4&isAllowed=y

Previous paper is describing process and metrics of evaluation of static properties and also brings some values of three RTK receivers:
https://dspace.emu.ee/xmlui/bitstream/handle/10492/3988/Vol16No3_14.pdf?sequence=4&isAllowed=y

