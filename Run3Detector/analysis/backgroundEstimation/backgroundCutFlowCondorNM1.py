


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


def runProcessor(cutflow, mycuts, myplotter, branches, step_size, qualityLevel, max_events, sim, outputFile, blindVar):
    #create a schedule of the cuts
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    #print out the schedule
    myschedule.printSchedule()

    #create the milliqan processor object
    myiterator = milliqanProcessor(filelist, branches, myschedule, step_size=stepSize, qualityLevel=qualityLevel, max_events=maxEvents, goodRunsList=os.getcwd()+'/goodRunsList.json', sim=sim)

    #run the milliqan processor
    myiterator.run()

    myschedule.cutFlowPlots(blind=blindVar)

    #save plots
    myplotter.saveHistograms(outputFile)
    print("--------------------------------------------------------")
    print("|\033[1;34m Total run time {}s and luminosity {}pb^-1 \033[0m|".format(runTime, lumi))
    print("--------------------------------------------------------")

    mycuts.getCutflowCounts(blind=blindVar)


@mqCut
def nm1Plots(self, cutName='nm1Cuts'):

    #number of layers hit
    barHits = self.events['layer'][self.events['type']==0]
    nLayers = (
        ak.values_astype(ak.any(barHits==0, axis=1), np.int32) + 
        ak.values_astype(ak.any(barHits==1, axis=1), np.int32) + 
        ak.values_astype(ak.any(barHits==2, axis=1), np.int32) + 
        ak.values_astype(ak.any(barHits==3, axis=1), np.int32)
    )
    _, nLayers = ak.broadcast_arrays(self.events['npulses'], nLayers)
    self.events[cutName+'NLayers'] = nLayers

    #number of bars hit
    nBars = ak.count(self.events['chan'][self.events['type']==0], axis=1)
    _, nBars = ak.broadcast_arrays(self.events['npulses'], nBars)
    self.events[cutName+'NBars'] = nBars

    #number of all hits
    nPulses = ak.count(self.events['chan'], axis=1)
    _, nPulses = ak.broadcast_arrays(self.events['npulses'], nPulses)
    self.events[cutName+'NPulses'] = nPulses    

    #number of front/back panels hit
    npanels = ak.count(self.events['chan'][self.events['type']==1], axis=1)
    _, npanels = ak.broadcast_arrays(self.events['npulses'], npanels)
    self.events[cutName+'NPanels'] = npanels
    self.events[cutName+'PanelNPE'] = self.events['nPE'][self.events['type']==1]

    #number of top/side panels hit
    nsidepanels = ak.count(self.events['chan'][self.events['type']==2], axis=1)
    _, nsidepanels = ak.broadcast_arrays(self.events['npulses'], nsidepanels)
    self.events[cutName+'NSidePanels'] = nsidepanels
    self.events[cutName+'SidePanelNPE'] = self.events['nPE'][self.events['type']==2]
    
    #ratio of max/min nPE
    maxEnergy = ak.max(self.events['energyCal'][self.events['type']==0], axis=1, keepdims=True)
    minEnergy = ak.min(self.events['energyCal'][self.events['type']==0], axis=1, keepdims=True)

    ratio = maxEnergy/minEnergy
    self.events[cutName+'EnergyRatio'] = ratio
    self.events[cutName+'EnergyMax'] = maxEnergy
    self.events[cutName+'EnergyMin'] = minEnergy

    #sideband RMS of channels passing
    sidebandVals = self.events['sidebandRMS']
    channelsHit = self.events['chan']
    sidebandsHit = sidebandVals[channelsHit]
    self.events[cutName+'SidebandRMS'] = sidebandsHit

    #straight line hit
    layer0Row = self.events['row'][(self.events['layer']==0) & (self.events['type']==0)]
    layer0Col = self.events['column'][(self.events['layer']==0) & (self.events['type']==0)]
    layer3Row = self.events['row'][(self.events['layer']==3) & (self.events['type']==0)]
    layer3Col = self.events['column'][(self.events['layer']==3) & (self.events['type']==0)]

    meanRow0 = ak.mean(layer0Row, axis=1, keepdims=True)
    meanCol0 = ak.mean(layer0Col, axis=1, keepdims=True)
    meanRow3 = ak.mean(layer3Row, axis=1, keepdims=True)
    meanCol3 = ak.mean(layer3Col, axis=1, keepdims=True)

    rowDiff = meanRow3 - meanRow0
    colDiff = meanCol3 - meanCol0

    slope = np.sqrt(rowDiff*rowDiff + colDiff*colDiff)

    self.events[cutName+'StraightRowDiff'] = rowDiff
    self.events[cutName+'StraightColDiff'] = colDiff
    self.events[cutName+'StraightSlope'] = slope

    #time Max/min
    maxTime = ak.max(self.events['timeFit_module_calibrated'][self.events['type']==0], axis=1, keepdims=True)
    minTime = ak.min(self.events['timeFit_module_calibrated'][self.events['type']==0], axis=1, keepdims=True)
    timeDiff = maxTime - minTime
    self.events[cutName+'TimeMaxMin'] = timeDiff

    #nBars hit
    nBars = ak.count(self.events['chan'][self.events['type']==0], axis=1)
    self.events[cutName+'NBars'] = nBars

    #max panel nPE
    maxPanelNPE = ak.max(self.events['nPE'][self.events['type']==1], axis=1, keepdims=True)
    self.events[cutName+'MaxPanelNPE'] = maxPanelNPE

if __name__ == "__main__":

    goodRuns = loadJson('goodRunsList.json')
    lumis = loadJson('mqLumis.json')

    #get list of files to look at
    files = []

    beam = False

    blindVar = None
    blind = False

    if blind:
        blindVar = 'energyMaxMin'

    if len(sys.argv) ==2:
        filelist = sys.argv[1]
        mass = '0p01'
        charge = '0p0037'
        job=0
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
                'time_module_calibrated', 'timeFit_module_calibrated', 'row', 'column', 'layer', 'height', 'area', 'npulses', 'sidebandRMS', 'eventWeight']


    #define the milliqan cuts object
    mycuts = milliqanCuts()

    setattr(milliqanCuts, 'nm1Plots', nm1Plots)

    #set the directory with milliqan configs
    #mycuts.configDir = '/../../configuration/'
    mycuts.configDir = '/'

    #require pulses are in trigger window
    centralTimeCut = getCutMod(mycuts.centralTime, mycuts, 'centralTimeCut', cut=True)

    #require pulses are not pickup
    pickupCut = getCutMod(mycuts.pickupCut, mycuts, 'pickupCut', cut=True, tight=True)

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
    energyMaxCut2p5 = getCutMod(mycuts.energyMaxCut, mycuts, 'energyMaxCut2p5', energyCut=2.5, cut=True)

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

    #N-1 plots
    h_nLayers = r.TH1F('h_nLayers', 'Number of Layers', 5, 0, 5)
    h_nBars = r.TH1F('h_nBars', 'Number of Bars Hit;# Bars;Events',64, 0, 64)
    h_frontBackHits = r.TH1F('h_frontBackHits', 'Number of Front/Back Panel Hits;# Hits;Events', 3, 0, 3)
    h_frontBackNPE = r.TH1F('h_frontBackNPE', 'NPE of Front/Back Panel Hits;NPE;Pulses', 200, 0, 600)
    h_nPulses = r.TH1F('h_nPulses', 'Number of Channels w/ Pulses;# Channels;Events', 80, 0, 80)
    h_nPE = r.TH1F('h_nPE', 'NPE of Channels Hit;nPE;Pulses', 100, 0, 400)
    h_energy = r.TH1F('h_energy', 'Energy of Channels Hit;Energy;Pulses',100, 0, 20)
    h_RMS = r.TH1F('h_RMS', 'Sideband RMS of Channels;RMS;Pulses;', 40, 0, 20)
    h_energyRatio = r.TH1F('h_energyRatio', 'Ratio of Max/Min Energy;Ratio;Events', 100, 0, 50)
    h_energyMaxMin = r.TH2F('h_energyMaxMin', 'Energy Max/Min;Min Energy;Max Energy', 100, 0, 100, 100, 0, 100)
    h_pulseTime = r.TH1F('h_pulseTime', 'Time of Pulses;Time [ns];Pulses', 600, 0, 2400)
    h_sidePanels = r.TH1F('h_sidePanels', 'Number of Top/Side Panels Hit', 7, 0, 7)
    h_sidePanelsNPE = r.TH1F('h_sidePanelsNPE', 'NPE in of Top/Side Panels;nPE;Pulses', 100, 0, 100)
    h_nPEvsArea = r.TH2F('h_nPEVsArea', 'NPE vs Area Distribution;nPE;Area [pVs]', 100, 0, 100, 200, 0, 200e3)
    h_nPEvsHeight = r.TH2F('h_nPEVsHeight', 'NPE vs Height Distribution;nPE;Height [mV]', 100, 0, 100, 145, 0, 1450)
    h_straightRowDiff = r.TH1F('h_straightRowDiff', "Row Diff Between Layer 3 and Layer 0;Row Diff;Events", 8, -4, 4)
    h_straightColDiff = r.TH1F('h_straightColDiff', "Col Diff Between Layer 3 and Layer 0;Col Diff;Events", 8, -4, 4)
    h_straightDist = r.TH1F('h_straightDist', "Row/Col Distance Between Layer 3 and Layer 0;#sqrt(#Delta(row)^{2} + #Delta(col)^{2});Events", 8, -4, 4)
    h_timeMaxMin = r.TH1F('h_timeMaxMin', 'Max-Min Time;#DeltaT(max-min) [ns];Events', 500, 0, 500)
    h_nBars = r.TH1F('h_nBars', 'Number of Bars Hit; # Bars Hit;Events', 64, 0, 64)
    h_maxPanelNPE = r.TH1F('h_maxPanelNPE', 'Max NPE in Front/Back Panel;NPE;Events', 250, 0, 500)

    #define milliqan plotter
    myplotter = milliqanPlotter()
    myplotter.dict.clear()

    myplotter.addHistograms(h_ABCD, ['straightLineCutPlot', 'timeMaxMinPlotDiff'], 'straightLineCutNew')
    
    #N-1 Plots:
    myplotter.addHistograms(h_nLayers, 'nm1CutsNLayers', 'first')
    myplotter.addHistograms(h_nBars, 'nm1CutsNBars', 'first')
    myplotter.addHistograms(h_frontBackHits, 'nm1CutsNPanels', 'first')
    myplotter.addHistograms(h_frontBackNPE, 'nm1CutsPanelNPE')
    myplotter.addHistograms(h_nPulses, 'nm1CutsNPulses')
    myplotter.addHistograms(h_nPE, 'nPE')
    myplotter.addHistograms(h_energy, 'energyCal')
    myplotter.addHistograms(h_RMS, 'nm1CutsSidebandRMS')
    myplotter.addHistograms(h_energyRatio, 'nm1CutsEnergyRatio')
    myplotter.addHistograms(h_energyMaxMin, ['nm1CutsEnergyMin', 'nm1CutsEnergyMax'])
    myplotter.addHistograms(h_pulseTime, 'timeFit_module_calibrated')
    myplotter.addHistograms(h_sidePanels, 'nm1CutsNSidePanels', 'first')
    myplotter.addHistograms(h_sidePanelsNPE, 'nm1CutsSidePanelNPE')
    myplotter.addHistograms(h_nPEvsArea, ['nPE', 'area'])
    myplotter.addHistograms(h_nPEvsHeight, ['nPE', 'height'])
    myplotter.addHistograms(h_straightRowDiff, 'nm1CutsStraightRowDiff')
    myplotter.addHistograms(h_straightColDiff, 'nm1CutsStraightColDiff')
    myplotter.addHistograms(h_straightDist, 'nm1CutsStraightSlope')
    myplotter.addHistograms(h_timeMaxMin, 'nm1CutsTimeMaxMin')
    myplotter.addHistograms(h_nBars, 'nm1CutsNBars')
    myplotter.addHistograms(h_maxPanelNPE, 'nm1CutsMaxPanelNPE')

    if SR==2:
        myplotter.addHistograms(h_ABCD2, ['maxPanelNPE', 'countNBars'])

    if SR==1:
        cutflow = [mycuts.totalEventCounter, 
                mycuts.fullEventCounter,
                nPEScaling,
                energyScaling,
                boardMatchCut, 
                pickupCut, 
                firstPulseCut,
                centralTimeCut,
                panelVeto,                

                mycuts.nLayersCut,
                mycuts.countNBars, 

                hitInAllLayers,

                nBarsCut, #SR1 only
               
                beamMuonPanelVeto, #SR1 only

                barsCut,

                energyMaxCut2p5, #SR1 only

                sidebandRMSCut,

                firstPulseMax,

                vetoEarlyPulse,
                
                energyMaxMin,
                
                mycuts.straightLineCut, 

                straightLineCutMod,
                
                timeMaxMin,

                mycuts.nm1Plots
            ]

    else:
        cutflow = [mycuts.totalEventCounter, 
                mycuts.fullEventCounter,
                nPEScaling,
                energyScaling,
                boardMatchCut, 
                pickupCut, 
                firstPulseCut,
                centralTimeCut,
                panelVeto,                
                mycuts.countNBars, 

                mycuts.nLayersCut,

                hitInAllLayers,

                frontBackPanelRequired, #SR2 only
               
                sidebandRMSCut,

                firstPulseMax,

                vetoEarlyPulse,

                energyMaxMin,

                mycuts.straightLineCut, 

                straightLineCutMod,
                   
                timeMaxMin,

                nBarsCut, #move cut here for SR2 only
                beamMuonPanelVeto50, #SR2 only

                mycuts.nm1Plots,

            ]

    for key, value in myplotter.dict.items():
        if value not in cutflow:
            cutflow.append(value)

    if SR==1:
        nm1Cuts = {'allCuts':-1, 'pickupCut':5, 'firstPulse':6, 'centralTiming':7, 'panelVeto':8, 'hitInAllLayers':11, 
               'nBarsCut':12, 'beamMuonPanelVeto':13, 'barsCut':14, 'energyMaxCut2p5':15, 'sidebandRMS':16, 'energyMaxMin': 19, 'straightLineCut':21, 'timeMaxMin':22}
    
    else:
        #nm1Cuts = {'allCuts':-1, 'pickupCut':5, 'firstPulse':6, 'centralTiming':7, 'panelVeto':8, 'hitInAllLayers':11, 'frontBackPanelRequired':12, 'sidebandRMS':13, 'energyMaxMin': 16}
        nm1Cuts = {'allCuts':-1, 'pickupCut':5, 'firstPulse':6, 'centralTiming':7, 'panelVeto':8, 'hitInAllLayers':11, 'frontBackPanelRequired':12, 'sidebandRMS':13, 'energyMaxMin': 16,
                  'straightLineCut':18, 'timeMaxMin':19, 'nBarsCut':20, 'beamMuonPanelVeto':21}

    for icut, (key, val) in enumerate(nm1Cuts.items()):
        #if key != 'allCuts': continue
        myplotter.resetHistograms()
        if val==-1:
            cutflowMod = cutflow
        elif SR ==1 and key=='beamMuonPanelVeto':
            #need to skim barsCut to see effect
            cutflowMod = cutflow[:val] + cutflow[val+1:]
        elif SR == 1 and key=='panelVeto':
            #want to skim bars cut if panvel veto selected
            barCutIndex = nm1Cuts['barsCut']
            cutflowMod = cutflow[:val] + cutflow[val+1:barCutIndex] + cutflow[barCutIndex+1:] 
        else:
            cutflowMod = cutflow[:val] + cutflow[val+1:]
        outputFileMod = outputFile.replace('.root', f'{key}.root')
        runProcessor(cutflowMod, mycuts, myplotter, branches, stepSize, qualityLevel, maxEvents, sim, outputFileMod, blindVar)
    

