import ROOT as r
import pickle
import os
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)

inputFile = r.TFile("/Users/mcitron/milliqanOffline/milliqanScripts/inputFiles/allPhysicsAndTripleChannelSinceTS1.root")
# inputFile = r.TFile("allTripleCoinc.root")
tree = inputFile.Get("t")

#Select real triple coinc
tree.Draw(">>eList","!beam&&((Sum$(chan==28)>0&&Sum$(chan==20)>0&&Sum$(chan==18)>0)||(Sum$(layer==1&&type==0)>0&&Sum$(layer==2&&type==0)>0)||(Sum$(layer==3&&type==0)>0&&Sum$(layer==1&&type==0)>0)||(Sum$(layer==3&&type==0)>0&&Sum$(layer==2&&type==0)>0))","entryList")#Sum$(layer==1&&type==0)>0&&Sum$(layer==2&&type==0)>0&&Sum$(layer==3&&type==0)>0","entryList");
# tree.Draw(">>eList","Sum$(chan==18)>0&&Sum$(chan==20)>0&&Sum$(chan==28)>0&&Sum$(chan==21)>0","entryList")#Sum$(layer==1&&type==0)>0&&Sum$(layer==2&&type==0)>0&&Sum$(layer==3&&type==0)>0","entryList");
# tree.Draw(">>eList","!beam&&MaxIf$(chan,layer==1&&type==0)==MinIf$(chan,layer==1&&type==0)&&MaxIf$(chan,layer==2&&type==0)==MinIf$(chan,layer==2&&type==0)&&MaxIf$(chan,layer==3&&type==0)==MinIf$(chan,layer==3&&type==0)&&Sum$(layer==1&&type==0)>0&&Sum$(layer==2&&type==0)>0&&Sum$(layer==3&&type==0)>0","entryList");
eList = r.gDirectory.Get("eList");
tree.SetEntryList(eList);
newFile = r.TFile("noBeamTwoLayerHitsOrThreeSlabHits.root","RECREATE");
newTree = tree.CloneTree(0)
for i in range(eList.GetN()):
    iEntry = eList.GetEntry(i)
    tree.GetEntry(iEntry)
    newTree.Fill()

newTree.AutoSave()
