## -*- coding: utf-8 -*-
#"""
#Created on Sat Aug 24 21:40:17 2019
#
#@author: xkadj
#"""
#function  [invalid_HALL] = filter_HALL_artifacts_v2(ENC_resolution,sensorHALL,sensorENC)
#
#% Programmed by Jan Sedlak @ Valeo 2019
#% vypocet vsech vzdalenosti Hall_time ~ ENC_pls_num 
#

import numpy as np
import numpy.matlib as nmp  

# =============================================================================
# FUNCTIONS
# =============================================================================

def find_cluster(row_col, val): #% nalezne shluky v indexech
    row_col_array = np.zeros([3,np.shape(row_col)[0]])
    for row in range(np.shape(row_col)[0]):
        row_col_array[0][row] = row_col[row][0]
        row_col_array[1][row] = row_col[row][1]
        row_col_array[2][row] = 0
    row_col = row_col_array   
    act_gr = 1
    group = []
    while 0 in row_col[2]:   #% dokud vsude neni prihlasena skupina  
        ind_piv = np.where(row_col[2] == 0)[0][0] #% prvni nulu ve sloupci skupina
        if ind_piv.size != 0:
            group.append(row_col.T[ind_piv][0:2])
            row_col[2][ind_piv] = act_gr
        else:
            break
        for i in range(np.shape(row_col)[0]):
#            print (i)
            if np.where(group[act_gr-1] == row_col[0][i])[0].size != 0 or np.where(group[act_gr-1] == row_col[1][i])[0].size != 0:
#                x = [group[act_gr-1], row_col.T[i][0:2]]
                if np.asarray(group[act_gr-1]).shape == (2,):
                    last = [group[act_gr-1]]
                else:
                    last = group[act_gr-1]
                last.extend([row_col.T[i][0:2]])
                x = last
                if len(np.unique(x, axis=0)) > 1:
                    np.unique(x, axis=0)
                else:    
                    x = np.reshape(np.unique(x, axis=0), (2,)) #np.unique(x, axis=0) #<-reshape        
                group[act_gr-1] = x #np.reshape(x[0],(2,))
                row_col[2][i] = act_gr;   
        act_gr = act_gr + 1
#    # =============================================================================
#    #% najdi nejlepsi skupinu
#    # =============================================================================
    row_col = np.insert(row_col, 3, val, axis=0)
    gr_val = np.zeros([int(max(row_col[2])),2])
    for i in range(int(max(row_col[2]))):
        ind_pom = np.where(row_col[2] == i)[0]
        a = []
        for ii in range(len(ind_pom)):
            a.append(val[ind_pom[ii]])
        gr_val[i,0] = int(np.sum(a))  
        gr_val[i,1] = len(group[i])
    ind_max = np.where(gr_val.T[1] == np.max(gr_val.T[1]))[0] #% podle nejvetsi skupiny, chyba asi neni signifikantni protoze neni minimalni(pro minimalni propojeni celnu skupiny)
    groups = []
    for gr in ind_max:
        groups.append(group[int(gr)])
    cls_members = np.unique(groups)
    return cls_members
# =============================================================================
    
def get_pls_num(HALL_time,sensorENC):
    diference = abs(sensorENC.ENCtime - HALL_time)
    presnost = min(diference)
    ind = np.argmin(diference)    
    if (presnost >= 10000): #  ~ 10ms          
        print('Warning: Big ambiguity in HALL filter matching ... ')              
    pls_num = sensorENC.ENCnum[ind]
    return pls_num
# =============================================================================
    
def filter_HALL_artifacts(ENC_resolution,sensorHALL,sensorENC):
    invalid_HALL = np.zeros((1,len(sensorHALL)))
    pls_num = np.zeros((1,len(sensorHALL)))
    for ind in range(len(sensorHALL)):
       pls_num[0,ind] = get_pls_num(sensorHALL.HALLtime[ind],sensorENC)
    
    eval_f = np.zeros((len(sensorHALL),len(sensorHALL)))
    for pivot_ind in range(len(sensorHALL)):
        pivot_pls_num = nmp.repmat(pls_num[0][pivot_ind],1, len(sensorHALL))
        eval_f[pivot_ind] = abs(pls_num - pivot_pls_num) % ENC_resolution
    
    R = np.array([eval_f,(ENC_resolution * np.ones(np.shape(eval_f))) - eval_f])
    R2 = np.zeros(np.shape(eval_f))
    for x in range(np.shape(eval_f)[0]):
        for y in range(np.shape(eval_f)[1]):
            R2[x][y] = min([R[0][x][y],R[1][x][y]])
    R = R2
    #%ENC_threshold = median(R(:)) * 10;  % ten -times higher median will indicate artifact 
    #%RR = median(R,1);
    
#    mode = 'complex'
#    if mode == 'simple': # jak tohle funguje??
#        ENC_threshold = 10
#        RR = median(R,1)
#        if (min(RR) > 100):
#           print('So much artifacts to obtained realiable results from FILTER') 
#        invalid_HALL = (RR > ENC_threshold)
#    elif mode == 'complex':  #odstrani nuly z diagonaly, tj. nahradi NaN + necha pouze dolni troj. matici 
#        pom = np.ones(np.shape(eval_f))
#        pom = np.triu(pom)
#        pom = np.where(pom==0, pom, np.nan)
#        R = R + pom

    pom = np.ones(np.shape(eval_f))
    pom = np.triu(pom)
    pom = np.where(pom==0, pom, np.nan)
    R = R + pom
    row_col = []
    ##        %% nejcastejsi hodnota R, tj. hlavni shluk
    ##        %R_modus = mode(R(:));
    for x in range(np.shape(eval_f)[0]):
        for y in range(np.shape(eval_f)[1]):
            if not np.isnan(R[x][y]) and R[x][y] >= 0 and R[x][y] <= 5:
                row_col.append([x,y])     
    values = []
    for i in range(len(row_col)):
        values.append(R[row_col[i][0]][row_col[i][1]])
        
    ind_ok = find_cluster(row_col,values)
    #    [ind_ok] = find_cluster([r,c],values);
    ##        %{       
    ##        [r,c,values']
    ##        %}
    invalid_HALL = np.ones([len(sensorHALL),1],dtype=bool)
    for ok in ind_ok:        
        invalid_HALL[int(ok)] = 0
    return invalid_HALL

# =============================================================================
# MAIN
# =============================================================================
def hall_filter(ENC_resolution,sensorHALL,sensorENC):
    invalid_HALL = filter_HALL_artifacts(ENC_resolution,sensorHALL,sensorENC)
    invalid_HALL = np.where(invalid_HALL == True)[0]
    print(" - hall filter result: ", invalid_HALL)
    sensorHALL_orig = sensorHALL    #% filter out HALL artifacts
    sensorHALL = sensorHALL.drop(invalid_HALL)
#    sensorHALL(invalid_HALL == 1,:) = [];
    #sensorHALL(:,1) = 1:size(sensorHALL,1);
    return sensorHALL,sensorHALL_orig

#ENC_resolution = 2500
#sensorHALL,sensorHALL_orig = hall_filter(ENC_resolution,sensorHALL,sensorENC)

# =============================================================================
#%{
#[osa_x_out,histogram_out]=error_hist2(R(:),'plot');
#figure
#plot(osa_x_out,histogram_out)
#%}
#
#%{
#ts_HALL_new = ts_HALL;
#ts_HALL_new(invalid_HALL==1) = [];
#[n; invalid_HALL]'
#figure
#hold on
#stem(ts_HALL,ones(1,length(ts_HALL)))
#stem(ts_HALL_new,ones(1,length(ts_HALL_new)),'r')
#%}

#%new_sensorHALL = sensorHALL;
#%new_sensorHALL(invalid_HALL==1,:) = [];