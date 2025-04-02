import uproot
import awkward as ak
import numpy as np
import sys
import os
from tabulate import tabulate

input_path = sys.argv[1]
file = uproot.open(input_path + "flattened_output.root")
tree = file["t;1"]
branches = tree.arrays(["pmt_chan","pmt_row","pmt_column","pmt_layer","pmt_type","pmt_time","pmt_nPE"])
weightBranch = tree.arrays(["eventWeight"])
weights = weightBranch.eventWeight
nevents = len(branches)
mass = input_path.split("/")[7].split("_")[1].replace("p",".")
charge = input_path.split("/")[8].split("_")[1].replace("p",".")
hits = ak.zip({
	"layer":branches["pmt_layer"],
	"row":branches["pmt_row"],
	"column":branches["pmt_column"],
	"chan":branches["pmt_chan"],
	"type":branches["pmt_type"],
	"time":branches["pmt_time"],
	"nPE":branches["pmt_nPE"],
	}
)

acceptance = 0.04

non_empty_mask = ak.num(hits.layer, axis=1) > 0
non_empty_hits = hits[non_empty_mask]
n_non_empty = len(non_empty_hits)
nonEmptyEff = round(n_non_empty / nevents,4) if nevents > 0 else 0
#Require at least one bar hit in each layer
l0_mask = (non_empty_hits["layer"] == 0) & (non_empty_hits["type"] == 0)
l1_mask = (non_empty_hits["layer"] == 1) & (non_empty_hits["type"] == 0)
l2_mask = (non_empty_hits["layer"] == 2) & (non_empty_hits["type"] == 0)
l3_mask = (non_empty_hits["layer"] == 3) & (non_empty_hits["type"] == 0)
fourLayersHitMask = ak.any(l0_mask,axis=1) & ak.any(l1_mask,axis=1) & ak.any(l2_mask,axis=1) & ak.any(l3_mask,axis=1) 
fourLayersHit = non_empty_hits[fourLayersHitMask]
n_4LHits = len(fourLayersHit)
fourLayersEff = round(n_4LHits/n_non_empty,4) if n_non_empty > 0 else 0

#Require exactly one bar hit in each layer
l0_mask = (fourLayersHit.layer == 0) * (fourLayersHit["type"] == 0)
l1_mask = (fourLayersHit.layer == 1) * (fourLayersHit["type"] == 0)
l2_mask = (fourLayersHit.layer == 2) * (fourLayersHit["type"] == 0)
l3_mask = (fourLayersHit.layer == 3) * (fourLayersHit["type"] == 0)
inl0 = ak.num(l0_mask[l0_mask],axis=1) == 1
inl1 = ak.num(l1_mask[l1_mask],axis=1) == 1
inl2 = ak.num(l2_mask[l2_mask],axis=1) == 1
inl3 = ak.num(l3_mask[l3_mask],axis=1) == 1
one_in_each_layer_mask = inl0 * inl1 * inl2 * inl3
oneInEachLayer = fourLayersHit[one_in_each_layer_mask]
n_oneInEachLayer = len(oneInEachLayer)
oneInEachLayerEff = round(n_oneInEachLayer / n_4LHits,4) if n_4LHits > 0 else 0

#Require they be in a straight line
bars = oneInEachLayer["type"]==0
same_cols = ak.all(oneInEachLayer.column[bars] == oneInEachLayer.column[bars][:,0],axis=1)
same_rows = ak.all(oneInEachLayer.row[bars] == oneInEachLayer.row[bars][:,0],axis=1)
in_a_line = same_rows * same_cols
inLineHits = oneInEachLayer[in_a_line]
n_inLine = len(inLineHits)
inLineEff = round(n_inLine / n_oneInEachLayer,4) if n_oneInEachLayer > 0 else 0


#Remove side panel hits
is_panel = inLineHits["type"] == 2
panel_hit = ak.any(inLineHits["nPE"][is_panel] > 0, axis=1)#.5,axis=1)
panellessHits = inLineHits[~panel_hit]
n_panelless = len(panellessHits)
panellessEff = round(n_panelless / n_inLine,4) if n_inLine > 0 else 0

#Remove hits in front/back slabs
is_slab = panellessHits["type"] == 1
#slab_hit = ak.any(panellessHits["nPE"][is_slab] > 0,axis=1)
slab_hit = ak.any(is_slab,axis=1)
slablessHits = panellessHits[~slab_hit]
n_slabless = len(slablessHits)
slablessEff = round(n_slabless / n_panelless,4) if n_panelless > 0 else 0

#Cut on ratio of max/min bar NPE
max_nPE = ak.max(slablessHits["nPE"][slablessHits["type"]==0],axis=1)
min_nPE = ak.min(slablessHits["nPE"][slablessHits["type"]==0],axis=1)
nPE_ratio = max_nPE/min_nPE
nPE_cut = 20
goodRatioHits = slablessHits[nPE_ratio < nPE_cut]
n_goodRatio = len(goodRatioHits)
ratioEff = round(n_goodRatio / n_slabless,4) if n_slabless > 0 else 0

#Cut on max - min bar time
max_time = ak.max(goodRatioHits["time"][goodRatioHits["type"] == 0],axis=1)
min_time = ak.min(goodRatioHits["time"][goodRatioHits["type"] == 0],axis=1)
dt = max_time - min_time
dt_cut = 20
signalRegionHits = goodRatioHits[dt < dt_cut]
n_signal_events = len(signalRegionHits)
dtEff = round(n_signal_events / n_goodRatio,4) if n_goodRatio > 0 else 0


signalWeights = weights[non_empty_mask][fourLayersHitMask][one_in_each_layer_mask][in_a_line][~panel_hit][~slab_hit][nPE_ratio < nPE_cut][dt < dt_cut]
max_weight = ak.max(signalWeights)
signal_yield = round(ak.sum(signalWeights,axis=0) * float(charge)**2,4)

"""
print("=====Efficiencies=====")
print(f"Any hit: {n_non_empty} / {nevents} = {nonEmptyEff}")
print(f"One hit in each layer: {n_4LHits} / {n_non_empty} = {fourLayEff} ")
print(f"In a straight line: {n_inLine} / {n_4LHits} = {inLineEff} ")
print(f"No side panel hits (NPE < 0.5): {n_panelless} / {n_inLine} = {panellessEff} ")
print(f"NPE < 50 in front/back slabs: {n_slabless} / {n_panelless} = {slablessEff} ")
print(f"max/min NPE < 10: {n_goodRatio} / {n_slabless} = {ratioEff} ")
print(f"max - min time < 15ns: {n_signal_events} / {n_goodRatio} = {dtEff} ")
print(f"Out of {nevents} events, {n_signal_events} are in the signal region.")
"""


# Compute final yield efficiency
final_efficiency = n_signal_events / nevents if nevents > 0 else 0
detector_efficiency = n_signal_events / (acceptance * nevents) if nevents > 0 else 0 
# Data for the table
table_data = [
    ["Any hit", f"{n_non_empty} / {nevents}", nonEmptyEff],
    ["At least one hit in each layer", f"{n_4LHits} / {n_non_empty}", fourLayersEff],
    ["Exactly one hit in each layer", f"{n_oneInEachLayer} / {n_4LHits}", oneInEachLayerEff],
    ["In a straight line", f"{n_inLine} / {n_oneInEachLayer}", inLineEff],
    ["No side panel hits (NPE < 0.5)", f"{n_panelless} / {n_inLine}", panellessEff],
    ["No hits in front/back slabs", f"{n_slabless} / {n_panelless}", slablessEff],
    [f"max/min NPE < {nPE_cut}", f"{n_goodRatio} / {n_slabless}", ratioEff],
    [f"max - min time < {dt_cut}ns", f"{n_signal_events} / {n_goodRatio}", dtEff]
]

# Display a summary row for the total events in the signal region
summary_data = [
    ["Total Events in Signal Region", f"{n_signal_events} / {nevents}", final_efficiency]
]

# Display table
print("===== Efficiencies Table =====")
print(tabulate(table_data, headers=["Cut", "Event Counts", "Cut Efficiency"], tablefmt="grid"))
print("\n===== Summary =====")
print(tabulate(summary_data, headers=["", "Event Counts", "Overall Efficiency"], tablefmt="grid"))
print("\n===== Weights =====")
print(np.unique(signalWeights * float(charge)**2))
print("\n===== Signal Yield =====")
print(signal_yield)


#with open(f"{input_path}/efficiency.txt","w") as outfile:
#	outfile.write(f"{mass} {charge} {detector_efficiency}\n")

with open(f"{input_path}/yield_SR1.txt","w") as outfile:
	outfile.write(f"{mass} {charge} {signal_yield} {max_weight} {detector_efficiency}\n")






