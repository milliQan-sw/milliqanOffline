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
                name = input.__parent__
        elif hasattr(input, '__code__') and input.__code__.co_name == 'decorator':
            print("trying to get name", name)
            name = input.__name__.split()[1]
        else:
            print("Inside else block", input, input.__name__)
            print(hasattr(input, '__code__'))
            if hasattr(input, '__code__'):
                print("co name", input.__code__.co_name, input.__name__)
            name = input.__name__
        
        if name in globals() or name in locals():
            self.schedule.append(input)
        elif name in dir(milliqanCuts) or name in dir(self.cuts):
            self.schedule.append(input)
        else:
            print("MilliQan Scheduler: Function {0} does not exist".format(name))
            print(name in globals())
            print(dir(self.cuts))
            print(dir(milliqanCuts))

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


    
