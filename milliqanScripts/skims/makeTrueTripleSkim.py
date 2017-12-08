import ROOT as r
import pickle
import os
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)

inputFile = r.TFile("realCoincAllTripleFull.root")
tree = inputFile.Get("t")

#Select real triple coinc
tree.Draw(">>eList","!beam&&MaxIf$(chan,layer==1)==MinIf$(chan,layer==1)&&MaxIf$(chan,layer==2)==MinIf$(chan,layer==2)&&MaxIf$(chan,layer==3)==MinIf$(chan,layer==3)&&Sum$(layer==1)>0&&Sum$(layer==2)>0&&Sum$(layer==3)>0","entryList");
eList = r.gDirectory.Get("eList");
tree.SetEntryList(eList);
newFile = r.TFile("realTripleCoincOneBarPerLayerNotBeam.root","RECREATE");
newTree = tree.CloneTree(0)
for i in range(eList.GetN()):
    iEntry = eList.GetEntry(i)
    tree.GetEntry(iEntry)
    newTree.Fill()

newTree.AutoSave()
