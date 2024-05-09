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

# define the function to get the time differences for the max height of events in each channel between layer 0 and layer 1
def getTimeDiff(self):

    max_heightsL0 = {}
    max_timeL0 = {}

    max_heightsL1 = {}
    max_timeL1 = {}

    max_heightsL2 = {}
    max_timeL2 = {}

    max_heightsL3 = {}
    max_timeL3 = {}
    
    time_diffsL10 = []

    for row in range(4):
        for column in range(4):
            # 2D True/False masks determined by channels (at current channel?)
            pulse_maskL0 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 0)
            pulse_maskL1 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 1)
            pulse_maskL2 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 2)
            pulse_maskL3 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 3)

            # 1D True/False mask determined by event (any straight line pass?)
            event_mask = ak.any(pulse_maskL0, axis=1) & ak.any(pulse_maskL1, axis=1) & ak.any(pulse_maskL2, axis=1) & ak.any(pulse_maskL3, axis=1)
            
            height_mask = self.events['height'] > 1000

            # select events on straight line passes then select layers
            mask0 = event_mask & pulse_maskL0
            mask1 = event_mask & pulse_maskL1
            mask2 = event_mask & pulse_maskL2
            mask3 = event_mask & pulse_maskL3

            heightsL0 = self.events['height'][mask0 & height_mask]  # 2D heights in one channel on layer 0
            timeL0 = self.events['timeFit_module_calibrated'][mask0 & height_mask]  # 2D times in one channel on layer 0

            heightsL1 = self.events['height'][mask1 & height_mask]
            timeL1 = self.events['timeFit_module_calibrated'][mask1 & height_mask]

            heightsL2 = self.events['height'][mask2 & height_mask]
            timeL2 = self.events['timeFit_module_calibrated'][mask2 & height_mask]

            heightsL3 = self.events['height'][mask3 & height_mask]
            timeL3 = self.events['timeFit_module_calibrated'][mask3 & height_mask]

            key = (row, column)
            
            max_heightsL0[key] = ak.max(heightsL0, axis = -1)  # 1D max heights of each event in one channel
            max_maskL0 = (heightsL0 == ak.broadcast_arrays(max_heightsL0[key], heightsL0)[0])
            raw_max_timesL0 = ak.mask(timeL0, max_maskL0)
            max_timeL0[key] = ak.Array([  # 1D max times of each event in one channel
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_timesL0)
            ])

            max_heightsL1[key] = ak.max(heightsL1, axis = -1)
            max_maskL1 = (heightsL1 == ak.broadcast_arrays(max_heightsL1[key], heightsL1)[0])
            raw_max_timesL1 = ak.mask(timeL1, max_maskL1)
            max_timeL1[key] = ak.Array([
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_timesL1)
            ])

            max_heightsL2[key] = ak.max(heightsL2, axis = -1)
            max_maskL2 = (heightsL2 == ak.broadcast_arrays(max_heightsL2[key], heightsL2)[0])
            raw_max_timesL2 = ak.mask(timeL2, max_maskL2)
            max_timeL2[key] = ak.Array([
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_timesL2)
            ])

            max_heightsL3[key] = ak.max(heightsL3, axis = -1)
            max_maskL3 = (heightsL3 == ak.broadcast_arrays(max_heightsL3[key], heightsL3)[0])
            raw_max_timesL3 = ak.mask(timeL3, max_maskL3)
            max_timeL3[key] = ak.Array([
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_timesL3)
            ])

            if ak.max(max_timeL0[key]) is not None and ak.max(max_timeL1[key]) is not None and ak.max(max_timeL2[key]) is not None and ak.max(max_timeL3[key]) is not None:
                time_diffsL10.append(ak.max(max_timeL1[key]) - ak.max(max_timeL0[key]))


    for key in max_heightsL0:
        print(key, "layer 0 Max Height: ", ak.max(max_heightsL0[key]))

    print()

    for key in max_heightsL1:
        print(key, "layer 1 Max Height: ", ak.max(max_heightsL1[key]))

    print()

    print(time_diffsL10)

    num_nones = 1000 - len(time_diffsL10)
    time_diffsL10.extend([None] * num_nones)

    self.events['timeDiff'] = time_diffsL10

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

# define a file list to run over
filelist = [
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.520_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.521_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.522_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.523_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.524_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.525_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.526_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.527_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.528_v34.root',
    '/mnt/hadoop/se/store/user/milliqan/trees/v34/1100/MilliQan_Run1118.529_v34.root'
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

# create a 1D root histogram
h_1d = r.TH1F("h_1d", "timeFit_module_calibrated Differences between layer 0 and 1", 60, -30, 30)
h_1d.GetXaxis().SetTitle("time difference (TimeLayer1 - TimeLayer0)")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.straightLineCut, mycuts.getTimeDiff, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("1DhistTimeDiff.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()