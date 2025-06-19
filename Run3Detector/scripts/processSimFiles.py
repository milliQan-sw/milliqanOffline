import ROOT as r
import os
import argparse
import shutil

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--inputFile",help="File to run over",type=str, required=True)
    parser.add_argument('-o', '--outputFile', help="Output file", type=str, required=True)
    parser.add_argument('-d', '--outputDir', help='Output directory to move file to', type=str, default=None)
    args = parser.parse_args()
    return args


if __name__ == "__main__":


    debug = False
    force = True
    dataDir = '/abyss/users/mcarrigan/milliqan/pulseInjectedSignal/'
    outputDir = os.getcwd()

    args = parse_args()
    if args.outputDir:
        outputDir = args.outputDir

    script_dir = os.path.dirname(os.path.realpath(__file__))
    r.gSystem.Load(script_dir+'/../../../MilliDAQ/libMilliDAQ.so')
    r.gROOT.LoadMacro(script_dir+'/../analysis/simConversion/utils/globalEventConv.C')

    tmp_output = '/'.join([os.getcwd(), args.outputFile.split('.root')[0] + '_tmp.root'])
    print("Trying to process {} into {}".format(args.inputFile, tmp_output))
    r.globalEventConv(args.inputFile, tmp_output)

    cmd = 'python3 scripts/runOfflineFactory.py --inputFile {} --outputFile {} --sim --exe ./run.exe'.format(tmp_output, args.outputFile)
    os.system(cmd)

    if outputDir != os.getcwd():
        shutil.move('/'.join([os.getcwd(), args.outputFile]), '/'.join([outputDir, args.outputFile]))
