import os
import sys
import numpy as np
from ROOT import TFile, TTree
import json

def getFile(fileNum):

    filelist = open('filelist.json')
    files = json.load(filelist)['filelist']
    filelist.close()

    return files[fileNum]


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Error need to provide the file number")
        sys.exit(1)

    thisNum = int(sys.argv[1])

    fileName = getFile(thisNum)
    runInfo = fileName.split('_')[1]

    print('Trying to open file', fileName)

    myfile = TFile.Open(fileName)
    mytree = myfile.Get('t')

    print('opened file')

    nameOut = 'MilliQan_' + runInfo + '_MuonSkim_v29.root'
    f_out = TFile.Open(nameOut, 'recreate')
    t_out = mytree.CloneTree(0)

    print("Cloned tree as {}".format(nameOut))

    numEventsPass = 0

    #loop over events in TChain ievent=index, event=event object
    for ievent, event in enumerate(mytree):

        #Print out every 1000 events so we know we are running
        if ievent%1000 == 0: 
            print("Working on event {}".format(ievent))

        #bool to track if event passes our cuts
        passCuts = False

        #loop over the pulses in an event
        for ipulse, pulse in enumerate(event.ipulse):

            #make sure event is not pickup
            if event.pickupFlag[ipulse]: continue

            if event.height[ipulse] < 500: continue

            passCuts = True

        if passCuts:
            numEventsPass += 1
            t_out.Fill()

    print("Total number of events passing cuts {0}".format(numEventsPass))
    
    if numEventsPass > 0:
        f_out.cd()
        t_out.Write()

    f_out.Close()