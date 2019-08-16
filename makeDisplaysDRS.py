#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call
import findEventsDRS
import argparse
import config as cfg


def parse_args():
	parser=argparse.ArgumentParser()
	parser.add_argument("timestamp",help="timestamp of output file",type=int)
	parser.add_argument("-s","--selection",help="Selection, if you call this script from bash and use the symbol $ in selection, you must use single quotes or backslash to escape.",
	type=str, default="")
	parser.add_argument("nEvents",help="Number of diplays to make",type=int)
	parser.add_argument("-t","--tag",help="Filename tag",default="")
	parser.add_argument("-r","--rangeForTime",nargs=2,help="Force time range for plots (default is zoomed to pulses)",type=float)
	parser.add_argument("-v","--rangeForVoltage",nargs=2,help="Force y range for plots (default is zoomed to pulses)",type=float)
	parser.add_argument("--noBounds",help="Disable display of pulsefinding bounds.",action='store_true',default=False)
	parser.add_argument("-c","--forceChans",nargs='+',help="List of channels to force in display (space separated, any length)")
	parser.add_argument("-f","--fft",help="run FFT",action="store_true")
	parser.add_argument("-l","--LPF",help="apply low pass filter",action="store_true")
	parser.add_argument("-p","--pulseInject",help="Inject pulses",action="store_true")
	parser.add_argument("-q","--signalInject",help="Inject signal",type=float,default=-1)
	parser.add_argument("-o","--onlyForceChans",action='store_true',help="Only show forced chans")
	args = parser.parse_args()
	#print args
	return args

def main(timestamp, selection, nEvents,tag="",rangeForTime=None,rangeForVoltage=None,noBounds=False,forceChans=[],onlyForceChans=False,fft=False,LPF=False,pulseInject=False,signalInject=-1.):
    timestamp = str(timestamp)
    if forceChans == None:
        forceChans = []
    displayPulseBounds = not noBounds
    table = findEventsDRS.main(timestamp,selection,nEvents,tag)
    if len(forceChans) == 0 and onlyForceChans:
        print "No forced chans to show!"
        exit()
    for i in range(len(table)):
        treeName = str(table[i][0])
        eventNumber = str(table[i][1])
        print treeName,eventNumber
        if rangeForTime == None:
            rangeForTime = ["-1","-1"]
        if rangeForVoltage == None:
            rangeForVoltage = ["-1000","-1000"]
        args = ["./make_tree_withDRS",treeName,eventNumber,tag,str(rangeForTime[0]),str(rangeForTime[1]),str(rangeForVoltage[0]),str(rangeForVoltage[1]),str(int(displayPulseBounds)),str(int(onlyForceChans)),str(int(fft)),str(int(LPF)),str(int(pulseInject)),str(float(signalInject)),"1"]
        if forceChans != None:
                args = args + forceChans
        call(args)

if __name__ == "__main__":
	#if len(sys.argv)<4:
	#	print "Usage: makeDisplays.py runNumber selection nEvents (optional filename tag)"
	#	print "If you call this script from bash and use the symbol $ in selection, you must use single quotes or backslash to escape."
	#elif len(sys.argv)==4: main(sys.argv[1],sys.argv[2],int(sys.argv[3]))
	#elif len(sys.argv)==5: main(sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4])
	main(**vars(parse_args()))
