import ROOT

def compare_histograms(file1_path, hist1_name, file2_path, hist2_name):
    # Open the ROOT files
    file1 = ROOT.TFile(file1_path)
    file2 = ROOT.TFile(file2_path)

    # Retrieve the histograms from the files
    hist1 = file1.Get(hist1_name)
    hist2 = file2.Get(hist2_name)

    # Create a new histogram to store the differences
    diff_hist = hist1.Clone("diffHist")
    diff_hist.Add(hist2, -1)

    ChanHist=diff_hist.ProjectionX()

    ChanHist.SetName("diff chan")

    ChanHist.SetXTitle("chan")

    output_file = ROOT.TFile("chanvsNPE_diff.root", "RECREATE")
    diff_hist.Write()
    ChanHist.Write()
    output_file.Close()

# Example usage:
compare_histograms("chanvsNPE_Nocut.root", "B ChanvsNPE", "chanvsNPE_withcut.root", "B ChanvsNPE")

