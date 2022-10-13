import ROOT as r
import pickle
import os
import matplotlib.pyplot as plt
import numpy as np
r.gROOT.SetBatch(True)

inputFile = r.TFile("../inputs/Run110V7.root")
outputFolder = "outputAfterpulsingNew"
if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

inputTree = inputFile.Get('t')

timePrevEvent = 0
timeDiffs = []
nPulsesNoDelay = []
nPulsesDelay = []
compPlots = {'nPulse':([],[]),'height':([],[]),'heightDiff':([],[]),'nPE':([],[])}
for iE,event in enumerate(inputTree):
    eventTime = event.event_trigger_time_tag
    if iE != 0:
        nPEChannel3 =  [nPE for nPE,chan,ipulse in zip(event.nPE,event.chan,event.ipulse) if chan == 3 and ipulse == 0]
        # if len(nPEChannel3) == 0: continue
        # if max(nPEChannel3) < 200 or max(nPEChannel3) == 0: continue
        heights1 = [height for height,chan,ipulse in zip(event.height,event.chan,event.ipulse) if chan == 1 and height >5 and ipulse==0]
        heights3 = [height for height,chan,ipulse in zip(event.height,event.chan,event.ipulse) if chan == 3 and height >5 and ipulse==0]
        nPEs = [nPE for nPE,chan in zip(event.nPE,event.chan) if chan == 1]
        # nPEs = [nPE for nPE,chan in zip(event.nPE,event.chan) if chan == 1]
        if len(heights1) > 0 and len(heights3) > 0:
            timeDiff = eventTime - timePrevEvent
            nPulse = len(heights1)
            timeDiffs.append(timeDiff)
            # if timeDiff < 4.1E4:
            #     compPlots['nPulse'][0].append(nPulse)
            #     if len(heights) > 1:
            #         compPlots['heightDiff'][0].append(heights[0]-heights[1])
            #     compPlots['height'][0].append(heights[0])
            #     compPlots['nPE'][0].append(nPEs[0])
            # elif timeDiff > 1E5:
            #     compPlots['nPulse'][1].append(nPulse)
            #     if len(heights) > 1:
            #         compPlots['heightDiff'][1].append(heights[0]-heights[1])
            #     compPlots['height'][1].append(heights[0])
            #     compPlots['nPE'][1].append(nPEs[0])

    timePrevEvent = eventTime*1.

print len(timeDiffs)
# plt.hist(timeDiffs,bins=np.arange(3.9350E4,3.9550E4,1))
# plt.yscale('log',nonposy='clip')
# plt.hist(timeDiffs,bins=np.logspace(3,10,50))
plt.hist(timeDiffs,bins=range(0,41000000,41000000/1000))
# plt.gca().set_xscale("log")
plt.savefig(outputFolder+"/timeDiff.pdf")
plt.cla()
exit()
# plt.gca().set_xscale("lin")
print max(compPlots['height'][0])
print max(compPlots['heightDiff'][0])
binsDict = {}
binsDict['height'] = range(0,1250,50)
binsDict['heightDiff'] = range(0,1250,50)
binsDict['nPE'] = range(0,1000,10)
binsDict['nPulse'] = range(20)
for name,compPlot in compPlots.iteritems():
    weightsA = np.ones_like(compPlot[0])/float(len(compPlot[0]))
    print name
    plt.hist(compPlot[0],bins=binsDict[name],label="NoDelay",alpha=0.5,weights=weightsA)
    weightsB = np.ones_like(compPlot[1])/float(len(compPlot[1]))
    plt.hist(compPlot[1],bins=binsDict[name],label="Delay",alpha=0.5,weights=weightsB)
    plt.legend()
    plt.savefig(outputFolder+"/"+name+".pdf")
    a = plt.hist(compPlot[0],bins=binsDict[name],label="NoDelay",alpha=0.5)
    b= plt.hist(compPlot[1],bins=binsDict[name],label="Delay",alpha=0.5)
    valsNoDelay = a[0]
    bins = a[1]
    valsDelay = b[0]
    uncsNoDelay = [x**0.5 for x in valsNoDelay]
    uncsDelay = [x**0.5 for x in valsDelay]
    print name
    print "delay", sum(compPlot[1])*1./len(compPlot[1]),sum(compPlot[1])**0.5*1./(len(compPlot[1]))
    print "no delay", sum(compPlot[0])*1./len(compPlot[0]),sum(compPlot[0])**0.5*1./(len(compPlot[0]))
    divs,divUncs = [],[]
    for iX in range(len(valsDelay)):
        if valsNoDelay[iX] != 0:
            div = valsDelay[iX]/valsNoDelay[iX]*weightsB[0]/weightsA[0]
            divUnc = ( (uncsDelay[iX]/(valsDelay[iX]+1E-3))**2+(uncsNoDelay[iX]/valsNoDelay[iX])**2)**0.5*div
        else:
            div = 0
            divUnc = 0
        divs.append(div)
        divUncs.append(divUnc)
    plt.cla()
    plt.errorbar(bins[:-1],divs,divUncs,[0]*len(divs))
    plt.savefig(outputFolder+"/"+name+"_divs.pdf")
    plt.cla()
