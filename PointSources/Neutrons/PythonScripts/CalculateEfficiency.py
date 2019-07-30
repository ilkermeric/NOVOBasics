#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 14:26:35 2019

@author: Ilker Meric

Calculate the total efficiency.

The total efficiency is determined as:
    
    N_detected / N_incident
    
N_detected: Total number of detected particles (including also those that scatter only once)
N_incident: Total number of incident particles 

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
FractionIncidentParticles = float(sys.argv[2])
TotalParticles = float(sys.argv[3])
IncidentParticleEnergy = float(sys.argv[4])

IncidentParticles = FractionIncidentParticles * TotalParticles

data = read_file(filename)
imax = len(data)
CurrentHistoryNo = data[0,0]

counter = 1 # Start with 1 otherwise the first history is unaccounted for.
flag = False

for i in range(len(data)):
        
    if(CurrentHistoryNo != data[i,0]): # New particle history, 1st hit 
        flag = True
        if(flag == True):
            counter += 1
        CurrentHistoryNo = data[i,0]
        continue
    if(CurrentHistoryNo == data[i,0] and CurrentHistoryNo != 0): # Same particle history
        flag = False
        continue
    
Efficiency = float(counter) / IncidentParticles


print("The total detection efficiency is: " + str(Efficiency))

f = open('TotalEfficiency','a')
f.write('Total efficiency is: ' + str(Efficiency))
