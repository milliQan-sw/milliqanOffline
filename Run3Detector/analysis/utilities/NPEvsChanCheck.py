"""
The goal of this file is to check how does the pickup & boardmatching can affect the number of hits at layer 2 and 3.

Previously, when doing cosmic muuon tag exploration, for the event that pass the tag1 / 2 I made the npe vs chan distribtuion for those events.
And I notice there is not much hit at layer 2 and 3. I suspect it is related the pickup tagging. 


tag1: there is a layer that both top and the bottom rows got big hits
tag2: there is a layer that both 4 rows got big hits
top & bottom row

This script is modified based on /home/czheng/scratch0/cosmicExplore/milliqanOffline/Run3Detector/analysis/utilities/CosmicTagPlots.py

"""

import ROOT as r
import os 
import sys
import time
import uproot 
import awkward as ak
from array import array
import numpy as np


#filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1190.4_v34.root:t']
#"""
runN = 1190
filelist = []

def appendRun(filelist,run):
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")
cosmicGoodRun = [runN]

for run in cosmicGoodRun:
    appendRun(filelist,run)

#"""

pulseBasedBranches = ["pickupFlag","layer","nPE","type","area","chan"]
branches = ["runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","area","chan"]

ChanVsbarNpeB = r.TH2F("B ChanvsNPE","bar chanvsmpe with pickup & board matching cut;chan; pulse NPE", 80,0,80,200,0,1000)
ChanVsbarNpeP = r.TH2F("P ChanvsNPE","panel chanvsmpe with pickup & board matching cut;chan; pulse NPE", 80,0,80,200,0,1000)


for events in uproot.iterate(
        filelist,
        branches,
        step_size=1000,
        num_workers=8,
        ):

        #"""

        for branch in pulseBasedBranches:
            events[branch] = events[branch][events.boardsMatched]
        for branch in pulseBasedBranches:
            events[branch] = events[branch][events.pickupFlag]

        #"""

        #separate get bar only pulses
        barCUT = events['type']==0
        for branch in pulseBasedBranches:
            events[branch] = events[branch][barCUT]

        npeList = ak.flatten(events.nPE,axis=None)
        chanList = ak.flatten(events.chan,axis=None)
        nPEarray = array('d', npeList)
        Chanarray = array('d', chanList)



        if (len(nPEarray) == len(Chanarray)):
            ChanVsbarNpeB.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))

for events2 in uproot.iterate(
        filelist,
        branches,
        step_size=1000,
        num_workers=8,
        ):
        #"""
        for branch in pulseBasedBranches:
            events2[branch] = events2[branch][events2.boardsMatched]
        for branch in pulseBasedBranches:
            events2[branch] = events2[branch][events2.pickupFlag]
        #"""

        #separate get panel only pulses
        panelCUT = events2['type']>0
        for branch in pulseBasedBranches:
            events2[branch] = events2[branch][panelCUT]
        
        events2["nPEEst"] = events2["area"]/1320

        npeList = ak.flatten(events2.nPEEst,axis=None)
        chanList = ak.flatten(events2.chan,axis=None)
        nPEarray = array('d', npeList)

        Chanarray = array('d', chanList)
        if len(Chanarray) == 0: continue


        if (len(nPEarray) == len(Chanarray)):
            
            ChanVsbarNpeP.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))






output_file = r.TFile("chanvsNPE_withcut.root", "RECREATE")
ChanVsbarNpeB.Write()
ChanVsbarNpeP.Write()
output_file.Close()

