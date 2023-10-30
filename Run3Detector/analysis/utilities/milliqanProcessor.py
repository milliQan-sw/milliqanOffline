#!/usr/bin/python3

import ROOT as r
import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import array as arr
from milliqanCuts import *

class milliqanProcessor():

    def __init__(self, filelist, branches):
        self.filelist = filelist
        self.branches = branches

    def setBranches(self, branches):
        self.branchesToMake = branches

    def setCuts(self, cuts):
        self.cuts = cuts

    def makeBranches(self, events):
        for branch in self.branchesToMake:
            if '(' in branch:
                branch = branch.split('(')
                fcn = eval(branch[0])
                args = branch[1].split(')')[0]
                args = args.split(';')
                events = fcn(events, *args)
            else:
                fcn = eval(branch)
                events = fcn(events)
        return events

    def makeCuts(self, events):
        return events

    def runCustomFunction(self, events):
        try:
            return self.customFunction(events)
        except:
            return

    def setCustomFunction(self, fcn):
        self.customFunction = fcn

    def makeHistograms(self, root=True, matplot=False):
        if matplot:
            self.ax2.scatter(ak.flatten(self.custom_out[3]).to_numpy(), ak.flatten(self.custom_out[0]).to_numpy(), s=5)
        if root:
            t0 = ak.flatten(self.custom_out[0]).to_list()
            t0 = arr.array('d', t0)
            if len(t0) > 0:
                t3 = arr.array('d', ak.flatten(self.custom_out[3]).to_list())
                self.h_time0.FillN(len(t0), t0, np.ones(len(t0)))
                self.h_timeDiff.FillN(len(t0), t0, t3, np.ones(len(t0)))


    def run(self):

        total_events = 0
        passing_events = 0
        
        self.fig2, self.ax2 = plt.subplots()
        self.ax2.set(xlim=(1200, 1400), ylim=(1200, 1400))

        self.h_timeDiff = r.TH2F("h_timeDiff", "Time Difference Layer0 and Layer3", 200, 1200, 1400, 200, 1200, 1400)
        self.h_time0 = r.TH1F("h_time0", "Time in Layer 0", 200, 1200, 1400)
        
        for events in uproot.iterate(

            #files
            self.filelist,

            #branches
            self.branches,

            step_size=1000,

            num_workers=8,

            ):

            events = self.makeBranches(events)

            events = self.makeCuts(events)

            self.custom_out = self.runCustomFunction(events)

            #self.makeHistograms()

            total_events += len(events)
            passing_events += len(ak.where(events.fourLayers)[0])
 
        print("Number of events", total_events)
        print("Number of passing events", passing_events)
