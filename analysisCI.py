import os
import sys
sys.path.append(os.getcwd() + '/Run3Detector/analysis/utilities/')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

if __name__ == "__main__":

    #get the offline file and a copy of output plots from cernbox
    #TODO may want to use the file processed when checking offline file processing
    if not os.path.exists('offline.root'): os.system('curl -o offline.root https://cernbox.cern.ch/s/7aVy5emV9tivPrl/download')
    if not os.path.exists('check.root'): os.system('curl -o check.root https://cernbox.cern.ch/s/hTZyaUVU9fuCWUX/download')

    #define a file list to run over
    filelist = ['offline.root:t']

    #define the necessary branches to run over
    branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type']

    #define the milliqan cuts object
    mycuts = milliqanCuts()

    #require pulses are not pickup
    pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

    #require that all digitizer boards are matched
    boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

    #Add four layer cut
    fourLayerCut = mycuts.getCut(mycuts.fourLayerCut, 'fourLayerCut', cut=False)

    #create our combined cut
    eventCuts = mycuts.getCut(mycuts.combineCuts, 'eventCuts', ['fourLayerCut', 'straightPulseCut', 'firstChanPulse', 'barCut'])

    #define milliqan plotter
    myplotter = milliqanPlotter()

    #create root histogram 
    h_height = r.TH1F("h_height", "Pulse Height", 1400, 0, 1400)

    #add root histogram to plotter
    myplotter.addHistograms(h_height, 'height')

    #defining the cutflow
    cutflow = [boardMatchCut, pickupCut, mycuts.layerCut, mycuts.fourLayerCut, mycuts.straightLineCut, mycuts.firstChanPulse, mycuts.barCut, eventCuts, myplotter.dict['h_height']]

    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

    #run the milliqan processor
    myiterator.run()

    #compare histo to saved version
    r_check = r.TFile.Open('check.root', 'read')
    h_heightCheck = r_check.Get('h_height')
    entries = h_heightCheck.GetEntries()
    h_heightCheck.Add(h_height, -1)
    if(h_heightCheck.Integral() > entries):
        print("Error: The plot created does not match the saved version!")
        sys.exit(1)
