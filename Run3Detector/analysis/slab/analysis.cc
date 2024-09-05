#include <RtypesCore.h>
#include <TFile.h>
#include <algorithm>
#include <iterator>
#include <set>
#include "TCanvas.h"
#include "utility.cpp"
#include "functions.h"
#include "TTree.h"
#include "TH1.h"
#include "TH2.h"
#include "TLegend.h"
#include "TString.h"
#include <iostream>



int main() {
  //gStyle->SetOptStat("oue");
  TFile *file = TFile::Open(
                            "/home/ryan/Documents/Research/Data/beam_muon_slabMilliQan_flat.root");
  TTree *tree = (TTree *)file->Get("t");

  // Setup variables to hold leaves
  std::vector<float> *nPE = 0;
  std::vector<float> *time = 0;
  std::vector<int> *layer = 0;
  std::vector<int> *column = 0;
  std::vector<int> *row = 0;
  tree->SetBranchAddress("pmt_nPE", &nPE);
  tree->SetBranchAddress("pmt_time", &time);
  tree->SetBranchAddress("pmt_layer", &layer);
  tree->SetBranchAddress("pmt_row", &row);
  tree->SetBranchAddress("pmt_column", &column);

  Long64_t nEntries = tree->GetEntries();

  // Initializng values to store cuts
  int layer_cut = 0;
  int four_layer_cut = 0;

  // Create histograms to store npe and timing distributions
  TH1F h_npe = TH1F("npe", "NPE", 500, 0, 100);
  TH1F h_time = TH1F("time", "Time", 500, -100, 100);
  TH2F h_npe_dist = TH2F("npe_dist" , "nPE Distribution", 16, 0, 16, 17, 0, 17);   

  // Creating histograms for timing distribution nPE scan
  TH1F hist_0_0 = TH1F("hist_0_0", "Time Difference between layer 0 and 1 (0 nPE)", 100, 0, 20);
  TH1F hist_1_0 = TH1F("hist_1_0", "Time Difference between layer 1 and 2 (0 nPE)", 100, 0, 20);
  TH1F hist_2_0 = TH1F("hist_2_0", "Time Difference between layer 2 and 3 (0 nPE)", 100, 0, 20);
  TH1F hist_0_1 = TH1F("hist_0_1", "Time Difference between layer 0 and 1 (1 nPE)", 100, 0, 20);
  TH1F hist_1_1 = TH1F("hist_1_1", "Time Difference between layer 1 and 2 (1 nPE)", 100, 0, 20);
  TH1F hist_2_1 = TH1F("hist_2_1", "Time Difference between layer 2 and 3 (1 nPE)", 100, 0, 20);
  TH1F hist_0_2 = TH1F("hist_0_2", "Time Difference between layer 0 and 1 (2 nPE)", 100, 0, 20);
  TH1F hist_1_2 = TH1F("hist_1_2", "Time Difference between layer 1 and 2 (2 nPE)", 100, 0, 20);
  TH1F hist_2_2 = TH1F("hist_2_2", "Time Difference between layer 2 and 3 (2 nPE)", 100, 0, 20);
  TH1F hist_0_3 = TH1F("hist_0_3", "Time Difference between layer 0 and 1 (3 nPE)", 100, 0, 20);
  TH1F hist_1_3 = TH1F("hist_1_3", "Time Difference between layer 1 and 2 (3 nPE)", 100, 0, 20);
  TH1F hist_2_3 = TH1F("hist_2_3", "Time Difference between layer 2 and 3 (3 nPE)", 100, 0, 20);
  TH1F hist_0_4 = TH1F("hist_0_4", "Time Difference between layer 0 and 1 (4 nPE)", 100, 0, 20);
  TH1F hist_1_4 = TH1F("hist_1_4", "Time Difference between layer 1 and 2 (4 nPE)", 100, 0, 20);
  TH1F hist_2_4 = TH1F("hist_2_4", "Time Difference between layer 2 and 3 (4 nPE)", 100, 0, 20);

  std::cout << "Initialized histograms" << std::endl;
  
  for(Long64_t i = 0; i < nEntries; ++i) {
    tree->GetEntry(i);

    // Apply Cuts
    if (layer->size() < 4)
      continue;
    ++layer_cut;
    if (!(fourLayers(*layer)))
      continue;
    ++four_layer_cut;

    // Plot time and nPE distribution
    for (const auto &value : *time) {
      h_time.Fill(value);
    }
    for (const auto &value : *nPE) {
      h_npe.Fill(value);
    }

    // Find the time difference
    float npeCuts[3] = {0. , 10., 20.};
    std::map<int, float> time_difference_between_layers1 =
        layerTimeDifference(*time, *layer, *nPE, npeCuts[0]);
    hist_0_0.Fill(time_difference_between_layers1[0]);
    hist_1_0.Fill(time_difference_between_layers1[1]);
    hist_2_0.Fill(time_difference_between_layers1[2]);

    std::map<int, float> time_difference_between_layers2 =
        layerTimeDifference(*time, *layer, *nPE, npeCuts[1]);
    hist_0_1.Fill(time_difference_between_layers2[0]);
    hist_1_1.Fill(time_difference_between_layers2[1]);
    hist_2_1.Fill(time_difference_between_layers2[2]);

    std::map<int, float> time_difference_between_layers3 =
        layerTimeDifference(*time, *layer, *nPE, npeCuts[2]);
    hist_0_2.Fill(time_difference_between_layers3[0]);
    hist_1_2.Fill(time_difference_between_layers3[1]);
    hist_2_2.Fill(time_difference_between_layers3[2]);
    

    // Find the nPE Distribution
    for (const auto item : *column) {
      for (const auto item2 : *row){
        for (const auto item3 : *nPE){
          h_npe_dist.Fill(item, item2, item3);
        }
      }
    }

  }

  


  TCanvas *canvas0 = new TCanvas("c", "c", 400, 400);
  canvas0->Divide(3);
  canvas0->SetLogy(); 

  TLegend *legend0 = new TLegend(0.1, 0.7, 0.48, 0.9);
  legend0->SetHeader("Legend", "C");
  legend0->AddEntry(&hist_0_0, "Max time difference between layer 0 and 1");
  legend0->AddEntry(&hist_1_0, "Max time difference between layer 1 and 2");
  legend0->AddEntry(&hist_2_0, "Max time difference between layer 2 and 3");

  hist_0_0.SetLineColor(kRed);
  hist_1_0.SetLineColor(kBlue);
  hist_2_0.SetLineColor(kGreen);

  canvas0->cd(1);
  gPad->SetLogy();
  hist_0_0.Fit("gaus", "", "", 0, 6);
  hist_0_0.Draw();
  legend0->Draw("SAME");
  hist_1_0.Draw("SAME");
  hist_2_0.Draw("SAME");

  TLegend *legend1 = new TLegend(0.1, 0.7, 0.48, 0.9);
  legend0->SetHeader("Legend", "C");
  legend0->AddEntry(&hist_0_1, "Max time difference between layer 0 and 1");
  legend0->AddEntry(&hist_1_1, "Max time difference between layer 1 and 2");
  legend0->AddEntry(&hist_2_1, "Max time difference between layer 2 and 3");

  hist_0_1.SetLineColor(kRed);
  hist_1_1.SetLineColor(kBlue);
  hist_2_1.SetLineColor(kGreen);

  canvas0->cd(2);
  gPad->SetLogy();
  hist_0_1.Fit("gaus", "", "", 0, 6);
  hist_0_1.Draw();
  legend1->Draw("SAME");
  hist_1_1.Draw("SAME");
  hist_2_1.Draw("SAME");

  TLegend *legend2 = new TLegend(0.1, 0.7, 0.48, 0.9);
  legend2->SetHeader("Legend", "C");
  legend2->AddEntry(&hist_0_2, "Max time difference between layer 0 and 1");
  legend2->AddEntry(&hist_1_2, "Max time difference between layer 1 and 2");
  legend2->AddEntry(&hist_2_2, "Max time difference between layer 2 and 3");

  hist_0_2.SetLineColor(kRed);
  hist_1_2.SetLineColor(kBlue);
  hist_2_2.SetLineColor(kGreen);

  canvas0->cd(3);
  gPad->SetLogy();
  hist_0_2.Fit("gaus", "", "", 0, 6);
  hist_0_2.Draw();
  legend2->Draw("SAME");
  hist_1_2.Draw("SAME");
  hist_2_2.Draw("SAME");

  canvas0->SaveAs("timingDistributionScan.pdf");
  canvas0->Show();

    TCanvas *canvas2 =
        new TCanvas("canvas", "NPE and Timing Distributions", 400, 400);
    canvas2->Divide(2, 1);
    canvas2->cd(1);
    h_npe.Draw();
    canvas2->cd(2);
    h_time.Draw();

    canvas2->Update();
    canvas2->SaveAs("npe_timing_dist.pdf");

    TCanvas *canvas3 = new TCanvas("canvas", "NPE distribution", 400, 400);
    canvas3->cd();
    h_npe_dist.Draw("COLZ");
    canvas3->Update();
    canvas3->SaveAs("npe_distribution.pdf");
    
      
    return 0;
}


