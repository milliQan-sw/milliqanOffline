#! /usr/bin/env/python

## take output root file from processBinary.py and
## add higher level information like pulse time, area, etc

import sys
import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import pickle as pickle

tstart = 230
tend   = 330

# tstart = 200
# tend   = 310

# tstart = 280
# tend   = 390

# determine the pulse time/width and store in tree
# (fairly time-consuming)
doTiming = False

if doTiming:
    # template = pickle.load(open("peak_templates/template_peak_70_75_2GHz.pkl", 'rb'))[::2]
    template = pickle.load(open("peak_templates/template_peak_r7725_400_550_1GHz.pkl", 'rb'))[::1]
    template /= np.sum(template)

f = r.TFile(sys.argv[1], "UPDATE")
t = f.Get("Events")
#times = np.zeros(1024, dtype=float)
#voltages = np.zeros(1024, dtype=float)
area = np.array([0], dtype=float)
offset = np.array([0], dtype=float)
noise = np.array([0], dtype=float)
smoothed_max = np.array([0], dtype=float)
tmax = np.array([0], dtype=float)
thalfmax = np.array([0], dtype=float)
fwhm = np.array([0], dtype=float)


t.SetBranchStatus("*", 0)
t.SetBranchStatus("times", 1)
t.SetBranchStatus("voltages", 1)
nt = t.CloneTree()

#nt.SetBranchAddress("times",times)
#nt.SetBranchAddress("voltages",voltages)
b_area = nt.Branch("area", area, "area/D")
b_offset = nt.Branch("offset", offset, "offset/D")
b_noise = nt.Branch("noise", noise, "noise/D")
b_smoothed_max = nt.Branch("smoothed_max", smoothed_max, "smoothed_max/D")
b_tmax = nt.Branch("tmax", tmax, "tmax/D")
b_thalfmax = nt.Branch("thalfmax", thalfmax, "thalfmax/D")
b_fwhm = nt.Branch("fwhm", fwhm, "fwhm/D")

Nevt = nt.GetEntries()
print("Nevt: " , Nevt)
for ievt in range(Nevt):
    print("This is ievt", ievt)
    nt.GetEntry(ievt)
    print("got entry")
    voltages = np.array(list(nt.voltages))
    print(voltages)
    times = np.array(list(nt.times))
    if ievt%10000==0:
        print("iEvt:", ievt)

    vs = -1*voltages

    # for j in range(1,vs.size):
    #     if abs(vs[j] - vs[j-1]) > 10:
    #         vs[j] = vs[j-1]
    istart = np.argmax(times>tstart+times[0])
    iend = np.argmax(times>tend+times[0])
    print("istart: " , istart)

    # offset[0] = np.median(vs)
    offset[0] = np.mean(vs[30:int(istart*3/4)])
    noise[0] = 0.5*(np.percentile(vs[:int(istart*3/4)],95) - np.percentile(vs[:int(istart*3/4)],5))
    
    vs -= offset[0]

    area[0] = np.trapz(vs[istart:iend], times[istart:iend])

    if not doTiming:
        smoothed_max[0] = -999
        tmax[0] = -999
        thalfmax[0] = -999
    else:
        convolved = np.convolve(vs, template[::-1], mode='valid')
        imax = np.argmax(template)
        convolved_time = times[imax:imax+convolved.size]
        icstart = np.argmax(convolved_time>tstart + times[0])
        icend = np.argmax(convolved_time>tend + times[0])
        icmax = np.argmax(convolved[icstart:icend]) + icstart
        cmax = convolved[icmax]
        ihm = icmax
        while ihm > icstart and convolved[ihm] > cmax/2:
            ihm -= 1
        if cmax < 0.5 or convolved[ihm] > cmax/2:
            thalfmax[0] = -999
        else:
            thalfmax[0] = convolved_time[ihm] + (convolved_time[ihm+1]-convolved_time[ihm])/(convolved[ihm+1]-convolved[ihm]) * (cmax/2 - convolved[ihm])
        ihm = icmax
        while ihm <icend and convolved[ihm] > cmax/2:
            ihm += 1
        if cmax < 0.5 or convolved[ihm] > cmax/2 or thalfmax[0]<0:
            fwhm[0] = -999
        else:
            fwhm[0] = convolved_time[ihm] + (convolved_time[ihm-1]-convolved_time[ihm])/(convolved[ihm-1]-convolved[ihm]) * (cmax/2 - convolved[ihm])
            fwhm[0] -= thalfmax

        smoothed_max[0] = cmax
        tmax[0] = convolved_time[icmax]

    b_area.Fill()
    b_offset.Fill()
    b_noise.Fill()
    b_smoothed_max.Fill()
    b_tmax.Fill()
    b_thalfmax.Fill()
    b_fwhm.Fill()

nt.Write("Events",r.TObject.kWriteDelete)
f.Close()
