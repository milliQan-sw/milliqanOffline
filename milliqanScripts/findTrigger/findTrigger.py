#!/usr/bin/env python

import ROOT as r
import os
import argparse
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
triggerGroups = [(x,y) for x,y in zip([3,7,11,1,5,9],[2,6,10,0,4,8])]
triggerGroups += [(14,12,15)]

intraModuleCalibrations = [0.0, 0.0, -2.5, -7.5, 0.625, 0.0, 1.875, 10.0, 1.25, 0.0, -3.75, -3.75, -1.875, 0.0, -24.375, -5.0]
interModuleCalibrations = [0.0, 0.0, 0.0, 0.0, -6.25, -6.25, -6.25, -6.25, 8.125, 8.125, 8.125, 8.125, -6.25, 0.0, 8.125, 0.0]
totalCalib = [x+y for x,y in zip(interModuleCalibrations,intraModuleCalibrations)]
def parse_args():
        parser=argparse.ArgumentParser()
        parser.add_argument("--iFile",help="Input file",type=str,required=True)
        parser.add_argument("--oFile",help="Output file",type=str,required=True)
        parser.add_argument("--nCoinc",help="Number of coinc for trigger",type=int,default=2)
        parser.add_argument("--window",help="Trigger window",type=float,default=100.)
        parser.add_argument("--triggerChannels",nargs="+",help="Which channels to use (all if unspecified)",type=int)
        parser.add_argument("--runRange",nargs="+",help="Run range",type=int)
        parser.add_argument("--maxSkip",help="Shift starting position maxSkip times incase window start position is causing issue",type=int,default=999)
        args = parser.parse_args()
        return args

def findTrigger(iFile,oFile,triggerChannels,nCoinc=2,window=100,maxSkip=1,runRange=None):
    if not runRange:
        runRange = [-10000,10000]
    elif len(runRange) != 2 or runRange[0] > runRange[1]:
        raise ValueError,"Run range must be empty or format: lower upper"
    iFile = r.TFile(iFile)
    oFile = r.TFile(oFile,"RECREATE")
    tree = iFile.Get("t")
    newTree = tree.CloneTree(0)
    nEventsTwentyPerc = tree.GetEntries()*0.2
    # leaves = "groupTDCZeroPrev/L"
    # leafValues = array.array("l",[0])
    v_triggerN = r.vector('double')()
    newTree.Branch("triggerN", v_triggerN)
    newTree.SetBranchAddress("triggerN", v_triggerN)
    v_triggerTime = r.vector('double')()
    newTree.Branch("triggerTime", v_triggerTime)
    newTree.SetBranchAddress("triggerTime", v_triggerTime)
    v_triggerNCalib = r.vector('double')()
    newTree.Branch("triggerNCalib", v_triggerNCalib)
    newTree.SetBranchAddress("triggerNCalib", v_triggerNCalib)
    v_triggerTimeCalib = r.vector('double')()
    newTree.Branch("triggerTimeCalib", v_triggerTimeCalib)
    newTree.SetBranchAddress("triggerTimeCalib", v_triggerTimeCalib)
    if triggerChannels == None:
        groups = list(set(triggerGroups))
        triggerChannels = range(16)
    else:
        groups = [X for X in triggerGroups if len(set(X).intersection(set(triggerChannels))) > 0]
        groups = list(set(groups))
    print "Running with triggering channels:",triggerChannels
    if len(groups) < nCoinc:
        raise ValueError,"Not enough triggering groups! Check your channel selection"
    allFound = 0
    allPulseFound = 0
    # averageTimeBetweenPulses = 0
    for iE,event in enumerate(tree):
        if iE % int(nEventsTwentyPerc) == 0:
            print "Processed %.1f" % (iE*100./tree.GetEntries()) + "%"
        if event.run < runRange[0] or event.run > runRange[1]:
            continue
        if iE == 0:
            continue
        found = {}
        v_triggerN.clear()
        v_triggerTime.clear()
        v_triggerNCalib.clear()
        v_triggerTimeCalib.clear()
        tree.GetEntry(iE)
        groupsTemp = groups+[]
        triggerCandidatesChannel = [x for _,x in sorted(zip(event.triggerCandidates,event.triggerCandidatesChannel))]
        triggerCandidates = sorted(event.triggerCandidates)
        # deltas = [triggerCandidates[i] - triggerCandidates[i-1] for i in range(1,len(triggerCandidates))]
        # averageTimeBetweenPulses += sum(deltas)*1./len(deltas)
        skip = 0
        triggerDetails = []
        while (len(triggerDetails) != nCoinc):
            if skip >= maxSkip: break
            triggerDetails = []
            timeInWindow = 0
            startTime = -99999
            iT = 0
            groupsTemp = groups + []
            for triggerChan,triggerTime in zip(triggerCandidatesChannel[skip:],triggerCandidates[skip:]):
                if triggerChan not in triggerChannels: continue
                inGroup = [triggerChan in x for x in groupsTemp]
                # print triggerChan,triggerTime
                if any(inGroup):
                    timeInWindow = triggerTime-startTime
                    if timeInWindow > window:
                        startTime = triggerTime
                        triggerDetails = []
                        iT = 0
                        groupsTemp = groups+[]
                        timeInWindow = 0
                    iGroup = inGroup.index(True)
                    del groupsTemp[iGroup]
                    triggerDetails.append((iT,triggerChan,triggerTime,triggerTime+totalCalib[triggerChan]))
                    found[iT] = False
                    iT += 1
                    if len(triggerDetails) == nCoinc:
                        allFound += 1
                        break
            skip+=1
        sortedByCalibTriggerDetails = sorted(triggerDetails,key=lambda x: x[3])
        for pTime,pDuration,pHeight,pChan in zip(event.time,event.duration,event.height,event.chan):
            pNum = -1
            pTrigTime = -1
            pNumCalib = -1
            pTrigTimeCalib = -1
            if len(triggerDetails) == nCoinc:
                if pHeight > 5:
                    for iSorted,triggerDetail in enumerate(sortedByCalibTriggerDetails):
                        if found[triggerDetail[0]]: continue
                        if pChan == triggerDetail[1]:
                            if pTime < triggerDetail[2] and triggerDetail[2] < pTime+pDuration:
                                pNum = triggerDetail[0]
                                pNumCalib = iSorted
                                pTrigTime = triggerDetail[2]
                                pTrigTimeCalib = triggerDetail[3]
                                found[triggerDetail[0]] = True
                                break
            v_triggerN.push_back(pNum)
            v_triggerTime.push_back(pTrigTime)
            v_triggerNCalib.push_back(pNumCalib)
            v_triggerTimeCalib.push_back(pTrigTimeCalib)
        newTree.Fill()
        if all(x for x in found.values()) == True:
            allPulseFound +=1
    print "Found trigger cands %s of %s" %(allFound,tree.GetEntries())
    print "Found matched pulses %s of %s" %(allPulseFound,tree.GetEntries())
    newTree.AutoSave()
if __name__=="__main__":
    findTrigger(**vars(parse_args()))#iFile,oFile,triggerChannels)
