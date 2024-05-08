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

    time_diffs = []

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

            heightsL0 = self.events['height'][mask0 & height_mask]  # 2D heights in one channel on layer 0
            timeL0 = self.events['timeFit_module_calibrated'][mask0 & height_mask]  # 2D times in one channel on layer 0

            heightsL1 = self.events['height'][mask1 & height_mask]
            timeL1 = self.events['timeFit_module_calibrated'][mask1 & height_mask]

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

            if ak.max(max_timeL1[key]) is not None and ak.max(max_timeL0[key]) is not None:
                time_diffs.append(ak.max(max_timeL1[key]) - ak.max(max_timeL0[key]))


    for key in max_heightsL0:
        print(key, "layer 0 Max Height: ", ak.max(max_heightsL0[key]))

    print()

    for key in max_heightsL1:
        print(key, "layer 1 Max Height: ", ak.max(max_heightsL1[key]))

    print()

    print(time_diffs)

    num_nones = 1000 - len(time_diffs)
    time_diffs.extend([None] * num_nones)

    self.events['timeDiff'] = time_diffs

# add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

# define a file list to run over
filelist = [
    '/mnt/hadoop/se/store/user/milliqan/run3/bar/1100/0007/MilliQan_Run1178.422_default.root:Events'
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
h_1d = r.TH1F("h_1d", "timeFit_module_calibrated Differences between layer 0 and 1", 40, -20, 20)
h_1d.GetXaxis().SetTitle("time difference between layer 0 and 1")

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


'''
    # iterate over each channel (using row/column/layer to locate each channel)
    for row in range(4):
        for column in range(4):
            for layer in range(2):
                # generate key for dictionaries
                key = (row, column, layer)

                # define the location mask for the current channel
                locationMask = (rows == row) & (columns == column) & (layers == layer)

                # get heights and times at current channel (they should have the exact same dimension)
                channel_heights = heights[locationMask]
                channel_times = times[locationMask]

                # find the max height of each event (sublist) and its corresponding time
                if ak.any(ak.num(channel_heights) > 0):  # check if any sublist in channel_heights is not empty in case it's an empty array
                    # store the list of max heights in each event (sublist) into the dictionary
                    max_heights[key] = ak.max(channel_heights, axis=-1) # now channel_heights is flattened

                    # boolean mask to know which pulse (element) in each event (sublist) achieves its max height
                    max_mask = (channel_heights == ak.broadcast_arrays(max_heights[key], channel_heights)[0])

                    # use the mask to pick out the corresponding times to the max pulse heights (element) in each event (sublist)
                    raw_cor_times = ak.mask(channel_times, max_mask)# an unflattened raw 2D array with only desired times

                    # for each event, extract the corresponding time or return None if there's no pulse in that event
                    cor_times[key] = ak.Array([
                        next((item for item in sublist if item is not None), None) 
                        if sublist is not None else None
                        for sublist in ak.to_list(raw_cor_times)
                    ])
                    # print out channel number and corresponding desired times of events in that channel
                    print(key, cor_times[key])

    # create an empty list to store time differences initialized with all Nones
    time_diffs = []
    # calculate time differences between layer 1 and layer 0 in each channel for each event
    for row in range(4):
        for column in range(4):
            # define keys to locate time
            key0 = (row, column, 0)
            key1 = (row, column, 1)

            if key0 in cor_times and key1 in cor_times:
                for i in range(len(times)): # iterate over each event that has passed straightLineCut in current channel
                    if cor_times[key0][i] is not None and cor_times[key1][i] is not None:
                        time_diff = cor_times[key1][i] - cor_times[key0][i]
                        time_diffs.append(time_diff)
    
    print(time_diffs)
    print("Effective time differences total number: ", len(time_diffs))

    # extend time_diffs to a 1000 sized list with Nones
    num_nones = 1000 - len(time_diffs)
    time_diffs.extend([None] * num_nones)

    # store the time differences in the 'timeDiff' branch
    self.events['timeDiff'] = time_diffs
'''