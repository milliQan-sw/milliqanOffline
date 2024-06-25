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
    try:
        run = int(filename.split('Run')[1].split('.')[0])
        file = int(filename.split('.')[1].split('_')[0])
        beam_value = mqLumis['beam'].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)].values[0]
        return beam_value
    except Exception as e:
        print(f"Error in checkBeam for file {filename}: {e}")
        return False

# Define the range of runs
start_run = 1550
end_run = 1559
dataDir = '/store/user/milliqan/trees/v34/1500/'  # Base directory for data

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
            else:
                print(f"Beam check failed for file {filename}")

# Print the number of entries in the TChain
entries = mychain.GetEntries()
print(f"There are {entries} total entries in the chain")

# Create the output root file
fout = r.TFile(f"Run{start_run}to{end_run}timingCorrection.root", 'RECREATE')
fout.cd()

# Create an empty histogram
h_timeDiff = r.TH1F("h_timeDiff", "Time Difference", 100, -50, 50)  # Adjust bins and range as needed

# Ensure there are entries before proceeding
if entries > 0:
    # Select only the events with hits in front and back slab with area > 100k
    mychain.Draw(">>eList", "MaxIf$(area, chan==74) > 100000 && MaxIf$(area, chan==75) > 100000", "entryList")
    eList = r.gDirectory.Get("eList")

    # Check if eList is valid
    if eList and isinstance(eList, r.TEntryList):
        print(f"Number of selected entries: {eList.GetN()}")  # Debug print to check selected entries
        mychain.SetEntryList(eList)

        if eList.GetN() > 0:
            # Create a canvas and draw the time difference 
            c1 = r.TCanvas("c1", "c1", 600, 600)
            draw_command = "MaxIf$(timeFit_module_calibrated, chan==75&&area==MaxIf$(area,chan==75)) - MaxIf$(timeFit_module_calibrated, chan==74&&area==MaxIf$(area,chan==74)) >> h_timeDiff"
            mychain.Draw(draw_command)
            h_timeDiff = r.gDirectory.Get('h_timeDiff')

            if h_timeDiff and isinstance(h_timeDiff, r.TH1):
                print(f"Number of entries in histogram: {h_timeDiff.GetEntries()}")  # Debug print to check histogram entries
                if h_timeDiff.GetEntries() > 0:
                    c1.Draw()
                else:
                    print("The histogram has no entries.")
            else:
                print("The histogram 'h_timeDiff' was not created or is not a TH1 object.")
        else:
            print("No entries matched the selection criteria.")
    else:
        print("Failed to create entry list or eList is not a TEntryList object.")
else:
    print("No entries in the TChain.")

# Write the plot to the file
h_timeDiff.Write()

# Close the file
fout.Close()