import numpy as np
import matplotlib.pyplot as plt
import ROOT as r
r.gROOT.SetBatch()
def extrapolate(dataset,order):
    xsForward = np.loadtxt("external/crossSecForward.csv",delimiter=",")
    xsCentral = np.loadtxt("external/crossSecCentral.csv",delimiter=",")*(1./(4*3.141*33*33))
    for point in dataset:
        xsF = np.interp(point[0],xsForward[:,0],xsForward[:,1])/1E6
        xsC = np.interp(point[0],xsCentral[:,0],xsCentral[:,1])*(1./(4*3.141*33*33))
        print(xsC,xsF)
        #Size difference between full and specialised (16 bars of 5x5)
        sizeRatio = 1/250.#(1./0.16)*(3000./200.)
        #Ratio in lowest charge scintillator can observe (<N LaBe>/<N plastic>^0.5)
        lowestChargeRatio = 1#((73*100*5.08)/(10.*100.*1.03))**0.5
        lowestCharge = 0.003
        #Dummy variable for number of events needed to set limit (no impact on result)
        nEvRecoOrig = 1
        #Total events is (number of events reconstructed)/(prob to reco each event). The prob is given by (1-exp(-<N>)^4), assuming <N>=1 for Q=0.001, and <N> ~ Q^2
        nEvTotalOrig = nEvRecoOrig/(1-np.exp(-(point[1]/lowestCharge)**(4+order)))
        #Total events through new detector at same mass,charge point (divide by size ratio)
        nEvTotalNew = nEvTotalOrig/sizeRatio
        #Reconstructed number of events through new detector is total number of events * prob to reco each event. The prob is given by (1-exp(-<N>)^4), assuming <N>=1 for Q=lowestCharge/charge ratio, and <N> ~ Q^2
        nEvRecoNew = nEvTotalNew*(1-np.exp(-(point[1]*lowestChargeRatio/lowestCharge)**(4+order)))
        #New limit is where we would expect to see one event
        #If start above new lowest charge for eff reco
        if point[1] > lowestCharge/lowestChargeRatio:
            #scales as nEv^2 above limit
            ratioLim = (nEvRecoNew/nEvRecoOrig)**0.5
            newQ = point[1]/ratioLim
            #if the new charge is below the lowest charge for eff reco then need to scale by 1/10 below this
            if newQ < lowestCharge/lowestChargeRatio:
                #find number of events at lowest eff charge
                nEvAtChargeLim = nEvRecoNew*((lowestCharge/lowestChargeRatio)/point[1])**0.5
                #now extend by 1/10 below this
                newQ = (lowestCharge/lowestChargeRatio)/((nEvAtChargeLim/nEvRecoOrig)**(1./(2+order*2)))
        elif point[1] < lowestCharge/lowestChargeRatio:
            #if start below lowest charge for eff reco need to scale by 1/10
            newQ = point[1]/((nEvRecoNew/nEvRecoOrig)**(1./(2+order*2)))
        point[1] = newQ
    return dataset

fig = plt.figure()
iFile = "./limitsMQMC_V5.root"
datasets = {}
for datasetName in ["ArgoNeut","SK","MilliQ","milliQan","CMS","Collider","SENSEI","milliQanRun3Final","BEBC"]:
    if  datasetName == "FORMOSA_dem_test":
        dataset = np.loadtxt("external/milliQanRun3Bar.csv",delimiter=",")
        dataset = extrapolate(dataset,4)
    elif  datasetName == "FORMOSA_crystal1003layer_test":
        dataset = np.loadtxt("external/FORMOSA_nominal3layer.csv",delimiter=",")
        dataset = extrapolate(dataset,3)
    else:
        dataset = np.loadtxt("external/"+datasetName+".csv",delimiter=",")
    if datasetName == "SK":
        plt.loglog(dataset[:,0],dataset[:,1],color="lightsalmon",linewidth=2)
    elif datasetName == "MilliQ":
        plt.loglog(dataset[:,0],dataset[:,1],color="green",linewidth=2)
    elif datasetName == "milliQan":
        plt.loglog(dataset[:,0],dataset[:,1],color="red",linewidth=2)
    elif datasetName == "milliQanRun3Bar":
        plt.loglog(dataset[:,0],dataset[:,1],color="blue",linewidth=2,label="Run 3 Bar Detector")
    elif datasetName == "milliQanRun3Slab":
        plt.loglog(dataset[:,0],dataset[:,1],color="green",linewidth=2,label="Run 3 Slab Detector")
    elif datasetName == "milliQanRun3Final":
        plt.loglog(dataset[:,0],dataset[:,1],color="green",linewidth=2,label="Run 3 Final")
    elif datasetName == "ArgoNeut":
        plt.loglog(dataset[:,0],dataset[:,1],color="mediumpurple",linewidth=2)
    elif datasetName == "FORMOSA_nominal":
        plt.loglog(dataset[:,0],dataset[:,1],color="fuchsia",linewidth=2,label="FORMOSA")
    elif datasetName == "FORMOSA_nominal3layer":
        plt.loglog(dataset[:,0],dataset[:,1],color="goldenrod",linewidth=2,label="FORMOSA (3 layers)")
    elif datasetName == "milliQanHL":
        plt.loglog(dataset[:,0],dataset[:,1],color="blue",linewidth=2,label="milliQan HL-LHC")
    elif datasetName == "FORMOSA_crystal100":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,label="FORMOSA+CeBr3")
    elif datasetName == "FORMOSA_crystal100_test":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,label="FORMOSA+CeBr3")
    elif datasetName == "FORMOSA_crystal100_3layer":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,label="FORMOSA+CeBr3 (3 layer)")
    elif datasetName == "FORMOSA_dem":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,label="FORMOSA demonstrator")
    elif datasetName == "milliQanSR1":
        plt.loglog(dataset[:,0],dataset[:,1],color="blue",linewidth=2,label="Run 3 low charge")
    elif datasetName == "milliQanSR2":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkblue",linewidth=2,label="Run 3 high charge")
    elif datasetName == "BEBC":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,label="BEBC")
    elif datasetName == "SENSEI":
        plt.loglog(dataset[:,0]/1000,dataset[:,1],color="lightblue",linewidth=2,label="SENSEI")
    elif datasetName == "moedalRun3":
        plt.loglog(dataset[:,0],dataset[:,1],color="lightblue",linewidth=2,label="Moedal Run 3")
    else:
        plt.loglog(dataset[:,0],dataset[:,1],color="sienna",linewidth=2)
    datasets[datasetName] = dataset
plt.fill_between(datasets["Collider"][:,0],datasets["Collider"][:,1],1,color="sienna",alpha=0.4)
plt.fill_between(datasets["ArgoNeut"][:,0],datasets["ArgoNeut"][:,1],1,color="mediumpurple",alpha=0.4)
plt.fill_between(datasets["milliQan"][:,0],datasets["milliQan"][:,1],1,color="red",alpha=0.4)
plt.fill_between(datasets["SK"][:,0],datasets["SK"][:,1],1,color="lightsalmon",alpha=0.4)
plt.fill_betweenx(datasets["CMS"][:,1],datasets["CMS"][:,0],200,color="sienna",alpha=0.4)
plt.fill_betweenx(datasets["MilliQ"][:,1],0.01,datasets["MilliQ"][:,0],color="lightgreen",alpha=0.4)

plt.text(4.7,0.11," milliQan\nprototype",fontsize=9,color="red")
plt.text(0.52,0.0125," ArgoNeuT",fontsize=9,color="mediumpurple")
plt.text(0.38,0.007," SuperK",fontsize=9,color="lightsalmon")
plt.text(0.022,0.002,"SLAC MilliQ",fontsize=9)
plt.text(7,0.35,"Colliders",fontsize=11)
plt.text(80,0.38,"CMS",fontsize=11)

plt.legend(frameon=False)
plt.xlim([0.02,200])
plt.xlabel("MCP mass/GeV",fontsize=14)
plt.ylabel("Q/e",fontsize=14 )
plt.ylim([0.001,0.6])
fig.savefig("finalLimit_Run3.pdf",transparent=True)
