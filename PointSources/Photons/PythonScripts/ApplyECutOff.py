# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 10:09:55 2019

@author: Ilker Meric

Apply energy cuts on the sorted PTRAC data arrays. 
A reasonable choice for recoil electrons would be a cut-off at E=10 keV.
Do this before segmentation !

"""

import numpy as np
import sys

def read_file(file):
   data = np.loadtxt(fname=file, delimiter=' ')
   return data

if(len(sys.argv) != 3):
    raise RuntimeError ("Please pass all the arguments!" ) 
filename = sys.argv[1]
RECutOff = float(sys.argv[2])

data = read_file(filename)

EventParameters_temp = []
EventParameters = []
for i in range(len(data)):
    if(i%1000 == 0):
        print("Processing history no: " + str(data[i,0]))
    if(data[i,4] >= RECutOff):
        EventParameters_temp = [data[i,0], data[i,1], data[i,2], data[i,3],
                                data[i,4], data[i,5]]
        EventParameters.append(EventParameters_temp)
    
EventParameters = np.array(EventParameters)

f = open('SortedPTRACdatawithECutOff','a')
np.savetxt(f, EventParameters, delimiter=' ', fmt=['%.10i', '%.10f', '%.10f',
                                                  '%.10f', '%.10f', '%.10f'])
  