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

cleanMuon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'Clean_MuonEvent')
clean_Muon_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_layer', ["MuonLayers","Clean_MuonEvent"])
clean_Muon_adj_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_adj_layer', ["MuonADJLayers","Clean_MuonEvent"])
clean_Muon_Dt = mycuts.getCut(mycuts.findCorrectTime, 'placeholder',cut = None,timeData = "time")
M_NPE_C = r.TH1F("M_NPE_C", "nPE muon event layer", 100, 0, 100)
M_adj_NPE_C = r.TH1F("M_adj_NPE_C", "nPE muon event adjacnet layer", 100, 0, 100)
myplotter.addHistograms(M_NPE_C, 'nPE', 'clean_Muon_layer')
myplotter.addHistograms(M_adj_NPE_C	, 'nPE', 'clean_Muon_adj_layer')
NuniqueBar_C = r.TH1F("NuniqueBar_C" , "NuniqueBar;number of unique bar;events",50,0,50)
myplotter.addHistograms(NuniqueBar_C, 'NBarsHits', 'Clean_MuonEvent')



NpeRatio_adj = r.TH1F("NpeRatio_adj","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
NpeRatio_adj_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_adj_tag",cut = "MuonADJLayers") 
myplotter.addHistograms(NpeRatio_adj, 'NpeRatio_adj_tag', 'Clean_MuonEvent')

#non- muon layer
NpeRatio_ot_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_ot_tag",cut = "MuonADJLayers")
NpeRatio_ot = r.TH1F("NpeRatio_ot","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
myplotter.addHistograms(NpeRatio_ot, 'NpeRatio_ot_tag', 'Clean_MuonEvent')



#extra histogram for Offline data
CorrectTime_OL =  r.TH1F("CorrectTime_OL" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
myplotter.addHistograms(CorrectTime_OL, 'DTL0L3', 'Clean_MuonEvent') 
#CorrectTime_default_OL is to check what does CorrectTime should look like without the Clean muon cut
CorrectTime_default_OL =  r.TH1F("CorrectTime_default_OL" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
myplotter.addHistograms(CorrectTime_default_OL, 'DTL0L3', 'StraghtCosmic') 



NPERatio_C = r.TH1F("NPERatio_C","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
myplotter.addHistograms(NPERatio_C, 'BarNPERatio', 'Clean_MuonEvent')
#FIXME:mycuts.offlinePreProcess   this method cause the find correctTime crash 
cutflow7 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.BarNPERatioCalculate,mycuts.NbarsHitsCount,mycuts.sudo_straight,NpeRatio_adj_tag,NpeRatio_ot_tag,clean_Muon_layer,clean_Muon_adj_layer,cleanMuon_count,clean_Muon_Dt,myplotter.dict['M_NPE_C'],myplotter.dict['M_adj_NPE_C'],myplotter.dict["NuniqueBar_C"],myplotter.dict["NPERatio_C"],myplotter.dict["CorrectTime_OL"],myplotter.dict["CorrectTime_default_OL"],myplotter.dict["NpeRatio_adj"],myplotter.dict["NpeRatio_ot"]]    


cutflow = cutflow7
myschedule = milliQanScheduler(cutflow, mycuts)
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)
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
    M_adj_NPE_C.Write()
    M_NPE_C.Write()
    NPERatio_C.Write()
    CorrectTime_OL.Write()
    CorrectTime_default_OL.Write()
    NpeRatio_adj.Write()
    NpeRatio_ot.Write()
    NuniqueBar_C.Write()
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
