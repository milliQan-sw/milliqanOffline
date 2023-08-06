#include <TFile.h>
#include <TH1D.h>
#include <TIterator.h>
#include <TKey.h>
#include <TList.h>
#include <iostream>

int plotWaveformExamples() {
  TFile *waveform_file =
      TFile::Open("/home/ryan/Documents/Research/MilliQan/"
                  "DataFiles/MilliQan_Run853_b00_LED2p5_Waveforms.root",
                  "READ");
  if (!waveform_file || waveform_file->IsZombie()) {
    std::cerr << "Error: Could not open file" << std::endl;
    return 1;
  }
  TList *keys = waveform_file->GetListOfKeys();
  TIterator *keyIter = keys->MakeIterator();
  TKey *key;

  while ((key = static_cast<TKey *>(keyIter->Next()))) {
    TObject *obj = key->ReadObj();

    // std::cout << key->GetClassName() << std::endl;
    if (obj->IsA() == TH1D::Class()) {
      TH1D *hist = dynamic_cast<TH1D *>(obj);
      std::cout << "Found Histogram: " << hist->GetName() << std::endl;
    }
  }
  return 0;
}
