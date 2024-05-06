import os
import pandas as pd
import ROOT as r
from datetime import datetime
import matplotlib.pyplot as plt
import math

#luminosity is recorded in inverse ub
#download lumi csv file from https://cmsoms.cern.ch/

class lumiDict:
    
    def __init__(self):
        
        self.run = -1
        self.file = -1
        self.lumis = None
        self.fill = None
        self.beam = None
        self.beamInRun = None
        self.dir = None
        self.filename = None
        self.start = None
        self.stop = None

class mqLumiList():
    
    def __init__(self):
        self.lumi_csv = ''
        self.rawPath = '/store/user/milliqan/run3/bar/'
        self.outputFile = '/eos/home-m/micarrig/MilliQanFiles/Configs/mqLumis.json'
        self.rawLumis = 'Run3_2024Lumis.csv'
        self.mqLumis = pd.DataFrame(columns=['run', 'file', 'lumis', 'fill', 'beam', 'beamInRun', 'dir', 'filename', 'start', 'stop'])
        self.debug = False
        
    def looper(self):
        rawDirectories = ['1000', '1100', '1200', '1300', '1400']
        rawSubDirectories = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

        for i, d1 in enumerate(rawDirectories):
            for j, d2 in enumerate(rawSubDirectories):
                if self.debug and j > 0: return
                if not os.path.exists(self.rawPath+'/'+d1+'/'+d2): 
                    print("Directory: ", self.rawPath+'/'+d1+'/'+d2, "does not exist")
                    continue
                print("Running over directory {}/{}/{}".format(self.rawPath, d1, d2))
                self.initializeDataframe('{0}/{1}'.format(d1, d2))
                self.setFileTimes()
                self.setMQLumis()
                if not self.debug: self.saveJson()
                else: self.saveJson(name='mqLumisDebug.json')

    def updateLumis(self):
        print("updating the lumi list")
        filesToProcess = self.getFilesToProcess()
        for directory, files in filesToProcess.items():
            print("update lumis, directory", directory, directory.replace(self.rawPath, ''))
            self.initializeDataframe(directory.replace(self.rawPath, ''), files)
            self.setFileTimes()
            self.setMQLumis()
            if not self.debug: self.saveJson()
            else: self.saveJson(name='mqLumisDebug.json')

    def getFilesToProcess(self):

        filesToProcess = {}

        lastRun, lastFile = self.getLastUpdate()
        startingDir0 = math.floor(lastRun/100)*100
        startingDir1 = math.floor((lastRun-startingDir0)/10)
        
        startingDir = '{}{}/000{}'.format(self.rawPath, startingDir0, startingDir1)
        print("Beginning with {}".format(startingDir))
        
        while(os.path.isdir(startingDir)):
            thisFileList = []
            print("Looking in directory {}".format(startingDir))
            for filename in os.listdir(startingDir):
                if not filename.startswith('MilliQan'): continue
                runNum, fileNum = self.getRunFile(filename)
                runNum = int(runNum)
                fileNum = int(fileNum)
                #print("Run {}, last run {})".format(runNum, lastRun))
                #print("File {}, last File {}".format(fileNum, lastFile))
                if (runNum < lastRun): continue
                if (runNum == lastRun and fileNum <= lastFile): continue
                #print("Need to process {}".format(filename))
                thisFileList.append(filename)
            filesToProcess[startingDir] = thisFileList
            
            if startingDir1 == 9:
                startingDir0+=100
                startingDir1 = 0
            else:
                startingDir1+=1
            startingDir = '{}{}/000{}'.format(self.rawPath, startingDir0, str(startingDir1))
            print("Updated dir to {}".format(startingDir))

        return filesToProcess

    def getLastUpdate(self):
        prevLumis = pd.read_json(self.outputFile, orient = 'split', compression = 'infer')
        lastProcess = prevLumis.tail(1)
        lastRun = lastProcess['run'].values[0]
        lastFile = lastProcess['file'].values[0]
        return lastRun, lastFile

    def initializeDataframe(self, path, fileList=None):
        fileCnt = 0
        if fileList is not None:
            print("initializing file list", path)
            for fileCnt, filename in enumerate(fileList):
                if self.debug and fileCnt > 100:
                    return
                if fileCnt % 1000 == 0: print("Working on processing file {}".format(fileCnt))
                runNum_, fileNum_ = self.getRunFile(filename)
                dict_ = lumiDict()
                dict_.run = int(runNum_)
                dict_.file = (fileNum_)
                dict_.dir = self.rawPath+'/'+path
                dict_.filename = filename
                #print(dict_.__dict__)
                self.mqLumis.loc[len(self.mqLumis.index)] = dict_.__dict__
        else:
            for ifile, filename in enumerate(os.listdir(self.rawPath+'/'+path)):
                if self.debug and fileCnt > 100: 
                    return
                if not filename.startswith("MilliQan"): continue
                if fileCnt % 1000 == 0: print("Working on processing file {}".format(fileCnt))
                runNum_, fileNum_ = self.getRunFile(filename)
                dict_ = lumiDict()
                dict_.run = int(runNum_)
                dict_.file = (fileNum_)
                dict_.dir = self.rawPath+'/'+path
                dict_.filename = filename
                self.mqLumis.loc[len(self.mqLumis.index)] = dict_.__dict__
                fileCnt += 1
                    
    def getRunFile(self, filename):
        runNum = filename.split('Run')[-1].split('.')[0]
        fileNum = filename.split('.')[1].split('_')[0]
        return runNum, fileNum
        
    def openLumis(self):
        self.lumiList = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+'/../configuration/' + self.rawLumis)

    def convertDatetime(self, time):
        dt_ = datetime.strptime(time, '%Y-%m-%d_%Hh%Mm%Ss')
        return dt_   

    def getFileTime(self, file):
        try:
            myfile = r.TFile.Open(file)
        except:
            print("File {} is a zombie, skipping...".format(file))
            return pd.NaT, pd.NaT
        meta = myfile.Get('Metadata')
        t_open = -1
        t_close = -1
        for event in meta:
            t_open = event.fileOpenTime
            t_close = event.fileCloseTime
        d_open = self.convertDatetime(str(t_open))
        d_close = self.convertDatetime(str(t_close))
        return d_open, d_close
        
    def setFileTimes(self):
        self.mqLumis[['start', 'stop']] = self.mqLumis.apply(lambda x: self.getFileTime(x.dir + '/' + x.filename) if pd.isnull(x.start) else (x.start, x.stop), axis='columns', result_type='expand')
        
    def addDatetimes(self):
        self.lumiList['start_time'] = self.lumiList['start_time'].where(pd.notnull(self.lumiList['start_time']), None)
        self.lumiList['end_time'] = self.lumiList['end_time'].where(pd.notnull(self.lumiList['end_time']), None)
        self.lumiList['start_stable_beam'] = self.lumiList['start_stable_beam'].astype(object).where(pd.notnull(self.lumiList['start_stable_beam']), None)

        self.lumiList['end_stable_beam'] = self.lumiList['end_stable_beam'].astype(object).where(pd.notnull(self.lumiList['end_stable_beam']), None)

        self.lumiList['start_time'] = self.lumiList['start_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if x != None else x)
        self.lumiList['end_time'] = self.lumiList['end_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if x != None else x)
        self.lumiList['start_stable_beam'] = self.lumiList['start_stable_beam'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if x != None else x)
        self.lumiList['end_stable_beam'] = self.lumiList['end_stable_beam'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S') if x != None else x)

        self.lumiList = self.lumiList.sort_values(by=['start_time'])
        self.lumiList = self.lumiList.reset_index(drop=True)
        
        self.lumiList['start_stable_beam'].replace({pd.NaT: None}, inplace=True)
        self.lumiList['end_stable_beam'].replace({pd.NaT: None}, inplace=True)


        
    def findLumiStart(self, start, stop):
    
        startId = -1
        stopId = -1

        #special case for zombie files (maybe better way than letting it get this far?)
        if pd.isnull(start) or pd.isnull(stop):
            mqLumi = 0
            lumis = 0
            fillId = None 
            beamType = None 
            beamEnergy = None
            betaStar = None 
            beamOn = False #if there is stable beams at time of milliqan run
            beamInRun = False #if there are any stable beams in the run
            fillStart = None 
            fillEnd = None
            startStableBeam = None
            endStableBeam = None
            return lumis, fillId, beamType, beamEnergy, betaStar, beamOn, beamInRun, fillStart, fillEnd, startStableBeam, endStableBeam, mqLumi
        
        #if milliqan run starts after all runs in lumi list
        if start > self.lumiList.start_time.max():
            mqLumi = 0
            lumis = 0
            fillId = None 
            beamType = None 
            beamEnergy = None
            betaStar = None 
            beamOn = False 
            beamInRun = False
            fillStart = None 
            fillEnd = None
            startStableBeam = None
            endStableBeam = None
            return lumis, fillId, beamType, beamEnergy, betaStar, beamOn, beamInRun, fillStart, fillEnd, startStableBeam, endStableBeam, mqLumi
        
        for i, st in enumerate(self.lumiList.start_time):
            if start < st: 
                startId = i-1
                break
        for i, (st, et) in enumerate(zip(self.lumiList.end_time[startId:], self.lumiList.start_time[startId:])):
            if stop < st: 
                stopId = startId + i
                break
            elif stop < et:
                stopId = startId + i
                break
        
        #if last milliqan run stops after last LHC run
        if stop > self.lumiList.end_time.max():
            stopId = len(self.lumiList)-1
                
        if startId == stopId:
            fillId = self.lumiList['fill_number'][startId]
            beamType = self.lumiList['fill_type_runtime'][startId]
            beamEnergy = self.lumiList['energy'][startId]
            betaStar = self.lumiList['beta_star'][startId]
            fillStart = self.lumiList['start_time'][startId]
            fillEnd = self.lumiList['end_time'][stopId]
            lumis = self.lumiList['delivered_lumi'][startId]
            startStableBeam = self.lumiList['start_stable_beam'][startId]
            endStableBeam = self.lumiList['end_stable_beam'][startId]
            beamOn = False
            beamInRun = False
            if not pd.isna(self.lumiList['start_stable_beam'][startId]):
                beamOn = True
            if not pd.isna(self.lumiList['start_time'][startId]):
                beamInRun = True
            
            mqLumi = 0
            if beamOn:
                totalLumi = self.lumiList['delivered_lumi'][startId]
                totalFillTime = self.lumiList['duration'][startId]
                totalMQTime = (stop-start).total_seconds()
                #print(totalLumi, totalFillTime, totalMQTime)
                frac = totalMQTime / totalFillTime
                mqLumi = totalLumi * frac
                
        else:
            print("ids", startId, stopId)
            print("start fill {0}, stop fill {1}".format(self.lumiList['fill_number'][startId], self.lumiList['fill_number'][stopId]))
            fillId = self.lumiList['fill_number'][startId:stopId+1].to_list()
            beamType = self.lumiList['fill_type_runtime'][startId:stopId+1].to_list()
            beamEnergy = self.lumiList['energy'][startId:stopId+1].to_list()
            betaStar = self.lumiList['beta_star'][startId:stopId+1].to_list()
            beamOn = [False if pd.isna(x) else True for x in self.lumiList['start_stable_beam'][startId:stopId+1]]
            beamInRun = [False if pd.isna(x) else True for x in self.lumiList['start_time'][startId:stopId+1]]
            fillStart = self.lumiList['start_time'][startId:stopId+1].to_list()
            fillEnd = self.lumiList['end_time'][startId:stopId+1].to_list()
            lumis = self.lumiList['delivered_lumi'][startId:stopId+1].to_list()
            startStableBeam = self.lumiList['start_stable_beam'][startId:stopId+1].to_list()
            endStableBeam = self.lumiList['end_stable_beam'][startId:stopId+1].to_list()
            mqLumi = 0
            for i in range(startId, stopId+1):
                x = self.lumiList[['start_time', 'end_time', 'start_stable_beam', 'end_stable_beam', 'delivered_lumi', 'duration', 'fill_number']].iloc[i]
                #print("checking fill", x.fill_number)
                if pd.isna(x.delivered_lumi): continue
                if start > x.end_stable_beam: continue
                if start < x.start_stable_beam: #milliqan run starts before fill
                    if stop >= x.end_stable_beam: #milliqan run spans entire fill
                        mqLumi += x.delivered_lumi
                    elif stop < x.end_stable_beam: #milliqan run stops before end of fill
                        total_time = (stop - x.start_stable_beam).total_seconds()
                        frac = total_time / x.duration
                        mqLumi += frac * x.delivered_lumi
                elif start > x.start_stable_beam: #milliqan run starts after fill
                    if stop >= x.end_stable_beam: #milliqan run ends after fill
                        total_time = (x.end_stable_beam - start).total_seconds()
                        frac = total_time / x.duration
                        mqLumi += frac * x.delivered_lumi
                    elif stop < x.end_stable_beam: #milliqan run ends before fill
                        print("This should be handled already!")
                        print(start, stop, x.start_stable_beam, x.end_stable_beam)
                else:
                    print("Bug in code, this case isn't handled")
                        
        return lumis, fillId, beamType, beamEnergy, betaStar, beamOn, beamInRun, fillStart, fillEnd, startStableBeam, endStableBeam, mqLumi
    
    def setMQLumis(self):
        self.mqLumis[['lumis', 'fill', 'beamType', 'beamEnergy', 'betaStar', 'beam', 'beamInRun', 'fillStart', 'fillEnd', 'startStableBeam', 'endStableBeam', 'lumiEst']] = self.mqLumis.apply(lambda x: self.findLumiStart(x.start, x.stop) if x.lumis is None else (x.lumis, x.fill, x.beamType, x.beamEnergy, x.betaStar, x.beam, x.beamInRun, x.fillStart, x.fillEnd, x.startStableBeam, x.endStableBeam, x.lumiEst), axis='columns', result_type='expand')

    def saveJson(self, name='mqLumis.json'):
        self.mqLumis.to_json(name, orient = 'split', compression = 'infer', index = 'true')

    def updateJson(self):
        existing = pd.read_json(self.outputFile, orient = 'split', compression = 'infer')
        self.mqLumis = pd.concat((existing, self.mqLumis), ignore_index=True)
        self.saveJson()

if __name__ == "__main__":

    update=True
    debug=False

    mylumiList = mqLumiList()
    mylumiList.debug = True
    mylumiList.openLumis()
    mylumiList.addDatetimes()

    if update:
        mylumiList.updateLumis()
        mylumiList.updateJson()
    else:
        mylumiList.looper()

    
