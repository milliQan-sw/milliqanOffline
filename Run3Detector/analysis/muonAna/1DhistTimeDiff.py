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

    print(height000)
    print(height010)
    print(height020)
    print(height030)
    print(height001)
    print(height011)
    print(height021)
    print(height031)
    print(height100)
    print(height110)
    print(height120)
    print(height130)
    print(height101)
    print(height111)
    print(height121)
    print(height131)
    print(height200)
    print(height210)
    print(height220)
    print(height230)
    print(height201)
    print(height211)
    print(height221)
    print(height231)
    print(height300)
    print(height310)
    print(height320)
    print(height330)
    print(height301)
    print(height311)
    print(height321)
    print(height331)
    print()

    height000MAX = ak.max(height000) if len(height000) > 0 else 0
    height010MAX = ak.max(height010) if len(height010) > 0 else 0
    height020MAX = ak.max(height020) if len(height020) > 0 else 0
    height030MAX = ak.max(height030) if len(height030) > 0 else 0
    height001MAX = ak.max(height001) if len(height001) > 0 else 0
    height011MAX = ak.max(height011) if len(height011) > 0 else 0
    height021MAX = ak.max(height021) if len(height021) > 0 else 0
    height031MAX = ak.max(height031) if len(height031) > 0 else 0
    height100MAX = ak.max(height100) if len(height100) > 0 else 0
    height110MAX = ak.max(height110) if len(height110) > 0 else 0
    height120MAX = ak.max(height120) if len(height120) > 0 else 0
    height130MAX = ak.max(height130) if len(height130) > 0 else 0
    height101MAX = ak.max(height101) if len(height101) > 0 else 0
    height111MAX = ak.max(height111) if len(height111) > 0 else 0
    height121MAX = ak.max(height121) if len(height121) > 0 else 0
    height131MAX = ak.max(height131) if len(height131) > 0 else 0
    height200MAX = ak.max(height200) if len(height200) > 0 else 0
    height210MAX = ak.max(height210) if len(height210) > 0 else 0
    height220MAX = ak.max(height220) if len(height220) > 0 else 0
    height230MAX = ak.max(height230) if len(height230) > 0 else 0
    height201MAX = ak.max(height201) if len(height201) > 0 else 0
    height211MAX = ak.max(height211) if len(height211) > 0 else 0
    height221MAX = ak.max(height221) if len(height221) > 0 else 0
    height231MAX = ak.max(height231) if len(height231) > 0 else 0
    height300MAX = ak.max(height300) if len(height300) > 0 else 0
    height310MAX = ak.max(height310) if len(height310) > 0 else 0
    height320MAX = ak.max(height320) if len(height320) > 0 else 0
    height330MAX = ak.max(height330) if len(height330) > 0 else 0
    height301MAX = ak.max(height301) if len(height301) > 0 else 0
    height311MAX = ak.max(height311) if len(height311) > 0 else 0
    height321MAX = ak.max(height321) if len(height321) > 0 else 0
    height331MAX = ak.max(height331) if len(height331) > 0 else 0

    print(height000MAX)
    print(height010MAX)
    print(height020MAX)
    print(height030MAX)
    print(height001MAX)
    print(height011MAX)
    print(height021MAX)
    print(height031MAX)
    print(height100MAX)
    print(height110MAX)
    print(height120MAX)
    print(height130MAX)
    print(height101MAX)
    print(height111MAX)
    print(height121MAX)
    print(height131MAX)
    print(height200MAX)
    print(height210MAX)
    print(height220MAX)
    print(height230MAX)
    print(height201MAX)
    print(height211MAX)
    print(height221MAX)
    print(height231MAX)
    print(height300MAX)
    print(height310MAX)
    print(height320MAX)
    print(height330MAX)
    print(height301MAX)
    print(height311MAX)
    print(height321MAX)
    print(height331MAX)
    print()

    print(len(height030))

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