# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 13:34:18 2020

@author: xkadj


"""


#def replace_times(enc,bad_times)
times = np.array([enc.index.tolist(),enc.time]).T
times_corr = np.array([bad_times.index.tolist(),bad_times.time]).T

for corr in range(len(times_corr)):
    for orig in range(len(times)):
        if times_corr[corr][0] == times[orig][0]:
            times[orig][1] = times_corr[corr][1]

enc["time"] = pd.Series(times.T[1],index=times.T[0].astype(int))
# enc["time"] =
#    return pd.DataFrame({'time': times[0],
#                    'num': enc.ENCnum}))
#        
#        
#for row in range(len(times)):
#    if times[row][0] == times_corr[row][0]:
#        print(times[row][1],times_corr[row][1])