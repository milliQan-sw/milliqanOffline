#include "myLooper.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "TChain.h"
#include "TFile.h"
#include <fstream>

void myLooper::Loop(TString outFile)
{
    // Ensure the input chain is valid
    if (fChain == 0) return;

    // Open the output ROOT file
    TFile* foutput = TFile::Open(outFile, "recreate");

    // Create an output tree by cloning the input tree structure
    TTree* tout = fChain->CloneTree(0);

    // Open a text file in append mode to log results
    std::ofstream outputTextFile("skim_results.txt", std::ios::app);

    // Minimum area threshold
    float minArea = 500000.;

    // Get the number of entries in the chain
    Long64_t nentries = fChain->GetEntriesFast();
    Long64_t passed = 0; // Counter for events passing the selection

    // Loop through each entry
    Long64_t nbytes = 0;
    for (Long64_t jentry = 0; jentry < nentries; jentry++) {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;

        // Load the current entry
        nbytes += fChain->GetEntry(jentry);

        // Provide progress updates to the user
        if (jentry % 1000 == 0) {
            std::cout << "Processing entry " << jentry << "/" << nentries << std::endl;
        }

        // Sanity check: Ensure `chan` and `area` vectors have the same size
        if (chan->size() != area->size()) {
            std::cerr << "Mismatch in sizes of chan and area vectors at entry " << jentry << std::endl;
            continue;
        }

        // Analyze the event
        int nSat = 0; // Number of saturated channels
        int nHitsByLayer[4] = {0, 0, 0, 0}; // Hit counts per layer

        // Loop over all channels in the event
        for (size_t k = 0; k < chan->size(); k++) {
            if (area->at(k) > minArea && type->at(k) == 0) {
                nSat++;
                nHitsByLayer[layer->at(k)]++;
            }
        }

        // Count the number of layers with hits
        int nLayersHit = 0;
        for (int k = 0; k < 4; k++) {
            if (nHitsByLayer[k] > 0) nLayersHit++;
        }

        // Save the event to the output tree if hits occurred in at least 3 layers
        if (nLayersHit >= 3) {
            tout->Fill();
            passed++;
        }
    }

    // Write the output tree to the file
    foutput->WriteTObject(tout);
    delete tout;
    foutput->Close();

    // Calculate and log the fraction of events that passed the selection
    float frac = static_cast<float>(passed) / nentries;
    outputTextFile << "Output file contains " << passed << " events" << std::endl;
    outputTextFile << "Input file contains " << nentries << " events" << std::endl;
    outputTextFile << std::fixed << std::setprecision(5)
                   << "Fraction of passed events: " << frac << std::endl
                   << std::endl;

    // Close the log file
    outputTextFile.close();
}