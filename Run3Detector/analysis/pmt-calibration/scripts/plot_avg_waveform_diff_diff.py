import sys
try:
    sys.path.remove('/home/users/bemarsh/.local/lib/python2.7/site-packages/matplotlib-1.4.3-py2.7-linux-x86_64.egg')
except:
    pass
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

fb0 = "avg_waveform_pickles/r878b_1450V_2p7V_20ns_300Hz_100000evnts_-5_0.pkl"
fb1 = "avg_waveform_pickles/r878b_1450V_2p7V_20ns_300Hz_100000evnts_5_10.pkl"
fs0 = "avg_waveform_pickles/r878h_1450V_2p7V_20ns_300Hz_400000evnts_v2_-5_0.pkl"
fs1 = "avg_waveform_pickles/r878h_1450V_2p7V_20ns_300Hz_400000evnts_v2_5_10.pkl"

tstart = 280
tend = 390

db0 = pickle.load(open(fb0, 'rb'))
db1 = pickle.load(open(fb1, 'rb'))
ds0 = pickle.load(open(fs0, 'rb'))
ds1 = pickle.load(open(fs1, 'rb'))

def getCorrected(orig_t, orig_v, new_t):
    new_v = []
    it = 0
    for t in new_t:
        if t < orig_t[it]:
            new_v.append(orig_v[it])
        else:
            while it<orig_t.size-1 and t > orig_t[it+1]:
                it += 1
            if it==orig_t.size-1:
                new_v.append(orig_v[it])
            else:
                new_v.append(orig_v[it] + (orig_v[it+1]-orig_v[it])/(orig_t[it+1]-orig_t[it]) * (t-orig_t[it]))
    return np.array(new_v)

time = ds0["t"]
vs0 = ds0["v"]
vs1 = getCorrected(ds1["t"], ds1["v"], time)
vb0 = getCorrected(db0["t"], db0["v"], time)
vb1 = getCorrected(db1["t"], db1["v"], time)


plt.figure()
plt.plot(time, -(vs1-vs0), 'b-', label="LED on")
plt.plot(time, -(vb1-vb0), 'r-', label="LED blocked")
plt.plot([tstart]*2, plt.gca().get_ylim(),'k--')
plt.plot([tend]*2, plt.gca().get_ylim(),'k--')
plt.legend()
plt.xlabel("time (ns)")
plt.ylabel("averaged voltage (mV)")
# plt.savefig("/home/users/bemarsh/public_html/milliqan/pmt_calib/avg_waveforms/diff_diff/sb_0_5_-5_0.png")

plt.figure()
plt.plot(time, -(vs1-vs0)+(vb1-vb0),'g-', label="(LED on) - (LED blocked)")
plt.plot([tstart]*2, plt.gca().get_ylim(),'k--')
plt.plot([tend]*2, plt.gca().get_ylim(),'k--')
plt.gca().set_ylim(-0.10, 0.10)
plt.legend()
plt.xlabel("time (ns)")
plt.ylabel("averaged voltage (mV)")
plt.savefig("/home/users/bemarsh/public_html/milliqan/pmt_calib/avg_waveforms/diff_diff/diff_5_10_-5_0.png")

plt.show()
