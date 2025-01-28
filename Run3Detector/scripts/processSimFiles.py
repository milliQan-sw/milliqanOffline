import ROOT as r
import os


if __name__ == "__main__":


    debug = False
    dataDir = '/abyss/users/mcarrigan/milliqan/pulseInjectedSignal/'

    script_dir = os.path.dirname(os.path.realpath(__file__))
    r.gSystem.Load(script_dir+'/../../../MilliDAQ/libMilliDAQ.so')
    r.gROOT.LoadMacro(script_dir+'/../analysis/simConversion/utils/globalEventConv.C')


    for ifile, filename in enumerate(os.listdir(dataDir)):
        if debug and ifile > 0: break

        if not filename.endswith('.root'): continue
       
        inputFile = '/'.join([dataDir, filename])
        charge = filename.split('_')[3]
        mass = filename.split('_')[2]
        outputFile = f'MilliQan_globalEvent_{charge}_{mass}.root'
        finalOutput = 'MilliQan_sim_{}_{}.root'.format(charge, mass)
        
        if os.path.exists(finalOutput): continue

        print("Trying to process {} into {}".format(inputFile, outputFile))
        r.globalEventConv(inputFile, outputFile)

        cmd = 'python3 scripts/runOfflineFactory.py --inputFile {} --outputFile {} --sim --exe ./run.exe'.format(outputFile, finalOutput)
        os.system(cmd)
