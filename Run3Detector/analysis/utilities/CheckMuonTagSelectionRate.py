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


mycuts = milliqanCuts()

myplotter = milliqanPlotter()

#--------------------------------T3 condor job section 1-----------------------------
"""
def getFile(processNum, fileList):

        filelist = open(fileList)
        files = json.load(filelist)['filelist']
        filelist.close()

        return files[processNum]

    #run number, filelist
processNum = int(sys.argv[1])
fileList = sys.argv[2]


#condor debug
print(f"processNum {processNum}")



#get the filename to run over
filename = getFile(processNum, fileList)

if('.root' in filename and 'output' in filename):
    numRun = filename.split('_')[1].split('.')[0]

filelist =[f'{filename}:t']
"""








#--------------------------------non-condor job sec 1-----------------------------

#"""
numRun = str(sys.argv[1])
filelist =[f'/home/czheng/SimCosmicFlatTree/withPhotonMuontag/output_{numRun}.root:t']
print(filelist)


BigHitThreashold = int(sys.argv[2]) # the big hit threashold for the 


outputPath = str(sys.argv[3]) # the path is used at the very end for the output txt file
print(outputPath)
#"""



#----------------------------------extra function----------------------------------------
#TP: True(pass the muon geometric cut) possitive(is muon event)
#FP: False positive: (pass the muon geometric cut but it is not the muon event)
#TN: fail the gemoectric cut abd fail the muon event
#FN: fail the geometric cut and pass the muon event
def MuonGeoValidation(self):
    self.event["ST_TP"] = self.events["StraghtCosmic"] & self.events["muonEvent"]
    self.event["DW_TP"] = self.events["downwardPath"] & self.events["muonEvent"]
    self.event["CL_TP"] = self.events["Clean_MuonEvent"] & self.events["muonEvent"]

    self.event["ST_FP"] = self.events["StraghtCosmic"] & ~self.events["muonEvent"]
    self.event["DW_FP"] = self.events["downwardPath"] & ~self.events["muonEvent"]
    self.event["CL_FP"] = self.events["Clean_MuonEvent"] & ~self.events["muonEvent"]

    self.event["ST_TN"] = ~self.events["StraghtCosmic"] & ~self.events["muonEvent"]
    self.event["DW_TN"] = ~self.events["downwardPath"] & ~self.events["muonEvent"]
    self.event["CL_TN"] = ~self.events["Clean_MuonEvent"] & ~self.events["muonEvent"]

    self.event["ST_FN"] = ~self.events["StraghtCosmic"] & self.events["muonEvent"]
    self.event["DW_FN"] = ~self.events["downwardPath"] & self.events["muonEvent"]
    self.event["CL_FN"] = ~self.events["Clean_MuonEvent"] & self.events["muonEvent"]

    #count the number of event that pass the muonEvent but fail the DetectableMuon
    #there is a need to do the check like above. 
    self.event["IncompleteMuonE"] = self.events["muonEvent"] & ~self.events["DetectableMuon"]


setattr(mycuts, 'MuonGeoValidation', MuonGeoValidation)






#----------------------------------section for using analysis tool----------------------
branches = ["column","time","chan","runNumber","event","layer","nPE","type","row","muonHit"]


ST_TP_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'ST_TP')
DW_TP_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'DW_TP')
CL_TP_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'CL_TP')

ST_FP_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'ST_FP')
DW_FP_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'DW_FP')
CL_FP_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'CL_FP')

ST_TN_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'ST_TN')
DW_TN_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'DW_TN')
CL_TN_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'CL_TN')

ST_FN_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'ST_FN')
DW_FN_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'DW_FN')
CL_FN_count = mycuts.getCut(mycuts.countEvent,cutName = True,Countobject= 'CL_FN')

MuonEventCount = mycuts.getCut(mycuts.countEvent,'muonEvent')

inCompleteMuonEventCount = mycuts.getCut(mycuts.countEvent,'IncompleteMuonE')




DW_Muon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'downwardPath')
cleanMuon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'Clean_MuonEvent')
SIM_sudo_straight = mycuts.getCut(mycuts.sudo_straight,'StraghtCosmic', NPEcut = BigHitThreashold,time = "time", offlineData = False)


cutflow8 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.NbarsHitsCount,MuonEventCount,SIM_sudo_straight,MuonGeoValidation,DW_Muon_count,cleanMuon_count,ST_TP_count,DW_TP_count,CL_TP_count,ST_FP_count,DW_FP_count,CL_FP_count,ST_TN_count,DW_TN_count,CL_TN_count,ST_FN_count,DW_FN_count,CL_FN_count]

cutflow = cutflow8
myschedule = milliQanScheduler(cutflow, mycuts)
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts,fileCheckerEnable = False)


#"""
#-----------------------------non-condor job sec 2-------------------
if outputPath == '':
    myiterator.run()

#output result to txt file
else:
    with open(f'{outputPath}/Run{numRun}MuonGeoTag_NPE_{BigHitThreashold}.txt', 'w') as cfFile:
        sys.stdout = cfFile  # Change the standard output to the file
        myiterator.run() #output from counting function will be saved in the txt file above.



    # After the block, stdout will return to its default (usually the console)
    # reset stdout to its original state
    sys.stdout = sys.__stdout__
    

#-----------------------------end of non-condor job sec 2-------------------
#"""

#---------------------------T3 condor job sectiont 2------------------------
#the print satement will be save to out file.
"""

myiterator.run()
f_out = r.TFile(f"Run{numRun}CutFlow8.root", "RECREATE")
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
"""
#---------------------------end of T3 condor job------------------------