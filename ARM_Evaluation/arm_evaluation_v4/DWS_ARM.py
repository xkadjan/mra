import numpy as np
import pandas as pd
import os
import dws_arm_helper as dah

class Arm_Processor(object):
    def __init__(self,arm_path,wgs_ref1,wgs_ref2,ENC_resolution=5000,Radius=3,time_lists=[[0,0]]):
        heading = dah.bearing(wgs_ref1, wgs_ref2)

        self.ARMPATH = arm_path
        self.PHASE = np.deg2rad(360 - heading + 90)
        self.ECN_RESOLUTION = ENC_resolution
        self.RADIUS = Radius
        self.COR = [0,0]
        self._time_list = time_lists
        self._arm_data = None
        self._hall_times = None
        self._owntime = None

    def arm_extractor(self):
        '''
        Imports and cleans raw arm data
        :param path
        :return: raw arm data
        '''
        data = pd.read_fwf(self.ARMPATH,
                           widths=[10, 1, 1, 2, 4, 7, 2, 1, 1, 1, 1, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3],
                           skiprows=4, header=None, skipfooter=2)
        # data = pd.read_fwf(path,widths = [10,1,1,2,4,7,2,1,1,1,1,2,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3],skiprows = 4, header = None, skipfooter = 2)
        data.drop(labels=[1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25], axis=1, inplace=True)
        data.rename(
            columns={0: 'Log_Time', 4: 'ID', 10: 'Bytes', 12: 1, 14: 2, 16: 3, 18: 4, 20: 5, 22: 6, 24: 7, 26: 8},
            inplace=True)
        # data.rename(columns={4: 'ID', 12: 1, 14: 2, 16: 3, 18: 4, 20: 5, 22: 6, 24: 7, 26: 8}, inplace=True)
        try:
            dropers = data.index[data.ID == '768'].tolist()

        except Exception:
            dropers = data.index[data.ID == 768].tolist()

        if dropers:
            data.drop(data.index[dropers[0]:], inplace=True)

        data = data.fillna(value=0)

        data.ID = data.ID.astype('int')
        cols_to_check = ['Bytes', 1, 2, 3, 4, 5, 6, 7, 8]
        for col in cols_to_check:
            if not isinstance(data[col].iloc[6], float):
                data[col] = data[col].astype(float)

        return data

    def Byte4_converter(self,c1, c2, c3, c4):
        '''
        4 byte message conversion
        '''
        return c1 * 16777216 + c2 * 65536 + c3 * 256 + c4

    def Bytes2dec(self,b1, b2, b3, b4):

        bn1 = int(b4) << 24
        bn2 = int(b3) << 16
        bn3 = int(b2) << 8
        bn4 = int(b1)
        n = bn1 | bn2 | bn3 | bn4
        bn = bin(n)

        e = int(bn[2:10], 2) - 127
        mantissa = (int(bn[10:], 2)) / 2. ** 23

        return (1 + mantissa) * 2 ** e

    def DetaTime2sec(self,hr, min, sec, milis=0):
        return hr * 3600 + min * 60 + sec + milis / 1000

    def arm_parser(self,data,msgID):
        '''

        :param data: raw data
        :param msgID: eg. 1040,1025,...
        :return data_out: parsed message according to ID
        '''
        ID_name = {1025: 'PPStime', 1026: 'PPSnum', 1040: 'HALLtime', 1041: 'HALLnum', 1056: 'ENCtime', 1057: 'ENCnum',
                   1570: 'Lon', 1571: 'Lat', 1572: 'Alt', 1575: 'Daysec', 1576: 'PPS'}

        if msgID == 1024:
            nmeacode = data[data.ID == 1024]
            nmeatime = nmeacode.iloc[0] - 48
            data_out = (nmeatime[1] * 10 + nmeatime[2]) * 3600 + (nmeatime[3] * 10 + nmeatime[4]) * 60 + nmeatime[
                                                                                                             5] * 10 + \
                       nmeatime[6]
            return data_out

        else:
            selection = data[data.ID == msgID]

            if msgID == 1570 or msgID == 1571 or msgID == 1572:
                outpt = selection.apply(lambda row: self.Bytes2dec(row[1], row[2], row[3], row[4]), axis=1)

            elif msgID == 1025 or msgID == 1026 or msgID == 1040 or msgID == 1041 or msgID == 1056 or msgID == 1057:
                outpt = selection.apply(lambda row: self.Byte4_converter(row[1], row[2], row[3], row[4]), axis=1)

            elif msgID == 1575:
                # takes byte 4 5 6 and convert to seconds of day
                outpt = selection.apply(lambda row: self.DetaTime2sec(row[4], row[5], row[6]), axis=1)

            elif msgID == 1576:
                outpt = selection[1]


            data_out = outpt.reset_index(drop=True)

            if msgID == 1025:
                nans = selection.iloc[0].count()
                if nans == 8:
                    newpps = selection.iloc[0] - 48
                    ps = int(newpps[1] * 1e6 + newpps[2] * 1e5 + newpps[3] * 1e4 + newpps[4] * 1e3 + newpps[5] * 1e2 +
                             newpps[6] * 10 + newpps[7])
                    data_out.set_value(0, ps)
        return data_out

    def orientation_adjustement(self):
        if (self.COR[0] > self.HALL[0]) and (self.COR[1] < self.HALL[1]):
            rshift = -1
            ashift = -1
            return rshift,ashift
        elif (self.COR[0] > self.HALL[0]) and (self.COR[1] > self.HALL[1]):
            rshift = -1
            ashift = 1
            return rshift,ashift
        elif (self.COR[0] < self.HALL[0]) and (self.COR[1] > self.HALL[1]):
            rshift = 1
            ashift = -1
            return rshift,ashift
        elif (self.COR[0] < self.HALL[0]) and (self.COR[1] < self.HALL[1]):
            rshift = 1
            ashift = 1
            return rshift,ashift

    def arm_processor(self):
        """

        :param time_list:
        :return: armPositions
        """
        ENC_resolution = self.ECN_RESOLUTION
        Radius = self.RADIUS
        COR = self.COR
        
        print ('Processing', self.ARMPATH)

        # load ASC data file
        arm = self.arm_extractor()

        fixtimesec = self.arm_parser(arm, 1024)

        ppsnum = self.arm_parser(arm, 1026)
        ppstime = self.arm_parser(arm, 1025)
        sensorPPS = pd.DataFrame({'PPSnum': ppsnum, 'PPStime': ppstime})

        hallnum = self.arm_parser(arm, 1041)
        halltime = self.arm_parser(arm, 1040)
        sensorHALL = pd.DataFrame({'HALLnum': hallnum, 'HALLtime': halltime})

        encnum = self.arm_parser(arm, 1057)
        enctime = self.arm_parser(arm, 1056)
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
        lastoff = sensorENC.loc[mask, [9]]
        if not lastoff.empty:
            sensorENC.loc[mask, [9]] = sensorENC.loc[mask, [9]] + ENC_resolution - lastoff.iloc[len(lastoff) - 1]

        sensorENC[10] = sensorENC[9] * 360 / ENC_resolution
        sensorENC[11] = np.radians(sensorENC[10])


        sensorENC[12] = r * np.cos(sensorENC[11] + self.PHASE)
        sensorENC[13] = r * np.sin(sensorENC[11] + self.PHASE)


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

        self._hall_times = sensorHALL[8]
        self._arm_data = armPositions
        
        return ENC_resolution,Radius,arm,sensorPPS,sensorPPSuError,sensorHALL,sensorENC,armPositions

    def _timeframe_selector(self):
        arm_start = self._arm_data.Time.iloc[0]
        arm_stop = self._arm_data.Time.iloc[-1]
        # find which list of times is applicable for this ASC file
        for times in self._time_list:
            if (times[0] >= arm_start) and (times[1] <= arm_stop):
                time_cut = times
                break
            elif (times[0] == 0) and (times[1] == 0):
                time_cut = times
                break
            else:
                time_cut = [0,0]

        self._owntime = time_cut
        thall = self._hall_times
        thall = dah.extract_np_signal(thall,time_cut)

        armpositions = dah.extract_np_signal(self._arm_data,time_cut,series='Time')
        m = armpositions.shape[0] - len(thall)
        hallnans = np.empty([m, 1])
        hallnans[:] = np.nan
        halltimes = np.append(thall, hallnans)
        armpositions['Hall_times'] = halltimes
        return armpositions

    def arm_exporter(self):

        root = os.path.dirname(self.ARMPATH)
        result_dir = os.path.join(root, 'Processed')
        # file name extraction for later csv write of results
        filename = os.path.basename(self.ARMPATH)
        fsplit = filename.split('.')

        data = self._timeframe_selector()
        start = self._owntime[0]
        stop = self._owntime[1]

        csvfile = '\\Arm_' + fsplit[0] + '_' + str(start) + '_' + str(stop) + '_processed.csv'
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        outpath = result_dir
        outpath = outpath + csvfile  # final ARM processed output filepath to the csv write
        data.to_csv(outpath)

class DWS_Processor(object):
    def __init__(self,dwspath,wgs_ref,wgs_ref2,radius=2.981,time_lists=[[0,0]],hall_times=[0,0]):
        self.DWSPATH = dwspath
        self.WGSREF = wgs_ref
        self.WGSREF2 = wgs_ref2
        self._time_list = time_lists
        self._hall_time = hall_times
        self.RADIUS = radius
        self._data = None

    def wgs2ECEF(self,wgs):
        a = 6378137
        b = 6.356752314252350e+06
        e2 = 0.006694379987901
        xyz = np.zeros((len(wgs), 3))

        N = a / (np.sqrt(1 - e2 * (np.sin(wgs[:, 0])) ** 2))
        xyz[:, 0] = (N + wgs[:, 2]) * np.cos(wgs[:, 0]) * np.cos(wgs[:, 1])
        xyz[:, 1] = (N + wgs[:, 2]) * np.cos(wgs[:, 0]) * np.sin(wgs[:, 1])
        xyz[:, 2] = (((b / a) ** 2) * N + wgs[:, 2]) * np.sin(wgs[:, 0])

        return xyz

    def wgs2enu(self,wgs):
        xyz_ref = self.wgs2ECEF(self.WGSREF)
        wgs_ref = self.WGSREF
        xyz = self.wgs2ECEF(wgs)

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

    def dws_processor(self):
        '''
        processing dws data
        :param filepath:
        :param wgs_ref:
        :param export_csv:
        :return:
        '''
        cols2drop = ['System_status', 'GNSS_status']
        cols2rename = {'Latitude': 'Lat', 'Longitude': 'Lon'}

        # read the file from the csv
        DS = pd.read_csv(self.DWSPATH)
        # drop not useful labels
        DS.drop(labels=cols2drop, axis=1, inplace=True)
        # timestamp processing
        stamp = DS.datetime.apply(lambda row: row.rsplit(' ', 1)[1])
        stampspl = stamp.apply(lambda row: row.split(':'))
        DS.datetime = stampspl

        DS[['hours', 'minutes', 'sec']] = pd.DataFrame(DS.datetime.values.tolist(), index=DS.index)

        DS.drop(labels=['datetime'], axis=1, inplace=True)

        DS.hours = DS.hours.astype('int')
        DS.minutes = DS.minutes.astype('int')
        DS.sec = DS.sec.astype('int')
        # calculating time in seconds
        DS['Time'] = DS.hours * 3600 + DS.minutes * 60 + DS.sec + DS.micro / 1000000
        colnames = DS.columns.tolist()
        colnames.pop(colnames.index('Time'))
        colnames.insert(0, 'Time')
        DS = DS[colnames]

        DS.drop(labels=['hours', 'minutes', 'sec', 'micro'], axis=1, inplace=True)
        DS.rename(columns=cols2rename, inplace=True)

        # MINUTES TO DEGREES
        DS.Lat = DS.Lat / 60
        DS.Lon = DS.Lon / 60

        # DEG to RAD
        DS['Lat_rad'] = DS.Lat * np.pi / 180
        DS['Lon_rad'] = DS.Lon * np.pi / 180

        wgs_ref1 = self.WGSREF.copy()

        bearings = dah.bearing(wgs_ref1, self.WGSREF2)

        self.WGSREF[0, [0, 1]] = self.WGSREF[0, [0, 1]] * np.pi / 180

        wgs = DS[['Lat_rad', 'Lon_rad', 'Height']]
        wgs = wgs.as_matrix()

        enu = self.wgs2enu(wgs)
        DS['ENU_X'] = enu[:, 0]
        DS['ENU_Y'] = enu[:, 1]
        DS['ENU_Z'] = enu[:, 2]


        df = dah.extract_np_signal(DS, self._hall_time, 'Time')
        _Hall_frame = df.copy()

        Hall_Lat_mean = _Hall_frame.Lat_rad.mean()
        Hall_Lon_mean = _Hall_frame.Lon_rad.mean()
        Hall_Height_mean = _Hall_frame.Height.mean()
        wgs_cor_rad = dah.wgsPoint([Hall_Lat_mean, Hall_Lon_mean, Hall_Height_mean], bearings - 180, self.RADIUS)

        COR_ENU = self.wgs2enu(wgs_cor_rad)
        DS['ENU_X_norm'] = DS.ENU_X - COR_ENU[:, 0]
        DS['ENU_Y_norm'] = DS.ENU_Y - COR_ENU[:, 1]
        print ('Shift from the reference is X=', COR_ENU[:, 0] * 100, 'Y=', COR_ENU[:, 1] * 100, '[cm]')
        self._data = DS

    def dws_exporter(self):
        root = os.path.dirname(self.DWSPATH)
        result_dir = os.path.join(root, 'Processed')

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        for slice in self._time_list:
            start = slice[0]
            stop = slice[1]

            if start == 0 and stop == 0:
                filename = 'DWS_full' + '.csv'
                filepath_out = os.path.join(result_dir, filename)
                self._data.to_csv(filepath_out, index=False)
                break
            elif start > stop:
                raise Exception('In the time_list start must be lower than stop')

            filename = 'DWS_' + str(start) + '_' + str(stop) + '.csv'
            filepath_out = os.path.join(result_dir, filename)
            df = dah.extract_np_signal(self._data, slice, 'Time')
            df.to_csv(filepath_out, index=False)


        start = self._hall_time[0]
        stop = self._hall_time[1]

        if start == 0 and stop == 0:
            raise Exception('In the time_list start and stop must be non-zero')
        elif start > stop:
            raise Exception('In the time_list start must be lower than stop')

        filename = 'DWS_' + 'hall' + str(start) + '_' + str(stop) + '.csv'
        filepath_out = os.path.join(result_dir, filename)
        df = dah.extract_np_signal(self._data, self._hall_time, 'Time')
        df.to_csv(filepath_out, index=False)


