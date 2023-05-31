#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call

def main(chain,run,nevents,tag,cuts):

    ROOT.PyConfig.IgnoreCommandLineOptions = True # avoid bizarre crash when constructing TChain
    chain.SetEstimate(nevents) # limit how many events are read to memory
    #use Draw to generate table and store in memory
    # goff = graphics off
    chain.Draw("runNumber:fileNumber:event",cuts,"goff")
    selected = chain.GetSelectedRows() #get how many events were found(can be larger than nevents)

    nsel = min(nevents,selected)
    if not os.path.exists(os.getenv("OFFLINEDIR")+"/eventLists"):
        os.mkdir(os.getenv("OFFLINEDIR")+"/eventLists")

    cuts = cuts.replace(">=","ge").replace("<=","le").replace(">","gt").replace("<","lt").replace("==","e")
    cuts = cuts.replace("&&","_").replace("||","_").replace("$","_of").replace("(","_").replace(")","_")
    outFileName = os.getenv("OFFLINEDIR")+"/eventLists/eventList_Run%s_n%s_%s.txt" % (run,nevents,cuts)
    if len(outFileName)>120:
            outFileName=os.getenv("OFFLINEDIR")+"/eventLists/eventList_Run%s_n%s_%s.txt" % (run,nevents,tag)
    runs=chain.GetV1()
    files=chain.GetV2()
    events=chain.GetV3()
    table = []
    with open(outFileName,"w") as outFile:
        for i in range(nsel):
                table.append([int(runs[i]),int(files[i]),int(events[i])])
                row = "%s %s %s\n" % (str(int(runs[i])),str(int(files[i])),str(int(events[i])))
                outFile.write(row)
    outFile.close()
    print ("Wrote list to")
    print (outFileName)
    return table


if __name__ == "__main__":
	if len(sys.argv)<4:
		print ("Usage: ./findEvents.py runNumber selection nEvents")
		print ("If you call this script from bash and use the symbol $ in selection, you must use single quotes or backslash to escape.")
	else: main(sys.argv[1],sys.argv[2],int(sys.argv[3]))
