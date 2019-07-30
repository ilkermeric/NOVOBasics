#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:03:55 2019

@author: Ilker Meric

Determine and plot hit multiplicities (number of responding segments) with segmentation.
Criterion:
    At least one hit in a given segment !
Note:
    These multiplicities are not corrected for multiple interactions in a given segment.
    Multiple hits in a given segment are counted as a single hit.

"""

import numpy as np
import matplotlib.pyplot as plt
import sys

def read_file(file):
   data = np.loadtxt(fname=file, delimiter=' ')
   return data

if(len(sys.argv) != 5):
    raise RuntimeError ("Please pass all the arguments!" ) 
filename = sys.argv[1]
FractionIncidentPhotons = float(sys.argv[2])
TotalPhotons = float(sys.argv[3])
IncidentPhotonEnergy = float(sys.argv[4])

IncidentPhotons = FractionIncidentPhotons * TotalPhotons

data = read_file(filename)
imax = len(data)
CurrentHistoryNo = data[0,0]
CurrentHitSegment = data[0,-1]

Multiplicities = np.zeros(11)
StoreHitSegment = []
counts = 0
Historyflag = False
Segmentflag = False

for i in range(len(data)):
        
    if(CurrentHistoryNo != data[i,0]): # New particle history, 1st hit 
        Historyflag = True
        counts = 0
        if(Historyflag == True):
            StoreHitSegment = np.array(StoreHitSegment)
            u = np.unique(StoreHitSegment)
            
            counts = len(u)
            if(counts >= len(Multiplicities)):
                Multiplicities[-1] += 1
            else:
                Multiplicities[counts] += 1
            StoreHitSegment  =[]
       
        CurrentHistoryNo = data[i,0]
        StoreHitSegment.append(data[i,-1])
       
        continue
    if(CurrentHistoryNo == data[i,0] and CurrentHistoryNo != 0): # Same particle history
        
        StoreHitSegment.append(data[i,-1])
        Historyflag = False
        continue
    
Multiplicities = Multiplicities / IncidentPhotons

print(Multiplicities)

ypos = np.arange(1,11,1)

plt.figure()

plt.bar(ypos,Multiplicities[1:],0.35,align='center')
plt.title( str(IncidentPhotonEnergy) + " MeV photons with segmentation")
plt.xlabel("Segment multiplicities")
plt.ylabel("Normalized entries")
plt.yscale("log")
plt.xticks(ypos, ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10+'))

plt.savefig('SegmentMultiplicities.png', dpi=250, bbox_inches='tight')

#plt.show()
