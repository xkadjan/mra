# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:58:56 2020

@author: xkadj
"""
import pandas as pd

res = 2500
enc_per_round = pd.DataFrame(sensorENC[[7,9]])
enc_per_round.rename(columns={7: 'hall', 9: 'enc'},inplace=True)
enc_per_round['enc'] = enc_per_round.enc + 1                    # maybe this woks with one direction 
enc_per_round['hall_diff'] = enc_per_round.hall.diff()
enc_per_round.enc = (enc_per_round.enc % res).astype(int)
first_circle = max(abs(enc_per_round.enc.where(enc_per_round.hall == 0).dropna()))
first_circle = pd.DataFrame({"hall":[0],"enc":[first_circle],"hall_diff":[1]})
enc_per_round = enc_per_round.append(first_circle).sort_index()
enc_per_round = enc_per_round.where(enc_per_round.hall_diff != 0).dropna()
enc_per_round = enc_per_round.drop(enc_per_round.index[1])
enc_per_round["hall"] = sensorHALL.HALLnum.tolist()

enc_per_round.enc.reset_index().enc