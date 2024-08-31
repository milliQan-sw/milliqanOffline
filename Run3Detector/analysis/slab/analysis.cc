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
#include <iostream>



int main() {
  //gStyle->SetOptStat("oue");
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
  //std::cout << "Number of entries " << nEntries << std::endl;
  int layer_cut = 0;
  int four_layer_cut = 0;

  // Create histograms to store npe and timing distributions
  TH1F *h_npe = new TH1F("npe", "NPE", 500, 0, 100);
  TH1F *h_time = new TH1F("time", "Time", 500, -100, 100);
  TH1F *h_time_diff = new TH1F("time", "Time Difference", 500, 0, 100);
  TH1F *h_time_diff_1 = new TH1F("time_diff_1", "Time Difference Between Layer 0 and 1", 100, 0, 20);
  TH1F *h_time_diff_2 = new TH1F("time_diff_2", "Time Difference Between Layer 1 and 2", 100, 0, 20);
  TH1F *h_time_diff_3 = new TH1F("time_diff_3", "Time Difference Between Layer 2 and 3", 100, 0, 20);
  TH2F *h_npe_dist = new TH2F("npe_dist" , "nPE Distribution", 16, 0, 16, 17, 0, 17);   

  
  for(Long64_t i = 0; i < nEntries; ++i) {
    tree->GetEntry(i);
    
    if (layer->size() < 4)
      continue;

    ++layer_cut;
    if (!(fourLayers(*layer)))
      continue;

    ++four_layer_cut;

    for (const auto &value : *time) {
      h_time->Fill(value);
    }
    for (const auto &value : *nPE) {
      h_npe->Fill(value);
    }

    std::map<int, float> time_difference_between_layers =
      layerTimeDifference(*time, *layer, *nPE, 30.);


    h_time_diff_1->Fill(time_difference_between_layers[0]);
    h_time_diff_2->Fill(time_difference_between_layers[1]);
    h_time_diff_3->Fill(time_difference_between_layers[2]);


    // Change these to 1D histograms for a certain channel
    // nPE Distribution
    for (const auto item : *column) {
      for (const auto item2 : *row){
        for (const auto item3 : *nPE){
          h_npe_dist->Fill(item, item2, item3);
        }
      }
    }

    // Timing distribution within a slab

  }

  


  TCanvas *canvas1 = new TCanvas("c", "c", 400, 400);
  canvas1->SetLogy(); 
  // Setup Legend
  TLegend *legend = new TLegend(0.1, 0.7, 0.48, 0.9);
  legend->SetHeader("Legend", "C");
  legend->AddEntry(h_time_diff_1, "Max time difference between layer 0 and 1");
  legend->AddEntry(h_time_diff_2, "Max time difference between layer 1 and 2");
  legend->AddEntry(h_time_diff_3, "Max time difference between layer 2 and 3");

  h_time_diff_1->SetLineColor(kRed);
  h_time_diff_2->SetLineColor(kBlue);
  h_time_diff_3->SetLineColor(kGreen);

  canvas1->cd();
  h_time_diff_1->Draw();
  legend->Draw("SAME");
  h_time_diff_2->Draw("SAME");
  h_time_diff_3->Draw("SAME");

  canvas1->SaveAs("max_time_diff.pdf");
  std::cout << "Cutflow" << std::endl;
  std::cout << "4 layers: " << layer_cut << std::endl;
  std::cout << "each layer: " << four_layer_cut << std::endl;


    TCanvas *canvas2 =
        new TCanvas("canvas", "NPE and Timing Distributions", 400, 400);
    canvas2->Divide(2, 1);
    canvas2->cd(1);
    h_npe->Draw();
    canvas2->cd(2);
    h_time->Draw();

    canvas2->Update();
    canvas2->SaveAs("npe_timing_dist.pdf");

    TCanvas *canvas3 = new TCanvas("canvas", "NPE distribution", 400, 400);
    canvas3->cd();
    h_npe_dist->Draw("COLZ");
    canvas3->Update();
    canvas3->SaveAs("npe_distribution.pdf");
    
      
    return 0;
}


