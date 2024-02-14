import os
import sys


from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *


    

mycuts = milliqanCuts()

fileNumber = 1163

#filelist =[f'/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run{fileNumber}.4_v34.root:t']

#"""
filelist = []

def appendRun(filelist,run):
    #directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/1000/"
    directory = "/mnt/hadoop/se/store/user/milliqan/trees/v34/"
    for filename in os.listdir(directory):
        if filename.startswith(f"MilliQan_Run{run}") and filename.endswith(".root"):
            filelist.append(directory+filename+":t")
cosmicGoodRun = [fileNumber]

for run in cosmicGoodRun:
    appendRun(filelist,run)
#"""

branches = ['boardsMatched', 'nPE', 'layer','type','chan','pickupFlag']

#require pulses are not pickup
pickupCut = mycuts.getCut(mycuts.pickupCut, 'pickupCut', cut=True, branches=branches)

#require that all digitizer boards are matched
boardMatchCut = mycuts.getCut(mycuts.boardsMatched, 'boardMatchCut', cut=True, branches=branches)

pulseNpeh = r.TH1F("pulseNpeh","pulse NPE histogram;pulse NPE; events",500,0,1000)

#define milliqan plotter
myplotter = milliqanPlotter()

myplotter.addHistograms(pulseNpeh,'nPE' ,'barCut')

cutflow = [boardMatchCut,pickupCut,mycuts.barCut, myplotter.dict['pulseNpeh']]

#create a schedule of the cuts
myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

#print out the schedule
myschedule.printSchedule()

#create the milliqan processor object
myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

#run the milliqan processor
myiterator.run()


output_file = r.TFile(f"Run{fileNumber}NPEdist.root", "RECREATE")
pulseNpeh.Write()
output_file.Close()
