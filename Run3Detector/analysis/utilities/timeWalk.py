import os
import sys
import ROOT as r
import numpy as np

sys.path.append("/Users/jahe0/Desktop/Physics-Research/Graduate-Research/MilliQan/milliqanOffline/Run3Detector/analysis/utilities/")
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

'''if not os.path.isfile('/Users/jahe0/Desktop/Physics-Research/Graduate-Research/MilliQan/milliqanOffline/Run3Detector/analysis/utilities/MilliQan_Run1035_v34.root'):
    print("Downloading our example files...")
    filePath2 = 'https://cernbox.cern.ch/s/tamc9PknEzhHwq4/download'
    os.system("wget -O $PWD/MilliQan_Run1035_v34.root {0} ".format(filePath2))
else:
    print("We already have our file!")'''
    
#Trying to plot the pulse area vs pulse time to see if we have time effects. This requires:
# 1) Identifying beam muons
# 2) Looking at small pulses near the beam path
# 3) pulse area vs pulse time plots

#define a file list to run over
#filelist = ['/net/cms26/cms26r0/milliqan/outputRun3Hadd/v34/MilliQan_Run1114_default_v34.root:t']
filelist = ['/Users/jahe0/Desktop/Physics-Research/Graduate-Research/MilliQan/milliqanOffline/Run3Detector/analysis/utilities/MilliQan_Run1035_v34.root:t',
            '/Users/jahe0/Desktop/Physics-Research/Graduate-Research/MilliQan/milliqanOffline/Run3Detector/analysis/utilities/MilliQan_Run1114_default_v34.root:t']

#define the relevant branches
branches = ['timeFit_module_calibrated', 'time', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

#define the milliqan cuts object
mycuts = milliqanCuts()

#Cuts
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=True) #Requires four layers to be hit
#layerCut = mycuts.getCut(mycuts.layerCut, 'layerCut', cut=False) #Required for the straightLineCut below
#straightLineCut = mycuts.getCut(mycuts.straightLineCut, 'straightLineCut', cut=False) #Make sure we have events in a straight line
#heightCut200 = mycuts.getCut(mycuts.heightCut, 'heightCut200', cut=500) #Add a height cut
#slabCut = mycuts.getCut(mycuts.slabCut, 'slabCut', cut=False) #Required for slabIncludedCut

#Custom cuts
def slabIncludedCut(self): #This requires both slabs to be hit with a certain threshold
  mask1 = ak.any((self.events['layer'] == -1) & (self.events['area'] > 60e3), axis=-1) & ak.any((self.events['layer'] == 4) & (self.events['area'] > 50e3), axis=-1)
  self.events['slabIncludedCut'] = mask1
  
def slabsOnly(self): #Looking for just the slabs themselves
  mask2 = (self.events['layer']==4) #| (self.events['layer']==4))
  self.events['slabsOnly'] = mask2
  
#def globPulse(self): #This will create a new branch with an integer corresponding to each pulse
#  self.events['globPulse'] = ak.local_index(self.events['ipulse'], axis=1)

def maxPulsePerLayer(self): #This labels the maximum pulse in each layer
  isMaxPulse = ak.zeros_like(self.events['height'], dtype=bool)
  #Cycle over each of the four layers and identify the maximum pulse time
  for i in np.arange(4):
    maxMask = ak.fill_none(self.events['height'] == ak.max(self.events['height'][self.events['layer'] == i], axis=-1, keepdims=True), False)
    first_occurrence_mask = (ak.num(maxMask[maxMask==True], axis=-1)) == 1 #Prevents the rare cases where two pulses are exact same height in same layer
    maxMask = ak.where(first_occurrence_mask, maxMask, isMaxPulse)
    isMaxPulse = isMaxPulse | maxMask 
  self.events['maxPulsePerLayer'] = isMaxPulse

def timeDiffMaxPulse(self): #This looks for the time difference between the max pulse and the other pulses
  maxPulsePerLayerMask = self.events['maxPulsePerLayer']
  timeDiffs = ak.zeros_like(self.events['height'], dtype=None)
  noneArray = ak.nan_to_none(ak.full_like(self.events['height'], None))
  onesArray = ak.ones_like(self.events['height'], dtype=int)
  
  for i in np.arange(4):
    layerMask = self.events['layer'] == i
    layerTimes = ak.where(layerMask, self.events['timeFit_module_calibrated'], noneArray) 
    layerMaxes = self.events['timeFit_module_calibrated'][layerMask & maxPulsePerLayerMask]
    expandedMaxes = ak.broadcast_arrays(ak.flatten(ak.pad_none(layerMaxes, 1)), onesArray)[0]

    tempTimeDiffs = layerTimes - expandedMaxes
    timeDiffs = ak.where(layerMask, tempTimeDiffs, timeDiffs)
    
  self.events['timeDiffMaxPulse'] = timeDiffs

def timeDiffMaxPulseCut(self): #For a time diff mask within a given region of time
  cutTimeDiffMask = (self.events['timeDiffMaxPulse'] < 100) & (self.events['timeDiffMaxPulse'] > -100)
  self.events['timeDiffMaxPulseCut'] = cutTimeDiffMask
  
def notMaxPulseBool(self): #This looks for the activity in nearby channels to the max pulse per layer
  notMaxPulseBool = ak.where((self.events['maxPulsePerLayer']), False, True)
  notMaxPulseBool = ak.where((self.events['layer']!=-1) & (self.events['layer']!=4), notMaxPulseBool, False)
  self.events['notMaxPulseBool'] = notMaxPulseBool

def singleChannelOnly(self): #Requires everything only be in a speficic channel
  singleChannelMask = (self.events['layer'] == 0) & (self.events['column'] == 0) & (self.events['row'] == 0)
  self.events['singleChannelOnly'] = singleChannelMask

#Calling custom cuts
setattr(milliqanCuts, 'slabIncludedCut', slabIncludedCut)
setattr(milliqanCuts, 'maxPulsePerLayer', maxPulsePerLayer)
setattr(milliqanCuts, 'timeDiffMaxPulse', timeDiffMaxPulse)
setattr(milliqanCuts, 'notMaxPulseBool', notMaxPulseBool)
setattr(milliqanCuts, 'timeDiffMaxPulseCut', timeDiffMaxPulseCut)
setattr(milliqanCuts, 'slabsOnly', slabsOnly)
setattr(milliqanCuts, 'singleChannelOnly', singleChannelOnly)

#create our combined cut
eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['fourLayerCut', 'slabIncludedCut', 'notMaxPulseBool', 'timeDiffMaxPulseCut'])
eventCutsSingleChannel = mycuts.getCut(mycuts.combineCuts, 'eventCutsSingleChannel', ['singleChannelOnly', 'fourLayerCut', 'slabIncludedCut', 'notMaxPulseBool', 'timeDiffMaxPulseCut'])
slabVerifyCut = mycuts.getCut(mycuts.combineCuts, 'slabVerifyCut', ['fourLayerCut', 'slabIncludedCut', 'slabsOnly'])
panelVerifyCut = mycuts.getCut(mycuts.combineCuts, 'panelVerifyCut', ['fourLayerCut', 'slabsOnly'])

#define milliqan plotter
myplotter = milliqanPlotter()

#create root histograms
#Eventcut heights
h_heights = r.TH1F("h_heights", "Heights [mV]", 140, 0, 1400)
h_heights.GetXaxis().SetTitle("Height [mV]")

#EventCut timeWalk plot (All channels)
h_timeWalk = r.TH2F("h_timeWalk", "Areas [mV] vs Time Difference from Max-in-Layer [ns]", 140, 0, 500000, 100, -100, 100)
h_timeWalk.GetXaxis().SetTitle("Area [pVs]")
h_timeWalk.GetYaxis().SetTitle("timeDiff [ns]")

#For looking at the slab cut verification
h_slabCutVerify = r.TH1F("h_slabCutVerify", "Slab Cut Verification", 100, 0, 1500)
h_slabCutVerify.GetXaxis().SetTitle("height [mV]")

#For looking at the eventCut layer distribution
h_layers = r.TH1F("h_layers", "Layers", 6, -1, 5)
h_layers.GetXaxis().SetTitle("Layer")

#For looking at eventCut time differences
h_timeDiffMaxPulse = r.TH1F("h_timeDiffMaxPulse", "Time Difference from Max Pulse", 100, -1000, 1000)
h_timeDiffMaxPulse.GetXaxis().SetTitle("Time Difference [ns]")

#For looking at in-layer eventCut positions of events
h_posn = r.TH2F("h_posn", "Position", 4, 0, 4, 4, 0, 4)
h_posn.GetXaxis().SetTitle("Column")
h_posn.GetYaxis().SetTitle("Row")

#For looking for the muon area threshold
h_panelArea = r.TH1F("h_panelArea", "Front/Back End Panel Areas", 100, 0, 700000)
h_panelArea.GetXaxis().SetTitle("Area [pVs]")

#For looking at the timeWalk plots in a specific channel
h_timeWalkSingleChannel = r.TH2F("h_timeWalkSingleChannel", "Areas [mV] vs Time Difference from Max-in-Layer [ns]", 140, 0, 500000, 100, -100, 100)
h_timeWalkSingleChannel.GetXaxis().SetTitle("Area [pVs]")
h_timeWalkSingleChannel.GetYaxis().SetTitle("timeDiff [ns]")

#add root histogram to plotter
myplotter.addHistograms(h_heights, 'height', 'eventCuts')
myplotter.addHistograms(h_timeWalk, ['area', 'timeDiffMaxPulse'], 'eventCuts')
myplotter.addHistograms(h_slabCutVerify, 'height', 'slabVerifyCut')
myplotter.addHistograms(h_layers, 'layer', 'eventCuts')
myplotter.addHistograms(h_timeDiffMaxPulse, 'timeDiffMaxPulse', 'eventCuts')
myplotter.addHistograms(h_posn, ['column', 'row'], 'eventCuts')
myplotter.addHistograms(h_panelArea, 'area', 'panelVerifyCut')
myplotter.addHistograms(h_timeWalkSingleChannel, ['area', 'timeDiffMaxPulse'], 'eventCutsSingleChannel')

#defining the cutflow
cutflow = [mycuts.singleChannelOnly, mycuts.fourLayerCut, mycuts.slabIncludedCut, mycuts.maxPulsePerLayer, mycuts.notMaxPulseBool, mycuts.timeDiffMaxPulse, mycuts.timeDiffMaxPulseCut, eventCuts, eventCutsSingleChannel, mycuts.slabsOnly, slabVerifyCut, panelVerifyCut, myplotter.dict['h_heights'], myplotter.dict['h_timeWalk'], myplotter.dict['h_posn'], myplotter.dict['h_layers'], myplotter.dict['h_slabCutVerify'], myplotter.dict['h_timeDiffMaxPulse'], myplotter.dict['h_panelArea'], myplotter.dict['h_timeWalkSingleChannel']]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

#run the milliqan processor
myiterator.run()

# Create a new TFile
f = r.TFile("timeWalkPlots.root", "recreate")

# Write the histograms to the file
h_heights.Write()
h_timeWalk.Write()
h_layers.Write()
h_posn.Write()
h_slabCutVerify.Write()
h_timeDiffMaxPulse.Write()
h_panelArea.Write()
h_timeWalkSingleChannel.Write()

# Close the file
f.Close()