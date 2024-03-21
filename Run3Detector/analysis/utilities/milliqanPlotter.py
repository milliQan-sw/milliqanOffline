from ROOT import TH1, TH2, TGraph
import awkward as ak
from array import array
import numpy as np

class milliqanPlot():

    def __init__(self, histogram, variables, cut=None):
        self.histogram = histogram
        self.variables = variables
        self.__name__ = self.histogram.GetName()
        self.cut = cut

    def plot(self, events):
        if isinstance(self.variables, list):
            if self.cut:
                output = [ak.flatten(events[x][events[self.cut]],axis=None) for x in self.variables]
            else:
                output = [ak.drop_none(events[x]) for x in self.variables]
                output = [ak.flatten(y,axis=None) for y in output]
            #2D histograms
            if len(output) == 2 and len(output[0])>0:
                myarray0 = array('d', output[0])
                myarray1 = array('d', output[1])
                self.histogram.FillN(len(myarray0), myarray0, myarray1, np.ones(len(myarray0)))
            #3d histograms
            elif len(output) == 3 and len(output[0])>0:
                print("No 3d printing capabilities yet!")
                
        else:
            if self.cut:
                output = ak.flatten(events[self.variables][events[self.cut]],axis=None)
            else:
                output = ak.drop_none(events[self.variables])
                output = ak.flatten(output,axis=None)
            myarray = array('d', output)
            #1D histograms
            if len(myarray)>0:
                self.histogram.FillN(len(myarray), myarray, np.ones(len(myarray)))

class milliqanPlotter():

    def __init__(self, histograms=[]):
        self.histograms = histograms
        self.events = []
        self.createDict()

    def __name__(self):
        self.__name__ = 'milliqanPlotter'

    def createDict(self):
        names = [x.__name__ for x in self.histograms]
        hists = [x for x in self.histograms]
        self.dict = dict(zip(names, hists))   

    def updateDict(self, hist):
        self.dict[hist.__name__] = hist     

    def addHistograms(self, histogram, variable, cut=None):
        h_ = milliqanPlot(histogram, variable, cut)
        self.histograms.append(h_)
        self.updateDict(h_)