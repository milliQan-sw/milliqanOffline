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
            print(branch.__name__)
            if isinstance(branch, milliqanPlot):
                if branch.variables in events.fields:
                    branch.plot(events)
                #elif branch.variables in self.custom_out:
                #    branch.plot(self.custom_out)
                else:
                    print("Branch {0} does not exist in event array or custom output".format(branch.variables))
            else:
                branch()
        return events

    def makeCuts(self, events):
        return events

    def runCustomFunction(self, events):
        try:
            return self.customFunction(events)
        except Exception as error:
            print("Error", error)
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

            total_events += len(events)
           
            if self.max_events and total_events >= self.max_events: break

            events = self.makeBranches(events)

            events = self.makeCuts(events)
            
            if hasattr(self, 'customFunction'):
                self.custom_out = self.runCustomFunction(events)

        print("Number of processed events", total_events)
