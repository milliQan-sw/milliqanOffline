import ROOT as r
import os
import pandas as pd
import shutil
import sys
sys.path.append('../utilities')
from utilities import *

def checkBeam(mqLumis, run, file, branch='beam'):
    #print("check beam run {} file {}".format(run, file))
    beam = mqLumis[branch].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)]
    if beam.size == 0: return None
    beam = beam.values[0]
    return beam

def checkGoodRun(goodRuns, run, file, branch='goodRunTight'):
    goodRun = goodRuns[branch].loc[(goodRuns['run'] == run) & (goodRuns['file'] == file)].values
    if len(goodRun) == 1:
        return goodRun[0]
    return False

shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', os.getcwd())
shutil.copy('/eos/experiment/milliqan/Configs/goodRunsList.json', os.getcwd())

mqLumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')
goodRuns = pd.read_json('goodRunsMerged.json', orient = 'split', compression = 'infer')

########################################################
################### Settings ##########################
directory = '/store/user/milliqan/trees/v35/bar/1500/'
outputName = 'MilliQan_Run1500_v35_signalSkim3Line_beamOff_tight.root'
beam = False
goodRun = 'goodRunTight'
#######################################################

mychain = r.TChain('t')
filesProcessed = 0

filelist = []

for ifile, filename in enumerate(os.listdir(directory)):
    #if filesProcessed > 100: break
    if not filename.endswith('root'): continue
    fin = r.TFile.Open(directory+filename)
    if fin.IsZombie(): 
        print("File {} is a zombie".format(filename))
        fin.Close()
        continue
    fin.Close()

    run = int(filename.split('Run')[1].split('.')[0])
    file = int(filename.split('.')[1].split('_')[0])

    #check if there is beam if desired
    if beam is not None:
        beamOn = checkBeam(mqLumis, run, file, branch='beamInFill')
        if beamOn == None: continue
        if (beam and not beamOn) or (not beam and beamOn): continue

    #print("file {} passes beam criteria".format(filename))
    #check good runs list
    if goodRun is not None:
        isGoodRun = checkGoodRun(goodRuns, run, file, branch=goodRun)

        if not isGoodRun: continue

    print(filename)

    mychain.Add(directory+filename)
    filesProcessed+=1

    filelist.append(filename)

lumi, runTime = getLumiofFileList(filelist)

nEntries = mychain.GetEntries()
print("There are {} events in the chain".format(nEntries))

if nEntries > 0:
    
    #r.gROOT.LoadMacro("myLooper.C")
    r.gROOT.LoadMacro("signalSkim.C")

    mylooper = r.myLooper(mychain)

    mylooper.Loop(outputName, r.TString(str(lumi)), r.TString(str(runTime.total_seconds())))