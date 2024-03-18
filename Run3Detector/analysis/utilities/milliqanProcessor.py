#!/usr/bin/python3

import os
import ROOT as r
import uproot
import matplotlib.pyplot as plt
import awkward as ak
import pathlib
import numpy as np
import array as arr
from milliqanPlotter import *

class milliqanProcessor():

    def __init__(self, filelist, branches, schedule=None, cuts=None, plotter=None, max_events=None, runQualityOverride=False, qualityLevel="loose"):
        self.filelist = filelist
        self.branches = branches
        self.mqSchedule = schedule
        #self.mqCuts = cuts
        #self.plotter = plotter
        self.max_events = max_events
        self.runQualityOverride = runQualityOverride
        self.qualityLevel = qualityLevel

    def fileChecker(self):
        goodJson_array = ak.from_json(pathlib.Path("goodRuns.json"))
        columns = ak.Array(goodJson_array['columns'])
        data = ak.Array(goodJson_array['data'])
        goodJson = ak.zip({
            'run': data[:, 0],
            'file': data[:, 1],
            'loose': data[:, 2],
            'medium': data[:, 3],
            'tight': data[:, 4]
        }, depth_limit=1)
        
        print(goodJson)
        
        for filepath in self.filelist:
            filename = os.path.basename(filepath)
            parts = filename.split('_')
            run_number, file_number = parts[1].replace("Run","").split('.')
            print(run_number, file_number)
            matching_goodJson = goodJson[(goodJson['run'] == int(run_number)) & (goodJson['file'] == int(file_number))]
            print(matching_goodJson)

            if len(matching_goodJson) == 0:
                #print("File {0} is not in goodRuns.json. Please consult goodRuns.json :)".format(filename))
                if self.runQualityOverride:
                    print("File {0} is not in goodRuns.json, but we are overriding the quality check".format(filename))
                else:
                    raise Exception("File {0} is not in goodRuns.json. Please consult goodRuns.json :)".format(filename))

            if len(matching_goodJson) == 1:
                if matching_goodJson['tight'] & ((self.qualityLevel == "tight") | (self.qualityLevel == "medium") | (self.qualityLevel == "loose")):
                    print("File {0} is good run (tight)".format(filename))
                elif matching_goodJson['medium'] & ((self.qualityLevel == "medium") | (self.qualityLevel == "loose")):
                    print("File {0} is good run (medium)".format(filename))
                elif matching_goodJson['loose'] & (self.qualityLevel == "loose"):
                    print("File {0} is good run (loose)".format(filename))
                elif self.runQualityOverride:
                    print("File {0} is not in goodRuns.json, but we are overriding the quality check".format(filename))
                else:
                    #print("File {0} is not a good run. Please consult goodRuns.json :)".format(filename))
                    raise Exception("File {0} is not a good run. Please consult goodRuns.json :)".format(filename))

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
    
        print("Number of processed events", total_events)