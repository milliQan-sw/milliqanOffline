#!/usr/bin/python3

import os
import re
import pathlib
import ROOT as r
import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import array as arr
import argparse
from milliqanPlotter import *
from processorConstants import *

class milliqanProcessor():

    def __init__(self, filelist, branches, schedule=None, cuts=None, plotter=None, max_events=None, step_size=10000, qualityLevel="tight", verbosity='minimal', goodRunsList=None, sim=False):
        self.script_dir = os.path.abspath(__file__).replace("milliqanProcessor.py", "")
        self.qualityLevelString = qualityLevel
        self.verbosityString = verbosity
        self.sim = sim
        
        #Checks the filelist against goodRuns.json
        self.filelist = filelist
        
        self.qualityLevel, self.verbosity = self.constantPuller()

        if not self.sim:
            self.fileChecker() 

        self.branches = branches
        self.mqSchedule = schedule
        self.max_events = max_events
        self.step_size = step_size
        self.mqSchedule.cuts.branches = list(branches)
        self.goodRunsList = goodRunsList

    def reset(self):
        self.mqSchedule.cuts.cutflow = {}
        self.mqSchedule.cuts.counter = 0
    
    #Pulls the quality level and verbosity from the processorConstants class based on the quality level input string
    def constantPuller(self):
        if self.qualityLevelString not in processorConstants.qualityDict.keys():
            raise Exception("\n\nQuality level '{0}' not recognized. Please use one of the following: {1}\n".format(self.qualityLevelString, list(processorConstants.qualityDict.keys())))
        if self.verbosityString not in processorConstants.verbosity.keys():
            raise Exception("\n\nVerbosity level '{0}' not recognized. Please use one of the following: {1}\n".format(self.verbosityString, list(processorConstants.verbosity.keys())))
        if processorConstants.verbosity[self.verbosityString] > 0:
            print("\nChosen quality level: \033[1;34m", self.qualityLevelString, "\033[0m")
            print("Chosen verbosity level: \033[1;34m", self.verbosityString, "\n\033[0m")
        return processorConstants.qualityDict[self.qualityLevelString], processorConstants.verbosity[self.verbosityString]

    #Get rid of the strings and make a dictionary so that it's easier to debug
    def fileChecker(self):
        #If user is overriding the quality check, then we don't need to check the files against goodRuns.json
        if self.qualityLevel == -2:
            print("\n\033[1;31mQuality check is being overridden. All files will be processed.\033[0m")
            return

        if self.goodRunsList is not None:
            goodJson_array = ak.from_json(pathlib.Path(self.goodRunsList))
        else:
            goodJson_array = ak.from_json(pathlib.Path(self.script_dir + "../../configuration/barConfigs/goodRunsList.json"))
        data = ak.Array(goodJson_array['data'])
        goodJson = ak.zip({
            'run': data[:, 0],
            'file': data[:, 1],
            'loose': data[:, 2],
            'medium': data[:, 3],
            'tight': data[:, 4],
            'single_trigger': data[:, 5]
        }, depth_limit=1)
        
        goodJson = ak.enforce_type(goodJson, "{run: int64, file: int64, loose: bool, medium: bool, tight: bool, single_trigger: bool}")
        
        filelist_copy = self.filelist.copy()
        for filepath in filelist_copy:
            filename = os.path.basename(filepath)
            pattern = r"Run(\d+)\.(\d+)"
            match = re.search(pattern, filename)
            if match:
                run_number = int(match.group(1))
                file_number = int(match.group(2))
            else:
                raise TypeError("Filename does not match the expected pattern")
            
            matching_goodJson = goodJson[(goodJson['run'] == int(run_number)) & (goodJson['file'] == int(file_number))]
            
            #Establishes the quality level of the run
            if len(matching_goodJson) == 0:
                self.filelist.remove(filepath)
                print("File {0} is not in goodRuns.json. Removing it from the filelist".format(filename))
            
            elif matching_goodJson[self.qualityLevelString] != True:
                self.filelist.remove(filepath)
                if self.verbosity > 0:
                    print("\033[1;31mFile {0} is not a good run at the level '{1}'. Removing it from the filelist!\033[0m".format(filename, self.qualityLevelString))
                continue
            
            elif matching_goodJson[self.qualityLevelString] == True and self.verbosity > 1:
                print("File {0} is a good run at the level '{1}'".format(filename, self.qualityLevelString))
        
        if self.verbosity > 0:
            print("\n\033[1;32mFiles that will be processed: \033[0m", self.filelist,"\n")

    def setBranches(self, branches):
        self.schedule = branches

    def makeBranches(self, events):

        self.mqSchedule.setEvents(events)
        for branch in self.mqSchedule.schedule:
            if isinstance(branch, milliqanPlot):
                if isinstance(branch.variables, list):
                    for i in branch.variables:
                        if i not in events.fields:
                            print("MilliQan Processor: Branch {0} does not exist in event array".format(i))
                            continue
                    branch.plot(events)
                else:
                    if branch.variables in events.fields:
                        branch.plot(events)

                    else:
                        print("MilliQan Processor: Branch {0} does not exist in event array or custom output".format(branch.variables))
                        continue
            else:
                branch()
        return events

    def makeCuts(self, events):
        return events

    def runCustomFunction(self, events):
        try:
            return self.customFunction(events)
        except Exception as error:
            print("MilliQan Processor: Error", error)
            return

    def setCustomFunction(self, fcn):
        self.customFunction = fcn

    def run(self):

        total_events = 0

        self.reset()
        
        for events in uproot.iterate(

            #files
            self.filelist,

            #branches
            self.branches,

            step_size=self.step_size,

            num_workers=8,

            ):

            print("MilliQan Processor: Processing event {}...".format(total_events))

            total_events += len(events)

            broadcastChan = 'npulses'

            _, events['fileNumber'] = ak.broadcast_arrays(events[broadcastChan], events['fileNumber'])
            _, events['runNumber'] = ak.broadcast_arrays(events[broadcastChan], events['runNumber'])
            _, events['tTrigger'] = ak.broadcast_arrays(events[broadcastChan], events['tTrigger'])
            _, events['event'] = ak.broadcast_arrays(events[broadcastChan], events['event'])
            _, events['boardsMatched'] = ak.broadcast_arrays(events[broadcastChan], events['boardsMatched'])

            if self.max_events and total_events >= self.max_events: break

            events = self.makeBranches(events)

            events = self.makeCuts(events)
            
            if hasattr(self, 'customFunction'):
                self.custom_out = self.runCustomFunction(events)
    
        print("Number of processed events", total_events)
