# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 01:07:13 2019

@author: Ilker Meric

Score load distributions and plot 2D load distributions for segmented PC.

Note: Multiple hits in the same particle history in a segment are counted as a single count.

"""

import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def read_file(file):
   data = np.loadtxt(fname=file, delimiter=' ')
   return data


if(len(sys.argv) != 6):
    raise RuntimeError ("Please pass all the arguments!" ) 
filename = sys.argv[1]
FractionIncidentParticles = float(sys.argv[2])
TotalParticles = float(sys.argv[3])
IncidentParticleEnergy = float(sys.argv[4])
SegmentSize = float(sys.argv[5])

IncidentParticles = FractionIncidentParticles * TotalParticles

data = read_file(filename)
imax = len(data)
CurrentHistoryNo = data[0,0]


StoreHitSegment     = []
Coordinates         = []
Coordinates_temp    = []
SegmentLoad         = []
SegmentLoad_temp    = []

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
            Coordinates = np.array(Coordinates)
            u,uindex,itemcount = np.unique(StoreHitSegment, return_index=True,
                                 return_counts=True)
            counts = 0
            if(len(u) == len(StoreHitSegment)): # All hits occur in separate segments !
                for j in range(len(StoreHitSegment)):
                    SegmentLoad_temp = [Coordinates[j,0], Coordinates[j,1], Coordinates[j,2]]
                    SegmentLoad.append(SegmentLoad_temp)
            elif(len(u) != len(StoreHitSegment)): # Some hits occur in the same segment !
                length = len(uindex)
                while length:
                    Index = np.argmin(uindex)
                    MinElement = np.amin(uindex)
                    SegmentLoad_temp = [Coordinates[MinElement,0], Coordinates[MinElement,1], Coordinates[MinElement,2]]
                    SegmentLoad.append(SegmentLoad_temp)
                    uindex = np.delete(uindex, Index)
                    length = len(uindex)        
           
            StoreHitSegment  =[]
            Coordinates = []
       
        CurrentHistoryNo = data[i,0]
        StoreHitSegment.append(data[i,-1])
        Coordinates_temp = [data[i,1], data[i,2], data[i,3]]
        Coordinates.append(Coordinates_temp)
       
        continue
    if(CurrentHistoryNo == data[i,0] and CurrentHistoryNo != 0): # Same particle history
        
        StoreHitSegment.append(data[i,-1])
        Coordinates_temp = [data[i,1], data[i,2], data[i,3]]
        Coordinates.append(Coordinates_temp)
        Historyflag = False
        continue

SegmentLoad = np.array(SegmentLoad)

min_z = 10.0
max_z = 30.0 + SegmentSize
min_y = -10.0
max_y = 10.0 + SegmentSize
bins_y = np.arange(min_z, max_z, SegmentSize) 
#bins_x = np.arange(-10.0, 20.0, 20.0)
bins_x = np.arange(min_y, max_y, SegmentSize)

h2d, xedges, yedges = np.histogram2d(SegmentLoad[:,1],SegmentLoad[:,2],[bins_x,bins_y])
h2d = np.rot90(h2d)
h2d = np.flipud(h2d)

TotalLoad = np.sum(np.sum(h2d))

h2d = h2d / IncidentParticles  # Normalized entries
TotalLoad = TotalLoad / IncidentParticles
HighestLoad = np.amax(h2d)
SmallestLoad = np.amin(h2d)

print("The total load (hits / incident neutron) is: " + str(TotalLoad))
print("The highest load (hits / incident neutron) per segment is: " + str(HighestLoad))

f = plt.figure()
ax = f.add_subplot(111)

plt.pcolormesh(bins_x, bins_y, h2d, edgecolors='k', norm=LogNorm())

v1 = np.linspace(SmallestLoad, HighestLoad, 5, endpoint=True)
plt.title( str(IncidentParticleEnergy) + " MeV neutrons with segmentation")
plt.xlabel("y [cm]")
plt.ylabel("z [cm]")
#plt.yscale("log")
#plt.colorbar().set_label("Total load per incident neutron", rotation=270, labelpad=20)
cb = plt.colorbar(ticks=v1)
cb.set_label("Load per incident neutron", rotation=270, labelpad=20)
cb.ax.set_yticklabels(["{:4.2e}".format(i) for i in v1])

plt.savefig('2DLoadDistribution.png', dpi=250, bbox_inches='tight')


f1 = open('DetectorLoad','a')
f1.write('Total load (hits / incident neutron) is: ' + str(TotalLoad) + '\n')
f1.write('Max. load (hits / incident neutron / segment) is: ' + str(HighestLoad) + '\n')
f1.write('Min. load (hits / incident neutron / segment) is: ' + str(SmallestLoad) + '\n')

#plt.show()
