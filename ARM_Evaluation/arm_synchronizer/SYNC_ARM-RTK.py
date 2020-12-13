# -*- coding: utf-8 -*-
"""
@author: xkadj
"""

import sync_armparser as arm_prs
import sync_rtk_parser as rtk_prs
import sync_rtk_evl as rtk_evl
import sync_plotting as plot

import configargparse
import os

def configArgParser():
    description = '   Measurement Robotic Arm (MRA), The MIT License (MIT), Copyright (c) 2019 CULS Prague TF\ndeveloped by: Jan Kaderabek\n'
    parser = configargparse.ArgParser(default_config_files=['config.ini'], description=description)
    parser.add('-da', '--dir_arm', type=str, help='path to MRA converted data')
    parser.add('-dr', '--dir_rtk', type=str, help='path to RTK data in NMEA GPGGA format')
    parser.add('-rr', '--result_dir', type=str, help='path to results')
    parser.add('-ref','--wgs_ref', type=lambda x: list(map(float,(str(x).split(',')))), help='reference point in center of rotation (in WGS84)')
    parser.add('-n','--rtk_names', type=lambda x: list(str(x).split(',')), help='names of evaluated RTK receivers')
    parser.add('-np', '--new_preproccess', type=lambda x: (str(x).lower() == 'true'), help='proccess MRA and DEWESOFT before evaluation')
    parser.add('-of','--only_fix', type=lambda x: (str(x).lower() == 'true'), help='evaluate only fix samples')
    parser.add('-p','--prefix', type=str, help='evaluate only sliced time')
    args = parser.parse()
    return args

def checkFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

print("MRA synchronizer started")

args = configArgParser()

if args.only_fix:
    measurement = 'FIX state epoch'
else:
    measurement = 'Whole measurement'

pltr = plot.Plotter(args)

# =============================================================================
# ARM:
# =============================================================================
if args.new_preproccess:
    arm = arm_prs.ArmParser(args)
    arm.parse_slices()
    arm.get_bad_cicles()
    arm.drop_peaks()
    arm.filter_signal()
    arm.drop_bad_circles()
    arm.drop_zero_speed()
    arm.drop_zero_acc()
    arm.drop_limit_acc()

# =============================================================================
# RTK
# =============================================================================
if args.new_preproccess:       
    rtk = rtk_prs.RtkParser(args,'kph')
    rtk.parse_slices()
    rtk.drop_points_wo_arm(arm.arm_20hz)
    rtk.drop_points_wo_rtk(arm.arm_20hz)
    rtk_list = rtk.concate_arm_and_rtks()
    
    rtk_static = rtk_prs.RtkParser(args,'static')
    rtk_static.parse_slices()
    rtk_static.create_static_reference()
    rtk_static_list = rtk_static.concate_static_and_rtks()   
    
# =============================================================================
# EVL
# =============================================================================
evl = rtk_evl.Evaluator()
if not args.new_preproccess:
    evl.csv_load(args.result_dir)
    rtk_list = evl.csv_load(checkFolder(args.result_dir))
evl.get_deviations(rtk_list)
if args.only_fix:
    evl.filter_fix()
# evl.filter_sigma()
# evl.abs_acc()
evl.get_make_boxes()
# evl.adjust_status()
evl.get_results(args.only_fix)
evl.csv_print(checkFolder(args.result_dir),args.new_preproccess)
evl.get_correlation()
evl.get_spearman()
evl.get_median()

evl_static = rtk_evl.Evaluator()
if not args.new_preproccess:
    evl_static.csv_load(args.result_dir)
    rtk_list = evl_static.csv_load(checkFolder(args.result_dir))
evl_static.get_deviations(rtk_static_list)
if args.only_fix:
    evl_static.filter_fix()
# evl_static.filter_sigma()
# evl_static.abs_acc()
evl_static.get_make_boxes()
# evl_static.adjust_status()
evl_static.get_results(args.only_fix)
evl_static.csv_print(checkFolder(args.result_dir),args.new_preproccess)
# evl_static.get_correlation()
# evl_static.get_spearman()
evl_static.get_median()

# =============================================================================
# PLOTTING - deviation histograms:
# =============================================================================

# Print deviations (The density of occurrence of horizontal deviations from the reference trajectory of the MRA in the latitude and longitude directions)
pltr.plot_hist(evl.novatel,args.rtk_names[0],evl.results_novatel.iloc[0],measurement,'dynamic')
pltr.plot_hist(evl.tersus,args.rtk_names[1],evl.results_tersus.iloc[0],measurement,'dynamic')
pltr.plot_hist(evl.ashtech,args.rtk_names[2],evl.results_ashtech.iloc[0],measurement,'dynamic')
pltr.plot_hist(evl.ublox,args.rtk_names[3],evl.results_ublox.iloc[0],measurement,'dynamic')

# Print density (The density of deviations)
pltr.plot_hist_dev(evl.novatel.deviation,args.rtk_names[0],evl.results_novatel.iloc[0],measurement,'dynamic')
pltr.plot_hist_dev(evl.tersus.deviation,args.rtk_names[1],evl.results_tersus.iloc[0],measurement,'dynamic')
pltr.plot_hist_dev(evl.ashtech.deviation,args.rtk_names[2],evl.results_ashtech.iloc[0],measurement,'dynamic')
pltr.plot_hist_dev(evl.ublox.deviation,args.rtk_names[3],evl.results_ublox.iloc[0],measurement,'dynamic')

pltr = plot.Plotter(args)
# Print deviations (The density of occurrence of horizontal deviations from the reference trajectory of the MRA in the latitude and longitude directions)
pltr.plot_hist(evl_static.novatel,args.rtk_names[0],evl_static.results_novatel.iloc[0],measurement,'static')
pltr.plot_hist(evl_static.tersus,args.rtk_names[1],evl_static.results_tersus.iloc[0],measurement,'static')
pltr.plot_hist(evl_static.ashtech,args.rtk_names[2],evl_static.results_ashtech.iloc[0],measurement,'static')
pltr.plot_hist(evl_static.ublox,args.rtk_names[3],evl_static.results_ublox.iloc[0],measurement,'static')

# Print density (The density of deviations)
pltr.plot_hist_dev(evl_static.novatel.deviation,args.rtk_names[0],evl_static.results_novatel.iloc[0],measurement,'dynamic')
pltr.plot_hist_dev(evl_static.tersus.deviation,args.rtk_names[1],evl_static.results_tersus.iloc[0],measurement,'dynamic')
pltr.plot_hist_dev(evl_static.ashtech.deviation,args.rtk_names[2],evl_static.results_ashtech.iloc[0],measurement,'dynamic')
pltr.plot_hist_dev(evl_static.ublox.deviation,args.rtk_names[3],evl_static.results_ublox.iloc[0],measurement,'dynamic')

# =============================================================================
# PLOTTING - median boxplots:
# =============================================================================

# # Print deviatiton by status (The distribution of deviations during individual states)
# pltr.plot_boxplot(evl.novatel,args.rtk_names[0],'status',measurement)
# pltr.plot_boxplot(evl.tersus,args.rtk_names[1],'status',measurement)
# pltr.plot_boxplot(evl.ashtech,args.rtk_names[2],'status',measurement)
# pltr.plot_boxplot(evl.ublox,args.rtk_names[3],'status',measurement)

# # Print deviatiton by phase (The distribution of deviations during individual phases of scenario)
# pltr.plot_boxplot(evl.novatel_by_acc,args.rtk_names[0],'phase',measurement)
# pltr.plot_boxplot(evl.tersus_by_acc,args.rtk_names[1],'phase',measurement)
# pltr.plot_boxplot(evl.ashtech_by_acc,args.rtk_names[2],'phase',measurement)
# pltr.plot_boxplot(evl.ublox_by_acc,args.rtk_names[3],'phase',measurement)

# =============================================================================
# PLOTTING - raw data:
# =============================================================================
    
# pltr.plot_rtk(rtk.novatel,args.rtk_names[0],"g")
# pltr.plot_rtk(rtk.tersus,args.rtk_names[1],"y")
# pltr.plot_rtk(rtk.ashtech,args.rtk_names[2],"b")
# pltr.plot_rtk(rtk.ublox,args.rtk_names[3],"m")

# pltr.plot_rtk(rtk_static.novatel,args.rtk_names[0],"g")
# pltr.plot_rtk(rtk_static.tersus,args.rtk_names[1],"y")
# pltr.plot_rtk(rtk_static.ashtech,args.rtk_names[2],"b")
# pltr.plot_rtk(rtk_static.ublox,args.rtk_names[3],"m")


# =============================================================================
# PLOTTING - deprecated plots:
# =============================================================================
# # =============================================================================
# # import numpy as np
# # import matplotlib.pyplot as plt
# # plt.scatter(evl.ashtech.status,evl.ashtech.deviation,marker ="_")
# # plt.scatter(evl.ashtech.status,evl.ashtech.cvl_speed,marker ="_")
# # plt.show()
# # =============================================================================

# # Print deviations (map,east,noth)
# # pltr.plot_devs(evl.novatel,'novatel',"g")
# # pltr.plot_devs(evl.tersus,'tersus',"y")
# # pltr.plot_devs(evl.ashtech,'ashtech',"b")
# # pltr.plot_devs(evl.ublox,'ublox',"m")

# # pltr.plot_lmplot(evl.novatel,'Novatel PwrPak7','speed [m/s]')
# # pltr.plot_lmplot(evl.tersus,'Tersus BX305','speed [m/s]')
# # pltr.plot_lmplot(evl.ashtech,'Ashtech MB800','speed [m/s]')
# # pltr.plot_lmplot(evl.ublox,'u-blox C94-M8P','speed [m/s]')
# # pltr.plot_lmplot(evl.novatel,'Novatel PwrPak7','acc [m/s]')
# # pltr.plot_lmplot(evl.tersus,'Tersus BX305','acc [m/s]')
# # pltr.plot_lmplot(evl.ashtech,'Ashtech MB800','acc [m/s]')
# # pltr.plot_lmplot(evl.ublox,'u-blox C94-M8P','acc [m/s]')

# # pltr.plot_correlation(evl.novatel.cvl_speed,evl.novatel.deviation,'Novatel PwrPak7','speed [m/s]')
# # pltr.plot_correlation(evl.tersus.cvl_speed,evl.tersus.deviation,'Tersus BX305','speed [m/s]')
# # pltr.plot_correlation(evl.ashtech.cvl_speed,evl.ashtech.deviation,'Ashtech MB800','speed [m/s]')
# # pltr.plot_correlation(evl.ublox.cvl_speed,evl.ublox.deviation,'u-blox C94-M8P','speed [m/s]')
# # pltr.plot_correlation(evl.novatel.cvl_acc,evl.novatel.deviation,'Novatel PwrPak7','acceleration [m/s²]')
# # pltr.plot_correlation(evl.tersus.cvl_acc,evl.tersus.deviation,'Tersus BX305','acceleration [m/s²]')
# # pltr.plot_correlation(evl.ashtech.cvl_acc,evl.ashtech.deviation,'Ashtech MB800','acceleration [m/s²]')
# # pltr.plot_correlation(evl.ublox.cvl_acc,evl.ublox.deviation,'u-blox C94-M8P','acceleration [m/s²]')

# # pltr.plot_pearsoncorr(evl.pearsoncorr_novatel,'Novatel PwrPak7')
# # pltr.plot_pearsoncorr(evl.pearsoncorr_tersus,'Tersus BX305')
# # pltr.plot_pearsoncorr(evl.pearsoncorr_ashtech,'Ashtech MB800')
# # pltr.plot_pearsoncorr(evl.pearsoncorr_ublox,'u-blox C94-M8P')