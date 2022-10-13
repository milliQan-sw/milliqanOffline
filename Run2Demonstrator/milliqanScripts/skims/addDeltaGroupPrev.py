import ROOT as r
import pickle
import os
import array
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)

inputFile = r.TFile("allTriple.root")
tree = inputFile.Get("t")

#Select real triple coinc
leaves = "groupTDCZeroPrev/L"
leafValues = array.array("l",[0])
newFile = r.TFile("allTripleWithTimePrev.root","RECREATE");
newTree = tree.CloneTree(0)
prevGroupTDCZeroBranch = newTree.Branch("groupTDCZeroPrev",leafValues,leaves)
tree.GetEntry(0)
leafValues[0] = tree.groupTDC[0]*1
newTree.Fill()
# for iEntry in range(1,1000):#tree.GetEntries()):
for iEntry in range(1,tree.GetEntries()):
    leafValues[0] = tree.groupTDC[0]*1
    tree.GetEntry(iEntry)
    newTree.Fill()
    if iEntry % int(1E6) == 0:
        print "%s of %s: %s %s" % (iEntry,tree.GetEntries(),leafValues,tree.groupTDC[0])

newTree.AutoSave()
