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

# define the function to get the areas of each pulse that has passed the cuts
def getArea(self):

    max_heightsL0 = {}
    max_areaL0 = {}

    max_heightsL1 = {}
    max_areaL1 = {}

    max_heightsL2 = {}
    max_areaL2 = {}

    max_heightsL3 = {}
    max_areaL3 = {}

    areas = []

    # remove events with panel pulses whose heights are more than 800
    panel_pulse_mask = (self.events['height'] > 800) & (self.events['type'] == 2)
    events_without_panel_pulses = ~ak.any(panel_pulse_mask, axis = 1)

    # ensure that events have slab pulses whose heights are more than 800
    slab_pulse_mask = (self.events['height'] > 800) & (self.events['type'] == 1)
    events_with_slab_pulses = ak.any(slab_pulse_mask, axis = 1)

    # combine masks to get valid events
    valid_events_mask = events_without_panel_pulses | events_with_slab_pulses

# iterate over straight line passes
    for row in range(4):
        for column in range(4):
            # pulse_based 2D boolean masks determined by channel and height
            pulse_maskL0 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 0) & (self.events['height'] > 1000)
            pulse_maskL1 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 1) & (self.events['height'] > 1000)
            pulse_maskL2 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 2) & (self.events['height'] > 1000)
            pulse_maskL3 = (self.events['row'] == row) & (self.events['column'] == column) & (self.events['layer'] == 3) & (self.events['height'] > 1000)

            # event_based 1D boolean mask determined by event
            event_mask = ak.any(pulse_maskL0, axis = 1) & ak.any(pulse_maskL1, axis = 1) & ak.any(pulse_maskL2, axis = 1) & ak.any(pulse_maskL3, axis = 1)

            # pick out pulses of type 0
            type_mask = self.events['type'] == 0

            # combine all the masks
            mask0 = event_mask & pulse_maskL0 & valid_events_mask
            mask1 = event_mask & pulse_maskL1 & valid_events_mask
            mask2 = event_mask & pulse_maskL2 & valid_events_mask
            mask3 = event_mask & pulse_maskL3 & valid_events_mask

            heightsL0 = self.events['height'][mask0]
            areaL0 = self.events['area'][mask0]

            heightsL1 = self.events['height'][mask1]
            areaL1 = self.events['area'][mask1]

            heightsL2 = self.events['height'][mask2]
            areaL2 = self.events['area'][mask2]

            heightsL3 = self.events['height'][mask3]
            areaL3 = self.events['area'][mask3]

            # store heights and times into dictionaries
            key = (row, column)

            # 1D max heights of each event
            max_heightsL0[key] = ak.max(heightsL0, axis = -1)  # 1D max heights of each event

            # broadcast to get a 2D list with every pulse being max height
            # then get a 2D boolean list to pick out which pulse has the max height so we can extract its time later
            max_maskL0 = (heightsL0 == ak.broadcast_arrays(max_heightsL0[key], heightsL0)[0])

            # get a 2D list of the times for the pulses with max heights
            raw_max_areasL0 = ak.mask(areaL0, max_maskL0)
            max_areaL0[key] = ak.Array([  # 1D max areas of each event
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_areasL0)
            ])

            # pull down the time of each sublist to get a 1D list of times
            max_heightsL1[key] = ak.max(heightsL1, axis = -1)
            max_maskL1 = (heightsL1 == ak.broadcast_arrays(max_heightsL1[key], heightsL1)[0])
            raw_max_areasL1 = ak.mask(areaL1, max_maskL1)
            max_areaL1[key] = ak.Array([
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_areasL1)
            ])

            # do the same for other 3 layers
            max_heightsL2[key] = ak.max(heightsL2, axis = -1)
            max_maskL2 = (heightsL2 == ak.broadcast_arrays(max_heightsL2[key], heightsL2)[0])
            raw_max_areasL2 = ak.mask(areaL2, max_maskL2)
            max_areaL2[key] = ak.Array([
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_areasL2)
            ])

            max_heightsL3[key] = ak.max(heightsL3, axis = -1)
            max_maskL3 = (heightsL3 == ak.broadcast_arrays(max_heightsL3[key], heightsL3)[0])
            raw_max_areasL3 = ak.mask(areaL3, max_maskL3)
            max_areaL3[key] = ak.Array([
                next((item for item in sublist if item is not None), None) 
                if sublist is not None else None
                for sublist in ak.to_list(raw_max_areasL3)
            ])

            # iterate over events
            for event in range(len(max_areaL0[key])):
                if max_areaL0[key][event] is not None and max_areaL1[key][event] is not None and max_areaL2[key][event] is not None and max_areaL3[key][event] is not None:
                    areas.append(max_areaL0[key][event])
                    areas.append(max_areaL1[key][event])
                    areas.append(max_areaL2[key][event])
                    areas.append(max_areaL3[key][event])

    print(areas)

    # extend the final list to match the size of the current file
    num_events = len(self.events['height'])
    num_nones = num_events - len(areas)
    areas.extend([None] * num_nones)

    # define custom branch
    self.events['areas'] = areas

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
h_1d = r.TH1F("h_1d", "Areas on All 4 Layers", 800000, 0, 800000)
h_1d.GetXaxis().SetTitle("Areas")

# add root histogram to plotter
myplotter.addHistograms(h_1d, 'areas')

# defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.getArea, myplotter.dict['h_1d']]

# create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

# print out the schedule
myschedule.printSchedule()

# create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

# run the milliqan processor
myiterator.run()

# create a new TFile
f = r.TFile("1DhistArea4L.root", "recreate")

# write the histograms to the file
h_1d.Write()

# close the file
f.Close()