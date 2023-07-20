import ROOT 

def create_custom_histogram(FourLayersD,e3InRowD,separateLayersD,adjacentLayersD,NLayersD,ExternalD,NHitsD,InternalD,TopPanelsD,TopPanelBotBarD,FrontBackPanelD,SParticleD,ZeroBiasD):
    # Create a histogram with custom bin titles
    hist = ROOT.TH1D("hist", "online&offline trigger comparision", 13, 0, 13)
    hist.GetXaxis().SetBinLabel(1, "FourLayers")
    hist.GetXaxis().SetBinLabel(2, "3InRow")
    hist.GetXaxis().SetBinLabel(3, "separateLayers")
    hist.GetXaxis().SetBinLabel(4, "adjacentLayers")
    hist.GetXaxis().SetBinLabel(5, "NLayers")
    hist.GetXaxis().SetBinLabel(6, "External")
    hist.GetXaxis().SetBinLabel(7, "NHits")
    hist.GetXaxis().SetBinLabel(8, "Internal")
    hist.GetXaxis().SetBinLabel(9, "TopPanels")
    hist.GetXaxis().SetBinLabel(10, "TopPanelBotBar")
    hist.GetXaxis().SetBinLabel(11, "FrontBackPanel")
    hist.GetXaxis().SetBinLabel(12, "SParticle")
    hist.GetXaxis().SetBinLabel(13, "ZeroBias")


    # Fill the histogram with data
    hist.Fill("FourLayers",FourLayersD)
    hist.Fill("3InRow", e3InRowD)
    hist.Fill("separateLayers", separateLayersD)
    hist.Fill("adjacentLayers",adjacentLayersD)
    hist.Fill("NLayers",NLayersD)
    hist.Fill("External",ExternalD)
    hist.Fill("NHits",NHitsD)
    hist.Fill("Internal",InternalD)
    hist.Fill("TopPanels",TopPanelsD)
    hist.Fill("TopPanelBotBar",TopPanelBotBarD)
    hist.Fill("FrontBackPanel",FrontBackPanelD)
    hist.Fill("SParticle",SParticleD)
    hist.Fill("ZeroBias",ZeroBiasD)
    


    return hist

def plot_scatter_plot(hist, output_file):

    canvas = ROOT.TCanvas("canvas", "Custom Scatter Plot Canvas", 800, 600)
    canvas.SetMargin(0.1, 0.1, 0.1, 0.1) 
    hist.SetStats(False)
    #hist.Draw("P") 
    hist.GetXaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetLabelOffset(0.01)

    Binlabel = ["FourLayers","3InRow","separateLayers","adjacentLayers","NLayers","External","NHits","Internal","TopPanels","TopPanelBotBar","FrontBackPanel","SParticle","ZeroBias"]

    
    points = ROOT.TGraph()
    for i in range(1, hist.GetNbinsX() + 1):
        bin_center = hist.GetXaxis().GetBinCenter(i)
        bin_value = hist.GetBinContent(i)
        points.SetPoint(i-1, bin_center, bin_value)
    
    #axis = points.GetXaxis()
    #for i in range(len(Binlabel)):
    #    axis.SetBinLabel(i + 1, Binlabel[i])


    points.SetMarkerStyle(20)
    points.Draw("SAMEP")

    canvas.Write()



if __name__ == "__main__":
    if not ROOT.gROOT.IsBatch():
        ROOT.gROOT.SetBatch(True)

    output_file = ROOT.TFile("output_file.root", "RECREATE")
    FourLayersD = 1
    e3InRowD = 2
    separateLayersD = 3
    adjacentLayersD = 7
    NLayersD = 9
    ExternalD = 11
    NHitsD = 0
    InternalD =0
    TopPanelsD=9
    TopPanelBotBarD=10
    FrontBackPanelD =11
    SParticleD=20
    ZeroBiasD = -10

    hist = create_custom_histogram(FourLayersD,e3InRowD,separateLayersD,adjacentLayersD,NLayersD,ExternalD,NHitsD,InternalD,TopPanelsD,TopPanelBotBarD,FrontBackPanelD,SParticleD,ZeroBiasD)

    plot_scatter_plot(hist, output_file)

    output_file.Close()







