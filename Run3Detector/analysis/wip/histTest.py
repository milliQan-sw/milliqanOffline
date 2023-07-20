import ROOT

def PlotScatter(offlineTrigs,onlineTrigs):
    # Create a 1D histogram with 2 bins ranging from 0 to 2
    hist = ROOT.TH1F("trigger test", "trigger test",13, 0, 13)

    # Create the first histogram for the first half-bin with the first contribution (e.g., 3)
    hist1 = ROOT.TH1F("offlineTrigs", "offlineTrigs", 39, 0, 13)
    #hist1.SetBinContent(1, 3)
    #hist1.SetBinContent(2, 2)
    #list1 = {1,2,3,4,5,6,7,8,9,10,11,12,13}
    for index,num in enumerate(offlineTrigs):
        hist1.SetBinContent(1 + 3*index, num)


    # Create the second histogram for the second half-bin with the second contribution (e.g., 2)
    hist2 = ROOT.TH1F("onlineTrigs", "onlineTrigs", 39, 0, 13)
    for index,num in enumerate(onlineTrigs):
        hist2.SetBinContent(2 + 3*index, num)
    hist3 = ROOT.TH1F("onlineTrigs-offlineTrigs", "Bar 3", 39, 0, 13)
    #hist2.SetBinContent(1, 2)
    #hist2.SetBinContent(3, 2)
    Difference = [x - y for x, y in zip(onlineTrigs, offlineTrigs)]
    for index,num in enumerate(Difference):
        hist3.SetBinContent(3 + 3*index, num)


    # Get the maximum content value among both histograms
    max_content = max(hist1.GetMaximum(), hist2.GetMaximum(),hist3.GetMaximum())
    min_content = min(hist1.GetMinimum(), hist2.GetMinimum(),hist3.GetMinimum())
    hist.SetMaximum(max_content * 1.2)  # Adjust the y-axis range
    hist.SetMinimum(min_content * 1.2)

    # Create a legend and add entries for the markers
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    marker_style = 8  # Marker style: 8 is an open circle
    marker_size = 1.2  # Marker size
    legend.AddEntry(hist1, "offlineTrigs 1", "p")
    legend.AddEntry(hist2, "onlineTrigs", "p")
    legend.AddEntry(hist3, "onlineTrigs-offlineTrigs", "p")
    legend.SetFillColor(0)   # Set legend fill color to transparent

    # Create a canvas and draw the histograms and legend
    canvas = ROOT.TCanvas("canvas", "Two Bars Side by Side", 800, 600)
    NameOfTrigger = ["FourLayersD","3InRow","separateLayers","adjacentLayers","NLayers","External","NHits","Internal","TopPanels","TopPanelBotBar","FrontBackPanel","SParticle","ZeroBias"]
    #hist.GetXaxis().SetBinLabel(1, "Label for Bin 1")
    #hist.GetXaxis().SetBinLabel(2, "Label for Bin 2")
    #hist.GetXaxis().SetBinLabel(3, "Label for Bin 3")
    for index,test in enumerate(NameOfTrigger):
        hist.GetXaxis().SetBinLabel(index+1, test)


    hist.Draw()           # Draw the main histogram to set the axis range
    hist1.SetMarkerStyle(marker_style)
    hist2.SetMarkerStyle(marker_style)
    hist3.SetMarkerStyle(marker_style)
    hist1.SetMarkerSize(marker_size)
    hist2.SetMarkerSize(marker_size)
    hist3.SetMarkerSize(marker_size)
    hist1.SetMarkerColor(ROOT.kBlue)
    hist2.SetMarkerColor(ROOT.kRed)
    hist3.SetMarkerColor(ROOT.kGreen)
    hist1.Draw("P same")  # Draw the first marker
    hist2.Draw("P same") 
    hist3.Draw("P same")  # Draw the second marker
    legend.Draw()         # Draw the legend

    # Save the plot to a file (optional)
    #canvas.SaveAs("markers.png")
    output_file = ROOT.TFile("output_file.root", "RECREATE")
    canvas.Write()
    output_file.Close()

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)
    # Run in batch mode to prevent graphical window from opening
    offlineTrigs=[1,2,3,4,5,6,7,8,9,10,11,12,13]
    onlineTrigs=[3,2,3,4,53,6,72,8,9,10,11,12,13]
    PlotScatter(offlineTrigs,onlineTrigs)







