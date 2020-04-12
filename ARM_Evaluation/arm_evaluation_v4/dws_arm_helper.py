import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import splrep,splev
from scipy.signal import hilbert
import DWS_ARM as da

def print_line(length=50,symbol='*'):
    for i in range(length):
        print (symbol),
    print

def extract_np_signal(signal,time_interval,series=None):
    '''
    the function extracts the data from the signal within the time interval
    :param signal: signal can be np.ndarray,pd.series or pd.DataFrame
    :param time_interval:
    :param series:
    :return:
    '''
    if time_interval:
        start = time_interval[0]
        stop = time_interval[1]
        if start > stop:
            raise Exception('In the time_list start must be lower than stop')

        if start == 0 and stop == 0:
            return signal
        elif isinstance(signal,pd.DataFrame):
            return signal.loc[(signal[series] >= start) & (signal[series] <= stop)]
        elif isinstance(signal,np.ndarray) or isinstance(signal,pd.Series):
            return signal[(signal >= start) & (signal <= stop)]
    else:
        return signal

def bearing(wgs_1,wgs_2):
    lat1 = wgs_1[0,0]
    lat2 = wgs_2[0,0]
    lon1 = wgs_1[0,1]
    lon2 = wgs_2[0,1]
    dlon = np.deg2rad(lon2 - lon1)

    bearing = np.arctan((np.sin(dlon) * np.cos(np.deg2rad(lat2))) / (np.cos(np.deg2rad(lat1)) * np.sin(np.deg2rad(lat2)) - np.sin(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.cos(dlon)))
    return 360 + bearing * 180 / np.pi

def wgsPoint(wgs_start,bearings,distance):
    '''
    calculates wgs coords in radians from known wgs,bearing and distance between points
    :param wgs_start: in degrees
    :param bearings:
    :param distance:
    :return: wgs in radians
    '''
    R = 6378137
    d = distance/R
    lat1 = (wgs_start[0])
    lon1 = (wgs_start[1])
    head = np.deg2rad(bearings)
    lat = np.arcsin(np.sin(lat1)*np.cos(d)+np.cos(lat1)*np.sin(d)*np.cos(head))
    lon = lon1+np.arctan(np.sin(head)*np.sin(d)*np.cos(lat1)/(np.cos(d)-np.sin(lat1)*np.sin(lat)))
    return np.array([[lat,lon,wgs_start[2]]])

def spline_fit_prediction(X,y,newX):
    '''
    :param X:
    :param y:
    :param newX:
    :return:
    '''
    tck = splrep(X,y)
    ynew = splev(newX,tck,der=0)
    return  ynew

def signal_phase(signal):
    '''
    calculate the phase of the signal in time
    :param signal:
    :return:
    '''
    hilb_tr = hilbert(signal)
    phase = np.unwrap(np.angle(hilb_tr))
    return phase

def signal_mean_std(signal):
    avg = np.nanmean(signal)
    std = np.nanstd(signal)
    return avg,std

def view_raw_data(dir,wgs_ref,wgs_ref2):
    '''
    the script plots X coordinates of ASC processed data and Dewesoft processed data
    :param dir: path to the parent folder of ASC and dewesoft files
    :param wgs_ref:
    :return:
    '''
    files = os.listdir(dir)
    ascs = [s for s in files if 'ASC' in s]
    csvs = [s for s in files if 'csv' in s]
    csvs = [s for s in csvs if 'processed' not in s] # omit files with "processed" in the name
    csvs = [s for s in csvs if 'DataSlice' not in s] # omit files with "DataSlice" in the name

    ascfilepaths = [os.path.join(dir, name) for name in ascs]
    csvfilepaths = [os.path.join(dir, name) for name in csvs]

    f = 1
    # arm processing
    for arm_path in ascfilepaths:
        armproc = da.Arm_Processor(arm_path,wgs_ref,wgs_ref2)
        ENC_resolution,Radius,arm,sensorPPS,sensorPPSuError,sensorHALL,sensorENC,armPositions = armproc.arm_processor()
        Arm = armproc._arm_data
        plt.figure(f)
        plt.plot(Arm.Time, Arm.Xarm, '.')
        title = 'X arm ' + os.path.basename(arm_path)
        plt.title(title)
        f += 1
    # dws processing
    for dws_path in csvfilepaths:
        dwsproc = da.DWS_Processor(dws_path,wgs_ref,wgs_ref2)
        dwsproc.dws_processor()
        DS = dwsproc._data
        plt.figure(f)
        plt.plot(DS.Time, DS.ENU_X, '.')
        title = 'X dws ' + os.path.basename(dws_path)
        plt.title(title)
        f += 1

    plt.show()
    return ENC_resolution,Radius,arm,sensorPPS,sensorPPSuError,sensorHALL,sensorENC,armPositions

def export_dws_arm(dirpath,wgs_ref,wgs_ref2,time_list,hall_time_list):

    dir = dirpath #r"c:\Users\mpavelka\Documents\MiscTests\hodnoceni GNSS pro Marka\12112017\valid_data"
    files = os.listdir(dir)

    ascs = [s for s in files if 'ASC' in s]
    csvs = [s for s in files if 'csv' in s]

    ascfilepaths = [os.path.join(dir, name) for name in ascs]
    dwspath = os.path.join(dir, csvs[0])
    print ('Found these ASC and csv files:')
    print (ascfilepaths)
    print (dwspath)

    for ascfile in ascfilepaths:
        armproc = da.Arm_Processor(ascfile,wgs_ref,wgs_ref2,time_lists=time_list)
        armproc.arm_processor()
        armproc.arm_exporter()


    dwsproc = da.DWS_Processor(dwspath,wgs_ref,wgs_ref2,time_lists=time_list,hall_times=hall_time_list)
    dwsproc.dws_processor()
    dwsproc.dws_exporter()

def dws_arm_static_evaluation(dwspath,wgs_ref1,wgs_ref2,verbose=True):
    bearings = bearing(wgs_ref1, wgs_ref2)
    phase = np.deg2rad(360 - bearings + 90)
    xhall_ref = 2.981 * np.cos(phase)
    yhall_ref = 2.981 * np.sin(phase)

    # LOAD HALL FRAME
    Hall_frame = pd.read_csv(dwspath)

    hall_x = Hall_frame.ENU_X_norm.mean()
    hall_y = Hall_frame.ENU_Y_norm.mean()

    xhall_offset = Hall_frame.ENU_X_norm - xhall_ref
    yhall_offset = Hall_frame.ENU_Y_norm - yhall_ref
    xyhall_offset = np.sqrt(xhall_offset**2 + yhall_offset**2)
    xyhall_offset_mean = np.mean(xyhall_offset)


    x_hall_offset_rmse = np.sqrt(np.mean(xhall_offset**2))
    y_hall_offset_rmse = np.sqrt(np.mean(yhall_offset**2))
    xy_hall_offset_rmse = np.sqrt(np.mean((xhall_offset**2+yhall_offset**2)))

    std_xhall_offset = np.std(xhall_offset)
    std_yhall_offset = np.std(yhall_offset)
    xyhall_offset_std = np.sqrt(std_xhall_offset**2+std_yhall_offset**2)

    dHX = Hall_frame.ENU_X_norm - hall_x
    dHY = Hall_frame.ENU_Y_norm - hall_y
    rmse_xy = np.sqrt(np.mean(dHX**2+dHY**2))*100
    # calculate the phase shift
    phaseshift = np.pi / 2 + np.arctan(abs(hall_x / hall_y))
    phasedeg = np.rad2deg(phaseshift)
    hallheading = 360 - (phasedeg - 90)

    difbearhall = bearings - hallheading

    if verbose:
        print_line()
        print ('                     STATIC MEASUREMENT')
        print_line()
        print ('Average and std of (DWS_HALL_X_mean - X_hall_ref) [cm]:', (xhall_ref - hall_x)*100,'+/-',std_xhall_offset * 100)
        print ('Average and std of (DWS_HALL_Y_mean - Y_hall_ref) [cm]:', (yhall_ref - hall_y) * 100,'+/-',std_yhall_offset * 100)
        print ('Average and std of (XY_DWS_HALL - XY_hall_ref) [cm]:',xyhall_offset_mean*100,'+/-',xyhall_offset_std*100)
        print_line()
        print ('RMSE X_hall_ref to X_dws:',x_hall_offset_rmse*100)
        print ('RMSE Y_hall_ref to Y_dws:', y_hall_offset_rmse * 100)
        print ('RMSE XY_hall_ref to XY_dws:',xy_hall_offset_rmse*100)
        print_line()
        print ('Hall probe phase shift [deg] from X axis (east)',phasedeg)
        print ('Hall probe heading [deg]', hallheading)
        print ('Heading from the wgs refs [deg]', bearings)
        print ('Difference of wgs refs bearing and Hall probe heading [deg]',difbearhall)
        print_line()

    X = Hall_frame.ENU_X_norm.as_matrix()
    Y = Hall_frame.ENU_Y_norm.as_matrix()

    f=plt.figure()
    plt.scatter((X-X.mean()) * 100, (Y-Y.mean()) * 100,marker='.',alpha=0.1)
    plt.xlabel('X[cm]'), plt.ylabel('Y[cm]'), plt.title('XY static measurement deviations from mean')
    plt.axis('equal')

    f=plt.figure()
    plt.hist((X-X.mean())*100,30)
    plt.xlabel('X[cm]'),plt.ylabel('counts[-]'),plt.title('Histogram of X values deviations from mean value of X')

    f=plt.figure()
    plt.hist((Y - Y.mean()) * 100, 30)
    plt.xlabel('Y[cm]'), plt.ylabel('counts[-]'), plt.title('Histogram of Y values deviations from mean value of Y')

    f=plt.figure()
    plt.scatter(xhall_offset * 100, yhall_offset * 100, marker='.', alpha=0.1)
    plt.axis('equal'), plt.xlabel('X [cm]'), plt.ylabel('Y [cm]')
    plt.title('X and Y hall position offset of dws from reference')

    #plt.show()

def dws_arm_dynamic_evaluation(directory,dws_name,arm_name,heading=0,plotting=False,verbose=True):
    '''
    calculate the time, angle offset of dws and arm with distance error interval
    :param directory:
    :param dws_name:
    :param arm_name:
    :param plotting:
    :param verbose:
    :return:
    '''

    RADIUS = 2.981
    PLOTTING = plotting
    VERBOSE = verbose
    dir = directory
    dwsname = dws_name
    armname = arm_name

    dwsfilename = os.path.join(dir,dwsname)
    armfilename = os.path.join(dir,armname)

    # import dws and arm data
    dws = pd.read_csv(dwsfilename)
    arm = pd.read_csv(armfilename)

    # fit spline to arm data and interpolate it to dws times
    Xarm_in_dws_time = spline_fit_prediction(arm.Time,arm.Xarm,dws.Time)
    Yarm_in_dws_time = spline_fit_prediction(arm.Time, arm.Yarm, dws.Time)

    dT_X = Xarm_in_dws_time - dws.ENU_X_norm
    dT_x2 = (dT_X)**2
    RMSE_dT_x = np.sqrt(np.mean(dT_x2)) * 100
    mean_dT_X,std_dT_X = signal_mean_std(dT_X)

    dT_Y = Yarm_in_dws_time - dws.ENU_Y_norm
    dT_y2 = (dT_Y)**2
    RMSE_dT_y = np.sqrt(np.mean(dT_y2)) * 100
    mean_dT_Y,std_dT_Y = signal_mean_std(dT_Y)

    RMSE_xy = np.sqrt(np.mean(dT_x2 + dT_y2))
    mean_xy = np.mean(np.sqrt(dT_x2 + dT_y2))
    std_xy = np.sqrt(std_dT_X**2 + std_dT_Y**2)

    # Heading evaluation
    Arm_Angle_in_dws_time = spline_fit_prediction(arm.Time, arm.ENCangle, dws.Time) # arm heading to dws times
    dws_heading = dws.Heading.as_matrix() + 90 # rotate the heading
    dmask = dws_heading >= 360
    dws_heading[dmask] -= 360

    arm_heading = heading - Arm_Angle_in_dws_time # heading is the initial heading of the hall probe
    amask = arm_heading < 0
    arm_heading[amask] += 360

    dheading = dws_heading - arm_heading # heading difference of arm and dws
    dhmask = abs(dheading) < 4 # outliers removal
    dheading = dheading[dhmask]

    RMSE_dheading = np.sqrt(np.mean(dheading))
    mean_dheading,std_dheading = signal_mean_std(dheading)

    if VERBOSE:
        print_line()
        print ('                    DYNAMIC MEASUREMENT')
        print_line()
        print ('RMSE x:(',RMSE_dT_x,') [cm]')
        print ('RMSE y:(',RMSE_dT_y,') [cm]')
        print ('RMSE XY (from time shift of x and y):(', RMSE_xy * 100, ') [cm]')
        print_line()
        print ('Mean and std of X offset from ref [cm]',mean_dT_X*100,'+/-',std_dT_X*100)
        print ('Mean and and std of Y offset from ref [cm]', mean_dT_Y * 100, '+/-', std_dT_Y * 100)
        print ('Mean and std of XY offset from ref [cm]',mean_xy * 100,'+/-',std_xy * 100)
        print_line()
        print ('RMSE heading [deg]:',RMSE_dheading)
        print ('Mean heading error and std [deg]:',mean_dheading,'+/-',std_dheading)

    #####################################################################################
    # Uncertainty circle calculation
    t = np.arange(0,2*np.pi,0.01*np.pi)
    x_uc2 = mean_dT_X * 100 + std_dT_X *100* np.sin(t)
    y_uc2 = mean_dT_Y * 100 + std_dT_Y *100* np.cos(t)

    if PLOTTING:
        f=plt.figure()
        plt.plot(dws.Time[dhmask],dheading,'.')
        plt.xlabel('Time [sec]')
        plt.ylabel('Heading error [deg]')
        plt.title('Difference between arm and dws heading')

        f=plt.figure()
        plt.plot(dws.Time,dT_X.abs() * 100,'.')
        plt.xlabel('Time [sec]'),plt.ylabel('abs(X coords diff) [cm]')
        plt.title('abs(X coords difference) of Dewesoft and ARM')

        f=plt.figure()
        plt.plot(dws.Time,dT_Y.abs() * 100,'.')
        plt.xlabel('Time [sec]'),plt.ylabel('abs(Y coords diff) [cm]')
        plt.title('abs(Y coords difference) of Dewesoft and ARM')

        f=plt.figure()
        plt.hist(dT_X.abs() * 100,50)
        plt.xlabel('abs(X coords diff) [cm]'),plt.ylabel('counts [-]')
        plt.title('Histogram of abs(X coords difference) of Dewesoft and ARM')

        f=plt.figure()
        plt.hist(dT_Y.abs() * 100,50)
        plt.xlabel('abs(Y coords diff) [cm]'),plt.ylabel('counts [-]'),plt.title('Histogram of abs(Y coords difference) of Dewesoft and ARM')

        f=plt.figure()
        plt.scatter(dT_X * 100,dT_Y * 100,marker='.',alpha=0.5)
        # plt.plot(x_uc,y_uc,'r')
        plt.plot(x_uc2, y_uc2,'r')
        plt.axis('equal')
        plt.xlabel('X coords diff [cm]'),plt.ylabel('Y coords diff [cm]')
        plt.title('X and Y coords difference of Dewesoft and ARM')
        plt.legend(['1sigma','XY errors'])
        plt.show()
