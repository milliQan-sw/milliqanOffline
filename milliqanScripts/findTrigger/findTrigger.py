import ROOT as r
import os
import argparse
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
triggerGroups = [(x,y) for x,y in zip([0,1,4,5,8,9],[2,3,6,7,10,11])]
triggerGroups += [(14,12,15)]
def parse_args():
        parser=argparse.ArgumentParser()
        parser.add_argument("--iFile",help="Input file",type=str,required=True)
        parser.add_argument("--oFile",help="Output file",type=str,required=True)
        parser.add_argument("--nCoinc",help="Number of coinc for trigger",type=int,default=2)
        parser.add_argument("--window",help="Trigger window",type=float,default=100.)
        parser.add_argument("--triggerChannels",nargs="+",help="Which channels to use (all if unspecified)",type=int)
        args = parser.parse_args()
        return args

def findTrigger(iFile,oFile,triggerChannels,nCoinc=2,window=100):
    iFile = r.TFile(iFile)
    oFile = r.TFile(oFile,"RECREATE")
    tree = iFile.Get("t")
    newTree = tree.CloneTree(0)
    # leaves = "groupTDCZeroPrev/L"
    # leafValues = array.array("l",[0])
    v_triggerN = r.vector('double')()
    newTree.Branch("triggerN", v_triggerN)
    newTree.SetBranchAddress("triggerN", v_triggerN)
    v_triggerTime = r.vector('double')()
    newTree.Branch("triggerTime", v_triggerTime)
    newTree.SetBranchAddress("triggerTime", v_triggerTime)
    if triggerChannels == None:
        groups = list(set(triggerGroups))
        triggerChannels = range(16)
    else:
        groups = [(x,y) for (x,y) in triggerGroups if x in triggerChannels]
        groups += [(x,y) for (x,y) in triggerGroups if y in triggerChannels]
        groups = list(set(groups))
    print "Running with triggering channels:",triggerChannels
    print groups
    if len(groups) < nCoinc:
        raise ValueError,"Not enough triggering groups! Check your channel selection"
    allFound = 0
    allPulseFound = 0
    for iE,event in enumerate(tree):
        found = {}
        v_triggerN.clear()
        v_triggerTime.clear()
        tree.GetEntry(iE)
        triggers = []
        groupsTemp = groups+[]
        timeInWindow = 0
        startTime = -99999
        triggerDetails = []
        iT = 0
        triggerCandidatesChannel = [x for _,x in sorted(zip(event.triggerCandidates,event.triggerCandidatesChannel))]
        triggerCandidates = sorted(event.triggerCandidates)
        for triggerChan,triggerTime in zip(triggerCandidatesChannel,triggerCandidates):
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
                iGroup = inGroup.index(True)
                del groupsTemp[iGroup]
                triggerDetails.append((iT,triggerChan,triggerTime))
                found[iT] = False
                iT += 1
                if len(triggerDetails) == nCoinc:
                    allFound += 1
                    break
        for pTime,pDuration,pHeight,pChan in zip(event.time,event.duration,event.height,event.chan):
            pNum = -1
            pTrigTime = -1
            if len(triggerDetails) == nCoinc:
                iT = 0
                if pHeight > 5:
                    for triggerDetail in triggerDetails:
                        if found[triggerDetail[0]]: continue
                        if pChan == triggerDetail[1]:
                            if pTime < triggerDetail[2] and triggerDetail[2] < pTime+pDuration:
                                pNum = triggerDetail[0]
                                pTrigTime = triggerDetail[2]
                                found[triggerDetail[0]] = True
                                break
                        iT += 1
            v_triggerN.push_back(pNum)
            v_triggerTime.push_back(pTrigTime)
        newTree.Fill()
        if all(x for x in found.values()) == True:
            allPulseFound +=1
        if (iE*100./tree.GetEntries()) % 20 == 0:
            print "%s" % (iE*1./tree.GetEntries())
    print "Found trigger cands %s of %s" %(allFound,tree.GetEntries())
    print "Found matched pulses %s of %s" %(allPulseFound,tree.GetEntries())
    newTree.AutoSave()
if __name__=="__main__":
    findTrigger(**vars(parse_args()))#iFile,oFile,triggerChannels)
