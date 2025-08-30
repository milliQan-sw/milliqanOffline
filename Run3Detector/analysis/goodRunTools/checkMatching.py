import os
import ROOT as r
import uproot
import time
import argparse
import pandas as pd
from datetime import datetime
import numpy as np
import json
from IPython.display import display
import awkward as ak
import math

class runInfo:
    
    def __init__(self):
        
        self.run = -1
        self.file = -1
        self.rawDirectory = None
        self.offlineDirectory = None
        self.daqFile = None
        self.trigFile = None
        self.matchFile = None
        self.offlineFile = None
        self.totalEvents = 0
        self.unmatchedEvents = 0
        self.startTime = -1
        self.unmatchedBoards = 0
        self.daqCTime = None
        self.trigCTime = None
        self.matchCTime = None
        self.offlineCTime = None
        self.offlineTrigMatched = 0
        self.triggerConfigPassing = False
        self.singleTriggerPassing = False
        self.activeChannels = np.full(80, False)
        self.runConfig = None
        self.trigger = None
    
    def __str__(self):
        out = 'run: {0} file: {1}\n\t\
               daqFile: {2}\n\t\
               trigFile: {3}\n\t\
               matchFile: {4}\n\t\
               offlineFile: {5}'.format(self.run, self.file, self.daqFile, self.trigFile, self.matchFile, self.offlineFile)
        return out

class runConfig:

    def __init__(self, name, dict):
        self.name = name
        self.startRun = dict['triggerConfig']['startRun']
        self.endRun = dict['triggerConfig']['endRun']
        self.fwVersion = dict['triggerConfig']['fwVersion']
        self.coincidenceTime = dict['triggerConfig']['coincidenceTime']
        self.deadTime = dict['triggerConfig']['deadTime']
        self.trigger = dict['triggerConfig']['trigger']
        self.channels = [ix for ix, x in enumerate(dict['chanMap']) if x[3] != -1]
        
        
rawDirectories = ['1000', '1100', '1200', '1300', '1400']
rawSubDirectories = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='Main directory to check files in', type=str)
    parser.add_argument('-s', '--subdir', help='Subdirectory to check for files', type=str)
    parser.add_argument('-n', '--outputName', help='Name of the output json files', type=str)
    parser.add_argument('-c', '--configDir', help='Path to config dir', type=str, default=os.path.dirname(os.path.abspath(__file__))+'/../../configuration/barConfigs/')
    parser.add_argument('-t', '--tag', help="Version of good run list (format v1p0)", type=str, default='v1p0')
    parser.add_argument('--debug', help='Option to run in debug mode', action='store_true')
    args = parser.parse_args()
    return args

class fileChecker():
    
    def __init__(self, rawDir='/store/user/milliqan/run3/bar/', offlineDir='/store/user/milliqan/trees/v35/bar/', configDir=os.path.dirname(os.path.abspath(__file__))+'/../../configuration/barConfigs/'):
        self.min_run = 1200
        self.max_run = 1300
        self.rawDir = rawDir
        self.offlineDir = offlineDir       
        self.configDir = configDir
            
        self.initializePlots()

        self.daqFiles = {}
        self.trigFiles = {}
        self.matchedFiles = {}
        self.offlineFiles = {}
        
        self.runInfos = pd.DataFrame(columns=['run', 'file', 'rawDir', 'offlineDir', 'daqFile', 'trigFile',
                                  'matchFile', 'offlineFile', 'totalEvents', 'unmatchedEvents', 
                                  'startTime', 'unmatchedBoards', 'daqCTime', 'trigCTime', 'matchCTime',
                                  'offlineCTime', 'offlineTrigMatched', 'triggerConfigPassing', 'singleTriggerPassing', 
                                  'activeChannels', 'runConfig', 'trigger'])
        
        self.debug = False
        
        self.rawDirs = rawDirectories = ['1000', '1100', '1200', '1300', '1400']
        self.subRawDirs = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

        self.configList = self.getConfigList()

        self.vetoedRuns = self.getVetoedRuns()

    def initializePlots(self):

        bins = self.max_run - self.min_run
        self.h_total = r.TH1F("h_total", "Total Number of Events in Run", bins, self.min_run, self.max_run)
        self.h_unmatched = r.TH1F("h_unmatched", "Number of Unmatched Events in Run", bins, self.min_run, self.max_run)
        self.h_startTimes = r.TH1F("h_startTimes", "Start Times of Runs", bins, self.min_run, self.max_run)
        self.h_boardUnmatched = r.TH1F("h_boardUnmatched", "Number of Boards Unmatched", bins, self.min_run, self.max_run)

        self.c1  = r.TCanvas("c1", "c1", 800,800)

    def getConfigList(self):
        configs = {}
        #TODO add ability to do this for slab
        for filename in os.listdir(self.configDir):
            if filename.startswith('configRun') and filename.endswith('.json'):
                fin = open(self.configDir+filename)
                info = json.load(fin)
                configs[filename] = runConfig(filename, info)
                fin.close()
        return configs

    def getTriggerConfig(self, run):
        for cfg in self.configList.values():
            if cfg.startRun > run: continue
            elif cfg.startRun <= run and cfg.endRun >= run:
                return cfg.name
            elif cfg.endRun == -1 and cfg.startRun <= run:
                return cfg.name
        return None

    def checkActiveTriggers(self, trigger):
        t_bin = trigger & 0b0000000001011111 #check only first 8 triggers
        minimumTriggers = t_bin & 0b01011111 #(1011111)
        if minimumTriggers == 95: 
            return True
        else: 
            return False

    def getVetoedRuns(self):

        with open(self.configDir+'vetoedRuns.json', 'r') as file:
            data = json.load(file)
            
        return data['vetoedRuns']
        
    def checkOfflineFiles(self, fileList):

        total_unmatched = 0
        for events in uproot.iterate(

            #files
            fileList,

            #branches
            ['runNumber', 'fileNumber', 'boardsMatched', 'tStartTime', 'tTrigger'],

            how="zip",

            step_size=10000,

            num_workers=8,

            ):

            unmatchedCut = events[:, "boardsMatched"] == 0
            unmatched = events[unmatchedCut, "boardsMatched"]
            self.h_boardUnmatched.Fill(events[0, 'runNumber'], len(unmatched))

            unmatchedEventCut = events[:, "tTrigger"] != -1
            unmatchedEvents = events[unmatchedEventCut, "tTrigger"]
            
            self.runInfos['unmatchedBoards'].loc[(self.runInfos['run'] == events[0, 'runNumber']) & (self.runInfos['file'] == events[0, 'fileNumber'])] += len(unmatched)
            self.runInfos['offlineTrigMatched'].loc[(self.runInfos['run'] == events[0, 'runNumber']) & (self.runInfos['file'] == events[0, 'fileNumber'])] += len(unmatchedEvents)
        
        for events in uproot.iterate(

            #files
            fileList,

            #branches
            ['runNumber', 'fileNumber', 'chan'],

            step_size=10000,

            num_workers=8,

            ):

            for i in range(80):
                chanPulses = ak.any(events[:, 'chan'] == i)
                self.runInfos.at[self.runInfos.index[(self.runInfos['run'] == events[0, 'runNumber']) & (self.runInfos['file'] == events[0, 'fileNumber'])][0], 'activeChannels'][i] = chanPulses

    
    def getRunFile(self, filename):
        runNum = filename.split('Run')[-1].split('.')[0]
        fileNum = filename.split('.')[1].split('_')[0]
        return runNum, fileNum
    
    
    def saveJson(self, name):
        self.runInfos.to_json(name, orient = 'split', compression = 'infer', index = 'true')
        
    def loadJson(self, jsonFile):
        fin = open(jsonFile)
        data = json.load(fin)
        self.runInfos = pd.DataFrame(data['data'], columns=data['columns'])
    
    def checkMatchedFiles(self, fileList):
        total_unmatched = 0
        for events in uproot.iterate(

            #files
            fileList,

            #branches
            ['runNum', 'eventNum', 'trigger', 'startTime'],

            #needs to be 1000 events for file number to be correct
            step_size=1000,

            num_workers=8,
            
        ):

            unmatchedCut = events[:, "trigger"] == -1
            unmatched = events[unmatchedCut, "trigger"]
            self.h_unmatched.Fill(events[0, 'runNum'], len(unmatched))
            self.h_total.Fill(events[0, 'runNum'], len(events))
            thisbin = self.h_startTimes.FindBin(events[0, 'runNum'])
            self.h_startTimes.SetBinContent(thisbin, events[0, 'startTime'])
            
            fileNum = events[0, 'eventNum']/1000 + 1
            
            #ToDo sometimes the first event has no start time, need to check a few other events 
            self.runInfos['startTime'].loc[(self.runInfos['run'] == events[0, 'runNum']) & (self.runInfos['file'] == fileNum)] = events[0, 'startTime'] 
            
            self.runInfos['totalEvents'].loc[(self.runInfos['run'] == events[0, 'runNum']) & (self.runInfos['file'] == fileNum)] += len(events)
            self.runInfos['unmatchedEvents'].loc[(self.runInfos['run'] == events[0, 'runNum']) & (self.runInfos['file'] == fileNum)] += len(unmatched)
    
        #TODO temporary hack to get trigger board meta data, eventually move these checks to offline checks
        fileListMeta = [x.split(':')[0] for x in fileList]
        for file in fileListMeta:
            runNum, fileNum = self.getRunFile(file)
            myfile = r.TFile.Open(file, 'read')
            if not myfile.GetListOfKeys().Contains("MetaData"): 
                if int(runNum) < 1059:
                    self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'triggerConfigPassing'] = True
                    self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'trigger'] = 95
                    self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'singleTriggerPassing'] = False
                continue
            metadata = myfile.Get("MetaData")
            passing = True
            thisTrigger = None
            configName = self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'runConfig']
            configName = configName.iloc[0]
            thisConfig = self.configList[configName]
            for events in metadata:
                #print("Run: {}, FW: {}, Trigger: {}, Coincidence: {}, Dead Time: {}".format(runNum, events.fwVersion, events.trigger, events.coincidenceTime, events.deadTime))
                passing = passing and events.fwVersion >= thisConfig.fwVersion
                passing = passing and events.coincidenceTime == thisConfig.coincidenceTime
                passing = passing and events.deadTime == thisConfig.deadTime

                #current triggers 0xff, 0xef, 0xff, 0xff, 0x3c, 0x01, 0x00, 0xc0
                activeLVDS = (events.channelMask0 & 0xff) == 0xff
                activeLVDS = ((events.channelMask1 & 0xef) == 0xef) and activeLVDS
                activeLVDS = ((events.channelMask2 & 0xff) == 0xff) and activeLVDS
                activeLVDS = ((events.channelMask3 & 0xff) == 0xff) and activeLVDS
                activeLVDS = ((events.channelMask4 & 0x3c) == 0x3c) and activeLVDS
                activeLVDS = ((events.channelMask5 & 0x01) == 0x01) and activeLVDS
                activeLVDS = ((events.channelMask6 & 0x00) == 0x00) and activeLVDS
                activeLVDS = ((events.channelMask7 & 0xc0) == 0xc0) and activeLVDS

                passing = passing and activeLVDS

                singleTrigger = False if events.trigger == 0 else (math.ceil(math.log10(events.trigger)/math.log10(2)) == math.floor(math.log10(events.trigger)/math.log10(2)))
                #print("Trigger:", events.trigger, "Single Trigger Bit:", singleTrigger, "Passing", passing)
                singlePass = passing and singleTrigger

                passing = passing and self.checkActiveTriggers(events.trigger)

                thisTrigger = events.trigger

            self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'triggerConfigPassing'] = passing
            self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'trigger'] = thisTrigger
            self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'singleTriggerPassing'] = singlePass

    def getOfflineInfo(self):

        print("Getting Offline Info...")
        #add loc statement to only get those that haven't been updated yet
        rawFiles = self.runInfos[['run', 'file']].loc[~pd.notnull(self.runInfos['offlineFile'])].to_numpy()
        for pair in rawFiles:
            thisConfig = self.getTriggerConfig(pair[0])
            print("Setting run config", thisConfig, pair)
            self.runInfos['runConfig'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = thisConfig

            subdir = int(math.floor(pair[0] / 100.0)) * 100
            offlineFile = '{0}/MilliQan_Run{1}.{2}_v35.root'.format(subdir, pair[0], pair[1])
            if os.path.exists(self.offlineDir+'/'+offlineFile): 
                self.runInfos['offlineFile'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = offlineFile
                self.runInfos['offlineDir'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = self.offlineDir
                self.runInfos['offlineCTime'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = datetime.fromtimestamp(os.path.getctime(self.offlineDir+'/'+offlineFile))
            else:
                print("File {0} does not exist".format(self.offlineDir+'/'+offlineFile))

    def getRawInfo(self, dir):
        print("Getting Raw Info...")
        if not isinstance(dir, dict):
            fullPath = self.rawDir+dir
            if not os.path.isdir(fullPath): 
                print("Directory {0} does not exist, skipping...".format(fullPath))
                return
            dir = {}
            files = os.listdir(fullPath)
            dir[fullPath] =files

        for idir, (fullPath, files) in enumerate(dir.items()):
            for filename in files:
                if not filename.endswith('.root'): continue
                if not filename.startswith('MilliQan'): continue
                if self.debug and len(self.runInfos) > 100: break
                print("File", filename, "Path", fullPath)
                thisRun = runInfo()
                runNum, fileNum = self.getRunFile(filename)
                thisRun.run = int(runNum)
                thisRun.file = int(fileNum)
                thisRun.daqFile = filename
                thisRun.rawDir = fullPath
                thisRun.daqCTime = datetime.fromtimestamp(os.path.getctime(fullPath+'/'+filename))
                trigName = "TriggerBoard_Run{0}.{1}.root".format(runNum, fileNum)
                matchName = "MatchedEvents_Run{0}.{1}_rematch.root".format(runNum, fileNum)
                if os.path.exists(fullPath+'/'+trigName): 
                    thisRun.trigFile = trigName
                    thisRun.trigCTime = datetime.fromtimestamp(os.path.getctime(fullPath+'/'+trigName))
                if os.path.exists(fullPath+'/'+matchName): 
                    thisRun.matchFile = matchName
                    thisRun.matchCTime = datetime.fromtimestamp(os.path.getctime(fullPath+'/'+matchName))

                self.runInfos.loc[len(self.runInfos.index)] = thisRun.__dict__
                            
    def runCheckMatchedFiles(self):
        print("Checking Matched Files...")
        runs = self.runInfos.run.unique()
        for run in runs:
            runList = self.runInfos[['rawDir', 'matchFile']].loc[(self.runInfos['run']==run) & (self.runInfos['totalEvents']==0)].apply(lambda x: '/'.join((x.rawDir, x.matchFile)) if (x.rawDir!=None and x.matchFile!=None) else None, axis=1).values.tolist()
            runList = [x+':matchedTrigEvents' for x in runList if x!=None]
            if len(runList) == 0: continue
            self.checkMatchedFiles(runList)
        
    def runCheckOfflineFiles(self):
        print("Checking Offline Files...")
        #now look at offline files post processing info
        runs = self.runInfos.run.unique()
        for run in runs:
            runList = self.runInfos[['offlineDir', 'offlineFile']].loc[(self.runInfos['run']==run) & (self.runInfos['unmatchedBoards']==0)].apply(lambda x: '/'.join((x.offlineDir, x.offlineFile)) if (x.offlineDir!=None and x.offlineFile!=None) else None, axis=1).values.tolist()
            runList = [x+':t' for x in runList if x!=None]
            if len(runList) == 0: continue
            self.checkOfflineFiles(runList)
    
    #function to do all tasks once per directory and update json
    def looper(self, dirs=[], subDirs=[], jsonName='checkMatching.json'):
        if len(dirs)==0:
            dirs = self.rawDirs
        if len(subDirs)==0:
            subDirs = self.subRawDirs
        for d1 in dirs:
            for d2 in subDirs:
                print("Running over directory {0}/{1}".format(d1, d2))
                self.getRawInfo('{0}/{1}'.format(d1, d2))
                self.getOfflineInfo()
                self.runCheckMatchedFiles()
                self.runCheckOfflineFiles()
                self.finalChecks()
                self.saveJson(jsonName)

    def updateRunList(self, startingDir=None, startingFile=None, checkTrigs=True, checkOffline=True):
        print("Updating run lists")
        filesToProcess = self.getFilesToProcess(startingDir, startingFile, checkTrigs, checkOffline)
        #print(filesToProcess)
        '''for id, (directory, files) in enumerate(filesToProcess.items()):
            print("There are {} total directories to process".format(len(filesToProcess)))'''
        self.getRawInfo(filesToProcess)
        self.getOfflineInfo()
        self.runCheckMatchedFiles()
        self.runCheckOfflineFiles()
        self.finalChecks()

    def getFilesToProcess(self, lastRun=None, lastFile=None, checkTrigs=True, checkOffline=True):

        filesToProcess = {}

        prevFile = pd.read_json(self.outputFile, orient = 'split', compression = 'infer')

        #this block gets all raw files that have yet to be added to the run list
        if lastRun is None and lastFile is None:
            lastRun, lastFile = self.getLastUpdate(prevFile)

        startingDir0 = math.floor(lastRun/100)*100
        startingDir1 = math.floor((lastRun-startingDir0)/10)
        
        startingDir = '{}{}/000{}'.format(self.rawDir, startingDir0, startingDir1)
        
        while(os.path.isdir(startingDir)):
            thisFileList = []
            for filename in os.listdir(startingDir):
                if not filename.startswith('MilliQan'): continue
                if not filename.endswith('.root'): continue
                runNum, fileNum = self.getRunFile(filename)
                runNum = int(runNum)
                fileNum = int(fileNum)
                if (runNum < lastRun): continue
                if (runNum == lastRun and fileNum <= lastFile): continue
                thisFileList.append(filename)
            filesToProcess[startingDir] = thisFileList
            
            if startingDir1 == 9:
                startingDir0+=100
                startingDir1 = 0
            else:
                startingDir1+=1
            startingDir = '{}{}/000{}'.format(self.rawDir, startingDir0, str(startingDir1))

        #this block checks for any files that have not been matched
        if checkTrigs:
            unmatched = prevFile[pd.isnull(prevFile['matchFile'])]
            unmatched = unmatched[['rawDir', 'daqFile']]

        #this block checks for files that have not had offline files produced (or offline files are unmatched)
        if checkOffline:
            missingOffline = prevFile[pd.isnull(prevFile['offlineFile'])]
            missingOffline = missingOffline[['rawDir', 'daqFile']]

            unmatchedOffline = prevFile[prevFile['OfflineFilesTrigMatched']==False]
            unmatchedOffline = unmatchedOffline[['rawDir', 'daqFile']]

            reprocessOffline = pd.concat((missingOffline, unmatchedOffline), ignore_index=True)

        if checkOffline and checkTrigs:
            reprocess = pd.concat((unmatched, reprocessOffline), ignore_index=True)
        elif checkTrigs:
            reprocess = unmatched
        elif checkOffline:
            reprocess = reprocessOffline
        else:
            return filesToProcess

        for index, row in reprocess.iterrows():
            if row['rawDir'] in filesToProcess:
                filesToProcess[row['rawDir']].append(row['daqFile'])
            else:
                filesToProcess[row['rawDir']] = [row['daqFile']]

        return filesToProcess

    #instead of finding the last update need to get the last entry (raw) and add any new files to processing list
    #also need to add any files missing matching files
    #also need to add any files missing offline files or non trig matched offline files
    def getLastUpdate(self, df):
        lastProcess = df.tail(1)
        lastRun = lastProcess['run'].values[0]
        lastFile = lastProcess['file'].values[0]
        return lastRun, lastFile

    def finalChecks(self):

        print("Running Final Checks...")
        self.runInfos['daqCTime'] = pd.to_datetime(self.runInfos['daqCTime'])
        self.runInfos['trigCTime'] = pd.to_datetime(self.runInfos['trigCTime'])
        self.runInfos['matchCTime'] = pd.to_datetime(self.runInfos['matchCTime'])
        self.runInfos['offlineCTime'] = pd.to_datetime(self.runInfos['offlineCTime'])

        self.runInfos['TriggersMatched'] = self.runInfos['unmatchedEvents'].apply(lambda x: True if x < 10 else False)
        self.runInfos['OfflineFilesTrigMatched'] = self.runInfos.apply(lambda x: True if (x['totalEvents'] > 0 and (x['offlineTrigMatched'] / x['totalEvents']) > 0.95) else False, axis=1)
        self.runInfos['passBoardMatching'] = self.runInfos.apply(lambda x: True if (x['totalEvents'] > 0 and (x['unmatchedBoards'] / x['totalEvents']) < 0.05) else False, axis=1)
        self.runInfos['passActiveChannels'] = self.runInfos.apply(lambda x: False if np.any(x['activeChannels'][self.configList[x['runConfig']].channels]==False) else True, axis=1)
        self.runInfos['inactiveChannels'] = self.runInfos.apply(lambda x: np.intersect1d(np.where(x['activeChannels']==False), self.configList[x['runConfig']].channels), axis=1)
        self.runInfos['lvdsSwapVeto'] = self.runInfos.apply(lambda x: True if ((x['daqCTime'] >= datetime(2023, 7, 6)) & (x['daqCTime'] <= datetime(2023, 11, 10))) else False, axis=1)
        self.runInfos['vetoRunManual'] = self.runInfos.apply(lambda x: True if (x['run'] in self.vetoedRuns) else False, axis=1)

        self.runInfos['goodRunLoose'] = (self.runInfos['passBoardMatching']) & \
                                        (self.runInfos['triggerConfigPassing']) & \
                                        (self.runInfos['inactiveChannels'].str.len() <= 2) & \
                                        (~self.runInfos['vetoRunManual'])
        self.runInfos['goodRunMedium'] = (self.runInfos['goodRunLoose']) & (self.runInfos['passActiveChannels']) & (~self.runInfos['lvdsSwapVeto'])
        self.runInfos['goodRunTight'] = (self.runInfos['goodRunMedium']) & (self.runInfos['TriggersMatched']) & (self.runInfos['OfflineFilesTrigMatched'])

        self.runInfos['goodSingleTrigger'] = (self.runInfos['TriggersMatched']) & \
                                    (self.runInfos['passBoardMatching']) & \
                                    (self.runInfos['singleTriggerPassing']) & \
                                    (self.runInfos['OfflineFilesTrigMatched']) & \
                                    (~self.runInfos['vetoRunManual'])

        self.runInfos['daqCTime'] = self.runInfos['daqCTime'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isnull(x) else None)
        self.runInfos['trigCTime'] = self.runInfos['trigCTime'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isnull(x) else None)
        self.runInfos['matchCTime'] = self.runInfos['matchCTime'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isnull(x) else None)
        self.runInfos['offlineCTime'] = self.runInfos['offlineCTime'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if not pd.isnull(x) else None)

    def makeGoodRunList(self, update=False, outName='goodRunList.json', tag='v1p0'):
                
        if update:
            outName = '/eos/experiment/milliqan/Configs/goodRunsList.json'
            checksName = '/eos/experiment/milliqan/Configs/checksMerged.json'

            goodRuns = self.runInfos[['run', 'file', 'goodRunLoose', 'goodRunMedium', 'goodRunTight', 'goodSingleTrigger']].copy(deep=True)
            goodRuns = goodRuns.drop(goodRuns.loc[(goodRuns['goodRunLoose']==False) & (goodRuns['goodSingleTrigger']==False)].index)
            goodRuns['tag'] = tag

            if os.path.exists(outName):
                goodRunList = pd.read_json(outName, orient='split')
                goodRuns = pd.concat([goodRunList, goodRuns], ignore_index=True)
                goodRuns = goodRuns.drop_duplicates(subset=['run', 'file'], keep='last')

                goodRuns = goodRuns.sort_values(by=['run', 'file'])

                goodRuns.to_json('goodRunsListUpdate.json', orient = 'split', compression = 'infer', index = 'true')
                if not self.debug: os.system('rsync -rzh goodRunsListUpdate.json {}'.format(outName))

            else:
                print("Error cannot access output file {}".format(outName))

            if os.path.exists(checksName):
                checks = pd.read_json(checksName, orient='split')
                checksUpdate = pd.concat([checks, self.runInfos], ignore_index=True)
                checksUpdate = checksUpdate.drop_duplicates(subset=['run', 'file'], keep='last')

                checksUpdate = checksUpdate.sort_values(by=['run', 'file'])

                checksUpdate.to_json('checksMergedUpdate.json', orient = 'split', compression = 'infer', index = 'true')
                if not self.debug: os.system('rsync -rzh checksMergedUpdate.json {}'.format(checksName))
            else:
                print("Error cannot access output file {}".format(checksName))

        else:
            goodRuns = self.runInfos[['run', 'file', 'goodRunLoose', 'goodRunMedium', 'goodRunTight', 'goodSingleTrigger']].copy(deep=True)

            #criteria for good runs
            goodRuns = goodRuns.drop(goodRuns.loc[(goodRuns['goodRunLoose']==False) & (goodRuns['goodSingleTrigger']==False)].index)
            
            goodRuns['tag'] = tag
            
            if os.path.exists(outName):
                goodRunList = pd.read_json(outName, orient='split')
                goodRuns = pd.concat([goodRunList, goodRuns])
                goodRuns = goodRuns.drop_duplicates(subset=['run', 'file'], keep='last')

            goodRuns.to_json(outName, orient = 'split', compression = 'infer', index = 'true')

    def customStyle(self, s):
        colors = ['background-color: white']*len(s)
        if s.unmatchedEvents > 10:
            color = 'yellow'
            if s.unmatchedEvents > 100: color = 'red'
            colors[s.keys().get_loc('unmatchedEvents')] = 'background-color: %s' % color
        if s.unmatchedBoards > 5:
            color = 'yellow'
            if s.unmatchedBoards > 50: color = 'red'
            colors[s.keys().get_loc('unmatchedBoards')] = 'background-color: %s' % color
        if s.startTime == -1:
            colors[s.keys().get_loc('startTime')] = 'background-color: red'    
        if s.trigFile == '':
            colors[s.keys().get_loc('trigFile')] = 'background-color: red'
        if s.matchFile == '':
            colors[s.keys().get_loc('matchFile')] = 'background-color: red'
        if s.offlineFile == '':
            colors[s.keys().get_loc('offlineFile')] = 'background-color: red'

        return colors

    def printInfo(self):
        display(self.runInfos.style.apply(self.customStyle, axis=1))
        
if __name__ == "__main__":

    r.gROOT.SetBatch(1)

    args = parse_args()

    goodRunListName = ''
    jsonName = ''

    update=False

    if not isinstance(args.dir, list): args.dir = [args.dir]
    if not isinstance(args.subdir, list): args.subdir = [args.subdir]

    if len(args.dir) > 1 or len(args.subdir) > 1:
        if not args.outputName:
            print("Please provide a name for the output files using the -n option \n\t files will be called checks_<name>.json and goodRuns_<name>.json")
            sys.exit(1)
        else:
            goodRunListName = 'goodRuns_{}.json'.format(args.outputName)
            jsonName = 'checks_{}.json'.format(args.outputName)
    else:
        jsonName = 'checks_{}_{}.json'.format(args.dir[0], args.subdir[0])
        goodRunListName = 'goodRuns_{}_{}.json'.format(args.dir[0], args.subdir[0])

    if not jsonName.endswith('.json'): jsonName += '.json'
    if not goodRunListName.endswith('.json'): goodRunListName += '.json'

    if update:
        print("Updating the good runs list")

        os.system('~/accessEOS.sh')
        jsonName = 'checksMatchedUpdate.json'
        goodRunListName = 'goodRunListUpdate.json'
        myfileChecker = fileChecker()
        myfileChecker.outputFile = '/eos/experiment/milliqan/Configs/checksMerged.json'
        myfileChecker.debug = False
        myfileChecker.updateRunList(startingDir=None, startingFile=None, checkTrigs=False, checkOffline=False)
        myfileChecker.makeGoodRunList(update=True, tag=args.tag)

    else:
        print("Running on", args.dir, args.subdir)

        myfileChecker = fileChecker(configDir=args.configDir)
        
        myfileChecker.debug = args.debug
        
        myfileChecker.looper(dirs=args.dir, subDirs=args.subdir, jsonName=jsonName)

        myfileChecker.printInfo()
        
        myfileChecker.makeGoodRunList(outName=goodRunListName, tag=args.tag)
