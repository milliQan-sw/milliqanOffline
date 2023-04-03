import sys
try:
    sys.path.remove('/home/users/bemarsh/.local/lib/python2.7/site-packages/matplotlib-1.4.3-py2.7-linux-x86_64.egg')
except:
    pass
import cPickle as pickle
import ROOT as r
import numpy as np
import matplotlib.pyplot as plt

f = r.TFile(sys.argv[1])
tree = f.Get("Events")

if len(sys.argv) > 2:
    sel = sys.argv[2]
else:
    sel = ""

tstart = 280
tend = 390

tree.Draw(">>entrylist",sel,"goff")
el = r.gDirectory.Get("entrylist")

nent = el.GetN()
nent = 10000
print "Number selected events:",nent
time = []
voltages = []
noise = 0.0
for i in range(nent):
# for i in range(100000):
    if i%10000==0:
        print "event", i
    tree.GetEntry(el.GetEntry(i))
    if i==0:
        time = np.array(list(tree.times))
        voltages = np.array(list(tree.voltages)) + float(tree.offset)
    else:
        ts = np.array(list(tree.times))
        vs = np.array(list(tree.voltages)) + float(tree.offset)

        adj_vs = []
        it = 0
        for t in time:
            if t <= ts[it]:
                adj_vs.append(vs[it])
                if it>2:
                    raise Exception("{0} {1} {2} {3}".format(it, t, ts[it], ts[it+1]))
            else:
                while it<ts.size-1 and t > ts[it+1]:
                    it += 1
                if it==ts.size-1:
                    adj_vs.append(vs[it])
                else:
                    adj_vs.append(vs[it] + (vs[it+1]-vs[it])/(ts[it+1]-ts[it]) * (t-ts[it]))
                    if not ts[it] < t <= ts[it+1]:
                        raise Exception("{0} {1} {2} {3}".format(it, t, ts[it], ts[it+1]))
        voltages += adj_vs

        # voltages += vs

    noise += float(tree.noise)

voltages /= nent
noise /= nent
noise /= np.sqrt(nent)

plt.plot(time, -voltages)
plt.plot([tstart]*2, plt.gca().get_ylim(),'k--')
plt.plot([tend]*2, plt.gca().get_ylim(),'k--')
plt.plot(plt.gca().get_xlim(), [noise, noise], 'k--')
plt.plot(plt.gca().get_xlim(), [-noise, -noise], 'k--')
plt.gca().set_ylim(-10,50)
plt.show()

# save to pickle
bn = sys.argv[1].split("/")[-1].split(".")[0]
if sel == "":
    area1, area2 = "all", "all"
else:
    area1 = int(sel.split("&")[0].split(">")[1])
    area2 = int(sel.split("&")[-1].split("<")[1])
# fout = "avg_waveform_pickles/{0}_{1}_{2}_NTC.pkl".format(bn,area1,area2)
fout = "avg_waveform_pickles/{0}_{1}_{2}.pkl".format(bn,area1,area2)
pickle.dump({"v":voltages, "t":time, "n":noise}, open(fout, 'wb'))

# save to root file
# fout = r.TFile("avg_waveforms.root","UPDATE")
# fout.mkdir(sys.argv[1].split(".")[0])
# fout.cd(sys.argv[1].split(".")[0])
# h = r.TH1D(sel, ";time [ns]", voltages.size, 0, time[-1]+time[-1]/(voltages.size-1))
# for i in range(voltages.size):
#     h.SetBinContent(i+1, voltages[i])
# h.Write()
# fout.Close()
