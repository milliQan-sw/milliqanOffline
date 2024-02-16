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


def plots(RunNum,filenum,eventNum,BARNPEvsChanplot = None,PanelNPEvsChanplot = None):

    pulseBasedBranches = ["pickupFlag","layer","nPE","type","area","chan"]
    branches = ["runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","area","chan"]
    filelist =[f'/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run{RunNum}.{filenum}_v34.root:t']
    
    for events in uproot.iterate(
                filelist,
                branches,
                step_size=1000,
                num_workers=8,
                ):

                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events.boardsMatched]
                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events.pickupFlag]

                #extract the intersting events
                events =  events[events.event == eventNum]
                
                #separate get bar only pulses
                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events['type']==0]

                npeList = ak.flatten(events.nPE,axis=None)
                chanList = ak.flatten(events.chan,axis=None)
                nPEarray = array('d', npeList)
                Chanarray = array('d', chanList)



                if (BARNPEvsChanplot != None) & (len(nPEarray) == len(Chanarray)):
                    BARNPEvsChanplot.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))
    
    for events in uproot.iterate(
                filelist,
                branches,
                step_size=1000,
                num_workers=8,
                ):

                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events.boardsMatched]
                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events.pickupFlag]

                #extract the intersting events
                events =  events[events.event == eventNum]
                
                #separate get bar only pulses
                for branch in pulseBasedBranches:
                    events[branch] = events[branch][events['type']>0]
                
                events["nPEEst"] = events["area"]/1320

                npeList = ak.flatten(events.nPEEst,axis=None)
                chanList = ak.flatten(events.chan,axis=None)
                nPEarray = array('d', npeList)
                print(npeList)
                Chanarray = array('d', chanList)
                if len(Chanarray) == 0: continue
		

                if (PanelNPEvsChanplot != None) & (len(nPEarray) == len(Chanarray)):
                    
                    PanelNPEvsChanplot.FillN(len(nPEarray), Chanarray, nPEarray, np.ones(len(nPEarray)))



if __name__ == "__main__":




    #tag1: top & bottom rows have big hits
    #tag2: 4 rows haves big hits

    #hitograms

    #panel pulse npe distribution
    #panPulseDistTag1 = 
    #panPulseDistTag2 =


    ChanVsbarNpeTag1 = r.TH2F("ChanvsNPE","chanvsmpe;chan;pulse NPE", 80,0,80,200,0,1000)
    #ChanVsbarNpeTag2

    plots(1190,100,249,ChanVsbarNpeTag1)

    output_file = r.TFile("chanvsNPEtest.root", "RECREATE")
    ChanVsbarNpeTag1.Write()

    output_file.Close()


    #plotting function

    #pickup & board matching cuts

