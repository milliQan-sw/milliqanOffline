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

  // The output tree (possibly pruned)
  // If you need to prune branches, disable the input branch first (part 1)...
  // ch.SetBranchStatus("[branch name]", 0);
  TTree* tout = fChain->CloneTree(0);

  // A text file opened in "append" mode, where we store the number of events
  std::ofstream outputTextFile("skim_results.txt", std::ios::app);

  // The minimum area requirement
  float minArea = 300000.;

   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t passed = 0;

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

      //      std::cout <<  event << " " << runNumber << std::endl;
      // if (jentry > 10) break;

      // Some feedback to the user
      if ( (jentry % 1000) == 0 ) {
	std::cout << "Processing " << jentry << "/" << nentries << std::endl;
      }

      // Sanity Check:
      if (chan->size() != area->size()) {
	std::cout << "Different sizes" << endl;
      }

      // Loop over areas, count the ones over the cut. 
      // Also: count layers hit
      int nSat=0;
      int nHitsByLayer[4] = {0, 0, 0, 0};
      for (unsigned long k=0; k<chan->size(); k++) {
	if (area->at(k) > minArea && type->at(k)==0) {
	  // std::cout << "here" << std::endl;
	  // std::cout << event << " " << area->at(k) << " " << layer->at(k) << std::endl;
	  nSat++;
	  nHitsByLayer[layer->at(k)]++;
	}
      }
    
      // Output tree if at least 3 layers hit
      int nL = 0;
      for (int k=0; k<3; k++) {
	if (nHitsByLayer[k] > 0) nL++;
      }
      if (nL > 2) {
	tout->Fill();
	passed = passed + 1;
      }


   }


  // Write the root file out
    foutput->WriteTObject(tout);
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
