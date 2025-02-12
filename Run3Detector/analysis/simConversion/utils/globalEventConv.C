#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TString.h"
#include "TObject.h"
#include "TTimeStamp.h"
#include "MilliDAQ/interface/GlobalEvent.h"
#include "MilliDAQ/interface/V1743Event.h"
#include <iostream>

R__ADD_LIBRARY_PATH(/home/rsantos/scratch0/MilliQan/CMSSW_13_0_13/src/MilliDAQ) // if needed
R__LOAD_LIBRARY(libMilliDAQ.so)

int globalEventConv() {
    bool isSlab = false;
    // open the input file and retrieve the ttree
    gSystem->Load("/home/rsantos/scratch0/MilliQan/CMSSW_13_0_13/src/MilliDAQ/libMilliDAQ.so");
    TString fileName = "/data/MilliQan_cosmicSimSample_waveinjected_v4.root";
    TFile *inputFile = TFile::Open(fileName);
    if (!inputFile){
        std::clog << "Input file does not exist!" << std::endl;
        return 1;
    }
    TTree *inputTree = (TTree*)inputFile->Get("Events");

    std::cout << "Trying to process " << inputFileName << ", into " << outputFileName << std::endl;

    // Define the waveform array to hold data from the tree
    float waveform[5][16][1024];
    Double_t eventWeight =-1;

    // Set branch address to read waveform data
    inputTree->SetBranchAddress("waveform", waveform);
    inputTree->SetBranchAddress("eventWeight", &eventWeight);

    TString outputFileName = "/data/bar_cosmic_sim_preprocessed_v4.root";
    // Create output file to save the GlobalEvent objects
    TFile *outputFile = new TFile(outputFileName, "RECREATE");

    TTree *outputTree = new TTree("Events", "GlobalEvents TTree");
    TTree *metadata = new TTree("Metadata", "Configuration");

    float secondsPerSample;
    int numChan;

    metadata->Branch("secondsPerSample", &secondsPerSample);
    metadata->Branch("numChan", &numChan);
    secondsPerSample = 2.5e-09;

    if (!isSlab){
        numChan = 80;
    }
    else {
      numChan = 96;
    }

    metadata->Fill();
    // Create GlobalEvent object to store processed data
    mdaq::GlobalEvent *globalEvent = new mdaq::GlobalEvent();
    outputTree->Branch("event", &globalEvent);
    outputTree->Branch("eventWeight", &eventWeight);

    // Loop over all events in the input tree
    int nEntries = inputTree->GetEntries();

    for (int i = 0; i < nEntries; ++i) {
      if ( nEntries % 1000 == 0 ){std::clog << "Processing event " << i << std::endl;}
        inputTree->GetEntry(i);

        // Reset the globalEvent for each new event
        globalEvent->Reset();

        // Set the event number
        globalEvent->SetEventNumber(i);

        // Loop through digitizers and channels
        for (unsigned int d = 0; d < 5; ++d) {
            mdaq::V1743Event &digitizerEvent = globalEvent->digitizers[d];
            digitizerEvent.nanosecondsPerSample = 2.5;

            for (unsigned int ch = 0; ch < 16; ++ch) {
              //TString histName = TString::Format("waveform_d%d_ch%d", d, ch);

                // Create a histogram for each waveform (1024 bins)
              // TH1D *hist = new TH1D(histName, histName, 1024, 0, 1024);

                // Copy waveform data into digitizerEvent and fill the histogram
                for (unsigned int sample = 0; sample < 1024; ++sample) {
                    float sampleValue = waveform[d][ch][sample];
                    //     hist->SetBinContent(sample + 1, sampleValue);
                    digitizerEvent.waveform[ch][sample] = sampleValue; // Set the waveform data
                    //if(sampleValue > 0) std::cout << sampleValue << std::endl;
                }

                // Optionally, you can avoid calling GetWaveform if not needed
                // If you need to update the histogram from digitizerEvent, ensure waveform data is set
                // digitizerEvent.GetWaveform(ch, hist);
            }
        }

        // Fill the output tree with the processed GlobalEvent
        outputTree->Fill();

    }

    // Write the output tree to the file
    outputTree->Write();
    metadata->Write();

    inputFile->Close();
    outputFile->Close();
      

    std::cout << "Conversion completed successfully!" << std::endl;

    return 0;
}

