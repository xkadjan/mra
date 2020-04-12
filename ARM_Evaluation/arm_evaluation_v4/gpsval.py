import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.interpolate import splrep,splev
from scipy.signal import hilbert
from matplotlib.patches import Ellipse

def arm_import_data(path):
    '''
    Imports and cleans raw arm data
    :param path
    :return: raw arm data
    '''
    data = pd.read_fwf(path, widths=[10, 1, 1, 2, 4, 7, 2, 1, 1, 1, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
                       skiprows=4, header=None, skipfooter=2)
    #data = pd.read_fwf(path,widths = [10,1,1,2,4,7,2,1,1,1,1,2,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3],skiprows = 4, header = None, skipfooter = 2)
    data.drop(labels=[1,2,3,5,6,7,8,9,11,13,15,17,19,21,23,25],axis = 1, inplace = True)
    data.rename(columns = {0:'Log_Time',4:'ID',10:'Bytes',12:1,14:2,16:3,18:4,20:5,22:6,24:7,26:8},inplace = True)
    #data.rename(columns={4: 'ID', 12: 1, 14: 2, 16: 3, 18: 4, 20: 5, 22: 6, 24: 7, 26: 8}, inplace=True)
    try:
        dropers = data.index[data.ID == '768'].tolist()

    except Exception:
        dropers = data.index[data.ID == 768].tolist()

    if dropers:
        if (data.shape[0]-1) == dropers[0]:
            data.drop(data.index[dropers[0]], inplace=True)
        else:
            data.drop(data.index[dropers[0]:], inplace=True)

    data = data.fillna(value=0)

    data.ID = data.ID.astype('int')
    cols_to_check = ['Bytes',1,2,3,4,5,6,7,8]
    for col in cols_to_check:
        if not isinstance(data[col].iloc[6],float):
            data[col] = data[col].astype(float)


    return data

def Byte4_converter(c1,c2,c3,c4):
    '''
    4 byte message conversion
    '''
    return c1*16777216 + c2*65536 + c3*256 + c4

def Bytes2dec(b1,b2,b3,b4):

    bn1 = int(b4) << 24
    bn2 = int(b3) << 16
    bn3 = int(b2) << 8
    bn4 = int(b1)
    n = bn1 | bn2 | bn3 | bn4
    bn = bin(n)

    e = int(bn[2:10], 2) - 127
    mantissa = (int(bn[10:], 2)) / 2. ** 23

    return (1 + mantissa) * 2 ** e

def DetaTime2sec(hr,min,sec,milis = 0):
    return hr * 3600 + min * 60 + sec + milis/1000

def parse_data(data,msgID,logtime=False):
    '''

    :param data: raw data
    :param msgID: eg. 1040,1025,...
    :return data_out: parsed message according to ID
    '''
    ID_name = {1025:'PPStime',1026:'PPSnum',1040:'HALLtime',1041:'HALLnum',1056:'ENCtime',1057:'ENCnum',
             1570:'Lon',1571:'Lat',1572:'Alt',1575:'Daysec',1576:'PPS'}

    if msgID == 1024:
        nmeacode = data[data.ID == 1024]
        nmeatime = nmeacode.iloc[0] - 48
        data_out = (nmeatime[1] * 10 + nmeatime[2]) * 3600 + (nmeatime[3] * 10 + nmeatime[4]) * 60 + nmeatime[5] * 10 + nmeatime[6]
        return data_out

    else:
        selection = data[data.ID == msgID]

        if msgID == 1570 or msgID == 1571 or msgID == 1572:
            outpt = selection.apply(lambda row: Bytes2dec(row[1], row[2], row[3], row[4]), axis = 1)

        elif msgID == 1025 or msgID == 1026 or msgID == 1040 or msgID == 1041 or msgID == 1056 or msgID == 1057:
            outpt = selection.apply(lambda row: Byte4_converter(row[1], row[2], row[3], row[4]), axis = 1)

        elif msgID == 1575:
            # takes byte 4 5 6 and convert to seconds of day
            outpt = selection.apply(lambda row: DetaTime2sec(row[4],row[5],row[6]), axis = 1)

        elif msgID == 1576:
            outpt = selection[1]

        if logtime:
            series = outpt.reset_index(drop = True)
            t = selection.Log_Time.reset_index(drop=True)

            data_out = series.to_frame(ID_name[msgID])
            log_time_name = ID_name[msgID] + '_Log_Time'
            data_out[log_time_name] = t
        else:
            data_out = outpt.reset_index(drop = True)

        if msgID == 1025:
            nans = selection.iloc[0].count()
            if nans == 8:
                newpps = selection.iloc[0] - 48
                ps = int(newpps[1]*1e6+newpps[2]*1e5+newpps[3]*1e4+newpps[4]*1e3+newpps[5]*1e2+newpps[6]*10+newpps[7])
                data_out.set_value(0,ps)
    return data_out

def wgs2xyz(wgs):
    '''
    conversion from wgs to xyz
    :param wgs: [lat lon h], lat and lon in radians
    :return: xyz [x y z]
    '''
    a = 6378137
    e2 = 0.006694379987901

    xyz = np.zeros((len(wgs),3))


    dnm = np.sqrt(1 + (1 - e2) * np.tan(wgs[:,0])**2)
    xyz[:,0] = a * np.cos(wgs[:,1])/ dnm + wgs[:,2]*np.cos(wgs[:,1])*np.cos(wgs[:,0])
    xyz[:,1] = a * np.sin(wgs[:,1])/ dnm + wgs[:,2]*np.sin(wgs[:,1])*np.cos(wgs[:,0])
    xyz[:,2] = a * (1 - e2) * np.sin(wgs[:,0])/ np.sqrt(1 - e2 * np.sin(wgs[:,0])**2)+wgs[:,2]*np.sin(wgs[:,0])

    return xyz

def xyz2enu(xyz,wgs_ref,method = 'def'):
    if method == 'ECEF':
        xyz_ref = wgs2ECEF(wgs_ref)
    else:
        xyz_ref = wgs2xyz(wgs_ref)

    xyz[:,0] = xyz[:,0] - xyz_ref[0,0]
    xyz[:,1] = xyz[:,1] - xyz_ref[0,1]
    xyz[:,2] = xyz[:,2] - xyz_ref[0,2]

    R = np.array([[-np.sin(wgs_ref[0,1]), np.cos(wgs_ref[0,1]), 0],
                  [-np.cos(wgs_ref[0,1])*np.sin(wgs_ref[0,0]), -np.sin(wgs_ref[0,1])*np.sin(wgs_ref[0,0]),np.cos(wgs_ref[0,0])],
                  [np.cos(wgs_ref[0,1])*np.cos(wgs_ref[0,0]), np.sin(wgs_ref[0,1])*np.cos(wgs_ref[0,0]),np.sin(wgs_ref[0,0])]])
    enu = np.dot(xyz,R.T)
    return enu

def wgs2ECEF(wgs):
    a = 6378137
    b = 6.356752314252350e+06
    e2 = 0.006694379987901
    xyz = np.zeros((len(wgs), 3))


    N = a/(np.sqrt(1 - e2*(np.sin(wgs[:,0]))**2))
    xyz[:,0] = (N + wgs[:,2]) * np.cos(wgs[:,0]) * np.cos(wgs[:,1])
    xyz[:,1] = (N + wgs[:,2]) * np.cos(wgs[:,0]) * np.sin(wgs[:,1])
    xyz[:,2] = (((b/a)**2)*N + wgs[:,2]) * np.sin(wgs[:,0])

    return xyz

def wgs2enu(wgs,wgs_ref):
    xyz_ref = wgs2ECEF(wgs_ref)
    xyz = wgs2ECEF(wgs)

    xyz[:, 0] = xyz[:, 0] - xyz_ref[0, 0]
    xyz[:, 1] = xyz[:, 1] - xyz_ref[0, 1]
    xyz[:, 2] = xyz[:, 2] - xyz_ref[0, 2]

    R = np.array([[-np.sin(wgs_ref[0, 1]), np.cos(wgs_ref[0, 1]), 0],
                  [-np.cos(wgs_ref[0, 1]) * np.sin(wgs_ref[0, 0]), -np.sin(wgs_ref[0, 1]) * np.sin(wgs_ref[0, 0]),
                   np.cos(wgs_ref[0, 0])],
                  [np.cos(wgs_ref[0, 1]) * np.cos(wgs_ref[0, 0]), np.sin(wgs_ref[0, 1]) * np.cos(wgs_ref[0, 0]),
                   np.sin(wgs_ref[0, 0])]])
    enu = np.dot(xyz, R.T)

    return enu

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

##############################################################
def ARM_Processing(ARM_path,time_list=[[0,0]],ENC_resolution=0.5,Radius=2.981,COR=[0,0],phase_shift=0,csvout=False):
    '''
    Processing of the raw ARM measurement

    :param ARM_path: whole path with file name of the ASC file
    :param Radius:
    :param COR:
    :param phase_shift:
    :return: armPositions
    '''
    print 'Processing',ARM_path
    DEBUGG = False
    # file name extraction for later csv write of results
    filename = os.path.basename(ARM_path)
    fsplit = filename.split('.')
    csvfile = '\\Arm_' + fsplit[0] + '_processed.csv'

    # load ASC data file
    arm = arm_import_data(ARM_path)

    fixtimesec = parse_data(arm, 1024)

    ppsnum = parse_data(arm, 1026)
    ppstime = parse_data(arm, 1025)
    sensorPPS = pd.DataFrame({'PPSnum': ppsnum, 'PPStime': ppstime})

    hallnum = parse_data(arm, 1041)
    halltime = parse_data(arm, 1040)
    sensorHALL = pd.DataFrame({'HALLnum': hallnum, 'HALLtime': halltime})

    encnum = parse_data(arm, 1057)
    enctime = parse_data(arm, 1056)

    sensorENC = pd.DataFrame({'ENCnum': encnum, 'ENCtime': enctime})

    ppsTdif = sensorPPS.PPStime.sub(sensorPPS.PPStime.shift(), fill_value=0)
    ppsNdif = 1000000 * sensorPPS.PPSnum.sub(sensorPPS.PPSnum.shift(), fill_value=0)
    relative_pps_time = (ppsNdif - ppsTdif)
    relative_pps_time[0] = 'NaN'
    sensorPPS['RelPPStime'] = relative_pps_time
    sensorPPSuFixTime = sensorPPS.PPStime[0]
    sensorPPSuError = sensorPPS.RelPPStime[2:len(relative_pps_time)].mean()

    sensorHALL[2] = sensorHALL.HALLtime - sensorPPSuFixTime
    sensorHALL[3] = sensorHALL[2] / 1000000
    sensorHALL[4] = np.floor(sensorPPSuError * sensorHALL[3].apply(np.floor))
    sensorHALL[5] = sensorHALL[2] + sensorHALL[4]
    sensorHALL[6] = sensorHALL[5] / 1000000
    sensorHALL[8] = fixtimesec + sensorHALL[6]

    sensorENC[2] = sensorENC.ENCtime * 1000 - sensorPPSuFixTime
    sensorENC[3] = sensorENC[2] / 1000000
    sensorENC[4] = np.floor(sensorPPSuError * sensorENC[3].apply(np.floor))
    sensorENC[5] = sensorENC[2] + sensorENC[4]
    sensorENC[6] = sensorENC[5] / 1000000

    lensENC = len(sensorENC)
    lensHALL = len(sensorHALL)

    cirnums = []
    for i in range(lensENC):
        numOfCircle = 0
        for j in range(lensHALL):

            if sensorENC[6].iloc[i] > sensorHALL[6].iloc[j]:
                numOfCircle += 1
        cirnums.append(numOfCircle)

    sensorENC[7] = cirnums

    units = []
    for i in range(lensHALL):
        numOfUnit = 0
        for j in range(lensENC):
            if sensorHALL.HALLnum[i] == sensorENC[7].iloc[j]:
                numOfUnit += 1
        units.append(numOfUnit)
    sensorHALL[7] = units

    xc = COR[0]
    yc = COR[1]
    r = Radius

    numOfDegree = 0
    numOfDegreeMem = 0

    col8 = [0]
    col9 = [0]
    for i in range(1, lensENC):
        if sensorENC[7].iloc[i] > sensorENC[7].iloc[i - 1]:
            numOfDegree = 1
            col9.append(sensorENC.ENCnum.iloc[i - 1] - numOfDegreeMem - col9[i - 1])
            numOfDegreeMem = sensorENC.ENCnum.iloc[i - 1]
        else:
            numOfDegree += 1
            col9.append(sensorENC.ENCnum.iloc[i] - numOfDegreeMem)

        col8.append(numOfDegree)
    sensorENC[8] = col8
    sensorENC[9] = col9

    mask = sensorENC[7] == 0
    lastoff = sensorENC.loc[mask, [8]]
    if not lastoff.empty:
        sensorENC.loc[mask, [8]] = sensorENC.loc[mask, [8]] + 720 - lastoff.iloc[len(lastoff) - 1]

    sensorENC[10] = sensorENC[8] * 360 / (720 / (ENC_resolution * 2))
    sensorENC[11] = sensorENC[8] * 2 * np.pi / (720 / (ENC_resolution * 2))
    sensorENC[12] = xc + r * np.cos(sensorENC[11] + phase_shift)
    sensorENC[13] = yc + r * np.sin(sensorENC[11] + phase_shift)

    diff6 = sensorENC[6].sub(sensorENC[6].shift(), fill_value=0)
    diff6[0] = 0
    sensorENC[14] = diff6

    armPositions = pd.DataFrame(sensorENC[['ENCnum', 6, 10, 12, 13, 14]])
    armPositions.rename(
        columns={'ENCnum': 'ENCnumber', 6: 'EventTime', 10: 'ENCangle', 12: 'Xarm', 13: 'Yarm', 14: 'TimeDif'},
        inplace=True)
    armPositions['Time'] = sensorENC[6] + fixtimesec
    colnames = armPositions.columns.tolist()
    colnames.pop(colnames.index('Time'))
    colnames.insert(0, 'Time')
    armPositions = armPositions[colnames]

    arm_start = armPositions.Time.iloc[0]
    arm_stop = armPositions.Time.iloc[-1]
    # find which list of times is applicable for this ASC file
    for times in time_list:
        if (times[0] >= arm_start) and (times[1] <= arm_stop):
            time_cut = times
            break
        elif (times[0] == 0) and (times[1] == 0):
            time_cut = times

    armPositions = extract_np_signal(armPositions, time_cut, 'Time')  # extract values that are in the time interval
    halltimes_cut = extract_np_signal(sensorHALL[8], time_cut)  # extract values that are in the time interval
    m = armPositions.shape[0] - len(halltimes_cut)
    hallnans = np.empty([m, 1])
    hallnans[:] = np.nan
    halltimes = np.append(halltimes_cut, hallnans)

    armPositions['Hall_times'] = halltimes  # add hall times to the DataFrame armPositions



    if csvout:
        root = os.path.dirname(ARM_path)
        result_dir = os.path.join(root, 'Processed')

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        outpath = result_dir
        outpath = outpath + csvfile  # final ARM processed output filepath to the csv write
        armPositions.to_csv(outpath)

    return armPositions

def process_dewesoft(filepath,wgs_ref,export_csv = False):
    '''
    processing dws data
    :param filepath:
    :param wgs_ref:
    :param export_csv:
    :return:
    '''
    cols2drop = ['System_status','GNSS_status']
    cols2rename = {'Latitude':'Lat','Longitude':'Lon'}

    # read the file from the csv
    DS = pd.read_csv(filepath)
    # drop not useful labels
    DS.drop(labels = cols2drop, axis = 1, inplace = True)
    # timestamp processing
    stamp = DS.datetime.apply(lambda row:row.rsplit(' ',1)[1])
    stampspl = stamp.apply(lambda row:row.split(':'))
    DS.datetime = stampspl

    DS[['hours','minutes','sec']] = pd.DataFrame(DS.datetime.values.tolist(), index= DS.index)

    DS.drop(labels = ['datetime'],axis = 1, inplace = True)

    DS.hours = DS.hours.astype('int')
    DS.minutes = DS.minutes.astype('int')
    DS.sec = DS.sec.astype('int')
    # calculating time in seconds
    DS['Time'] = DS.hours * 3600 + DS.minutes * 60 + DS.sec + DS.micro/1000000
    colnames = DS.columns.tolist()
    colnames.pop(colnames.index('Time'))
    colnames.insert(0, 'Time')
    DS = DS[colnames]

    DS.drop(labels = ['hours','minutes','sec','micro'], axis = 1, inplace = True)
    DS.rename(columns = cols2rename, inplace = True)

    # MINUTES TO DEGREES
    DS.Lat = DS.Lat/60
    DS.Lon = DS.Lon/60


    # DEG to RAD
    DS['Lat_rad'] = DS.Lat * np.pi / 180
    DS['Lon_rad'] = DS.Lon * np.pi / 180
    wgs_ref[0, [0, 1]] = wgs_ref[0, [0, 1]] * np.pi / 180

    wgs = DS[['Lat_rad', 'Lon_rad', 'Height']]
    wgs = wgs.as_matrix()


    enu = wgs2enu(wgs, wgs_ref)
    DS['ENU_X'] = enu[:,0]
    DS['ENU_Y'] = enu[:,1]
    DS['ENU_Z'] = enu[:,2]

    ecef = wgs2ECEF(wgs)
    DS['ECEF_X'] = ecef[:,0]
    DS['ECEF_Y'] = ecef[:,1]
    DS['ECEF_Z'] = ecef[:,2]

    if export_csv:
        root = os.path.dirname(filepath)
        result_dir = os.path.join(root, 'Processed')

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        dir_out = result_dir #os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        filename_out = filename.split('.')
        filename_out = filename_out[0] + '_processed.csv'
        filepath_out = os.path.join(dir_out,filename_out)
        DS.to_csv(filepath_out,index=False)

    return DS

def select_dataslices(dataframe,time_list,dir_path,export_csv = False):
    '''
    from the dewesoft dataframe extract part of the data within time list time intervals

    :param dataframe:
    :param time_list:
    :param export_path:
    :param export_csv:
    :return: list of extracted DataFrames
    '''
    FrameList = []
    for slice in time_list:
        start = slice[0]
        stop = slice[1]
        if start == 0 or stop == 0:
            raise  Exception('start or stop in the time_list cannot be zero')
        elif start > stop:
            raise  Exception('In the time_list start must be lower than stop')

        df = extract_np_signal(dataframe,slice,'Time')

        FrameList.append(df)
        if export_csv:
            root = dir_path
            result_dir = os.path.join(root, 'Processed')

            if not os.path.exists(result_dir):
                os.makedirs(result_dir)
            dir_out = result_dir
            filename = 'DataSlice_' + str(start) + '_' + str(stop) + '.csv'
            filepath_out = os.path.join(dir_out, filename)
            df.to_csv(filepath_out,index=False)

    return FrameList

def Kasa_circ_fit(XY):
    '''
    Circle fit to estimate circle parameters
    P = [XY ones(size(XY,1),1)] \ [XY(:,1).^2 + XY(:,2).^2];
    Par = [P(1)/2 , P(2)/2 , sqrt((P(1)^2+P(2)^2)/4+P(3))];
    linalg.lstsq(a,b)
    '''
    ons = np.ones((len(XY),1))
    Pa = np.hstack([XY,ons])
    Pb = XY[:,0]**2 + XY[:,1]**2
    P,res,b,c = np.linalg.lstsq(Pa,Pb)
    Par = [P[0]/2,P[1]/2,np.sqrt(((P[0])**2 + (P[1])**2)/4 + P[2])]

    return Par,np.sqrt(res)

def selection_mean_paras(Frames,verbose = 0):
    '''
    takes extracted frames and calculate for each a circle fit
    then averages the parameters
    :param Frames:
    :param verbose:
    :return: [avg_corx,avg_cory,avr_R]
    '''
    cor_x = list([])
    cor_y = list([])
    R = list([])
    for df in Frames:
        slice = df.copy()
        XY = slice.as_matrix(['ENU_X', 'ENU_Y'])
        pars,res = Kasa_circ_fit(XY)
        slice['ENU_X_corr'] = slice.ENU_X - pars[0]
        slice['ENU_Y_corr'] = slice.ENU_Y - pars[1]
        cor_x.append(pars[0])
        cor_y.append(pars[1])
        R.append(pars[2])

        if verbose:
            print pars,res

    avg_corx = np.mean(cor_x)
    avg_cory = np.mean(cor_y)
    avr_R = np.mean(R)

    return [avg_corx,avg_cory,avr_R]

def export_dws_arm(dirpath,wgs_ref,time_list,hall_time_list,wgs_ref2,verbose=False,CORest=False):
    '''
    export to the csv the dws, dws exctracted dataframes and arm files
    :param dirpath:
    :param wgs_ref:
    :param time_list:
    :param hall_time_list:
    :return:
    '''
    radius = 2.981

    wgs_ref1 = wgs_ref.copy()
    wgs_reff = wgs_ref.copy()
    dir = dirpath #r"c:\Users\mpavelka\Documents\MiscTests\hodnoceni GNSS pro Marka\12112017\valid_data"
    files = os.listdir(dir)

    ascs = [s for s in files if 'ASC' in s]
    csvs = [s for s in files if 'csv' in s]

    ascfilepaths = [os.path.join(dir, name) for name in ascs]
    csvfilepaths = [os.path.join(dir, name) for name in csvs]
    print 'Found these ASC and csv files:'
    print ascfilepaths
    print csvfilepaths

    bearings = bearing(wgs_ref1, wgs_ref2)
    phase = np.deg2rad(360 - bearings + 90)
    xhall_ref = 2.981 * np.cos(phase)
    yhall_ref = 2.981 * np.sin(phase)
    #
    # for ascfile in ascfilepaths:
    #     Arm = ARM_Processing(ascfile,time_list=time_list, phase_shift=phase,csvout=True)

    for csvfile in csvfilepaths:
        DS = process_dewesoft(csvfile, wgs_ref, export_csv=True)
        Frames = select_dataslices(DS, time_list, dir, export_csv=False) #extract time slices

        # XY offset correction
        if CORest:
            paras = selection_mean_paras(Frames)  # calculate the avg. shift in the origin position
            # center the data around the origin
            DS['ENU_X_norm'] = DS.ENU_X - paras[0]
            DS['ENU_Y_norm'] = DS.ENU_Y - paras[1]
            print 'Shift from the reference is X=', paras[0] * 100, 'Y=', paras[1] * 100, '[cm]'
        else:
            h = select_dataslices(DS, hall_time_list, dir)
            _Hall_frame = h[0].copy()

            Hall_Lat_mean = _Hall_frame.Lat_rad.mean()
            Hall_Lon_mean = _Hall_frame.Lon_rad.mean()
            Hall_Height_mean = _Hall_frame.Height.mean()
            wgs_cor_rad = wgsPoint([Hall_Lat_mean, Hall_Lon_mean, Hall_Height_mean], bearings - 180, radius)
            wgs_reff[0, [0, 1]] = wgs_reff[0, [0, 1]] * np.pi / 180
            COR_ENU = wgs2enu(wgs_cor_rad, wgs_reff)
            DS['ENU_X_norm'] = DS.ENU_X - COR_ENU[:,0]
            DS['ENU_Y_norm'] = DS.ENU_Y - COR_ENU[:,1]
            print 'Shift from the reference is X=', COR_ENU[:,0] * 100, 'Y=', COR_ENU[:,1] * 100, '[cm]'

        # export the extracted time slices
        Frames = select_dataslices(DS, time_list, dir, export_csv=True)

        # extract the time period when the dws was measuring hall position
        hFrames = select_dataslices(DS, hall_time_list, dir)
        Hall_frame = hFrames[0].copy()
        hall_x = Hall_frame.ENU_X_norm.mean()
        hall_y = Hall_frame.ENU_Y_norm.mean()
        std_hall_x = Hall_frame.ENU_X_norm.std()
        std_hall_y = Hall_frame.ENU_Y_norm.std()

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
        R95 = 2.08*(0.59*(std_xhall_offset+std_yhall_offset))

        dHX = Hall_frame.ENU_X_norm - hall_x
        dHY = Hall_frame.ENU_Y_norm - hall_y
        rmse_xy = np.sqrt(np.mean(dHX**2+dHY**2))*100
        # calculate the phase shift
        phaseshift = np.pi / 2 + np.arctan(abs(hall_x / hall_y))
        phasedeg = np.rad2deg(phaseshift)
        hallheading = 360 - (phasedeg - 90)

        difbearhall = bearings - hallheading


        if verbose:
            print 'X_hall_ref - X_dws.mean() ,static accuracy:', (xhall_ref - hall_x)*100,'[cm]'
            print 'Y_hall_ref - Y_dws.mean(),static accuracy:', (yhall_ref - hall_y) * 100, '[cm]'
            print '(XY_hall_ref - XY_dws).mean():',xyhall_offset_mean*100,'[cm]'
            print '(XY_hall_ref - XY_dws).std():',xyhall_offset_std*100,'[cm]'
            print 'R95:',R95*100,'[cm]'
            print 'RMSE X_hall_ref to X_dws:',x_hall_offset_rmse*100,'[cm]'
            print 'RMSE Y_hall_ref to Y_dws:', y_hall_offset_rmse * 100, '[cm]'
            print 'RMSE XY_hall_ref to XY_dws:',xy_hall_offset_rmse*100,'[cm]'
            print 'Std (dws_x - ref_x):',std_xhall_offset*100,'[cm]'
            print 'Std (dws_y - ref_y):', std_yhall_offset * 100, '[cm]'
            print '###################################################################'
            print 'Hall probe phase shift [deg] from X axis (east)',phasedeg
            print 'Hall probe heading [deg]', hallheading
            print 'Heading from the wgs refs [deg]', bearings
            print 'Difference of wgs refs bearing and Hall probe heading',difbearhall
        X = Hall_frame.ENU_X_norm.as_matrix()
        Y = Hall_frame.ENU_Y_norm.as_matrix()

        plt.figure(1)
        plt.scatter((X-X.mean()) * 100, (Y-Y.mean()) * 100,marker='.',alpha=0.1)
        plt.xlabel('X[cm]'), plt.ylabel('Y[cm]'), plt.title('XY static measurement deviations from mean')
        plt.axis('equal')

        plt.figure(2)
        plt.hist((X-X.mean())*100,30)
        plt.xlabel('X[cm]'),plt.ylabel('counts[-]'),plt.title('Histogram of X values deviations from mean value of X')

        plt.figure(3)
        plt.hist((Y - Y.mean()) * 100, 30)
        plt.xlabel('Y[cm]'), plt.ylabel('counts[-]'), plt.title('Histogram of Y values deviations from mean value of Y')

        plt.figure(4)
        plt.scatter(xhall_offset * 100, yhall_offset * 100, marker='.', alpha=0.1)
        plt.axis('equal'), plt.xlabel('X [cm]'), plt.ylabel('Y [cm]')
        plt.title('X and Y hall position offset of dws from reference')

        plt.show()
def lin_fit(X,y):

    a,b = np.polyfit(X,y,1)
    return a,b

def predict_lin_fit(X,fit_pars):

    a = fit_pars[0]
    b = fit_pars[1]

    prediction = X * a + b
    return prediction

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

def dws_arm_evaluation(directory,dws_name,arm_name,heading=0,plotting=False,verbose=True):
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
        print 'RMSE XY (from time shift of x and y):(',RMSE_xy*100,') [cm]'
        print 'RMSE x:(',RMSE_dT_x,') [cm]'
        print 'RMSE y:(',RMSE_dT_y,') [cm]'
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        print 'Mean X offset from ref [cm]',mean_dT_X*100,'+/-',std_dT_X*100
        print 'Mean Y offset from ref [cm]', mean_dT_Y * 100, '+/-', std_dT_Y * 100
        print 'Mean XY offset from ref [cm]',mean_xy * 100,'+/-',std_xy * 100
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        print 'RMSE heading [deg]:',RMSE_dheading
        print 'Mean heading error and std [deg]:',mean_dheading,'+/-',std_dheading

    #####################################################################################
    # Uncertainty circle calculation
    t = np.arange(0,2*np.pi,0.01*np.pi)
    x_uc2 = mean_dT_X * 100 + std_dT_X *100* np.sin(t)
    y_uc2 = mean_dT_Y * 100 + std_dT_Y *100* np.cos(t)

    if PLOTTING:
        plt.figure(1)
        plt.plot(dws.Time[dhmask],dheading,'.')
        plt.xlabel('Time [sec]')
        plt.ylabel('Heading error [deg]')
        plt.title('Difference between arm and dws heading')

        plt.figure(5)
        plt.plot(dws.Time,dT_X.abs() * 100,'.')
        plt.xlabel('Time [sec]'),plt.ylabel('abs(X coords diff) [cm]')
        plt.title('abs(X coords difference) of Dewesoft and ARM')

        plt.figure(6)
        plt.plot(dws.Time,dT_Y.abs() * 100,'.')
        plt.xlabel('Time [sec]'),plt.ylabel('abs(Y coords diff) [cm]')
        plt.title('abs(Y coords difference) of Dewesoft and ARM')

        plt.figure(7)
        plt.hist(dT_X.abs() * 100,50)
        plt.xlabel('abs(X coords diff) [cm]'),plt.ylabel('counts [-]')
        plt.title('Histogram of abs(X coords difference) of Dewesoft and ARM')

        plt.figure(8)
        plt.hist(dT_Y.abs() * 100,50)
        plt.xlabel('abs(Y coords diff) [cm]'),plt.ylabel('counts [-]'),plt.title('Histogram of abs(Y coords difference) of Dewesoft and ARM')

        plt.figure(10)
        plt.scatter(dT_X * 100,dT_Y * 100,marker='.',alpha=0.5)
        # plt.plot(x_uc,y_uc,'r')
        plt.plot(x_uc2, y_uc2,'r')
        plt.axis('equal')
        plt.xlabel('X coords diff [cm]'),plt.ylabel('Y coords diff [cm]')
        plt.title('X and Y coords difference of Dewesoft and ARM')
        plt.legend(['1sigma','XY errors'])
        plt.show()

def extract_np_signal(signal,time_interval,series=None):
    '''
    the function extracts the data from the signal within the time interval
    :param signal: signal can be np.ndarray,pd.series or pd.DataFrame
    :param time_interval:
    :param series:
    :return:
    '''
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

def view_raw_data(dir,wgs_ref):
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
        Arm = ARM_Processing(arm_path)
        plt.figure(f)
        plt.plot(Arm.Time, Arm.Xarm, '.')
        title = 'X arm ' + os.path.basename(arm_path)
        plt.title(title)
        f += 1
    # dws processing
    for dws_path in csvfilepaths:
        DS = process_dewesoft(dws_path, wgs_ref)
        plt.figure(f)
        plt.plot(DS.Time, DS.ENU_X, '.')
        title = 'X dws ' + os.path.basename(dws_path)
        plt.title(title)
        f += 1

    plt.show()

########################################################################################################################
def Peak_ARM_Processing(filepath, time_list=[[0, 0]], ENC_resolution=0.5, Radius=2.981, COR=[0, 0], phase_shift=0,
                   csvout=False):
    '''
    Processing of the raw ARM measurement

    :param ARM_path: whole path with file name of the ASC file
    :param Radius:
    :param COR:
    :param phase_shift:
    :return: armPositions
    '''
    print 'Processing', filepath
    DEBUGG = False
    # file name extraction for later csv write of results
    filename = os.path.basename(filepath)
    fsplit = filename.split('.')
    csvfile = '\\Arm_' + fsplit[0] + '_processed.csv'

    # load ASC data file
    arm = arm_import_data(filepath)

    fixtimesec = parse_data(arm, 1024,True)

    ppsnum = parse_data(arm, 1026,True)
    ppstime = parse_data(arm, 1025,True)
    sensorPPS = pd.merge(ppsnum,ppstime,left_index=True,right_index=True)

    hallnum = parse_data(arm, 1041,True)
    halltime = parse_data(arm, 1040,True)
    sensorHALL = pd.merge(hallnum,halltime,left_index=True,right_index=True)

    encnum = parse_data(arm, 1057,True)
    enctime = parse_data(arm, 1056,True)
    sensorENC = pd.merge(encnum,enctime,left_index=True,right_index=True)

    peak_Daysec = parse_data(arm,1575,True)
    Lon = parse_data(arm,1570,True)
    Lat = parse_data(arm, 1571, True)

    ppsTdif = sensorPPS.PPStime.sub(sensorPPS.PPStime.shift(), fill_value=0)
    ppsNdif = 1000000 * sensorPPS.PPSnum.sub(sensorPPS.PPSnum.shift(), fill_value=0)
    relative_pps_time = (ppsNdif - ppsTdif)
    relative_pps_time[0] = 'NaN'
    sensorPPS['RelPPStime'] = relative_pps_time
    sensorPPSuFixTime = sensorPPS.PPStime[0]
    sensorPPSuError = sensorPPS.RelPPStime[2:len(relative_pps_time)].mean()

    sensorHALL[2] = sensorHALL.HALLtime - sensorPPSuFixTime
    sensorHALL[3] = sensorHALL[2] / 1000000
    sensorHALL[4] = np.floor(sensorPPSuError * sensorHALL[3].apply(np.floor))
    sensorHALL[5] = sensorHALL[2] + sensorHALL[4]
    sensorHALL[6] = sensorHALL[5] / 1000000
    sensorHALL[8] = fixtimesec + sensorHALL[6]

    sensorENC[2] = sensorENC.ENCtime * 1000 - sensorPPSuFixTime
    sensorENC[3] = sensorENC[2] / 1000000
    sensorENC[4] = np.floor(sensorPPSuError * sensorENC[3].apply(np.floor))
    sensorENC[5] = sensorENC[2] + sensorENC[4]
    sensorENC[6] = sensorENC[5] / 1000000

    lensENC = len(sensorENC)
    lensHALL = len(sensorHALL)

    cirnums = []
    for i in range(lensENC):
        numOfCircle = 0
        for j in range(lensHALL):

            if sensorENC[6].iloc[i] > sensorHALL[6].iloc[j]:
                numOfCircle += 1
        cirnums.append(numOfCircle)

    sensorENC[7] = cirnums

    units = []
    for i in range(lensHALL):
        numOfUnit = 0
        for j in range(lensENC):
            if sensorHALL.HALLnum[i] == sensorENC[7].iloc[j]:
                numOfUnit += 1
        units.append(numOfUnit)
    sensorHALL[7] = units

    xc = COR[0]
    yc = COR[1]
    r = Radius

    numOfDegree = 0
    numOfDegreeMem = 0

    col8 = [0]
    col9 = [0]
    for i in range(1, lensENC):
        if sensorENC[7].iloc[i] > sensorENC[7].iloc[i - 1]:
            numOfDegree = 1
            col9.append(sensorENC.ENCnum.iloc[i - 1] - numOfDegreeMem - col9[i - 1])
            numOfDegreeMem = sensorENC.ENCnum.iloc[i - 1]
        else:
            numOfDegree += 1
            col9.append(sensorENC.ENCnum.iloc[i] - numOfDegreeMem)

        col8.append(numOfDegree)
    sensorENC[8] = col8
    sensorENC[9] = col9

    mask = sensorENC[7] == 0
    lastoff = sensorENC.loc[mask, [8]]
    if not lastoff.empty:
        sensorENC.loc[mask, [8]] = sensorENC.loc[mask, [8]] + 720 - lastoff.iloc[len(lastoff) - 1]

    sensorENC[10] = sensorENC[8] * 360 / (720 / (ENC_resolution * 2))
    sensorENC[11] = sensorENC[8] * 2 * np.pi / (720 / (ENC_resolution * 2))
    sensorENC[12] = xc + r * np.cos(sensorENC[11] + phase_shift)
    sensorENC[13] = yc + r * np.sin(sensorENC[11] + phase_shift)

    diff6 = sensorENC[6].sub(sensorENC[6].shift(), fill_value=0)
    diff6[0] = 0
    sensorENC[14] = diff6

    armPositions = pd.DataFrame(sensorENC[['ENCnum', 6, 8, 12, 13, 14]])
    armPositions.rename(
        columns={'ENCnum': 'ENCnumber', 6: 'EventTime', 8: 'ENCcounter', 12: 'Xarm', 13: 'Yarm', 14: 'TimeDif'},
        inplace=True)
    armPositions['Time'] = sensorENC[6] + fixtimesec

    peak_Daysec_rolled = TimeSpread(peak_Daysec)
    time_diff = Peak_Arm_Time_Offset(sensorENC.ENCtime_Log_Time,armPositions['Time'],peak_Daysec)

    print time_diff.mean(),time_diff.std()
    print InterpTime(peak_Daysec_rolled,34.419993)


    colnames = armPositions.columns.tolist()
    colnames.pop(colnames.index('Time'))
    colnames.insert(0, 'Time')
    armPositions = armPositions[colnames]

    arm_start = armPositions.Time.iloc[0]
    arm_stop = armPositions.Time.iloc[-1]
    # find which list of times is applicable for this ASC file
    for times in time_list:
        if (times[0] >= arm_start) and (times[1] <= arm_stop):
            time_cut = times
            break
        elif (times[0] == 0) and (times[1] == 0):
            time_cut = times

    armPositions = extract_np_signal(armPositions, time_cut, 'Time')  # extract values that are in the time interval
    halltimes_cut = extract_np_signal(sensorHALL[8], time_cut)  # extract values that are in the time interval
    m = armPositions.shape[0] - len(halltimes_cut)
    hallnans = np.empty([m, 1])
    hallnans[:] = np.nan
    halltimes = np.append(halltimes_cut, hallnans)

    armPositions['Hall_times'] = halltimes  # add hall times to the DataFrame armPositions

    plt.figure(1)
    plt.plot(sensorENC.ENCtime_Log_Time, armPositions['Time'], '.')
    plt.plot(peak_Daysec.Daysec_Log_Time, peak_Daysec.Daysec, '.')
    plt.plot(peak_Daysec_rolled[:, 1], peak_Daysec_rolled[:, 0], '.')

    plt.figure(2)
    plt.plot(Lat.Lat_Log_Time,Lat.Lat,'.')
    plt.show()

    if csvout:
        root = os.path.dirname(filepath)
        result_dir = os.path.join(root,'Processed')

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        outpath = result_dir
        outpath = outpath + csvfile  # final ARM processed output filepath to the csv write
        armPositions.to_csv(outpath)

    return armPositions

def TimeSpread(time):
    time = time.as_matrix()
    m = len(time)
    start = 1

    while time[start,0] == time[start-1,0]:
        start += 1
    newtime = np.zeros([m,2])
    inc = 0.1
    for i in range(start,m):
        if newtime[i-1, 0]+0.1 == time[i, 0]:
            newtime[i, 0] = time[i, 0]
        else:
            newtime[i, 0] = time[i, 0] + inc

        inc += 0.1
        if inc > 1:
            inc = 0.1

    newtime[:,1] = time[:,1]
    return newtime

def InterpTime(peak_time,sig_log_time):
    '''

    :param peak_time: peak_time[:,0] - dayseconds , peak_time[:,1] - Log_Time
    :param sig_log_time: second signal Log_Time
    :return:
    '''
    y = np.interp(sig_log_time,peak_time[:,1],peak_time[:,0])
    return y

def Peak_Arm_Time_Offset(ENC_Log_Time,Arm_Daysec,Peak_Dayesec):
    newtime = TimeSpread(Peak_Dayesec) # seconds of peak roll out
    peak_interp_time = InterpTime(newtime, ENC_Log_Time)
    dT = peak_interp_time - Arm_Daysec
    return dT
