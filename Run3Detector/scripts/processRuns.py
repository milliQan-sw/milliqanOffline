from runOfflineFactory import runOfflineFactory,publishDataset
from mongoConnect import mongoConnect
from subprocess import call
from subprocess import check_output
import json, math
import os
exe_default = os.getenv("OFFLINEDIR")+"/display_MC.exe"
site = os.getenv("OFFLINESITE")
import calendar;
import time;
  

def checkMongoDB(db,_id):
    nX = 0
    #Check for existing entry 
    # milliQanOfflineDataset["_id"] = "{}_{}_{}_{}_{}".format(runNumber,fileNumber,tag,inputType,site)
    # milliQanOfflineDataset["run"] = runNumber
    # milliQanOfflineDataset["file"] = fileNumber
    # milliQanOfflineDataset["version"] = tag
    # milliQanOfflineDataset["location"] = os.path.abspath(outputFile)
    # milliQanOfflineDataset["type"] = inputType
    # milliQanOfflineDataset["site"] = site
    for x in (db.milliQanOfflineDatasets.find({"_id" : _id})):
        nX +=1
    return nX
def processRuns(mongoSelection="{}",outputDir="/net/cms26/cms26r0/milliqan/Run3Offline/",appendToTag=None,exe=None,force =False):
    inputDatabase = mongoConnect()
    if exe == None:
        exe = exe_default
    
    # version = <get version>
    version = check_output([exe, "-v"]).strip().decode("utf-8")
    if appendToTag:
        version = version.split("-")[0]+"_"+appendToTag
    else:
        version = version.split("-")[0]
    selectionDict = json.loads(mongoSelection)
    selectionDict["site"] = site
    selectionDict["type"] = "MilliQan"
    #checking input samples to run
    outputSamplesToRun = inputDatabase.milliQanRawDatasets.find(selectionDict)
    submissions = []
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    #making output samples
    for x in outputSamplesToRun:
        print (x)
        sampleId = "_".join(str(e) for e in [x["run"],x["file"],version,selectionDict["type"],selectionDict["site"]])
        inputName = x["location"]
        offlineEntryExists = checkMongoDB(inputDatabase,sampleId)
        if force or not offlineEntryExists:
            outputName = outputDir+inputName.split("/")[-1]
            submissions.append("python3 {}/scripts/runOfflineFactory.py -i {} -o {} -e {} -f".format(os.getenv("OFFLINEDIR"),inputName,outputName,exe))
            #Add dummy entries to database to avoid resubmission
            if not offlineEntryExists:
                publishDataset({},"DUMMY","DUMMY",x["file"],x["run"],version,site,"MilliQan",False,inputDatabase)

    filesPerJob=15.
    nFiles=len(submissions)
    iFile=0
    nJobs= int(math.ceil(nFiles/filesPerJob))
    submitDir = "submit"
    # gmt stores current gmtime
    gmt = time.gmtime()
    print("gmt:-", gmt)
      
    # ts stores timestamp
    ts = calendar.timegm(gmt)
    print("timestamp:-", ts)
    if not os.path.exists(submitDir):
        os.makedirs(submitDir)
    for iJob in range(nJobs):
        scriptName= submitDir+"/Job_"+str(iJob)+"ID_"+str(ts)+".sh"
        script = open(scriptName,"w")
        script.write("#!/bin/bash\n")
        script.write("cd {}\n".format(os.getenv("OFFLINEDIR")))
        script.write("source setup.sh\n")
        for i in range(15):
            if iFile>=nFiles: break
            script.write(submissions[i]+"\n")
            iFile += 1

        script.close()
        os.chmod(scriptName,0o777)
        call(["JobSubmit.csh",scriptName])


if __name__ == "__main__":
    processRuns(mongoSelection='{"run" : 309}',force=True)
