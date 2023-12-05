from ROOT import TH1, TH2, TGraph
import awkward as ak
from array import array
import numpy as np

class milliqanPlotter():

    def __init__(self, histogram, variable):
        print("initialize")
        self.hist = histogram
        self.variable = variable
        self.events = []

    def __name__(self):
        self.__name__ == 'milliqanPlotter'

    def plot(self):
        output = ak.flatten(self.events[self.variable])
        print(output)
        myarray = array('d', output)
        self.hist.FillN(len(myarray), myarray, np.ones(len(myarray)))