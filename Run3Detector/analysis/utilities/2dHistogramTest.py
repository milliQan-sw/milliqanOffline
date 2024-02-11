#This is an example of how to use my 2d/3d plotting functionality in milliqanPlotter
import os
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
layerCut = mycuts.getCut(mycuts.layerCut, 'layerCut', cut=False) #Required for the straightLineCut below
fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False) #Requires four layers to be hit
straightLineCut = mycuts.getCut(mycuts.straightLineCut, 'straightLineCut', cut=False) #Make sure we have events in a straight line
heightCut200 = mycuts.getCut(mycuts.heightCut, 'heightCut200', cut=200) #Add a height cut
slabCut = mycuts.getCut(mycuts.slabCut, 'slabCut', cut=False) #Required for slabIncludedCut

#create our combined cut
eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['fourLayerCut', 'straightLineCut', 'heightCut200', 'slabCut'])

#define milliqan plotter
myplotter = milliqanPlotter()

#create root histograms
h_test1d = r.TH1F("h_test1d", "1d Histogram", 100, 0, 500000)
h_test1d.GetXaxis().SetTitle("area [pVs]")
h_test2d = r.TH2F("h_test2d", "2d Histogram", 140, 0, 500000, 100, 0, 3000)
h_test2d.GetXaxis().SetTitle("area [pVs]")
h_test2d.GetYaxis().SetTitle("time [ns]")

#add root histogram to plotter
myplotter.addHistograms(h_test1d, 'area', 'eventCuts')
myplotter.addHistograms(h_test2d, ['area', 'time'], 'eventCuts')

#defining the cutflow
cutflow = [mycuts.fourLayerCut, mycuts.layerCut, mycuts.straightLineCut, heightCut200, mycuts.slabCut, eventCuts, myplotter.dict['h_test1d'], myplotter.dict['h_test2d']]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

#run the milliqan processor
myiterator.run()

# Create a new TFile
f = r.TFile("2dTest.root", "recreate")

# Write the histograms to the file
h_test1d.Write()
h_test2d.Write()

# Close the file
f.Close()

