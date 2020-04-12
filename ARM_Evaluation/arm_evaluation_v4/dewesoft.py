import pandas as pd
import numpy as np
import gpsval as gv
import matplotlib.pyplot as plt

PLOTTING = True

ARM_path = r"c:\Users\mpavelka\Documents\MiscTests\hodnoceni GNSS pro Marka\12112017\2017-12-11_14-01-32\Data1F003.ASC"
pathDS = r"c:\Users\mpavelka\Documents\MiscTests\hodnoceni GNSS pro Marka\12112017\20171211DS.csv"
export_path = r"c:\Users\mpavelka\Documents\MiscTests\hodnoceni GNSS pro Marka\12112017"

wgs_ref = np.array([[50.23485480,14.91233270,242.86]]) #194.432540893555
wgs_ref2 = np.array([[50.23494790,14.91207070,242.982]]) #194.432540893555
time_list = [[39700,39950],[46200,46400],[46550,46750]]#[[40600,45500]]#[[39700,39950],[46550,46750]]
hall_time_list = [[40600,45500]]

azimuth = gv.bearing(wgs_ref,wgs_ref2)

print azimuth

DS = gv.process_dewesoft(pathDS,wgs_ref,export_csv = False)
Frames = gv.select_dataslices(DS,time_list,export_path,export_csv = False)
paras = gv.selection_mean_paras(Frames,verbose=True)

DS['ENU_X_norm'] = DS.ENU_X - paras[0]
DS['ENU_Y_norm'] = DS.ENU_Y - paras[1]

Frames = gv.select_dataslices(DS,time_list,export_path,export_csv = False)

hFrames = gv.select_dataslices(DS,hall_time_list,export_path)
Hall_frame = hFrames[0].copy()
hall_x = Hall_frame.ENU_X_norm.mean()
hall_y = Hall_frame.ENU_Y_norm.mean()

phaseshift = np.pi/2 + np.arctan(abs(hall_x/hall_y))

print 360 - np.rad2deg(phaseshift)
Arm = gv.ARM_Processing(ARM_path,phase_shift=phaseshift)



if PLOTTING:
    t = np.arange(0,1000,0.1)
    f = 0.1
    x = paras[2] * np.cos(2*np.pi*f*t)
    y = paras[2] * np.sin(2*np.pi*f*t)

    plt.figure(1)
    plt.plot(DS.Time,DS.ENU_X_norm,'r*')
    plt.plot(Arm.Time, Arm.Xarm, '.')
    #
    # plt.figure(2)
    # plt.plot(DS.Time, DS.ENU_Y_norm, 'r*')
    #
    # plt.figure(3)
    # plt.plot(DS.ENU_X_norm,DS.ENU_Y_norm,'.')
    # plt.axis('equal')
    plt.figure(4)
    plt.plot(DS.ENU_X_norm,DS.ENU_Y_norm,'r*')
    plt.plot(x,y,'b.')
    plt.axis('equal')
    # plt.figure(5)
    # plt.plot(Arm.Time,Arm.Yarm,'.')
    # plt.title('Y arm')

    plt.show()

