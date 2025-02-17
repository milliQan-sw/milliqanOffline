#define myLooper_cxx
#include "myLooper.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "TChain.h"
#include "TFile.h"
#include <fstream>
#include "TNamed.h"
#include <vector>
#include <iomanip>

void myLooper::Loop(TString outFile, TString lumi, TString runTime)
{
   // Check that the input tree/chain exists
   if (fChain == 0) return;
   
   // Open the output file
   TFile* foutput = TFile::Open(outFile, "recreate");
   if (!foutput || foutput->IsZombie()){
      std::cout << "Could not create output file" << std::endl;
      return;
   }
   
   // Create TNamed objects to store luminosity and runtime info
   TNamed t_lumi("luminosity", lumi.Data());
   TNamed t_time("runTime", runTime.Data());
   
   // Clone the tree structure (but not the events yet)
   TTree* tout = fChain->CloneTree(0);
   
   // Open a text file in append mode to log results
   std::ofstream outputTextFile("skim_results.txt", std::ios::app);
   
   // Set the minimum area requirement
   float minArea = 100000.;
   
   // Get the total number of entries
   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t passed = 0;
   
   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry = 0; jentry < nentries; jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);
      nbytes += nb;
      
      // Provide feedback every 1000 events
      if ((jentry % 1000) == 0)
         std::cout << "Processing " << jentry << "/" << nentries << std::endl;
      
      // Sanity check (assuming 'chan' and 'area' are vectors)
      if (chan->size() != area->size()){
         std::cout << "Different sizes in 'chan' and 'area' for entry " << jentry << std::endl;
      }
      
      // Initialize a 3D array to record slab hits.
      // Dimensions: 4 layers x 4 rows x 3 columns.
      std::vector<std::vector<std::vector<bool>>> slabHit(
         4, std::vector<std::vector<bool>>(4, std::vector<bool>(3, false))
      );
      
      // Loop over hits in the event
      for (unsigned long k = 0; k < chan->size(); k++){
         // Apply the standard cuts
         if (pickupFlagTight->at(k)) continue;
         if (boardsMatched->at(k)) continue;
         if (ipulse->at(k) != 0) continue;
         if (timeFit_module_calibrated->at(k) < 900 ||
             timeFit_module_calibrated->at(k) > 1500) continue;
         if (area->at(k) < minArea) continue;
         
         // Get the offline channel number for this hit
         int ch = chan->at(k);
         
         // Determine the layer from the channel number.
         // Channels 0-23: Layer 0, 24-47: Layer 1, 48-71: Layer 2, 72-95: Layer 3.
         int layer = ch / 24;  // 0-indexed layers
         if (layer < 0 || layer > 3) continue; // safety check
         
         // Determine the channel number within the layer.
         int ch_in_layer = ch % 24;
         
         // Determine the column:
         // ch_in_layer in [0,7] -> column 2, [8,15] -> column 1, [16,23] -> column 0.
         int col;
         if (ch_in_layer < 8)      col = 2;
         else if (ch_in_layer < 16) col = 1;
         else                      col = 0;
         
         // Determine the row:
         // For each column block of 8 channels, row = 3 - ((ch_in_layer % 8) / 2)
         int row = 3 - ((ch_in_layer % 8) / 2);
         
         // Mark this slab as hit in the given layer.
         slabHit[layer][row][col] = true;
      }
      
      // Now, for each slab position (row, col), count how many layers are hit.
      bool straightLineEvent = false;
      for (int r = 0; r < 4 && !straightLineEvent; r++){
         for (int c = 0; c < 3 && !straightLineEvent; c++){
            int layersHit = 0;
            for (int l = 0; l < 4; l++){
               if (slabHit[l][r][c])
                  layersHit++;
            }
            // Require the slab to be hit in at least 3 layers.
            if (layersHit >= 3)
               straightLineEvent = true;
         }
      }
      
      // Fill the event only if the straight-line cut is satisfied.
      if (straightLineEvent) {
         tout->Fill();
         passed++;
      }
   }
   
   // Write the output tree and additional objects to the ROOT file
   foutput->WriteTObject(tout);
   t_lumi.Write();
   t_time.Write();
   delete tout;
   foutput->Close();
   
   // Write summary information to the text file
   float frac = (nentries > 0 ? static_cast<float>(passed) / nentries : 0);
   outputTextFile << "Output file has    " << passed    << " events" << std::endl;
   outputTextFile << "Input  file has    " << nentries  << " events" << std::endl;
   outputTextFile << std::fixed << std::setprecision(5) << "Fraction of passed " << frac << std::endl;
   outputTextFile << " " << std::endl;
   outputTextFile.close();
}