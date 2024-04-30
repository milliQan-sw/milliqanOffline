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

#define function to extract the max value of a nested array
def max_of_nested_subarrays(nested_array):
    nested_list = ak.to_list(nested_array)
    non_empty_values = [item for sublist in nested_list for item in sublist if len(sublist) > 0]
    return max(non_empty_values, default=0)

#define function to get the 16 time difference between pulses in layer0 and layer1
def getTimeDiff(self):

    rows = self.events['row'][self.events['straightLineCut']]
    columns = self.events['column'][self.events['straightLineCut']]
    layers = self.events['layer'][self.events['straightLineCut']]

    heights = self.events['height'][self.events['straightLineCut']]
    times = self.events['timeFit_module_calibrated'][self.events['straightLineCut']]
    
    height000 = heights[(rows == 0) & (columns == 0) & (layers == 0)]
    height010 = heights[(rows == 0) & (columns == 1) & (layers == 0)]
    height020 = heights[(rows == 0) & (columns == 2) & (layers == 0)]
    height030 = heights[(rows == 0) & (columns == 3) & (layers == 0)]
    height001 = heights[(rows == 0) & (columns == 0) & (layers == 1)]
    height011 = heights[(rows == 0) & (columns == 1) & (layers == 1)]
    height021 = heights[(rows == 0) & (columns == 2) & (layers == 1)]
    height031 = heights[(rows == 0) & (columns == 3) & (layers == 1)]
    height100 = heights[(rows == 1) & (columns == 0) & (layers == 0)]
    height110 = heights[(rows == 1) & (columns == 1) & (layers == 0)]
    height120 = heights[(rows == 1) & (columns == 2) & (layers == 0)]
    height130 = heights[(rows == 1) & (columns == 3) & (layers == 0)]
    height101 = heights[(rows == 1) & (columns == 0) & (layers == 1)]
    height111 = heights[(rows == 1) & (columns == 1) & (layers == 1)]
    height121 = heights[(rows == 1) & (columns == 2) & (layers == 1)]
    height131 = heights[(rows == 1) & (columns == 3) & (layers == 1)]
    height200 = heights[(rows == 2) & (columns == 0) & (layers == 0)]
    height210 = heights[(rows == 2) & (columns == 1) & (layers == 0)]
    height220 = heights[(rows == 2) & (columns == 2) & (layers == 0)]
    height230 = heights[(rows == 2) & (columns == 3) & (layers == 0)]
    height201 = heights[(rows == 2) & (columns == 0) & (layers == 1)]
    height211 = heights[(rows == 2) & (columns == 1) & (layers == 1)]
    height221 = heights[(rows == 2) & (columns == 2) & (layers == 1)]
    height231 = heights[(rows == 2) & (columns == 3) & (layers == 1)]
    height300 = heights[(rows == 3) & (columns == 0) & (layers == 0)]
    height310 = heights[(rows == 3) & (columns == 1) & (layers == 0)]
    height320 = heights[(rows == 3) & (columns == 2) & (layers == 0)]
    height330 = heights[(rows == 3) & (columns == 3) & (layers == 0)]
    height301 = heights[(rows == 3) & (columns == 0) & (layers == 1)]
    height311 = heights[(rows == 3) & (columns == 1) & (layers == 1)]
    height321 = heights[(rows == 3) & (columns == 2) & (layers == 1)]
    height331 = heights[(rows == 3) & (columns == 3) & (layers == 1)]

    height000MAX = max_of_nested_subarrays(height000)
    height010MAX = max_of_nested_subarrays(height010)
    height020MAX = max_of_nested_subarrays(height020)
    height030MAX = max_of_nested_subarrays(height030)
    height001MAX = max_of_nested_subarrays(height001)
    height011MAX = max_of_nested_subarrays(height011)
    height021MAX = max_of_nested_subarrays(height021)
    height031MAX = max_of_nested_subarrays(height031)
    height100MAX = max_of_nested_subarrays(height100)
    height110MAX = max_of_nested_subarrays(height110)
    height120MAX = max_of_nested_subarrays(height120)
    height130MAX = max_of_nested_subarrays(height130)
    height101MAX = max_of_nested_subarrays(height101)
    height111MAX = max_of_nested_subarrays(height111)
    height121MAX = max_of_nested_subarrays(height121)
    height131MAX = max_of_nested_subarrays(height131)
    height200MAX = max_of_nested_subarrays(height200)
    height210MAX = max_of_nested_subarrays(height210)
    height220MAX = max_of_nested_subarrays(height220)
    height230MAX = max_of_nested_subarrays(height230)
    height201MAX = max_of_nested_subarrays(height201)
    height211MAX = max_of_nested_subarrays(height211)
    height221MAX = max_of_nested_subarrays(height221)
    height231MAX = max_of_nested_subarrays(height231)
    height300MAX = max_of_nested_subarrays(height300)
    height310MAX = max_of_nested_subarrays(height310)
    height320MAX = max_of_nested_subarrays(height320)
    height330MAX = max_of_nested_subarrays(height330)
    height301MAX = max_of_nested_subarrays(height301)
    height311MAX = max_of_nested_subarrays(height311)
    height321MAX = max_of_nested_subarrays(height321)
    height331MAX = max_of_nested_subarrays(height331)

    time000 = ak.min(times[(heights == height000MAX) & (rows == 0) & (columns == 0) & (layers == 0)])
    time010 = ak.min(times[(heights == height010MAX) & (rows == 0) & (columns == 1) & (layers == 0)])
    time020 = ak.min(times[(heights == height020MAX) & (rows == 0) & (columns == 2) & (layers == 0)])
    time030 = ak.min(times[(heights == height030MAX) & (rows == 0) & (columns == 3) & (layers == 0)])
    time001 = ak.min(times[(heights == height001MAX) & (rows == 0) & (columns == 0) & (layers == 1)])
    time011 = ak.min(times[(heights == height011MAX) & (rows == 0) & (columns == 1) & (layers == 1)])
    time021 = ak.min(times[(heights == height021MAX) & (rows == 0) & (columns == 2) & (layers == 1)])
    time031 = ak.min(times[(heights == height031MAX) & (rows == 0) & (columns == 3) & (layers == 1)])
    time100 = ak.min(times[(heights == height100MAX) & (rows == 1) & (columns == 0) & (layers == 0)])
    time110 = ak.min(times[(heights == height110MAX) & (rows == 1) & (columns == 1) & (layers == 0)])
    time120 = ak.min(times[(heights == height120MAX) & (rows == 1) & (columns == 2) & (layers == 0)])
    time130 = ak.min(times[(heights == height130MAX) & (rows == 1) & (columns == 3) & (layers == 0)])
    time101 = ak.min(times[(heights == height101MAX) & (rows == 1) & (columns == 0) & (layers == 1)])
    time111 = ak.min(times[(heights == height111MAX) & (rows == 1) & (columns == 1) & (layers == 1)])
    time121 = ak.min(times[(heights == height121MAX) & (rows == 1) & (columns == 2) & (layers == 1)])
    time131 = ak.min(times[(heights == height131MAX) & (rows == 1) & (columns == 3) & (layers == 1)])
    time200 = ak.min(times[(heights == height200MAX) & (rows == 2) & (columns == 0) & (layers == 0)])
    time210 = ak.min(times[(heights == height210MAX) & (rows == 2) & (columns == 1) & (layers == 0)])
    time220 = ak.min(times[(heights == height220MAX) & (rows == 2) & (columns == 2) & (layers == 0)])
    time230 = ak.min(times[(heights == height230MAX) & (rows == 2) & (columns == 3) & (layers == 0)])
    time201 = ak.min(times[(heights == height201MAX) & (rows == 2) & (columns == 0) & (layers == 1)])
    time211 = ak.min(times[(heights == height211MAX) & (rows == 2) & (columns == 1) & (layers == 1)])
    time221 = ak.min(times[(heights == height221MAX) & (rows == 2) & (columns == 2) & (layers == 1)])
    time231 = ak.min(times[(heights == height231MAX) & (rows == 2) & (columns == 3) & (layers == 1)])
    time300 = ak.min(times[(heights == height300MAX) & (rows == 3) & (columns == 0) & (layers == 0)])
    time310 = ak.min(times[(heights == height310MAX) & (rows == 3) & (columns == 1) & (layers == 0)])
    time320 = ak.min(times[(heights == height320MAX) & (rows == 3) & (columns == 2) & (layers == 0)])
    time330 = ak.min(times[(heights == height330MAX) & (rows == 3) & (columns == 3) & (layers == 0)])
    time301 = ak.min(times[(heights == height301MAX) & (rows == 3) & (columns == 0) & (layers == 1)])
    time311 = ak.min(times[(heights == height311MAX) & (rows == 3) & (columns == 1) & (layers == 1)])
    time321 = ak.min(times[(heights == height321MAX) & (rows == 3) & (columns == 2) & (layers == 1)])
    time331 = ak.min(times[(heights == height331MAX) & (rows == 3) & (columns == 3) & (layers == 1)])

    print(time000)
    print(time010)
    print(time020)
	print(time030)
	print(time001)
	print(time011)
	print(time021)
	print(time031)
	print(time100)
	print(time110)
	print(time120)
	print(time130)
	print(time101)
	print(time111)
	print(time121)
	print(time131)
	print(time200)
	print(time210)
	print(time220)
	print(time230)
	print(time201)
	print(time211)
	print(time221)
	print(time231)
	print(time300)
	print(time310)
	print(time320)
	print(time330)
	print(time301)
	print(time311)
	print(time321)
	print(time331)

    timeDiff00 = time001 - time000
    timeDiff01 = time011 - time010
    timeDiff02 = time021 - time020
    timeDiff03 = time031 - time030
    timeDiff10 = time101 - time100
    timeDiff11 = time111 - time110
    timeDiff12 = time121 - time120
    timeDiff13 = time131 - time130
    timeDiff20 = time201 - time200
    timeDiff21 = time211 - time210
    timeDiff22 = time221 - time220
    timeDiff23 = time231 - time230
    timeDiff30 = time301 - time300
    timeDiff31 = time311 - time310
    timeDiff32 = time321 - time320
    timeDiff33 = time331 - time330

    time_diffs = [timeDiff00, timeDiff01, timeDiff02, timeDiff03, timeDiff10, timeDiff11, timeDiff12, timeDiff13, 
              timeDiff20, timeDiff21, timeDiff22, timeDiff23, timeDiff30, timeDiff31, timeDiff32, timeDiff33]
    print(time_diffs)



#add our custom function to milliqanCuts
setattr(milliqanCuts, 'getTimeDiff', getTimeDiff)

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
h_1d = r.TH1F("h_1d", "Time Difference 1D Hist", 80, -40, 40)
h_1d.GetXaxis().SetTitle("time difference between layer 0 and 1")

#add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

#defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.straightLineCut, mycuts.getTimeDiff, myplotter.dict['h_1d']]

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