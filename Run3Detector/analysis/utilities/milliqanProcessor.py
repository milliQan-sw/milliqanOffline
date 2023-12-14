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
                if isinstance(branch.variables, list):
                    for i in branch.variables:
                        if i not in events.fields:
                            print("Branch {0} does not exist in event array".format(i))
                            break
                    branch.plot(events)
                else:
                    if branch.variables in events.fields:
                        branch.plot(events)
                    #elif branch.variables in self.custom_out:
                    #    branch.plot(self.custom_out)
                    else:
                        print("Branch {0} does not exist in event array or custom output".format(branch.variables))
                        break
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

<<<<<<< HEAD
        print("Number of processed events", total_events)
=======

            total_events += len(events)
 
        print("Number of events prior to cuts", total_events)
>>>>>>> b12d1c1 (Added a script to explore time walk effects. Also modified Plot() in milliqanProcessor to be able to generate 2d and 3d histograms.)
