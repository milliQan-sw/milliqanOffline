#!/user/bin/python3

import os
from milliqanCuts import *
from milliqanPlotter import *
from functools import partial
import types


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
            #print("Lambda:", input)
            name = input.__parent__
        else:
            #print("Name", input.__name__)
            print(input, type(input))
            name = input.__name__
        
        if name in globals() or name in locals():
            #input = hello_decorator(input)
            self.schedule.append(input)
        elif name in dir(milliqanCuts) or name in dir(self.cuts):
            #input = hello_decorator(input)
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


    
