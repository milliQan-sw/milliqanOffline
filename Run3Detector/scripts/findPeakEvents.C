#include "TFile.h"
#include "TH1.h"
#include "TKey.h"
#include "TROOT.h"
#include <iostream>
#include <sstream>

using namespace std;

int findPeakEvents() {
  TFile *inputFile = new TFile(
      "/home/ryan/Documents/Research/MilliQan/DataFiles/SPE_Run733.root",
      "read");
  TFile *outputFile = new TFile("peakedEventsRun733.root", "recreate");
  TIter keyList(inputFile->GetListOfKeys());
  TKey *key;
  int i = 0;
  while ((key = (TKey *)keyList())) {
    TClass *cl = gROOT->GetClass((key->GetClassName()));
    cout << key->GetClassName() << endl;
    if (!cl->InheritsFrom("TH1"))
      continue;
    TH1 *h = (TH1 *)key->ReadObj();
    if (h->GetMaximum() >= 3.5) {
      stringstream fileName;
      fileName << "hist_" << i;
      cout << fileName.str() << endl;
      TString name = fileName.str();
      outputFile->WriteObject(h, name);
    }
    cout << h->GetMaximum() << endl;
    i++;
  }
  outputFile->Close();
  inputFile->Close();
  return 0;
}
