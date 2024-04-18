#!/usr/bin/python3
#only works at UCSB
from subprocess import call
from runOfflineFactory import runOfflineFactory
from subprocess import check_output
import argparse
import json, math
import ROOT as r
import findEvents
import os
exeTemp="./exe/v{}.exe"

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-s","--selection",help="root selection string",type=str)
    parser.add_argument("-t","--tag",help="tag for display",type=str,default="")
    parser.add_argument("-r","--run",help="run number",type=int,required=True)
    parser.add_argument("-m","--maxEvents",help="max events to display",type=int,default=10)
    parser.add_argument("-v","--version",help="version number",type=int,default=34)
    parser.add_argument("--formosa",help="formosa config",default=True,action="store_true")
    args = parser.parse_args()
    return args

def makeEventDisplays(selection,run,version,tag,maxEvents,formosa):
    inDir1 = int(run/100)*100
    inDir2 = "000"+str(int(run%100/10))
    offlineDir = "/eos/experiment/formosa/commissioning/data/offline/v{0}/{1}/{2}/MilliQan_Run{3}.*_v{0}.root".format(version,inDir1,inDir2,run)
    # offlineDir = "/net/cms26/cms26r0/milliqan/Run3Offline/v{1}/{0}/MilliQan_Run{0}.*_v{1}.root".format(run,version)
    chain = r.TChain("t")
    chain.Add(offlineDir)
    table = findEvents.main(chain,run,maxEvents,tag,selection)
    exe = exeTemp.format(version)
    for run,fileNumber,eventNumber in table:
        inDir1 = int(run/100)*100
        inDir2 = "000"+str(int(run%100/10))
        inputFile = "/eos/experiment/formosa/commissioning/data/DAQ/{}/{}/MilliQan_Run{}.{}_default.root".format(inDir1,inDir2,run,fileNumber)
        runOfflineFactory(inputFile,"temp.root",exe,None,False,force_publish=False,database=None,appendToTag=tag,mergedTriggerFile="",drs=False,display=[eventNumber],slab=False,formosa=formosa,runNumber=run,fileNumber=fileNumber)
        # os.system("python3 scripts/runOfflineFactory.py -i /net/cms26/cms26r0/milliqan/Run3/MilliQan_Run{}.{}_default.root --display {} -o temp.root -e exe/v31.exe -a {}".format(run,fileNumber,eventNumber,tag))


if __name__ == "__main__":
    makeEventDisplays(**vars(parse_args()))

