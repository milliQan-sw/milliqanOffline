#!/usr/bin/python3

import ROOT as r
import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import array as arr
from milliqanPlotter import *

class milliqanProcessor():

    def __init__(self, filelist, branches, schedule=None, cuts=None, plotter=None, max_events=None):
        self.filelist = filelist
        self.branches = branches
        self.mqSchedule = schedule
        #self.mqCuts = cuts
        #self.plotter = plotter
        self.max_events = max_events

    def setBranches(self, branches):
        self.schedule = branches

    '''def setCuts(self, cuts):
        self.cuts = cuts'''

    def makeBranches(self, events):
        #self.mqCuts.events = events
        #self.plotter.events = events
        self.mqSchedule.setEvents(events)
        for branch in self.mqSchedule.schedule:
            if isinstance(branch, milliqanPlot):
                branch.plot(events)
            else:
                branch()
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

    def run(self):

        total_events = 0
        
        for events in uproot.iterate(

            #files
            self.filelist,

            #branches
            self.branches,

            step_size=1000,

            num_workers=8,

            ):

            if self.max_events and total_events >= self.max_events: break

            events = self.makeBranches(events)

            events = self.makeCuts(events)

            self.custom_out = self.runCustomFunction(events)

            total_events += len(events)
 
        print("Number of events", total_events)
