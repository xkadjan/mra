# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:57:48 2019

@author: xkadj
"""

import sync_armparser as arm
import sync_rtk_parser as rtk_prs
import sync_rtk_evl as rtk_evl
import sync_plotting as plot

# =============================================================================
#  DEFINITIONS
# =============================================================================
dir_rtk = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\RTK\TO_PROCESS"
dir_arm = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\MERENI\4xVRS_ARM_tettrack_final\ARM\arm_converted_200327"
csv_dir = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - RTK\zaverecna zprava\vysledky\csv"
#csv_dir = os.path.join(dir_arm,'output')

wgs_ref = [50.07478605085059,14.52025289904692,286.6000000000184]
fixed_height = 235.58

prefix = 'all'

if prefix == 'auto': slice_times = [57800,61500]
if prefix == 'car': slice_times = [71800,76000]
if prefix == 'ped': slice_times = [0,90000]

new_preproccess = False
only_fix = True

pltr = plot.Plotter(new_preproccess)

# =============================================================================
# ARM:
# =============================================================================
if new_preproccess:
    arm = arm.ArmParser(dir_arm,prefix)
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
evl.filter_sigma()
evl.get_make_boxes()
evl.get_results(only_fix)
evl.csv_print(csv_dir,new_preproccess)

pltr.plot_devs(evl.novatel,'novatel',"g")
pltr.plot_devs(evl.tersus,'tersus',"y")
pltr.plot_devs(evl.ashtech,'ashtech',"b")
pltr.plot_devs(evl.ublox,'ublox',"m")

pltr.plot_hist(evl.novatel,200,'Novatel PwrPak7',500,evl.results_novatel.iloc[0])
pltr.plot_hist(evl.tersus,200,'Tersus BX305',500,evl.results_tersus.iloc[0])
pltr.plot_hist(evl.ashtech,5000,'Ashtech MB800',500,evl.results_ashtech.iloc[0])
pltr.plot_hist(evl.ublox,1000,'u-blox C94-M8P',500,evl.results_ublox.iloc[0])