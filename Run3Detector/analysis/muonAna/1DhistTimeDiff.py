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
    heights = self.events['height']['straightLineCut']

    height000 = heights[(self.events['row']==0)&(self.events['column']==0)&(self.events['layer']==0)]
    height010 = heights[(self.events['row']==0)&(self.events['column']==1)&(self.events['layer']==0)]
    height020 = heights[(self.events['row']==0)&(self.events['column']==2)&(self.events['layer']==0)]
    height030 = heights[(self.events['row']==0)&(self.events['column']==3)&(self.events['layer']==0)]
    height001 = heights[(self.events['row']==0)&(self.events['column']==0)&(self.events['layer']==1)]
    height011 = heights[(self.events['row']==0)&(self.events['column']==1)&(self.events['layer']==1)]
    height021 = heights[(self.events['row']==0)&(self.events['column']==2)&(self.events['layer']==1)]
    height031 = heights[(self.events['row']==0)&(self.events['column']==3)&(self.events['layer']==1)]
    height100 = heights[(self.events['row']==1)&(self.events['column']==0)&(self.events['layer']==0)]
    height110 = heights[(self.events['row']==1)&(self.events['column']==1)&(self.events['layer']==0)]
    height120 = heights[(self.events['row']==1)&(self.events['column']==2)&(self.events['layer']==0)]
    height130 = heights[(self.events['row']==1)&(self.events['column']==3)&(self.events['layer']==0)]
    height101 = heights[(self.events['row']==1)&(self.events['column']==0)&(self.events['layer']==1)]
    height111 = heights[(self.events['row']==1)&(self.events['column']==1)&(self.events['layer']==1)]
    height121 = heights[(self.events['row']==1)&(self.events['column']==2)&(self.events['layer']==1)]
    height131 = heights[(self.events['row']==1)&(self.events['column']==3)&(self.events['layer']==1)]
    height200 = heights[(self.events['row']==2)&(self.events['column']==0)&(self.events['layer']==0)]
    height210 = heights[(self.events['row']==2)&(self.events['column']==1)&(self.events['layer']==0)]
    height220 = heights[(self.events['row']==2)&(self.events['column']==2)&(self.events['layer']==0)]
    height230 = heights[(self.events['row']==2)&(self.events['column']==3)&(self.events['layer']==0)]
    height201 = heights[(self.events['row']==2)&(self.events['column']==0)&(self.events['layer']==1)]
    height211 = heights[(self.events['row']==2)&(self.events['column']==1)&(self.events['layer']==1)]
    height221 = heights[(self.events['row']==2)&(self.events['column']==2)&(self.events['layer']==1)]
    height231 = heights[(self.events['row']==2)&(self.events['column']==3)&(self.events['layer']==1)]
    height300 = heights[(self.events['row']==3)&(self.events['column']==0)&(self.events['layer']==0)]
    height310 = heights[(self.events['row']==3)&(self.events['column']==1)&(self.events['layer']==0)]
    height320 = heights[(self.events['row']==3)&(self.events['column']==2)&(self.events['layer']==0)]
    height330 = heights[(self.events['row']==3)&(self.events['column']==3)&(self.events['layer']==0)]
    height301 = heights[(self.events['row']==3)&(self.events['column']==0)&(self.events['layer']==1)]
    height311 = heights[(self.events['row']==3)&(self.events['column']==1)&(self.events['layer']==1)]
    height321 = heights[(self.events['row']==3)&(self.events['column']==2)&(self.events['layer']==1)]
    height331 = heights[(self.events['row']==3)&(self.events['column']==3)&(self.events['layer']==1)]

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

    times = self.events['timeFit_module_calibrated']['straightLineCut']
    time000 = times[self.events['height'] == height000MAX]
    time010 = times[self.events['height'] == height010MAX]
    time020 = times[self.events['height'] == height020MAX]
    time030 = times[self.events['height'] == height030MAX]
    time001 = times[self.events['height'] == height001MAX]
    time011 = times[self.events['height'] == height011MAX]
    time021 = times[self.events['height'] == height021MAX]
    time031 = times[self.events['height'] == height031MAX]
    time100 = times[self.events['height'] == height100MAX]
    time110 = times[self.events['height'] == height110MAX]
    time120 = times[self.events['height'] == height120MAX]
    time130 = times[self.events['height'] == height130MAX]
    time101 = times[self.events['height'] == height101MAX]
    time111 = times[self.events['height'] == height111MAX]
    time121 = times[self.events['height'] == height121MAX]
    time131 = times[self.events['height'] == height131MAX]
    time200 = times[self.events['height'] == height200MAX]
    time210 = times[self.events['height'] == height210MAX]
    time220 = times[self.events['height'] == height220MAX]
    time230 = times[self.events['height'] == height230MAX]
    time201 = times[self.events['height'] == height201MAX]
    time211 = times[self.events['height'] == height211MAX]
    time221 = times[self.events['height'] == height221MAX]
    time231 = times[self.events['height'] == height231MAX]
    time300 = times[self.events['height'] == height300MAX]
    time310 = times[self.events['height'] == height310MAX]
    time320 = times[self.events['height'] == height320MAX]
    time330 = times[self.events['height'] == height330MAX]
    time301 = times[self.events['height'] == height301MAX]
    time311 = times[self.events['height'] == height311MAX]
    time321 = times[self.events['height'] == height321MAX]
    time331 = times[self.events['height'] == height331MAX]

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

    self.events['timeDiff02'] = timeDiff02
    self.events['timeDiff03'] = timeDiff03
    self.events['timeDiff10'] = timeDiff10
    self.events['timeDiff11'] = timeDiff11
    self.events['timeDiff12'] = timeDiff12
    self.events['timeDiff13'] = timeDiff13
    self.events['timeDiff20'] = timeDiff20
    self.events['timeDiff21'] = timeDiff21
    self.events['timeDiff22'] = timeDiff22
    self.events['timeDiff23'] = timeDiff23
    self.events['timeDiff30'] = timeDiff30
    self.events['timeDiff31'] = timeDiff31
    self.events['timeDiff32'] = timeDiff32
    self.events['timeDiff33'] = timeDiff33



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