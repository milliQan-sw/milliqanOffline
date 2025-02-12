#define myLooper_cxx
#include "myLooper.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "TChain.h"
#include "TFile.h"
#include <fstream>

void myLooper::Loop( TString outFile, TString lumi, TString runTime)
{

   if (fChain == 0) return;
   
  // The root output file
  TFile* foutput = TFile::Open(outFile, "recreate");

  TNamed t_lumi("luminosity", lumi.Data());
  TNamed t_time("runTime", runTime.Data());
  
  TTree* tout = fChain->CloneTree(0);

  // A text file opened in "append" mode, where we store the number of events
  std::ofstream outputTextFile("skim_results.txt", std::ios::app);

   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t passed = 0;

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;


      // Some feedback to the user
      if ( (jentry % 1000) == 0 ) {
	    std::cout << "Processing " << jentry << "/" << nentries << std::endl;
      }

      // Sanity Check:
      if (chan->size() != area->size()) {
	    std::cout << "Different sizes" << endl;
      }
      if(runNumber == 1464) continue; //remove once good runs list is fixed

      if(tTrigger != 4096) continue;
      if(abs(tTimeDiff) > 250) continue;

	tout->Fill();
	passed = passed + 1;


   }


  // Write the root file out
    foutput->WriteTObject(tout);
    t_lumi.Write();
    t_time.Write();
    delete tout;
    foutput->Close();


    // Now the text file
    float frac =  1.*passed/nentries;
    outputTextFile << "Output file has    " << passed    << " events" << endl;
    outputTextFile << "Input  file has    " << nentries  << " events" << endl;
    outputTextFile << std::fixed << std::setprecision(5) << "Fraction of passed " << frac << endl;
    outputTextFile << " " << endl;
    outputTextFile.close();
}
