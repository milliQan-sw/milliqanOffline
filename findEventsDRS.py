#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call
import config as cfg

def main(timestamp,cuts,nevents,tag):
	ROOT.PyConfig.IgnoreCommandLineOptions = True # avoid bizarre crash when constructing TChain

	treeList=glob.glob(cfg.offlineDir+"DRS/trees/Run*"+timestamp+"/*"+timestamp+".root")
        print cfg.offlineDir+"DRS/trees/Run*"+timestamp+"/*"+timestamp+".root"
        print treeList
        cutsName = cuts.replace(">=","ge").replace("<=","le").replace(">","gt").replace("<","lt").replace("==","e")
        cutsName = cuts.replace("&&","_").replace("||","_").replace("$","_of").replace("(","_").replace(")","_")
	outFileName = cfg.offlineDir+"eventListsDRS/eventList_Run%s_n%s_%s.txt" % (timestamp,nevents,cutsName)
        if len(outFileName)>120:
                outFileName=cfg.offlineDir+"eventListsDRS/eventList_Run%s_n%s_%s.txt" % (timestamp,nevents,tag)
        outFile = open(outFileName,"w")
        table = []
        nselTot = 0
        for fileName in treeList:
            fileNameDRS = fileName.split("/")[-1][3:]
	    t = ROOT.TChain("t")
            if "SignalInjected" in fileName: continue
	    t.Add(fileName)

	    t.SetEstimate(nevents) # limit how many events are read to memory
            #use Draw to generate table and store in memory
            # goff = graphics off
            t.Draw("event",cuts,"goff")
            selected = t.GetSelectedRows() #get how many events were found(can be larger than nevents)
	
	    nsel = min(nevents,selected)

	    events=t.GetV1()
            for i in range(nsel):
                table.append([cfg.rawDirDRS+"/"+fileNameDRS,int(events[i])])
                row = "%s %s\n" % (cfg.rawDirDRS+"/"+fileNameDRS,str(int(events[i])))
                outFile.write(row)
                nselTot += 1
                if nselTot >= nevents:
                    return table
        outFile.close()
	print "Wrote list to",outFileName
	return table


if __name__ == "__main__":
	if len(sys.argv)<4:
		print "Usage: ./findEvents.py runNumber selection nEvents"
		print "If you call this script from bash and use the symbol $ in selection, you must use single quotes or backslash to escape."
	else: main(sys.argv[1],sys.argv[2],int(sys.argv[3]))

