


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


#################################################################
################ condor function definitions ####################

def getFileList(filelist, job):

    with open(filelist, 'r') as fin:
        data = json.load(fin)

    mylist = data[job]

    return mylist

def extract_tar_file(tar_file='milliqanProcessing.tar.gz'):
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall()

##################################################################

def loadJson(jsonFile):
    fin = open(jsonFile)
    data = json.load(fin)
    lumis = pd.DataFrame(data['data'], columns=data['columns'])
    return lumis


def getRunFile(filename):
    run = filename.split('Run')[1].split('.')[0]
    file = filename.split('.')[1].split('_')[0]
    return [int(run), int(file)]


def getLumiofFileList(filelist):

    inputFiles = [getRunFile(x.split('/')[-1]) for x in filelist]

    #mqLumis = shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', 'mqLumis.json')
    lumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')

    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])

    myfiles = lumis[lumis.apply(lambda row: [int(row['run']), int(row['file'])] in inputFiles, axis=1)]

    totalLumi = myfiles['lumiEst'].sum()

    runTime = getRunTimes(myfiles)

    print("Running over {} files \n total of {} pb^-1 \n total run time {}s".format(len(filelist), totalLumi, runTime))

def getRunTimes(df):

    runTimes = df['stop'] - df['start']

    total_time = runTimes.sum()

    return total_time


if __name__ == "__main__":

    goodRuns = loadJson('goodRunsList.json')
    lumis = loadJson('mqLumis.json')

    #get list of files to look at
    files = []

    beam = False

    if len(sys.argv) <=2:
        mass = 'test'
        charge = 'test'
        job = 0
        filelist = [sys.argv[1]]

    else:
        #get the filelist and job number
        filelist = sys.argv[1]
        job = sys.argv[2]

        #define a file list to run over
        filelist = getFileList(filelist, job)

        mass = filelist[0].split('/')[-1].split('_')[1]
        charge = filelist[0].split('/')[-1].split('_')[-1].split('.')[0]

    SR=1
    outputFile = f'bgCutFlow_signalSim_{mass}_{charge}_{job}.root'
    beam = False
    skim = True
    sim = True
    qualityLevel = 'tight'
    maxEvents = None
    stepSize = 20000
    runTime = 0
    lumi = 0

    print("Running on files {}".format(filelist))

    #find the luminosity of files in filelist
    #getLumiofFileList(filelist)

    #define the necessary branches to run over
    #define the necessary branches to run over
    branches = ['event', 'tTrigger', 'boardsMatched', 'pickupFlag', 'pickupFlagTight', 'fileNumber', 'runNumber', 'type', 'ipulse', 'nPE', 'chan',
                'time_module_calibrated', 'timeFit_module_calibrated', 'row', 'column', 'layer', 'height', 'area', 'npulses', 'sidebandRMS', 'eventWeight',
                'riseSamples', 'fallSamples', 'prePulseMean', 'prePulseRMS', 'sidebandMean', 'duration']


    #define the milliqan cuts object
    mycuts = milliqanCuts()

    #set the directory with milliqan configs
    mycuts.configDir = '/../../configuration/'
    #mycuts.configDir = '/'

    #require pulses are in trigger window
    centralTimeCut = getCutMod(mycuts.centralTime, mycuts, 'centralTimeCut', cut=True)

    #require pulses are not pickup
    #pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', cut=True, tight=True)
    pickupCut = getCutMod(mycuts.pickupCutCustom, mycuts, 'pickupCut', cut=True)
    noiseCut = getCutMod(mycuts.noiseCut, mycuts, 'noiseCut', cut=True)
    darkRateCut = getCutMod(mycuts.darkRateCut, mycuts, 'darkRateCut', cut=True)

    #require that all digitizer boards are matched
    boardMatchCut = getCutMod(mycuts.boardsMatched, mycuts, 'boardMatchCut', cut=True, branches=branches)

    #greater than or equal to one hit per layer
    hitInAllLayers = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'hitInAllLayers', cut=True, multipleHits=True)

    #exactly one hit per layer
    oneHitPerLayer = getCutMod(mycuts.oneHitPerLayerCut, mycuts, 'oneHitPerLayer', cut=True, multipleHits=False)

    #panel veto
    panelVeto = getCutMod(mycuts.panelVeto, mycuts, 'panelVeto', cut=True, nPECut=None)
    #panelVeto = getCutMod(mycuts.panelVetoMod, mycuts, 'panelVeto', cut=True, areaCut=80e3, nPECut=None, panelsAllowed=1)

    #first pulse max
    firstPulseMax = getCutMod(mycuts.firstPulseMax, mycuts, 'firstPulseMax', cut=True)

    #veto events with an early pulse
    vetoEarlyPulse = getCutMod(mycuts.vetoEarlyPulse, mycuts, 'vetoEarlyPulse', cut=True)

    #straight line for max/min
    straightLineMaxMin = getCutMod(mycuts.straightLineCut, mycuts, 'straightLineMaxMin')

    #four in line cut
    straightLineCutMod = getCutMod(mycuts.straightLineCut, mycuts, 'straightLineCutMod', cut=True)

    #npe max-min < 10 cut
    nPEMaxMin = getCutMod(mycuts.nPEMaxMin, mycuts, 'nPEMaxMin', nPERatioCut=20, cut=True, straight=False)
    energyMaxMin = getCutMod(mycuts.energyMaxMin, mycuts, 'energyMaxMin', energyRatioCut=10, cut=True, straight=False)

    nPEMaxCut = getCutMod(mycuts.nPEMaxCut, mycuts, 'nPEMaxCut', nPECut=20, cut=True)
    energyMaxCut2p5 = getCutMod(mycuts.energyMaxCut, mycuts, 'energyMaxCut2p5', energyCut=55, cut=True)

    #time max-min < 15 cut
    timeMaxMinNoCut = getCutMod(mycuts.timeMaxMin, mycuts, 'timeMaxMinPlot', timeCut=20)
    timeMaxMin = getCutMod(mycuts.timeMaxMin, mycuts, 'timeMaxMin', timeCut=20, cut=True, straight=True)

    #veto events with nPE>50 in SR2
    beamMuonPanelVeto50 = getCutMod(mycuts.beamMuonPanelVeto, mycuts, 'beamMuonPanelVeto50', cut=True, nPECut=50)
    beamMuonPanelVeto50NoCut = getCutMod(mycuts.beamMuonPanelVeto, mycuts, 'beamMuonPanelVeto50NoCut', cut=False, nPECut=50)
    
    #veto events with large hit in front/back panels, SR1
    beamMuonPanelVeto = getCutMod(mycuts.beamMuonPanelVeto, mycuts, 'beamMuonPanelVeto', cut=True, nPECut=0)

    #require # bars in event  < cut
    nBarsCut = getCutMod(mycuts.nBarsCut, mycuts, 'nBarsCut', nBarsCut=4, cut=True)
    
    #require < nBars within deltaT
    nBarsDeltaTCut = getCutMod(mycuts.nBarsDeltaTCut, mycuts, 'nBarsDeltaTCut', nBarsCut=4, timeCut=100, cut=True)

    #sideband RMS cut
    sidebandRMSCut = getCutMod(mycuts.sidebandRMSCut, mycuts, 'sidebandRMSCut', cutVal=2, cut=True)

    #use first pulse in a channel only
    firstPulseCut = getCutMod(mycuts.firstPulseCut, mycuts, 'firstPulseCut', cut=True)

    #cut out all pulses except bars
    barsCut = getCutMod(mycuts.barCut, mycuts, 'barCut', cut=True)

    #require a hit in front and/or back panel
    frontBackPanelRequired = getCutMod(mycuts.requireFrontBackPanel, mycuts, 'frontBackPanelRequired', cut=True)

    nPEScaling = getCutMod(mycuts.applyNPEScaling, mycuts, 'nPEScaling', sim=True)
    energyScaling = getCutMod(mycuts.applyEnergyScaling, mycuts, 'energyScaling', sim=True)

    #define histograms
    h_timeDiff1 = r.TH1F('h_timeDiff1', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff2 = r.TH1F('h_timeDiff2', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff3 = r.TH1F('h_timeDiff3', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff4 = r.TH1F('h_timeDiff4', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff5 = r.TH1F('h_timeDiff5', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff6 = r.TH1F('h_timeDiff6', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff7 = r.TH1F('h_timeDiff7', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff8 = r.TH1F('h_timeDiff8', "Layer 3 and 0 Time Difference", 100, -50, 50)
    h_timeDiff9 = r.TH1F('h_timeDiff9', "Layer 3 and 0 Time Difference", 100, -50, 50)

    h_nBars = r.TH1F('h_nBars', "Number of Bars per Event;# Bars;# Events", 64, 0, 64)
    h_nLayersBeforeAllLayers = r.TH1F('h_nLayersBeforeAllLayers', 'Number of Layers Hit Before N Layers Cut;Layers;Events', 5, 0, 5)
    h_nLayersAfterAllLayers = r.TH1F('h_nLayersAfterAllLayers', 'Number of Layers Hit After N Layers Cut;Layers;Events', 5, 0, 5)
    h_nHitsPerLayerBefore = r.TH1F('h_nHitsPerLayerBefore', 'Number of Hits Per Layer Before All Layers Hit Cut;nHits per Layer;Events*Layers', 16, 0, 16)
    h_nHitsPerLayerAfter = r.TH1F('h_nHitsPerLayerAfter', 'Number of Hits Per Layer After All Layers Hit Cut;nHits per Layer;Events*Layers', 16, 0, 16)
    h_nLayersBeforeOneHitPerLayer = r.TH1F('h_nLayersBeforeOneHitPerLayer', 'Number of Layers Hit Before One Hit Per Layer;Layers;Events', 5, 0, 5)
    h_nLayersAfterOneHitPerLayer = r.TH1F('h_nLayersAfterOneHitPerLayer', 'Number of Layers Hit After One Hit Per Layer;Layers;Events', 5, 0, 5)
    h_nBarsBeforeCut = r.TH1F('h_nBarsBeforeCut', 'Number of Bars Before Bar Cut;Bars;Events', 64, 0, 64)
    h_nBarsAfterCut = r.TH1F('h_nBarsAfterCut', 'Number of Bars After Bar Cut;Bars;Events', 64, 0, 64)
    h_nBarsInWindowBefore = r.TH1F('h_nBarsInWindowBefore', 'Number of Bars within Timing Window Before Cut;Bars;Events', 20, 0, 20)
    h_nBarsInWindowAfter = r.TH1F("h_nBarsInWindowAfter", 'Number of Bars Within Timing Window After Cut;Bars;Events', 20, 0, 20)
    h_sidebandsBefore = r.TH1F('h_sidebandsBefore', 'Sideband RMS Before Cut;Sideband RMS;Events', 50, 0, 10)
    h_sidebandsAfter = r.TH1F('h_sidebandsAfter', 'Sideband RMS After Cut;Sideband RMS;Events', 50, 0, 10)
    h_panelNPEBefore = r.TH1F('h_panelNPEBefore', 'nPE in Panels Before Cut;nPE;Panel Hits', 100, 0, 1e3)
    h_panelAreaBefore = r.TH1F('h_panelAreaBefore', 'Area in Panels Before Cut;Area;Panel Hits', 200, 0, 100e3)
    h_panelNPEAfter = r.TH1F('h_panelNPEAfter', 'nPE in Panels After Cut;nPE;Panel Hits', 100, 0, 1e3)
    h_panelAreaAfter = r.TH1F('h_panelAreaAfter', 'Area in Panels After Cut;Area;Panel Hits', 200, 0, 100e3)
    h_panelHitsBefore = r.TH1F('h_panelHitsBefore', 'Number of Panel Hits Before Cut;# Panels;Events', 10, 0, 10)
    h_panelHitsAfter = r.TH1F('h_panelHitsAfter', 'Number of Panel Hits After Cut;# Panels;Events', 10, 0, 10)
    h_frontPanelNPEBefore = r.TH1F('h_frontPanelNPEBefore', 'nPE of Front Panel Before Cut;nPE;# Pulses', 300, 0, 3e3)
    h_frontPanelNPEAfter = r.TH1F('h_frontPanelNPEAfter', 'nPE of Front Panel After Cut;nPE;# Pulses', 300, 0, 3e3)
    h_backPanelNPEBefore = r.TH1F('h_backPanelNPEBefore', 'nPE of Back Panel Before Cut;nPE;# Pulses', 300, 0, 3e3)
    h_backPanelNPEAfter = r.TH1F('h_backPanelNPEAfter', 'nPE of Back Panel After Cut;nPE;# Pulses', 300, 0, 3e3)
    h_straightTimeBefore = r.TH1F('h_straightTimeBefore', 'Pulse Times Before Straight Line Cut;Time;# Pulses', 240, 0, 2400)
    h_straightTimeAfter = r.TH1F('h_straightTimeAfter', 'Pulse Times After Straight Line Cut;Time;# Pulses', 240, 0, 2400)
    h_straightNPEBefore = r.TH1F('h_straightNPEBefore', 'nPE of Pulses Before Straight Line Cut;nPE;# Pulses', 100, 0, 100)
    h_straightNPEAfter = r.TH1F('h_straightNPEAfter', 'nPE of Pulses After Straight Line Cut;nPE; # Pulses', 100, 0, 100)
    h_straightEnergyBefore = r.TH1F('h_straightEnergyBefore', 'Energy Cal of Pulses Before Straight Line Cut;Source Energy/sPE;# Pulses', 100, 0, 100)
    h_straightEnergyAfter = r.TH1F('h_straightEnergyAfter', 'Energy Cal of Pulses After Straight Line Cut;Source Energy/sPE; # Pulses', 100, 0, 100)
    h_straightHeightBefore = r.TH1F('h_straightHeightBefore', 'Height of Pulses Before Straight Line Cut;Height;# Pulses', 1400, 0, 1400)
    h_straightHeightAfter = r.TH1F('h_straightHeightAfter', 'Height of Pulses After Straight Line Cut;Height;# Pulses', 1400, 0, 1400)
    h_straightChannelBefore = r.TH1F('h_straightChannelBefore', 'Channels Before Straight Line Cut;Channel;# Pulses', 80, 0, 80)
    h_straightChannelAfter = r.TH1F('h_straightChannelAfter', 'Channels After Straight Line Cut;Channel; # Pulses', 80, 0, 80)
    h_straightNumPaths = r.TH1F('h_straightNumPaths', "Number of Straight Line Paths in Event;Num Paths;Events", 16, 0, 16)
    h_maxNPEBefore = r.TH1F('h_maxNPEBefore', 'Max NPE in Event Before Cut;Max NPE;Events', 100, 0, 300)
    h_minNPEBefore = r.TH1F('h_minNPEBefore', 'Min NPE in Event Before Cut;Min NPE;Events', 100, 0, 300)
    h_maxNPEAfter = r.TH1F('h_maxNPEAfter', 'Max NPE in Event After Cut;Max NPE;Events', 100, 0, 300)
    h_minNPEAfter = r.TH1F('h_minNPEAfter', 'Min NPE in Event After Cut;Min NPE;Events', 100, 0, 300)
    h_nPEBefore = r.TH2F('h_nPEBefore', 'NPE in Event Before Cut;Min NPE;Max NPE', 100, 0, 100, 100, 0, 100)
    h_nPEAfter = r.TH2F('h_nPEAfter', 'NPE in Event After Cut;Min NPE;Max NPE', 100, 0, 100, 100, 0, 100)
    h_minTimeBefore = r.TH1F('h_minTimeBefore', 'Min Pulse Time Before Cut;Min Time;Events', 1200, 0, 2400)
    h_maxTimeBefore = r.TH1F('h_maxTimeBefore', 'Max Pulse Time Before Cut;Min Time;Events', 1200, 0, 2400)
    h_minTimeAfter = r.TH1F('h_minTimeAfter', 'Min Pulse Time After Cut;Min Time;Events', 1200, 0, 2400)
    h_maxTimeAfter = r.TH1F('h_maxTimeAfter', 'Max Pulse Time After Cut;Min Time;Events', 1200, 0, 2400)
    h_timeBefore = r.TH2F('h_timeBefore', 'Pulse Times Before Cut;Min Time;Max Time', 1200, 0, 2400, 1200, 0, 2400)
    h_timeAfter = r.TH2F('h_timeAfter', 'Pulse Times After Cut;Min Time;Max Time', 1200, 0, 2400, 1200, 0, 2400)
    h_timeDiff = r.TH1F('h_timeDiff', 'Time Difference (Max-Min);Time Diff (ns);Events', 500, 0, 500)
    h_ABCD = r.TH2F('h_ABCD', 'Straight Line vs Time Window Cuts for ABCD;Straight Line Paths;Max-Min Time (ns)', 2, 0, 2, 300, 0, 300)
    h_ABCD2 = r.TH2F('h_ABCD2', 'Max Panel NPE vs N Bars Hit;Max Panel NPE;N Bars Hit', 100, 0, 500, 20, 0, 20)
    h_eventWeights = r.TH1F('h_eventWeights', 'Event Weights', 200, 0, 200)
    h_nPERatio = r.TH1F('h_nPERatio', 'Ratio of Max/Min nPE', 100, 0, 100)
    h_nPEVsTime = r.TH2F('h_nPEVsTime', 'Time vs NPE of Pulses;Time [ns];nPE', 200, 1000, 1400, 100, 0, 300)
    h_energyDeposited = r.TH1F('h_energyDeposited', 'Energy Deposited in Bars;Energy [keV];Pulses', 700, 0, 2800)
    h_nPEDeposited = r.TH1F('h_nPEDeposited', 'nPE Deposited in Bars;NPE;Pulses', 100, 0, 1000)

    h_nPEFrontPanel = r.TH1F('h_nPEFrontPanel', 'NPE Front Panel;NPE;Pulses', 75, 0, 150)
    h_nPEBackPanel = r.TH1F('h_nPEBackPanel', 'NPE Back Panel;NPE;Pulses', 75, 0, 150)
    h_nPEPanels = r.TH2F('h_nPEPanels', 'NPE of Panels;Front Panel NPE;Back Panel NPE', 76, -2, 150, 76, -2, 150)
    h_numPanels = r.TH1F('h_numPanels', 'Number of Front/Back Panels;Panels Hit;Events', 4, 0, 4)

    h_TimeDiffStraight = r.TH1F('h_TimeDiffStraight', 'Max-Min Time Difference Straight Paths', 1200, 0, 2400)
    h_TimeDiffNotStraight = r.TH1F('h_TimeDiffNotStraight', 'Max-Min Time Difference Non Straight Paths', 1200, 0, 2400)
    h_eventWeights = TH1F('h_eventWeights', 'Event Weight', 1, 0, 1)

    #define milliqan plotter
    myplotter = milliqanPlotter()
    myplotter.dict.clear()

    myplotter.addHistograms(h_timeDiff1, 'timeDiff')
    myplotter.addHistograms(h_timeDiff2, 'timeDiff')
    myplotter.addHistograms(h_timeDiff3, 'timeDiff')
    myplotter.addHistograms(h_timeDiff4, 'timeDiff')
    myplotter.addHistograms(h_timeDiff5, 'timeDiff')
    myplotter.addHistograms(h_timeDiff6, 'timeDiff')
    myplotter.addHistograms(h_timeDiff7, 'timeDiff')
    myplotter.addHistograms(h_timeDiff8, 'timeDiff')
    myplotter.addHistograms(h_timeDiff9, 'timeDiff')
    myplotter.addHistograms(h_nBars, 'countNBars', 'first')
    myplotter.addHistograms(h_nLayersBeforeAllLayers, 'nLayers', 'first')
    myplotter.addHistograms(h_nLayersAfterAllLayers, 'nLayers', 'first')
    myplotter.addHistograms(h_nHitsPerLayerBefore, 'nHitsPerLayerBefore')
    myplotter.addHistograms(h_nHitsPerLayerAfter, 'nHitsPerLayerAfter')
    myplotter.addHistograms(h_nLayersBeforeOneHitPerLayer, 'nLayers', 'first')
    myplotter.addHistograms(h_nLayersAfterOneHitPerLayer, 'nLayers', 'first')
    myplotter.addHistograms(h_nBarsBeforeCut, 'countNBars', 'first')
    myplotter.addHistograms(h_nBarsAfterCut, 'countNBars', 'first')
    myplotter.addHistograms(h_panelNPEBefore, 'panelVetoNPEBefore')
    myplotter.addHistograms(h_panelNPEAfter, 'panelVetoNPEAfter')
    myplotter.addHistograms(h_panelHitsBefore, 'panelVetoHitsBefore', 'first')
    myplotter.addHistograms(h_panelHitsAfter, 'panelVetoHitsAfter', 'first')
    myplotter.addHistograms(h_frontPanelNPEBefore, 'frontPanelNPEBefore')
    myplotter.addHistograms(h_frontPanelNPEAfter, 'frontPanelNPEAfter')
    myplotter.addHistograms(h_backPanelNPEBefore, 'backPanelNPEBefore')
    myplotter.addHistograms(h_backPanelNPEAfter, 'backPanelNPEAfter')
    myplotter.addHistograms(h_straightChannelBefore, 'chan')
    myplotter.addHistograms(h_straightChannelAfter, 'chan')
    myplotter.addHistograms(h_straightHeightBefore, 'height')
    myplotter.addHistograms(h_straightHeightAfter, 'height')
    myplotter.addHistograms(h_straightNPEBefore, 'nPE')
    myplotter.addHistograms(h_straightNPEAfter, 'nPE')
    myplotter.addHistograms(h_straightEnergyBefore, 'energyCal')
    myplotter.addHistograms(h_straightEnergyAfter, 'energyCal')
    myplotter.addHistograms(h_straightTimeBefore, 'timeFit_module_calibrated')
    myplotter.addHistograms(h_straightTimeAfter, 'timeFit_module_calibrated')
    myplotter.addHistograms(h_straightNumPaths, 'numStraightPaths')
    myplotter.addHistograms(h_minTimeBefore, 'minTimeBefore')
    myplotter.addHistograms(h_maxTimeBefore, 'maxTimeBefore')
    myplotter.addHistograms(h_minTimeAfter, 'minTimeAfter')
    myplotter.addHistograms(h_maxTimeAfter, 'maxTimeAfter')
    myplotter.addHistograms(h_timeBefore, ['minTimeBefore', 'maxTimeBefore'])
    myplotter.addHistograms(h_timeAfter, ['minTimeAfter', 'maxTimeAfter'])
    myplotter.addHistograms(h_timeDiff, 'timeMaxMinDiff')
    myplotter.addHistograms(h_ABCD, ['straightLineCut', 'timeMaxMinPlotDiff'], 'straightLineCutNew')
    myplotter.addHistograms(h_TimeDiffStraight, 'timeMaxMinPlotDiff', 'straightLineCutNew')
    myplotter.addHistograms(h_TimeDiffNotStraight, 'timeMaxMinPlotDiff', 'straightLineCutNew')
    myplotter.addHistograms(h_nPEVsTime, ['timeFit_module_calibrated', 'nPE'])
    myplotter.addHistograms(h_eventWeights, 'eventWeight', 'weight')
    myplotter.addHistograms(h_energyDeposited, 'barEnergy')
    myplotter.addHistograms(h_nPEDeposited, 'barNPE')
    myplotter.addHistograms(h_nPEFrontPanel, 'frontNPE')
    myplotter.addHistograms(h_nPEBackPanel, 'backNPE')
    myplotter.addHistograms(h_nPEPanels, ['frontNPE', 'backNPE'])
    myplotter.addHistograms(h_numPanels, 'nPanels')

    if SR==2:
        myplotter.addHistograms(h_ABCD2, ['maxPanelNPE', 'countNBars'])

    if SR==1:
        cutflow = [mycuts.totalEventCounter, 
                mycuts.fullEventCounter,
                nPEScaling,
                energyScaling,
                mycuts.timeDiff,
                boardMatchCut, 
                pickupCut, 
                noiseCut, 
                darkRateCut,
                firstPulseCut,
                centralTimeCut,
                panelVeto,                

                mycuts.nLayersCut,
                mycuts.countNBars, 

                myplotter.dict['h_nLayersBeforeAllLayers'],
                hitInAllLayers,

                myplotter.dict['h_nLayersAfterAllLayers'],
                myplotter.dict['h_nHitsPerLayerBefore'],
                myplotter.dict['h_nHitsPerLayerAfter'],

                myplotter.dict['h_nBarsBeforeCut'],
                nBarsCut, #SR1 only
                myplotter.dict['h_nBarsAfterCut'],
               
                beamMuonPanelVeto, #SR1 only

                energyMaxCut2p5, #SR1 only

                myplotter.dict['h_nBars'],

                firstPulseMax,

                vetoEarlyPulse,
                
                energyMaxMin,

                #include versions of these selections w/o cutting to make ABCD plot
                mycuts.straightLineCut, 
                timeMaxMinNoCut,
                myplotter.dict['h_ABCD'],
                myplotter.dict['h_TimeDiffStraight'],
                myplotter.dict['h_TimeDiffNotStraight'],

                myplotter.dict['h_straightTimeBefore'],
                myplotter.dict['h_straightNPEBefore'],
                myplotter.dict['h_straightHeightBefore'],
                myplotter.dict['h_straightChannelBefore'],
                straightLineCutMod,
                myplotter.dict['h_straightTimeAfter'],
                myplotter.dict['h_straightNPEAfter'],
                myplotter.dict['h_straightHeightAfter'],
                myplotter.dict['h_straightChannelAfter'],
                myplotter.dict['h_straightNumPaths'],
                myplotter.dict['h_nPEVsTime'],
                
                timeMaxMin,
                myplotter.dict['h_minTimeBefore'],
                myplotter.dict['h_maxTimeBefore'],
                myplotter.dict['h_minTimeAfter'],
                myplotter.dict['h_maxTimeAfter'],
                mycuts.panelInfo,
            ]

    else:
        cutflow = [mycuts.totalEventCounter, 
                mycuts.fullEventCounter,
                nPEScaling,
                energyScaling,
                mycuts.timeDiff,
                boardMatchCut, 
                pickupCut, 
                firstPulseCut,
                centralTimeCut,
                panelVeto,                

                mycuts.nLayersCut,

                myplotter.dict['h_nLayersBeforeAllLayers'],
                hitInAllLayers,
                myplotter.dict['h_nLayersAfterAllLayers'],
                myplotter.dict['h_nHitsPerLayerBefore'],
                myplotter.dict['h_nHitsPerLayerAfter'],

                frontBackPanelRequired, #SR2 only
               
                sidebandRMSCut,

                firstPulseMax,

                vetoEarlyPulse,
                
                energyMaxMin,

                #include versions of these selections w/o cutting to make ABCD plot
                mycuts.straightLineCut, 
                timeMaxMinNoCut,
                myplotter.dict['h_ABCD'],
                myplotter.dict['h_TimeDiffStraight'],
                myplotter.dict['h_TimeDiffNotStraight'],

                myplotter.dict['h_straightTimeBefore'],
                myplotter.dict['h_straightNPEBefore'],
                myplotter.dict['h_straightHeightBefore'],
                myplotter.dict['h_straightChannelBefore'],
                straightLineCutMod,
                myplotter.dict['h_straightTimeAfter'],
                myplotter.dict['h_straightNPEAfter'],
                myplotter.dict['h_straightHeightAfter'],
                myplotter.dict['h_straightChannelAfter'],
                myplotter.dict['h_straightNumPaths'],
                myplotter.dict['h_nPEVsTime'],

                timeMaxMin,
                myplotter.dict['h_minTimeBefore'],
                myplotter.dict['h_maxTimeBefore'],
                myplotter.dict['h_minTimeAfter'],
                myplotter.dict['h_maxTimeAfter'],

                mycuts.countNBars,
                beamMuonPanelVeto50NoCut, 
                myplotter.dict['h_ABCD2'],
               
                nBarsCut, #move cut here for SR2 only
                beamMuonPanelVeto50, #SR2 only
                mycuts.panelInfo,

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

    myschedule.plotEventWeight()

    #save plots
    myplotter.saveHistograms(outputFile)

    print("--------------------------------------------------------")
    print("|\033[1;34m Total run time {}s and luminosity {}pb^-1 \033[0m|".format(runTime, lumi))
    print("--------------------------------------------------------")

    mycuts.getCutflowCounts()

