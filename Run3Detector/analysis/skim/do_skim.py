import ROOT as r
import os
import pandas as pd
import shutil

def checkBeam(mqLumis, run, file, branch='beam'):
    print("check beam run {} file {}".format(run, file))
    beam = mqLumis[branch].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)]
    if beam.size == 0: return None
    beam = beam.values[0]
    return beam

def checkGoodRun(goodRuns, run, file, branch='goodRunTight'):
    goodRun = goodRuns[branch].loc[(goodRuns['run'] == run) & (goodRuns['file'] == file)].values
    if len(goodRun) == 1:
        return goodRun[0]
    return False

# Copying configuration files
print("Copying configuration files...")
shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', os.getcwd())
shutil.copy('/eos/experiment/milliqan/Configs/goodRunsList.json', os.getcwd())

# Loading JSON files into DataFrames
print("Loading JSON files...")
mqLumis = pd.read_json('mqLumis.json', orient='split', compression='infer')
goodRuns = pd.read_json('goodRunsList.json', orient='split', compression='infer')

########################################################
################### Settings ##########################
directory = '/store/user/milliqan/trees/v35/bar/1700/'
outputName = os.path.join(os.getcwd(), 'MilliQan_Run1700_v35_skim_beamOff_tight.root')  # Save to current directory
beam = False
goodRun = 'goodRunTight'
#######################################################

# Initializing TChain
mychain = r.TChain('t')
print("Initialized TChain.")

for ifile, filename in enumerate(os.listdir(directory)):
    # Uncomment the following line to limit the number of processed files for testing
    # if ifile > 100: break
    if not filename.endswith('root'): 
        continue

    print(f"Processing file: {filename}")
    
    fin = r.TFile.Open(directory + filename)
    if fin.IsZombie():
        print(f"File {filename} is a zombie. Skipping...")
        fin.Close()
        continue
    fin.Close()

    run = int(filename.split('Run')[1].split('.')[0])
    file = int(filename.split('.')[1].split('_')[0])

    # Check if there is beam if desired
    if beam is not None:
        beamOn = checkBeam(mqLumis, run, file, branch='beamInFill')
        if beamOn is None: 
            print(f"Beam data not found for Run {run}, File {file}. Skipping...")
            continue
        if (beam and not beamOn) or (not beam and beamOn): 
            print(f"Beam condition not met for Run {run}, File {file}. Skipping...")
            continue

    # Check good runs list
    if goodRun is not None:
        isGoodRun = checkGoodRun(goodRuns, run, file, branch=goodRun)
        if not isGoodRun: 
            print(f"Run {run}, File {file} is not in the good runs list. Skipping...")
            continue

    print(f"Adding file {filename} to the chain.")
    mychain.Add(directory + filename)

# Print the total number of entries
nEntries = mychain.GetEntries()
print(f"Total number of events in the chain: {nEntries}")

if nEntries > 0:
    print("Loading macro and starting loop...")
    r.gROOT.LoadMacro("myLooper_v2.C")
    mylooper = r.myLooper(mychain)
    mylooper.Loop(outputName)
    print(f"Loop completed. Output saved to {outputName}.")
else:
    print("No entries found in the chain. Exiting.")