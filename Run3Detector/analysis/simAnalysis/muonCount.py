# importing packages
import os
import ROOT as r
import uproot
import hist
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import pandas as pd
import array as arr
import sys
sys.path.append('../utilities')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

# define the function to get the number of muons
def getMuonNum(self):

    countMuon = []

    hit_muons = self.events['hit_particleName'][ak.any(abs(self.events['hit_particleName']) == 13, axis = 1)]

    for i in range(len(hit_muons)):
        if hit_muons[i] is not None:
            countMuon.append(hit_muons[i])

    self.events['countMuon'] = countMuon

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getMuonNum', getMuonNum)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_particleName', 'layer', 'nPE', 'time', 'chan']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "Number of Muons", 20, 0, 20)
h_1d.GetXaxis().SetTitle("hit_particleName")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'countMuon')

# defining the cutflow
cutflow = [mycuts.getMuonNum, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("countMuon.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()