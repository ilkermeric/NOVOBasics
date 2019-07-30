# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 23:59:54 2019

@author: Ilker Meric

Perform segmentation of the hit data in SVSC
Apply first Energy cut-offs !

"""

import numpy as np
import sys

def read_file(file):
   data = np.loadtxt(fname=file, delimiter=' ')
   return data

if(len(sys.argv) != 3):
    raise RuntimeError ("Please pass all the arguments!" ) 
filename = sys.argv[1]
SegmentSize = float(sys.argv[2])

data = read_file(filename)

min_z = 10.0
max_z = 30.0 + SegmentSize
min_y = -10.0
max_y = 10.0 + SegmentSize
bins_z = np.arange(min_z, max_z, SegmentSize) 
bins_x = np.arange(-10.0, 20.0, 20.0)
bins_y = np.arange(min_y, max_y, SegmentSize)

NSegments = (len(bins_x)-1)*(len(bins_y)-1)*(len(bins_z)-1)
print("Total Number of Segments: " + str(NSegments))

Segments = []
Segments_temp = []

counter = 0 
for i in range(len(bins_x)-1):
    for j in range(len(bins_y)-1):
        for k in range(len(bins_z)-1):
            counter += 1
            Segments_temp = [bins_x[i], bins_x[i+1], bins_y[j], bins_y[j+1],
                                 bins_z[k], bins_z[k+1]]
            Segments.append(Segments_temp)


Segments = np.array(Segments)

if(len(Segments) != NSegments):
    raise RuntimeError ("The array Segments contains more elements than NSegments! Aborting !" ) 

print(Segments)
SegmentedData_temp = []
SegmentedData = []
SegmentNumber = 0

for i in range(len(data)):
    if(i%100 == 0):
        print("Processing history no: " + str(data[i,0]))
    x = data[i,1]
    y = data[i,2]
    z = data[i,3]
    for j in range(len(Segments)):
        if(x >= Segments[j,0] and x < Segments[j,1]):
            if(y >= Segments[j,2] and y < Segments[j,3]):
                if(z >= Segments[j,4] and z < Segments[j,5]):
                    SegmentNumber = j
                    break
    SegmentedData_temp = [data[i,0], data[i,1], data[i,2], data[i,3],
                          data[i,4], data[i,5], SegmentNumber]                          
    SegmentedData.append(SegmentedData_temp)
    
SegmentedData = np.array(SegmentedData)    
    
f = open('SegmentedData','a')
np.savetxt(f, SegmentedData, delimiter=' ', fmt=['%.10i', '%.10f', '%.10f',
                                                  '%.10f', '%.10f', '%.10f',
                                                  '%.4i'])
  