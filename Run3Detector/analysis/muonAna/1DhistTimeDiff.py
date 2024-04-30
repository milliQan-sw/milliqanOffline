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


    height000MAX = height000.max() if not height000.empty else 0
    height010MAX = height010.max() if not height010.empty else 0
    height020MAX = height020.max() if not height020.empty else 0
    height030MAX = height030.max() if not height030.empty else 0
    height001MAX = height001.max() if not height001.empty else 0
    height011MAX = height011.max() if not height011.empty else 0
    height021MAX = height021.max() if not height021.empty else 0
    height031MAX = height031.max() if not height031.empty else 0
    height100MAX = height100.max() if not height100.empty else 0
    height110MAX = height110.max() if not height110.empty else 0
    height120MAX = height120.max() if not height120.empty else 0
    height130MAX = height130.max() if not height130.empty else 0
    height101MAX = height101.max() if not height101.empty else 0
    height111MAX = height111.max() if not height111.empty else 0
    height121MAX = height121.max() if not height121.empty else 0
    height131MAX = height131.max() if not height131.empty else 0
    height200MAX = height200.max() if not height200.empty else 0
    height210MAX = height210.max() if not height210.empty else 0
    height220MAX = height220.max() if not height220.empty else 0
    height230MAX = height230.max() if not height230.empty else 0
    height201MAX = height201.max() if not height201.empty else 0
    height211MAX = height211.max() if not height211.empty else 0
    height221MAX = height221.max() if not height221.empty else 0
    height231MAX = height231.max() if not height231.empty else 0
    height300MAX = height300.max() if not height300.empty else 0
    height310MAX = height310.max() if not height310.empty else 0
    height320MAX = height320.max() if not height320.empty else 0
    height330MAX = height330.max() if not height330.empty else 0
    height301MAX = height301.max() if not height301.empty else 0
    height311MAX = height311.max() if not height311.empty else 0
    height321MAX = height321.max() if not height321.empty else 0
    height331MAX = height331.max() if not height331.empty else 0

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