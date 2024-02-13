import os
import sys
import ROOT as r
import numpy as np

sys.path.append("/Users/jahe0/Desktop/Physics-Research/Graduate-Research/MilliQan/milliqanOffline/Run3Detector/analysis/utilities/")
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

if not os.path.isfile('/Users/jahe0/Desktop/Physics-Research/Graduate-Research/MilliQan/milliqanOffline/Run3Detector/analysis/utilities/MilliQan_Run1035_v34.root'):
    print("Downloading our example files...")
    filePath2 = 'https://cernbox.cern.ch/s/tamc9PknEzhHwq4/download'
    os.system("wget -O $PWD/MilliQan_Run1035_v34.root {0} ".format(filePath2))
else:
    print("We already have our file!")
    
#Trying to plot the pulse area vs pulse time to see if we have time effects. This requires:
# 1) Identifying beam muons
# 2) Looking at small pulses near the beam path
# 3) pulse area vs pulse time plots

#define a file list to run over
filelist = ['/Users/jahe0/Desktop/Physics-Research/Graduate-Research/MilliQan/milliqanOffline/Run3Detector/analysis/utilities/MilliQan_Run1035_v34.root:t']

#define the relevant branches
branches = ['timeFit_module_calibrated', 'time', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

#define the milliqan cuts object
mycuts = milliqanCuts()

#Cuts
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False) #Requires four layers to be hit
#layerCut = mycuts.getCut(mycuts.layerCut, 'layerCut', cut=False) #Required for the straightLineCut below
#straightLineCut = mycuts.getCut(mycuts.straightLineCut, 'straightLineCut', cut=False) #Make sure we have events in a straight line
#heightCut200 = mycuts.getCut(mycuts.heightCut, 'heightCut200', cut=500) #Add a height cut
#slabCut = mycuts.getCut(mycuts.slabCut, 'slabCut', cut=False) #Required for slabIncludedCut

#Custom cuts
def slabIncludedCut(self): #This requires both slabs to be hit
  mask1 = ak.any((self.events['layer'] == -1) & (self.events['height'] > 400), axis=-1) & ak.any((self.events['layer'] == 4) & (self.events['height'] > 400), axis=-1)
  self.events['slabIncludedCut'] = mask1
  
def slabsOnly(self):
  mask2 = ((self.events['layer']==1) | (self.events['layer']==4))
  self.events['slabsOnly'] = mask2
  
#def globPulse(self): #This will create a new branch with an integer corresponding to each pulse
#  self.events['globPulse'] = ak.local_index(self.events['ipulse'], axis=1)

def notMaxPulseBool(self):
  overall_indices = ak.zeros_like(self.events['height'], dtype=bool)
  false_array = ak.zeros_like(self.events['height'], dtype=bool)
  
  for i in np.arange(4): #Columns
    for k in np.arange(4): #Rows
        for l in np.arange(4): #Layers
          #For the current channel
          channel_indices = ((self.events['column'] == i) & (self.events['row'] == k) & (self.events['layer'] == l))
          #For the nearby channels (inclusive of channel_indices)
          neighbor_indices = (
                                (((self.events['column'] == i+1) & (i+1<4)) | ((self.events['column'] == i) & (self.events['row'] != k)) | ((self.events['column'] == i-1) & (i-1>-1))) 
                                & (((self.events['row'] == k+1) & (k+1<4)) | ((self.events['row'] == k) & (self.events['column'] != i)) | ((self.events['row'] == k-1) & (k-1>-1))) 
                                & (self.events['layer'] == l) 
                                )
          #Join the location cuts with the height cut
          neighbor_height_indices = (neighbor_indices) & (self.events['height'] < ak.max(ak.where((channel_indices), self.events['height'], false_array), keepdims=1, axis=-1))
          #Append these cuts to the overall_indices using boolean OR logic.
          overall_indices = overall_indices | neighbor_height_indices
  self.events['notMaxPulseBool'] = overall_indices

#Calling custom cuts
setattr(milliqanCuts, 'slabIncludedCut', slabIncludedCut)
#setattr(milliqanCuts, 'globPulse', globPulse)
setattr(milliqanCuts, 'notMaxPulseBool', notMaxPulseBool)
setattr(milliqanCuts, 'slabsOnly', slabsOnly)

#create our combined cut
eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['fourLayerCut', 'slabIncludedCut', 'notMaxPulseBool'])
slabVerifyCut = mycuts.getCut(mycuts.combineCuts, 'slabVerifyCut', ['fourLayerCut', 'slabIncludedCut', 'slabsOnly'])

#define milliqan plotter
myplotter = milliqanPlotter()

#create root histograms
h_heights = r.TH1F("h_heights", "Heights [mV]", 140, 0, 1400)
h_heights.GetXaxis().SetTitle("Height [mV]")

h_timeWalk = r.TH2F("h_timeWalk", "Areas [mV] vs Time [ns]", 140, 0, 500000, 100, 0, 3000)
h_timeWalk.GetXaxis().SetTitle("Area [pVs]")
h_timeWalk.GetYaxis().SetTitle("timeFit_module_calibrated [ns]")

h_slabCutVerify = r.TH1F("h_slabCutVerify", "Slab Cut Verification", 100, 0, 1500)
h_timeWalk.GetXaxis().SetTitle("height [mV]")

#h_timeWalkOrig = r.TH2F("h_timeWalkOrig", "Areas [mV] vs Original Time [ns]", 140, 0, 500000, 100, 0, 3000)
#h_timeWalkOrig.GetXaxis().SetTitle("Area [pVs]")
#h_timeWalkOrig.GetYaxis().SetTitle("time [ns]")

h_layers = r.TH1F("h_layers", "Layers", 6, -1, 5)
h_layers.GetXaxis().SetTitle("Layer")

#h_globPulse = r.TH1F("h_globPulse", "Global Pulse Integers", 100, 0, 100)
#h_globPulse.GetXaxis().SetTitle("Global Pulse Integer")

h_posn = r.TH2F("h_posn", "Position", 4, 0, 4, 4, 0, 4)
h_posn.GetXaxis().SetTitle("Column")
h_posn.GetYaxis().SetTitle("Row")


#add root histogram to plotter
myplotter.addHistograms(h_heights, 'height', 'eventCuts')
myplotter.addHistograms(h_timeWalk, ['area', 'timeFit_module_calibrated'], 'eventCuts')
#myplotter.addHistograms(h_timeWalkOrig, ['area', 'time'], 'eventCuts')
myplotter.addHistograms(h_layers, 'layer', 'eventCuts')
#myplotter.addHistograms(h_globPulse, 'globPulse', 'eventCuts')
myplotter.addHistograms(h_posn, ['column', 'row'], 'eventCuts')
myplotter.addHistograms(h_slabCutVerify, 'height', 'slabVerifyCut')

#defining the cutflow
cutflow = [mycuts.fourLayerCut, mycuts.slabIncludedCut, mycuts.notMaxPulseBool, eventCuts, mycuts.slabsOnly, slabVerifyCut, myplotter.dict['h_heights'], myplotter.dict['h_timeWalk'], myplotter.dict['h_posn'], myplotter.dict['h_layers'], myplotter.dict['h_slabCutVerify']]

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
#h_timeWalkOrig.Write()
h_layers.Write()
#h_globPulse.Write()
h_posn.Write()
h_slabCutVerify.Write()

# Close the file
f.Close()