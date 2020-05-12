#!/usr/bin/env python
import os, sys, re
import ROOT
import os
from array import array
import cfg
import util as u
import subprocess
#from ROOT import kBlack,kRed,kGreen,kOrange,kBlue,kPink,kYellow,kGray,kMagenta,kSpring,kAzure,kTeal
ROOT.gROOT.SetBatch(ROOT.kTRUE)


if len(sys.argv) < 3:
    sys.exit('usage: {0} <TAG> <run> (<channel>)'.format(sys.argv[0])

TAG = sys.argv[1]
runNum = str(sys.argv[2])

oneChan=-1
if len(sys.argv)>=4:
    oneChan=int(sys.argv[3])

# check if SPE or cosmic run
measureCosmic= ((int(runNum) < 66 or int(runNum)>70)) and runNum != "115" and runNum != "114"
if int(runNum) == 156 or int(runNum) == 157:
    measureCosmic=False
if int(runNum)>=193: measureCosmic=False
if int(runNum)>=425: measureCosmic=True
if int(runNum)>=442 and int(runNum)<=449: measureCosmic=False
if int(runNum)>=523: measureCosmic=False
if int(runNum)>=584 and int(runNum)<=687: measureCosmic=True
if int(runNum)>=699 and int(runNum)<=724: measureCosmic=False
if int(runNum)>=2573 and int(runNum)<=2579: measureCosmic=False
if int(runNum)>=2580 and int(runNum)<=2661: measureCosmic=True
if int(runNum)>=2720 and int(runNum)<=2767: measureCosmic=False
write=True # generate table?
bfield=True # only for naming
u.makeDirRecursive(TAG+"/tables")
tableName = TAG+"/tables/table_run%s_3p8T.csv"%runNum
if (int(runNum)>115 and int(runNum)<=449) or 2573 <= int(runNum) <= 2800:
    bfield = False
    tableName=TAG+"/tables/table_run%s_0T.csv"%runNum

# for SPE runs, multiply the measured mean area by these numbers, to account
# for the fact that the true mean area is a bit lower than the mode
# (these numbers were derived with LED bench tests)           
mean_corrections = {
    "R878":  0.930,
    "R7725": 0.905,
    "ET":    0.980,
    }

useNarrowRange=True or measureCosmic
vetoOtherChannels=True and not measureCosmic
vetoOtherChannels=False # for SPE

u.makeDirRecursive(TAG+"/plots/Run"+runNum+"/measure")
# if not os.path.exists("plots/Run"+runNum):
#     os.mkdir("plots/Run"+runNum)
# if not os.path.exists("plots/Run"+runNum+"/measure"):
#     os.mkdir("plots/Run"+runNum+"/measure")

u.defineColors()

t=u.getTrees(runNum)
print "N entries:",t.GetEntries()
startTime=t.GetMinimum("event_time_b0")
endTime=t.GetMaximum("event_time_b0")
runDuration = endTime - startTime
#if runNum=="425": runDuration= 9*3600

types = ["ET","R878","R7725"]
variables= ["area"]#,"height","duration","delay","dtstart"]
if measureCosmic: variables=["area"]#,"height","duration"]
cosvar=["Pulse area [pVs]", "Pulse height [mV]","Pulse duration [ns]"]
nbins= [[[30,30,30],[40,40,40],[40,40,40],[40,40,40]], #area
        [[60,60,60],[60,60,60]], #height
        [[50,50,50]],#duration
        [[50,50,50]],[[50,50,50]]]
minx=  [[[0,0,0],[0,0,0],[0,0,0],[0,0,0]],#area
        [[0,0,0],[0,0,0]],#height
        [[0,0,0]],#duration
        [[0,0,0]],[[0,0,0]]]
maxx=  [[[300,300,300],[800,800,800],[1500,1500,1500],[5000,5000,5000]], #area
        [[60,60,60],[300,300,300]], #height
        [[100,100,100]], #duration
        [[500,500,500]],[[500,500,500]]]


if measureCosmic:
    nbins= [[[30,30,30],[30,30,30],[30,30,30],[30,30,30],[30,30,30],[30,30,30]], #area
            [[40,40,40],[50,50,50],[50,50,50]], #height
            [[50,50,50]]]#duration
    minx=  [[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],#area
            [[0,0,0],[0,0,0],[0,0,0]],#height
            #[[0,0,0],[0,0,0],[1000,1000,1000],[4000,5000,4000],[2000,2000,2000],[0,0,0]],#area
            [[0,0,0]]]#duration
    maxx=  [[[8000,5000,5000],[20000,10000,10000],[50000,30000,20000],[180000,90000,120000],[60000,60000,60000],[4000,2500,2500]], #area
            [[200,200,200],[500,500,500],[1260,1260,1260]], #height
            #[[8000,5000,5000],[20000,10000,10000],[50000,30000,30000],[180000,100000,120000],[60000,60000,60000],[4000,2500,2500]], #area
            [[250,250,250]]] #duration


##species summary plots
# for itube,tubetype in enumerate(types):
#     for ivar,var in enumerate(variables):
#         hists=[]
#         legs=[]
#         for i,spec in enumerate(cfg.tubeSpecies):
#             if spec != tubetype: continue
#             if i==0 or i==13: continue
#             leg = cosvar[ivar]+", Ch "+str(i)
#             title = ";Pulse area [pVs];Events"
#             if "height" in var: title = ";Pulse height [mV];Events"
#             if "duration" in var: title = ";Pulse Duration [ns];Events"
#             name = "Run "+runNum+" "+leg
#             selection = "chan=="+str(i)

#             hist = u.getHist(t,name,title,selection,var,nbins[ivar][itube],minx[ivar][itube],maxx[ivar][itube])
#             u.cosmeticTH1(hist,i)

#             hists.append(hist)
#             legs.append(leg)


#         filename = "plots/Run%s/Run%s_SPE_%s_%s.pdf" % (runNum, runNum, var, tubetype)
#         u.printTH1s(hists,legs,filename)


##per channel look
## plot first pulse, afterpulses, and cleaned afterpulses
selNames =["First pulses","Afterpulses","Cleaned afterpulses"]
sels= ["ipulse==0","ipulse>0","ipulse>0&&quiet&&delay>20&&sideband_RMS[CHAN]<1.3"] ## have to define cosmic selection channel by channel in loop
# quiet: RMS and mean before pulse = 0

if measureCosmic:
    selNames = ["All events","Vertical cosmics","Cosmics without saturation"]
    sels= ["ipulse==0","ipulse==0&&vert","ipulse==0&&(vert)&&height<1245"]



colIndices= [6,11,9] ## define colors based on channel map

additionalSels=[ [["","",""]] for x in range(32)]

R7725HV= 1600
if int(runNum) in cfg.tableHV:
    R7725HV = cfg.tableHV[int(runNum)][2]

if False: # old channel numbers
    #additionalSels[5].append(["duration<30","duration<30&&height<15","height<15"])
    additionalSels[8].append(["","height>%0.1f"%cfg.fracSPEThresh8[R7725HV],"height>%0.1f"%cfg.fracSPEThresh8[R7725HV]])
    additionalSels[9].append(["","height>%0.1f"%cfg.fracSPEThresh9[R7725HV],"height>%0.1f"%cfg.fracSPEThresh9[R7725HV]])
    additionalSels[10].append(["","height>%0.1f"%cfg.fracSPEThresh10[R7725HV],"height>%0.1f"%cfg.fracSPEThresh10[R7725HV]])
    additionalSels[11].append(["","height>%0.1f"%cfg.fracSPEThresh11[R7725HV],"height>%0.1f"%cfg.fracSPEThresh11[R7725HV]])

measureZoom= [0 for x in range(32)]
if not measureCosmic:
    measureZoom[10]=2
    measureZoom[11]=2
    if R7725HV>1600:
        measureZoom[10]=3
        measureZoom[11]=3

if int(runNum) == 24:
    measureZoom[11] = 0
    measureZoom[9] = 0
    measureZoom[8] = 5
    measureZoom[6] = 1
    measureZoom[5] = 1
    measureZoom[4] = 1
    measureZoom[1] = 1

if int(runNum) == 25:
    measureZoom[11] = 2
    measureZoom[8] = 5
    measureZoom[7] = 2
    measureZoom[6] = 4
    measureZoom[5] = 4
    measureZoom[4] = 4
    measureZoom[3] = 1
    measureZoom[1] = 3

if int(runNum) == 28:
    measureZoom[11] = 3
    measureZoom[10] = 4
    measureZoom[9] = 1
    measureZoom[8] = 1
    measureZoom[7] = 3
    measureZoom[6] = 3
    measureZoom[5] = 3
    measureZoom[4] = 4
    measureZoom[3] = 2
    measureZoom[1] = 3

if int(runNum) == 32:
    measureZoom[1] = 4
    measureZoom[3] = 4


if int(runNum) == 95:
    measureZoom[9] = 5
    measureZoom[6] = 1
    measureZoom[3]=5

if int(runNum) == 97:
    measureZoom[1]=5
    measureZoom[3]=5
    measureZoom[7]=5

if int(runNum) == 156:
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[10]=2
    measureZoom[11]=2
if int(runNum) == 157:
    measureZoom[8]=2

if int(runNum) == 159:
    measureZoom[1]=0
    measureZoom[3]=5
    measureZoom[4]=4
    measureZoom[5]=4
    measureZoom[6]=4
    measureZoom[8]=3
    measureZoom[9]=4
    measureZoom[10]=2
    measureZoom[11]=4

if int(runNum) == 160:
    measureZoom[1]=5
    measureZoom[2]=5
    measureZoom[3]=5
    measureZoom[4]=2
    measureZoom[5]=2
    measureZoom[6]=2
    measureZoom[7]=5
    measureZoom[8]=4
    measureZoom[9]=2
    measureZoom[11]=2

if int(runNum) == 161:
    measureZoom[1]=1
    measureZoom[3]=1
    measureZoom[4]=1
    measureZoom[5]=1
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=2
    measureZoom[9]=1


if int(runNum) == 171:
    measureZoom[1]=4
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[5]=0
    measureZoom[6]=5
    measureZoom[7]=4
    measureZoom[9]=5
    measureZoom[10]=5
    measureZoom[11]=5

if int(runNum) == 172:
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=4
    measureZoom[5]=4
    measureZoom[6]=3
    measureZoom[7]=1
    measureZoom[8]=3
    measureZoom[9]=3
    measureZoom[10]=4
    measureZoom[11]=3

if int(runNum) == 193:
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[10]=1
    measureZoom[11]=1
if int(runNum) == 194:
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[10]=2
    measureZoom[11]=2
if int(runNum) == 195:
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[10]=2
    measureZoom[11]=2

if int(runNum) == 196:
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[7]=1
    measureZoom[8]=3
    measureZoom[9]=1
    measureZoom[10]=3
    measureZoom[11]=3

if int(runNum) == 197:
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[7]=1
    measureZoom[8]=3
    measureZoom[9]=1
    measureZoom[10]=3
    measureZoom[11]=3

if int(runNum) == 425:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=1
    measureZoom[5]=0
    measureZoom[6]=1
    measureZoom[7]=2
    measureZoom[8]=0 # peak quite close to 0
    measureZoom[9]=0
    measureZoom[12]=1
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=1
    measureZoom[24]=1
    measureZoom[25]=0

if int(runNum) == 429:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=1
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=0 # peak quite close to 0
    measureZoom[9]=1
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=1
    measureZoom[22]=1
    measureZoom[23]=2
    measureZoom[24]=1
    measureZoom[25]=1

if int(runNum) == 430:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=2
    measureZoom[5]=2
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=0 # peak quite close to 0
    measureZoom[9]=1
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=1
    measureZoom[17]=1
    measureZoom[22]=2
    measureZoom[23]=1
    measureZoom[24]=1
    measureZoom[25]=1

if int(runNum) == 431:
    measureZoom[0]=0
    measureZoom[1]=0
    measureZoom[2]=0
    measureZoom[3]=0
    measureZoom[4]=1
    measureZoom[5]=2
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=0 # peak quite close to 0
    measureZoom[9]=1
    measureZoom[12]=1
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=1
    measureZoom[22]=2
    measureZoom[23]=1
    measureZoom[24]=1
    measureZoom[25]=1

if int(runNum) == 449:
    measureZoom[22]=1

if int(runNum) == 523:
    measureZoom[0]=0

if int(runNum) == 584:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=1
    measureZoom[5]=1
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=0 # peak quite close to 0
    measureZoom[9]=0
    measureZoom[12]=1
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=0
    measureZoom[22]=1
    measureZoom[23]=3
    measureZoom[24]=0
    measureZoom[25]=0

if int(runNum) == 617:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=1
    measureZoom[5]=1
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=0
    measureZoom[9]=0
    measureZoom[12]=1
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=0
    measureZoom[22]=1
    measureZoom[23]=3
    measureZoom[24]=2
    measureZoom[25]=0

if int(runNum) == 663:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=1
    measureZoom[5]=1
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=0
    measureZoom[9]=2
    measureZoom[12]=1
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=1
    measureZoom[22]=0
    measureZoom[23]=3
    measureZoom[24]=1
    measureZoom[25]=1

if int(runNum) == 672:
    measureZoom[0]=0
    measureZoom[1]=0
    measureZoom[2]=1
    measureZoom[3]=0
    measureZoom[4]=0
    measureZoom[5]=2
    measureZoom[6]=0
    measureZoom[7]=1
    measureZoom[8]=0
    measureZoom[9]=2
    measureZoom[12]=1
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=1
    measureZoom[22]=2
    measureZoom[23]=3
    measureZoom[24]=2
    measureZoom[25]=2

if int(runNum) == 674:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=3
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=1
    measureZoom[9]=3
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=2
    measureZoom[22]=2
    measureZoom[23]=3
    measureZoom[24]=2
    measureZoom[25]=2

# For R878: singleChannel200mVAny878bar.py
# ET=1600, 878=1450, 7725=1450, 878box2=1450, slabs and sheets=1450
if int(runNum) == 700:
    measureZoom[0]=0
    measureZoom[1]=0
    measureZoom[2]=0
    measureZoom[3]=0
    measureZoom[4]=0
    measureZoom[6]=0
    measureZoom[7]=0
    measureZoom[12]=0
    measureZoom[13]=0
    measureZoom[16]=0
    measureZoom[23]=0

# For 7725: singleChannel500mVAny7725
# ET=1570, 878=1430, 7725=1430, 878box2=1430, others slabs and sheets=1450
if int(runNum) == 714:
    measureZoom[5]=0
    measureZoom[22]=1

# For 7725: singleChannel5mVAny7725
# ET=1570, 878=1430, 7725=1430, 878box2=1430, others slabs and sheets=1450
if int(runNum) == 715:
    measureZoom[5]=0
    measureZoom[22]=1

# For ET: singleChannel5mVAnyET
# ET=1570, 878=1430, 7725=1430, 878box2=1430, others slabs and sheets=1450
if int(runNum) == 716:
    measureZoom[8]=0
    measureZoom[9]=0
    measureZoom[17]=0
    measureZoom[24]=0
    measureZoom[25]=0

# For ET: singleChannel5mVAnyET
# ET=1550, 878=1410, 7725=1410, 878box2=1410, others slabs and sheets=1450
if int(runNum) == 723:
    measureZoom[8]=0
    measureZoom[9]=0
    measureZoom[17]=0
    measureZoom[24]=0
    measureZoom[25]=0

# For 7725: singleChannel5mVAny7725
# ET=1550, 878=1410, 7725=1410, 878box2=1410, others slabs and sheets=1450
if int(runNum) == 724:
    measureZoom[5]=0
    measureZoom[22]=1

if int(runNum) == 2584:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=2
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=2
    measureZoom[24]=1
    measureZoom[25]=0

if int(runNum) == 2588:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=3
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=2
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=2
    measureZoom[22]=2
    measureZoom[23]=2
    measureZoom[24]=3
    measureZoom[25]=2

if int(runNum) == 2599:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=4
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=1
    measureZoom[22]=1
    measureZoom[23]=2
    measureZoom[24]=2
    measureZoom[25]=1

if int(runNum) == 2604:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=2
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=1
    measureZoom[22]=0
    measureZoom[23]=2
    measureZoom[24]=1
    measureZoom[25]=0

if int(runNum) == 2608:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=2
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=1
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=2
    measureZoom[24]=1
    measureZoom[25]=0

if int(runNum) == 2609:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=2
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=0
    measureZoom[12]=2
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=1
    measureZoom[24]=0
    measureZoom[25]=0
    measureZoom[20]=1
    measureZoom[28]=1

if int(runNum) == 2611:
    measureZoom[0]=2
    measureZoom[1]=2
    measureZoom[2]=2
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=1
    measureZoom[6]=2
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=0
    measureZoom[12]=2 
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=1
    measureZoom[24]=0
    measureZoom[25]=0
    measureZoom[20]=1
    measureZoom[28]=1

if int(runNum) == 2614:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=2
    measureZoom[4]=2
    measureZoom[5]=1
    measureZoom[6]=1
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=0
    measureZoom[12]=1 
    measureZoom[13]=2
    measureZoom[16]=2
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=1
    measureZoom[24]=0
    measureZoom[25]=0
    measureZoom[20]=1

if int(runNum) == 2616:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=2
    measureZoom[5]=0
    measureZoom[6]=1
    measureZoom[7]=2
    measureZoom[8]=2
    measureZoom[9]=0
    measureZoom[12]=1 
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=1
    measureZoom[24]=0
    measureZoom[25]=0
if int(runNum) in [2617,2618]:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=1
    measureZoom[5]=0
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=2
    measureZoom[9]=0
    measureZoom[12]=1 
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=1
    measureZoom[24]=0
    measureZoom[25]=0

if int(runNum) == 2620:
    measureZoom[0]=1
    measureZoom[1]=1
    measureZoom[2]=1
    measureZoom[3]=1
    measureZoom[4]=1
    measureZoom[5]=0
    measureZoom[6]=1
    measureZoom[7]=1
    measureZoom[8]=1
    measureZoom[9]=0
    measureZoom[12]=1
    measureZoom[13]=1
    measureZoom[16]=1
    measureZoom[17]=0
    measureZoom[22]=0
    measureZoom[23]=1
    measureZoom[24]=0
    measureZoom[25]=0

# need update
measureSels =[0 for x in range(32)]
#if not measureCosmic:
#    measureSels[8]=1
#    measureSels[9]=1
#    measureSels[10]=1
#    measureSels[11]=1

#topChannels= [2,3,6,7,10,11]
slices = [[0,24,8],[1,25,9],[6,16,12],[7,17,13],[2,22,4],[3,23,5],[20,28]] # vertical bars

#if write:
#    table = open("tableSPE.csv","a")
for ichan in range(32):
    if oneChan!=-1 and ichan!=oneChan: continue
    #if measureCosmic and ichan>=12: continue
    if ichan==15: continue
    if cfg.tubeSpecies[ichan] =="veto": continue
    #if ichan!=6: continue
    #if ichan<8 or ichan>11: continue
    for ivar,var in enumerate(variables):
        #if measureCosmic and ivar!=1: continue

        HV = cfg.tableHV[int(runNum)][u.getTubeType(ichan)]
        if ichan==5:
            HV = cfg.tableHV[int(runNum)][3] # this is different than nominal 7725 voltage

        title = ("Run %i, Channel %i, %i V;" % (int(runNum),ichan,HV)) + cosvar[ivar]+";Pulses"

        for iad,addSel in enumerate(additionalSels[ichan]):
            for izoom,zoom in enumerate(nbins[ivar]):
                measureIteration=False
                if write and var == "area" and measureZoom[ichan]==izoom and measureSels[ichan]==iad: measureIteration = True
                if not measureIteration:
                    continue
                #if izoom!=3: continue
                hists=[]
                legs=[]
                for isel,sel in enumerate(sels):
                    thissel = sel.replace("CHAN",str(ichan))
                    if "vert" in thissel:
                        for sli in slices:
                            if ichan in sli:
                                vertSel=""
                                for ics in sli:
                                    if ics != ichan:
                                        if vertSel != "": vertSel=vertSel+"&&"
                                        vertSel = vertSel + "Sum$(area>%.f&&chan==%i)>0" % (cfg.getCosmicThresh(int(runNum),ics),ics)
                                thissel= thissel.replace("vert",vertSel)
                                break


                    selection = "chan==%i&&%s" % (ichan,thissel)
                    vetoSel=""
                    if vetoOtherChannels:
                        for iveto in range(32):
                            if iveto != ichan and iveto != 15:
                                vetoSel = vetoSel + "&&max_%i<5" % iveto
                    if ichan==23:
                        selection += "&&area>10"

                    if addSel[ivar] != "": selection = selection + "&&" +addSel[ivar]
                    print selection
                    itube = u.getTubeType(ichan)

                    name = "Run%s_chan%i_%s_%s_zoom%i" % (runNum,ichan,var,u.cutToString(selection),izoom+1)
                    hist = u.getHist(t,name,title,selection+vetoSel,var,nbins[ivar][izoom][itube],minx[ivar][izoom][itube],maxx[ivar][izoom][itube])

                    u.cosmeticTH1(hist,colIndices[isel])
                    hists.append(hist)
                    legs.append(selNames[isel])

                filename = TAG+"/plots/Run%s/Run%s_SPE_%s_%s_zoom%i.pdf" % (runNum, runNum, var, u.cutToString(selection),izoom+1)
                if measureCosmic: filename = filename.replace("SPE","cosmic")
                if not useNarrowRange: filename = filename.replace(".pdf","fullrange.pdf")
                if vetoOtherChannels: filename = filename.replace(".pdf","_vetoOtherChan.pdf")
                filename= filename.replace("_heightlt1245","").replace("chan","ch").replace("Sumarea","SumA").replace("ipulse","ip")

                #if int(runNum)==28 and izoom+1<3 and ichan != 8 and ichan !=9: continue
                thresh=0
                #print "Measure iteration is ",measureIteration
                if measureCosmic:
                    thresh=cfg.getCosmicThresh(int(runNum),ichan)
                runDuration = t.GetEntries("Sum$(chan=={0})>0".format(ichan))

                # corrections to account for the fact that the mean SPE area is different from the peak SPE area
                meanCorr = 1.00
                if not measureCosmic:
                    meanCorr = mean_corrections[cfg.tubeSpecies[ichan]]

                mean,err,rate = u.printTH1s(hists,legs,filename,runDuration,"area" in var,measureCosmic,False,thresh,useNarrowRange,False,meanCorr=meanCorr)
                if int(runNum)==70: u.printTH1s(hists,legs,filename,runDuration,False,measureCosmic,False,thresh,useNarrowRange,False)

                if measureIteration:
                    u.replaceTableRow(tableName,runNum,ichan,HV,mean,err,rate)

                    measureFilename = filename.replace("Run%s/"%runNum,"Run%s/measure/"%runNum)
                    subprocess.call(["cp", filename, measureFilename])

