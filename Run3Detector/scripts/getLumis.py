import os
import pandas as pd
import ROOT as r
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math
import sys
from omsapi import OMSAPI

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
        self.outputFile = '/eos/experiment/milliqan/Configs/mqLumis.json'
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
                    continue
                self.initializeDataframe('{0}/{1}'.format(d1, d2))
                self.setFileTimes()
                self.setMQLumis()
                if not self.debug: self.saveJson()
                else: self.saveJson(name='mqLumisDebug.json')

    def getOMSInfo(self):
        my_app_id='milliqan-oms'
        my_app_secret='AvwJaQWfSMuDsOhYwPxynQMrFN7YXfPV'

        omsapi = OMSAPI("https://cmsoms.cern.ch/agg/api", "v1", cert_verify=False)
        omsapi.auth_oidc(my_app_id,my_app_secret)
        
        cols=['fill_number',
            'first_run_number',
            'last_run_number',
            'duration',
            'start_time',
            'start_stable_beam',
            'end_stable_beam',
            'end_time',
            'delivered_lumi',
            'recorded_lumi',
            'efficiency_time',
            'efficiency_lumi',
            'peak_lumi',
            'peak_pileup',
            'bunches_colliding',
            'beta_star',
            'energy',
            'injection_scheme',
            'fill_type_runtime']

        q = omsapi.query("fills")
        q.filter('sequence','GLOBAL-RUN')
        q.filter('fill_number', 8800, 'GT') #our runs start at fill 8800
        q.sort("fill_number", asc=False).paginate(per_page = 1000)
        q.attrs(cols)

        response = q.data()
        dataframe = [x['attributes'] for x in response.json()['data']]

        current_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        if dataframe[0]['end_time'] is None:
            dataframe[0]['end_time'] = str(current_datetime)
        if dataframe[0]['end_stable_beam'] is None:
            dataframe[0]['end_stable_beam'] = str(current_datetime)
        dataframe = pd.DataFrame(dataframe)
        return dataframe

    def updateLumis(self, startingDir=None, startingFile=None):
        print("Updating the lumi list...")
        filesToProcess = self.getFilesToProcess(startingDir, startingFile)
        for id, (directory, files) in enumerate(filesToProcess.items()):
            if self.debug:
                if id > 0: break
            self.initializeDataframe(directory.replace(self.rawPath, ''), files)
            self.setFileTimes()
            self.setMQLumis()
            if not self.debug: self.saveJson()
            else: self.saveJson(name='mqLumisDebug.json')

    def getFilesToProcess(self, lastRun=None, lastFile=None):

        filesToProcess = {}

        if lastRun is None and lastFile is None:
            lastRun, lastFile = self.getLastUpdate()
        startingDir0 = math.floor(lastRun/100)*100
        startingDir1 = math.floor((lastRun-startingDir0)/10)
        
        startingDir = '{}{}/000{}'.format(self.rawPath, startingDir0, startingDir1)
        
        while(os.path.isdir(startingDir)):
            thisFileList = []
            for filename in os.listdir(startingDir):
                if not filename.startswith('MilliQan'): continue
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
            startingDir = '{}{}/000{}'.format(self.rawPath, startingDir0, str(startingDir1))

        return filesToProcess

    def getLastUpdate(self, reprocess=True):
        prevLumis = pd.read_json(self.outputFile, orient = 'split', compression = 'infer')

        if reprocess==False:
            lastProcess = prevLumis.tail(1)
            lastRun = lastProcess['run'].values[0]
            lastFile = lastProcess['file'].values[0]
            return lastRun, lastFile
        else:
            #option to reprocess anything less than one day old, some files may be ongoing since list fill -> update info
            prevLumis['start'] = pd.to_datetime(prevLumis['start'], unit='ms')
            one_day_ago = datetime.utcnow() - timedelta(days=1)
            result = prevLumis[prevLumis['start'] >= one_day_ago]
            lastProcess = result.head(1)
            lastRun = lastProcess['run'].values[0]
            lastFile = lastProcess['file'].values[0]
            return lastRun, lastFile


    def initializeDataframe(self, path, fileList=None):
        fileCnt = 0
        if fileList is not None:
            for fileCnt, filename in enumerate(fileList):
                if self.debug and fileCnt > 100: break
                if fileCnt % 1000 == 0: print("Working on processing file {}".format(fileCnt))
                print("Processing", fileCnt, filename)
                runNum_, fileNum_ = self.getRunFile(filename)
                dict_ = lumiDict()
                dict_.run = int(runNum_)
                dict_.file = (fileNum_)
                dict_.dir = self.rawPath+'/'+path
                dict_.filename = filename
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
                dict_.file = int(fileNum_)
                dict_.dir = self.rawPath+'/'+path
                dict_.filename = filename
                self.mqLumis.loc[len(self.mqLumis.index)] = dict_.__dict__
                fileCnt += 1
                    
    def getRunFile(self, filename):
        runNum = filename.split('Run')[-1].split('.')[0]
        fileNum = filename.split('.')[1].split('_')[0]
        return runNum, fileNum
        
    def openLumis(self):
        try:
            self.lumiList = self.getOMSInfo()
        except:
            print("Error: unable to get lumi info from OMS, defaulting to local luminosity file", os.path.dirname(os.path.realpath(__file__))+'/../configuration/' + self.rawLumis)
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

        self.lumiList['start_time'] = self.lumiList['start_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)
        self.lumiList['end_time'] = self.lumiList['end_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)
        self.lumiList['start_stable_beam'] = self.lumiList['start_stable_beam'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)
        self.lumiList['end_stable_beam'] = self.lumiList['end_stable_beam'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)

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
                frac = totalMQTime / totalFillTime
                mqLumi = totalLumi * frac
                
        else:
            #print("ids", startId, stopId)
            #print("start fill {0}, stop fill {1}".format(self.lumiList['fill_number'][startId], self.lumiList['fill_number'][stopId]))
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
                #print('fill {}, lumi {}, stable beam start {}, stable beam stop {}, start {}, stop {}, mqLumi {}'.format(x.fill_number, x.delivered_lumi, x.start_stable_beam, x.end_stable_beam, start, stop, mqLumi))
                if pd.isna(x.delivered_lumi): continue
                if start > x.end_stable_beam: continue
                if start < x.start_stable_beam: #milliqan run starts before fill
                    if stop < x.start_stable_beam: continue
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
                        print("Error: This should be handled already!")
                else:
                    print("Error: Bug in code, this case isn't handled")
                        
        return lumis, fillId, beamType, beamEnergy, betaStar, beamOn, beamInRun, fillStart, fillEnd, startStableBeam, endStableBeam, mqLumi
    
    def setMQLumis(self):
        self.mqLumis[['lumis', 'fill', 'beamType', 'beamEnergy', 'betaStar', 'beam', 'beamInRun', 'fillStart', 'fillEnd', 'startStableBeam', 'endStableBeam', 'lumiEst']] = self.mqLumis.apply(lambda x: self.findLumiStart(x.start, x.stop) if x.lumis is None else (x.lumis, x.fill, x.beamType, x.beamEnergy, x.betaStar, x.beam, x.beamInRun, x.fillStart, x.fillEnd, x.startStableBeam, x.endStableBeam, x.lumiEst), axis='columns', result_type='expand')

    def saveJson(self, name='mqLumisUpdate.json'):
        self.mqLumis.to_json(name, orient = 'split', compression = 'infer', index = 'true')

    def updateJson(self):
        existing = pd.read_json(self.outputFile, orient = 'split', compression = 'infer')
        existing = existing.sort_values(by='start')
        self.mqLumis = self.mqLumis.sort_values(by='start')
        self.mqLumis['run'] = self.mqLumis['run'].astype(int)
        self.mqLumis['file'] = self.mqLumis['file'].astype(int)
        self.mqLumis = pd.concat([existing, self.mqLumis], ignore_index=True)
        #print("Total entries after merge {}".format(len(self.mqLumis)))
        #print("Number of duplicates ", len(self.mqLumis[self.mqLumis.duplicated(subset=['run', 'file'])]))
        self.mqLumis = self.mqLumis.drop_duplicates(subset=['run', 'file'], keep='last')
        #print("Total entries after drop {}".format(len(self.mqLumis)))
        if self.debug:
            self.saveJson(name='mqLumisDebug.json')
        else:
            self.saveJson()
        if not self.debug: os.system('rsync -rzh mqLumisUpdate.json {}'.format(self.outputFile))


if __name__ == "__main__":

    LOCK_FILE = "/tmp/getLumis.lock"

    # Check if lock file exists
    if os.path.exists(LOCK_FILE):
        print("Another instance of the script is already running. Exiting.")
        sys.exit(1)

    # Create lock file
    with open(LOCK_FILE, "w") as f:
        f.write("")

    try:
        update=True
        debug=False

        startingRun = None
        startingFile = None

        mylumiList = mqLumiList()
        mylumiList.debug = debug
        mylumiList.openLumis()
        mylumiList.addDatetimes()

        if update:
            os.system('~/accessEOS.sh')
            mylumiList.updateLumis(startingRun, startingFile)
            mylumiList.updateJson()
        else:
            mylumiList.looper()
    finally:
        # Remove lock file when finished
        os.remove(LOCK_FILE)



    
