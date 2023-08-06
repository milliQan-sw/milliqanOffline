/*
Original Author: Ryan De Los Santos
Email: delossantos.22@osu.edu

Description: This file is used to create a root file for the SPE calibration.
This will take in the raw root data file from MilliDAQ and will convert it to a
root file with a voltages branch and a time branch which is expected by the
pmt-calibration code.
 */

#include "../../../../../MilliDAQ/interface/GlobalEvent.h"
#include <TChain.h>
#include <TFile.h>
#include <TH1.h>
#include <TString.h>
#include <TTree.h>
#include <iostream>
#include <string>

using namespace std;

const int MaxSamples = 1024;            // This is what was set in MilliDAQ
const float nanosecondsPerSample = 2.5; // This value can be read from ROOT file
int SPECalibration() {
  // Read in dataFile
  TString dataDirectory = "/home/ryan/Documents/Research/MilliQan/DataFiles/";
  TChain chain("Events");
  chain.Add(dataDirectory + "MilliQan_Run733.*_default.root");

  unique_ptr<TFile> outputFile(
      TFile::Open("./ProcessedData/MilliQan_Run732.merged_SPE.root",
                  "RECREATE")); // Change Here

  mdaq::GlobalEvent *evt = new mdaq::GlobalEvent();
  chain.SetBranchAddress("event", &evt);

  int numEntries = chain.GetEntries();
  cout << numEntries << endl;
  float voltage = 0;
  float time = 0;

  TTree *output_tree = new TTree("Events", "Events");

  vector<float> voltage_vector = {};
  vector<float> time_vector = {};

  output_tree->Branch("voltages", &voltage_vector);
  output_tree->Branch("times", &time_vector);

  for (int i = 0; i < numEntries; i++) {
    voltage_vector.clear();
    time_vector.clear();
    chain.GetEntry(i); // Initialize event and get new set of variables
    for (int j = 0; j <= MaxSamples; j++) {
      voltage = evt->digitizers[0]
                    .waveform[4][j]; // We used digitizer 0 and channel 4
      cout << voltage << endl;
      if (voltage > 10) {
        std::cout << "Found high voltage value at entry" << i << std::endl;
      }
      voltage_vector.push_back(voltage);
      time_vector.push_back(nanosecondsPerSample * j);
    }
    assert(voltage_vector.size() == time_vector.size());
    output_tree->Fill();
  }
  output_tree->Write();

  outputFile->Close();

  cout << "Finished" << endl;

  return 0;
}
