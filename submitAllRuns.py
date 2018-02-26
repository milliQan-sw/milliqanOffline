#!/usr/bin/env python
import os, sys, re
import ROOT
import glob
import math
from subprocess import call
import processRun

#os.system("root -b -q compile.C")
runList = set([x.split("Run")[1].split("/")[0] for x in glob.glob("/net/cms26/cms26r0/milliqan/UX5/Run*/")])
for i in runList:
    #if int(i) < 30 or int(i) >= 115: continue
    processRun.main(i)
