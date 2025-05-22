import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

def extrapolate(dataset, order):
    xsForward = np.loadtxt("external/crossSecForward.csv", delimiter=",")
    xsCentral = np.loadtxt("external/crossSecCentral.csv", delimiter=",") * (1./(4*3.141*33*33))
    for point in dataset:
        xsF = np.interp(point[0], xsForward[:,0], xsForward[:,1])/1E6
        xsC = np.interp(point[0], xsCentral[:,0], xsCentral[:,1]) * (1./(4*3.141*33*33))
        print(xsC, xsF)
        # Size difference between full and specialised (16 bars of 5x5)
        sizeRatio = 1/250.  # (1./0.16)*(3000./200.)
        # Ratio in lowest charge scintillator can observe (<N LaBe>/<N plastic>^0.5)
        lowestChargeRatio = 1  # ((73*100*5.08)/(10.*100.*1.03))**0.5
        lowestCharge = 0.003
        # Dummy variable for number of events needed to set limit (no impact on result)
        nEvRecoOrig = 1
        # Total events is (number of events reconstructed)/(prob to reco each event). The prob is given by (1-exp(-<N>)^4), assuming <N>=1 for Q=0.001, and <N> ~ Q^2
        nEvTotalOrig = nEvRecoOrig/(1-np.exp(-(point[1]/lowestCharge)**(4+order)))
        # Total events through new detector at same mass,charge point (divide by size ratio)
        nEvTotalNew = nEvTotalOrig/sizeRatio
        # Reconstructed number of events through new detector is total number of events * prob to reco each event. The prob is given by (1-exp(-<N>)^4), assuming <N>=1 for Q=lowestCharge/charge ratio, and <N> ~ Q^2
        nEvRecoNew = nEvTotalNew*(1-np.exp(-(point[1]*lowestChargeRatio/lowestCharge)**(4+order)))
        # New limit is where we would expect to see one event
        # If start above new lowest charge for eff reco
        if point[1] > lowestCharge/lowestChargeRatio:
            # scales as nEv^2 above limit
            ratioLim = (nEvRecoNew/nEvRecoOrig)**0.5
            newQ = point[1]/ratioLim
            # if the new charge is below the lowest charge for eff reco then need to scale by 1/10 below this
            if newQ < lowestCharge/lowestChargeRatio:
                # find number of events at lowest eff charge
                nEvAtChargeLim = nEvRecoNew*((lowestCharge/lowestChargeRatio)/point[1])**0.5
                # now extend by 1/10 below this
                newQ = (lowestCharge/lowestChargeRatio)/((nEvAtChargeLim/nEvRecoOrig)**(1./(2+order*2)))
        elif point[1] < lowestCharge/lowestChargeRatio:
            # if start below lowest charge for eff reco need to scale by 1/10
            newQ = point[1]/((nEvRecoNew/nEvRecoOrig)**(1./(2+order*2)))
        point[1] = newQ
    return dataset

# Create a custom legend handler class to stack the elements
class StackedHandler(matplotlib.legend_handler.HandlerBase):
    def __init__(self, fill_handler, line_handler):
        self.fill_handler = fill_handler
        self.line_handler = line_handler
        super().__init__()
        
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        # Create the filled area first (bottom layer)
        filled_artists = self.fill_handler.create_artists(
            legend, filled_patch, xdescent, ydescent, width, height, fontsize, trans)
        
        # Create the line on top
        line_artists = self.line_handler.create_artists(
            legend, dotted_proxy, xdescent, ydescent, width, height, fontsize, trans)
        
        # Return both, with line artists last so they're drawn on top
        return filled_artists + line_artists

fig = plt.figure()
iFile = "./limitsMQMC_V5.root"
datasets = {}
datasetCM = np.loadtxt("external/ColliderWithMilliQ.csv", delimiter=",")

# Create separate lists for milliQan and other experiment legend entries
milliQan_handles = []
milliQan_labels = []
other_handles = []
other_labels = []

# "milliQanProjHighBkg",
for datasetName in ["MilliQ", "ArgoNeut", "SENSEI", "CMS", "milliQan", "milliQanRun3Fix", "milliQanRun3Exp", "milliQanRun3ExpUp1", "milliQanRun3ExpDown1", "Collider", "BEBC"][1:-1]:
    if datasetName == "FORMOSA_dem_test":
        dataset = np.loadtxt("external/milliQanRun3Bar.csv", delimiter=",")
        dataset = extrapolate(dataset, 4)
    elif datasetName == "FORMOSA_crystal1003layer_test":
        dataset = np.loadtxt("external/FORMOSA_nominal3layer.csv", delimiter=",")
        dataset = extrapolate(dataset, 3)
    else:
        dataset = np.loadtxt("external/"+datasetName+".csv", delimiter=",")
    
    if datasetName == "SK":
        line, = plt.loglog(dataset[:,0], dataset[:,1], color="lightsalmon", linewidth=2)
    elif datasetName == "MilliQ":
        plt.loglog(dataset[:,0], dataset[:,1], color="lightgray", linewidth=2)
    elif datasetName == "milliQan":
        line, = plt.loglog(dataset[:,0], dataset[:,1], color="lightcoral", alpha=0.8, linewidth=2)
        other_handles.append(line)
        other_labels.append("Run 2 milliQan demonstrator 37.5 $\\rm{fb}^{-1}$\n[PRD 102, 032002 (2020)]")
    elif datasetName == "milliQanRun3Bar":
        plt.loglog(dataset[:,0], dataset[:,1], color="blue", alpha=0.2, linewidth=2, label="Run 3 200 $\\rm{fb}^{-1}$ Proj")
    elif datasetName == "milliQanProjHighBkg":
        plt.loglog(dataset[:,0], dataset[:,1], color="red", linestyle="--", alpha=1, linewidth=2, label="Run 3 304 $\\rm{fb}^{-1}$ Proj")
    elif datasetName == "milliQanRun3Slab":
        plt.loglog(dataset[:,0], dataset[:,1], color="gray", linewidth=2, label="Run 3 Slab Proj")
    elif "milliQanRun3Fix" in datasetName:
        line, = plt.loglog(dataset[:,0], dataset[:,1], color="black", linewidth=2, zorder=21)
        milliQan_handles.append(line)
        milliQan_labels.append("Observed")
    elif "milliQanRun3ExpUp1" in datasetName:
        plt.loglog(dataset[:,0], dataset[:,1], color="black", linewidth=0, zorder=21)
    elif "milliQanRun3ExpDown1" in datasetName:
        plt.loglog(dataset[:,0], dataset[:,1], color="black", linewidth=0, zorder=21)
    elif "milliQanRun3Exp" in datasetName:
        # Store this line for the combined legend entry
        dotted_line, = plt.loglog(dataset[:,0], dataset[:,1], color="black", linewidth=2, linestyle=":", zorder=21)
        # No separate legend entry here
    elif datasetName == "SENSEI":
        line, = plt.loglog(dataset[:,0]/1000, dataset[:,1], color="lightskyblue", linewidth=2)
        other_handles.append(line)
        other_labels.append("SENSEI\n[PRL 133, 071801 (2024)]")
    elif datasetName == "BEBC":
        plt.loglog(dataset[:,0], dataset[:,1], color="fuchsia", linewidth=2)
    elif datasetName == "ArgoNeut":
        line, = plt.loglog(dataset[:,0], dataset[:,1], color="steelblue", linewidth=2)
        other_handles.append(line)
        other_labels.append("ArgoNeuT\n[PRL 124, 131801 (2020)]")
    elif datasetName == "FORMOSA_nominal":
        plt.loglog(dataset[:,0], dataset[:,1], color="fuchsia", linewidth=2, label="FORMOSA")
    elif datasetName == "FORMOSA_nominal3layer":
        plt.loglog(dataset[:,0], dataset[:,1], color="goldenrod", linewidth=2, label="FORMOSA (3 layers)")
    elif datasetName == "milliQanHL":
        plt.loglog(dataset[:,0], dataset[:,1], color="blue", linewidth=2, label="milliQan HL-LHC")
    elif datasetName == "FORMOSA_crystal100":
        plt.loglog(dataset[:,0], dataset[:,1], color="darkmagenta", linewidth=2, label="FORMOSA+CeBr3")
    elif datasetName == "FORMOSA_crystal100_test":
        plt.loglog(dataset[:,0], dataset[:,1], color="darkmagenta", linewidth=2, label="FORMOSA+CeBr3")
    elif datasetName == "FORMOSA_crystal100_3layer":
        plt.loglog(dataset[:,0], dataset[:,1], color="darkmagenta", linewidth=2, label="FORMOSA+CeBr3 (3 layer)")
    elif datasetName == "FORMOSA_dem":
        plt.loglog(dataset[:,0], dataset[:,1], color="darkmagenta", linewidth=2, label="FORMOSA demonstrator")
    elif datasetName == "moedalRun3":
        plt.loglog(dataset[:,0], dataset[:,1], color="lightskyblue", linewidth=2, label="Moedal Run 3")
    elif datasetName == "CMS":
        line, = plt.loglog(dataset[:,0], dataset[:,1], color="orange", linewidth=2)
        other_handles.append(line)
        other_labels.append("CMS FCP 138 $\\rm{fb}^{-1}$\n[PRL 134, 131802 (2025)]")
    else:
        plt.loglog(dataset[:,0], dataset[:,1], color="gray", linewidth=2, zorder=22)
    datasets[datasetName] = dataset

plt.fill_between(datasets["Collider"][:,0], datasets["Collider"][:,1], 1, color="gray", alpha=0.4)
if "ArgoNeut" in datasets:
    AN_interpUp = np.interp(datasets["ArgoNeut"][:,0], datasets["Collider"][:,0], datasets["Collider"][:,1])
    plt.fill_between(datasets["ArgoNeut"][:,0], datasets["ArgoNeut"][:,1], AN_interpUp, color="steelblue", alpha=0.4)

milliQanForShade = np.loadtxt("external/milliQanForShade.csv", delimiter=",")
milliQanForShadeUp = np.interp(milliQanForShade[:,0], datasets["ArgoNeut"][:,0], datasets["ArgoNeut"][:,1])
plt.fill_between(milliQanForShade[:,0], milliQanForShade[:,1]*0.99, milliQanForShadeUp, color="lightcoral", alpha=0.4)

SENSEI_interpUp = np.interp(datasets["SENSEI"][:,0]/1000, datasets["Collider"][:,0], datasets["Collider"][:,1])
SENSEI_interpUp2 = np.interp(datasets["SENSEI"][:,0]/1000, datasetCM[:,0], datasetCM[:,1])
SENSEI_interpUp3 = np.interp(datasets["SENSEI"][:,1], datasetCM[:,1], datasetCM[:,0])
SENSEI_interpUp2 = np.interp(datasets["SENSEI"][:,0]/1000, datasets["ArgoNeut"][:,0], datasets["ArgoNeut"][:,1])
if "SENSEI" in datasets:
    plt.fill_between(datasets["SENSEI"][:,0]/1000, datasets["SENSEI"][:,1], SENSEI_interpUp2, color="lightskyblue", alpha=0.4)

if "BEBC" in datasets:
    plt.fill_between(datasets["BEBC"][:,0], datasets["BEBC"][:,1], 1, color="fuchsia", alpha=0.4)
if "SK" in datasets:
    plt.fill_between(datasets["SK"][:,0], datasets["SK"][:,1], 1, color="lightsalmon", alpha=0.4)
plt.fill_betweenx(datasets["CMS"][:,1], datasets["CMS"][:,0], 200, color="orange", alpha=0.4)
if "MilliQ" in datasets:
    plt.fill_betweenx(datasets["MilliQ"][:,1], 0.01, datasets["MilliQ"][:,0], color="lightgray", alpha=0.4)

# Create the filled polygon for Expected ±1σ
polygon = np.concatenate([datasets["milliQanRun3ExpUp1"], datasets["milliQanRun3ExpDown1"][::-1]], axis=0)
filled_area = plt.fill(polygon[:, 0], polygon[:, 1], color="lime", zorder=20)

# Create custom legend handles for the Expected ±1σ entry
filled_patch = Patch(facecolor='lime', alpha=0.7, linewidth=0)
dotted_proxy = Line2D([0], [0], color='black', linestyle=':', linewidth=2)

# Add the Expected ±1σ to the milliQan legend handles and labels
milliQan_handles.append((filled_patch, dotted_proxy))
milliQan_labels.append("Expected $\pm 1 \sigma$")

# Create the handler map for the stacked legend elements
handler_map = {tuple: StackedHandler(
    matplotlib.legend_handler.HandlerPatch(),
    matplotlib.legend_handler.HandlerLine2D()
)}

# Create two separate legends
# First legend for milliQan results
first_legend = plt.legend(milliQan_handles, milliQan_labels, 
                          frameon=False, fontsize=12,loc=(0.46,0.02),
                          handler_map=handler_map, title="Run 3 milliQan bar detector",title_fontsize=12)

first_legend._legend_box.align = "left"
# Add the first legend manually to the axes
plt.gca().add_artist(first_legend)

# Second legend for other experiments
leg = plt.legend(other_handles, other_labels,
           frameon=False, fontsize=8,loc=(0.47,0.25))
for text in leg.get_texts():
    plt.setp(text, color = 'black',alpha=0.8)
           # title="Past constraints",title_fontsize=8)

plt.xlim([0.1, 200])
plt.xlabel("mCP mass (GeV)", fontsize=14, loc="right")
plt.ylabel("Q/e", fontsize=14, loc="top")
plt.ylim([0.0005, 0.6])
plt.text(0.088, 1.05, "$\\bf{milliQan}$", horizontalalignment='center',
     verticalalignment='center', transform=plt.gca().transAxes, fontsize=14)
plt.text(0.81, 1.05, "$124.7\ \\rm{fb}^{-1}$ (13.6 TeV)", horizontalalignment='center',
     verticalalignment='center', transform=plt.gca().transAxes, fontsize=14)
plt.text(5.5,0.45,"Previous constraints",color="black",fontsize=9,zorder=30,alpha=0.5)
fig.savefig("finalLimit_Run3.pdf", transparent=True)
fig.savefig("finalLimit_Run3.png")
