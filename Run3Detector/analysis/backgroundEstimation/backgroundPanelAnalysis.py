


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
import shutil
import itertools

sys.path.append(os.path.dirname(__file__) + '/../utilities/')
from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *
from utilities import *

@mqCut
def cosmicMuonCut(self, cutName='cosmicMuonCut', nBarsRequired = 2, areaCut=10e3, cut=False, branches=None):


    frontPanels = ak.any((self.events['type']==2) & self.events['layer']==0, axis=1)
    backPanels = ak.any((self.events['type']==2) & self.events['layer']==2, axis=1)

    nBarsL1 = ak.sum((self.events['type']==0) & (self.events['layer']==0) & (self.events['area'] > areaCut), axis=1) > nBarsRequired
    nBarsL2 = ak.sum((self.events['type']==0) & (self.events['layer']==1) & (self.events['area'] > areaCut), axis=1) > nBarsRequired
    nBarsL3 = ak.sum((self.events['type']==0) & (self.events['layer']==2) & (self.events['area'] > areaCut), axis=1) > nBarsRequired
    nBarsL4 = ak.sum((self.events['type']==0) & (self.events['layer']==3) & (self.events['area'] > areaCut), axis=1) > nBarsRequired

    frontBars = nBarsL1 | nBarsL2  
    backBars = nBarsL3 | nBarsL4

    #cosmicCut = (frontPanels & frontBars) | (backPanels & backBars)
    cosmicCut = frontBars | backBars

    _, cosmicCut = ak.broadcast_arrays(self.events['npulses'], cosmicCut)

    self.events[cutName] = cosmicCut

    if cut:
        self.cutBranches(branches, cutName)

@mqCut
def cosmicMuonCutHard(self, cutName='cosmicMuonCutHard', nBarsRequired=4, areaCut=300e3, cut=False, branches=None):

    L1 = (self.events['type'] == 0) & (self.events['layer'] == 0) & (self.events['area'] >= areaCut)
    L4 = (self.events['type'] == 0) & (self.events['layer'] == 3) & (self.events['area'] >= areaCut)

    for i in range(4):
        if i==0:
            passes1 = ak.sum(L1 & (self.events['column'] == i), axis=1) >= nBarsRequired
            passes4 = ak.sum(L4 & (self.events['column'] == i), axis=1) >= nBarsRequired
        else:
            passes1 = passes1 | (ak.sum(L1 & (self.events['column'] == i), axis=1) >= nBarsRequired)
            passes4 = passes4 | (ak.sum(L4 & (self.events['column'] == i), axis=1) >= nBarsRequired)

    passes = passes1 | passes4

    _, passes = ak.broadcast_arrays(self.events['npulses'], passes)
    self.events[cutName] = passes

    if cut:
        self.cutBranches(branches, cutName)


@mqCut
def frontBackPanelInfo(self, cutName='frontBackPanelInfo', cut=False, branches=None):

    frontPanelCut = (self.events['type']==1) & (self.events['layer']==-1)
    backPanelCut = (self.events['type']==1) & (self.events['layer']==4)

    frontPanelCut = frontPanelCut & (self.events['height']>=1200)
    backPanelCut = backPanelCut & (self.events['height']>=1200)
    
    self.events['frontArea'] = self.events['area'][frontPanelCut]
    self.events['backArea'] = self.events['area'][backPanelCut]

    self.events['frontNPE'] = self.events['nPE'][frontPanelCut]
    self.events['backNPE'] = self.events['nPE'][backPanelCut]

    self.events['frontHeight'] = self.events['height'][frontPanelCut]
    self.events['backHeight'] = self.events['height'][backPanelCut]

    self.events['frontDuration'] = self.events['duration'][frontPanelCut]
    self.events['backDuration'] = self.events['duration'][backPanelCut]

    self.events['frontRiseSamples'] = self.events['riseSamples'][frontPanelCut]
    self.events['backRiseSamples'] = self.events['riseSamples'][backPanelCut]

    self.events['frontFallSamples'] = self.events['fallSamples'][frontPanelCut]
    self.events['backFallSamples'] = self.events['fallSamples'][backPanelCut]

    _, self.events['frontHits'] = ak.broadcast_arrays(self.events['npulses'], ak.count(self.events['npulses'][frontPanelCut], axis=1))
    _, self.events['backHits'] = ak.broadcast_arrays(self.events['npulses'], ak.count(self.events['npulses'][backPanelCut], axis=1))
    


if __name__ == "__main__":

    beam = False
    skim = True
    sim = True
    outputFile = 'bgCutPanelAnalysisCosmicSkimV2.root'
    qualityLevel = 'tight'
    maxEvents = None
    stepSize = 20000
    makeCut = True

    filelist = [     

        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1300_v35_cosmic_beamOff_tight.root', 
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1400_v35_cosmic_beamOff_tight.root', 
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1500_v35_cosmic_beamOff_tight.root', 
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1600_v35_cosmic_beamOff_tight.root', 
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1700_v35_cosmic_beamOff_tight.root', 
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1800_v35_cosmic_beamOff_tight.root', 
        '/eos/experiment/milliqan/skims/cosmic/MilliQan_Run1900_v35_cosmic_beamOff_tight.root', 

        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1400_v35_beam_beamOn_tight.root',
        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1500_v35_beam_beamOn_tight.root',
        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1600_v35_beam_beamOn_tight.root',
        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1700_v35_beam_beamOn_tight.root',
        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1800_v35_beam_beamOn_tight.root',
        #'/eos/experiment/milliqan/skims/beam/MilliQan_Run1900_v35_beam_beamOn_tight.root',

        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1000_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1100_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1300_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1400_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1500_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1600_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1700_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1800_v35_signal_beamOff_medium.root",
        #"/eos/experiment/milliqan/skims/signal/panel50kAllowed/MilliQan_Run1900_v35_signal_beamOff_medium.root",

        #"/eos/experiment/milliqan/skims/signal/MilliQan_Run1300_v35_signal_beamOff_tight.root",
        #"/eos/experiment/milliqan/skims/signal/MilliQan_Run1400_v35_signal_beamOff_tight.root",
        #"/eos/experiment/milliqan/skims/signal/MilliQan_Run1500_v35_signal_beamOff_tight.root",
        #"/eos/experiment/milliqan/skims/signal/MilliQan_Run1600_v35_signal_beamOff_tight.root",
        #"/eos/experiment/milliqan/skims/signal/MilliQan_Run1700_v35_signal_beamOff_tight.root",
        #"/eos/experiment/milliqan/skims/signal/MilliQan_Run1800_v35_signal_beamOff_tight.root",
        #"/eos/experiment/milliqan/skims/signal/MilliQan_Run1900_v35_signal_beamOff_tight.root",
        ]

    if skim:
        qualityLevel = 'override'

    if len(sys.argv) > 7:
        beam = (sys.argv[1] == 'True')
        skim = (sys.argv[2] == 'True')
        sim = (sys.argv[3] == 'True')
        outputFile = str(sys.argv[4])
        qualityLevel = str(sys.argv[5])
        filelist = sys.argv[6].split(',')
        if sys.argv[7] == 'None':
            maxEvents = None
        else:
            maxEvents = int(sys.argv[7])

    print("Running on files {}".format(filelist))

    goodRunsName = '/eos/experiment/milliqan/Configs/goodRunsList.json'
    lumisName = '/eos/experiment/milliqan/Configs/mqLumis.json'
    shutil.copy(goodRunsName, 'goodRunsList.json')
    shutil.copy(lumisName, 'mqLumis.json')

    goodRuns = loadJson('goodRunsList.json')
    lumis = loadJson('mqLumis.json')

    if skim:
        lumi, runTime = getSkimLumis(filelist)
    elif not sim:
        lumi, runTime = getLumiofFileList(filelist)
    else:
        lumi, runTime = 0, 0 #TODO scale to data 

    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'pickupFlagTight', 'fileNumber', 
                'runNumber', 'type', 'ipulse', 'nPE', 'chan','time_module_calibrated', 'timeFit_module_calibrated', 
                'row', 'column', 'layer', 'height', 'area', 'npulses', 'sidebandRMS', 'duration', 'riseSamples', 'fallSamples']


    #define the milliqan cuts object
    mycuts = milliqanCuts()

    setattr(milliqanCuts, "frontBackPanelInfo", frontBackPanelInfo)
    setattr(milliqanCuts, "comsicMuonCut", cosmicMuonCut)
    setattr(milliqanCuts, "comsicMuonCutHard", cosmicMuonCutHard)



    #require pulses are in trigger window
    centralTimeCut = getCutMod(mycuts.centralTime, mycuts, 'centralTimeCut', cut=makeCut)

    #require pulses are not pickup
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', cut=makeCut, tight=True)

    #require that all digitizer boards are matched
    boardMatchCut = getCutMod(mycuts.boardsMatched, mycuts, 'boardMatchCut', cut=makeCut, branches=branches)

    #greater than or equal to one hit per layer
    hitInAllLayers = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'hitInAllLayers', cut=makeCut, multipleHits=True)

    #exactly one hit per layer
    oneHitPerLayer = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'oneHitPerLayer', cut=makeCut, multipleHits=False)

    #panel veto
    panelVeto = getCutMod(mycuts.panelVeto, mycuts, 'panelVeto', cut=makeCut, nPECut=None)
    #panelVeto = getCutMod(mycuts.panelVetoMod, mycuts, 'panelVeto', cut=makeCut, nPECut=None, areaCut=100e3, panelsAllowed=1)

    #first pulse max
    firstPulseMax = getCutMod(mycuts.firstPulseMax, mycuts, 'firstPulseMax', cut=makeCut)

    #veto events with an early pulse
    vetoEarlyPulse = getCutMod(mycuts.vetoEarlyPulse, mycuts, 'vetoEarlyPulse', cut=makeCut)

    #four in line cut
    straightLineCutMod = getCutMod(mycuts.straightLineCut, mycuts, 'straightLineCutMod', cut=makeCut)

    #npe max-min < 10 cut
    nPEMaxMin = getCutMod(mycuts.nPEMaxMin, mycuts, 'nPEMaxMin', nPECut=20, cut=makeCut)
    #nPEMaxMin = getCutMod(mycuts.nPEStdDev, mycuts, 'nPEStdDev', std=5, cut=makeCut)

    nPEMaxCut = getCutMod(mycuts.nPEMaxCut, mycuts, 'nPEMaxCut', nPECut=20, cut=makeCut)

    #time max-min < 15 cut
    timeMaxMinNoCut = getCutMod(mycuts.timeMaxMin, mycuts, 'timeMaxMinPlot', timeCut=20)
    timeMaxMin = getCutMod(mycuts.timeMaxMin, mycuts, 'timeMaxMin', timeCut=20, cut=makeCut, straight=False)

    #veto events with large hit in front/back panels
    beamMuonPanelVeto = getCutMod(mycuts.beamMuonPanelVeto, mycuts, 'beamMuonPanelVeto', cut=makeCut, nPECut=0)

    #require # bars in event  < cut
    nBarsCut = getCutMod(mycuts.nBarsCut, mycuts, 'nBarsCut', nBarsCut=4, cut=makeCut)

    #require < nBars within deltaT
    nBarsDeltaTCut = getCutMod(mycuts.nBarsDeltaTCut, mycuts, 'nBarsDeltaTCut', nBarsCut=4, timeCut=100, cut=makeCut)

    #sideband RMS cut
    sidebandRMSCut = getCutMod(mycuts.sidebandRMSCut, mycuts, 'sidebandRMSCut', cutVal=2, cut=makeCut)

    #use first pulse in a channel only
    firstPulseCut = getCutMod(mycuts.firstPulseCut, mycuts, 'firstPulseCut', cut=makeCut)

    #cut out all pulses except bars
    barsCut = getCutMod(mycuts.barCut, mycuts, 'barCut', cut=makeCut)

    #require a hit in front and/or back panel
    frontBackPanelRequired = getCutMod(mycuts.requireFrontBackPanel, mycuts, 'frontBackPanelRequired', cut=makeCut)

    cosmicMuonCut = getCutMod(cosmicMuonCut, mycuts, 'cosmicMuonCut', cut=makeCut)
    cosmicMuonCutHard = getCutMod(cosmicMuonCutHard, mycuts, 'cosmicMuonCutHard', cut=makeCut)

    h_frontPanelHits = r.TH1F('h_frontPanelHits', 'Number of Front Panel Hits;# Panels;Events', 10, 0, 10)
    h_backPanelHits = r.TH1F('h_backPanelHits', 'Number of Back Panel Hits;# Panels;Events', 10, 0, 10)
    h_frontPanelNPE = r.TH1F('h_frontPanelNPE', 'nPE of Front Panel;nPE;# Pulses', 3000, 0, 6e6)
    h_frontPanelArea = r.TH1F('h_frontPanelArea', 'Area of Front;Area;# Pulses', 900, 0, 9e5)
    h_backPanelNPE = r.TH1F('h_backPanelNPE', 'nPE of Back Panel;nPE;# Pulses', 3000, 0, 6e6)
    h_backPanelArea = r.TH1F('h_backPanelArea', 'Area of Back Panel;Area;# Pulses', 900, 0, 9e5)
    h_frontPanelHeight = r.TH1F('h_frontPanelHeight', 'Height of Front Panel;Height;# Pulses', 130, 0, 1300)
    h_backPanelHeight = r.TH1F('h_backPanelHeight', 'Height of Back Panel;Height;# Pulses', 130, 0, 1300)
    h_frontPanelDuration = r.TH1F('h_frontPanelDuration', 'Duration of Front Panel;Duration (ns);# Pulses', 200, 0, 1200)
    h_backPanelDuration = r.TH1F('h_backPanelDuration', 'Duration of Back Panel;Duration (ns);# Pulses', 200, 0, 1200)
    h_frontPanelRiseSamples = r.TH1F('h_frontPanelRiseSamples', 'Rise Samples in Front Panel;Rise Samples;# Pulses', 60, 0, 60)
    h_backPanelRiseSamples = r.TH1F('h_backPanelRiseSamples', 'Rise Samples in Front Panel;Rise Samples;# Pulses', 60, 0, 60)
    h_frontPanelFallSamples = r.TH1F('h_frontPanelFallSamples', 'Fall Samples in Front Panel;Rise Samples;# Pulses', 120, 0, 120)
    h_backPanelFallSamples = r.TH1F('h_backPanelFallSamples', 'Fall Samples in Front Panel;Rise Samples;# Pulses', 120, 0, 120)
    
    h_frontPanelAreaVsHeight = r.TH2F('h_frontPanelAreaVsHeight', 'Area vs Height Front Panel;Area;Height', 900, 0, 9e5, 130, 0, 1300)
    h_backPanelAreaVsHeight = r.TH2F('h_backPanelAreaVsHeight', 'Area vs Height Back Panel;Area;Height', 900, 0, 9e5, 130, 0, 1300)
    h_frontPanelDurationVsHeight = r.TH2F('h_frontPanelDurationVsHeight', 'Duration vs Height Front Panel', 200, 0, 600, 130, 0, 1300)
    h_backPanelDurationVsHeight = r.TH2F('h_backPanelDurationVsHeight', 'Duration vs Height Back Panel', 200, 0, 600, 130, 0, 1300)

    #define milliqan plotter
    myplotter = milliqanPlotter()
    myplotter.dict.clear()


    myplotter.addHistograms(h_frontPanelHits, 'frontHits', 'first')
    myplotter.addHistograms(h_backPanelHits, 'backHits', 'first')
    myplotter.addHistograms(h_frontPanelNPE, 'frontNPE')
    myplotter.addHistograms(h_backPanelNPE, 'backNPE')
    myplotter.addHistograms(h_frontPanelArea, 'frontArea')
    myplotter.addHistograms(h_backPanelArea, 'backArea')
    myplotter.addHistograms(h_frontPanelHeight, 'frontHeight')
    myplotter.addHistograms(h_backPanelHeight, 'backHeight')
    myplotter.addHistograms(h_frontPanelDuration, 'frontDuration')
    myplotter.addHistograms(h_backPanelDuration, 'backDuration')
    myplotter.addHistograms(h_frontPanelRiseSamples, 'frontRiseSamples')
    myplotter.addHistograms(h_backPanelRiseSamples, 'backRiseSamples')
    myplotter.addHistograms(h_frontPanelFallSamples, 'frontFallSamples')
    myplotter.addHistograms(h_backPanelFallSamples, 'backFallSamples')    
    myplotter.addHistograms(h_frontPanelAreaVsHeight, ['frontArea', 'frontHeight'])
    myplotter.addHistograms(h_backPanelAreaVsHeight, ['backArea', 'backHeight'])
    myplotter.addHistograms(h_frontPanelDurationVsHeight, ['frontDuration', 'frontHeight'])
    myplotter.addHistograms(h_backPanelDurationVsHeight, ['backDuration', 'backHeight'])


    
    cutflow = [mycuts.totalEventCounter, 
                mycuts.fullEventCounter, 
                boardMatchCut, 
                pickupCut, 
                firstPulseCut,
                centralTimeCut,
                #cosmicMuonCutHard,
                cosmicMuonCut,
                mycuts.frontBackPanelInfo,
            ]

    for key, value in myplotter.dict.items():
        if value not in cutflow:
            cutflow.append(value)

    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=stepSize, qualityLevel=qualityLevel, max_events=maxEvents, goodRunsList=os.getcwd()+'/goodRunsList.json', sim=sim)

    #run the milliqan processor
    myiterator.run()

    myschedule.cutFlowPlots()

    #save plots
    myplotter.saveHistograms(outputFile)
    print("--------------------------------------------------------")
    print("|\033[1;34m Total run time {}s and luminosity {}pb^-1 \033[0m|".format(runTime, lumi))
    print("--------------------------------------------------------")

    mycuts.getCutflowCounts()