#!/usr/bin/python3
from subprocess import call
from runOfflineFactory import runOfflineFactory
from subprocess import check_output
import argparse
import json, math
import ROOT as r
import findEvents
import os
exe="./exe/v32.exe"

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-s","--selection",help="root selection string",type=str)
    parser.add_argument("-t","--tag",help="tag for display",type=str,default="")
    parser.add_argument("-r","--run",help="run number",type=int,required=True)
    parser.add_argument("-m","--maxEvents",help="max events to display",type=int,default=10)
    parser.add_argument("-v","--version",help="version number",type=int,default=32)
    args = parser.parse_args()
    return args

def makeEventDisplays(selection,run,version,tag,maxEvents):
    offlineDir = "/net/cms26/cms26r0/milliqan/Run3Offline/v{1}/MilliQan_Run{0}.*_default_v{1}.root".format(run,version)
    chain = r.TChain("t")
    chain.Add(offlineDir)
    table = findEvents.main(chain,run,maxEvents,tag,selection)
    for run,fileNumber,eventNumber in table:
        inputFile = "/net/cms26/cms26r0/milliqan/Run3/MilliQan_Run{}.{}_default.root".format(run,fileNumber)
        runOfflineFactory(inputFile,"temp.root",exe,None,False,force_publish=False,database=None,appendToTag=tag,mergedTriggerFile="",drs=False,display=[eventNumber],runNumber=run,fileNumber=fileNumber)
        # os.system("python3 scripts/runOfflineFactory.py -i /net/cms26/cms26r0/milliqan/Run3/MilliQan_Run{}.{}_default.root --display {} -o temp.root -e exe/v31.exe -a {}".format(run,fileNumber,eventNumber,tag))


if __name__ == "__main__":
    makeEventDisplays(**vars(parse_args()))

