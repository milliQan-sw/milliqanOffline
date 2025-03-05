import ROOT as r
import os
import pandas as pd
import shutil
import sys
sys.path.append('../utilities')
from utilities import *

########################################################
################### Settings ########################## 600 / 700 / 800 / 900 / 1000
directory = '/store/user/milliqan/trees/v35/slab/900/'
outputName = 'MilliQan_Run900_v35_cosmic_beamOff_tight_slab.root'
beam = False
goodRun = 'goodRunTight'
skimType = 'cosmic'
debug = False
#######################################################

if len(sys.argv) > 5:
    directory = sys.argv[1]
    outputName = sys.argv[2]
    beam = sys.argv[3] == "True"
    goodRun = str(sys.argv[4])
    skimType = str(sys.argv[5])
    print("processing", sys.argv)

mychain = r.TChain('t')
filesProcessed = 0

filelist = []

for ifile, filename in enumerate(os.listdir(directory)):
    if debug and filesProcessed > 100: 
        break
    if not filename.endswith('root'): 
        continue

    file_path = os.path.join(directory, filename)
    try:
        fin = r.TFile.Open(file_path)
    except Exception as e:
        print("Skipping corrupted file: {}".format(filename))
        continue

    # Check if file failed to open or is a zombie (corrupted/truncated)
    if not fin or fin.IsZombie():
        print("Skipping corrupted file: {}".format(filename))
        if fin:
            fin.Close()
        continue
    fin.Close()

    run = int(filename.split('Run')[1].split('.')[0])
    file = int(filename.split('.')[1].split('_')[0])

    print(filename)

    mychain.Add(file_path)
    filesProcessed += 1
    filelist.append(filename)

lumi, runTime = getLumiofFileList(filelist)

nEntries = mychain.GetEntries()
print("There are {} events in the chain".format(nEntries))

if nEntries > 0:
    
    if skimType == 'beam':
        r.gROOT.LoadMacro("beamMuonSkim.C")
    elif skimType == 'cosmic':
        r.gROOT.LoadMacro("cosmicSkimSlab.C")
    elif skimType == 'signal':
        r.gROOT.LoadMacro("signalSkim.C")

    mylooper = r.myLooper(mychain)
    mylooper.Loop(outputName, r.TString(str(lumi)), r.TString(str(runTime.total_seconds())))