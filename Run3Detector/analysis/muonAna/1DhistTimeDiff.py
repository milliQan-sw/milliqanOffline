#importing packages
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

#define function to get the time difference between pulses in layer0 and layer1
def getPulseDiff(self):
    # Initialize an empty (or placeholder) array for time differences
    # Using a masked array or setting up a NaN array for floats can work
    t_out = ak.full_like(self.events['timeFit_module_calibrated'], np.nan, highlevel=False)
    
    # Apply cuts to timeFit_module_calibrated
    times = self.events['timeFit_module_calibrated'][self.events['straightLineCut']]
    
    # Apply cuts to layer and type for further cut to timeFit_module_calibrated
    layer = self.events['layer'][self.events['straightLineCut']]
    type = self.events['type'][self.events['straightLineCut']]
    
    # Filter to get times at each specific layer
    times0 = times[(layer == 0) & (type == 0)]
    times1 = times[(layer == 1) & (type == 0)]
    
    # Calculate the time difference between the two layers for events that pass the cuts
    t_out_valid = times1 - times0
    
    # We only assign these valid differences to the indices where the straightLineCut is True
    # Find the indices where straightLineCut is True
    indices = ak.nonzero(self.events['straightLineCut'])[0]
    
    # Assign the computed time differences to these indices in the placeholder array
    ak.num(t_out)[indices] = t_out_valid
    
    # Assign the computed array back to the event structure
    self.events['timeDiff'] = t_out


#add our custom function to milliqanCuts
setattr(milliqanCuts, 'getPulseDiff', getPulseDiff)

#define a file list to run over
filelist = ['/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/MilliQan_Run1006.4_v34.root:t']

#define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

#define the milliqan cuts object
mycuts = milliqanCuts()

#require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

#require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

#add four layer cut
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

#define milliqan plotter
myplotter = milliqanPlotter()

#create a 1D root histogram
h_1d = r.TH1F("h_1d", "1D Histogram", 80, -40, 40)
h_1d.GetXaxis().SetTitle("timeDiff between layer 0 and 1")

#add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

#defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.straightLineCut, mycuts.getPulseDiff, myplotter.dict['h_1d']]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

#run the milliqan processor
myiterator.run()

#create a new TFile
f = r.TFile("1DhistTimeDiff.root", "recreate")

#write the histograms to the file
h_1d.Write()

#close the file
f.Close()