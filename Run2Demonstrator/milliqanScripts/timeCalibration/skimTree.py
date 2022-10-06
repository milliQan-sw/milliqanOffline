#!/usr/local/bin/python

import ROOT as r
import pickle
import os,sys
import pandas as pd
r.gROOT.SetBatch(True)

inputFile = r.TFile('AllTripleCoincidenceNominalHVNov7_v2.root')
oldtree = inputFile.Get('t')

newFile = r.TFile('skimmed.root','recreate')
jaeData = pd.read_csv('dataJae.txt',sep=' ')

newtree = oldtree.CloneTree(0);

for entry in oldtree:
    if len(jaeData.loc[(jaeData["run"]==entry.run) & (jaeData["file"] == entry.file) & (jaeData["event"] == entry.event)]) != 0:
        newtree.Fill()
    # if (entry.run in jaeData["run"]):
    #     if (entry.file in jaeData[jaeData["run"] == entry.run]"file"]):
    #         if (entry.event in jaeData["event"]):
    #             newtree.Fill()
newtree.AutoSave()
