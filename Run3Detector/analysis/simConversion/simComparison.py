import ROOT as r
import uproot
import awkward as ak
import sys
sys.path.append('..')
import numpy as np
from utilities.milliqanProcessor import *
from utilities.milliqanScheduler import *
from utilities.milliqanCuts import *
from utilities.milliqanPlotter import *
import os
from functools import partial


if __name__ == "__main__":
    filelist = ["/data/bar_cosmic_sim_processed.root:t",
                "/store/MilliQan_Run1901.1_v35.root:t"]
    branches = ["sidebandMean", "sidebandRMS", "chan", "row", "column",
                "layer", "height", "area", "nPE", "riseSamples", "fallSamples",
                "npulses", "time", "duration", "beamOn"]
    cuts = milliqanCuts()

    plotter = milliqanPlotter()
    
    cutflow = [cuts.beamOnCut]

    schedule = milliQanScheduler(cutflow, cuts, plotter)

    schedule.printSchedule()

    iterator = milliqanProcessor(filelist, branches, schedule, cuts, plotter)
    iterator.run()
    
