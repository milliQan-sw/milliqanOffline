#!/usr/local/bin/python

import ROOT as r
import pickle
import os,sys
import pandas as pd
r.gROOT.SetBatch(True)
r.gStyle.SetOptFit(0)

# inputFile = r.TFile('recalibTree.root')
inputFile = r.TFile('/Users/mcitron/milliqanScripts/realTripleCoinc.root')
# inputFile = r.TFile('AllTripleCoincidenceNominalHVNov7_v2.root')
tempCanvas = r.TCanvas()
tempCanvas.cd()
oldtree = inputFile.Get('t')
bins = '(40,{0},{1})'.format(-30,20)

oldtree.Draw("MinIf$(time_module_calibrated,(((chan==8||chan==9)&&nPE>=200)||((chan==11||chan==10)&&nPE>=75)))-MinIf$(time_module_calibrated,(layer==1&&nPE>=200))>>noBeam"+bins,"MinIf$(time_module_calibrated,((chan==8||chan==9)&&nPE>=200)||((chan==11||chan==10)&&nPE>=75))>0&&MinIf$(time_module_calibrated,layer==1&&nPE>=200)>0&&!beam","")
histNoBeam = tempCanvas.GetListOfPrimitives()[0]

oldtree.Draw("MinIf$(time_module_calibrated,((chan==8||chan==9)&&nPE>=200)||((chan==11||chan==10)&&nPE>=75))-MinIf$(time_module_calibrated,(layer==1&&nPE>=200))>>beam"+bins,"MinIf$(time_module_calibrated,((chan==8||chan==9)&&nPE>=200)||((chan==11||chan==10)&&nPE>=75))>0&&MinIf$(time_module_calibrated,layer==1&&nPE>=200)>0&&beam","")
histBeam = tempCanvas.GetListOfPrimitives()[0]
histBeamBackgroundSubtract = histBeam.Clone('backgroundSubtract')
histNoBeamToSubtract = histNoBeam.Clone()
histNoBeamToSubtract.Scale(1.97)
histBeamBackgroundSubtract.Add(histNoBeamToSubtract,-1)

gNoBeam = r.TF1('gNoBeam','gaus',-30,20)
gBeam = r.TF1('gBeam','gaus',5,15)

histNoBeam.Fit(gNoBeam,"R")
print gNoBeam.GetProb()
histNoBeam.Draw()
tempCanvas.SaveAs("noBeam.pdf")
tempCanvas.Clear()

histBeamBackgroundSubtract.Fit(gBeam,"R")
print gBeam.GetProb()
histBeamBackgroundSubtract.Draw()
tempCanvas.SaveAs("backgroundSubtract.pdf")
tempCanvas.Clear()

doubleG = r.TF1("doubleG","gaus(0)+gaus(3)",-30,20)
doubleG.SetParameter(0,gNoBeam.GetParameter(0))
doubleG.SetParameter(1,gNoBeam.GetParameter(1))
doubleG.SetParameter(2,gNoBeam.GetParameter(2))
doubleG.SetParameter(3,gBeam.GetParameter(0))
doubleG.SetParameter(4,gBeam.GetParameter(1))
doubleG.SetParameter(5,gBeam.GetParameter(2))
histBeam.Fit(doubleG,"R")
gNoBeam.SetParameter(0,doubleG.GetParameter(0))
gNoBeam.SetParameter(1,doubleG.GetParameter(1))
gNoBeam.SetParameter(2,doubleG.GetParameter(2))
print doubleG.GetProb()

tempCanvas.Clear()
histBeam.Draw()
gNoBeam.SetLineColor(r.kBlue)
gNoBeam.Draw("same")
tempCanvas.SaveAs("mess.pdf")


# newFile = r.TFile('skimmed.root','recreate')
# jaeData = pd.read_csv('dataJae.txt',sep=' ')

# newtree = oldtree.CloneTree(0);

# threetimes = []

# for entry in oldtree:
#     minTimeLayer1 = 9999
#     minTimeLayer2 = 9999
#     minTimeLayer3 = 9999
#     for iT in range(len(entry.time_module_calibrated)):
#         if entry.nPE[iT] >= 100:
#             if entry.layer[iT] == 1:
#                 if entry.time_module_calibrated[iT] < minTimeLayer1:
#                     minTimeLayer1 = entry.time_module_calibrated[iT]
#             elif entry.layer[iT] == 2:
#                 if entry.time_module_calibrated[iT] < minTimeLayer2:
#                     minTimeLayer2 = entry.time_module_calibrated[iT]
#             elif entry.layer[iT] == 3:
#                 if entry.time_module_calibrated[iT] < minTimeLayer3:
#                     minTimeLayer3 = entry.time_module_calibrated[iT]
#     if all(x != 9999 for x in [minTimeLayer1,minTimeLayer2,minTimeLayer3]):
#         threetimes.append([minTimeLayer1,minTimeLayer2,minTimeLayer3])
#     # if len(jaeData.loc[(jaeData["run"]==entry.run) & (jaeData["file"] == entry.file) & (jaeData["event"] == entry.event)]) != 0:
#     #     newtree.Fill()
#     # if (entry.run in jaeData["run"]):
#     #     if (entry.file in jaeData[jaeData["run"] == entry.run]"file"]):
#     #         if (entry.event in jaeData["event"]):
#     #             newtree.Fill()
# pickle.dump(threetimes,open("threetimes.pkl","w"))
