#include "TCanvas.h"
#include "TTree.h"
#include "TGaxis.h"
#include "TStyle.h"
#include "TFile.h"
#include <iostream>
#include <fstream>
#include "TMath.h"
#include "TChain.h"
#include "/net/cms26/cms26r0/zheng/barsim/milliQanSim/include/mqROOTEvent.hh"
#include "/net/cms26/cms26r0/zheng/barsim/milliQanSim/include/mqPMTRHit.hh"
//#include "/net/cms18/cms18r0/cms26r0/zheng/barsim/milliQanSim/include/mqROOTEvent.hh"
//#include "/net/cms18/cms18r0/cms26r0/zheng/barsim/milliQanSim/include/mqPMTRHit.hh"
//#include "milliQanSim/include/mqROOTEvent.hh"
//#include "milliQanSim/include/mqPMTRHit.hh"
#include "TGraph.h"
#include "TVector.h"
#include "TVectorD.h"
#include "TVectorF.h"
#include "TH1.h"
#include "TH1F.h"
#include "TString.h"
#include "TChain.h"
#include "TMultiGraph.h"
#include <vector>
#include <map>
//R__LOAD_LIBRARY(/homes/tianjiad/milliQanSim/build/libBenchCore.so)
R__LOAD_LIBRARY(/net/cms26/cms26r0/zheng/barsim/milliQanSim/build/libMilliQanCore.so)
using namespace std;


int simToDataPMT(int simChannel) {
    // First, if the hit is in a panel or slab, we manually map it
    if (simChannel == 77) return 68;
    else if (simChannel == 78) return 70;
    else if (simChannel == 79) return 69;
    else if (simChannel == 81) return 72;
    else if (simChannel == 82) return 74;
    else if (simChannel == 83) return 73;
    else if (simChannel == 97) return 71;
    else if (simChannel == 96) return 75;

    // Save the layer number, map the sim channel to the correct data number, and add the layer number back in
    int layerNumber = simChannel / 216;
    simChannel = simChannel % 216;

    if (simChannel <= 4) {
        return (simChannel + 11) + layerNumber * 16;
    } else if (simChannel <= 12) {
        return simChannel - 1 + layerNumber * 16;
    } else if (simChannel <= 16) {
        return simChannel - 13 + layerNumber * 16;
    } else {
        std::cerr << "Error: simChannel out of range" << std::endl;
        return -1;
    }
}

void waveinject() {
   // Open the input and output ROOT files
   TChain rootEvents("Events");
   rootEvents.Add("MilliQan.root");
   mqROOTEvent* myROOTEvent = new mqROOTEvent();
   rootEvents.SetBranchAddress("ROOTEvent", &myROOTEvent);
   TFile* outfile = new TFile("MilliQan_waveinjected.root", "RECREATE");
   
   // Variables for the waveform data structure
   const int nDigitizers = 5;
   const int nChannelsPerDigitizer = 16;
   const int nBins = 1024;
   double binWidth = 2.5;
   double rms_noise = 1;

   // Waveform data structure (5 digitizers, 16 channels each, and 1024 bins per channel)
   Float_t waveform[nDigitizers][nChannelsPerDigitizer][nBins] = {{{0}}};

   // Create a TTree to store the digitizer waveform data
   TTree* injectedTree = new TTree("Events", "Tree with digitizer waveform data");
   injectedTree->Branch("waveform", waveform, Form("waveform[%d][%d][%d]/F", nDigitizers, nChannelsPerDigitizer, nBins));

   // Load multifit pulse area function
   TF1 *fit = new TF1("fit", "gaus(0)", 0, 5000);
   fit->SetParameter(0, 7.23967e-02);
   fit->SetParameter(1, 1.48539e+03);
   fit->SetParameter(2, 2.90976e+02);

   // Load pulse shape
   TFile* f = new TFile("outputs/dataset812_averaged_waveform.root");
   TH1F* pulse_shape = (TH1F*)f->Get("average_waveform");

   // Random generator for noise
   TRandom3 randGen(0);

   Long64_t nentries = rootEvents.GetEntries();
   std::cout << "Entries: " << nentries << std::endl;

   // Loop over events
   for (Long64_t i = 0; i < nentries; i++) {
      if(i % (nentries / 100) == 0) std::cout << "Processing Event " << i << "..." << std::endl;
      rootEvents.GetEntry(i);

      // Clear the waveform data for the new event
      memset(waveform, 0, sizeof(waveform));

      // Loop over all hits for the PMTs in this event
      for (int j = 0; j < myROOTEvent->GetPMTRHits()->size(); j++) {
         mqPMTRHit* PMTRHit = myROOTEvent->GetPMTRHits()->at(j);
         int PMT_number = PMTRHit->GetPMTNumber();
         double initial_hit_time = PMTRHit->GetFirstHitTime();

         // Remap the PMT number to a digitizer and channel
         int remappedPMT = simToDataPMT(PMT_number);
         if (remappedPMT == -1) continue;  // Skip invalid PMT numbers

         // Determine which digitizer and channel this PMT corresponds to
         int digitizer = remappedPMT / nChannelsPerDigitizer;
         int channel = remappedPMT % nChannelsPerDigitizer;

         // Create a new histogram that copies the content of pulse_shape
         TH1F* new_waveform = (TH1F*)pulse_shape->Clone();
         
         // Scale the new waveform by the event area
         double event_area = fit->GetRandom();
         new_waveform->Scale(event_area / new_waveform->Integral(480, 640));

         // Fill the waveform array with the content from the new waveform
         for (int bin = 1; bin <= nBins; ++bin) {
            double bin_content = new_waveform->GetBinContent(bin);
            double noise = randGen.Gaus(0, rms_noise);
            waveform[digitizer][channel][bin - 1] += (bin_content + noise);
            
            // Cap the waveform value at 1250
            if (waveform[digitizer][channel][bin - 1] > 1250) waveform[digitizer][channel][bin - 1] = 1250;
         }

         delete new_waveform;  // Clean up the dynamically created histogram
      }

      // Fill the TTree with the waveform data for the current event
      injectedTree->Fill();
   }

   // Write the tree to the output file
   outfile->cd();
   injectedTree->Write();  // Write the tree with digitizer waveform data

   // Close the files
   f->Close();
   outfile->Close();
}

