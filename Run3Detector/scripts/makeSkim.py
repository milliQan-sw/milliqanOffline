import ROOT as r
import os
import sys
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)

def makeSkim(inputFile,outputFile,cutString,test=False):
    if inputFile == outputFile:
        print ("DON'T OVERWRITE THE INPUT!")
        exit()
    inputFile = r.TFile(inputFile)
    tree = inputFile.Get("t")
    if test:
        tree.Draw(">>eList",cutString,"entryList",1000);
    else:
        tree.Draw(">>eList",cutString,"entryList",);
    eList = r.gDirectory.Get("eList");
    tree.SetEntryList(eList);
    newFile = r.TFile(outputFile,"RECREATE");
    newTree = tree.CloneTree(0)
    for i in range(eList.GetN()):
        iEntry = eList.GetEntry(i)
        tree.GetEntry(iEntry)
        newTree.Fill()

    newTree.AutoSave()

if __name__ == "__main__":
    # defaultCutString = "Sum$(caloJetTotalEmEnergyEcalCellDT > 1 && caloJetTotalEmEnergyEcalCellCap > 10 && abs(caloJetEta)<1.48 && caloJetNEcalCellCap > 25 && caloJetTotalEmEnergyEcalCellWeird < 1 && caloJetTotalEmEnergyEcalCellDiWeird < 1) > 0"
    defaultCutString = "Max$(layer==0)&&Max$(layer==1)&&Max$(layer==2)&&Max$(layer==3)&&MaxIf$(area,chan==16)>7E3&&MaxIf$(area,chan==18)>4E3"
    # defaultCutString = "Sum$(caloJetNEcalCell>10&&caloJetTotalEmEnergyEcalCellCap>10&&caloJetWeightedTimeEcalCellMedianCap<-2)>0"
    if len(sys.argv) < 3:
        print ("usage python skimAllRelevantEvents.py <inputFile> <outputFile> <optional: cut string>")
        exit()
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    if len(sys.argv) == 4:
        cutString = sys.argv[3]
    else:
        cutString = defaultCutString
    makeSkim(inputFile,outputFile,cutString)

