"""
10-21 
the goal of this file is to normalized histograms in folder OSU_quickCheck


"""


import ROOT

root_file = ROOT.TFile("/home/czheng/scratch0/eventmissing/milliqanWorking/milliqanOffline/Run3Detector/analysis/wip/pulse_h/dataCut_variant/run1026_manyplots_more_bins.root", "UPDATE")

root_file_objects = root_file.GetListOfKeys()

for obj in root_file_objects:
    single_hist_name = obj.GetName()
    print(single_hist_name)
    if "chan vs npe : chan based" == single_hist_name:
        hist1=root_file.Get("Chan NPE distribution")
        hist1 = root_file.Get(single_hist_name)
        hist1.Scale(1.0 / hist1.Integral())
        hist1.Write("Normalized NPE(chan based) vs Chan")
  
    if "npe : chan based" == single_hist_name:
        hist2 = root_file.Get(single_hist_name)
        hist2.Scale(1.0 / hist2.Integral())
        hist2.Write("Normalized NPE distribution(chan based)")




root_file.Close()