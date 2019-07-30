#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:03:55 2019

@author: Ilker Meric

Determine the fraction of multiple hits in the first, second and third hit segments

This information can be used to plot "clean" multiplicity distributions for the
number of responding segments.

"""

import numpy as np
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

MultipleHits = np.zeros(3)  # The first three responding segments.
 
StoreHitSegment = []
Historyflag = False
Segmentflag = False

for i in range(len(data)):
    
    if(i%10000 == 0):
        print("Processing Detection # " + str(i))
        
    if(CurrentHistoryNo != data[i,0]): # New particle history, 1st hit 
        Historyflag = True
        
        if(Historyflag == True):
            StoreHitSegment = np.array(StoreHitSegment)
            u,uindex,itemcount = np.unique(StoreHitSegment, return_index=True,
                                 return_counts=True)
            counts = 0
            if(len(u) != len(StoreHitSegment)): # There are segments with multiple hits !
                length = len(uindex)
                while length:
                    Index = np.argmin(uindex)
                    if(itemcount[Index] > 1 and counts <= 2):
                        MultipleHits[counts] += 1
                    uindex = np.delete(uindex, Index)
                    counts += 1
                    length = len(uindex)
                
            StoreHitSegment = []
            
        CurrentHistoryNo = data[i,0]
        StoreHitSegment.append(data[i,-1])
        
        continue
    if(CurrentHistoryNo == data[i,0] and CurrentHistoryNo != 0): # Same particle history
        
        StoreHitSegment.append(data[i,-1])
        Historyflag = False
        continue
    
MultipleHits = MultipleHits / IncidentPhotons

print("Fraction of multiple of interactions in the 1st responding segment: " +
      str(MultipleHits[0]))
print("Fraction of multiple of interactions in the 2nd responding segment: " +
      str(MultipleHits[1]))
print("Fraction of multiple of interactions in the 3rd responding segment: " +
      str(MultipleHits[2]))

print("Writing results to file...")

f = open('IntrinsicPileUp','a')
np.savetxt(f, np.reshape(MultipleHits,(1,3)), delimiter=' ', fmt=['%.10f', 
                                                                 '%.10f', 
                                                                 '%.10f'])

