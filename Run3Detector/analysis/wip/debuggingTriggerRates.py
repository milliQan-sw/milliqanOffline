import os
import sys
import ROOT as r
import numpy as np

r.gROOT.SetBatch(True)

class Analyzer:

    def __init__(self, dataDir, runNum):
        self.dataDir = dataDir
        self.runNum = runNum

        self.getTChain()
        self.fout = r.TFile("output.root", "recreate")

    def getTChain(self):
        mychain = r.TChain("t")
        files = "{0}MilliQan_Run{1}.*.root".format(self.dataDir, self.runNum)
        mychain.Add(files)
        self.totalEntries = mychain.GetEntries()
        print("There are {0} events in the TChain".format(self.totalEntries))
        self.mychain = mychain

    def checkForChannel(self, chanNum):
        self.mychain.Draw(">>mylist","chan=={}".format(chanNum))
        mylist = r.gDirectory.Get("mylist")
        numEntries = mylist.GetN()
        return numEntries

    def chanPulseVsEvent(self):
        nbins = self.totalEntries / 100
        print("Number of bins", nbins, "upper limit", self.totalEntries)
        self.mychain.Draw("chan:event+(fileNumber*1000)>>h_chanVEvent({0}, 0, {1}, 76, 0, 76)".format(nbins, self.totalEntries))
        h_tmp = r.gDirectory.Get("h_chanVEvent")
        h_tmp.SetTitle("Pulses in Channels vs Event Number")
        h_tmp.GetXaxis().SetTitle("Event Number")
        h_tmp.GetYaxis().SetTitle("Channel")
        self.fout.cd()
        h_tmp.Write("h_chanVEvent")

if __name__ == "__main__":

    dataDir = '/store/user/milliqan/trees/v31/'
    runNum = 879

    myanalyzer = Analyzer(dataDir, runNum)

    #1. check three in row trigger events
    #2. fraction of events with hits in channel 50 (also as function of event num)
    #3. percent of events where each chan is over threshold (as function of event num)


    #2
    fracChanEvents = np.zeros(75)
    h_chanFrac = r.TH1F("h_chanFrac", "Fraction of Events w/ Pulses in Channel", 75, 0, 75)
    for channel in range(75):
        print("Plotting channel {0}".format(channel))
        fracChanEvents[channel] = myanalyzer.checkForChannel(channel)
        h_chanFrac.Fill(channel, fracChanEvents[channel]/myanalyzer.totalEntries)
    myanalyzer.chanPulseVsEvent()
    myanalyzer.fout.cd()
    h_chanFrac.Write()
