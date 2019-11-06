import numpy as np
import matplotlib.pyplot as plt
import ROOT as r
r.gROOT.SetBatch()

fig = plt.figure()
iFile = "/Users/mcitron/llpStudies/darkTime/timeTreePlotting/stats/limitsMQMC_V5.root"
datasets = {}
for datasetName in ["MilliQ","CMB","CMS","Collider"]:
    dataset = np.loadtxt("external/"+datasetName+".csv",delimiter=",")
    plt.loglog(dataset[:,0],dataset[:,1],color="sienna",linewidth=2)
    datasets[datasetName] = dataset
    
plt.fill_between(datasets["Collider"][:,0],datasets["Collider"][:,1],1,color="sienna",alpha=0.4)
plt.fill_betweenx(datasets["CMS"][:,1],datasets["CMS"][:,0],200,color="sienna",alpha=0.4)
plt.fill_betweenx(datasets["CMB"][:,1],0.01,datasets["CMB"][:,0],color="sienna",alpha=0.2)
plt.fill_betweenx(datasets["MilliQ"][:,1],0.01,datasets["MilliQ"][:,0],color="lawngreen",alpha=0.4)

plt.text(0.012,0.003,"SLAC MilliQ",fontsize=12)
plt.text(0.13,0.003,"CMB $\\rm{N}_{\\rm{eff}}$ \n (indirect)",fontsize=12)
plt.text(2,0.4,"Colliders",fontsize=12)
plt.text(80,0.45,"CMS",fontsize=12)

internalInput = r.TFile(iFile)
contour = internalInput.Get("All/All_r1Contour_1")
nPoints = contour.GetN()
internalData = []
x,y = r.Double(),r.Double()
for i in range(nPoints):
    contour.GetPoint(i,x,y)
    internalData.append([10**x,10**y])
internalData = np.array(internalData)
plt.loglog(internalData[:,0],internalData[:,1],linewidth=2,label="95% UL from demonstrator")
plt.legend(frameon=False)
plt.xlim([0.01,200])
plt.ylim([0.001,1])
fig.savefig("testExternal.pdf",transparent=True)
