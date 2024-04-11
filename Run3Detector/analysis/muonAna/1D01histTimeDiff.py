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
      #assuming self.events is a dictionary containing awkward arrays
      times = self.events['timeFit_module_calibrated']
      layer = self.events['layer']

      #applying the eventCuts mask
      eventCuts = self.events['straightLineCut']  #this is a boolean array
      times = times[eventCuts]
      layer = layer[eventCuts]

      #require only 4 pulses in the event (possible multiple straight line paths were found)
      count = ak.count(times, keepdims=True, axis=1)
      count = count == 4
      count, times = ak.broadcast_arrays(count, times)
      times = times[count]
      layer = layer[count]

      times0 = times[layer == 0]
      times1 = times[layer == 1]
      times2 = times[layer == 2]
      times3 = times[layer == 3]

      #get time difference between two layers (here 1 and 0)
      t_out = times1-times0
      self.events['timeDiff'] = t_out
      print(type(self.events))
      print(self.events)


#define a file list to run over
filelist = ['/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/MilliQan_Run1006.4_v34.root:t']

#define the necessary branches to run over
branches = ['pickupFlag', 'boardsMatched', 'time_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

#define the milliqan cuts object
mycuts = milliqanCuts()

#require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

#require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

#add four layer cut
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

#add our custom function
setattr(milliqanCuts, 'getPulseDiff', getPulseDiff)

#call custom function to create timeDiff branch
mycuts.getPulseDiff()

#define milliqan plotter
myplotter = milliqanPlotter()

#create a 1D root histogram
h_1d = r.TH1F("h_1d", "1d Histogram", 80, -40, 40)
h_1d.GetXaxis().SetTitle("layer0-1 time diff")

#add root histogram to plotter
myplotter.addHistograms(h_1d, 'timeDiff')

#defining the cutflow
cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.straightLineCut, myplotter.dict['h_1d']]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

#run the milliqan processor
myiterator.run()

#create a new TFile
f = r.TFile("1DhistTimeDiff0-1.root", "recreate")

#write the histograms to the file
h_1d.Write()

#close the file
f.Close()