import numpy as np
import pandas as pd
import ROOT as r
import os 
import sys
import time
import uproot 


filelist ='/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1035.100_v34.root'

fin = uproot.open(filelist)
tree = fin['t']
data = tree.arrays(["event","layer","height","pickupFlag","type","nPE","layer","chan"],library='pd')

NPE_height = r.TH2F("h_NPE","h_npe;height;NPE",1250, 0, 1250,100,0,100)

N_bar = r.TH1F("NBar","Nbar;Nbar;# of event",20,0,20)

NumEvent = data["event"].max() + 1

AL1HitCout = 0
for event in range(NumEvent):
    selected_data = data[data["event"] == event]
    pickupFlagList = selected_data["pickupFlag"]
    height_list=selected_data["height"]
    type_list = selected_data["type"]
    npe_list = selected_data["nPE"]
    layer_list = selected_data["layer"]
    chan_list = selected_data["chan"]
    
    layerSet = set()
    chanSet = set()
    for pickUp,height,Type,npe,layer,chan in zip(pickupFlagList,height_list,type_list,npe_list,layer_list,chan_list):
        if len(pickupFlagList) != 0 and pickUp == False and Type ==0:
            pass
        else:
            continue
            
        NPE_height.Fill(height,npe)
        #print(height,npe)
        layerSet.add(layer)
        chanSet.add(chan)
    if len(layerSet) == 4:
        N_bar.Fill(len(chanSet))
        print("found one !")
        AL1HitCout = 1 + AL1HitCout

if (AL1HitCout >= 1):
    root_file = r.TFile("output.root", "RECREATE")
    NPE_height.Write()
    N_bar.Write()
    root_file.Close()

"""
c1 = r.TCanvas("c1", "c1", 500, 400)
c1.cd()
NPE_height.Draw()
c1.Draw()


c2 = r.TCanvas("c1", "c1", 500, 400)
c2.cd()
N_bar.Draw()
c2.Draw()
"""