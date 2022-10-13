import sys
import glob
import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import ROOT as r

chan = int(sys.argv[1])
TAG = sys.argv[2]

errc = 0.03
errs = 0.06

runsc = [2620,2617,2616,2614,2611,2609]
#runsc = [584, 617, 663, 672, 674]
#runss = [2579,2578,2577,2576,2575,2574,2573,2753,2755,2757,2759]
runss = [2576,2575,2574,2573,2753,2755,2757,2759]
#runss = [700]
bonus_spe = [700]
if chan in [5,22]:
    runsc = [2609,2608,2604,2599,2588]
#    runss = [724,714]
    bonus_spe = [724,714]
if chan in [9,17,24,25]:
    runsc = [2614,2611,2609,2608,2604,2599]
#    runss = [723,716]
    bonus_spe = [723,716]
if chan in [8]:    
    bonus_spe = []

bonus_spe = []

HVs_c = []
areas_c = []
HVs_s = []
areas_s = []
rates_s = []
bonus_HVs = []
bonus_areas = []
gc = r.TGraphErrors()
gs = r.TGraphErrors()
for run in runsc+runss+bonus_spe:
    fname = glob.glob("{0}/tables/table_run{1}_*T.csv".format(TAG, run))[0]
    g = gc
    if run in runss:
        g = gs
    with open(fname) as fid:
        for line in fid:
            sp = line.strip().split(",")
            if chan == int(sp[1]):
                HV = int(sp[2])
                area = float(sp[3])
                rate = float(sp[-1])
                N = g.GetN()                
                if run not in bonus_spe:
                    g.SetPoint(N, np.log(HV), np.log(area))
                    relerr = errc if run in runsc else errs
                    g.SetPointError(N, 0, 0.5*(np.log((1+relerr)*area)-np.log((1-relerr)*area)))
                if run in runsc:
                    HVs_c.append(HV)
                    areas_c.append(area)
                elif run in runss:
                    HVs_s.append(HV)
                    areas_s.append(area)
                    rates_s.append(rate)
                else:
                    bonus_HVs.append(HV)
                    bonus_areas.append(area)
                break

HVs_c = np.array(HVs_c)
areas_c = np.array(areas_c)
HVs_s = np.array(HVs_s)
areas_s = np.array(areas_s)
bonus_HVs = np.array(bonus_HVs)
bonus_areas = np.array(bonus_areas)

gc.Print("all")
fitc = r.TF1("fitc", "[0] + [1]*x", np.log(600), np.log(1600))
gc.Fit(fitc, "R EX0 E", "goff")

print ""
gs.Print("all")
fits = r.TF1("fits", "[0] + [1]*x", np.log(600), np.log(1600))
fitsfix = r.TF1("fitsfix", "[0] + [1]*x", np.log(600), np.log(1600))
fitsfix.FixParameter(1, fitc.GetParameter(1))
gs.Fit(fits, "R EX0", "goff")
gs.Fit(fitsfix, "R EX0", "goff")

m_c = fitc.GetParameter(1)
N_c = HVs_c.size
la = np.log(areas_c)
lh = np.log(HVs_c)
dm_c = np.sqrt(np.sum((N_c*lh-np.sum(lh))**2*errc**2))
#dm_c = N_c*np.sum(la*lh) - np.sum(lh)*np.sum(la)
dm_c /= N_c*np.sum(lh**2)-np.sum(lh)**2
print dm_c

m_s = fits.GetParameter(1)
N_s = HVs_s.size
la = np.log(areas_s)
lh = np.log(HVs_s)
dm_s = np.sqrt(np.sum((N_s*lh-np.sum(lh))**2*errs**2))
#dm_s = N_s*np.sum(la*lh) - np.sum(lh)*np.sum(la)
dm_s /= N_s*np.sum(lh**2)-np.sum(lh)**2
print dm_s

plt.figure(figsize=(14,6))
ax = plt.subplot(121)
plt.errorbar(HVs_c, areas_c, yerr=errc*areas_c, fmt='ro')
finex = np.linspace(np.amin(HVs_c)-20, np.amax(HVs_c)+20, 301)
finey = np.exp(m_c*np.log(finex) + fitc.GetParameter(0))
plt.plot(finex, finey, 'b-')
plt.text(0.05, 0.92, "Cosmics", transform=ax.transAxes, fontsize='large', weight="bold")
plt.text(0.05, 0.85, "slope = {0:.2f} $\pm$ {1:.2f}".format(m_c, dm_c), transform=ax.transAxes, fontsize='large')
plt.xlabel("HV (V)")
plt.ylabel("pulse area (pVs)")

ax = plt.subplot(122)
plt.errorbar(HVs_s, areas_s, yerr=errs*areas_s, fmt='ro')
#plt.errorbar(HVs_s[7:], areas_s[7:], yerr=errs*areas_s[7:], fmt='go')
plt.plot(bonus_HVs, bonus_areas, '*', color='gold', ms=20.0) 
finex = np.linspace(np.amin(HVs_s)-20, np.amax(HVs_s)+20, 301)
finey = np.exp(m_s*np.log(finex) + fits.GetParameter(0))
fineyfix = np.exp(m_c*np.log(finex) + fitsfix.GetParameter(0))
plt.plot(finex, finey, 'b-')
plt.plot(finex, fineyfix, 'b--')
plt.text(0.05, 0.92, "SPEs", transform=ax.transAxes, fontsize='large', weight="bold")
plt.text(0.05, 0.85, "slope = {0:.2f} $\pm$ {1:.2f}".format(m_s, dm_s), transform=ax.transAxes, fontsize='large')
ratio = m_s / m_c
err = ratio * np.sqrt((dm_s/m_s)**2+(dm_c/m_c)**2)
plt.text(0.05, 0.78, "Slope ratio = {0:.2f} $\pm$ {1:.2f}".format(ratio, err), transform=ax.transAxes, fontsize='large', weight="bold", color='b')
plt.xlabel("HV (V)")
plt.ylabel("pulse area (pVs)")


plt.savefig(TAG+"/slopes/plots/ch{0}.pdf".format(chan), bbox_inches="tight")
plt.savefig(TAG+"/slopes/plots/ch{0}.png".format(chan), bbox_inches="tight")

plt.figure()
plt.plot(HVs_s, rates_s, 'o')
plt.gca().set_xlim(np.amin(HVs_s)-20, np.amax(HVs_s)+20)
plt.gca().set_ylim(0,1)
plt.xlabel("HV")
plt.ylabel("mean # afterpulses")
plt.savefig(TAG+"/slopes/plots/rates/ch{0}.pdf".format(chan))
plt.savefig(TAG+"/slopes/plots/rates/ch{0}.png".format(chan))

fid = open("tmp/test.txt", 'a')
for HV, area in zip(bonus_HVs, bonus_areas):
    predarea = np.exp(m_s*np.log(HV) + fits.GetParameter(0))
    fid.write("{0},{1},{2},{3}\n".format(chan,HV, area, predarea))
fid.close()
