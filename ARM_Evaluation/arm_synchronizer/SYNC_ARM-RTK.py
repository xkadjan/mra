# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:57:48 2019

@author: xkadj
"""

import sync_armparser as arm_prs
import sync_rtk_parser as rtk_prs
import sync_rtk_evl as rtk_evl
import sync_plotting as plot

# =============================================================================
#  DEFINITIONS
# =============================================================================
dir_rtk = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\RTK\TO_PROCESS"
dir_arm = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\arm_converted_200327"
# csv_dir = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\RESULTS"
csv_dir = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\Computers and Electronics in Agriculture\RESULTS"
#csv_dir = os.path.join(dir_arm,'output')

wgs_ref = [50.07478605085059,14.52025289904692,286.6000000000184]
fixed_height = 235.58

prefix = 'all'

if prefix == 'auto': slice_times = [57800,61500]
if prefix == 'car': slice_times = [71800,76000]
if prefix == 'ped': slice_times = [0,90000]

new_preproccess = False
only_fix = False

print("MRA synchronizer started")

pltr = plot.Plotter(new_preproccess,only_fix,csv_dir)

# =============================================================================
# ARM:
# =============================================================================
if new_preproccess:
    arm = arm_prs.ArmParser(dir_arm,prefix)
    arm.parse_slices()
    #arm.slice_times(slice_times)
    arm.get_bad_cicles()
    arm.drop_peaks()
    arm.filter_signal()
    arm.drop_bad_circles()
    arm.drop_zero_speed()
    arm.drop_zero_acc()
    arm.drop_limit_acc()

    #pltr.plot_arm(arm.arm_async,'arm_async','k')
    pltr.plot_arm(arm.arm_20hz,'arm_20hz','r')
    pltr.plot_marks(arm)

# =============================================================================
# RTK
# =============================================================================
if new_preproccess:
    rtk = rtk_prs.RtkParser(dir_rtk,wgs_ref)
    rtk.parse_slices(prefix)
    #rtk.slice_times(slice_times)
    rtk.drop_points_wo_arm(arm.arm_20hz)
    rtk.drop_points_wo_rtk(arm.arm_20hz)
    rtk_list = rtk.concate_arm_and_rtks()

    pltr.plot_rtk(rtk.novatel,'novatel',"g")
    pltr.plot_rtk(rtk.tersus,'tersus',"y")
    pltr.plot_rtk(rtk.ashtech,'ashtech',"b")
    pltr.plot_rtk(rtk.ublox,'ublox',"m")

# =============================================================================
# EVL
# =============================================================================
evl = rtk_evl.Evaluator()
if not new_preproccess:
    evl.csv_load(csv_dir)
    rtk_list = evl.csv_load(csv_dir)
evl.get_deviations(rtk_list)
if only_fix:
    evl.filter_fix()
# evl.filter_sigma()
# evl.abs_acc()
evl.get_make_boxes()
# evl.adjust_status()
evl.get_results(only_fix)
evl.get_correlation()
evl.csv_print(csv_dir,new_preproccess)

# Print deviatiton by status
pltr.plot_boxplot(evl.novatel,'Novatel PwrPak7','status')
pltr.plot_boxplot(evl.tersus,'Tersus BX305','status')
pltr.plot_boxplot(evl.ashtech,'Ashtech MB800','status')
pltr.plot_boxplot(evl.ublox,'u-blox C94-M8P','status')

# Print deviatiton by phase:
pltr.plot_boxplot(evl.novatel_by_acc,'Novatel PwrPak7','phase')
pltr.plot_boxplot(evl.tersus_by_acc,'Tersus BX305','phase')
pltr.plot_boxplot(evl.ashtech_by_acc,'Ashtech MB800','phase')
pltr.plot_boxplot(evl.ublox_by_acc,'u-blox C94-M8P','phase')
# =============================================================================
# import numpy as np
# import matplotlib.pyplot as plt
# plt.scatter(evl.ashtech.status,evl.ashtech.deviation,marker ="_")
# plt.scatter(evl.ashtech.status,evl.ashtech.cvl_speed,marker ="_")
# plt.show()
# =============================================================================

# Print deviations (map,east,noth)
# pltr.plot_devs(evl.novatel,'novatel',"g")
# pltr.plot_devs(evl.tersus,'tersus',"y")
# pltr.plot_devs(evl.ashtech,'ashtech',"b")
# pltr.plot_devs(evl.ublox,'ublox',"m")

# Print deviations (map,east,noth)
# pltr.plot_hist(evl.novatel,'Novatel PwrPak7',evl.results_novatel.iloc[0])
# pltr.plot_hist(evl.tersus,'Tersus BX305',evl.results_tersus.iloc[0])
# pltr.plot_hist(evl.ashtech,'Ashtech MB800',evl.results_ashtech.iloc[0])
# pltr.plot_hist(evl.ublox,'u-blox C94-M8P',evl.results_ublox.iloc[0])


# #Print density
# pltr.plot_hist_dev(evl.novatel.deviation,'Novatel PwrPak7',evl.results_novatel.iloc[0])
# pltr.plot_hist_dev(evl.tersus.deviation,'Tersus BX305',evl.results_tersus.iloc[0])
# pltr.plot_hist_dev(evl.ashtech.deviation,'Ashtech MB800',evl.results_ashtech.iloc[0])
# pltr.plot_hist_dev(evl.ublox.deviation,'u-blox C94-M8P',evl.results_ublox.iloc[0])

# pltr.plot_lmplot(evl.novatel,'Novatel PwrPak7','speed [m/s]')
# pltr.plot_lmplot(evl.tersus,'Tersus BX305','speed [m/s]')
# pltr.plot_lmplot(evl.ashtech,'Ashtech MB800','speed [m/s]')
# pltr.plot_lmplot(evl.ublox,'u-blox C94-M8P','speed [m/s]')
# pltr.plot_lmplot(evl.novatel,'Novatel PwrPak7','acc [m/s]')
# pltr.plot_lmplot(evl.tersus,'Tersus BX305','acc [m/s]')
# pltr.plot_lmplot(evl.ashtech,'Ashtech MB800','acc [m/s]')
# pltr.plot_lmplot(evl.ublox,'u-blox C94-M8P','acc [m/s]')

# pltr.plot_correlation(evl.novatel.cvl_speed,evl.novatel.deviation,'Novatel PwrPak7','speed [m/s]')
# pltr.plot_correlation(evl.tersus.cvl_speed,evl.tersus.deviation,'Tersus BX305','speed [m/s]')
# pltr.plot_correlation(evl.ashtech.cvl_speed,evl.ashtech.deviation,'Ashtech MB800','speed [m/s]')
# pltr.plot_correlation(evl.ublox.cvl_speed,evl.ublox.deviation,'u-blox C94-M8P','speed [m/s]')
# pltr.plot_correlation(evl.novatel.cvl_acc,evl.novatel.deviation,'Novatel PwrPak7','acceleration [m/s²]')
# pltr.plot_correlation(evl.tersus.cvl_acc,evl.tersus.deviation,'Tersus BX305','acceleration [m/s²]')
# pltr.plot_correlation(evl.ashtech.cvl_acc,evl.ashtech.deviation,'Ashtech MB800','acceleration [m/s²]')
# pltr.plot_correlation(evl.ublox.cvl_acc,evl.ublox.deviation,'u-blox C94-M8P','acceleration [m/s²]')

# pltr.plot_pearsoncorr(evl.pearsoncorr_novatel,'Novatel PwrPak7')
# pltr.plot_pearsoncorr(evl.pearsoncorr_tersus,'Tersus BX305')
# pltr.plot_pearsoncorr(evl.pearsoncorr_ashtech,'Ashtech MB800')
# pltr.plot_pearsoncorr(evl.pearsoncorr_ublox,'u-blox C94-M8P')