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

def getTimeDiff(self):
    
    nPE_backSlab = []

    nPEL0 = self.events['nPE'][self.events['layer'] == 0]
    nPEL1 = self.events['nPE'][self.events['layer'] == 1]
    nPEL2 = self.events['nPE'][self.events['layer'] == 2]
    nPEL3 = self.events['nPE'][self.events['layer'] == 3]

    nPEL4 = self.events['nPE'][self.events['layer'] == 4]

    def minTime(pulse_times):
        filtered_times = [time for time in pulse_times if time is not None]
        return min(filtered_times) if filtered_times else None

    nPEL0_min = [minTime(event) for event in ak.to_list(nPEL0)]
    nPEL1_min = [minTime(event) for event in ak.to_list(nPEL1)]
    nPEL2_min = [minTime(event) for event in ak.to_list(nPEL2)]
    nPEL3_min = [minTime(event) for event in ak.to_list(nPEL3)]

    for i in range(len(self.events)):
        if nPEL0_min[i] is not None and nPEL1_min[i] is not None and nPEL2_min[i] is not None and nPEL3_min[i] is not None:
            nPE_backSlab.append(nPEL4[i])

    num_events = len(self.events)
    num_nones = num_events - len(nPE_backSlab)
    nPE_backSlab.extend([None] * num_nones)

    self.events['timeDiff'] = nPE_backSlab

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_particleName', 'layer', 'nPE', 'time', 'chan']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "nPE in back slab", 5000, 0, 5000)
h_1d.GetXaxis().SetTitle("nPE")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# defining the cutflow
cutflow = [mycuts.getTimeDiff, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("nPE_backSlab.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()