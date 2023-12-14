import os
import sys
import ROOT as r

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

if not os.path.isfile('MilliQan_Run1035_v34.root'):
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
filelist = ['MilliQan_Run1035_v34.root:t']

#define the relevant branches
branches = ['timeFit_module_calibrated', 'time', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

#define the milliqan cuts object
mycuts = milliqanCuts()

#Cuts
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False) #Requires four layers to be hit
layerCut = mycuts.getCut(mycuts.layerCut, 'layerCut', cut=False) #Required for the straightLineCut below
straightLineCut = mycuts.getCut(mycuts.straightLineCut, 'straightLineCut', cut=False) #Make sure we have events in a straight line
heightCut200 = mycuts.getCut(mycuts.heightCut, 'heightCut200', cut=500) #Add a height cut
slabCut = mycuts.getCut(mycuts.slabCut, 'slabCut', cut=False) #Required for slabIncludedCut

#Custom cuts
def slabIncludedCut(self): #This requires both slabs to be hit
  mask1 = ak.any(self.events['layer'] == -1, axis=-1) & ak.any(self.events['layer'] == 4, axis=-1)
  self.events['slabIncludedCut'] = mask1
  
def pulseInt(self): #This will create a new branch with an integer corresponding to each pulse
  self.events['pulseInt'] = ak.local_index(self.events['ipulse'], axis=1)
  
def maxPulseInt(self): #This will create a new branch with the pulse integer of the pulse with max height
  self.events['maxPulseInt'] = ak.argmax(self.events['height']['eventCuts'], axis=1)

#Calling custom cuts
setattr(milliqanCuts, 'slabIncludedCut', slabIncludedCut)
setattr(milliqanCuts, 'pulseInt', pulseInt)

#create our combined cut
eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['fourLayerCut', 'straightLineCut', 'slabIncludedCut'])

#define milliqan plotter
myplotter = milliqanPlotter()

#create root histograms
h_heights = r.TH1F("h_heights", "Heights [mV]", 140, 0, 1400)
h_heights.GetXaxis().SetTitle("Height [mV]")

h_timeWalk = r.TH2F("h_timeWalk", "Areas [mV] vs Time [ns]", 140, 0, 500000, 100, 0, 3000)
h_timeWalk.GetXaxis().SetTitle("Area [pVs]")
h_timeWalk.GetYaxis().SetTitle("timeFit_module_calibrated [ns]")

h_timeWalkOrig = r.TH2F("h_timeWalkOrig", "Areas [mV] vs Original Time [ns]", 140, 0, 500000, 100, 0, 3000)
h_timeWalkOrig.GetXaxis().SetTitle("Area [pVs]")
h_timeWalkOrig.GetYaxis().SetTitle("time [ns]")

h_layers = r.TH1F("h_layers", "Layers", 6, -1, 5)
h_layers.GetXaxis().SetTitle("Layer")

h_pulseInt = r.TH1F("h_pulseInt", "Pulse Integers", 100, 0, 100)
h_pulseInt.GetXaxis().SetTitle("Pulse Integer")


#add root histogram to plotter
myplotter.addHistograms(h_heights, 'height', 'eventCuts')
myplotter.addHistograms(h_timeWalk, ['area', 'timeFit_module_calibrated'], 'eventCuts')
myplotter.addHistograms(h_timeWalkOrig, ['area', 'time'], 'eventCuts')
myplotter.addHistograms(h_layers, 'layer', 'eventCuts')
myplotter.addHistograms(h_pulseInt, 'pulseInt', 'eventCuts')

#defining the cutflow
cutflow = [mycuts.fourLayerCut, mycuts.layerCut, mycuts.straightLineCut, heightCut200, mycuts.slabCut, mycuts.slabIncludedCut, eventCuts, mycuts.pulseInt, myplotter.dict['h_heights'], myplotter.dict['h_timeWalk'], myplotter.dict['h_timeWalkOrig'], myplotter.dict['h_layers'], myplotter.dict['h_pulseInt']]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

#run the milliqan processor
myiterator.run()

# Create a new TFile
f = r.TFile("test.root", "recreate")

# Write the histograms to the file
h_heights.Write()
h_timeWalk.Write()
h_timeWalkOrig.Write()
h_layers.Write()
h_pulseInt.Write()

# Close the file
f.Close()

