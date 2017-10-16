#!/usr/bin/env python
import os, sys, re
import os
from array import array
import ROOT

## This function reads a fill report and returns a list of fill start and end times, in seconds (measured by TTimeStamp relative to Jan 1, 1970 00:00:00 UTC)
outFile = open("collisionsTimeList.txt","w")
with open("FillReport_Oct16.txt") as fills:
	for fill in fills:
		#print fill
		if "Fill" in fill.split("\t")[0]: 
			print "skipping"
			continue
		
		print "\tFill ",fill.split("\t")[0], ", start time ",fill.split("\t")[11],", end time ",fill.split("\t")[13],"Type",fill.split("\t")[14]
		startDate = fill.split("\t")[11]
		year = int(startDate.split(".")[0])
		month = int(startDate.split(".")[1])
		day = int(startDate.split(".")[2].split(" ")[0])
		startTimeList = startDate.split(" ")[2].split(":")
		hours = int(startTimeList[0])#hours
		minutes = int(startTimeList[1])#minutes
		seconds =int(startTimeList[2])#seconds

		#print startDate,startTimeList,year,month,day,hours,minutes,seconds
		#Fill report times are in UTC
		startTime=ROOT.TTimeStamp(year,month,day,hours,minutes,seconds)

		endDate = fill.split("\t")[13]
		year = int(endDate.split(".")[0])
		month = int(endDate.split(".")[1])
		day = int(endDate.split(".")[2].split(" ")[0])
		endTimeList = endDate.split(" ")[2].split(":")
		hours = int(endTimeList[0])#hours
		minutes = int(endTimeList[1])#minutes
		seconds =int(endTimeList[2])#seconds

		endTime=ROOT.TTimeStamp(year,month,day,hours,minutes,seconds)

		duration = round((endTime.GetSec()-startTime.GetSec())/3600.,1)
		fillNum =fill.split("\t")[0].strip()
		fillLumi = fill.split("\t")[7].strip()
		print duration,"hours"
		if "PROTON" in fill.split("\t")[14]:
			outFile.write("%s %s %s %s\n" % (fillNum, str(startTime.GetSec()),str(endTime.GetSec()),fillLumi))



