#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 14:26:35 2019

@author: Ilker Meric

Calculate the total efficiency.

The total efficiency is determined as:
    
    N_detected / N_incident
    
N_detected: Total number of detected neutrons (including also those that scatter only once)
N_incident: Total number of neutrons incident on the SVSC

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
FractionIncidentNeutrons = float(sys.argv[2])
TotalNeutrons = float(sys.argv[3])
IncidentNeutronEnergy = float(sys.argv[4])

IncidentNeutrons = FractionIncidentNeutrons * TotalNeutrons

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
    
Efficiency = float(counter) / IncidentNeutrons


print("The total detection efficiency is: " + str(Efficiency))