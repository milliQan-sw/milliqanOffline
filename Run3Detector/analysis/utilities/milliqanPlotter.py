from ROOT import TH1, TH2, TGraph
import awkward as ak
from array import array
import numpy as np

class milliqanPlot():

    def __init__(self, histogram, variables):
        self.histogram = histogram
        self.variables = variables
        self.__name__ = self.histogram.GetName()

    def plot(self, events):
        output = ak.flatten(events[self.variables])
        myarray = array('d', output)
        self.histogram.FillN(len(myarray), myarray, np.ones(len(myarray)))

class milliqanPlotter():

    def __init__(self, histograms=[]):
        self.histograms = histograms
        self.events = []
        self.createDict()
        print(self.dict)

    def __name__(self):
        self.__name__ = 'milliqanPlotter'

    def createDict(self):
        names = [x.__name__ for x in self.histograms]
        hists = [x for x in self.histograms]
        self.dict = dict(zip(names, hists))   

    def updateDict(self, hist):
        self.dict[hist.__name__] = hist     

    def addHistograms(self, histogram, variable):
        h_ = milliqanPlot(histogram, variable)
        self.histograms.append(h_)
        self.updateDict(h_)

    def plot(self, mqPlot):
        output = ak.flatten(self.events[mqPlot.variables])
        myarray = array('d', output)
        mqPlot.histogram.FillN(len(myarray), myarray, np.ones(len(myarray)))

        '''output = ak.flatten(self.events[self.variable])
        print(output)
        myarray = array('d', output)
        self.hist.FillN(len(myarray), myarray, np.ones(len(myarray)))'''