import os
import sys
import shutil
import argparse

def parseArgs():
    parser=argparse.ArgumentParser()
    parser.add_argument("-c", "--copy", action='store_true', help="Copies any files missing from output directories")
    parser.add_argument("-d", "--delete", action='store_true', help="Delete all files from input directory that are found in output directory")
    parser.add_argument("-i", "--inputDir", type=str, default=None, help="Set the input directory")
    parser.add_argument("-o", "--outputDir", type=str, default=None, help="Set the output directory")
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parseArgs()

    inputDir = '/store/user/milliqan/trees/v34/'
    outputDir = '/store/user/milliqan/trees/v34/1000/'

    if args.inputDir: inputDir = args.inputDir
    if args.outputDir: outputDir = args.outputDir

    checkStr = 'Run10'

    if not os.path.isdir(inputDir):
        print("Input directory {} does not exist".format(inputDir))
        sys.exit(1)

    if not os.path.isdir(outputDir):
        print("Output directory {} does not exist".format(outputDir))
        sys.exit(1)

    print("Looking in {}".format(inputDir))

    for filename in os.listdir(inputDir):
        if checkStr != None and checkStr not in filename: continue
        transferFile = os.path.join(outputDir, filename)
        if not os.path.exists(transferFile):
            if args.copy: 
                shutil.copyfile(inputDir+filename, transferFile)
                print("Copied file {} to {}".format(filename, transferFile))
            else:
                print("File {} does not exist".format(transferFile))
                continue

        if args.delete:
            print(inputDir+filename, "will be deleted")
            os.remove(inputDir+filename)
        

    '''for root, _, filenames in os.walk(inputDir):
        for filename in filenames:
            if checkStr != None and checkStr not in filename: continue
            print(os.path.relpath(os.path.join(root, filename), inputDir))

            transferFile = os.path.join(outputDir, filename)
            if not os.path.exists(transferFile):
                print("File {} does not exist".format(transferFile))
                continue #TODO transfer file here if non existant'''

