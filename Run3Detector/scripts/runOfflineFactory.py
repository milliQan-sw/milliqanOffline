#!/usr/bin/python3
import os, sys, re
import json
import ROOT as r
r.gROOT.SetBatch()
import glob
import math
from subprocess import call
import argparse
import traceback
from pprint import pprint
from mongoConnect import mongoConnect
from subprocess import Popen, PIPE
import pandas as pd
import numpy as np
from datetime import datetime

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
    parser.add_argument("-p","--publish",help="Publish dataset",nargs="?",const=True,type=str,default=False)
    parser.add_argument("-f","--force_publish",help="Force publish dataset",action="store_true",default=False)
    parser.add_argument("-c","--configurations",help="JSON Configuration files or string",type=str,nargs="+")
    parser.add_argument("--drs",help="DRS input",action="store_true",default=False)
    parser.add_argument("--display",help="Display events",type=int,nargs="+")
    parser.add_argument("--slab", help="Forces slab detector configuration", action="store_true", default=False)
    parser.add_argument("--sim", help="Forces sim configuration", action="store_true", default=False)
    args = parser.parse_args()
    return args
def validateOutput(outputFile,runNumber=-1,fileNumber=-1):
    foundBad = False
    try:
        f1 = r.TFile(outputFile,"READ")
        t = f1.Get("t")
        nevts = t.GetEntries()
        print("Output file {} has {} events".format(outputFile, nevts))
        # print "[RSR] ntuple has %i events and expected %i" % (t.GetEntries(), expectednevts)
        # if int(expectednevts) > 0 and int(t.GetEntries()) != int(expectednevts):
        #     print "[RSR] nevents mismatch"
        #     foundBad = True
        tagObj = f1.Get("tag")
        if not tagObj:
            tagObj = f1.Get("tag_{}_{}".format(runNumber,fileNumber))
        tag = tagObj.GetTitle()
        f1.Close()
    except Exception as ex:
        msg = traceback.format_exc()
        if "EDProductGetter" not in msg:
            tag = None
    if tag==None:
        print ("removing output file because it does not deserve to live (result will not be published)")
        os.system("rm "+outputFile)
    return tag 
def runOfflineFactory(inputFile,outputFile,exe,configurations,publish,force_publish,database,appendToTag,mergedTriggerFile,drs,display, slab, sim, runNumber=None,fileNumber=None):
    if force_publish and not publish:
        publish = True
    if runNumber == None:
        try:
            if drs:
                runNumber = int(inputFile.split("/")[-1].split("CMS")[-1].split(".")[0])
                fileNumber = int(1)
            elif sim:
                runNumber = int(1)
                fileNumber = int(1)
            else:
                runNumber = int(inputFile.split("/")[-1].split("Run")[-1].split(".")[0])
                fileNumber = int(inputFile.split("/")[-1].split(".")[1].split("_")[0]) 
                print("Run, {}, File, {}".format(inputFile.split("/")[-1].split("Run")[-1].split(".")[0], inputFile.split("/")[-1].split(".")[1].split("_")[0]))   
        except:
            if publish:
                print ("Could not identify file and/or run number so cannot publish")
                exit()
            fileNumber = -1
            runNumber = -1
    if display and publish:
        print("Can't publish in display mode!")
        exit()
    
    #copy files from eos
    if not sim:
        copyFromEOS()

    offlineDir = os.getenv("OFFLINEDIR")
    if not configurations:
        if drs:
            configurations = [offlineDir+"/configuration/pulseFinding/pulseFindingDRS.json"]
        if slab:
            chanConfig = offlineDir + "/configuration/slabConfigs/" + getConfigs(runNumber, offlineDir+'/configuration/slabConfigs') + '.json'
            print("Using the chan config", chanConfig)
            configurations = [chanConfig, offlineDir+"/configuration/pulseFinding/pulseFindingSlab.json"]
        if sim:
            print("Using sim config file")
            chanConfig = offlineDir + '/configuration/barConfigs/simConfig.json'
            configurations = [chanConfig, offlineDir+"/configuration/pulseFinding/pulseFindingBar.json"]
        else:
            chanConfig = offlineDir + "/configuration/barConfigs/" + getConfigs(runNumber, offlineDir+'/configuration/barConfigs') + '.json'
            print("Using the chan config", chanConfig)
            configurations = [chanConfig,offlineDir+"/configuration/pulseFinding/pulseFindingBar.json"]

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
            "-r "+str(runNumber),"-f "+str(fileNumber),"--offlineDir "+offlineDir,"-a",appendToTag]
    if mergedTriggerFile != "":
            argList.append("-m "+mergedTriggerFile)
    if drs:
        argList.append("--drs")
    if display:
        argList.append("--display "+",".join([str(x) for x in display]))
    if slab:
        argList.append("--slab")
    if sim:
        argList.append("--sim")
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
        tag = validateOutput(outputFile,runNumber,fileNumber).split("-")[0]
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
            elif slab:
                inputType = 'MilliQanSlab'
            else:
                inputType = "MilliQan"
            matched = mergedTriggerFile!="" 
            publishing_inputs = {
                'configurationsJSON': configurationsJSON,
                'inputFile': inputFile,
                'outputFile': os.path.abspath(outputFile),
                'fileNumber': fileNumber,
                'runNumber': runNumber,
                'tag': tag,
                'site': site,
                'inputType': inputType,
                'matched': matched
            }
            if publish and isinstance(publish, str):
                publish = eval(publish)
                for k, v in publish.items():
                    publishing_inputs[k] = v
            publishDataset(publishing_inputs['configurationsJSON'],publishing_inputs['inputFile'],publishing_inputs['outputFile'], publishing_inputs['fileNumber'],
                           publishing_inputs['runNumber'],publishing_inputs['tag'],site=publishing_inputs['site'],inputType=publishing_inputs['inputType'],matched=publishing_inputs['matched'],
                           force_publish=force_publish,db=db)
        return tag != None
def getId(runNumber,fileNumber,tag,inputType,site):
    _id = "{}_{}_{}_{}_{}".format(runNumber,fileNumber,tag,inputType,site)
    return _id

def publishDataset(configurationsJSON,inputFile,outputFile,fileNumber,runNumber,tag,site=site,inputType="MilliQan",matched=False,force_publish=False,db=None,quiet=False):
    _id = getId(runNumber,fileNumber,tag,inputType,site)
    milliQanOfflineDataset = configurationsJSON
    milliQanOfflineDataset["_id"] = "{}_{}_{}_{}_{}".format(runNumber,fileNumber,tag,inputType,site)
    milliQanOfflineDataset["run"] = runNumber
    milliQanOfflineDataset["file"] = fileNumber
    milliQanOfflineDataset["version"] = tag
    milliQanOfflineDataset["location"] = outputFile
    milliQanOfflineDataset["type"] = inputType
    milliQanOfflineDataset["site"] = site
    milliQanOfflineDataset["matched"] = matched
    
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
            return False
    else:
        db.milliQanOfflineDatasets.insert_one(milliQanOfflineDataset)
        if not quiet:
            print ("Added new entry in database")
    return True

def getConfigs(runNum, offlineDir):
    if runNum == -1 and 'barConfigs' in offlineDir: return 'configRun1296_present'
    elif runNum == -1 and 'slabConfigs' in offlineDir: return 'configRun0_present'
    fin = open(offlineDir+"/runInfo.json")
    runs = json.load(fin)
    fin.close()
    for key, value in runs.items():
        #print(key, value)
        if len(value) > 1:
            if value[0] <= runNum <= value[1]: return key
        else:
            #print(runNum)
            if runNum >= value[0]: return key
    print("Did not find the correct channel map for run {}".format(runNum))
    sys.exit(1)

def copyFromEOS(slab=False):

    if not slab and os.path.exists('configuration/barConfigs/goodRunsList.json'): 
        print("Warning (runOfflineFactory.py): goodRunsList.json is not available locally, trying to access from eos")
        try:
            os.system('cp /eos/experiment/milliqan/Configs/goodRunsList.json configuration/slabConfigs/')
        except:
            print("Error (runOfflineFactory.py): could not access the goodRunList.json on eos or locally")
    
    if not slab:
        if not os.path.exists('configuration/barConfigs/mqLumis.json'):
            print("Warning (runOfflineFactory.py): mqLumis.json is not available locally, trying to access from eos")
            try:
                os.system('cp /eos/experiment/milliqan/Configs/mqLumis.json configuration/barConfigs/')
            except:
                print("Error (runOfflineFactory.py): unable to access the mqLumis file on eos or locally")
        
    #make datetimes into uint64 to be read by c++
    lumis = pd.read_json('configuration/barConfigs/mqLumis.json', orient = 'split', compression = 'infer')
    convert_cols = ['start', 'stop', 'fillStart', 'fillEnd', 'startStableBeam', 'endStableBeam']

    for col in convert_cols:
        lumis[col] = convertTimes(lumis[col])
    lumis.to_json('configuration/barConfigs/mqLumis.json', orient = 'split', compression = 'infer', index = 'true')

def convertTimes(input):
    input = input.apply(datetime_to_uint64)
    return input

def datetime_to_uint64(x):
    if isinstance(x, str):  # If x is a string
        dt = datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ')
        return np.uint64(dt.timestamp())
    elif isinstance(x, list):  # If x is a list
        timestamps = [datetime_to_uint64(item) for item in x]
        return timestamps
    return x  # Return unchanged if x is None or some other non-string value

if __name__ == "__main__":
    valid = runOfflineFactory(**vars(parse_args()))
    if valid:
        print("Output made successfully")

