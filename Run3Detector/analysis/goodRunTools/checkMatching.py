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
        self.activeChannels = np.full(80, False)
    
    def __str__(self):
        out = 'run: {0} file: {1}\n\t\
               daqFile: {2}\n\t\
               trigFile: {3}\n\t\
               matchFile: {4}\n\t\
               offlineFile: {5}'.format(self.run, self.file, self.daqFile, self.trigFile, self.matchFile, self.offlineFile)
        return out
        
        
rawDirectories = ['1000', '1100', '1200', '1300', '1400']
rawSubDirectories = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

usedChannels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                21, 22, 23, 26, 27, 28, 29, 30, 
                31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                61, 62, 63, 68, 69, 70, 
                71, 72, 73, 74, 75, 78, 79]

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-d', "--dir", help='Main directory to check files in', type=str, required=True)
    parser.add_argument('-s', '--subdir', help='Subdirectory to check for files', type=str, required=True)
    parser.add_argument('-n', '--outputName', help='Name of the output json files', type=str)
    parser.add_argument('--debug', help='Option to run in debug mode', action='store_true')
    args = parser.parse_args()
    return args

class fileChecker():
    
    def __init__(self):
        self.min_run = 1200
        self.max_run = 1300
        self.rawDir = ''
        self.offlineDir = ''        
        
        self.parse_args()
        if self.args.rawDir: self.rawDir = self.args.rawDir
        if self.args.offlineDir: self.offlineDir = self.args.offlineDir
            
        self.initializePlots()

        self.daqFiles = {}
        self.trigFiles = {}
        self.matchedFiles = {}
        self.offlineFiles = {}
        
        self.runInfos = pd.DataFrame(columns=['run', 'file', 'rawDir', 'offlineDir', 'daqFile', 'trigFile',
                                  'matchFile', 'offlineFile', 'totalEvents', 'unmatchedEvents', 
                                  'startTime', 'unmatchedBoards', 'daqCTime', 'trigCTime', 'matchCTime',
                                  'offlineCTime', 'offlineTrigMatched', 'triggerConfigPassing', 'activeChannels'])
        
        self.debug = False
        
        self.rawDirs = rawDirectories = ['1000', '1100', '1200', '1300', '1400']
        self.subRawDirs = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']
        
    def parse_args(self):
        parser=argparse.ArgumentParser()
        parser.add_argument("-r", "--rawDir", type=str, default = '/store/user/milliqan/run3/bar/', help="Raw data directory")
        parser.add_argument("-o", "--offlineDir", type=str, default = '/store/user/milliqan/trees/v34/', help="Offline data directory")
        self.args = parser.parse_args(args=[])

    def initializePlots(self):

        bins = self.max_run - self.min_run
        self.h_total = r.TH1F("h_total", "Total Number of Events in Run", bins, self.min_run, self.max_run)
        self.h_unmatched = r.TH1F("h_unmatched", "Number of Unmatched Events in Run", bins, self.min_run, self.max_run)
        self.h_startTimes = r.TH1F("h_startTimes", "Start Times of Runs", bins, self.min_run, self.max_run)
        self.h_boardUnmatched = r.TH1F("h_boardUnmatched", "Number of Boards Unmatched", bins, self.min_run, self.max_run)

        self.c1  = r.TCanvas("c1", "c1", 800,800)

    def checkActiveTriggers(self, trigger):
        t_bin = trigger & 0b0000000001011111 #check only first 8 triggers
        minimumTriggers = t_bin & 0b01011111 #(1011111)
        if minimumTriggers == 95: 
            return True
        else: 
            return False
        
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
            step_size=10000,

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
            #self.runInfos['startTime'].loc[(self.runInfos['run'] == events[0, 'runNum']) & (self.runInfos['file'] == fileNum)] = events[0, 'startTime']
            
            self.runInfos['totalEvents'].loc[(self.runInfos['run'] == events[0, 'runNum']) & (self.runInfos['file'] == fileNum)] += len(events)
            self.runInfos['unmatchedEvents'].loc[(self.runInfos['run'] == events[0, 'runNum']) & (self.runInfos['file'] == fileNum)] += len(unmatched)
    
        #TODO temporary hack to get trigger board meta data, eventually move these checks to offline checks
        fileListMeta = [x.split(':')[0] for x in fileList]

        for file in fileListMeta:
            myfile = r.TFile.Open(file, 'read')
            metadata = myfile.Get("MetaData")
            passing = True
            runNum, fileNum = self.getRunFile(file)
            for events in metadata:
                passing = passing and events.fwVersion >= 11
                passing = passing and self.checkActiveTriggers(events.trigger)
                passing = passing and (events.coincidenceTime == 10 or events.coincidenceTime == 20) #This also changed
                passing = passing and events.deadTime >= 100 #TODO changed to 142 in later runs
            self.runInfos.loc[(self.runInfos['run'] == int(runNum)) & (self.runInfos['file'] == int(fileNum)), 'triggerConfigPassing'] = passing
    
    def getOfflineInfo(self):
        #add loc statement to only get those that haven't been updated yet
        rawFiles = self.runInfos[['run', 'file']].loc[~pd.notnull(self.runInfos['offlineFile'])].to_numpy()
        for pair in rawFiles:
            offlineFile = 'MilliQan_Run{0}.{1}_v34.root'.format(pair[0], pair[1])
            if os.path.exists(self.offlineDir+'/'+offlineFile): 
                self.runInfos['offlineFile'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = offlineFile
                self.runInfos['offlineDir'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = self.offlineDir
                self.runInfos['offlineCTime'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = datetime.fromtimestamp(os.path.getctime(self.offlineDir+'/'+offlineFile))
            else:
                print("File {0} does not exist".format(self.offlineDir+'/'+offlineFile))

    def getRawInfo(self, directory):
        fullPath = self.rawDir+directory
        if not os.path.isdir(fullPath): 
            print("Directory {0} does not exist, skipping...".format(fullPath))
            return
        for ifile, filename in enumerate(os.listdir(fullPath)):
            if not filename.endswith('.root'): continue
            if not filename.startswith('MilliQan'): continue
            if self.debug and len(self.runInfos) > 10: break

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
        runs = self.runInfos.run.unique()
        for run in runs:
            runList = self.runInfos[['rawDir', 'matchFile']].loc[(self.runInfos['run']==run) & (self.runInfos['totalEvents']==0)].apply(lambda x: '/'.join((x.rawDir, x.matchFile)) if (x.rawDir!=None and x.matchFile!=None) else None, axis=1).values.tolist()
            runList = [x+':matchedTrigEvents' for x in runList if x!=None]
            if len(runList) == 0: continue
            self.checkMatchedFiles(runList)
        
    def runCheckOfflineFiles(self):
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

    def finalChecks(self):

        self.runInfos['TriggersMatched'] = self.runInfos['unmatchedEvents'].apply(lambda x: True if x < 10 else False)
        self.runInfos['OfflineFilesTrigMatched'] = self.runInfos.apply(lambda x: True if (x['totalEvents'] > 0 and (x['offlineTrigMatched'] / x['totalEvents']) > 0.99) else False, axis=1)
        self.runInfos['passBoardMatching'] = self.runInfos.apply(lambda x: True if (x['totalEvents'] > 0 and (x['unmatchedBoards'] / x['totalEvents']) < 0.01) else False, axis=1)
        self.runInfos['passActiveChannels'] = self.runInfos.apply(lambda x: False if np.any(x['activeChannels'][usedChannels]==False) else True, axis=1)
        self.runInfos['inactiveChannels'] = self.runInfos.apply(lambda x: np.intersect1d(np.where(x['activeChannels']==False), usedChannels), axis=1)

        self.runInfos['goodRuns'] = self.runInfos['TriggersMatched'] & self.runInfos['OfflineFilesTrigMatched'] & \
                                    self.runInfos['passBoardMatching'] & self.runInfos['triggerConfigPassing'] #& \
                                    #self.runInfos['passActiveChannels'] #remove condition for now to create era appropriate missing channels
    def makeGoodRunList(self, outName='goodRunList.json'):
                
        goodRuns = self.runInfos

        #criteria for good runs
        goodRuns = goodRuns.drop(goodRuns.loc[goodRuns['goodRuns']==False].index)
        
        goodRuns = goodRuns[['run', 'file']]
        
        if os.path.exists(outName):
            goodRunList = pd.read_json(outName, orient='split')
            goodRuns = pd.concat([goodRunList, goodRuns])
            goodRuns.drop_duplicates()

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
    
    myfileChecker = fileChecker()
    
    myfileChecker.debug = args.debug
    
    myfileChecker.looper(dirs=args.dir, subDirs=args.subdir, jsonName=jsonName)

    myfileChecker.printInfo()
    
    myfileChecker.makeGoodRunList(outName=goodRunListName)
