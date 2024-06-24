import sys
sys.path.append('/root/lib/')
import os
import ROOT as r
import pandas as pd
import json
import shutil

shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', os.getcwd())
mqLumis = pd.read_json('mqLumis.json', orient='split', compression='infer')

def checkBeam(mqLumis, filename):
    run = int(filename.split('Run')[1].split('.')[0])
    file = int(filename.split('.')[1].split('_')[0])
    return mqLumis['beam'].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)].values[0]

# Define the range of runs
start_run = 1040
end_run = 1049
dataDir = '/store/user/milliqan/trees/v34/1000/'  # Base directory for data

# Create TChain that will read in tree with name t
mychain = r.TChain('t')

# Loop through the range of runs and add files to the TChain
for run in range(start_run, end_run + 1):
    for filename in os.listdir(dataDir):
        if not filename.endswith('.root'): continue
        if f'Run{run}' in filename:
            print(f"Adding file {filename} from run {run} to the chain")
            if checkBeam(mqLumis, filename):
                mychain.Add(dataDir + filename)

# Print the number of entries in the TChain
entries = mychain.GetEntries()
print(f"There are {entries} total entries in the chain")

# Ensure there are entries before proceeding
if entries > 0:
    # Select only the events with hits in front and back slab with area > 100k
    mychain.Draw(">>eList", "MaxIf$(area, chan==74) > 100000 && MaxIf$(area, chan==75) > 100000", "entryList")
    eList = r.gDirectory.Get("eList")

    # Check if eList is valid
    if eList:
        print(f"Number of selected entries: {eList.GetN()}")  # Debug print to check selected entries
        mychain.SetEntryList(eList)

        if eList.GetN() > 0:
            # Create a canvas and draw the time difference 
            c1 = r.TCanvas("c1", "c1", 600, 600)
            mychain.Draw("MaxIf$(timeFit_module_calibrated, chan==75&&area==MaxIf$(area,chan==75)) - MaxIf$(timeFit_module_calibrated, chan==74&&area==MaxIf$(area,chan==74)) >> h_timeDiff")
            h_timeDiff = r.gDirectory.Get('h_timeDiff')

            if h_timeDiff:
                print(f"Number of entries in histogram: {h_timeDiff.GetEntries()}")  # Debug print to check histogram entries
                if h_timeDiff.GetEntries() > 0:
                    c1.Draw()
                    # Save the output in a root file
                    # Create the output root file
                    fout = r.TFile(f"Run{start_run}to{end_run}timingCorrection.root", 'RECREATE')
                    
                    # Switch to our root file for writing
                    fout.cd()

                    # Write the plot to the file
                    h_timeDiff.Write()

                    # Close the file
                    fout.Close()
                else:
                    print("The histogram has no entries.")
            else:
                print("The histogram 'h_timeDiff' was not created.")
        else:
            print("No entries matched the selection criteria.")
    else:
        print("Failed to create entry list; check selection criteria.")
else:
    print("No entries in the TChain; check if files were added correctly.")
