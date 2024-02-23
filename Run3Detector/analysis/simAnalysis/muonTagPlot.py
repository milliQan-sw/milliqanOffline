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


def plots(RunNum,eventNum,BARNPEvsChanplot = None,PanelNPEvsChanplot = None):

    pulseBasedBranches = ["layer","nPE","type","chan","row","column"]
    branches = ["runNumber","event","layer","nPE","type","chan","row","column"]
    filelist =[f'/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/output_{RunNum}.root:t']
    
    for events in uproot.iterate(
                filelist,
                branches,
                step_size=10000,
                num_workers=8,
                ):

                #extract the intersting events
                events =  events[events.event == eventNum]
                
                #separate get bar only pulses
                barCUT = events['type']==0
                for branch in pulseBasedBranches:
                    events[branch] = events[branch][barCUT]
                #print(ak.to_pandas(events))
                npeList = ak.flatten(events.nPE,axis=None)
                chanList = ak.flatten(events.chan,axis=None)
                nPEarray = array('d', npeList)
                Chanarray = array('d', chanList)

                if len(nPEarray) == 0: continue

                if (BARNPEvsChanplot != None) & (len(nPEarray) == len(Chanarray)):
                    BARNPEvsChanplot.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))
    #"""
    for events2 in uproot.iterate(
                filelist,
                branches,
                step_size=10000,
                num_workers=8,
                ):



                #extract the intersting events
                events2 =  events2[events2.event == eventNum]
                #print(ak.to_pandas(events2))
                #print(ak.to_list(events2))
                #separate get bar only pulses
                panelCUT = events2['type']>0
                
                #print(events2['type'])#debug
                #print(events2['layer'])
                for branch in pulseBasedBranches:
                    #print(branch) #debug
                    #print(len(events2[branch])) #debug
                    #print(events2[branch]) #debug
                    #print(len(panelCUT)) #debug
                    #print(panelCUT) #debug
                    events2[branch] = events2[branch][panelCUT]


                npeList = ak.flatten(events2.nPE,axis=None)
                chanList = ak.flatten(events2.chan,axis=None)
                nPEarray = array('d', npeList)
                #print(npeList)
                Chanarray = array('d', chanList)
                if len(Chanarray) == 0: continue
		

                if (PanelNPEvsChanplot != None) & (len(nPEarray) == len(Chanarray)):
                    
                    PanelNPEvsChanplot.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))
    #"""



