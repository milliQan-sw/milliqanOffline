#collect the range of NPE for event that is tagged & channel that has hit above 20 NPE(plot chan vs NPE).
#The head(max) of NPE distribution is for cosmic muon and the tail is for low energy photon 
#there is need to get the origianl event since I used bar & NPE trim


import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np




def plots(RunNum,eventNum,BARNPEvsChanplot = None,PanelNPEvsChanplot = None,NBarsHit = None,DTHist=None,NPERatio=None):

    pulseBasedBranches = ["layer","nPE","type","chan","row","column","time"]
    branches = ["runNumber","event","layer","nPE","type","chan","row","column","time"]
    filelist =[f'/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/output_{RunNum}.root:t']
    
    for events in uproot.iterate(
                filelist,
                branches,
                step_size=10000,
                num_workers=8,
                ):

                #extract the intersting events
                events =  events[events.event == eventNum]
                barEvents = events
                
                
                #separate to get bar only data
                barCUT = barEvents['type']==0
                for branch in pulseBasedBranches:
                    barEvents[branch] = barEvents[branch][barCUT]
                #print(ak.to_pandas(events))
                npeList = ak.flatten(barEvents.nPE,axis=None)
                chanList = ak.flatten(barEvents.chan,axis=None)
                nPEarray = array('d', npeList)
                Chanarray = array('d', chanList)

                if len(nPEarray) == 0: continue

                if (BARNPEvsChanplot != None) & (len(nPEarray) == len(Chanarray)):
                    BARNPEvsChanplot.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))
                
                if (NBarsHit != None):
                    uniqueBars = ak.Array([np.unique(x) for x in barEvents.chan])
                    NumberOfBarHits = ak.count(uniqueBars, axis = 1)
                    NBarsHit.FillN(len(NumberOfBarHits), NumberOfBarHits, np.ones(len(NumberOfBarHits)))
                

                dT = 3.96 #The shortest time for photon travel 1 bar scitillator + 1 air gap between two bars.
                Lay0Time=barEvents["time"][barEvents.layer==0]
                Lay1Time=barEvents["time"][barEvents.layer==1] -dT
                Lay2Time=barEvents["time"][barEvents.layer==2] -2*dT
                Lay3Time=barEvents["time"][barEvents.layer==3] -3*dT
                CorretTimeArray = np.concatenate((Lay0Time, Lay1Time,Lay2Time,Lay3Time), axis=1)
                CorretTimeDiff = (np.max(CorretTimeArray,axis=1)-np.min(CorretTimeArray,axis=1)).tolist()
                DTHist.FillN(len(CorretTimeDiff), CorretTimeDiff, np.ones(len(CorretTimeDiff)))

                NpeRatioArr = (np.max(barEvents.nPE,axis=1) / np.min(barEvents.nPE,axis=1)).tolist()
                NPERatio.FillN(len(NpeRatioArr), NpeRatioArr, np.ones(len(NpeRatioArr)))


                #-----------------------
                panelEvents = events
                #separate get panel only pulses
                panelEvents = panelEvents['type']>0
                

                for branch in pulseBasedBranches:
                    panelEvents[branch] = panelEvents[branch][panelCUT]


                npeList2 = ak.flatten(panelEvents.nPE,axis=None)
                chanList2 = ak.flatten(panelEvents.chan,axis=None)
                nPEarray2 = array('d', npeList2)

                Chanarray2 = array('d', chanList2)
                if len(Chanarray2) == 0: continue
		

                if (PanelNPEvsChanplot != None) & (len(nPEarray2) == len(Chanarray2)):
                    
                    PanelNPEvsChanplot.FillN(len(nPEarray2), Chanarray2, nPEarray2, np.ones(len(nPEarray2)))
    #"""



