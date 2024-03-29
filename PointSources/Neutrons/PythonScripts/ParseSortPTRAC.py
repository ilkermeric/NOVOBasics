# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 12:35:46 2019

@author: Ilker Meric

Parse MCNP PTRAC output and sort the events in the succession order.

Note: This script only keeps track of BankType() == 12, i.e. only
Compton recoil electrons. Secondry electrons from photoelectric effect
& pair production are ignored for now.

"""

from mcnptools import Ptrac
import numpy as np
import matplotlib.pyplot as plt
import sys

plt.rc('font',  size=12)  # controls default text sizes
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('figure', titlesize=12)    # fontsize of title

if(len(sys.argv) != 2):
    raise RuntimeError ("Please pass all the arguments!" ) 
filename = sys.argv[1]

print("Processing file: " + str(filename))

p = Ptrac(filename, Ptrac.BIN_PTRAC)


SortedEntries = []

hists = p.ReadHistories(10000)

while hists:
    
    for h in hists:
        EventParameters = []
        EventParameters_temp = []
        eventcnt = 0
        history = h.GetNPS()
        if(int(history.NPS())%10000 == 0):
            print("Processing History: " + str(history.NPS()))
        
        for e in range(h.GetNumEvents()):
            event = h.GetEvent(e)
            
            if(event.Type() == Ptrac.BNK):
                if(event.BankType() == 34 or event.BankType() == 30):
                    #if(event.Get(Ptrac.ENERGY) >= RPCutoff):
                        EventParameters_temp = [history.NPS(), event.Get(Ptrac.X), event.Get(Ptrac.Y),
                                                event.Get(Ptrac.Z), event.Get(Ptrac.ENERGY),
                                                event.Get(Ptrac.TIME)]
                        EventParameters.append(EventParameters_temp)
                        eventcnt += 1
        
        if(eventcnt == 0):
            continue
        EventParameters = np.array(EventParameters)
        for i in range(len(EventParameters)):
            SortIndex = np.argmin(EventParameters[:,5])
            SortedEntries.append(EventParameters[SortIndex,:])
            EventParameters = np.delete(EventParameters, obj=SortIndex, axis=0)
           # print(SortedEntries)
            
        
    
    hists = p.ReadHistories(10000)

f = open('SortedPTRACData','a')
np.savetxt(f, SortedEntries, delimiter=' ', fmt=['%.10i', '%.10f', '%.10f',
                                                  '%.10f', '%.10f', '%.10f'])

plt.show()