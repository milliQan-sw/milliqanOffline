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

# define the function to get the area and height in slabs
def getAreaHeight(self):
    slab_area = self.events['area'][self.events['type'] == 1]
    slab_height = self.events['height'][self.events['type'] == 1]
    self.events['SLABAREA'] = slab_area
    self.events['SLABHEIGHT'] = slab_height

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getAreaHeight', getAreaHeight)

'''
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
'''
filelist = ['/home/bpeng/muonAnalysis/MilliQan_Run1000_v34_skim_correction.root']

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

# create a 1D root histogram
h_2d = r.TH2F("h_2d", "Height VS Area in Slabs", 500, 0, 500000, 100, 0, 5000)
h_2d.GetXaxis().SetTitle("Area")
h_2d.GetYaxis().SetTitle("Height")

# add root histogram to plotter
myplotter.addHistograms(h_2d, ['SLABAREA', 'SLABHEIGHT'], cut=None)

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getAreaHeight, myplotter.dict['h_2d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("2dHistSlabHeightArea.root", "recreate")

# write the histograms to the file
h_2d.Write()

# close the file
f.Close()