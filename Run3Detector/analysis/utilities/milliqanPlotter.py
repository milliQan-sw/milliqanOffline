from ROOT import TH1, TH2, TGraph, TFile
import awkward as ak
from array import array
import numpy as np

class milliqanPlot():

    def __init__(self, histogram, variables, cut=None, invert=False):
        self.histogram = histogram
        self.variables = variables
        self.__name__ = self.histogram.GetName()
        self.cut = cut
        self.invert = invert

    def plot(self, events):
        if isinstance(self.variables, list):
            for var in self.variables:
                if var not in events.fields:
                    print("Variable {} not found in keys, skipping".format(var))
                    return 
            if self.cut:
                if self.cut == 'first': #cut to get just first pulse for plotting event level
                    output = [ak.flatten(ak.firsts(events[x]),axis=None) for x in self.variables]
                elif self.cut in events.fields:
                    if self.invert: #TODO fix this inversion
                        output = [ak.flatten(events[x][~events[self.cut]],axis=None) for x in self.variables]
                    else:
                        output = [ak.flatten(events[x][events[self.cut]],axis=None) for x in self.variables]
                else:
                    print("No branch {} found in keys".format(self.cut))
            else:
                output = [ak.drop_none(events[x]) for x in self.variables]
                output = [ak.flatten(y,axis=None) for y in output]
            #2D histograms
            if len(output) == 2 and len(output[0])>0 and len(output[1])>0:
                myarray0 = array('d', output[0])
                myarray1 = array('d', output[1])
                self.histogram.FillN(len(myarray0), myarray0, myarray1, np.ones(len(myarray0)))
            #3d histograms
            elif len(output) == 3 and len(output[0])>0:
                print("MilliQan Plotter: No 3d printing capabilities yet!")
                
        else:
            if self.cut:
                if self.cut == 'weight':
                    weight = ak.sum(ak.firsts(events[self.variables]))
                    self.histogram.Fill(0, weight)
                    return
                elif self.cut == 'first': #cut to get just first pulse for plotting event level
                    output = ak.flatten(ak.firsts(events[self.variables]),axis=None)
                elif self.cut in events.fields:
                    if self.invert: #TODO fix this inversion
                        output = ak.flatten(events[self.variables][~events[self.cut]],axis=None)
                    else:
                        output = ak.flatten(events[self.variables][events[self.cut]],axis=None)
                else:
                    print("No branch {} found in keys".format(self.cut))
            else:
                output = ak.drop_none(events[self.variables])
                output = ak.flatten(output,axis=None)
            myarray = array('d', output)
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

    def addHistograms(self, histogram, variable, cut=None, invert=False):
        h_ = milliqanPlot(histogram, variable, cut, invert)
        self.histograms.append(h_)
        self.updateDict(h_)

    def resetHistograms(self):
        for hist in self.histograms:
            hist.histogram.Reset()

    def saveHistograms(self, outputFile):
        fout = TFile.Open(outputFile, 'RECREATE')
        fout.cd()

        for hist in self.histograms:
            hist.histogram.Write()
