"""
9-26
the goal of this file is plot the histogram of same kind into the same canvas.

"""

import ROOT





def HistMerge(fileName):

	defaultTlist = ["default time"]
	correctedTList = ["default time"]

	#line_colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta, ROOT.kCyan, ROOT.kBlue-6, ROOT.kCyan-3,ROOT.kRed-6,ROOT.kBlack,ROOT.kViolet-9,ROOT.kOrange+1,ROOT.kRed-1,ROOT.kCyan+3]
	line_colors = [ROOT.kWhite, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kMagenta, ROOT.kCyan, ROOT.kBlue-6, ROOT.kCyan-3,ROOT.kRed-6,ROOT.kBlack,ROOT.kViolet-9,ROOT.kOrange+1,ROOT.kRed-1,ROOT.kCyan+3]
	root_file = ROOT.TFile(fileName, "UPDATE")


	canvas_title = " canvas title "
	root_file_objects = root_file.GetListOfKeys()
	for obj in root_file_objects:
		single_hist_name = obj.GetName()
		if "time" in single_hist_name:
			parts = single_hist_name.split('time')
			CutDetails = parts[0]
			if "corrected" in CutDetails:
				correctedTList.append(single_hist_name)
			else:
				defaultTlist.append(single_hist_name)

	
	NewCanvasName = "CorrectedmergedPlot"
	i = 0
	legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9) 
	canvas = ROOT.TCanvas(NewCanvasName, canvas_title, 800, 1200)
	for obj in root_file_objects:
		single_hist_name = obj.GetName()
		if single_hist_name in correctedTList:
			
			hist = root_file.Get(single_hist_name)
			hist.SetLineColor(line_colors[i])
			legend.AddEntry(hist, single_hist_name, "l")
			hist.Draw("same")
			i += 1
	
	legend.Draw()
	canvas.Write()
	canvas.Close()



	
	NewCanvasName = "defaultmergedPlot"
	i = 0
	legend1 = ROOT.TLegend(0.7, 0.7, 0.9, 0.9) 
	canvas1 = ROOT.TCanvas(NewCanvasName, canvas_title, 800, 1200)
	for obj in root_file_objects:
		single_hist_name = obj.GetName()
		if single_hist_name in defaultTlist:
			
			hist1 = root_file.Get(single_hist_name)
			hist1.SetLineColor(line_colors[i])
			hist1.Draw("same")
			legend1.AddEntry(hist1, single_hist_name, "l")
			i += 1
	
	legend1.Draw()
	canvas1.Write()
	canvas1.Close()



	#root_file.Delete("canvas_name" + ";*") #delete canvas
	root_file.Close()

if __name__ == "__main__":

	HistMerge("run1026_TimeFitdistributionEX1Hit.root")
	#HistMerge("run1026_durationcut.root")