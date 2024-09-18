#!/user/bin/python3

import os
from milliqanCuts import *
from milliqanPlotter import *
from functools import partial
import types
from ROOT import TH1F


class milliQanScheduler():

    def __init__(self, inputs, cuts=None, plotter=None):
        self.schedule = []
        self.events = []
        self.inputs = inputs
        self.cuts = cuts
        self.plotter = plotter

        self.createSchedule()

    def setEvents(self, events):
        self.events = events
        self.cuts.events = self.events
        if (self.plotter  != None):
            self.plotter.events = self.events
        else:
            print("MilliQan Scheduler: Please be aware that plotter is not being used now")

    def addToSchedule(self, input):
        name = None
        if isinstance(input, milliqanPlot):
            self.schedule.append(input)
            return
        
        if isinstance(input, partial):
            name = input.func.__name__
        elif hasattr(input, '__code__') and input.__code__.co_name == '<lambda>':
                name = input.__parent__
        elif hasattr(input, '__code__') and input.__code__.co_name == 'decorator':
            name = input.__name__.split()[1]
        else:
            name = input.__name__
        
        if name in globals() or name in locals():
            self.schedule.append(input)
        elif name in dir(milliqanCuts) or name in dir(self.cuts):
            self.schedule.append(input)
        else:
            print("MilliQan Scheduler: Function {0} does not exist".format(name))

    def createSchedule(self):
        for input in self.inputs:
            self.addToSchedule(input)

    def printSchedule(self):
        print("----------------------------")
        print("MilliQan Scheduler:")
        for is_, s in enumerate(self.schedule):
            print('\t{0}. {1}'.format(is_, s.__name__))
        print("----------------------------")

    def insert(self, process, pos):
        self.schedule.insert(process, pos)

    def cutFlowPlots(self):
        #make cutflow plots
        numCuts = count = sum(1 for key, sub_dict in self.cuts.cutflow.items() if sub_dict.get('cut', True) or 'EventCounter' in key)
        totalEvents = self.cuts.cutflow['totalEventCounter']['events']
        totalPulses = self.cuts.cutflow['totalEventCounter']['pulses']

        self.eventCutFlow = TH1F("eventCutFlow", 'Cut Flow for Event Counts', numCuts, 0, numCuts)
        self.pulseCutFlow = TH1F("pulseCutFlow", 'Cut Flow for Pulse Counts', numCuts, 0, numCuts)
        self.eventCutEfficiencies = TH1F("eventCutEfficiencies", 'Efficiencies for Cuts on Events', numCuts, 0, numCuts)
        self.pulseCutEfficiencies = TH1F("pulseCutEfficiencies", 'Efficiencies for Cuts on Pulses', numCuts, 0, numCuts)

        ibin = 0
        for i, (key, value) in enumerate(self.cuts.cutflow.items()):
            if not value['cut'] and 'EventCounter' not in key: continue
            self.eventCutFlow.Fill(ibin, value['events'])
            self.pulseCutFlow.Fill(ibin, value['pulses'])
            self.eventCutEfficiencies.Fill(ibin, value['events'] / totalEvents)
            self.pulseCutEfficiencies.Fill(ibin, value['pulses'] / totalPulses)

            self.eventCutFlow.GetXaxis().SetBinLabel(ibin+1, key)
            self.pulseCutFlow.GetXaxis().SetBinLabel(ibin+1, key)
            self.eventCutEfficiencies.GetXaxis().SetBinLabel(ibin+1, key)
            self.pulseCutEfficiencies.GetXaxis().SetBinLabel(ibin+1, key)
            ibin+=1

        self.plotter.histograms.append(milliqanPlot(self.eventCutFlow, None))
        self.plotter.histograms.append(milliqanPlot(self.pulseCutFlow, None))
        self.plotter.histograms.append(milliqanPlot(self.eventCutEfficiencies, None))
        self.plotter.histograms.append(milliqanPlot(self.pulseCutEfficiencies, None))



    
