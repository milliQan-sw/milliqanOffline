import os
import pandas as pd
import ROOT as r
from datetime import datetime, timedelta, timezone
import pytz
import matplotlib.pyplot as plt
import math
import sys
from omsapi import OMSAPI

#using omsapi client https://gitlab.cern.ch/cmsoms/oms-api-client/-/tree/master


class lumiDict:
    
    def __init__(self):
        
        self.run = -1
        self.file = -1
        self.lumis = None
        self.fill = None
        self.beam = None
        self.beamInFill = None
        self.dir = None
        self.filename = None
        self.start = None
        self.stop = None

class mqLumiList():
    
    def __init__(self):
        self.lumi_csv = ''
        self.rawPath = '/store/user/milliqan/run3/slab/'
        self.outputFile = '/eos/experiment/milliqan/Configs/mqLumisSlab.json'
        self.rawLumis = '/eos/experiment/milliqan/Configs/rawLumis.json'
        self.mqLumis = pd.DataFrame(columns=['run', 'file', 'lumis', 'fill', 'beam', 'beamInFill', 'dir', 'filename', 'start', 'stop'])
        self.debug = False
        
    def looper(self):
        rawDirectories = ['600', '700']
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

        dtype_dict={'fill_number': 'int64',
                    'peak_lumi': 'object',
                    'bunches_colliding': 'object',
                    'efficiency_time': 'object',
                    'end_time': 'datetime64[s]',
                    'end_stable_beam': 'datetime64[s]',
                    'duration': 'object',
                    'start_time': 'datetime64[s]',
                    'peak_pileup': 'object',
                    'fill_type_runtime': 'object',
                    'beta_star': 'object',
                    'first_run_number': 'object',
                    'delivered_lumi_stablebeams': 'float64',
                    'start_stable_beam': 'datetime64[s]',
                    'efficiency_lumi': 'object',
                    'injection_scheme': 'object',
                    'recorded_lumi': 'object',
                    'delivered_lumi': 'object',
                    'last_run_number': 'object',
                    'energy': 'object'}

        rawLumis = pd.read_json(self.rawLumis, orient = 'split', compression = 'infer', dtype=dtype_dict)
        lastRun = rawLumis[(rawLumis['end_time'].isna()) & (~rawLumis['start_stable_beam'].isna())].head(1)['fill_number']
        if len(lastRun) == 0:
            lastRun = rawLumis.tail(1)['fill_number']
        lastRun = lastRun.iloc[0]

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
            'fill_type_runtime',
            'delivered_lumi_stablebeams']

        q = omsapi.query("fills")
        q.filter('sequence','GLOBAL-RUN')
        q.filter('fill_number', lastRun-1, 'GT') #our runs start at fill 8800
        q.sort("fill_number", asc=False).paginate(per_page = 1000)
        q.attrs(cols)

        response = q.data()

        print(response)

        dataframe = [x['attributes'] for x in response.json()['data']]
        dataframe = pd.DataFrame(dataframe)

        current_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        if len(dataframe) == 0:
            if rawLumis.iloc[-1]['end_time'] is None:
                rawLumis.at[rawLumis.index[-1], 'end_time'] = current_datetime
            if rawLumis.iloc[-1]['end_stable_beam'] is None:
                rawLumis.at[rawLumis.index[-1], 'end_stable_beam'] = current_datetime
            return rawLumis

        if len(dataframe) > 0:
            dataframe = dataframe.sort_values(by='fill_number')
            if dataframe.iloc[-1]['end_time'] is None:
                dataframe.at[dataframe.index[-1], 'end_time'] = current_datetime
            if dataframe.iloc[-1]['end_stable_beam'] is None:
                dataframe.at[dataframe.index[-1], 'end_stable_beam'] = current_datetime

            dataframe['start_time'] = pd.to_datetime(dataframe['start_time'])
            dataframe['end_time'] = pd.to_datetime(dataframe['end_time'])
            dataframe['start_stable_beam'] = pd.to_datetime(dataframe['start_stable_beam'])
            dataframe['end_stable_beam'] = pd.to_datetime(dataframe['end_stable_beam'])

            rawLumis = pd.concat((rawLumis, dataframe), ignore_index=True)
            rawLumis = rawLumis.drop_duplicates(subset=['fill_number'], keep='last')
            rawLumis = rawLumis.sort_values(by='fill_number')

            #rawLumis = rawLumis.where(pd.notna(rawLumis), None)
            rawLumis.to_json('rawLumis.json', date_format='iso', orient = 'split', compression = 'infer')

        return rawLumis

    def updateLumis(self, startingDir=None, startingFile=None):
        print("Updating the lumi list...")
        filesToProcess = self.getFilesToProcess(startingDir, startingFile)
        for id, (directory, files) in enumerate(filesToProcess.items()):
            if self.debug:
                if id > 0: break
            print("Working on id {}, directory {}".format(id, directory))
            if len(files) == 0: continue
            self.initializeDataframe(directory.replace(self.rawPath, ''), files)
            self.setFileTimes()
            self.setMQLumis()
            if not self.debug: self.saveJson()
            else: self.saveJson(name='mqLumisDebugSlab.json')

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

        lastProcess = prevLumis.tail(1)
        lastRun = lastProcess['run'].values[0]
        lastFile = lastProcess['file'].values[0]
        if not reprocess:
            return lastRun, lastFile
        else:
            #option to reprocess anything less than one day old, some files may be ongoing since list fill -> update info
            #prevLumis['start'] = pd.to_datetime(prevLumis['start'], unit='ms', errors='coerce')
            prevLumis['start'] = pd.to_datetime(prevLumis['start'], errors='coerce')

            one_day_ago = pd.Timestamp(datetime.utcnow() - timedelta(days=1), tz=pytz.UTC)
            result = prevLumis[prevLumis['start'] >= one_day_ago]
            if len(result) == 0:
                return lastRun, lastFile
            lastProcess = result.head(1)
            lastRun = lastProcess['run'].values[0]
            lastFile = lastProcess['file'].values[0]
            return lastRun, lastFile


    def initializeDataframe(self, path, fileList=None):
        fileCnt = 0
        if fileList is not None:
            for fileCnt, filename in enumerate(fileList):
                if self.debug and fileCnt > 2000: break
                if fileCnt % 1000 == 0: print("Working on processing file {}".format(fileCnt))
                print("Processing", fileCnt, filename)
                runNum_, fileNum_ = self.getRunFile(filename)
                dict_ = lumiDict()
                dict_.run = int(runNum_)
                dict_.file = (fileNum_)
                dict_.dir = self.rawPath+'/'+path
                dict_.filename = filename
                print(dict_.__dict__)
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
        #try:

        self.lumiList = self.getOMSInfo()

        self.lumiList['end_time'] = pd.to_datetime(self.lumiList['end_time'], errors='coerce', utc=True, format='%Y-%m-%dT%H:%M:%SZ')
        self.lumiList['start_time'] = pd.to_datetime(self.lumiList['start_time'], errors='coerce', utc=True, format='%Y-%m-%dT%H:%M:%SZ')
        self.lumiList['start_stable_beam'] = pd.to_datetime(self.lumiList['start_stable_beam'], errors='coerce', utc=True) #for some reason format was causing issues for this...
        self.lumiList['end_stable_beam'] = pd.to_datetime(self.lumiList['end_stable_beam'], errors='coerce', utc=True)
        self.lumiList = self.lumiList.sort_values(by='start_time')
        '''except:
            print("Error: unable to get lumi info from OMS, defaulting to local luminosity file", os.path.dirname(os.path.realpath(__file__))+'/../configuration/' + self.rawLumis)
            self.lumiList = pd.read_csv(os.path.dirname(os.path.realpath(__file__))+'/../configuration/' + self.rawLumis)'''

    def convertDatetime(self, time):
        #geneva_tz = pytz.timezone('Europe/Zurich')
        utc_tz = pytz.timezone('UTC')
        dt_ = datetime.strptime(time, '%Y-%m-%d_%Hh%Mm%Ss')
        #dt_ = geneva_tz.localize(dt_)
        dt_ = utc_tz.localize(dt_)
        #dt_ = dt_.astimezone(pytz.UTC)
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

        #self.lumiList['start_time'] = self.lumiList['start_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)
        #self.lumiList['end_time'] = self.lumiList['end_time'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)
        #self.lumiList['start_stable_beam'] = self.lumiList['start_stable_beam'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)
        #self.lumiList['end_stable_beam'] = self.lumiList['end_stable_beam'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') if x != None else x)

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
            beamInFill = False #if there are any stable beams in the run
            fillStart = None 
            fillEnd = None
            startStableBeam = None
            endStableBeam = None
            return lumis, fillId, beamType, beamEnergy, betaStar, beamOn, beamInFill, fillStart, fillEnd, startStableBeam, endStableBeam, mqLumi
        
        #if milliqan run starts after all runs in lumi list
        if start > self.lumiList.start_time.max() or stop < self.lumiList.start_time.min():
            mqLumi = 0
            lumis = 0
            fillId = None 
            beamType = None 
            beamEnergy = None
            betaStar = None 
            beamOn = False 
            beamInFill = False
            fillStart = None 
            fillEnd = None
            startStableBeam = None
            endStableBeam = None
            return lumis, fillId, beamType, beamEnergy, betaStar, beamOn, beamInFill, fillStart, fillEnd, startStableBeam, endStableBeam, mqLumi
        
        for i, st in enumerate(self.lumiList.start_time):
            if start < st: 
                startId = i-1
                #print('case 1 start {}, stop {}, st {}'.format(start, stop, st))
                break
        for i, (st, et) in enumerate(zip(self.lumiList.start_time[startId:], self.lumiList.end_time[startId:])):
            #print(startId, i, st, et)
            if stop < st: 
                stopId = startId + i - 1
                #print('case 2 start {}, stop {}, st {}, et {}'.format(start, stop, st, et))

                break
            elif stop < et:
                stopId = startId + i
                #print('case 3 start {}, stop {}, st {}, et {}'.format(start, stop, st, et))

                break
        
        #if last milliqan run stops after last LHC run
        if stop > self.lumiList.end_time.max():
            stopId = len(self.lumiList)-1
                
        #print("startID: {}, stopID: {}, start {}, max start {}, min start {}".format(startId, stopId, start, self.lumiList.start_time.max(), self.lumiList.start_time.min()))
        if startId == stopId:
            #print("single fill mq file")
            fillId = self.lumiList['fill_number'][startId]
            beamType = self.lumiList['fill_type_runtime'][startId]
            beamEnergy = self.lumiList['energy'][startId]
            betaStar = self.lumiList['beta_star'][startId]
            fillStart = self.lumiList['start_time'][startId]
            fillEnd = self.lumiList['end_time'][stopId]
            lumis = self.lumiList['delivered_lumi_stablebeams'][startId]
            startStableBeam = self.lumiList['start_stable_beam'][startId]
            endStableBeam = self.lumiList['end_stable_beam'][startId]
            beamOn = False
            beamInFill = False
            if not pd.isna(self.lumiList['start_stable_beam'][startId]):
                beamInFill = True
            '''if not pd.isna(self.lumiList['start_time'][startId]):
                beamInFill = True'''
            
            mqLumi = 0
            if beamInFill:

                l_start = 0
                l_stop = 0
                
                #start1, end1 = range1 #(stable beam start, stable_beam_end)
                #start2, end2 = range2 #(start, stop)
                
                # Check for no overlap
                findLumis = True
                if start < self.lumiList['start_stable_beam'][startId] and stop < self.lumiList['start_stable_beam'][startId]:
                    findLumis = False
                if start > self.lumiList['end_stable_beam'][startId] and stop > self.lumiList['end_stable_beam'][startId]:
                    findLumis = False
                
                if findLumis:
                    # Calculate overlap
                    overlap_start = max(self.lumiList['start_stable_beam'][startId], start)
                    overlap_end = min(self.lumiList['end_stable_beam'][startId], stop)
                    overlap_duration = overlap_end - overlap_start
                    
                    # Convert overlap duration to seconds
                    overlap_seconds = max(0, overlap_duration.total_seconds())

                    totalLumi = self.lumiList['delivered_lumi_stablebeams'][startId]
                    totalFillTime = self.lumiList['duration'][startId]
                    totalMQTime = (stop-start).total_seconds()
                    frac = overlap_seconds / totalFillTime
                    mqLumi = totalLumi * frac
                    #print("case 0, startstart {}, stop {}, fillId {}, mqLumis {}, lumis {}, fill time {}, mqTime {}".format(start, stop, fillId, mqLumi, lumis, totalFillTime, overlap_seconds))

            #print('mqlumi', mqLumi)
            if mqLumi > 0:
                beamOn = True
                
        else:
            fillId = self.lumiList['fill_number'][startId:stopId+1].to_list()
            beamType = self.lumiList['fill_type_runtime'][startId:stopId+1].to_list()
            beamEnergy = self.lumiList['energy'][startId:stopId+1].to_list()
            betaStar = self.lumiList['beta_star'][startId:stopId+1].to_list()
            beamInFill = [False if pd.isna(x) else True for x in self.lumiList['start_stable_beam'][startId:stopId+1]]
            beamOn = False
            #beamInFill = [False if pd.isna(x) else True for x in self.lumiList['start_time'][startId:stopId+1]]
            fillStart = self.lumiList['start_time'][startId:stopId+1].to_list()
            fillEnd = self.lumiList['end_time'][startId:stopId+1].to_list()
            lumis = self.lumiList['delivered_lumi_stablebeams'][startId:stopId+1].to_list()
            startStableBeam = self.lumiList['start_stable_beam'][startId:stopId+1].to_list()
            endStableBeam = self.lumiList['end_stable_beam'][startId:stopId+1].to_list()
            mqLumi = 0
            for i in range(startId, stopId+1):
                x = self.lumiList[['start_time', 'end_time', 'start_stable_beam', 'end_stable_beam', 'delivered_lumi_stablebeams', 'duration', 'fill_number']].iloc[i]
                if pd.isna(x.delivered_lumi_stablebeams) or x.delivered_lumi_stablebeams == 0: continue
                if start > x.end_stable_beam: continue
                if start < x.start_stable_beam: #milliqan run starts before fill
                    if stop < x.start_stable_beam: continue
                    if stop >= x.end_stable_beam: #milliqan run spans entire fill
                        mqLumi += x.delivered_lumi_stablebeams
                        #print("case 1, startstart {}, stop {}, fillId {}, mqLumis {}, lumis {}".format(start, stop, fillId, mqLumi, lumis))
                    elif stop < x.end_stable_beam: #milliqan run stops before end of fill
                        total_time = (stop - x.start_stable_beam).total_seconds()
                        frac = total_time / x.duration
                        mqLumi += frac * x.delivered_lumi_stablebeams
                        #print("case 2, startstart {}, stop {}, fillId {}, mqLumis {}, lumis {}".format(start, stop, fillId, mqLumi, lumis))

                elif start > x.start_stable_beam: #milliqan run starts after fill
                    if stop >= x.end_stable_beam: #milliqan run ends after fill
                        total_time = (x.end_stable_beam - start).total_seconds()
                        frac = total_time / x.duration
                        mqLumi += frac * x.delivered_lumi_stablebeams
                        #print("case 3, startstart {}, stop {}, fillId {}, mqLumis {}, lumis {}".format(start, stop, fillId, mqLumi, lumis))
                    elif stop < x.end_stable_beam: #milliqan run ends before fill
                        print('start {}, stop {}, start stable {}, stop stable {}'.format(start, stop, x.start_stable_beam, x.end_stable_beam))
                        print("Error: This should be handled already!")
                else:
                    print("Error: Bug in code, this case isn't handled")

            if mqLumi > 0:
                beamOn = True
                        
        return lumis, fillId, beamType, beamEnergy, betaStar, beamOn, beamInFill, fillStart, fillEnd, startStableBeam, endStableBeam, mqLumi
    
    def setMQLumis(self):
        self.mqLumis[['lumis', 'fill', 'beamType', 'beamEnergy', 'betaStar', 'beam', 'beamInFill', 'fillStart', 'fillEnd', 'startStableBeam', 'endStableBeam', 'lumiEst']] = self.mqLumis.apply(lambda x: self.findLumiStart(x.start, x.stop) if x.lumis is None else (x.lumis, x.fill, x.beamType, x.beamEnergy, x.betaStar, x.beam, x.beamInFill, x.fillStart, x.fillEnd, x.startStableBeam, x.endStableBeam, x.lumiEst), axis='columns', result_type='expand')

    def saveJson(self, name='mqLumisUpdateSlab.json'):
        self.mqLumis.to_json(name, orient = 'split', compression = 'infer', index = 'true', date_format='iso')

    def updateJson(self):
        existing = pd.read_json(self.outputFile, orient = 'split', compression = 'infer')
        existing['start'] = pd.to_datetime(existing['start'])
        existing = existing.sort_values(by='start')
        self.mqLumis['run'] = self.mqLumis['run'].astype(int)
        self.mqLumis['file'] = self.mqLumis['file'].astype(int)
        self.mqLumis = pd.concat([existing, self.mqLumis], ignore_index=True)
        self.mqLumis = self.mqLumis.drop_duplicates(subset=['run', 'file'], keep='last')
        self.mqLumis = self.mqLumis.sort_values(by='start')
        if self.debug:
            self.saveJson(name='mqLumisDebugSlab.json')
        else:
            self.saveJson()
        if not self.debug: 
            os.system('rsync -rzh mqLumisUpdateSlab.json {}'.format(self.outputFile))
            os.system('rsync -rzh rawLumisSlab.json {}'.format(self.rawLumis))


if __name__ == "__main__":

    LOCK_FILE = "/tmp/getLumisSlab.lock"

    # Check if lock file exists
    if os.path.exists(LOCK_FILE):
        print("Another instance of the script is already running. Exiting.")
        sys.exit(1)

    # Create lock file
    with open(LOCK_FILE, "w") as f:
        f.write("")

    try:
        update=False
        debug=False

        startingRun = 600
        startingFile = 1

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



    
