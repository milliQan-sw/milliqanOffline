import sys
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

# fb = "r878b_1450V_2p7V_20ns_300Hz_100000evnts_-5_0.pkl"
fb = "r878h_1450V_2p7V_20ns_300Hz_400000evnts_v2_-5_0.pkl"
fs = "r878h_1450V_2p7V_20ns_300Hz_400000evnts_v2_70_75.pkl"
# fs = "r878b_1450V_2p7V_20ns_300Hz_100000evnts_0_5.pkl"

tstart = 280
tend = 390

db = pickle.load(open(fb, 'rb'))
ds = pickle.load(open(fs, 'rb'))

corrb_t = ds["t"]
corrb_v = []
it = 0
for t in corrb_t:
    if t < db["t"][it]:
        corrb_v.append(db["v"][it])
    else:
        while it<db["t"].size-1 and t > db["t"][it+1]:
            it += 1
        if it==db["t"].size-1:
            corrb_v.append(db["v"][it])
        else:
            corrb_v.append(db["v"][it] + (db["v"][it+1]-db["v"][it])/(db["t"][it+1]-db["t"][it]) * (t-db["t"][it]))


# corrb_t = db["t"]
# corrb_v = db["v"]

corrb_v = np.array(corrb_v)
corrb_t = np.array(corrb_t)

plt.figure()
plt.plot(corrb_t, -corrb_v, 'r-', label="Low-area control sample")
plt.plot(ds["t"], -ds["v"], 'b-', label="Signal")
ylim = plt.gca().get_ylim()
plt.plot([tstart]*2, ylim, 'k--')
plt.plot([tend]*2, ylim, 'k--')
plt.xlabel("time (ns)")
plt.ylabel("voltage (mV)")
plt.legend(loc='upper left', fontsize='medium')
# plt.savefig("/home/users/bemarsh/public_html/milliqan/pmt_calib/avg_waveforms/diff/sb_25_30_-5_0.png")

plt.figure()
plt.plot(ds["t"],-ds["v"]+corrb_v,'g-', label="Noise subtracted off")
ylim = plt.gca().get_ylim()
plt.plot([tstart]*2, ylim,'k--')
plt.plot([tend]*2, ylim,'k--')
plt.xlabel("time (ns)")
plt.ylabel("voltage (mV)")
plt.legend(loc='upper left', fontsize='medium')
# plt.savefig("/home/users/bemarsh/public_html/milliqan/pmt_calib/avg_waveforms/diff/diff_25_30_-5_0.png")

diff = -ds["v"]+corrb_v
pickle.dump(diff, open("diff_70_75_-5_0.pkl",'wb'))

plt.show()
