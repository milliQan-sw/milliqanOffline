#!/usr/bin/python3
from runOfflineFactory import runOfflineFactory,publishDataset
from mongoConnect import mongoConnect
from subprocess import call
from subprocess import check_output
import argparse
import json, math
import os
exe_default = os.getenv("OFFLINEDIR")+"/exe/v32.exe"
site = os.getenv("OFFLINESITE")
import calendar;
import time;
  
def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-s","--selectionString",help="MongoDB selection string",type=str,default='{"run" : {"$gt" : 468}}')
    parser.add_argument("-o","--outputDir",help="Output file name",type=str,default="/net/cms26/cms26r0/milliqan/Run3Offline/")
    parser.add_argument("-a","--appendToTag",help="Append to database tag",default=None)
    parser.add_argument("-e","--exe",help="Executable to run")
    parser.add_argument("-f","--force",help="Force overwrite",action="store_true",default=False)
    parser.add_argument("-r","--recovery",help="Overwrite failed jobs",action="store_true",default=False)
    args = parser.parse_args()
    return args

def checkMongoDB(db,allIds):
    nX = 0
    #Check for existing entry 
    locationsInDb = []
    indicesInDb = []
    matchedInDb = []
    for x in (db.milliQanOfflineDatasets.find({"_id" :{"$in": allIds}})):
        indexInDb = allIds.index(x["_id"])
        indicesInDb.append(indexInDb)
        locationsInDb.append(x["location"])
        matchedInDb.append(x["matched"])
    allLocations = []
    allOfflineEntriesExist = []
    offlineMatched = []
    for index in range(len(allIds)):
        if index in indicesInDb:
            allLocations.append(locationsInDb[indicesInDb.index(index)])
            offlineMatched.append(matchedInDb[indicesInDb.index(index)])
            if (os.path.exists(locationsInDb[indicesInDb.index(index)])):
                allOfflineEntriesExist.append(True)
            else:
                allOfflineEntriesExist.append(False)
        else:
            allLocations.append(None)
            allOfflineEntriesExist.append(False)
            offlineMatched.append(False)
    return allOfflineEntriesExist,allLocations,offlineMatched

def checkQueueStatus():
    readyFile = "/net/cms2/cms2r0/milliqan/jobs/ready.list"
    runningFile = "/net/cms2/cms2r0/milliqan/jobs/running.list"
    queuedFile = "/net/cms2/cms2r0/milliqan/jobs/queued.list"
    allFiles = [readyFile,runningFile,queuedFile]
    offDir = os.getenv("OFFLINEDIR")
    allJobs = 0
    locations = []
    for iFile in allFiles:
        if not os.path.exists(iFile): continue
        with open(iFile,"r") as iF:
            for iJob in iF.readlines():
                if "MilliQanJob" in iJob:
                    shellScript = iJob.split(" ")[-1].strip()
                    with open(shellScript,"r") as iS:
                        for iSub in iS.readlines():
                            if "python" in iSub:
                                location = iSub.split("-o")[-1].split(".root")[0]+".root"
                                locations.append(location.strip())
    return locations
        
def processRuns(selectionString="{}",outputDir="/net/cms26/cms26r0/milliqan/Run3Offline/",appendToTag=None,exe=None,force =False, recovery=False):
    locationsRunningJobs = checkQueueStatus()
    inputDatabase = mongoConnect()
    if exe == None:
        exe = exe_default
    
    version = check_output([exe, "-v"]).strip().decode("utf-8")
    version = version.split("-")[0]
    if appendToTag:
        version += "_"+appendToTag

    outputDirFull = outputDir + "/"+version.split("-")[0]+"/"
    selectionDict = json.loads(selectionString)
    selectionDict["site"] = site
    selectionDict["type"] = "MilliQan"
    #checking input samples to run
    outputSamplesToRun = inputDatabase.milliQanRawDatasets.find(selectionDict)
    selectionDictMatch = selectionDict.copy()
    selectionDictMatch["type"] = "MatchedEvents"
    matchedSamplesToRun = inputDatabase.milliQanRawDatasets.find(selectionDictMatch)
    matchedLocationDict = {}
    for xM in matchedSamplesToRun:
        matchedLocationDict[xM["_id"]] = xM["location"]
    submissions = []
    if not os.path.exists(outputDirFull):
        os.makedirs(outputDirFull)
    #making output samples
    runs = []
    totalSamples = inputDatabase.milliQanRawDatasets.count_documents(selectionDict)
    allSampleIds,allInputs,allMatchedLocations,allIFiles,allRuns = [],[],[],[],[]
    for x in outputSamplesToRun:
        sampleId = "_".join(str(e) for e in [x["run"],x["file"],version,selectionDict["type"],selectionDict["site"]])
        idMatched = x["_id"].split("_")
        idMatched[2] = "MatchedEvents"
        idMatched = "_".join(idMatched)
        matchedLocation = None
        if idMatched in matchedLocationDict:
            matchedLocation = matchedLocationDict[idMatched]
        inputName = x["location"]
        allSampleIds.append(sampleId)
        allInputs.append(inputName)
        allMatchedLocations.append(matchedLocation)
        allIFiles.append(x["file"])
        allRuns.append(x["run"])
    #Check if output already made
    allOfflineEntryExists,allLocations,offlineMatched = checkMongoDB(inputDatabase,allSampleIds)

    for sampleId,inputName,matchedLocation,offlineEntryExists,location,iFile,run,matchedInDb in zip(allSampleIds,allInputs,allMatchedLocations,allOfflineEntryExists,allLocations,allIFiles,allRuns,offlineMatched):
        # print  (sampleId,run,offlineEntryExists,matchedLocation,matchedInDb)
        # continue
        if not offlineEntryExists or force or (recovery and "DUMMY" in location) or (matchedLocation != None and matchedInDb == False):
            outputName = outputDirFull+inputName.split("/")[-1]
            outputName = outputName.replace(".root","_"+version+".root")
            if outputName in locationsRunningJobs:
                continue
            submitCommand = "python3 {}/scripts/runOfflineFactory.py -i {} -o {} -e {} -f".format(os.getenv("OFFLINEDIR"),inputName,outputName,exe)
            matched = matchedLocation != None
            if matched:
                submitCommand += " -m {}".format(matchedLocation)
            if appendToTag != None:
                submitCommand += " -a {}".format(appendToTag)
            submissions.append(submitCommand)
            #Add dummy entries to database to avoid resubmission
            runs.append(run)
            print(offlineEntryExists)
            if not offlineEntryExists:
                publishDataset({},"DUMMY","DUMMY",iFile,run,version,site,"MilliQan",matched,True,inputDatabase,quiet=True)
    filesPerJob=15.
    if len(runs) > 0:
        print ("Submiting runs:",sorted(list(set(runs))))
    else:
        print ("No jobs to submit")
    nFiles=len(submissions)
    iFile=0
    nJobs= int(math.ceil(nFiles/filesPerJob))
    submitDir = "submit"
    # gmt stores current gmtime
    gmt = time.gmtime()
      
    # ts stores timestamp
    ts = calendar.timegm(gmt)
    if not os.path.exists(submitDir):
        os.makedirs(submitDir)
    for iJob in range(nJobs):
        scriptName= submitDir+"/MilliQanJob_"+str(iJob)+"ID_"+str(ts)+".sh"
        script = open(scriptName,"w")
        script.write("#!/bin/bash\n")
        script.write("cd {}\n".format(os.getenv("OFFLINEDIR")))
        script.write("source setup.sh\n")
        for i in range(15):
            if iFile>=nFiles: break
            script.write(submissions[iFile]+"\n")
            iFile += 1

        script.close()
        os.chmod(scriptName,0o777)
        # call(["JobSubmit.csh",scriptName])
        call(["/net/cms2/cms2r0/Job/JobSubmit.csh","-node","py3",scriptName])


if __name__ == "__main__":
    processRuns(**vars(parse_args()))
    # processRuns(selectionString='{"run" : {"$gt" : 468}}',force=True)
