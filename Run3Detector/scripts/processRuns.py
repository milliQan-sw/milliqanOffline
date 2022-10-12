from runOfflineFactory import runOfflineFactory,publishDataset
from mongoConnect import mongoConnect
from subprocess import call
from subprocess import check_output
import argparse
import json, math
import os
exe_default = os.getenv("OFFLINEDIR")+"/display_MC.exe"
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
    location = None
    for x in (db.milliQanOfflineDatasets.find({"_id" : _id})):
        nX +=1
        location = x["location"]
    return nX,location
def processRuns(selectionString="{}",outputDir="/net/cms26/cms26r0/milliqan/Run3Offline/",appendToTag=None,exe=None,force =False, recovery=False):
    inputDatabase = mongoConnect()
    if exe == None:
        exe = exe_default
    
    # version = <get version>
    version = check_output([exe, "-v"]).strip().decode("utf-8")
    if appendToTag:
        version = version.split("-")[0]+"_"+appendToTag
    else:
        version = version.split("-")[0]
    selectionDict = json.loads(selectionString)
    selectionDict["site"] = site
    selectionDict["type"] = "MilliQan"
    #checking input samples to run
    outputSamplesToRun = inputDatabase.milliQanRawDatasets.find(selectionDict)
    submissions = []
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    #making output samples
    runs = []
    totalSamples = inputDatabase.milliQanRawDatasets.count_documents(selectionDict)
    ix = 0
    for x in outputSamplesToRun:
        ix += 1
        if (ix % 20 == 0): print ("Progress: {}%".format("%.1f"%(ix*100./totalSamples)))
        sampleId = "_".join(str(e) for e in [x["run"],x["file"],version,selectionDict["type"],selectionDict["site"]])
        inputName = x["location"]
        offlineEntryExists,location = checkMongoDB(inputDatabase,sampleId)
        if not offlineEntryExists or force or (recovery and location == "DUMMY"):
            outputName = outputDir+inputName.split("/")[-1]
            outputName = outputName.replace(".root","_"+version+".root")
            submissions.append("python3 {}/scripts/runOfflineFactory.py -i {} -o {} -e {} -f".format(os.getenv("OFFLINEDIR"),inputName,outputName,exe))
            #Add dummy entries to database to avoid resubmission
            runs.append(x["run"])
            if not offlineEntryExists:
                publishDataset({},"DUMMY","DUMMY",x["file"],x["run"],version,site,"MilliQan",False,inputDatabase,quiet=True)

    filesPerJob=15.
    print ("Submiting runs:",sorted(list(set(runs))))
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
        scriptName= submitDir+"/Job_"+str(iJob)+"ID_"+str(ts)+".sh"
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
        call(["JobSubmit.csh","-node","py3",scriptName])


if __name__ == "__main__":
    processRuns(**vars(parse_args()))
    # processRuns(selectionString='{"run" : {"$gt" : 468}}',force=True)
