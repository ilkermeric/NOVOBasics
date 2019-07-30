# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 00:54:22 2019

@author: Ilker Meric


Energy deposition, Distance and TOF distributions with segmentation.

Energy deposition:
    1. First interaction
    2. Second interaction
    3. Third interaction
    
Distance and TOF:
    1. Between the First and the Second interaction
    2. Between the Second and the Third interaction

Note: Even if there are multiple hits in a given segment (invalid events), these are still used
in the following analyses. If there are multiple hits in a given segment, then only the data 
corresponding to the first collision are used !
 
Usage:
    ./python DistributionsNoSeg.py [SegmentedData] [Fraction] [TotalHistories] [ParticleEnergy] [ParticleName]

"""

import numpy as np
import sys
import matplotlib.pyplot as plt

def read_file(file):
   data = np.loadtxt(fname=file, delimiter=' ')
   return data


if(len(sys.argv) != 6):
    raise RuntimeError ("Please pass all the arguments!" ) 
filename = sys.argv[1]
FractionIncidentParticles = float(sys.argv[2])
TotalParticles = float(sys.argv[3])
IncidentParticleEnergy = float(sys.argv[4])
IncidentParticleName = sys.argv[5]

IncidentParticles = FractionIncidentParticles * TotalParticles

data = read_file(filename)
imax = len(data)
CurrentHistoryNo = data[0,0]

Edeposition = [[] for i in range(3)]
Distance    = [[] for i in range(2)]
TOF         = [[] for i in range(2)]

StoreHitSegment     = []
EnergyDep_temp      = []
Coordinates         = []
Coordinates_temp    = []
Time                = []
SCoordinates        = []
SCoordinates_temp   = []
STime               = []

counts = 0
Historyflag = False

for i in range(len(data)):
    
    if(i%10000 == 0):
        print("Processing Detection # " + str(i))
              
    if(CurrentHistoryNo != data[i,0]): # New particle history, 1st hit 
        Historyflag = True
        counts = 0
        if(Historyflag == True):
            StoreHitSegment = np.array(StoreHitSegment)
            EnergyDep_temp = np.array(EnergyDep_temp)
            Coordinates = np.array(Coordinates)
            Time = np.array(Time)
            u,uindex,itemcount = np.unique(StoreHitSegment, return_index=True,
                                 return_counts=True)
            counts = 0
            if(len(Coordinates) != len(Time)):
                raise RuntimeError ("The two arrays Coordinates and Time should have the same length!" ) 
            if(len(u) == len(StoreHitSegment)): # All hits occur in separate segments !
                for j in range(len(StoreHitSegment)):
                    if(j <= 2):
                        Edeposition[j].append(EnergyDep_temp[j])
                    if(len(StoreHitSegment) > 1):
                        for j in range(len(StoreHitSegment)):
                            if(j < len(StoreHitSegment)-1):
                               distanceValue = np.sqrt(np.sum((Coordinates[j,:]-Coordinates[j+1,:])**2))
                               TOFValue = (Time[j+1] - Time[j]) * 10.0
                               if(distanceValue < 0.0 or TOFValue < 0.0):
                                   raise RuntimeError ("Distance or TOF cannot be negative !" ) 
                               if(j==0):
                                  Distance[j].append(distanceValue)
                                  TOF[j].append(TOFValue)
                               if(j==1):
                                  Distance[j].append(distanceValue)
                                  TOF[j].append(TOFValue)
            elif(len(u) != len(StoreHitSegment)): # Some hits occur in the same segment !
                length = len(uindex)
                while length:
                    Index = np.argmin(uindex)
                    MinElement = np.amin(uindex)
                    if(counts <= 2):
                        Edeposition[counts].append(EnergyDep_temp[MinElement])
                        STime.append(Time[MinElement])
                        SCoordinates_temp = [Coordinates[MinElement,0], Coordinates[MinElement,1], Coordinates[MinElement,2]]
                        SCoordinates.append(SCoordinates_temp)
                    uindex = np.delete(uindex, Index)
                    counts += 1
                    length = len(uindex)
                STime = np.array(STime)
                #print(STime)
                SCoordinates = np.array(SCoordinates)
                if(len(STime) > 1):
                    for j in range(len(STime)):
                        if(j < len(STime)-1):
                            distanceValue = np.sqrt(np.sum((Coordinates[j,:]-Coordinates[j+1,:])**2))
                            TOFValue = (STime[j+1] - STime[j]) * 10.0
                            if(distanceValue < 0.0 or TOFValue < 0.0):
                                   raise RuntimeError ("Distance or TOF cannot be negative !" ) 
                            if(j == 0):
                                Distance[j].append(distanceValue)
                                TOF[j].append(TOFValue)
                            if(j == 1):
                                Distance[j].append(distanceValue)
                                TOF[j].append(TOFValue)
           
            StoreHitSegment  =[]
            EnergyDep_temp = []
            Coordinates = []
            Time = []
            SCoordinates = []
            STime = []
       
        CurrentHistoryNo = data[i,0]
        StoreHitSegment.append(data[i,-1])
        EnergyDep_temp.append(data[i,4])
        Coordinates_temp = [data[i,1], data[i,2], data[i,3]]
        Coordinates.append(Coordinates_temp)
        Time.append(data[i,5])
       
        continue
    if(CurrentHistoryNo == data[i,0] and CurrentHistoryNo != 0): # Same particle history
        
        StoreHitSegment.append(data[i,-1])
        EnergyDep_temp.append(data[i,4])
        Coordinates_temp = [data[i,1], data[i,2], data[i,3]]
        Coordinates.append(Coordinates_temp)
        Time.append(data[i,5])
        Historyflag = False
        continue

Edeposition = np.array(Edeposition)
Distance = np.array(Distance)
TOF = np.array(TOF)

if((len(Distance[0]) != len(TOF[0])) or (len(Distance[1]) != len(TOF[1]))):
    raise RuntimeError ("Arrays Distance and TOF must have the same length !" ) 


MeanEnergy = np.zeros(3)
MeanDistance = np.zeros(2)
MeanTOF = np.zeros(2)

plt.figure()
bins = np.arange(0.1, IncidentParticleEnergy, 0.01)

for i in range(len(Edeposition)):
    plt.hist(Edeposition[i], bins, histtype='step', label='coll. ' + str(i+1),
             linewidth=2.0)
    MeanEnergy[i] = np.mean(Edeposition[i])
    print('Mean energy recoil particles ' + str(i+1) + ' ' + str(MeanEnergy[i])+ ' MeV')

plt.title( str(IncidentParticleEnergy) + " MeV " + IncidentParticleName + " with segmentation")
plt.xlabel("Energy[MeV]")
plt.ylabel("Entries")
plt.yscale("log")
plt.legend()

plt.savefig('SegmentEnergyDistribution.png', dpi=250, bbox_inches='tight')

plt.figure()
bins = np.arange(0.0, 30, 0.1)

for i in range(len(Distance)):
    plt.hist(Distance[i], bins, histtype='step', label='Distance ' + str(i+1) + ' - ' + str(i+2),
             linewidth=2.0)
    MeanDistance[i] = np.mean(Distance[i])
    print('Mean distance ' + str(i+1) + ' - ' + str(i+2) + ' ' + str(MeanDistance[i])+ ' cm')

plt.title( str(IncidentParticleEnergy) + " MeV " + IncidentParticleName + " with segmentation")
plt.xlabel("Distance [cm]")
plt.ylabel("Entries")
plt.yscale("log")
plt.legend()

plt.savefig('SegmentDistancesDistribution.png', dpi=250, bbox_inches='tight')

plt.figure()
bins = np.arange(0.0, 15, 0.1)

for i in range(len(TOF)):
    plt.hist(TOF[i], bins, histtype='step', label='TOF ' + str(i+1) + ' - ' + str(i+2),
             linewidth=2.0)
    MeanTOF[i] = np.mean(TOF[i])
    print('Mean TOF ' + str(i+1) + ' - ' + str(i+2) + ' ' + str(MeanTOF[i])+ ' ns')

plt.title( str(IncidentParticleEnergy) + " MeV " + IncidentParticleName + " with segmentation")
plt.xlabel("TOF [ns]")
plt.ylabel("Entries")
plt.yscale("log")
plt.legend()

plt.savefig('SegmentTOFsDistribution.png', dpi=250, bbox_inches='tight')

f1 = open('MeanEnergiesSeg','a')
np.savetxt(f1, np.reshape(MeanEnergy,(1,3)), delimiter=' ', fmt=['%.10f', 
                                                                 '%.10f', 
                                                                 '%.10f'])

f2 = open('MeanDistancesSeg','a')
np.savetxt(f2, np.reshape(MeanDistance,(1,2)), delimiter=' ', fmt=['%.10f', 
                                                                   '%.10f'])

f3 = open('MeanTOFsSeg','a')
np.savetxt(f3, np.reshape(MeanTOF,(1,2)), delimiter=' ', fmt=['%.10f',
                                                              '%.10f'])

#plt.show()
