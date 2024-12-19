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


Simcuts = milliqanCuts()


simPlotter = milliqanPlotter()

sim_file_list = ['cosmicMuonRun3MilliQan_waveinjected_v3_processed.root'] #can be found at /eos/experiment/milliqan/sim/bar/cosmics



sim_file_list = [filename+":t" for filename in sim_file_list]


branches = [ 'fileNumber', 'pickupFlag', 'runNumber',
            'tTrigger', 'event', 'boardsMatched', 'height', 'area',
            'chan', 'row', 'column', 'layer', 'nPE', 'riseSamples',
            'fallSamples', 'npulses', 'timeFit_module_calibrated',
            'duration','type','ipulse']


simPickupCut = Simcuts.getCut(Simcuts.pickupCut, 'pickupCut',
                        cut=True, branches=branches) 


firstPulseCut= Simcuts.getCut(Simcuts.firstPulseCut,'firstPulse', cut=True, branches=branches)


NuniqueBarSim = r.TH1F("NuniqueBarSim" , "NuniqueBar with bar counting TH nPE >= 1;number of unique bar;events",50,0,50)
NPEDistSim = r.TH1F("NPEDistSim", "nPE; nPE ; bar", 500, 0, 1000)
DtmaxSim = r.TH1F("DtmaxSim", "Dt max", 30, -30, 30)


countbarEvent = Simcuts.getCut(Simcuts.countNBars, 'countNBars',pulseBase = False,nPECut = 2 )
simPlotter.addHistograms(NuniqueBarSim, 'countNBars', 'CosmicTG')
simPlotter.addHistograms(NPEDistSim, 'lnPE', 'CosmicTG')
simPlotter.addHistograms(DtmaxSim, 'timeDiff_simValid', 'CosmicTG')



SimCutflow = [simPickupCut,firstPulseCut,Simcuts.CosmicTG,countbarEvent,Simcuts.lnPE,Simcuts.timeDiff_simValid,simPlotter.dict['NuniqueBarSim'],simPlotter.dict['NPEDistSim'] ,simPlotter.dict['DtmaxSim']]



schedule_sim = milliQanScheduler(SimCutflow, Simcuts, simPlotter)
iterator_sim = milliqanProcessor(sim_file_list, branches, schedule_sim,
                                 Simcuts, simPlotter, qualityLevel='override',step_size=110000)

iterator_sim.run()



#------------offline file analysis part--------------------------
Offline_file = ['MilliQan_Run1700_v35_signal_beamOff_tight.root'] #can be found at /eos/experiment/milliqan/skims/signal/MilliQan_Run1700_v35_signal_beamOff_tight.root

Offline_file_list = [filename+":t" for filename in Offline_file]

Offlinecuts =milliqanCuts()
OfflinePlotter = milliqanPlotter()

Offlinebranches = ['fileNumber', 'pickupFlag', 'runNumber',
            'tTrigger', 'event', 'boardsMatched', 'height', 'area',
             'row', 'column', 'layer', 'nPE', 'riseSamples',
            'fallSamples', 'npulses', 'timeFit_module_calibrated',
            'duration','type','ipulse','beamOn']

OffLinePickupCut = Offlinecuts.getCut(Offlinecuts.pickupCut, 'pickupCut',
                        cut=True, branches=Offlinebranches) 

OfflinefirstPulseCut= Offlinecuts.getCut(Offlinecuts.firstPulseCut,'firstPulse', cut=True, branches=branches)


CosmicTGOL = Offlinecuts.getCut(Offlinecuts.CosmicTG,"CosmicTG",cut=False, branches=branches , Offline = True)
NuniqueBarOffline = r.TH1F("NuniqueBarOffline" , "NuniqueBar with bar counting TH nPE >= 1;number of unique bar;events",50,0,50)
NPEDistOffline = r.TH1F("NPEDistOffline", "nPE; nPE ; events", 500, 0, 1000)
DtmaxOffline = r.TH1F("DtmaxOffline", "Dt max; ns; events  ", 30, -30, 30)

countbarEventOL = Offlinecuts.getCut(Offlinecuts.countNBars, 'countNBars',pulseBase = False,nPECut = 2 )
OfflinePlotter.addHistograms(NuniqueBarOffline, 'countNBars', 'CosmicTG')
OfflinePlotter.addHistograms(NPEDistOffline, 'lnPE', 'CosmicTG')
OfflinePlotter.addHistograms(DtmaxOffline, 'timeDiff_simValid', 'CosmicTG')


#OfflineCutflow = [OffLinePickupCut,OfflinefirstPulseCut,CosmicTGOL,countbarEventOL,Offlinecuts.lnPE,Offlinecuts.timeDiff_simValid,OfflinePlotter.dict['NuniqueBarOffline'],OfflinePlotter.dict['NPEDistOffline'] ,OfflinePlotter.dict['DtmaxOffline']] 
OfflineCutflow = [OffLinePickupCut] 

schedule_offline = milliQanScheduler(OfflineCutflow, Offlinecuts, OfflinePlotter)
iterator_OL = milliqanProcessor(Offline_file_list, Offlinebranches, schedule_offline,
                                 Offlinecuts, OfflinePlotter, qualityLevel='override',step_size=110000)

iterator_OL.run()


output_file = r.TFile.Open("comparison.root", "RECREATE")
DtmaxSim.Write()
NPEDistSim.Write()
NuniqueBarSim.Write()
DtmaxOffline.Write()
NPEDistOffline.Write()
NuniqueBarOffline.Write()

output_file.Close()
#mycuts.cutflowCounter("comparisonstSim"
