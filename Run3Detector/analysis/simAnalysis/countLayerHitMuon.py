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

# define the function to get the number of events with muons in layers
def getMuonNum(self):

    countMuon = 0
    
    # extract muons for each layer
    muonL0Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 0), axis = 1)
    muonL1Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 1), axis = 1)
    muonL2Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 2), axis = 1)
    muonL3Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 3), axis = 1)
    muonL4Mask = ak.any((abs(self.events['hit_particleName']) == 13) & (self.events['hit_layer'] == 4), axis = 1)

    # check each event
    for i in range(len(self.events)):
        if muonL0Mask[i] and muonL1Mask[i] and muonL2Mask[i] and muonL3Mask[i] and muonL4Mask[i]:
            countMuon += 1
    
    print(countMuon)

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