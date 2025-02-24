import ROOT as r
import os
import pandas as pd
import shutil
import sys
sys.path.append('../utilities')
from utilities import *

########################################################
################### Settings ##########################
directory = '/store/user/milliqan/trees/v35/slab/1000/MilliQanSlab_Run1089.63_v35.root'
outputName = 'MilliQan_Run1000_v35_cosmic_beamOff_tight_slab.root'
beam = False
goodRun = 'goodRunTight'
skimType = 'cosmic'
debug=False
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
    if debug and filesProcessed > 100: break
    if not filename.endswith('root'): continue
    fin = r.TFile.Open(directory+filename)
    if fin.IsZombie(): 
        print("File {} is a zombie".format(filename))
        fin.Close()
        continue
    fin.Close()

    run = int(filename.split('Run')[1].split('.')[0])
    file = int(filename.split('.')[1].split('_')[0])

    print(filename)

    mychain.Add(directory+filename)
    filesProcessed+=1

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
