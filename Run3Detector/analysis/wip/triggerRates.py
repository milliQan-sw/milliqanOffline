import sys

sys.path.append('/root/lib/')

import ROOT as r
import os
import json
import pandas as pd
import uproot 
import awkward as ak
import array as arr
import numpy as np
import sys

sys.path.append(os.getcwd() + '/../utilities/')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *

'''@mqCut
def countTriggers(self, cutName='countTriggers', trigNum=2):
    triggers = ak.firsts(self.events['tTrigger'])
    binary_trig = 1 << (trigNum-1)
    #print("Binary", trigNum, binary_trig)
    thisTrig = ak.count(triggers[triggers == binary_trig], axis=None)
    #print("instances of trigger {}, {}".format(trigNum, thisTrig))
    self.events[cutName] = thisTrig

print(countTriggers.__name__)

@mqCut
def firstEvent(self):
    events = ak.firsts(self.events['event'])
    mask = np.zeros(len(events), dtype=bool)
    mask[0] = True
    mask = ak.Array(mask)
    self.events['firsts'] = mask'''

if __name__ == "__main__":

    #get list of files to look at
    files = []

    dataDir = '/store/user/milliqan/trees/v34/1400/'
    for filename in os.listdir(dataDir):
        #if len(files) > 10: break
        if not filename.endswith('root'): continue
        if not int(filename.split('Run')[1].split('.')[0]) >= 1400: continue
        files.append(dataDir+filename)

    #define a file list to run over
    filelist = files[100:110]

    print(filelist)

    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'fileNumber', 'runNumber']

    #define the milliqan cuts object
    mycuts = milliqanCuts()

    #require pulses are not pickup
    pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)
    

    #require that all digitizer boards are matched
    #boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)
    boardMatchCut = getCutMod('boardMatchCut', cut=True, branches=branches)(mycuts, mycuts.boardsMatched)
    setattr(mycuts, 'boardMatchCut', boardMatchCut)

    #setattr(milliqanCuts, 'countTriggers', countTriggers)
    #setattr(milliqanCuts, 'firstEvent', firstEvent)

    trig1 = getCutMod('trig1', trigNum=1)(mycuts, mycuts.countTriggers)
    setattr(mycuts, 'trig1', trig1)


    #mycuts.trig1 = mycuts.getCut(mycuts.countTriggers, "trig1", trigNum=1)
    trig2 = mycuts.getCut(mycuts.countTriggers, "trig2", trigNum=2)
    trig3 = mycuts.getCut(mycuts.countTriggers, "trig3", trigNum=3)
    trig4 = mycuts.getCut(mycuts.countTriggers, "trig4", trigNum=4)
    trig5 = mycuts.getCut(mycuts.countTriggers, "trig5", trigNum=5)
    trig7 = mycuts.getCut(mycuts.countTriggers, "trig7", trigNum=7)
    trig9 = mycuts.getCut(mycuts.countTriggers, "trig9", trigNum=9)
    trig10 = mycuts.getCut(mycuts.countTriggers, "trig10", trigNum=10)
    trig11 = mycuts.getCut(mycuts.countTriggers, "trig11", trigNum=11)
    trig13 = mycuts.getCut(mycuts.countTriggers, "trig13", trigNum=13)

    #trig1 = mycuts.mqCut(trig1)

    
    setattr(milliqanCuts, 'trig2', trig2)
    setattr(milliqanCuts, 'trig3', trig3)
    setattr(milliqanCuts, 'trig4', trig4)
    setattr(milliqanCuts, 'trig5', trig5)
    setattr(milliqanCuts, 'trig7', trig7)
    setattr(milliqanCuts, 'trig9', trig9)
    setattr(milliqanCuts, 'trig10', trig10)
    setattr(milliqanCuts, 'trig11', trig11)
    setattr(milliqanCuts, 'trig13', trig13)

    #define milliqan plotter
    myplotter = milliqanPlotter()

    #create root histogram 
    bins = 200
    xmin = 0
    xmax = 400

    h_triggers = r.TH1F("h_triggers", "Triggers", bins, xmin, xmax)
    h_trig1 = r.TH1F("h_trig1", "Trigger 1", bins, xmin, xmax)
    h_trig2 = r.TH1F("h_trig2", "Trigger 2", bins, xmin, xmax)
    h_trig3 = r.TH1F("h_trig3", "Trigger 3", bins, xmin, xmax)
    h_trig4 = r.TH1F("h_trig4", "Trigger 4", bins, xmin, xmax)
    h_trig5 = r.TH1F("h_trig5", "Trigger 5", bins, xmin, xmax)
    h_trig7 = r.TH1F("h_trig7", "Trigger 7", bins, xmin, xmax)
    h_trig9 = r.TH1F("h_trig9", "Trigger 9", bins, xmin, xmax)
    h_trig10 = r.TH1F("h_trig10", "Trigger 10", bins, xmin, xmax)
    h_trig11 = r.TH1F("h_trig11", "Trigger 11", bins, xmin, xmax)
    h_trig13 = r.TH1F("h_trig13", "Trigger 13", bins, xmin, xmax)

    binsx = 100
    xmax_2d = 1500
    xmin_2d = 1400
    binsy = 200
    ymin = 0
    ymax = 400

    h_trig1_file = r.TH2F("h_trig1_file", "Trigger 1 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig2_file = r.TH2F("h_trig2_file", "Trigger 2 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig3_file = r.TH2F("h_trig3_file", "Trigger 3 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig4_file = r.TH2F("h_trig4_file", "Trigger 4 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig5_file = r.TH2F("h_trig5_file", "Trigger 5 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig7_file = r.TH2F("h_trig7_file", "Trigger 7 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig9_file = r.TH2F("h_trig9_file", "Trigger 9 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig10_file = r.TH2F("h_trig10_file", "Trigger 10 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig11_file = r.TH2F("h_trig11_file", "Trigger 11 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)
    h_trig13_file = r.TH2F("h_trig13_file", "Trigger 13 vs File", binsx, xmin_2d, xmax_2d, binsy, ymin, ymax)



    #add root histogram to plotter
    myplotter.addHistograms(h_triggers, 'tTrigger')
    myplotter.addHistograms(h_trig1, 'trig1', cut='firsts')
    myplotter.addHistograms(h_trig2, 'trig2', cut='firsts')
    myplotter.addHistograms(h_trig3, 'trig3', cut='firsts')
    myplotter.addHistograms(h_trig4, 'trig4', cut='firsts')
    myplotter.addHistograms(h_trig5, 'trig5', cut='firsts')
    myplotter.addHistograms(h_trig7, 'trig7', cut='firsts')
    myplotter.addHistograms(h_trig9, 'trig9', cut='firsts')
    myplotter.addHistograms(h_trig10, 'trig10', cut='firsts')
    myplotter.addHistograms(h_trig11, 'trig11', cut='firsts')
    myplotter.addHistograms(h_trig13, 'trig13', cut='firsts')

    myplotter.addHistograms(h_trig1_file, ["runNumber", "trig1"], cut='firsts')
    myplotter.addHistograms(h_trig2_file, ["runNumber", "trig2"], cut='firsts')
    myplotter.addHistograms(h_trig3_file, ["runNumber", "trig3"], cut='firsts')
    myplotter.addHistograms(h_trig4_file, ["runNumber", "trig4"], cut='firsts')
    myplotter.addHistograms(h_trig5_file, ["runNumber", "trig5"], cut='firsts')
    myplotter.addHistograms(h_trig7_file, ["runNumber", "trig7"], cut='firsts')
    myplotter.addHistograms(h_trig9_file, ["runNumber", "trig9"], cut='firsts')
    myplotter.addHistograms(h_trig10_file, ["runNumber", "trig10"], cut='firsts')
    myplotter.addHistograms(h_trig11_file, ["runNumber", "trig11"], cut='firsts')
    myplotter.addHistograms(h_trig13_file, ["runNumber", "trig13"], cut='firsts')


    #defining the cutflow
    #cutflow = [boardMatchCut, pickupCut, 
    cutflow = [boardMatchCut, 
                mycuts.trig1, 
                mycuts.countTriggers, 
                #trig2, trig3, trig4, trig5, trig7, 
                #trig9, trig10, trig11,trig13,
                mycuts.firstEvent]
                #myplotter.dict['h_triggers'], 
                #myplotter.dict['h_trig1'], myplotter.dict['h_trig2'], myplotter.dict['h_trig3'], myplotter.dict['h_trig4'], 
                #myplotter.dict['h_trig5'], myplotter.dict['h_trig7'], myplotter.dict['h_trig9'], myplotter.dict['h_trig10'], 
                #myplotter.dict['h_trig11'], myplotter.dict['h_trig13'], myplotter.dict['h_trig1_file'], myplotter.dict['h_trig2_file'],
                #myplotter.dict['h_trig3_file'], myplotter.dict['h_trig4_file'], myplotter.dict['h_trig5_file'], myplotter.dict['h_trig7_file'],
                #myplotter.dict['h_trig9_file'], myplotter.dict['h_trig10_file'], myplotter.dict['h_trig11_file'], myplotter.dict['h_trig13_file']]

    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=1000)

    #run the milliqan processor
    myiterator.run()

    #print cut flow
    mycuts.getCutflowCounts()

    #save plots
    myplotter.saveHistograms("test.root")