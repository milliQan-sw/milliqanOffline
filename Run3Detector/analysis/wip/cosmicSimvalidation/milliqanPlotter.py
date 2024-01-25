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
        if self.cut:
            output = ak.flatten(events[self.variables][events[self.cut]],axis=None)
        else:
            output = ak.drop_none(events[self.variables])
            output = ak.flatten(output,axis=None)
        myarray = array('d', output)
        if len(myarray) > 0:
            self.histogram.FillN(len(myarray), myarray, np.ones(len(myarray)))
    
    #create the script for plotting the histogram that count the number of bar get hit
    #This is an event based analysis. So I can't use "flatten()" to plot histogram.
    def NBarHitsplot(self,events):
        #loop over events
        for pair in events:
            #get the truth table by checking channel type
            bar_cut = pair["type"] == 0
            #get the bar only data
            bar_data = pair[bar_cut]
            if len(bar_data["type"]) == 0: 
                continue
            NumBarHits = len(set(bar_data["chan"]))
            NumLayerHits = len(set(bar_data["layer"]))
            if NumBarHits >= 4 and NumLayerHits ==4: 
                self.histogram.Fill(NumBarHits)

            
            



        


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