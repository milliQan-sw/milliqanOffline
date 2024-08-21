import os
import sys
sys.path.append("../utilities/")

import ROOT as r

from milliqanProcessor import milliqanProcessor
from milliqanScheduler import milliQanScheduler
from milliqanPlotter import milliqanPlotter
from milliqanCuts import milliqanCuts

file_list = ["/home/ryan/Documents/Data/MilliQan/beam_muon_slabMilliQan_flat.root:t"]
branch_list = ["layer", "row", "column", "nPE"]

my_cuts = milliqanCuts()
four_layer_cut = my_cuts.getCut(my_cuts.fourLayerCut, 'four_layer_cut', cut=True)

my_plotter = milliqanPlotter()

h_npe_before = r.TH1F("h_npe_before", "npe", 140, 0, 1500)
my_plotter.addHistograms(h_npe_before, 'nPE')

h_npe_after = r.TH1F("h_npe_after", "npe", 140, 0, 1500)
my_plotter.addHistograms(h_npe_after, 'nPE')

cutflow = [my_cuts.layerCut, my_cuts.fourLayerCut, my_plotter.dict['h_npe_after']]
my_schedule = milliQanScheduler(cutflow, my_cuts, my_plotter)

my_processor = milliqanProcessor(file_list, branch_list, my_schedule, my_cuts, my_plotter)
my_processor.run()

c1 = r.TCanvas("c1", "c1", 400, 400)
c1.cd()
h_npe_after.Draw()
c1.Draw()
