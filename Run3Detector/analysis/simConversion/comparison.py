import sys
import os
sys.path.append(os.path.join(os.getcwd(), "../utilities"))

import ROOT as r

from milliqanProcessor import milliqanProcessor
from milliqanScheduler import milliQanScheduler
from milliqanCuts import milliqanCuts
from milliqanPlotter import milliqanPlotter

r.gROOT.SetBatch(True) # Disable drawing of figures to screen

data_directory = '~/Documents/Data/MilliQan/'

sim_file_list = ['bar_cosmic_sim_processed.root']

data_file_list = ['MilliQan_Run1900.110_v35.root',
                  # 'MilliQan_Run1900.111_v35.root',
                  # 'MilliQan_Run1900.112_v35.root',
                  # 'MilliQan_Run1900.113_v35.root',
                  # 'MilliQan_Run1900.114_v35.root',
                  # 'MilliQan_Run1900.115_v35.root',
                  # 'MilliQan_Run1900.116_v35.root',
                  # 'MilliQan_Run1900.117_v35.root',
                  # 'MilliQan_Run1900.118_v35.root',
                  # 'MilliQan_Run1900.119_v35.root'
                   ]

sim_file_list = [data_directory+filename+":t" for filename in sim_file_list]
data_file_list = [data_directory+filename+":t" for filename in data_file_list]


# The milliqanProcessor always needs fileNumber, pickupFlag, runNumber,
# tTrigger, event, and boardsMatched
branches = ['fileNumber', 'pickupFlag', 'runNumber',
            'tTrigger', 'event', 'boardsMatched', 'height', 'area',
            'chan', 'row', 'column', 'layer', 'nPE', 'riseSamples',
            'fallSamples', 'npulses', 'time_module_calibrated',
            'duration'
            ]

cuts = milliqanCuts() 

# Cuts made to hypothetically make data match sim considering
# that sim data would not have pickup and would always have
# boards matched
pickupCut = cuts.getCut(cuts.pickupCut, 'pickupCut',
                        cut=True, branches=branches) 
boardsMatched = cuts.getCut(cuts.boardsMatched, 'boardsMatchedCut',
                            cut=True, branches=branches)

simCuts = milliqanCuts()


# Cuts made to hypothetically make data match sim considering
# that sim data would not have pickup and would always have
# boards matched
# pickupCut = cuts.getCut(cuts.pickupCut, 'pickupCut',
#                         cut=True, branches=branches) 
# boardsMatched = cuts.getCut(cuts.boardsMatched, 'boardsMatchedCut',
#                             cut=True, branches=branches)


plotter = milliqanPlotter()
sim_plotter = milliqanPlotter()


h_height_data = r.TH1F("h_height_data", "Height", 140, 0, 1400)
h_height_sim = r.TH1F("h_height_sim", "Height", 140, 0, 1400)
h_area_data =  r.TH1F("h_area_data", "Area", 140, 0, 400000)
h_area_sim =  r.TH1F("h_area_sim", "Area", 140, 0, 400000)
h_chan_data =  r.TH1F("h_chan_data", "Channel", 80, 0, 80)
h_chan_sim =  r.TH1F("h_chan_sim", "Channel", 80, 0, 80)
h_row_data =  r.TH1F("h_row_data", "Row", 5, 0, 5)
h_row_sim =  r.TH1F("h_row_sim", "Row", 5, 0, 5)
h_column_data =  r.TH1F("h_column_data", "Column", 5, 0, 5)
h_column_sim =  r.TH1F("h_column_sim", "Column", 5, 0, 5)
h_layer_data =  r.TH1F("h_layer_data", "Layer", 5, 0, 5)
h_layer_sim =  r.TH1F("h_layer_sim", "Layer", 5, 0, 5)
h_npe_data =  r.TH1F("h_npe_data", "nPE", 5, 0, 5)
h_npe_sim =  r.TH1F("h_npe_sim", "nPE", 5, 0, 5)
h_riseSamples_data =  r.TH1F("h_riseSamples_data", "riseSamples", 15, 0, 15)
h_riseSamples_sim =  r.TH1F("h_riseSamples_sim", "riseSamples", 15, 0, 15)
h_fallSamples_data =  r.TH1F("h_fallSamples_data", "fallSamples", 30, 0, 30)
h_fallSamples_sim =  r.TH1F("h_fallSamples_sim", "riseSamples", 30, 0, 30)
h_npulses_data =  r.TH1F("h_npulses_data", "npulses", 45, 0, 45)
h_npulses_sim =  r.TH1F("h_npulses_sim", "npulses", 45, 0, 45)
h_time_data =  r.TH1F("h_time_data", "time", 500, 0, 1650)
h_time_sim =  r.TH1F("h_time_sim", "time", 500, 0, 1650)
h_duration_data =  r.TH1F("h_duration_data", "duration", 400, 0, 400)
h_duration_sim =  r.TH1F("h_duration_sim", "duration", 400, 0, 400)


# Setting up plotters
plotter.addHistograms(h_height_data, "height")
plotter.addHistograms(h_area_data, "area")
plotter.addHistograms(h_chan_data, "chan")
plotter.addHistograms(h_row_data, "row")
plotter.addHistograms(h_column_data, "column")
plotter.addHistograms(h_layer_data, "layer")
plotter.addHistograms(h_npe_data, "nPE")
plotter.addHistograms(h_riseSamples_data, "riseSamples")
plotter.addHistograms(h_fallSamples_data, "fallSamples")
plotter.addHistograms(h_npulses_data, "npulses")
plotter.addHistograms(h_time_data, "time_module_calibrated")
plotter.addHistograms(h_duration_data, "duration")

sim_plotter.addHistograms(h_height_sim, "height")
sim_plotter.addHistograms(h_area_sim, "area")
sim_plotter.addHistograms(h_chan_sim, "chan")
sim_plotter.addHistograms(h_row_sim, "row")
sim_plotter.addHistograms(h_column_sim, "column")
sim_plotter.addHistograms(h_layer_sim, "layer")
sim_plotter.addHistograms(h_npe_sim, "nPE")
sim_plotter.addHistograms(h_riseSamples_sim, "riseSamples")
sim_plotter.addHistograms(h_fallSamples_sim, "fallSamples")
sim_plotter.addHistograms(h_npulses_sim, "npulses")
sim_plotter.addHistograms(h_time_sim, "time_module_calibrated")
sim_plotter.addHistograms(h_duration_sim, "duration")

cutflow = [boardsMatched, pickupCut, plotter.dict['h_height_data'], plotter.dict['h_area_data'], plotter.dict['h_chan_data'],
           plotter.dict['h_row_data'], plotter.dict['h_column_data'], plotter.dict['h_layer_data'],
           plotter.dict['h_npe_data'], plotter.dict['h_riseSamples_data'], plotter.dict['h_fallSamples_data'],
           plotter.dict['h_npulses_data'], plotter.dict['h_time_data'], plotter.dict['h_duration_data']]

sim_cutflow = [sim_plotter.dict['h_height_sim'], sim_plotter.dict['h_area_sim'], sim_plotter.dict['h_chan_sim'],
           sim_plotter.dict['h_row_sim'], sim_plotter.dict['h_column_sim'], sim_plotter.dict['h_layer_sim'],
           sim_plotter.dict['h_npe_sim'], sim_plotter.dict['h_riseSamples_sim'], sim_plotter.dict['h_fallSamples_sim'],
           sim_plotter.dict['h_npulses_sim'], sim_plotter.dict['h_time_sim'], sim_plotter.dict['h_duration_sim']]

schedule_data = milliQanScheduler(cutflow, cuts, plotter)
schedule_sim = milliQanScheduler(sim_cutflow, simCuts, sim_plotter)

iterator = milliqanProcessor(data_file_list, branches, schedule_data,
                             cuts, plotter, qualityLevel='override')
iterator_sim = milliqanProcessor(sim_file_list, branches, schedule_sim,
                                 simCuts, sim_plotter, qualityLevel='override')

iterator.run()
iterator_sim.run()


output_file = r.TFile.Open("comparison.root", "RECREATE")

 # Plot histograms
for data, sim in zip(list(plotter.dict.keys()),
                    list(sim_plotter.dict.keys())):
    print(data, sim)
    variable = data.split("_")[1]
    canvas = r.TCanvas(f"{variable}Canvas", f"{variable}Canvas", 600, 600)
    canvas.cd()


    
    eval(f"{sim}.SetLineColor(r.kRed)")
    eval(f"{data}.SetLineColor(r.kBlack)")
    eval(f"{data}.Draw(\"HIST\")")
    eval(f"{sim}.Draw(\"HIST SAME\")")
    canvas.Write()
