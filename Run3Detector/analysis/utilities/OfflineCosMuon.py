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



branches = ["height","timeFit_module_calibrated","chan","runNumber","column","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row","area"]


#--------------------------------T3 condor job-----------------------------
"""
#need to check this one.
def getFile(processNum, fileList):

    filelist = open(fileList)
    files = json.load(filelist)['filelist']
    filelist.close()

    return files[processNum]

    #run number, filelist
    processNum = int(sys.argv[1])
    fileList = sys.argv[2]


    #get the filename to run over
    filename = getFile(processNum, fileList)

    if('.root' in filename and 'output' in filename):
        numRun = filename.split('_')[1].split('.')[0].replace('Run', '')

    #filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/offlinefile/output_1.root:t']
    filelist =[f'{filename}:t']

"""


#--------------------------------Non condor job--------------------------------
numRun = str(sys.argv[1])
fileNum = str(sys.argv[2])
filelist =[f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_Run{numRun}.{fileNum}_v34.root:t']
print(filelist)

outputPath = str(sys.argv[3]) # the path is used at the very end for the output txt file
print(outputPath)


#-------------------------------------------------------------------------
mycuts = milliqanCuts()

myplotter = milliqanPlotter()


#new count for downwardPath
DW_Muon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'downwardPath')
OL_sudo_straight = mycuts.getCut(mycuts.sudo_straight,'StraghtCosmic', NPEcut = 20,time = "timeFit_module_calibrated")
cleanMuon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'Clean_MuonEvent')


#--------------------------plots for N-bars, plots for area and npe(without layer constaints). ---------
#histograms for downwardPath
Bar_Area_DW = r.TH1F("Bar_Area_DW", "area bar; area ; pulse", 7000, 0, 700000)
Bar_NPE_DW = r.TH1F("Bar_NPE_DW", "nPE bar; nPE ; pulse", 500, 0, 1000)
Slab_Area_DW = r.TH1F("Slab_Area_DW", "area Slab; area ; pulse", 7000, 0, 700000)
#for offline file V34, the npe is the same as pulse area. So I only draw the 2D histogram for bars
Bar_NPE_Area_DW = r.TH2F("Bar_NPE_Area_DW", "bar channels; nPE; area",20,0,1000,20, 0, 700000)

NuniqueBar_DW = r.TH1F("NuniqueBar_DW" , "NuniqueBar DW;number of unique bar;events",50,0,50)
NuniqueBar_CL = r.TH1F("NuniqueBar_CL" , "NuniqueBar CL;number of unique bar;events",50,0,50)
NuniqueBar_ST = r.TH1F("NuniqueBar_ST" , "NuniqueBar ST;number of unique bar;events",50,0,50)

myplotter.addHistograms(NuniqueBar_DW, 'NBarsHits', 'downwardPath')
myplotter.addHistograms(NuniqueBar_ST, 'NBarsHits', 'StraghtCosmic')
myplotter.addHistograms(NuniqueBar_CL, 'NBarsHits', 'Clean_MuonEvent')


#histograms for StraghtCosmic
Bar_Area_St = r.TH1F("Bar_Area_St", "area bar; area ; pulse", 7000, 0, 700000)
Bar_NPE_St = r.TH1F("Bar_NPE_St", "nPE bar; nPE ; pulse", 500, 0, 1000)
Slab_Area_St = r.TH1F("Slab_Area_St", "area Slab; area ; pulse", 7000, 0, 700000)
Bar_NPE_Area_St = r.TH2F("Bar_NPE_Area_St", "bar channels; nPE; area",20,0,1000,20, 0, 700000)

#histograms for Clean_MuonEvent
Bar_Area_CL = r.TH1F("Bar_Area_CL", "area bar; area ; pulse", 7000, 0, 700000)
Bar_NPE_CL = r.TH1F("Bar_NPE_CL", "nPE bar; nPE ; pulse", 500, 0, 1000)
Slab_Area_CL = r.TH1F("Slab_Area_CL", "area Slab; area ; pulse", 7000, 0, 700000)
Bar_NPE_Area_CL = r.TH2F("Bar_NPE_Area_CL", "bar channels; nPE; area",20,0,1000,20, 0, 700000)


#adding combine cuts for downwardPath
dw_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'dw_bar_cf8', ["downwardPath", "barCut"])
dw_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'dw_panel_cf8', ["downwardPath", "panelCut"])

#adding combine cuts for StraghtCosmic
St_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'St_bar_cf8', ["StraghtCosmic", "barCut"])
St_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'St_panel_cf8', ["StraghtCosmic", "panelCut"])

#adding combine cuts for Clean_MuonEvent
CL_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'CL_bar_cf8', ["Clean_MuonEvent", "barCut"])
CL_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'CL_panel_cf8', ["Clean_MuonEvent", "panelCut"])



#add hists with tags
myplotter.addHistograms(Bar_Area_DW, 'area', 'dw_bar_cf8')
myplotter.addHistograms(Bar_NPE_DW, 'nPE', 'dw_bar_cf8')
myplotter.addHistograms(Slab_Area_DW, 'area', 'dw_panel_cf8')
myplotter.addHistograms(Bar_NPE_Area_DW, ['nPE','area'], 'dw_bar_cf8')

myplotter.addHistograms(Bar_Area_St, 'area', 'St_bar_cf8')
myplotter.addHistograms(Bar_NPE_St, 'nPE', 'St_bar_cf8')
myplotter.addHistograms(Slab_Area_St, 'area', 'St_panel_cf8')
myplotter.addHistograms(Bar_NPE_Area_St, ['nPE','area'], 'St_bar_cf8')


myplotter.addHistograms(Bar_Area_CL, 'area', 'CL_bar_cf8')
myplotter.addHistograms(Bar_NPE_CL, 'nPE', 'CL_bar_cf8')
myplotter.addHistograms(Slab_Area_CL, 'area', 'CL_panel_cf8')
myplotter.addHistograms(Bar_NPE_Area_CL, ['nPE','area'], 'CL_bar_cf8')


#-----------------plots for NPE and NPE ratio with layer constaints and time difference----------------
Dt = mycuts.getCut(mycuts.findCorrectTime, 'placeholder',cut = None,timeData = "timeFit_module_calibrated",offlineMode = True)

Dt_CL =  r.TH1F("Dt_CL" , "D_t CL;D_t ns; Events",6000,-3000,3000)
Dt_ST =  r.TH1F("Dt_ST" , "D_t ST;D_t ns; Events",6000,-3000,3000)
Dt_DW =  r.TH1F("Dt_DW" , "D_t ST;D_t ns; Events",6000,-3000,3000)

myplotter.addHistograms(Dt_ST, 'DTL0L3', 'StraghtCosmic') 
myplotter.addHistograms(Dt_DW, 'DTL0L3', 'downwardPath') 
myplotter.addHistograms(Dt_CL, 'DTL0L3', 'Clean_MuonEvent') 


Muon_adj_layer_CL = mycuts.getCut(mycuts.combineCuts, 'Muon_adj_layer_CL', ["MuonADJLayers","Clean_MuonEvent"])
Muon_adj_layer_ST = mycuts.getCut(mycuts.combineCuts, 'Muon_adj_layer_ST', ["MuonADJLayers","StraghtCosmic"])
Muon_adj_layer_DW = mycuts.getCut(mycuts.combineCuts, 'Muon_adj_layer_DW', ["MuonADJLayers_DW","downwardPath"])

#Pulse at muon event layer are not super interesting in my anlaysis. But you can uncomment it if needed.
#Muon_layer_CL = mycuts.getCut(mycuts.combineCuts, 'Muon_layer_CL', ["MuonLayers","Clean_MuonEvent"])
#Muon_layer_ST = mycuts.getCut(mycuts.combineCuts, 'Muon_layer_ST', ["MuonLayers","StraghtCosmic"])
#Muon_layer_DW = mycuts.getCut(mycuts.combineCuts, 'Muon_layer_DW', ["MuonLayers_DW","downwardPath"])


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


cutflow8 = [mycuts.offlinePreProcess,mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.NbarsHitsCount,OL_sudo_straight,dw_bar_cf8,dw_panel_cf8,St_bar_cf8,St_panel_cf8,CL_bar_cf8,CL_panel_cf8,DW_Muon_count,cleanMuon_count,mycuts.findMaxNPE,myplotter.dict['NuniqueBar_DW'],myplotter.dict['NuniqueBar_ST'],myplotter.dict['NuniqueBar_CL'],myplotter.dict['Bar_Area_DW'],myplotter.dict['Bar_NPE_DW'],myplotter.dict['Slab_Area_DW'],myplotter.dict['Bar_NPE_Area_DW'],myplotter.dict['Bar_Area_St'],myplotter.dict['Bar_NPE_St'],myplotter.dict['Slab_Area_St'],myplotter.dict['Bar_NPE_Area_St'],myplotter.dict['Bar_Area_CL'],myplotter.dict['Bar_NPE_CL'],myplotter.dict['Slab_Area_CL'],myplotter.dict['Bar_NPE_Area_CL'], Dt, myplotter.dict['Dt_ST'], myplotter.dict['Dt_DW'],myplotter.dict['Dt_CL'],Muon_adj_layer_CL,Muon_adj_layer_ST,Muon_adj_layer_DW , myplotter.dict['adj_NPE_CL'], myplotter.dict['adj_NPE_DW'],myplotter.dict['adj_NPE_ST'],NpeRatio_adj_tag,NpeRatio_adj_DW_tag,myplotter.dict['NPERatio_CL'],myplotter.dict['NPERatio_DW'],myplotter.dict['NPERatio_ST'] ]



cutflow = cutflow8

myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts,fileCheckerEnable=False)

#myiterator.run() # comment this out when checking cut efficiency

#--------------section for using to check cut efficiency-----------------------------
print(outputPath)
if outputPath == '':
    myiterator.run()

#output result to txt file
else:
    with open(f'{outputPath}/Run{numRun}_file{fileNum}CutFlow8.txt', 'w') as cfFile:
        sys.stdout = cfFile  # Change the standard output to the file
        myiterator.run() #output from counting function will be saved in the txt file above.



    # After the block, stdout will return to its default (usually the console)
    # reset stdout to its original state
    sys.stdout = sys.__stdout__

    f_out = r.TFile(f"{outputPath}/Run{numRun}_file{fileNum}_CutFlow8.root", "RECREATE")
    """#histograms for cutflow 7
    M_adj_NPE_C.Write()
    M_NPE_C.Write()
    NPERatio_C.Write()
    CorrectTime_OL.Write()
    CorrectTime_default_OL.Write()
    NpeRatio_adj.Write()
    NpeRatio_ot.Write()
    NuniqueBar_C.Write()
    """
    Bar_Area_DW.Write()
    Bar_NPE_DW.Write()
    Slab_Area_DW.Write()
    Bar_NPE_Area_DW.Write()
    Bar_Area_St.Write()
    Bar_NPE_St.Write()
    Slab_Area_St.Write()
    Bar_NPE_Area_St.Write()
    Bar_Area_CL.Write()
    Bar_NPE_CL.Write()
    Slab_Area_CL.Write()
    Bar_NPE_Area_CL.Write()
    NuniqueBar_DW.Write()
    NuniqueBar_ST.Write()
    NuniqueBar_CL.Write()
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
