import sys
import os
sys.path.append(os.path.join(os.getcwd(), "../utilities"))

import ROOT as r

from milliqanProcessor import milliqanProcessor
from milliqanScheduler import milliQanScheduler
from milliqanCuts import milliqanCuts
from milliqanPlotter import milliqanPlotter

r.gROOT.SetBatch(True) # Disable drawing of figures to screen

import json


mycuts = milliqanCuts()

simPlotter = milliqanPlotter()

sim_file_list = ['cosmicMuonRun3MilliQan_waveinjected_v3_processed.root']

sim_file_list = [filename+":t" for filename in sim_file_list]

branches = [ 'fileNumber', 'pickupFlag', 'runNumber',
            'tTrigger', 'event', 'boardsMatched', 'height', 'area',
            'chan', 'row', 'column', 'layer', 'nPE', 'riseSamples',
            'fallSamples', 'npulses', 'timeFit_module_calibrated',
            'duration','type','ipulse']


simPickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut',
                        cut=True, branches=branches) 


firstPulseCut= mycuts.getCut(mycuts.firstPulseCut,'firstPulse', cut=True, branches=branches)


NuniqueBarSim = r.TH1F("NuniqueBarSim" , "NuniqueBar with bar counting TH nPE >= 1;number of unique bar;events",50,0,50)
NPEDistSim = r.TH1F("NPEDistSim", "nPE; nPE ; bar", 500, 0, 1000)
DtmaxSim = r.TH1F("DtmaxSim", "Dt max", 30, -30, 30)


countbarEvent = mycuts.getCut(mycuts.countNBars, 'countNBars',pulseBase = False,nPECut = 2 )
simPlotter.addHistograms(NuniqueBarSim, 'countNBars', 'CosmicTG')
simPlotter.addHistograms(NPEDistSim, 'lnPE', 'CosmicTG')
simPlotter.addHistograms(DtmaxSim, 'timeDiff_simValid', 'CosmicTG')



SimCutflow = [simPickupCut,firstPulseCut,mycuts.CosmicTG,countbarEvent,mycuts.lnPE,mycuts.timeDiff_simValid,simPlotter.dict['NuniqueBarSim'],simPlotter.dict['NPEDistSim'] ,simPlotter.dict['DtmaxSim']]



schedule_sim = milliQanScheduler(SimCutflow, mycuts, simPlotter)
iterator_sim = milliqanProcessor(sim_file_list, branches, schedule_sim,
                                 mycuts, simPlotter, qualityLevel='override',step_size=110000)

iterator_sim.run()

output_file = r.TFile.Open("comparison.root", "RECREATE")
DtmaxSim.Write()
NPEDistSim.Write()
NuniqueBarSim.Write()
output_file.Close()
#mycuts.cutflowCounter("comparisonstSim"
