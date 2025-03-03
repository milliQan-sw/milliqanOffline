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
#include <map>
#include <set>
#include <utility>

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
   
   // Retrieve the channel mapping from the first event.
   // We assume the branch "chanMap" is already set up and is of type
   // std::vector<std::vector<int>>* where each inner vector has 4 ints: 
   // [col, row, layer, PMT].
   fChain->GetEntry(0);
   // "chanMap" is assumed to be a member variable (pointer) set via SetBranchAddress.
   
   // Loop over entries (events)
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
      
      // Build a map keyed by (col, row) to record which layers have a hit.
      std::map< std::pair<int,int>, std::set<int> > hit_map;
      
      // Loop over hits in the event
      for (unsigned long k = 0; k < chan->size(); k++){
         // Apply standard cuts
         if (pickupFlagTight->at(k)) continue;
         if (!boardsMatched) continue;
         if (ipulse->at(k) != 0) continue;
         if (timeFit_module_calibrated->at(k) < 900 ||
             timeFit_module_calibrated->at(k) > 1500) continue;
         if (area->at(k) < minArea) continue;
         
         // Get the channel number for this hit
         int ch = chan->at(k);
         
         // Retrieve the mapping for channel 'ch' from the chanMap branch.
         // Each mapping is a vector with 4 integers: [col, row, layer, PMT]
         if (ch < 0 || ch >= static_cast<int>(chanMap->size())) continue;
         std::vector<int> mapping = chanMap->at(ch);
         if (mapping.size() < 4) continue; // Safety check
         
         int col   = mapping[0];
         int row   = mapping[1];
         int layer = mapping[2];
         // int pmt = mapping[3]; // PMT info not needed here.
         
         std::pair<int,int> key = std::make_pair(col, row);
         hit_map[key].insert(layer);
      }
      
      // Check if any (col, row) location has hits in at least 3 distinct layers.
      bool straightLineEvent = false;
      for (auto const &entry : hit_map) {
         if (entry.second.size() >= 3) {
            straightLineEvent = true;
            break;
         }
      }
      
      // Fill the event only if the condition is met.
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