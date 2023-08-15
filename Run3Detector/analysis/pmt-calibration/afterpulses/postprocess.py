import os, sys
import ROOT as r
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt
from findAPs import findAPs

# t0 = 140
t0 = 75
minamp = 300
# tend   = 290

Nevt = -1
plotFirst = 0
make_output_tree = True

f = r.TFile(sys.argv[1])
t = f.Get("Events")
print "Reading from:", sys.argv[1]

outname = sys.argv[1].split(".")[0] + "_postprocessed.root"
bn = sys.argv[1].split("/")[-1].split(".")[0]
outdir = "/home/users/bemarsh/public_html/milliqan/aps/{0}".format(sys.argv[1].split("/")[-1].split(".")[0])
os.system("mkdir -p "+outdir)
os.system("cp /home/users/bemarsh/scripts/index.php "+outdir)

if make_output_tree:
    print "Outputting to:", outname
    fout = r.TFile(outname, "RECREATE")

if plotFirst>0:
    print "Plotting to:", outdir
    plt.figure(1, figsize=(12,9))

times = np.zeros(1024, dtype=float)
voltages = np.zeros(1024, dtype=float)
area = np.array([0], dtype=float)
offset = np.array([0], dtype=float)
noise = np.array([0], dtype=float)
raw_max = np.array([0], dtype=float)
smoothed_max = np.array([0], dtype=float)
tmax = np.array([0], dtype=float)
tstart = np.array([0], dtype=float)
tend = np.array([0], dtype=float)
thalfmax = np.array([0], dtype=float)
n_APs = np.array([0], dtype=int)
AP_time = np.zeros(100, dtype=float)
AP_area = np.zeros(100, dtype=float)
AP_height = np.zeros(100, dtype=float)
AP_lowbound = np.zeros(100, dtype=float)
AP_highbound = np.zeros(100, dtype=float)

if Nevt<0:
    Nevt = t.GetEntries()
t.SetBranchStatus("*", 0)
t.SetBranchStatus("times", 1)
t.SetBranchStatus("voltages", 1)
nt = t.CloneTree(Nevt)

nt.SetBranchAddress("times",times)
nt.SetBranchAddress("voltages",voltages)
b_area = nt.Branch("area", area, "area/D")
b_offset = nt.Branch("offset", offset, "offset/D")
b_noise = nt.Branch("noise", noise, "noise/D")
b_raw_max = nt.Branch("raw_max", raw_max, "raw_max/D")
b_smoothed_max = nt.Branch("smoothed_max", smoothed_max, "smoothed_max/D")
b_tmax = nt.Branch("tmax", tmax, "tmax/D")
b_tstart = nt.Branch("tstart", tstart, "tstart/D")
b_tend = nt.Branch("tend", tend, "tend/D")
b_thalfmax = nt.Branch("thalfmax", thalfmax, "thalfmax/D")
b_n_APs = nt.Branch("n_afterpulses", n_APs, "n_afterpulses/i")
b_AP_time = nt.Branch("afterpulse_time", AP_time, "afterpulse_time[n_afterpulses]/D")
b_AP_area = nt.Branch("afterpulse_area", AP_area, "afterpulse_area[n_afterpulses]/D")
b_AP_height = nt.Branch("afterpulse_height", AP_height, "afterpulse_height[n_afterpulses]/D")
b_AP_lowbound = nt.Branch("afterpulse_lowbound", AP_lowbound, "afterpulse_lowbound[n_afterpulses]/D")
b_AP_highbound = nt.Branch("afterpulse_highbound", AP_highbound, "afterpulse_highbound[n_afterpulses]/D")

# template = pickle.load(open("../peak_templates/template_peak_70_75_1GHz.pkl", 'rb'))[::2]
template = pickle.load(open("../peak_templates/template_peak_r7725_400_550_1GHz.pkl", 'rb'))[::1]
template /= np.sum(template)

baseline = pickle.load(open("scripts/baseline_pickles/{0}.pkl".format(bn), 'rb'))

for ievt in range(Nevt):
# for i in range(10000):
    nt.GetEntry(ievt)
    if ievt%1000==0:
        print "iEvt:", ievt

    vs = -voltages

    i0 = np.argmax(times > t0)

    offset[0] = np.median(vs[30:i0*3/4])
    vs_nospikes = vs*(vs>-4)+offset*(vs<=-4)
    noise[0] = 0.5*(np.percentile(vs_nospikes[30:i0*3/4],95) - np.percentile(vs_nospikes[30:i0*3/4],5))

    vs -= offset
    vs_nospikes = vs*(vs>baseline-4*noise)+baseline*(vs<=baseline-4*noise)

    istart = np.argmax(vs[i0:] > minamp) + i0
    iend = istart
    while vs[istart] > 0 or vs[istart-1] > 0:
        istart -= 1
    while vs[iend] > 0 or vs[iend+1] > 0:
        iend += 1
    tstart[0] = times[istart]
    tend[0] = times[iend]
    if tstart[0]<30:
        print "WARNING: tstart shouldn't be this low! {0} {1}".format(tstart[0], ievt)
        continue
    if tstart[0]>300:
        raise Exception("tstart shouldn't be this high! {0} {1}".format(tstart[0], ievt))
    # if tend[0]>450:
    #     raise Exception("tend shouldn't be this high! {0} {1}".format(tend[0], ievt))

    area[0] = np.trapz(vs[istart:iend], times[istart:iend])

    convolved = np.convolve(vs_nospikes, template[::-1], mode='valid')
    imax = np.argmax(template)
    convolved_time = times[imax:imax+convolved.size]
    icstart = np.argmax(convolved_time>tstart[0] + times[0])
    icend = np.argmax(convolved_time>tend[0] + times[0])
    icmax = np.argmax(convolved[icstart:icend]) + icstart
    cmax = convolved[icmax]
    ihm = icmax
    while ihm > icstart and convolved[ihm] > cmax/2:
        ihm -= 1
    if cmax < 0.5 or convolved[ihm] > cmax/2:
        thalfmax[0] = -999
    else:
        thalfmax[0] = convolved_time[ihm] + (convolved_time[ihm+1]-convolved_time[ihm])/(convolved[ihm+1]-convolved[ihm]) * (cmax/2 - convolved[ihm])

    raw_max[0] = np.amax(vs[istart:iend])
    smoothed_max[0] = cmax
    tmax[0] = convolved_time[icmax]

    peaks = findAPs(times, vs, 0, noise[0], template, tstart[0], tend[0], convolved=convolved, baseline=baseline, remove_neg_spikes=True)
    n_APs[0] = len(peaks)
    for i in range(len(peaks)):
        idx = peaks[i][0]
        end1, end2 = peaks[i][1]
        parea = peaks[i][2]

        AP_time[i] = times[idx]
        AP_area[i] = parea
        AP_height[i] = vs[idx]
        AP_lowbound[i] = times[end1]
        AP_highbound[i] = times[end2]

    if ievt < plotFirst:
        plt.clf()
        plt.plot(times,vs+offset[0],color="red")
        plt.axvline(tstart,ls="dashed",color="black")
        plt.axvline(tend,ls="dashed",color="black")
        # plt.axhspan(offset[0]-noise[0],offset[0]+noise[0],color='red',alpha=0.3)
        # plt.axhline(offset[0],ls="dashed",color="black")
        # plt.axhline(offset[0]-noise[0],ls="dashed",color="black",lw=1.2)
        # plt.axhline(offset[0]+noise[0],ls="dashed",color="black",lw=1.2)
        plt.plot(times, baseline+offset[0], 'k--')
        plt.plot(times, baseline+offset[0]+noise[0], 'k--')
        plt.plot(times, baseline+offset[0]-noise[0], 'k--')
        plt.fill_between(times, baseline+offset[0]+noise[0], baseline+offset[0]-noise[0], color='r', alpha=0.3)
        plt.plot(convolved_time, convolved+offset[0], 'b-', linewidth=2)
        plt.plot(times[:template.size], template*75+offset[0], 'g-', linewidth=2)
        plt.xlim(0,times[-1])
        plt.xlabel('Time (ns)')
        # plt.ylim(-5,100)
        plt.ylim(-5,25)
        plt.ylabel('Vout (mV)')

        plt.grid(True)
        plt.title("waveform{0:05d}".format(ievt))
        inds = [p[0] for p in peaks]
        plt.plot(times[inds],vs[inds]+offset[0],"x",markersize=10,markeredgewidth=3,color='Blue',alpha=0.5)

        for j in range(len(peaks)):
            end1, end2 = peaks[j][1]
            ypos = np.amax(vs[end1:end2]) + offset[0]
            ypos = min(ypos, 22.5)
            plt.text(np.mean([times[end1],times[end2]]), ypos+0.4, "{0:.1f}".format(AP_area[j]), fontsize='medium', horizontalalignment='center')
            plt.fill_between(times[end1:end2+1],baseline[end1:end2+1]+offset[0],[ypos]*(end2-end1+1),color="k",alpha=0.2)
            

        plt.savefig(outdir+"/wavform{0:05d}.png".format(ievt))

    b_area.Fill()
    b_offset.Fill()
    b_noise.Fill()
    b_raw_max.Fill()
    b_smoothed_max.Fill()
    b_tmax.Fill()
    b_tstart.Fill()
    b_tend.Fill()
    b_thalfmax.Fill()
    b_n_APs.Fill()
    b_AP_time.Fill()
    b_AP_area.Fill()
    b_AP_height.Fill()
    b_AP_lowbound.Fill()
    b_AP_highbound.Fill()

if make_output_tree:
    nt.Write("Events",r.TObject.kWriteDelete)
    fout.Close()

f.Close()
