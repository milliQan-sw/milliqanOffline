#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call
import argparse


def parse_args():
	parser=argparse.ArgumentParser()
        parser.add_argument("-i","--inputFile",help="File to run over",type=str, required=True)
        parser.add_argument("-o","--outputFile",help="Output file name",type=str, required=True)
        parser.add_argument("-e","--exe",help="Executable to run",type=str,default="./test.exe")
        parser.add_argument("-c","--configurations",help="JSON Configuration files or string",type=str,nargs="+")
	args = parser.parse_args()
	#print args
	return args

def runOfflineFactory(inputFile,outputFile,exe,configurations):
    if not configurations:
        configurations = "/home/milliqan/milliqanOffline/offlineProduction/configuration/chanMaps/testMap.json,/home/milliqan/milliqanOffline/offlineProduction/configuration/pulseFinding/pulseFindingTest.json,/home/milliqan/milliqanOffline/offlineProduction/configuration/calibrations/testCalibration.json"
    if "{" in configurations and "}" in configurations:
        args = " ".join([exe,"-i "+inputFile,"-o "+outputFile,"-c "+",".join(configurations)])
    else:
        args = " ".join([exe,"-i "+inputFile,"-o "+outputFile,"-c "+",".join(configurations)])
    os.system(args)

if __name__ == "__main__":
	runOfflineFactory(**vars(parse_args()))

