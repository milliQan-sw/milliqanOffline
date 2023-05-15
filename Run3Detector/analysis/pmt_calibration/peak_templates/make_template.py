#########################################################################################################################
# This file expects a root file to be input with a TTree named "Events" and two branches called "voltages" and "times". The pmt type is automatically
# set to r878.
# This file will produce the following items:
# 1.) An area plot of the voltage v time plot.
#
#
#
#
#########################################################################################################################


import os,sys
import numpy as np
import matplotlib.pyplot as plt
import ROOT as r
r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)
r.gErrorIgnoreLevel = r.kWarning

fin = r.TFile("/home/rsantos/Data/PostProcessData/MilliQan_Run848_default_peak_template.root")
tree = fin.Get("Events")

pmt = "r878"
plotdir = "/home/rsantos/Data/Plots/Testing/"
os.system("mkdir -p "+plotdir)
# Previously it looks like pV was used as the measurement for voltage, at OSU milliDAQ used mV. The time is also in seconds when at OSU it is nanoseconds
vrange = (-100,100)

# These times should surround your peak, not too closely though
# since you want to be able to capture photoelectrons on non-optimal paths
tstart = 1200
tend = 1750

# FIXME: This value is probably wrong


control_range=(-5000,3000)


# establish a common set of time points to sync waveforms
# Should be fast; points will be interpolated by the code
# Use 0.2 ns (5 GHz) here. May need to change upper time bound
t_baseline = np.arange(0, 2000+1e-10, 0.2)

# frequencies at which to store final template
output_freqs = [0.7, 1, 2, 5]

# make area histogram for reference
print("Histogramming pulse areas")
c = r.TCanvas("c","c",604,528)

# Create histogram with 125 bins from -500 to 500
h = r.TH1D("h",";pulse area [pVs];Events / 2 pVs", 125, -500, 500) # The ranges should probably not be set directly

h.SetLineColor(r.kBlack)
h.SetLineWidth(2)
tree.Draw("area>>h","") # Draw area branch from root file
line = r.TLine()
line.SetLineStyle(2)
line.SetLineWidth(2)
line.SetLineColor(r.kRed)


m = h.GetMaximum()

# Draw line from (x1, y1) to (x2,y2) where Drawline(x1,y1,x2,y2)
# Draw line at control range
line.SetLineColor(r.kRed)
line.DrawLine(control_range[0], 0, control_range[0], m)
line.DrawLine(control_range[1], 0, control_range[1], m)

# Draw lines vertical lines at vrange value
line.SetLineColor(r.kBlue)
line.DrawLine(vrange[0], 0, vrange[0], m)
line.DrawLine(vrange[1], 0, vrange[1], m)
# line.DrawLine(control_range[0], 0, control_range[0], m)
# line.DrawLine(control_range[1], 0, control_range[1], m)


# Save files
c.SaveAs(os.path.join(plotdir, "pulse_area.png"))
c.SaveAs(os.path.join(plotdir, "pulse_area.pdf"))


# first get average "control" waveform (i.e., 0PE, just background), the area must be greater than -5 and less than 3
print("Loop over tree to get average 0-PE control waveform")

# Draw values inside the area branch that are between values in control range
tree.Draw(">>entrylist", "area>{0} && area<{1}".format(*control_range), "goff")
el = r.gDirectory.Get("entrylist")
nent = el.GetN()

for i in range(nent):
    tree.GetEntry(el.GetEntry(i))

    # Get all the times and voltages from the tree
    ts = np.array(list(tree.times))
    vs = np.array(list(tree.voltages))

    # interpolate into the predefined baseline time points
    vs = np.interp(t_baseline, ts, vs)

    # Calculate the average voltage
    if i==0:
        avg_control = np.array(vs)
    else:
        avg_control += vs

avg_control /= nent

# now get average SPE pulse, first subtracting off average control from each waveform. For the r878 the vrange is from 25 to 35
print("Loop over tree to get average control-subtracted SPE waveform")
tree.Draw(">>entrylist", "area>{0} && area<{1}".format(*vrange), "goff")
el = r.gDirectory.Get("entrylist")
nent = el.GetN()
waveforms = []

for i in range(nent):
    # Loop through all entries
    tree.GetEntry(el.GetEntry(i))
    ts = np.array(list(tree.times))
    vs = np.array(list(tree.voltages))

    # interpolate into the predefined baseline time points
    vs = np.interp(t_baseline, ts, vs)
    
    waveforms.append(vs)

    # Subtract off average voltage
    if i==0:
        avg_spe = np.array(vs)
        avg_spe_fix = np.array(vs - avg_control)
    else:
        avg_spe += vs
        avg_spe_fix += vs - avg_control

avg_spe /= nent
avg_spe_fix /= nent
# Needs to be converted to ROOT files
plt.figure(figsize=(6,5), dpi=100)
plt.plot(t_baseline, avg_control, 'r-', label="Average 0-PE control")

plt.plot(t_baseline, avg_spe, 'b-', label="Average SPE")

# These plot the vertical lines on the plot
plt.plot([tstart]*2, [np.amin(avg_spe), np.amax(avg_spe)], 'k--')

plt.plot([tend]*2, [np.amin(avg_spe), np.amax(avg_spe)], 'k--')

plt.gca().set_ylim(ymax=1.3*np.amax(avg_spe))

plt.legend(loc='upper left')
plt.savefig(os.path.join(plotdir, "avg_spe_control.png"))
plt.savefig(os.path.join(plotdir, "avg_spe_control.pdf"))

plt.figure(figsize=(6,5), dpi=100)


plt.plot(t_baseline, avg_spe_fix, 'g-', label="Average corrected-SPE")

# Plots vertical lines on plot
plt.plot([tstart]*2, [np.amin(avg_spe_fix), np.amax(avg_spe_fix)], 'k--') # Will plot two points, for 878, at (280, min(avg_spe_fix)) and another at (280, max(avg_spe_fix))
plt.plot([tend]*2, [np.amin(avg_spe_fix), np.amax(avg_spe_fix)], 'k--') # Plot two point similar to previous line

dt = 100
plt.gca().set_xlim(tstart-dt, tend+dt)
plt.gca().set_ylim(ymax=1.3*np.amax(avg_spe_fix))
plt.legend(loc='upper left')
plt.savefig(os.path.join(plotdir, "avg_spe_fixed.png"))
plt.savefig(os.path.join(plotdir, "avg_spe_fixed.pdf"))

# TODO Start Here
def get_template(avg):
    imin = np.argmax(t_baseline > tstart) # Find first value in t_baseline that is greater than tstart
    imax = np.argmax(t_baseline > tend)
    template = np.array(avg[imin:imax]) # The template is only the values between imin and imax and averaged
    template /= np.sum(template)
    return template

# NOTE Don't worry about make_event_display or anywhere it's used. This should just plot
# unrelated things to the template
def make_event_display(avg, vs, draw_smoothed=False, saveAs=None):
    template = get_template(avg)
    print(vs)
    print(template[::-1])
    # NOTE Don't know why the template is reversed or why i_peak is defined the way it is, check here for errors
    smoothed = np.convolve(template[::-1], vs, mode='valid')
    offset = np.argmax(template)
    i_peak = offset + np.argmax(smoothed)

    #NOTE The time is divide by the area of the waveform plot???
    fitted = template * np.trapz(vs[i_peak-offset:i_peak-offset+template.size], t_baseline[:template.size]) / np.trapz(template, t_baseline[:template.size])
    mults = np.linspace(0.5,2.0,101)
    sses = []
    for a in mults:
        test = fitted * a
        sses.append(np.sum((vs[i_peak-offset:i_peak-offset+template.size] - test)**2))    
    mult = mults[np.argmax(-np.array(sses))]
    fitted *= mult

    plt.plot(t_baseline, vs, '-', color="0.6")
    if draw_smoothed:
        plt.plot(t_baseline[offset:offset+smoothed.size], smoothed, 'r-', lw=2)
    plt.plot(t_baseline[i_peak-offset:i_peak-offset+fitted.size], fitted, 'g-', lw=2)
    plt.gca().set_xlim(tstart-70, tend+70)
    plt.gca().set_ylim(ymin = -2 if pmt=="r878" else -10, ymax=np.amax(vs)*1.2)
    plt.savefig(os.path.join(plotdir, saveAs+".png"))
    plt.savefig(os.path.join(plotdir, saveAs+".pdf"))
    
vs = waveforms[0] - avg_control
plt.figure(figsize=(6,5), dpi=100)

make_event_display(avg_spe_fix, vs, draw_smoothed=True, saveAs="samp_smoothed")

os.system("mkdir -p "+plotdir+"/events")
for i in range(10):
    plt.clf()
    vs = waveforms[i] - avg_control
    make_event_display(avg_spe_fix, vs, draw_smoothed=False, saveAs="events/event{0:03d}".format(i))


print("Loop over tree to get average time-corrected SPE waveform")
template = get_template(avg_spe_fix)
offset = np.argmax(template)
t_peaks = []
for i in range(nent):
    vs = waveforms[i] - avg_control
    
    # smooth to find the peak
    smoothed = np.convolve(template[::-1], vs, mode='valid')
    t_peak = t_baseline[offset+np.argmax(smoothed)]
    t_peaks.append(t_peak)

    # shift in time and re-interpolate into the baseline time points
    vs = np.interp(t_baseline, t_baseline-(t_peak-t_peaks[0]), vs)
    if i==0:
        avg_spe_tcorr = np.array(vs)
    else:
        avg_spe_tcorr += vs

avg_spe_tcorr /= nent

if pmt=="r878":
    # weird noise issue in 878 after averaging... smooth out here
    ones = np.ones(21)

    # Moving sum of width 21
    avg_spe_tcorr = np.convolve(ones, avg_spe_tcorr, mode='same')

    # How many averages you took
    counts = np.convolve(ones, np.ones(avg_spe_tcorr.size), mode='same')


    avg_spe_tcorr /= counts

# plot histogram of peak time
plt.figure(figsize=(6,5), dpi=100)
plt.hist(t_peaks, range=[np.mean(t_peaks)-20, np.mean(t_peaks)+20], bins=40, histtype='step')
plt.savefig(os.path.join(plotdir, "time_spread.png"))
plt.savefig(os.path.join(plotdir, "time_spread.pdf"))

# plot time-corrected template
plt.figure(figsize=(6,5), dpi=100)
plt.plot(t_baseline, avg_spe_fix, 'r-', label="Non-time-shifted SPE average")
plt.plot(t_baseline, avg_spe_tcorr, 'g-', lw=2, label="Time-shifted SPE average")
plt.plot([tstart]*2, [np.amin(avg_spe_tcorr), np.amax(avg_spe_tcorr)], 'k--')
plt.plot([tend]*2, [np.amin(avg_spe_tcorr), np.amax(avg_spe_tcorr)], 'k--')
dt = 100 if pmt=="r878" else 50
plt.gca().set_xlim(tstart-dt, tend+dt)
plt.gca().set_ylim(ymax=1.35*np.amax(avg_spe_tcorr))
plt.legend(loc='upper left')
plt.savefig(os.path.join(plotdir, "avg_spe_fixed_tcorr.png"))
plt.savefig(os.path.join(plotdir, "avg_spe_fixed_tcorr.pdf"))

vs = waveforms[0] - avg_control
plt.figure(figsize=(6,5), dpi=100)
make_event_display(avg_spe_tcorr, vs, draw_smoothed=True, saveAs="samp_smoothed_tcorr")

os.system("mkdir -p "+plotdir+"/events_tcorr")
for i in range(10):
    plt.clf()
    vs = waveforms[i] - avg_control
    make_event_display(avg_spe_tcorr, vs, draw_smoothed=False, saveAs="events_tcorr/event{0:03d}".format(i))





############# Important Part of the Code ####################################
template = get_template(avg_spe_tcorr)
offset = np.argmax(template)
# redefine t=0 to be the maximum of the template
t_template = t_baseline[:template.size] - t_baseline[offset]


print("Generating templates at frequencies", output_freqs, "GHz")
hs = {}

for freq in output_freqs:
    dt = 1.0 / freq
    np_left = int(abs(t_template[0]) / dt)+1
    np_right = int(abs(t_template[-1]) / dt)+1
    
    ts = np.append(
        np.linspace(-np_left*dt, 0, np_left+1),
        np.linspace(dt, np_right*dt, np_right),
        )

    out = np.interp(ts, t_template, template, left=0.0, right=0.0) # This gets the time
    out /= np.trapz(out, ts) # Take the area underneath the graph
    hs[freq] = r.TH1D("h"+str(freq), ";time[ns]", out.size, 0, out.size*dt)
    for i in range(out.size):
        hs[freq].SetBinContent(i+1, out[i])

c = r.TCanvas("c2","c2",604, 528)
for freq in output_freqs:
    c.Clear()
    hs[freq].SetLineColor(r.kBlack)
    hs[freq].Draw("HIST")
    c.SaveAs(os.path.join(plotdir, "template_{0}_GHz.png".format(str(freq).replace(".","p"))))
    c.SaveAs(os.path.join(plotdir, "template_{0}_GHz.pdf".format(str(freq).replace(".","p"))))
    
