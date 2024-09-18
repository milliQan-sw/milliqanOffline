#!/usr/bin/python3

import ROOT as r
import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import array as arr
from milliqanPlotter import *

class milliqanProcessor():

    def __init__(self, filelist, branches, schedule=None, max_events=None, step_size=10000):
        self.filelist = filelist
        self.branches = branches
        self.mqSchedule = schedule
        self.max_events = max_events
        self.step_size = step_size

    def makeBranches(self, events):

        self.mqSchedule.setEvents(events)
        for branch in self.mqSchedule.schedule:
            #if branch == 'tTrigger':
            #    print("found trigger")
            #    continue
            if isinstance(branch, milliqanPlot):
                if isinstance(branch.variables, list):
                    for i in branch.variables:
                        if i not in events.fields:
                            print("MilliQan Processor: Branch {0} does not exist in event array".format(i))
                            break
                    branch.plot(events)
                else:
                    if branch.variables in events.fields:
                        branch.plot(events)
                    #elif branch.variables in self.custom_out:
                    #    branch.plot(self.custom_out)
                    else:
                        print("MilliQan Processor: Branch {0} does not exist in event array or custom output".format(branch.variables))
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
            print("MilliQan Processor: Error", error)
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

            step_size=self.step_size,

            num_workers=8,

            ):

            print("MilliQan Processor: Processing event {}...".format(total_events))

            total_events += len(events)

            broadcastChan = 'npulses'

            #print(events['tTrigger'][0])
            #_, events['boardMatchCut'] = ak.broadcast_arrays(events['pickupFlag'], events['boardMatchCut'])
            _, events['fileNumber'] = ak.broadcast_arrays(events[broadcastChan], events['fileNumber'])
            _, events['runNumber'] = ak.broadcast_arrays(events[broadcastChan], events['runNumber'])
            _, events['tTrigger'] = ak.broadcast_arrays(events[broadcastChan], events['tTrigger'])
            _, events['event'] = ak.broadcast_arrays(events[broadcastChan], events['event'])
            _, events['boardsMatched'] = ak.broadcast_arrays(events[broadcastChan], events['boardsMatched'])

            #_, events['fileNumber'] = ak.broadcast_arrays(events['pickupFlag'], events['fileNumber'])
            #print(events['pickupFlag'][0])
            #print(events['tTrigger'][0])



            if self.max_events and total_events >= self.max_events: break

            events = self.makeBranches(events)

            events = self.makeCuts(events)
            
            if hasattr(self, 'customFunction'):
                self.custom_out = self.runCustomFunction(events)
    
        print("Number of processed events", total_events)