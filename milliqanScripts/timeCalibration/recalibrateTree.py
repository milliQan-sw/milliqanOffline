#!/usr/local/bin/python

import ROOT as r
import pickle
import os,sys
import pandas as pd
r.gROOT.SetBatch(True)

inputFile = r.TFile('AllTripleCoincidenceNominalHVNov7_v2.root')
oldtree = inputFile.Get('t')

newFile = r.TFile('recalibTree.root','recreate')
jaeData = pd.read_csv('dataJae.txt',sep=' ')

newtree = oldtree.CloneTree(0);

intraCalib = [0.0, 0.0, -2.5, -7.5, 0.625, 0.0, 1.875, 10.0, 1.25, 0.0, -3.75, -3.75, -1.875, 0.0, -24.375, -5.0]
interCalib = [0.0, 0.0, 0.0, 0.0, -6.25, -6.25, -6.25, -6.25, 8.125, 8.125, 8.125, 8.125, -6.25, 0.0, 8.125, 0.0]
for entry in oldtree:
    for iT in range(len(entry.time)):
        entry.time_module_calibrated[iT] = entry.time[iT] + intraCalib[entry.chan[iT]] + interCalib[entry.chan[iT]]
    newtree.Fill()
    # if (entry.run in jaeData["run"]):
    #     if (entry.file in jaeData[jaeData["run"] == entry.run]"file"]):
    #         if (entry.event in jaeData["event"]):
    #             newtree.Fill()
newtree.AutoSave()
