# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:16:34 2020

@author: xkadj
"""

# =============================================================================
# DEWESOFT:
# =============================================================================
import os
import pandas as pd


dewsoft_files = os.listdir(dir_rtk)
dewesoft_csvs = [i for i in dewsoft_files if 'csv' in i]
dewesoft_csvs_paths = [os.path.join(dir_rtk, name) for name in dewesoft_csvs]

#header = ['lat', 'lon', 'height', 'utc_time', 'east_row', 'north_row', 'up_row', 'utc_time_2']
#for file in [novatel_csvs_paths[7]]:
for file in dewesoft_csvs_paths:
#    dewesoft = pd.read_csv(file, sep=',', names=header , engine='python')#.values.tolist()
    dewesoft = pd.read_csv(file, sep=';', engine='python')#.values.tolist()

#    dewesoft["utc_time"] = dewesoft.utc_time % 86400

#    dewesoft.insert(len(dewesoft.count()), 'lat_in_rad', dewesoft.lat*np.pi/180, allow_duplicates=False)
#    dewesoft.insert(len(dewesoft.count()), 'lon_in_rad', dewesoft.lon*np.pi/180, allow_duplicates=False)
#
#    xyz = transpos.wgs2xyz(dewesoft[['lat_in_rad','lon_in_rad','height']].values)
#    enu = transpos.xyz2enu(xyz,wgs_ref)
#
#    dewesoft["east"], dewesoft["north"], dewesoft["up"] = enu.T[0], enu.T[1], enu.T[2]
    dewesoft = dewesoft[["utc_time","lat","lon","height","east","north","up"]]
    print(' - dewesoft loading done, ' + str(len(dewesoft)) + ' points')

    dewesoft["east"] = dewesoft.east - 0.59
    dewesoft["north"] = dewesoft.north - 0.588

    filename = file.split("\\")[-1][:-4]
    plot.plot_EN(dewesoft, filename, "b")
    plot.plot_utcE(dewesoft, filename, "b")