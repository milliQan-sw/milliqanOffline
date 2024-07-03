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

# define the function to get the number of events with muons in all 4 layers
def getMuonNum(self):

    print(len(self.events['hit_particleName']))
    print(len(self.events['hit_layer']))

    countMuon = []

    hit_muons = self.events['hit_particleName'][ak.any(abs(self.events['hit_particleName']) == 13, axis = 1)]

    hit_muons_L0 = hit_muons[self.events['hit_layer'] == 0]
    hit_muons_L1 = hit_muons[self.events['hit_layer'] == 1]
    hit_muons_L2 = hit_muons[self.events['hit_layer'] == 2]
    hit_muons_L3 = hit_muons[self.events['hit_layer'] == 3]

    for i in range(len(hit_muons_L0)):
        if ak.any(hit_muons_L0[i]) is not None and ak.any(hit_muons_L1[i]) is not None and ak.any(hit_muons_L2[i]) is not None and ak.any(hit_muons_L3[i]) is not None:
            countMuon.append(0)

    print(len(countMuon))

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getMuonNum', getMuonNum)

filelist = ['/home/bpeng/muonAnalysis/dy_nophoton_flat.root']

# define the necessary branches to run over
branches = ['hit_hitTime_ns', 'hit_nPE', 'hit_layer', 'hit_particleName', 'layer', 'nPE', 'time', 'chan']

# define the milliqan cuts object
mycuts = milliqanCuts()

# define milliqan plotter
myplotter = milliqanPlotter()

# defining the cutflow
cutflow = [mycuts.getMuonNum]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()