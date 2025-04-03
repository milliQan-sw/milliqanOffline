import ROOT as r
import os
import argparse
import shutil
import sys
import json

################################################################################################
# This file acts as a wrapper to process the pulse injection through offline tree processing
################################################################################################

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--inputFile",help="File to run over",type=str, default=None)
    parser.add_argument('-o', '--outputFile', help="Output file", type=str, default=None)
    parser.add_argument('-d', '--outputDir', help='Output directory to move file to', type=str, default=None)
    parser.add_argument('-n', '--number', help="Process number to load from fileList", type=int, default=None)
    parser.add_argument('-f', '--fileList', help="file list containing input and output file for running with condor", type=str, default=None)
    args = parser.parse_args()
    return args


if __name__ == "__main__":


    debug = False
    force = True
    dataDir = '/data/user/mcarrigan/milliqan/signalSim/'
    outputDir = os.getcwd()

    processingDir = "/../../../../"
    #processingDir = '/'

    args = parse_args()
    if args.outputDir:
        outputDir = args.outputDir

    if args.inputFile!=None and args.outputFile!=None:
        inputFile = args.inputFile
        outputFile = args.outputFile
    elif args.number!=None and args.fileList!=None:
        f_in = open(args.fileList)
        f_list = json.load(f_in)
        inputs = f_list[str(args.number)]
        inputFile = inputs[0]
        outputFile = inputs[1]
        f_in.close()
    else:
        print("Error need to either provide input and output files or a filelist and run number")
        sys.exit(0)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(script_dir+processingDir+'/milliQanSim/inputData/waveinject_v2.C')

    os.chdir('milliqanOffline/Run3Detector/')
    os.system('source setup.sh')
    os.chdir('../../')


    pulse_output = '/'.join([os.getcwd(), outputFile.split('.root')[0] + '_pulseInjected.root'])
    print("Processing pulse injection {} -> {}".format(inputFile, pulse_output))

    r.gROOT.LoadMacro(script_dir+processingDir+'milliQanSim/inputData/waveinject_v2.C')
    r.waveinject_v2(inputFile, pulse_output, script_dir+processingDir+'milliQanSim/inputData/modified_waveform.root')

    r.gSystem.Load(script_dir+processingDir+'MilliDAQ/libMilliDAQ.so')
    r.gROOT.LoadMacro(script_dir+processingDir+'milliqanOffline/Run3Detector/analysis/simConversion/utils/globalEventConv.C')

    tmp_output = '/'.join([os.getcwd(), outputFile.split('.root')[0] + '_globalEvent.root'])
    print("Processing Global event {} -> {}".format(pulse_output, tmp_output))
    r.globalEventConv(pulse_output, tmp_output)

    os.chdir('milliqanOffline/Run3Detector/')

    print("Processing offline tree {} -> {}".format(tmp_output, outputFile))
    cmd = 'source $PWD/setup.sh && python3 scripts/runOfflineFactory.py --inputFile {} --outputFile {} --sim --exe ./run.exe'.format(tmp_output, outputFile)
    os.system(cmd)

    if outputDir != os.getcwd():
        print(f"Moving {outputFile} to {args.outputDir+'/trees/'}")
        if os.path.exists(args.outputDir+'/trees/'+outputFile):
            os.remove(args.outputDir+'/trees/'+outputFile)
        shutil.move(outputFile, args.outputDir+'/trees/')
        os.chdir('../../')
        print(f"Moving {pulse_output} to {args.outputDir+'/pulseInjected/'}")
        if os.path.exists(args.outputDir+'/pulseInjected/'+pulse_output):
            os.remove(args.outputDir+'/pulseInjected/'+pulse_output)
        shutil.move(pulse_output, args.outputDir+'/pulseInjected/')
        print(f"Moving {tmp_output} to {args.outputDir+'/globalEvent/'}")
        if os.path.exists(args.outputDir+'/globalEvent/'+tmp_output):
            os.remove(args.outputDir+'/globalEvent/'+tmp_output)
        shutil.move(tmp_output, args.outputDir+'/globalEvent/')

