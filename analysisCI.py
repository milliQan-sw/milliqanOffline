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
    if not os.path.exists('notActuallyRun1364.3.root'): os.system('curl -o notActuallyRun1364.3.root https://cernbox.cern.ch/s/7aVy5emV9tivPrl/download')
    if not os.path.exists('check.root'): os.system('curl -o check.root https://cernbox.cern.ch/s/hTZyaUVU9fuCWUX/download')

    #define a file list to run over
    filelist = ['notActuallyRun1364.3.root:t']

    #define the necessary branches to run over
    branches = ['pickupFlag', 'boardsMatched', 'timeFit_module_calibrated', 'height', 'area', 'column', 'row', 'layer', 'chan', 'ipulse', 'type', 'fileNumber', 'runNumber', 'tTrigger', 'event', 'npulses']

    #define the milliqan cuts object
    mycuts = milliqanCuts()

    #require pulses are not pickup
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', cut=True)

    #require that all digitizer boards are matched
    boardMatchCut = getCutMod(mycuts.boardsMatched, mycuts, 'boardMatchCut', cut=True)

    #Add four layer cut
    fourLayerCut = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'oneHitPerLayer', cut=True, multipleHits=False)


    #define milliqan plotter
    myplotter = milliqanPlotter()

    #create root histogram 
    h_height = r.TH1F("h_height", "Pulse Height", 1400, 0, 1400)

    #add root histogram to plotter
    myplotter.addHistograms(h_height, 'height')

    #defining the cutflow
    cutflow = [boardMatchCut, pickupCut, fourLayerCut, mycuts.straightLineCut, mycuts.barCut, myplotter.dict['h_height']]

    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter, qualityLevel='override')

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
