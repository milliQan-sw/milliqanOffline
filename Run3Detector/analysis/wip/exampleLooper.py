from ROOT import TFile, TTree, TH1F, TChain
import os
import sys
import time

#returns a TChain of all files in run 
def getTChain(runNum):

    #directory where files are stored
    fileDir = '/store/user/mcarrigan/trees/v29/'

    fileStr = 'MilliQan_Run' + str(runNum)

    #define TChain for tree 't'
    mychain = TChain('t')

    #loop over files in directory
    for filename in os.listdir(fileDir):
        if not filename.endswith('.root'): continue
        if not filename.startswith(fileStr): continue

        #add files to the chain
        mychain.Add(fileDir + filename)

    return mychain


if __name__ == "__main__":

    #run number
    runNum = 591

    #define histograms
    h_numChannels = TH1F("h_numChannels", "Number of Channels Passing Cuts in Event", 20, 0, 20)
    h_timePulse = TH1F("h_timePulse", "Time of Pulses Passing Cuts in Event", 2600, 0, 2600)

    #define output root file
    f_out = TFile.Open('outputFile.root', 'recreate')

    #get the TChain 
    mychain = getTChain(runNum)

    #get number of events in run
    numEntries = mychain.GetEntries()

    print("There are {0} events in run {1}".format(numEntries, runNum))

    #timing script
    time1 = time.time()

    #loop over events in TChain ievent=index, event=event object
    for ievent, event in enumerate(mychain):

        #Print out every 1000 events so we know we are running
        if ievent%1000 == 0: 
            time2 = time.time()
            print("Working on event {}".format(ievent))
            print("Took {} seconds to run over 1k events".format(time2-time1))
            time1 = time2

        #bool to track if event passes our cuts
        passCuts = False

        #channels passing cut
        chanList = []

        #loop over the pulses in an event
        for ipulse, pulse in enumerate(event.ipulse):

            #make sure event is not pickup
            if event.pickupFlag[ipulse]: continue
            
            #make sure event is from bar
            if event.type[ipulse] != 0: continue

            #selection cuts
            if event.height[ipulse] < 20: continue
            if event.area[ipulse] < 10: continue
            if event.nPE[ipulse] < 10: continue
            if event.duration[ipulse] < 10: continue

            passCuts = True

            if event.chan[ipulse] not in chanList: chanList.append(event.chan[ipulse])

            #fill histograms for pulses
            h_timePulse.Fill(event.time[ipulse])

        #Now fill event wide histograms
        if passCuts:

            h_numChannels.Fill(len(chanList))

    #make sure we are writing to f_out
    f_out.cd()

    #Write our histograms
    h_timePulse.Write()
    h_numChannels.Write()

    #close our file
    f_out.Close()
        




            
            



