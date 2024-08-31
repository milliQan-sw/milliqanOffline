#include <TFile.h>
#include <TH1I.h>
#include <TTree.h>
#include <vector>
#include <iostream>

int verifyData() {
  // Load in ROOT file
  TFile *file = TFile::Open(
                            "/home/ryan/Documents/Data/MilliQan/beam_muon_slabMilliQan_flat.root");
  TTree *tree = (TTree *)file->Get("t");

  // Instantiate Branch Variables
  // You have to initialize the vector pointer to 0 otherwise it breaks
  std::vector<int>* columns = 0;
  std::vector<int>* rows = 0;
  std::vector<int>* layers = 0;
  std::vector<float>* time = 0;

  tree->SetBranchAddress("pmt_column", &columns);
  tree->SetBranchAddress("pmt_row", &rows);
  tree->SetBranchAddress("pmt_time", &time);
  tree->SetBranchAddress("pmt_layer", &layers);
  

  
  // Instantiate Histograms
  TH1I *hist_columns = new TH1I("hist_columns", "Columns", 16, 0, 15);
  TH1I *hist_layers = new TH1I("hist_layers", "layers", 4, 0, 3);
  TH1I *hist_rows = new TH1I("hist_rows", "Rows", 12, 0, 11);

  Long64_t nEntries = tree->GetEntries();
  std::cout << "Number of entries: " <<  nEntries << std::endl;

  // The first 2 entries have poorly formatted data
  for(Long64_t i = 2; i < nEntries; ++i) {
    tree->GetEntry(i);
    // Ensure that the numbering of columns is really from 0-11
    hist_columns->Fill(columns->front());
    // Ensure that the numbering of rows is from 0-15
    hist_rows->Fill(rows->front());
    // Ensure that only columns 0-3 pops up in layer 0, 4-7 in layer 1 etc.
    }
    };
   TCanvas *canvas = new TCanvas("c", "c", 400, 400);
   canvas->Divide(2, 1);
   canvas->cd(1);
   hist_columns->Draw();
   canvas->cd(2);
   hist_rows->Draw();

   canvas->Update();
  
  return 0;
}
