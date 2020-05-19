# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:07:41 2020

@author: xkadj
"""
res = 2500
errors = sensorHALL.enc_err.tolist()
for error in range(len(errors)): 
    if errors[error] > res/2: errors[error] = errors[error] - res
sensorHALL.enc_err = errors
