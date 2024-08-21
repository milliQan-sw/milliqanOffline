import os
import sys
sys.path.append("../utilities/")

import ROOT as r

from milliqanProcessor import milliqanProcessor
from milliqanScheduler import milliQanScheduler
from milliqanPlotter import milliqanPlotter
from milliqanCuts import milliqanCuts

filelist = ["/home/ryan/Documents/Data/MilliQan/beam_muon_slabMilliQan_flat.root:t"]
branch_list = ["layer", "row", "column", "eventID"]

my_cuts = milliqanCuts()
four_layer_cut = my_cuts.getCut(my_cuts.fourLayerCut, 'four_layer_cut', cut=False)

my_plotter = milliqanPlotter()
h_height = r.TH1F("h_four_layer", "Layers", 140, 0, 3000)
my_plotter.addHistograms(h_height, 'eventID')

cutflow = [my_plotter.dict["h_four_layer"]]
my_schedule = milliQanScheduler(cutflow, my_cuts, my_plotter)

my_processor = milliqanProcessor(filelist, branch_list, my_schedule, my_cuts, my_plotter, max_events=1000)

my_processor.run()

c1 = r.TCanvas("c1", "c1", 400, 400)
c1.cd()
h_height.Draw()
c1.Draw()


