#include "TCanvas.h"
#include "TH1.h"
#include "TH2.h"
#include "TLegend.h"
#include "TTree.h"
#include "functions.h"
#include "utility.cpp"
#include <RtypesCore.h>
#include <TFile.h>
#include <iostream>

int main() {
  // gStyle->SetOptStat("oue");
  TFile *file = TFile::Open(
      "/home/ryan/Documents/Data/MilliQan/beam_muon_slabMilliQan_flat.root");
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
  TH1F *h_npe = new TH1F("npe", "NPE", 500, 0, 100);
  TH1F *h_time = new TH1F("time", "Time", 500, -100, 100);

  // Creating histograms for timing distribution nPE scan
  TH1F *hist_0_2 =
      new TH1F("hist_0_1_1ns", "Time Difference between layer 0 and 2", 20, 0, 20);
  TH1F *hist_0_3 =
      new TH1F("hist_1_2_1ns", "Time Difference between layer 0 and 3 ", 20, 0, 20);
  TH1F *hist_1_3 =
      new TH1F("hist_2_3_1ns", "Time Difference between layer 1 and 3", 20, 0, 20);

  std::cout << "Initialized histograms" << std::endl;

  for (Long64_t i = 0; i < nEntries; ++i) {
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
      h_time->Fill(value);
    }

    for (const auto &value : *nPE) {
      h_npe->Fill(value);
    }

    // Find the time difference
    std::map<int, eventInfo> time_difference =
        layerTimeDifference(*time, *layer, *nPE);
    fillTimeDifference(*hist_0_2, time_difference, 0, 1);
    fillTimeDifference(*hist_0_3, time_difference, 1, 2);
    fillTimeDifference(*hist_1_3, time_difference, 2, 3);
  }

  // Display Plots
  TCanvas *canvas0 = new TCanvas("c", "c", 400, 400);
  TLegend *legend0 = new TLegend(0.1, 0.7, 0.48, 0.9);
  legend0->SetHeader("Legend", "C");
  legend0->AddEntry(hist_0_2, "0 and 1 ");
  legend0->AddEntry(hist_0_3, "1 and 2");
  legend0->AddEntry(hist_1_3, "2 and 3");
  gPad->SetLogy();
  hist_0_2->SetLineColor(kRed);
  hist_0_3->SetLineColor(kBlue);
  hist_1_3->SetLineColor(kGreen);
  hist_0_2->Draw();
  legend0->Draw("SAME");
  hist_0_3->Draw("SAME");
  hist_1_3->Draw("SAME");
  canvas0->Update();


  // Save Plots in ROOT file
  TFile outputFile("timeDifference.root", "UPDATE");
  canvas0->Write();
  hist_0_2->Write();
  hist_0_3->Write();
  hist_1_3->Write();

  return 0;
}
