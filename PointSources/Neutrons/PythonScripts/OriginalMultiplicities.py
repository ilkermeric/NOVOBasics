#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:03:55 2019

@author: Ilker Meric

Determine and plot original hit multiplicities w/o segmentation.

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

Multiplicities = np.zeros(11)
counter = 0
flag = False

for i in range(len(data)):
        
    if(CurrentHistoryNo != data[i,0]): # New particle history, 1st hit 
        flag = True
        if(flag == True):
            if(counter >= len(Multiplicities)):
                Multiplicities[-1] += 1
            else:
                Multiplicities[counter] += 1
        counter = 0
        CurrentHistoryNo = data[i,0]
        counter += 1
        continue
    if(CurrentHistoryNo == data[i,0] and CurrentHistoryNo != 0): # Same particle history
        counter += 1
        flag = False
        continue
    
Multiplicities = Multiplicities / IncidentPhotons

print(Multiplicities)

ypos = np.arange(1,11,1)

plt.figure()

plt.bar(ypos,Multiplicities[1:],0.35,align='center')
plt.title( str(IncidentPhotonEnergy) + " MeV neutrons w/o segmentation")
plt.xlabel("Recoil proton multiplicities")
plt.ylabel("Normalized entries")
plt.yscale("log")
plt.xticks(ypos, ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10+'))

plt.savefig('OriginalMultiplicities.png', dpi=250, bbox_inches='tight')

#plt.show()
