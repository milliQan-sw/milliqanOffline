import sys
import os
import ROOT as r
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

name = "r878_1450V_1p90V_13ns_300Hz_50000evnts"
# name = "afterpulses/r7725_1450V_2p4V_13ns_300Hz_1p0GHz_500000evnts"
# name = "r7725/r7725_1600V_1p89V_13ns_300Hz_20000evnts"

outdir = "/home/users/bemarsh/public_html/milliqan/pmt_calib/plots/{0}/".format(name)

os.system("mkdir -p {0}".format(outdir))
os.system("cp ~/scripts/index.php {0}".format(outdir))

f = r.TFile("/nfs-7/userdata/bemarsh/milliqan/pmt_calib/processed/{0}.root".format(name))
t = f.Get("Events")

times = np.zeros(1024, dtype=float)
voltages = np.zeros(1024, dtype=float)

t.SetBranchAddress("times",times)
t.SetBranchAddress("voltages",voltages)

plt.figure(1)

# tstart = 280
# tend   = 390

# tstart = 200
# tend   = 310

# tstart = 280
# tend   = 350

tstart = 230
tend   = 330

Nevt = t.GetEntries()
# for i in range(Nevt):
for i in range(50):
# for i in range(267,268):
    t.GetEntry(i)

    vs = -voltages

    # for j in range(1,vs.size):
    #     if abs(vs[j] - vs[j-1]) > 10:
    #         vs[j] = vs[j-1]

    istart = np.argmax(times>tstart+times[0])
    iend = np.argmax(times>tend+times[0])

    offset = np.mean(vs[10:istart * 3/4])
    noise = 0.5*(np.percentile(vs[:istart*3/4],95) - np.percentile(vs[:istart*3/4],5))
    
    area = np.trapz(vs[istart:iend] - offset, times[istart:iend])

    plt.clf()
    plt.plot(times,vs,'r')
    plt.grid()
    plt.xlabel("Time (ns)")
    plt.ylabel("Voltage (mV)")
    mint = np.amin(times)
    maxt = np.amax(times)
    plt.gca().set_xlim(mint-25, maxt+25)
    # plt.gca().set_xlim(mint-25, 425)
    plt.gca().set_ylim(-1, np.amax(vs)*1.3)
    # plt.gca().set_ylim(-10, 100)
    plt.plot([mint-25, maxt+25], [offset, offset], 'k-')
    plt.plot([mint-25, maxt+25], [offset+noise, offset+noise], 'k--')
    plt.plot([mint-25, maxt+25], [offset-noise, offset-noise], 'k--')
    plt.plot([times[istart],times[istart]], plt.gca().get_ylim(), 'k--')
    plt.plot([times[iend-1],times[iend-1]], plt.gca().get_ylim(), 'k--')
    plt.fill_between([mint-25, maxt+25], offset-noise, offset+noise, color='r', alpha=0.25)
    plt.text(0.10, 0.93, "Area = {0:.1f} mV$\cdot$nS".format(area), transform=plt.gca().transAxes)
    # plt.text(0.60, 0.93, "Area = {0:.1f} mV$\cdot$nS".format(area), transform=plt.gca().transAxes)

    plt.savefig(outdir + "/rawevt{0:06d}.png".format(i))


    # print area
