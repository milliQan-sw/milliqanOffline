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
#include <iomanip>

void myLooper::Loop(TString outFile, TString lumi, TString runTime)
{
   // Check that the input tree/chain exists
   if (fChain == 0) return;

   // Create the output file
   TFile* foutput = TFile::Open(outFile, "RECREATE");
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
      // Load the jentry-th entry
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);
      nbytes += nb;

      // Provide feedback every 1000 entries
      if (jentry % 1000 == 0)
         std::cout << "Processing " << jentry << "/" << nentries << std::endl;

      // Sanity Check: assume 'chan' and 'area' are branches that are vectors.
      if (chan->size() != area->size()){
         std::cout << "Different sizes in 'chan' and 'area' for entry " << jentry << std::endl;
      }

      // Loop over the elements in the event (assuming vector branches)
      unsigned long nElements = chan->size();
      for (unsigned long k = 0; k < nElements; k++){
         // Apply a series of cuts
         if (pickupFlagTight->at(k)) continue;
         if (boardsMatched->at(k)) continue;
         if (type->at(k) != 1) continue;
         if (ipulse->at(k) != 0) continue;
         if (timeFit_module_calibrated->at(k) < 900 || timeFit_module_calibrated->at(k) > 1500) continue;
         if (area->at(k) < minArea) continue;

         // Originally, hit information for the straight-line cut was collected here.
         // Since the straight-line cut is deactivated, we do not need to mark any hits.
      }

      // Since the straight-line cut is removed, fill every event that passes the above cuts.
      tout->Fill();
      passed++;
   }

   // Write the output tree and additional objects to the ROOT file
   foutput->WriteTObject(tout);
   t_lumi.Write();
   t_time.Write();
   delete tout;
   foutput->Close();

   // Write summary information to the text file
   float frac = (nentries > 0 ? static_cast<float>(passed)/nentries : 0);
   outputTextFile << "Output file has    " << passed    << " events" << std::endl;
   outputTextFile << "Input  file has    " << nentries  << " events" << std::endl;
   outputTextFile << std::fixed << std::setprecision(5) << "Fraction of passed " << frac << std::endl;
   outputTextFile << std::endl;
   outputTextFile.close();
}