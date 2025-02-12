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

        allLayersIndex = -1
        for index, (key, value) in enumerate(self.cuts.cutflow.items()):
            if key == "hitInAllLayers":
                allLayersIndex = index-1
                break

        self.eventCutFlow = TH1F("eventCutFlow", 'Cut Flow for Event Counts', numCuts, 0, numCuts)
        self.pulseCutFlow = TH1F("pulseCutFlow", 'Cut Flow for Pulse Counts', numCuts, 0, numCuts)
        self.eventSelectionEff = TH1F("eventSelectionEff", 'Selection Efficiency for Events', numCuts, 0, numCuts)
        self.pulseSelectionEff = TH1F("pulseSelectionEff", 'Selection Efficiency for Pulses', numCuts, 0, numCuts)
        self.eventCutEfficiencies = TH1F("eventCutEfficiencies", 'Efficiencies for Cuts on Events', numCuts, 0, numCuts)
        self.pulseCutEfficiencies = TH1F("pulseCutEfficiencies", 'Efficiencies for Cuts on Pulses', numCuts, 0, numCuts)

        if allLayersIndex >= 0:
            self.eventCutEffAllLayers = TH1F("eventCutEffAllLayers", 'Efficiencies for Cuts on Events', numCuts-allLayersIndex, 0, numCuts-allLayersIndex)
            self.pulseCutEffAllLayers = TH1F("pulseCutEffAllLayers", 'Efficiencies for Cuts on Pulses', numCuts-allLayersIndex, 0, numCuts-allLayersIndex)

        ibin = 0
        prevEvents = -1
        prevPulses = -1
        allLayersEvents = -1
        allLayersPulses = -1
        for i, (key, value) in enumerate(self.cuts.cutflow.items()):
            if not value['cut'] and 'EventCounter' not in key: continue
            evtEff, pulseEff = 1.0, 1.0
            if prevEvents > 0:
                evtEff = value['events'] / prevEvents
            if prevPulses > 0:
                pulseEff = value['pulses'] / prevPulses
            if prevEvents == 0:
                evtEff = 0.0
            if prevPulses == 0:
                pulseEff = 0.0

            if i==allLayersIndex+1:
               allLayersEvents = value['events']
               allLayersPulses = value['pulses']

            self.eventCutFlow.Fill(ibin, value['events'])
            self.pulseCutFlow.Fill(ibin, value['pulses'])
            self.eventCutEfficiencies.Fill(ibin, value['events'] / totalEvents)
            self.pulseCutEfficiencies.Fill(ibin, value['pulses'] / totalPulses)
            self.eventSelectionEff.Fill(ibin, evtEff)
            self.pulseSelectionEff.Fill(ibin, pulseEff)

            self.eventCutFlow.GetXaxis().SetBinLabel(ibin+1, key)
            self.pulseCutFlow.GetXaxis().SetBinLabel(ibin+1, key)
            self.eventCutEfficiencies.GetXaxis().SetBinLabel(ibin+1, key)
            self.pulseCutEfficiencies.GetXaxis().SetBinLabel(ibin+1, key)
            self.eventSelectionEff.GetXaxis().SetBinLabel(ibin+1, key)
            self.pulseSelectionEff.GetXaxis().SetBinLabel(ibin+1, key)

            if allLayersIndex >= 0 and i > allLayersIndex:
                self.eventCutEffAllLayers.Fill(ibin-allLayersIndex, value['events'] / allLayersEvents)
                self.pulseCutEffAllLayers.Fill(ibin-allLayersIndex, value['pulses'] / allLayersPulses)
                self.eventCutEffAllLayers.GetXaxis().SetBinLabel(ibin-allLayersIndex+1, key)
                self.pulseCutEffAllLayers.GetXaxis().SetBinLabel(ibin-allLayersIndex+1, key)

            prevEvents = value['events']
            prevPulses = value['pulses']
            ibin+=1


        self.plotter.histograms.append(milliqanPlot(self.eventCutFlow, None))
        self.plotter.histograms.append(milliqanPlot(self.pulseCutFlow, None))
        self.plotter.histograms.append(milliqanPlot(self.eventCutEfficiencies, None))
        self.plotter.histograms.append(milliqanPlot(self.pulseCutEfficiencies, None))
        self.plotter.histograms.append(milliqanPlot(self.eventSelectionEff, None))
        self.plotter.histograms.append(milliqanPlot(self.pulseSelectionEff, None))
        if allLayersIndex>=0:
            self.plotter.histograms.append(milliqanPlot(self.eventCutEffAllLayers, None))
            self.plotter.histograms.append(milliqanPlot(self.pulseCutEffAllLayers, None))




    
