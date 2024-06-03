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

# define the function to get the areas of layer -1 and layer 0
def getArea(self):
    num_events = len(self.events)

    AreaLn1 = self.events['area'][self.events['layer'] == -1]
    num_nonesLn1 = num_events - len(AreaLn1)
    AreaLn1.extend([None] * num_nonesLn1)
    self.events['AreaLn1'] = AreaLn1

    AreaL0 = self.events['area'][self.events['layer'] == 0]
    num_nonesL0 = num_events - len(AreaL0)
    AreaL0.extend([None] * num_nonesL0)
    self.events['AreaL0'] = AreaL0
    
# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getArea', getArea)

# check if command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 [file_name] [start_file_index] [end_file_index]")
    sys.exit(1)

# assign start and end indices from command line
start_index = int(sys.argv[1])
end_index = int(sys.argv[2])

# define a file list to run over
filelist = [
    f"/home/bpeng/muonAnalysis/MilliQan_Run1118.{i}_v34.root"
    for i in range(start_index, end_index + 1)
    if os.path.exists(f"/home/bpeng/muonAnalysis/MilliQan_Run1118.{i}_v34.root")
]

# define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

# define the milliqan cuts object
mycuts = milliqanCuts()

# require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

# require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

# add four layer cut
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

# define milliqan plotter
myplotter = milliqanPlotter()

# create a 2D root histogram
h_2d = r.TH2F("h_2d", "Areas of Layer 0 VS Layer -1", 140, 0, 500000, 140, 0, 500000)
h_2d.GetXaxis().SetTitle("AreaL-1")
h_2d.GetYaxis().SetTitle("AreaL0")

# add root histogram to plotter
myplotter.addHistograms(h_2d, ['AreaLn1', 'AreaL0'], cut=None)

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getArea, myplotter.dict['h_2d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("2dHistAreaL0Ln1.root", "recreate")

# write the histograms to the file
h_2d.Write()

# close the file
f.Close()