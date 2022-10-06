#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call
import findEvents
import argparse
import config as cfg


def parse_args():
	parser=argparse.ArgumentParser()
	parser.add_argument("-i","--inFiles",help="File to run over",type=str,nargs='+')
	parser.add_argument("-l","--LPF",help="apply low pass filter",action="store_true")
	parser.add_argument("-e","--exe",help="executable to run",type=str,default="make_tree")
	parser.add_argument("-p","--pulseInject",help="Inject pulses",action="store_true")
	parser.add_argument("-s","--signalInject",help="Inject signal",type=float,default=-1)
	parser.add_argument("-d","--DRS",help="DRS input",action="store_true")
	args = parser.parse_args()
	#print args
	return args

def main(inFiles,LPF,exe,pulseInject,signalInject,DRS):
	for inFileText in inFiles:
		inFilesTextExpanded = glob.glob(inFileText)
		if len(inFilesTextExpanded) == 0:
			print ("No files found for string: ")
			print (inFileText)
		for inFile in inFilesTextExpanded:
			args = [exe,inFile,"-1","","-1","-1","-1000","-1000","0","0","0",str(int(LPF)),str(int(pulseInject)),str(float(signalInject)),str(int(DRS))]
			call(args)

if __name__ == "__main__":
	#if len(sys.argv)<4:
	#	print "Usage: makeDisplays.py runNumber selection nEvents (optional filename tag)"
	#	print "If you call this script from bash and use the symbol $ in selection, you must use single quotes or backslash to escape."
	#elif len(sys.argv)==4: main(sys.argv[1],sys.argv[2],int(sys.argv[3]))
	#elif len(sys.argv)==5: main(sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4])
	main(**vars(parse_args()))

