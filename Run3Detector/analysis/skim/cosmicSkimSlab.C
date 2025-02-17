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
      if ( (jentry % 1000) == 0 ) {
         std::cout << "Processing " << jentry << "/" << nentries << std::endl;
      }
      
      // Sanity Check: assume 'chan' and 'area' are vectors.
      if (chan->size() != area->size()){
         std::cout << "Different sizes in 'chan' and 'area' for entry " << jentry << std::endl;
      }
      
      // Instead of the previous 16-path (4x4) structure, create a new 2D array
      // for the new detector: 3 columns x 4 layers.
      std::vector<std::vector<bool>> columnLayerHit(3, std::vector<bool>(4, false));
      
      // (Optional) Flags for panel hits; kept in case they are used elsewhere.
      bool frontPanelHit = false;
      bool backPanelHit = false;
      
      // Loop over all elements (hits) in the event
      for (unsigned long k = 0; k < chan->size(); k++) {
            // Panel info (unchanged)
            if (type->at(k) == 2) {
                  if (layer->at(k) == 0) frontPanelHit = true;
                  if (layer->at(k) == 2) backPanelHit = true;
            }
            // Apply cuts
            if (pickupFlagTight->at(k)) continue; 
            if (boardsMatched->at(k)) continue;
            if (ipulse->at(k) != 0) continue;
            if (timeFit_module_calibrated->at(k) < 900 || timeFit_module_calibrated->at(k) > 1500) continue;
            if (area->at(k) < minArea) continue;
            
            // For the new geometry, record a hit by column and layer.
            // (Assuming: column->at(k) in {0,1,2} and layer->at(k) in {0,1,2,3})
            int col = column->at(k);
            int lay = layer->at(k);
            if(col < 3 && lay < 4) {
               columnLayerHit[col][lay] = true;
            }
      }
      
      // Check if any column (across layers) has at least 3 layers with a hit.
      bool straightLineEvent = false;
      for (int col = 0; col < 3; col++) {
            int layersHit = 0;
            for (int lay = 0; lay < 4; lay++){
                  if(columnLayerHit[col][lay])
                        layersHit++;
            }
            if(layersHit >= 3){
                  straightLineEvent = true;
                  break;
            }
      }
      
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