# -*- coding: utf-8 -*-
"""
Created on Mon May 11 11:24:21 2020

@author: xkadj
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 14:57:48 2019

@author: xkadj
"""

import sync_armparser as arm
import sync_dws_parser as dws_prs
import sync_dws_evl as dws_evl
import sync_plotting as plot

# =============================================================================
#  DEFINITIONS
# =============================================================================
dir_rtk = r"C:\Users\xkadj\OneDrive\valeo\191114_ARM_DEWESOFT_NOVATEL\dewesoft_data\petr_posvic\DATA\used"
dir_arm = r"C:\Users\xkadj\OneDrive\valeo\191114_ARM_DEWESOFT_NOVATEL\arm_data\arm_output_200427-enctol3-offset17.7"
csv_dir = r"C:\Users\xkadj\OneDrive\valeo\191114_ARM_DEWESOFT_NOVATEL\output_eval"

wgs_ref = [50.07478605085059,14.52025289904692,235.05] # dws using this
fixed_height = 235.05                                  # not used by dws

new_preproccess = True
only_fix = False

pltr = plot.Plotter(new_preproccess)

# =============================================================================
# ARM:
# =============================================================================
if new_preproccess:
    arm = arm.ArmParser(dir_arm,'all')
    arm.parse_slices()
    #arm.slice_times(slice_times)
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
if new_preproccess:
    dws_p = dws_prs.DwsParser(dir_rtk,wgs_ref)
    dws_p.parse_slices()
    dws_p.compensate_offset()
    dws_p.drop_unpaired_points(arm.arm_20hz)
    rtk_list = dws_p.concate_arm_and_rtks()

    pltr.plot_rtk(dws_p.dewesoft,'dewesoft',"b")
    #pltr.plot_arm(arm.arm_async,'arm_async','k')
    pltr.plot_arm(arm.arm_20hz,'arm_20hz','r')
    pltr.plot_marks(arm)

# =============================================================================
# EVL
# =============================================================================

dws_e = dws_evl.Evaluator()
#if not new_preproccess:
#    evl.csv_load(csv_dir)# dws_evl have not 'csv_load' (rkt_eval have it)
dws_e.get_deviations(rtk_list)
if only_fix:
    dws_e.filter_fix()
dws_e.filter_sigma()
dws_e.get_make_boxes()
dws_e.get_results(only_fix)
dws_e.csv_print(csv_dir,new_preproccess)

pltr.plot_devs(dws_e.dewesoft,'dewesoft',"b")
pltr.plot_hist(dws_e.dewesoft,200,'Dewesoft - whole measurement',40,dws_e.results_dewesoft.iloc[0])

for speed in range(len(dws_e.dewesoft_by_speed)):
    title = 'Dewesoft - speed ' + str(dws_e.bounds_speed[speed]) + '-' + str(dws_e.bounds_speed[speed+1]) + 'm/s'
    pltr.plot_hist(dws_e.dewesoft_by_speed[speed],100,title,40,dws_e.results_dewesoft.iloc[1+speed])

#for acc in range(len(dws_e.dewesoft_by_acc)):
#    title = 'Dewesoft - acc ' + str(dws_e.bounds_acc[acc]) + '-' + str(dws_e.bounds_acc[acc+1]) + 'm/s²'
#    pltr.plot_hist(dws_e.dewesoft_by_acc[acc],100,title,70)

pltr.plot_hist_dev(dws_e.dewesoft.deviation,50,'Dewesoft - whole measurement',dws_e.results_dewesoft.iloc[0])
for speed in range(len(dws_e.dewesoft_by_speed)):
    title = 'Dewesoft - speed ' + str(dws_e.bounds_speed[speed]) + '-' + str(dws_e.bounds_speed[speed+1]) + 'm/s'
    pltr.plot_hist_dev(dws_e.dewesoft_by_speed[speed].deviation,50,title,dws_e.results_dewesoft.iloc[speed+1])

#pltr.plot_correlation(dws_e.dewesoft.cvl_speed,dws_e.dewesoft.deviation,'Dewesoft','speed [m/s]')
pltr.plot_lmplot(dws_e.dewesoft,'Dewesoft','speed [m/s]')
pltr.plot_pearsoncorr(dws_e.dewesoft.corr(method='pearson'),'Dewesoft')