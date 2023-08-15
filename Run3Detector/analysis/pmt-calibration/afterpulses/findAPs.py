import time
import sys, os
import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

def findAPs(time, voltage, offset, noise, template, main_peak_start, main_peak_end, plot=False, outName=None, 
            convolved=None, baseline=None, remove_neg_spikes=False):

    voltage = np.array(voltage)-offset
    if convolved is None:
        convolved = np.convolve(voltage, template[::-1], mode='valid')
    if baseline is None:
        baseline = np.zeros(time.size)
    if remove_neg_spikes:
        voltage = voltage*(voltage>baseline-4*noise) + baseline*(voltage<=baseline-4*noise)

    imax = np.argmax(template)
    convolved_time = time[imax:imax+convolved.size]
    convolved_baseline = baseline[imax:imax+convolved.size]

    max_inds = []
    for i in range(convolved.size):
        if convolved_time[i] > main_peak_end and convolved[i] >= np.amax(convolved[max(0,i-5):min(convolved.size,i+6)]) and convolved[i] > convolved_baseline[i] + noise*0.75:
            oi = i + imax

            # argmax finds the index of the maximum value
            # in this case, find the largest voltage near the found peak, +-10 bins to each side
            imaxnear = np.argmax(voltage[oi-10:oi+10]) + (oi-10)
            end1, end2 = imaxnear, imaxnear

            # find the boundaries of the peak by tracing until we hit 0 or the endpoints of the waveform
            while time[end1] > main_peak_end and (voltage[end1] > baseline[end1]-noise/2):
                end1 -= 1
            while  end2 < voltage.size-1 and (voltage[end2] > baseline[end2]-noise/2):
                end2 += 1
            
            # don't count if we've hit a boundary
            if time[end1] <= main_peak_end or end2 == voltage.size-1:
                continue
            # if something went wrong and our original peak isn't in our found boundaries
            if not end1 <= oi <= end2:
                continue

            # make sure we don't double count
            if len(max_inds)>0 and (end1, end2) == max_inds[-1][1]:
                # same boundaries, but this one has a higher maximum
                # delete previous one and save this one
                if convolved[oi-imax] > convolved[max_inds[-1][0]-imax]:
                    max_inds = max_inds[:-1]
                # same boundaries, but previous one has a higher maximum
                # skip this one
                else:
                    continue

            area = np.trapz(voltage[end1:end2+1]-baseline[end1:end2+1], time[end1:end2+1])
            max_inds.append((oi, (end1, end2), area))


    if plot and outName is not None:
        plt.figure(1, figsize=(12,9))
        plt.clf()
        plt.plot(time,voltage, 'b-')
        plt.plot([main_peak_start]*2, [-5,30], 'k--')
        plt.plot([main_peak_end]*2, [-5,30], 'k--')
        plt.plot([0,time[-1]], [0,0], 'k--')
        plt.plot([0,time[-1]], [noise]*2, 'k--')
        plt.plot([0,time[-1]], [-noise]*2, 'k--')
        plt.plot(convolved_time, convolved, 'r-', linewidth=2)
        plt.plot(time[:template.size], template*75, 'g-', linewidth=2)
        for oi,(lb,hb),area in max_inds:
            plt.fill_between([time[lb], time[hb]], [0]*2, [20]*2, color='k', alpha=0.2)
            plt.plot([time[oi]]*2, [0, 20], 'k:')
            plt.text(np.mean([time[lb],time[hb]]), 20.2, "{0:.1f}".format(area), fontsize='small', horizontalalignment='center')
        plt.gca().set_ylim(-5, 30)
        plt.gca().set_xlim(0, time[-1])
        plt.xlabel("Time (ns)")
        plt.ylabel("Voltage (mV)")
        plt.savefig(outName)

    return max_inds

if __name__=="__main__":
    # template = pickle.load(open("../../pmt_calib/peak_templates/template_peak_70_75_0p7GHz.pkl", 'rb'))[::2]
    template = pickle.load(open("../../pmt_calib/peak_templates/template_peak_70_75_1GHz.pkl", 'rb'))[::2]
    template /= np.sum(template)
    
    tstart = 150
    tend = 290

# f = r.TFile("../../pmt_calib/output/r878h_1450V_2p7V_20ns_300Hz_400000evnts_v2.root")
    fname = "/nfs-7/userdata/bemarsh/milliqan/pmt_calib/processed/afterpulses/test_postprocessed.root"
    # fname = "/nfs-7/userdata/bemarsh/milliqan/pmt_calib/processed/afterpulses/r878_1450V_1p9V_300Hz_0p7GHz_200000evnts.root"
    f = r.TFile(fname)
    t = f.Get("Events")

    bn = fname.split("/")[-1].split(".")[0]
    outdir = "/home/users/bemarsh/public_html/milliqan/aps/" + bn
    os.system("mkdir -p " + outdir)
    os.system("cp ~/scripts/index.php " + outdir)

    start = time.time()

    # for i in range(200):
    for i in range(t.GetEntries()):
        t.GetEntry(i)

        # print i
        
        times = np.array(list(t.times))
        voltage = -np.array(list(t.voltages))
                            
        max_inds = findAPs(times, voltage, t.offset, t.noise, template, tstart, tend, plot=False, outName=outdir+"/{0:05d}.png".format(i))
        
        if i%10==0:
            print i, [mi[0] for mi in max_inds]


    end = time.time()

    print "Time elapsed:", end-start
