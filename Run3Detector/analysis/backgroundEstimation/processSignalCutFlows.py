import os
import ROOT as r


if __name__ == "__main__":

    beam = True
    skim = False
    sim = True 
    qualityLevel = 'override'
    maxEvents = None

    dataDir = '/eos/experiment/milliqan/sim/bar/signal/'

    info_out = open('signalCutFlowInfo.txt', 'w+')
 
    for ifile, filename in enumerate(os.listdir(dataDir)):

        #if ifile > 2: break

        if not filename.endswith('root'):
            continue

        inputFile = '/'.join([dataDir, filename])
        
        mass = filename.split('_')[-1].replace('.root', '')
        charge = filename.split('_')[-2]
        outputFile = 'bgCutFlow_{}_{}.root'.format(charge, mass)

        cmd = 'python3 backgroundCutFlow.py {} {} {} {} {} {} {}'.format(beam, skim, sim, outputFile, qualityLevel, inputFile, maxEvents)

        print(cmd)
        os.system(cmd)

        fin = r.TFile.Open(outputFile, 'READ')
        h_eventCutFlow = fin.Get('eventCutFlow')
        nBins = h_eventCutFlow.GetNbinsX()
        totalEvents = h_eventCutFlow.GetBinContent(1)
        passingEvents = h_eventCutFlow.GetBinContent(nBins)

        ratio = passingEvents/totalEvents
        print("Total events: {}, Total passing: {} ({})".format(totalEvents, passingEvents, ratio))
        info_out.write(f'{totalEvents} {passingEvents} {ratio}\n')

        fin.Close()
    
    info_out.close()

