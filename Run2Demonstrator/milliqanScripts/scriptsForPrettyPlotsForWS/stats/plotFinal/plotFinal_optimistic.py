import numpy as np
import matplotlib.pyplot as plt
import ROOT as r
r.gROOT.SetBatch()
def extrapolate(dataset,order):
    for point in dataset:
        #Size difference between full and specialised (16 bars of 5x5)
        sizeRatio = 25
        #Ratio in lowest charge scintillator can observe (<N LaBe>/<N plastic>^0.5)
        lowestChargeRatio = ((73*100*5.08)/(10.*100.*1.03))**0.5
        #Dummy variable for number of events needed to set limit (no impact on result)
        nEvRecoOrig = 1
        #Total events is (number of events reconstructed)/(prob to reco each event). The prob is given by (1-exp(-<N>)^4), assuming <N>=1 for Q=0.001, and <N> ~ Q^2
        nEvTotalOrig = nEvRecoOrig/(1-np.exp(-(point[1]/0.001)**(4+order)))
        #Total events through new detector at same mass,charge point (divide by size ratio)
        nEvTotalNew = nEvTotalOrig/sizeRatio
        #Reconstructed number of events through new detector is total number of events * prob to reco each event. The prob is given by (1-exp(-<N>)^4), assuming <N>=1 for Q=0.001/charge ratio, and <N> ~ Q^2
        nEvRecoNew = nEvTotalNew*(1-np.exp(-(point[1]*lowestChargeRatio/0.001)**(4+order)))
        #New limit is where we would expect to see one event
        #If start above new lowest charge for eff reco
        if point[1] > 0.001/lowestChargeRatio:
            #scales as nEv^2 above limit
            ratioLim = (nEvRecoNew/nEvRecoOrig)**0.5
            newQ = point[1]/ratioLim
            #if the new charge is below the lowest charge for eff reco then need to scale by 1/10 below this
            if newQ < 0.001/lowestChargeRatio:
                #find number of events at lowest eff charge
                nEvAtChargeLim = nEvRecoNew*((0.001/lowestChargeRatio)/point[1])**0.5
                #now extend by 1/10 below this
                newQ = (0.001/lowestChargeRatio)/((nEvAtChargeLim/nEvRecoOrig)**(1./(2+order*2)))
        elif point[1] < 0.001/lowestChargeRatio:
            #if start below lowest charge for eff reco need to scale by 1/10
            newQ = point[1]/((nEvRecoNew/nEvRecoOrig)**(1./(2+order*2)))
        point[1] = newQ
    return dataset

fig = plt.figure()
iFile = "./limitsMQMC_V5.root"
datasets = {}
# for datasetName in ["directDetection","ArgoNeut","SK","MilliQ","milliQanRun3Both","milliQan","CMS","Collider","SUBMET"][:-1]:
"FORMOSA_crystal100"
for datasetName in ["directDetection","ArgoNeut","SK","MilliQ","milliQan","milliQanRun3Both","FORMOSA_nominal","CMS","Collider","SENSEI","luminiQPlastic","LongQuestLarge","SHIP"][:-1]:
    if  datasetName == "FORMOSA_crystal100_test":
        dataset = np.loadtxt("external/FORMOSA_nominal.csv",delimiter=",")
        dataset = extrapolate(dataset,4)
    elif  datasetName == "FORMOSA_crystal1003layer_test":
        dataset = np.loadtxt("external/FORMOSA_nominal3layer.csv",delimiter=",")
        dataset = extrapolate(dataset,3)
    else:
        dataset = np.loadtxt("external/"+datasetName+".csv",delimiter=",")
    if datasetName == "SK":
        plt.loglog(dataset[:,0],dataset[:,1],color="lightsalmon",linewidth=2)
    elif datasetName == "luminiQ":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkkhaki",linewidth=2,label="LANSCE-mQ")
    elif  "LongQuestSmall" in datasetName:
        plt.loglog(dataset[:,0],dataset[:,1],color="orchid",linewidth=2,label="FLAME demonstrator")
    elif  "LongQuest" in datasetName:
        plt.loglog(dataset[:,0],dataset[:,1],color="purple",linewidth=2,label="FLAME FNAL")
    elif datasetName == "luminiQPlastic":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkkhaki",linewidth=2,label="FLAME LANL")
    elif datasetName == "MilliQ":
        plt.loglog(dataset[:,0],dataset[:,1],color="green",linewidth=2)
    elif datasetName == "SHIP":
        plt.loglog(dataset[:,0],dataset[:,1],color="darksalmon",linewidth=2,label="SHIP")
    elif datasetName == "milliQan":
        plt.loglog(dataset[:,0],dataset[:,1],color="red",linewidth=2)
    elif datasetName == "milliQanRun3Both":
        plt.loglog(dataset[:,0],dataset[:,1],color="blue",linewidth=2,alpha=0.5,label="Run 3 milliQan")
    elif datasetName == "milliQanRun3Slab":
        plt.loglog(dataset[:,0],dataset[:,1],color="green",linewidth=2,label="Run 3 Slab Detector")
    elif datasetName == "ArgoNeut":
        plt.loglog(dataset[:,0],dataset[:,1],color="mediumpurple",linewidth=2)
    elif datasetName == "SENSEI":
        plt.loglog(dataset[:,0]/1000,dataset[:,1],color="lightblue",linewidth=2)
    elif datasetName == "FORMOSA_nominal":
        plt.loglog(dataset[:,0],dataset[:,1],color="fuchsia",linewidth=2,label="FORMOSA")
    elif datasetName == "FORMOSA_nominal3layer":
        plt.loglog(dataset[:,0],dataset[:,1],color="lightcoral",linewidth=2,label="FORMOSA3")
    elif datasetName == "milliQanHL":
        plt.loglog(dataset[:,0],dataset[:,1],color="blue",linewidth=2,label="HL-LHC milliQan")
    elif datasetName == "FORMOSA_crystal100":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkslateblue",linewidth=2,label="FORMOSA+CeBr3")
    elif datasetName == "FORMOSA_crystal20":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkslateblue",linewidth=2,label="FORMOSA+CeBr3 20")
    elif datasetName == "FORMOSA_crystal100_test":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,label="FORMOSA+CeBr3")
    elif datasetName == "FORMOSA_crystal100_3layer":
        plt.loglog(dataset[:,0],dataset[:,1],color="firebrick",linewidth=2,label="FORMOSA3+CeBr3")
    elif datasetName == "FORMOSA_crystal1003layer_test":
        plt.loglog(dataset[:,0],dataset[:,1],color="red",linewidth=2,label="FORMOSA3+CeBr3 test")
    elif datasetName == "FORMOSA_dem":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,alpha=0.5,label="FORMOSA demonstrator")
    elif datasetName == "directDetection":
        continue
        plt.loglog(dataset[:,0],dataset[:,1],color="darkgray",linewidth=2,linestyle="--",alpha=0.8)
    elif datasetName == "SUBMET":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkcyan",linewidth=2,label="SUBMET")
    else:
        plt.loglog(dataset[:,0],dataset[:,1],color="sienna",linewidth=2)
    datasets[datasetName] = dataset

plt.fill_between(datasets["Collider"][:,0],datasets["Collider"][:,1],1,color="sienna",alpha=0.4)
plt.fill_between(datasets["ArgoNeut"][:,0],datasets["ArgoNeut"][:,1],1,color="mediumpurple",alpha=0.4)
if "SENSEI" in datasets:
    plt.fill_between(datasets["SENSEI"][:,0]/1000,datasets["SENSEI"][:,1],1,color="lightblue",alpha=0.4)
# plt.fill_between(datasets["directDetection"][:,0],datasets["directDetection"][:,1],1E-9,color="gray",alpha=0.1)
plt.fill_between(datasets["milliQan"][:,0],datasets["milliQan"][:,1],1,color="red",alpha=0.4)
plt.fill_between(datasets["SK"][:,0],datasets["SK"][:,1],1,color="lightsalmon",alpha=0.4)
plt.fill_betweenx(datasets["CMS"][:,1],datasets["CMS"][:,0],200,color="sienna",alpha=0.4)
plt.fill_betweenx(datasets["MilliQ"][:,1],0.01,datasets["MilliQ"][:,0],color="lightgreen",alpha=0.4)

# plt.text(4.7,0.11," milliQan\nprototype",fontsize=9,color="red")
# plt.text(0.12,0.0018,"milliQan Run 3",fontsize=9,color="blue",alpha=0.5)
# plt.text(8,0.006,"   FORMOSA\ndemonstrator",fontsize=9,color="darkmagenta",alpha=0.5)
# plt.text(20,0.0008,"Direct DM detection",fontsize=9,color="gray",alpha=0.5,rotation=20)
# plt.text(0.43,0.012," ArgoNeuT",fontsize=9,color="mediumpurple")
# plt.text(0.38,0.007," SuperK",fontsize=9,color="lightsalmon")
plt.text(0.022,0.001,"SLAC MilliQ",fontsize=9)
plt.text(7,0.35,"Colliders",fontsize=11)
plt.text(80,0.38,"CMS",fontsize=11)
plt.xlabel("MCP mass/GeV",fontsize=14)
plt.ylabel("Q/e",fontsize=14 )

plt.legend(frameon=False)
plt.xlim([0.021,200])
plt.ylim([0.00006,0.6])
fig.savefig("finalLimit.pdf",transparent=True)
