#!/usr/bin/python3
import os, sys, re
import json
import ROOT as r
import glob
import math
from subprocess import call
import argparse
import traceback
from pprint import pprint
from mongoConnect import mongoConnect
from subprocess import Popen, PIPE

site = os.getenv("OFFLINESITE")
if not site:
    print ("Need to source setup.sh")
    exit()


def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--inputFile",help="File to run over",type=str, required=True)
    parser.add_argument("-o","--outputFile",help="Output file name",type=str, required=True)
    parser.add_argument("-a","--appendToTag",help="Append to database tag",type=str,default="")
    parser.add_argument("-m","--mergedTriggerFile",help="Trigger file friend tree",type=str,default="")
    parser.add_argument("-e","--exe",help="Executable to run",type=str,default="./script.exe")
    parser.add_argument("-d","--database",help="Database string",default=None)
    parser.add_argument("-p","--publish",help="Publish dataset",action="store_true",default=False)
    parser.add_argument("-f","--force_publish",help="Force publish dataset",action="store_true",default=False)
    parser.add_argument("-c","--configurations",help="JSON Configuration files or string",type=str,nargs="+")
    parser.add_argument("--drs",help="DRS input",action="store_true",default=False)
    parser.add_argument("--display",help="Display events",type=int,nargs="+")
    args = parser.parse_args()
    return args
def validateOutput(outputFile):
    foundBad = False
    try:
        f1 = r.TFile(outputFile,"READ")
        t = f1.Get("t")
        nevts = t.GetEntries()
        # print "[RSR] ntuple has %i events and expected %i" % (t.GetEntries(), expectednevts)
        # if int(expectednevts) > 0 and int(t.GetEntries()) != int(expectednevts):
        #     print "[RSR] nevents mismatch"
        #     foundBad = True
        tag = f1.Get("tag").GetTitle();
    except Exception as ex:
        msg = traceback.format_exc()
        if "EDProductGetter" not in msg:
            tag = None
    if tag==None:
        print ("removing output file because it does not deserve to live (result will not be published)")
        os.system("rm "+outputFile)
    return tag 
def runOfflineFactory(inputFile,outputFile,exe,configurations,publish,force_publish,database,appendToTag,mergedTriggerFile,drs,display,runNumber=None,fileNumber=None):
    if force_publish:
        publish = True
    if runNumber == None:
        try:
            if drs:
                runNumber = int(inputFile.split("/")[-1].split("CMS")[-1].split(".")[0])
                fileNumber = 0
            else:
                runNumber = int(inputFile.split("/")[-1].split("Run")[-1].split(".")[0])
                fileNumber = int(inputFile.split("/")[-1].split(".")[1].split("_")[0])    
        except:
            if publish:
                print ("Could not identify file and/or run number so cannot publish")
                exit()
            fileNumber = -1
            runNumber = -1
    if display and publish:
        print("Can't publish in display mode!")
        exit()
    
    if not configurations:
        offlineDir = os.getenv("OFFLINEDIR")
        if drs:
            configurations = [offlineDir+"/configuration/pulseFinding/pulseFindingTest.json"]
        else:
            configurations = [offlineDir+"/configuration/chanMaps/fullSuperModuleMap.json",offlineDir+"/configuration/pulseFinding/pulseFindingTest.json",offlineDir+"/configuration/calibrations/firstSupermodulesCalibration.json"]

    if "{" in configurations and "}" in configurations:
        configurationsJSONString = configurations
        configurationsJSON = json.load(configurations)
    else:
        #Merge configuration jsons
        configurationsJSON = {}
        for config in configurations:
            with open(config,'r') as f:
                configurationsJSONTemp = json.load(f)
                for key in configurationsJSONTemp.keys():
                    configurationsJSON[key] = configurationsJSONTemp[key]
        configurationsJSONString = json.dumps(configurationsJSON)
    argList = [exe,"-i "+inputFile,"-o "+outputFile,"-c "+"'"+configurationsJSONString+"'",
            "-r "+str(runNumber),"-f "+str(fileNumber),"--offlineDir "+offlineDir,"-a",appendToTag,
            "-m", mergedTriggerFile]
    if drs:
        argList.append("--drs")
    if display:
        argList.append("--display "+",".join([str(x) for x in display]))
    args = " ".join(argList)

    # from subprocess import Popen, PIPE, CalledProcessError
    # with Popen(args,shell=True, stdout=PIPE, bufsize=1) as p:
    #     for line in p.stdout:
    #         print(line, end='') # process line here
    # if p.returncode != 0:
    #     raise CalledProcessError(p.returncode, p.args)
    #
    import time
    tempFileName = "stdoutput"+str(time.time())+".tmp"
    os.system(args+" | tee "+tempFileName)
    with open (tempFileName,"r") as f:
        for line in f.readlines():
            if "Overwriting sample rate" in line:
                trueRate = float(line.split("GHz")[0].split("data:")[1])
                if "pulseParams" in configurationsJSON:
                    configurationsJSON["sampleRate"] = trueRate
    os.remove(tempFileName) 

    tag = None
    if display:
        return True
    else:
        tag = validateOutput(outputFile).split("-")[0]
        #Only use short version of tag
    if publish:
        if database:
            db = mongoConnect(database)
        else:
            db = mongoConnect()
        if tag != None:  
            if appendToTag:
                tag += "_"+appendToTag
            if drs:
                inputType = "DRS"
            else:
                inputType = "MilliQan"
            publishDataset(configurationsJSON,inputFile,outputFile,fileNumber,runNumber,tag,site=site,inputType=inputType,force_publish=force_publish,db=db)
        return tag != None
def getId(runNumber,fileNumber,tag,inputType,site):
    _id = "{}_{}_{}_{}_{}".format(runNumber,fileNumber,tag,inputType,site)
    return _id

def publishDataset(configurationsJSON,inputFile,outputFile,fileNumber,runNumber,tag,site=site,inputType="MilliQan",force_publish=False,db=None,quiet=False):
    _id = getId(runNumber,fileNumber,tag,inputType,site)
    milliQanOfflineDataset = configurationsJSON
    milliQanOfflineDataset["_id"] = "{}_{}_{}_{}_{}".format(runNumber,fileNumber,tag,inputType,site)
    milliQanOfflineDataset["run"] = runNumber
    milliQanOfflineDataset["file"] = fileNumber
    milliQanOfflineDataset["version"] = tag
    milliQanOfflineDataset["location"] = os.path.abspath(outputFile)
    milliQanOfflineDataset["type"] = inputType
    milliQanOfflineDataset["site"] = site

    nX = 0
    #Check for existing entry
    for x in (db.milliQanOfflineDatasets.find({"_id" : _id})):
        nX +=1
    if nX:
        if force_publish:
            db.milliQanOfflineDatasets.replace_one({"_id": _id},milliQanOfflineDataset)
            print ("Replaced exisiting entry in database")
        else:
            print ("Entry already exists in database. To overwrite use --force_publish.")
            print("Output made successfully but not published")
            exit()
    else:
        db.milliQanOfflineDatasets.insert_one(milliQanOfflineDataset)
        if not quiet:
            print ("Added new entry in database")

if __name__ == "__main__":
    valid = runOfflineFactory(**vars(parse_args()))
    if valid:
        print("Output made successfully")

