import sys
sys.path.append('/root/lib/')
import os
import ROOT as r
import pandas as pd
import json
import shutil

#%jsroot on

shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', os.getcwd())
mqLumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')

def checkBeam(mqLumis, filename):
    run = int(filename.split('Run')[1].split('.')[0])
    file = int(filename.split('.')[1].split('_')[0])
    return mqLumis['beam'].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)].values[0]

#create root TChain of files for a given run
run = 1000######################################################################################################################################
dataDir = '/store/user/milliqan/trees/v34/1000/'###################################################################################################

#create tchain that will read in tree with name t
mychain = r.TChain('t') 

#add files to mychain
for filename in os.listdir(dataDir):
    if not filename.endswith('.root'): continue
    if 'Run{}'.format(run) in filename:
        print("Adding file {} to the chain".format(filename))
        if checkBeam(mqLumis, filename):
            mychain.Add(dataDir + filename)

#print the number of entries in my tchain
entries = mychain.GetEntries()
print("There are {} total entries in the chain".format(entries))

#select only the events with hits in front and back slab with area > 100k
mychain.Draw(">>eList", "MaxIf$(area, chan==74) > 100000 && MaxIf$(area, chan==75) > 100000", "entryList")
eList = r.gDirectory.Get("eList")
print(f"Number of selected entries: {eList.GetN()}")  # Debug print to check selected entries
mychain.SetEntryList(eList)

if eList.GetN() > 0:
    #create a canvas and draw the time difference 
    c1 = r.TCanvas("c1", "c1", 600, 600)
    mychain.Draw("MaxIf$(timeFit_module_calibrated, chan==75&&area==MaxIf$(area,chan==75)) - MaxIf$(timeFit_module_calibrated, chan==74&&area==MaxIf$(area,chan==74)) >> h_timeDiff")
    h_timeDiff = r.gDirectory.Get('h_timeDiff')

    if h_timeDiff:
        print(f"Number of entries in histogram: {h_timeDiff.GetEntries()}")  # Debug print to check histogram entries
        if h_timeDiff.GetEntries() > 0:
            c1.Draw()
            #save the output in a root file
            #create the output root file
            fout = r.TFile("Run1000timingCorrection.root", 'RECREATE')##########################################################################################
            
            #switch to our root file for writing
            fout.cd()

            #write the plot to the file
            h_timeDiff.Write()

            #close the file
            fout.Close()
        else:
            print("The histogram has no entries.")
    else:
        print("The histogram 'h_timeDiff' was not created.")
else:
    print("No entries matched the selection criteria.")
