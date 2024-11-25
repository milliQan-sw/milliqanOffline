#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TString.h"
#include "TObject.h"
#include "TTimeStamp.h"
#include "MilliDAQ/interface/GlobalEvent.h"
#include "MilliDAQ/interface/V1743Event.h"
#include <iostream>

int globalEventConv(int fileNumber) {
    // Open the input file and retrieve the TTree
    TString fileName = Form("/data/bar_cosmic_sim_%d.root",fileNumber);
    TFile *inputFile = TFile::Open(fileName);
    TTree *inputTree = (TTree*)inputFile->Get("Events");

    // Define the waveform array to hold data from the tree
    float waveform[5][16][1024];

    // Set branch address to read waveform data
    inputTree->SetBranchAddress("waveform", waveform);

    TString outputFileName = Form("/data/bar_cosmic_sim_preprocessed_%d.root", fileNumber);
    // Create output file to save the GlobalEvent objects
    TFile *outputFile = new TFile(outputFileName, "RECREATE");

    TTree *outputTree = new TTree("Events", "GlobalEvents TTree");
    TTree *metadata = new TTree("Metadata", "Configuration");

    float secondsPerSample;
    int numChan;

    metadata->Branch("secondsPerSample", &secondsPerSample);
    metadata->Branch("numChan", &numChan);
    secondsPerSample = 2.5e-09;
    numChan = 80;
    metadata->Fill();
    // Create GlobalEvent object to store processed data
    mdaq::GlobalEvent *globalEvent = new mdaq::GlobalEvent();
    outputTree->Branch("event", &globalEvent);

    // Loop over all events in the input tree
    int nEntries = inputTree->GetEntries();
    for (int i = 0; i < nEntries; ++i) {
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
                TString histName = TString::Format("waveform_d%d_ch%d", d, ch);

                // Create a histogram for each waveform (1024 bins)
                TH1D *hist = new TH1D(histName, histName, 1024, 0, 1024);

                // Copy waveform data into digitizerEvent and fill the histogram
                for (unsigned int sample = 0; sample < 1024; ++sample) {
                    float sampleValue = waveform[d][ch][sample];
                    hist->SetBinContent(sample + 1, sampleValue);
                    digitizerEvent.waveform[ch][sample] = sampleValue; // Set the waveform data
                    if(sampleValue > 0) std::cout << sampleValue << std::endl;
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

    std::cout << "Conversion completed successfully!" << std::endl;

    return 0;
}

