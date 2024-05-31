import os
import ROOT as r
import uproot
import time
import argparse
import pandas as pd
from datetime import datetime
import numpy as np
import json

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
        self.totalEvents = -1
        self.unmatchedEvents = -1
        self.startTime = -1
        self.unmatchedBoards = -1
        self.daqCTime = None
        self.trigCTime = None
        self.matchCTime = None
        self.offlineCTime = None
    
    def __str__(self):
        out = 'run: {0} file: {1}\n\t\
               daqFile: {2}\n\t\
               trigFile: {3}\n\t\
               matchFile: {4}\n\t\
               offlineFile: {5}'.format(self.run, self.file, self.daqFile, self.trigFile, self.matchFile, self.offlineFile)
        return out
        

class fileChecker():
    
    def __init__(self):
        self.min_run = 1022
        self.max_run = 1123
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
                                  'offlineCTime'])
        #self.runInfos.set_index(['run', 'file'], inplace=True)
        
        self.debug = False
        
        self.rawDirs = rawDirectories = ['1000', '1100']
        self.subRawDirs = ['0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']
        
    def parse_args(self):
        parser=argparse.ArgumentParser()
        parser.add_argument("-r", "--rawDir", type=str, default = '/store/user/milliqan/run3/', help="Raw data directory")
        parser.add_argument("-o", "--offlineDir", type=str, default = '/store/user/milliqan/trees/v33/bar/', help="Offline data directory")
        self.args = parser.parse_args(args=[])

    def initializePlots(self):

        bins = self.max_run - self.min_run
        self.h_total = r.TH1F("h_total", "Total Number of Events in Run", bins, self.min_run, self.max_run)
        self.h_unmatched = r.TH1F("h_unmatched", "Number of Unmatched Events in Run", bins, self.min_run, self.max_run)
        self.h_startTimes = r.TH1F("h_startTimes", "Start Times of Runs", bins, self.min_run, self.max_run)
        self.h_boardUnmatched = r.TH1F("h_boardUnmatched", "Number of Boards Unmatched", bins, self.min_run, self.max_run)

        self.c1  = r.TCanvas("c1", "c1", 800,800)
        
        
    def checkOfflineFiles(self, fileList):

        total_unmatched = 0
        for events in uproot.iterate(

            #files
            fileList,

            #branches
            ['runNumber', 'fileNumber', 'boardsMatched'],

            #cut
            #cut="",

            how="zip",

            step_size=1000,

            num_workers=8,

            ):

            unmatchedCut = events[:, "boardsMatched"] == 0
            unmatched = events[unmatchedCut, "boardsMatched"]
            self.h_boardUnmatched.Fill(events[0, 'runNumber'], len(unmatched))
            
            self.runInfos['unmatchedBoards'].loc[(self.runInfos['run'] == events[0, 'runNumber']) & (self.runInfos['file'] == events[0, 'fileNumber'])] += len(unmatched)
    
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
    
    def getOfflineInfo(self):
        #add loc statement to only get those that haven't been updated yet
        rawFiles = self.runInfos[['run', 'file']].loc[self.runInfos['offlineFile'] == None].to_numpy()
        for pair in rawFiles:
            offlineFile = 'MilliQan_Run{0}.{1}_v33_firstPedestals.root'.format(pair[0], pair[1])
            if os.path.exists(self.offlineDir+'/'+offlineFile): 
                self.runInfos['offlineFile'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = offlineFile
                self.runInfos['offlineDir'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = self.offlineDir
                self.runInfos['offlineCTime'].loc[(self.runInfos['run'] == pair[0]) & (self.runInfos['file'] == pair[1])] = datetime.fromtimestamp(os.path.getctime(self.offlineDir+'/'+offlineFile))

    def getRawInfo(self, directory):
        #for directory in rawDirectories:
        #    for sub in rawSubDirectories:
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
            runList = self.runInfos[['rawDir', 'matchFile']].loc[(self.runInfos['run']==run) & (self.runInfos['totalEvents']==-1)].apply(lambda x: '/'.join((x.rawDir, x.matchFile)) if (x.rawDir!=None and x.matchFile!=None) else None, axis=1).values.tolist()
            #print(runList)
            runList = [x+':matchedTrigEvents' for x in runList if x!=None]
            if len(runList) == 0: continue
            self.checkMatchedFiles(runList)
        
    def runCheckOfflineFiles(self):
        #now look at offline files post processing info
        runs = self.runInfos.run.unique()
        for run in runs:
            runList = self.runInfos[['offlineDir', 'offlineFile']].loc[self.runInfos['run']==run & (self.runInfos['unmatchedBoards']==-1)].apply('/'.join, axis=1).tolist()
            runList = [x+':t' for x in runList]
            if len(runList) == 0: continue
            self.checkOfflineFiles(runList)
    
    #function to do all tasks once per directory and update json
    def looper(self, dirs=[], subDirs=[], jsonName='checkMatching.json'):
        if len(dirs)==0 and len(subDirs)==0:
            dirs = self.rawDirs
            subDirs = self.subRawDirs
        for d1 in dirs:
            for d2 in subDirs:
                print("Running over directory {0}/{1}".format(d1, d2))
                self.getRawInfo('{0}/{1}'.format(d1, d2))
                self.getOfflineInfo()
                self.runCheckMatchedFiles()
                self.runCheckOfflineFiles()
                self.saveJson(jsonName)
            
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
    
    myfileChecker = fileChecker()
    myfileChecker.debug = False
    
    myfileChecker.looper()

    myfileChecker.printInfo()

