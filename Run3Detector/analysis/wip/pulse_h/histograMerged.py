"""
9-26
the goal of this file is plot the histogram of same kind into the same canvas.

"""

import ROOT

plotingDict = {}

Datalist = []



line_colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta,
               ROOT.kCyan, ROOT.kViolet, ROOT.kPink, ROOT.kAzure, ROOT.kTeal,ROOT.kBlack,ROOT.kGray]

root_file = ROOT.TFile("run1026_heightcut.root", "UPDATE")


canvas_title = " canvas title "
root_file_objects = root_file.GetListOfKeys()
for obj in root_file_objects:
	single_hist_name = obj.GetName()
	if ":" in single_hist_name:
		parts = single_hist_name.split(':')
		CutDetails = parts[0]
		
		#print(CutDetails)
		dataCollect = parts[1]
		Datalist.append(dataCollect)

DataSet=set(Datalist)

for data in DataSet:
	NewCanvasName = str(data) + "mergedPlot"
	i = 0
	legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9) 
	canvas = ROOT.TCanvas(NewCanvasName, canvas_title, 800, 600)
	for obj in root_file_objects:
		single_hist_name = obj.GetName()
		if ":" in single_hist_name:
			parts = single_hist_name.split(':')
			if parts[1] == data:
				hist = root_file.Get(single_hist_name)
				hist.SetLineColor(line_colors[i])
				hist.Draw("same")
				legend.AddEntry(hist, parts[0], "l")
				i += 1
	
	legend.Draw()
	canvas.Write()
	canvas.Close()

#root_file.Delete("canvas_name" + ";*") #delete canvas
root_file.Close()
