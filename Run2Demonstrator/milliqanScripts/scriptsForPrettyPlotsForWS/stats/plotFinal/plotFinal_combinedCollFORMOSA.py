import numpy as np
import matplotlib
import matplotlib.pyplot as plt
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
datasetA = np.loadtxt("external/ArgoNeuTWithMQ.csv",delimiter=",")
#"milliQanProjHighBkg",
# for datasetName in ["MilliQ","ArgoNeut","SENSEI","CMS","milliQan","milliQanRun3Both","ColliderWithMilliQ","FORMOSA_dem",]:
for datasetName in ["MilliQ","ArgoNeut","SENSEI","CMS","milliQan","milliQanRun3Both","ColliderWithMilliQ","FORMOSA_SND","FORMOSA_SND_HLLHC","FORMOSA_nominal"][1:]:
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
        plt.loglog(dataset[:,0],dataset[:,1],color="lightgray",linewidth=2)
    elif datasetName == "milliQan":
        plt.loglog(dataset[:,0],dataset[:,1],color="lightcoral",alpha=0.8,linewidth=2)
    elif datasetName == "milliQanRun3Both":
        plt.loglog(dataset[:,0],dataset[:,1],color="blue",linewidth=2,alpha=0.5,label="Run 3 milliQan")
    elif datasetName == "milliQanRun3Bar":
        plt.loglog(dataset[:,0],dataset[:,1],color="blue",alpha=0.2,linewidth=2,label="Run 3 200 $\\rm{fb}^{-1}$ projection")
    elif datasetName == "milliQanProjRealBkg":
        plt.loglog(dataset[:,0],dataset[:,1],color="red",linestyle="--",alpha=1,linewidth=2,label="Run 3 bar detector 304 $\\rm{fb}^{-1}$")
    elif datasetName == "milliQanProjLowBkg":
        plt.loglog(dataset[:,0],dataset[:,1],color="red",linestyle=":",alpha=1,linewidth=2,label="Run 3 bar detector 304 $\\rm{fb}^{-1}$ optimistic")
    elif datasetName == "milliQanRun3Slab":
        plt.loglog(dataset[:,0],dataset[:,1],color="green",linewidth=2,linestyle="--",label="Run 3 slab detector 200 $\\rm{fb}^{-1}$ projection\nPRD 104 032002 (2021)")
    elif  "milliQanRun3Fix" in datasetName:
        plt.loglog(dataset[:,0],dataset[:,1],color="red",linewidth=2,label="Run 3 milliQan bar detector 124.7 $\\rm{fb}^{-1}$")
    elif datasetName == "SENSEI":
        plt.loglog(dataset[:,0]/1000,dataset[:,1],color="lightskyblue",linewidth=2)
    elif datasetName == "BEBC":
        plt.loglog(dataset[:,0],dataset[:,1],color="fuchsia",linewidth=2)
    elif datasetName == "ArgoNeut":
        plt.loglog(dataset[:,0],dataset[:,1],color="steelblue",linewidth=2)
    elif datasetName == "FORMOSA_nominal":
        plt.loglog(dataset[:,0],dataset[:,1],color="fuchsia",linewidth=2,label="FORMOSA at the FPF (2000/fb)")
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
    elif datasetName == "FORMOSA_SND":
        plt.loglog(dataset[:,0],dataset[:,1],color="mediumvioletred",linewidth=2,label="FORMOSA at SND (200/fb)")
    elif datasetName == "FORMOSA_SND_HLLHC":
        plt.loglog(dataset[:,0],dataset[:,1],color="darkmagenta",linewidth=2,label="FORMOSA at SND (3000/fb)")
    elif datasetName == "moedalRun3":
        plt.loglog(dataset[:,0],dataset[:,1],color="lightskyblue",linewidth=2,label="Moedal Run 3")
    elif datasetName == "CMS":
        plt.loglog(dataset[:,0],dataset[:,1],color="orange",linewidth=2)
    else:
        plt.loglog(dataset[:,0],dataset[:,1],color="gray",linewidth=2)
    datasets[datasetName] = dataset
plt.fill_between(datasets["ColliderWithMilliQ"][:,0],datasets["ColliderWithMilliQ"][:,1],1,color="gray",alpha=0.4)
if "ArgoNeut" in datasets:
    AN_interpUp = np.interp(datasets["ArgoNeut"][:,0],datasets["ColliderWithMilliQ"][:,0],datasets["ColliderWithMilliQ"][:,1])
    plt.fill_between(datasets["ArgoNeut"][:,0],datasets["ArgoNeut"][:,1],AN_interpUp,color="steelblue",alpha=0.4)
milliQanForShade = np.loadtxt("external/milliQanForShade.csv",delimiter=",")
milliQanForShadeUp = np.interp(milliQanForShade[:,0],datasets["ArgoNeut"][:,0],datasets["ArgoNeut"][:,1])
plt.fill_between(milliQanForShade[:,0],milliQanForShade[:,1]*0.99,milliQanForShadeUp,color="lightcoral",alpha=0.4)
SENSEI_interpUp2 = np.interp(datasets["SENSEI"][:,0]/1000,datasets["ColliderWithMilliQ"][:,0],datasets["ColliderWithMilliQ"][:,1])
if "SENSEI" in datasets:
    plt.fill_between(datasets["SENSEI"][:,0]/1000,datasets["SENSEI"][:,1],SENSEI_interpUp2,color="lightskyblue",alpha=0.4)
    # plt.fill_betweenx(datasets["SENSEI"][:,1],SENSEI_interpUp3,datasets["SENSEI"][:,0]/1000,color="sienna",alpha=0.4)
if "BEBC" in datasets:
    plt.fill_between(datasets["BEBC"][:,0],datasets["BEBC"][:,1],1,color="fuchsia",alpha=0.4)
if "SK" in datasets:
    plt.fill_between(datasets["SK"][:,0],datasets["SK"][:,1],1,color="lightsalmon",alpha=0.4)
plt.fill_betweenx(datasets["CMS"][:,1],datasets["CMS"][:,0],200,color="orange",alpha=0.4)
if "MilliQ" in datasets:
    plt.fill_betweenx(datasets["MilliQ"][:,1],0.01,datasets["MilliQ"][:,0],color="lightgray",alpha=0.4)

# plt.text(4.7,0.11," milliQan\nprototype",fontsize=9,color="red")
# plt.text(0.52,0.0125," ArgoNeuT",fontsize=9,color="mediumpurple")
# plt.text(0.38,0.007," SuperK",fontsize=9,color="lightsalmon")
# plt.text(0.022,0.002,"SLAC MilliQ",fontsize=9)
  
# plt.text(14,0.35,"Colliders",fontsize=11) 
# plt.text(50,0.32,"CMS FCP\nEXO 24 006",fontsize=11)
# plt.text(0.105,0.0015,"SENSEI",fontsize=11)
# plt.text(50,0.36,"PhysRevLett.134.131802",fontsize=4)

plt.legend(frameon=False,loc="lower right",fontsize=9)
plt.xlim([0.02,200])
plt.xlabel("MCP mass (GeV)",fontsize=14,loc="right")
plt.ylabel("Q/e",fontsize=14,loc="top" )
plt.ylim([0.00008,0.6])
plt.text(0.205,1.05, "$\\bf{FORMOSA}$ $\it{Simulation}$", horizontalalignment='center',
     verticalalignment='center',transform=plt.gca().transAxes,fontsize=14)
plt.text(0.81,1.05, "$2000\ \\rm{fb}^{-1}$ (13.6 TeV)", horizontalalignment='center',
     verticalalignment='center',transform=plt.gca().transAxes,fontsize=14)
fig.savefig("finalLimit_FORMOSARun3.pdf",transparent=True)
