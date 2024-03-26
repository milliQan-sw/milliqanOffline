#!/usr/bin/python3

import os
import pathlib
import ROOT as r
import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import array as arr
from milliqanPlotter import *

class milliqanProcessor():

    def __init__(self, filelist, branches, schedule=None, cuts=None, plotter=None, max_events=None, runQualityOverride=False, qualityLevel="tight"):
        self.qualityLevelString = qualityLevel
        self.runQualityOverride = runQualityOverride
        
        #Converting the quality level to an integer
        self.qualityDict = {"single_trigger": -1, "loose": 0, "medium": 1, "tight": 2}
        if self.qualityLevelString not in self.qualityDict.keys():
            raise Exception("Quality level '{0}' not recognized".format(self.qualityLevelString))
        print("Chosen quality level: ", self.qualityLevelString)
        self.qualityLevel = self.qualityDict[self.qualityLevelString]
        
        #Checks the filelist against goodRuns.json
        self.filelist = filelist
        self.fileChecker() 
        
        self.branches = branches
        self.mqSchedule = schedule
        #self.mqCuts = cuts
        #self.plotter = plotter
        self.max_events = max_events

    #Get rid of the strings and make a dictionary so that it's easier to debug
    def fileChecker(self):
        #goodJson_array = ak.from_json(pathlib.Path("../goodRunTools/goodRunsMerged.json"))
        goodJson_array = ak.from_json(pathlib.Path("goodRuns.json"))
        data = ak.Array(goodJson_array['data'])
        goodJson = ak.zip({
            'run': data[:, 0],
            'file': data[:, 1],
            'loose': data[:, 2],
            'medium': data[:, 3],
            'tight': data[:, 4],
            'single_trigger': data[:, 5]
        }, depth_limit=1)
        
        for filepath in self.filelist:
            filename = os.path.basename(filepath)
            parts = filename.split('_')
            run_number, file_number = parts[1].replace("Run","").split('.')
            matching_goodJson = goodJson[(goodJson['run'] == int(run_number)) & (goodJson['file'] == int(file_number))]
            
            #Establishes the quality level of the run
            runQualityLevel = -1
            if len(matching_goodJson) == 0:
                pass
            elif (matching_goodJson['tight'] == True) and (matching_goodJson['medium'] == True) and (matching_goodJson['loose'] == True):
                runQualityLevel = 2
            elif (matching_goodJson['tight'] == False) and (matching_goodJson['medium'] == True) and (matching_goodJson['loose'] == True):
                runQualityLevel = 1
            elif (matching_goodJson['tight'] == False) and (matching_goodJson['medium'] == False) and (matching_goodJson['loose'] == True):
                runQualityLevel = 0
                
            #Establishes whether the run is a single trigger run
            singleTriggerBool = False
            if len(matching_goodJson) == 0:
                pass
            elif matching_goodJson['single_trigger']:
                singleTriggerBool = True

            #Determines if the file was found
            if len(matching_goodJson) == 0:
                if self.runQualityOverride:
                    print("File {0} is not in goodRuns.json, but we are overriding the quality check".format(filename))
                else:
                    raise Exception("File {0} is not in goodRuns.json. Please consult goodRuns.json :)".format(filename))

            #Determines if it's a good run (for non-single-trigger runs)
            if len(matching_goodJson) == 1 and self.qualityLevel>=0:
                if runQualityLevel == -1 and not singleTriggerBool:
                    print("File {0} has a quality level that cannot be determined. Please consult goodRuns.json :)".format(filename))
                elif runQualityLevel==2 and (self.qualityLevel <= runQualityLevel):
                    print("File {0} is good run (tight)".format(filename))
                elif runQualityLevel==1 and (self.qualityLevel <= runQualityLevel):
                    print("File {0} is good run (medium)".format(filename))
                elif runQualityLevel==0 and (self.qualityLevel <= runQualityLevel):
                    print("File {0} is good run (loose)".format(filename))
                elif self.runQualityOverride:
                    print("File {0} is not a good run at the quality level '{1}', but we are overriding the quality check".format(filename, self.qualityLevelString))
                else:
                    raise Exception("File {0} is not a good run at the level '{1}'. Please consult goodRuns.json :)".format(filename, self.qualityLevelString))
                
            #Determines if it's a good run (for single-trigger runs)
            if len(matching_goodJson) == 1 and self.qualityLevel==-1:
                if singleTriggerBool:
                    print("File {0} is a single trigger run".format(filename))
                elif self.runQualityOverride:
                    print("File {0} is not a single trigger run, but we are overriding the quality check".format(filename))
                else:
                    raise Exception("File {0} is not a single trigger run. Please consult goodRuns.json :)".format(filename))

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