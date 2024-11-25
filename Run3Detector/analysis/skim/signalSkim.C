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

void myLooper::Loop( TString outFile, TString lumi, TString runTime)
{
  // I think the following works 
  // .L myLooper.C+
  // TChain *ch = new TChain("t");
  // ch->Add("SomeOtherRun.root");
  // ch->Add("YetAnotherRun.root");
  // myLooper t(ch);
  // t.Loop("outfile.root")

  //       To read only selected branches, Insert statements like:
  // METHOD1:
  //    fChain->SetBranchStatus("*",0);  // disable all branches
  //    fChain->SetBranchStatus("branchname",1);  // activate branchname
  // METHOD2: replace line
  //    fChain->GetEntry(jentry);       //read all branches
  // by  b_branchname->GetEntry(ientry); //read only this branch

   if (fChain == 0) return;
   
  // The root output file
  TFile* foutput = TFile::Open(outFile, "recreate");

  TNamed t_lumi("luminosity", lumi.Data());
  TNamed t_time("runTime", runTime.Data());

  // The output tree (possibly pruned)
  // If you need to prune branches, disable the input branch first (part 1)...
  // ch.SetBranchStatus("[branch name]", 0);
  TTree* tout = fChain->CloneTree(0);

  // A text file opened in "append" mode, where we store the number of events
  std::ofstream outputTextFile("skim_results.txt", std::ios::app);

  // The minimum area requirement
  float minArea = 500000.;

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

      //create boolean to track which straight line paths / layers have been hit in this event
      std::vector<std::vector<bool>> straightPathsHit(16, std::vector<bool>(4, false));

      bool panelHit = false;

      for (unsigned long k=0; k<chan->size(); k++) {
            if (type->at(k) == 2) {
                  panelHit = true;
                  break;
            }
            if (pickupFlagTight->at(k)) continue;
            if (type->at(k) != 0) continue;
            if (ipulse->at(k) != 0) continue;
            if (timeFit_module_calibrated->at(k) < 900 || timeFit_module_calibrated->at(k) > 1500) continue;
            if (height->at(k) < 15) continue;

            straightPathsHit[row->at(k)*4+column->at(k)][layer->at(k)] = true;

      }
    
      if (panelHit) continue;
      
      // Output tree if any path has 4 in a line hit
      bool straightLineEvent = false;
      for (int i=0; i<16; i++) {
            /*bool straightPath = true;
            for (int j=0; j<4; j++){
                  if (!straightPathsHit[i][j]) {
                        straightPath = false;
                        break;
                  }
            }*/
            int straightPathCount = 0;
            for (int j=0; j<4; j++){
                  if(straightPathsHit[i][j]){
                        straightPathCount++;
                        if(straightPathCount >= 3) break;
                  }
            }
            if(straightPathCount >= 3){
                  straightLineEvent = true;
                  break;
            }
      }

      if (straightLineEvent) {
	      tout->Fill();
	      passed = passed + 1;
      }
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
