import math


import os
import sys
import time
import json

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
import awkward as ak



#--------------------------------T3 condor job-----------------------------
"""
filelist = []

def appendRun(filelist):
    directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/"
    for filename in os.listdir(directory):
        if filename.startswith("output") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")


appendRun(filelist)

"""

mycuts = milliqanCuts()

myplotter = milliqanPlotter()

#--------------------------------non-condor job-----------------------------


numRun = str(sys.argv[1])
filelist =[f'/home/czheng/SimCosmicFlatTree/withPhotonMuontag/output_{numRun}.root:t']
print(filelist)

outputPath = str(sys.argv[2]) # the path is used at the very end for the output txt file
print(outputPath)



#----------------------------------section for using analysis tool----------------------
branches = ["column","time","chan","runNumber","event","layer","nPE","type","row","muonHit"]

DW_Muon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'downwardPath')
cleanMuon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'Clean_MuonEvent')
SIM_sudo_straight = mycuts.getCut(mycuts.sudo_straight,'StraghtCosmic', NPEcut = 20,time = "time", offlineData = False)
Bar_NPE_DW = r.TH1F("Bar_NPE_DW", "nPE bar; nPE ; bar", 500, 0, 1000)
Bar_NPE_St = r.TH1F("Bar_NPE_St", "nPE bar; nPE ; bar", 500, 0, 1000)
Bar_NPE_CL = r.TH1F("Bar_NPE_CL", "nPE bar; nPE ; bar", 500, 0, 1000)



NuniqueBar_DW = r.TH1F("NuniqueBar_DW" , "NuniqueBar DW;number of unique bar;events",50,0,50)
NuniqueBar_CL = r.TH1F("NuniqueBar_CL" , "NuniqueBar CL;number of unique bar;events",50,0,50)
NuniqueBar_ST = r.TH1F("NuniqueBar_ST" , "NuniqueBar ST;number of unique bar;events",50,0,50)

myplotter.addHistograms(NuniqueBar_DW, 'NBarsHits', 'downwardPath')
myplotter.addHistograms(NuniqueBar_ST, 'NBarsHits', 'StraghtCosmic')
myplotter.addHistograms(NuniqueBar_CL, 'NBarsHits', 'Clean_MuonEvent')



#adding combine cuts for downwardPath
dw_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'dw_bar_cf8', ["downwardPath", "barCut"])
dw_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'dw_panel_cf8', ["downwardPath", "panelCut"])

#adding combine cuts for StraghtCosmic
St_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'St_bar_cf8', ["StraghtCosmic", "barCut"])
St_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'St_panel_cf8', ["StraghtCosmic", "panelCut"])

#adding combine cuts for Clean_MuonEvent
CL_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'CL_bar_cf8', ["Clean_MuonEvent", "barCut"])
CL_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'CL_panel_cf8', ["Clean_MuonEvent", "panelCut"])

myplotter.addHistograms(Bar_NPE_DW, 'nPE', 'dw_bar_cf8')
myplotter.addHistograms(Bar_NPE_St, 'nPE', 'St_bar_cf8')
myplotter.addHistograms(Bar_NPE_CL, 'nPE', 'CL_bar_cf8')

#-----------------plots for NPE and NPE ratio with layer constaints and time difference----------------
Dt = mycuts.getCut(mycuts.findCorrectTime, 'placeholder',cut = None,timeData = "time",offlineMode = True)

Dt_CL =  r.TH1F("Dt_CL" , "D_t CL;D_t ns; Events",6000,-3000,3000)
Dt_ST =  r.TH1F("Dt_ST" , "D_t ST;D_t ns; Events",6000,-3000,3000)
Dt_DW =  r.TH1F("Dt_DW" , "D_t ST;D_t ns; Events",6000,-3000,3000)

myplotter.addHistograms(Dt_ST, 'DTL0L3', 'StraghtCosmic') 
myplotter.addHistograms(Dt_DW, 'DTL0L3', 'downwardPath') 
myplotter.addHistograms(Dt_CL, 'DTL0L3', 'Clean_MuonEvent') 

Muon_adj_layer_CL = mycuts.getCut(mycuts.combineCuts, 'Muon_adj_layer_CL', ["MuonADJLayers","Clean_MuonEvent"])
Muon_adj_layer_ST = mycuts.getCut(mycuts.combineCuts, 'Muon_adj_layer_ST', ["MuonADJLayers","StraghtCosmic"])
Muon_adj_layer_DW = mycuts.getCut(mycuts.combineCuts, 'Muon_adj_layer_DW', ["MuonADJLayers_DW","downwardPath"])


adj_NPE_CL = r.TH1F("adj_NPE_CL", "nPE muon event adjacnet layer CL", 100, 0, 100)
myplotter.addHistograms(adj_NPE_CL	, 'nPE', 'Muon_adj_layer_CL')

adj_NPE_DW = r.TH1F("adj_NPE_DW", "nPE muon event adjacnet layer CL", 100, 0, 100)
myplotter.addHistograms(adj_NPE_DW	, 'nPE', 'Muon_adj_layer_DW')

adj_NPE_ST = r.TH1F("adj_NPE_ST", "nPE muon event adjacnet layer ST", 100, 0, 100)
myplotter.addHistograms(adj_NPE_ST	, 'nPE', 'Muon_adj_layer_ST')

NpeRatio_adj_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_adj_tag",cut = "MuonADJLayers") #The tag "NpeRatio_adj_tag" can be used to extract the NPE ratio for ST and CL event.
NpeRatio_adj_DW_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_adj_DW_tag",cut = "MuonADJLayers_DW")
NPERatio_CL = r.TH1F("NPERatio_CL","NPE ratio CL adj;max NPE/min NPE;Events",5000,0,5000)
NPERatio_DW = r.TH1F("NPERatio_DW","NPE ratio DW adj;max NPE/min NPE;Events",5000,0,5000)
NPERatio_ST = r.TH1F("NPERatio_ST","NPE ratio ST adj;max NPE/min NPE;Events",5000,0,5000)
myplotter.addHistograms(NPERatio_CL, 'NpeRatio_adj_tag', 'Clean_MuonEvent')
myplotter.addHistograms(NPERatio_ST, 'NpeRatio_adj_tag', 'StraghtCosmic')
myplotter.addHistograms(NPERatio_DW, 'NpeRatio_adj_DW_tag', 'downwardPath')

cutflow8 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.NbarsHitsCount,SIM_sudo_straight,dw_bar_cf8,dw_panel_cf8,St_bar_cf8,St_panel_cf8,CL_bar_cf8,CL_panel_cf8,DW_Muon_count,cleanMuon_count,myplotter.dict['NuniqueBar_DW'],myplotter.dict['NuniqueBar_ST'],myplotter.dict['NuniqueBar_CL'],myplotter.dict['Bar_NPE_DW'],myplotter.dict['Bar_NPE_St'],myplotter.dict['Bar_NPE_CL'], Dt, myplotter.dict['Dt_ST'], myplotter.dict['Dt_DW'],myplotter.dict['Dt_CL'],Muon_adj_layer_CL,Muon_adj_layer_ST,Muon_adj_layer_DW , myplotter.dict['adj_NPE_CL'], myplotter.dict['adj_NPE_DW'],myplotter.dict['adj_NPE_ST'],NpeRatio_adj_tag,NpeRatio_adj_DW_tag,myplotter.dict['NPERatio_CL'],myplotter.dict['NPERatio_DW'],myplotter.dict['NPERatio_ST'] ]

cutflow = cutflow8
myschedule = milliQanScheduler(cutflow, mycuts)
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts,fileCheckerEnable = False)
#-----------------------------save the txt and root file without condor job-------------------
if outputPath == '':
    myiterator.run()

#output result to txt file
else:
    with open(f'{outputPath}/Run{numRun}CutFlow7.txt', 'w') as cfFile:
        sys.stdout = cfFile  # Change the standard output to the file
        myiterator.run() #output from counting function will be saved in the txt file above.



    # After the block, stdout will return to its default (usually the console)
    # reset stdout to its original state
    sys.stdout = sys.__stdout__
    
    f_out = r.TFile(f"{outputPath}/Run{numRun}CutFlow7.root", "RECREATE")
    Bar_NPE_DW.Write()
    Bar_NPE_St.Write()
    Bar_NPE_CL.Write()
    NuniqueBar_DW.Write()
    NuniqueBar_CL.Write()
    NuniqueBar_ST.Write()
    Dt_CL.Write()
    Dt_ST.Write()
    Dt_DW.Write()
    adj_NPE_CL.Write()
    adj_NPE_DW.Write()
    adj_NPE_ST.Write()
    NPERatio_CL.Write()
    NPERatio_DW.Write()
    NPERatio_ST.Write()
    f_out.Close()


#---------------------------save the files when using condor jobs------------------------
#the print satement will be save to out file.
#
"""
with open(f'{outputPath}/Run{numRun}CutFlow7.txt', 'w') as cfFile:
        sys.stdout = cfFile  # Change the standard output to the file
        myiterator.run() #output from counting function will be saved in the txt file above.



    # After the block, stdout will return to its default (usually the console)
    # reset stdout to its original state
    sys.stdout = sys.__stdout__
    
    f_out = r.TFile(f"{outputPath}/Run{numRun}CutFlow7.root", "RECREATE")
    M_adj_NPE_C.Write()
    M_NPE_C.Write()
    NPERatio_C.Write()
    CorrectTime_OL.Write()
    CorrectTime_default_OL.Write()
    NpeRatio_adj.Write()
    NpeRatio_ot.Write()
    NuniqueBar_C.Write()
    f_out.Close()


"""
