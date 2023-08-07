#include <TFile.h>
#include <TH1D.h>
#include <TIterator.h>
#include <TKey.h>
#include <TList.h>
#include <iostream>

int plotWaveformExamples() {
  // Read waveforms and extra the extra info from root files.
  // The waveforms look like they were saved by event and when reading the files
  // they come in order.
  TFile *waveform_file = TFile::Open("/home/ryan/Documents/Research/MilliQan/"
                                     "Data/outputWaveforms_805_noLED.root",
                                     "READ");
  TFile *extra_file =
      TFile::Open("/home/ryan/Documents/Research/MilliQan/Data/");

  TList *keys = waveform_file->GetListOfKeys();
  TIterator *keyIter = keys->MakeIterator();
  TKey *key;

  while ((key = static_cast<TKey *>(keyIter->Next()))) {
    TObject *obj = key->ReadObj();

    // std::cout << key->GetClassName() << std::endl;
    if (obj->IsA() == TH1D::Class()) {
      TH1D *hist = dynamic_cast<TH1D *>(obj);
      std::cout << hist->GetName() << std::endl;
    }
  }
  return 0;
}
