# Evaluation codes for determinte of position senzors properties by MRA method

## Prerequisites:
 - MRA raw data (*.ASC)
 - data of system being tested:
    - NMEA GPGGA format in (**.txt); eval: 'python SYNC_ARM-DWS.py'; e.g..:
     *"$GPGGA,185050.80,5004.48861503,N,1431.21637337,E,4,24,0.9,235.49,M,45.00,M,01,0001*5A"*
    - native format in (*.txt); eval: 'python SYNC_ARM-DWS.py'; e.g..:
     *"1;46738.15;50.074771314094164;14.520278664782351;234.760330200195;7;0"*
     with header:
     *";utc_time;lat;lon;height;status_gnss;status_sys"*
     
## Installation:
1) unzip data to local drive (below: '<your_data_folder>')
2) clone or download zip of repository (DEWESOFT_evaluation):
https://github.com/xkadjan/mra/tree/DEWESOFT_evaluation
3) go to 'mra/ARM_Evalution' in terminal
4) run 'pip install -r req.txt' (PIP is necessary to installatd)

## Converting of MRA data:
2) copy MRA raw data (*.ASC) to '<your_data_folder>/arm_raw' 
3) adjust the 'data_path' in mra/ARM_Evaluation/arm_convertor/config.ini (path where you have '<your_data_folder>')
4) go to 'mra/ARM_Evalution/arm_convertor' and run 'python ARM_CONVERTOR.py'

## Evaluation of MRA data:
1) copy this data to '<your_data_folder>/dewesoft_converted' 
2) adjust the 'data_path' in mra/ARM_Evaluation/arm_synchronizer/config.ini (path where you have '<your_data_folder>')
3) go to 'mra/ARM_Evalution/arm_convertor'

4a) if you are using NMEA (stantart GNSS serial bus message format)
   run 'python SYNC_ARM-DWS.py'
4b) elif you are using native format (which not have not standart structure, e.g.: converted DEWESOFT data, see Prerequisites)
   run 'python SYNC_ARM-DWS.py'
5) results could be ploted and results be writed to '<your_data_folder>/output_eval'                                                 






********************************************************************************
The MIT License (MIT), Copyright (c) 2020 CULS Prague TF

MRA is platform for verify of the dynamic properties of the Real-Time Kinematic receivers (RTK receivers). 
MRA also can be suitable for verify of other localisation devices.
MRA is not only this software part but whole methodology for creating of reference trajectory described in paper here:
https://dspace.emu.ee/xmlui/bitstream/handle/10492/4809/AR2019_Vol17No4_Matejka.pdf?sequence=4&isAllowed=y

Previous paper is describing process and metrics of evaluation of static properties and also brings some values of three RTK receivers:
https://dspace.emu.ee/xmlui/bitstream/handle/10492/3988/Vol16No3_14.pdf?sequence=4&isAllowed=y

