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
#include <map>
#include <set>

using namespace std;

void myLooper::Loop(TString outFile) {
    // Ensure the input chain is valid
    if (fChain == 0) return;

    // Open the output ROOT file
    TFile* foutput = TFile::Open(outFile, "recreate");

    // Create an output tree by cloning the input tree structure
    TTree* tout = fChain->CloneTree(0);

    // Open a text file in append mode to log results
    ofstream outputTextFile("skim_results.txt", ios::app);

    // Minimum nPE threshold
    float minNPE = 90; 

    // Get the number of entries in the chain
    Long64_t nentries = fChain->GetEntriesFast();
    Long64_t passed = 0; // Counter for events passing the selection

    // Loop through each entry
    Long64_t nbytes = 0, nb = 0;
    for (Long64_t jentry = 0; jentry < nentries; jentry++) {
        Long64_t ientry = LoadTree(jentry);
        if (ientry < 0) break;

        // Load the current entry
        nb = fChain->GetEntry(jentry);
        nbytes += nb;

        // Provide progress updates to the user
        if (jentry % 1000 == 0) {
            cout << "Processing entry " << jentry << "/" << nentries << endl;
        }

        // Sanity check: Ensure `chan` and `nPE` vectors have the same size
        if (chan->size() != nPE->size()) {
            cerr << "Mismatch in sizes of chan and nPE vectors at entry " << jentry << endl;
            continue;
        }

        // Create a map to track hits by layer and row
        map<int, set<int>> hitsByLayerAndRow; // Maps layer to set of rows with hits

        // Process all channels in the event
        for (size_t k = 0; k < chan->size(); k++) {
            // Apply the selection criteria for valid hits
            if (nPE->at(k) > minNPE && type->at(k) == 0) { // Check nPE and type
                int layerID = layer->at(k);
                int rowID = row->at(k);
                hitsByLayerAndRow[layerID].insert(rowID);
            }
        }

        // Check if any layer has hits in more than 3 rows
        bool validEvent = false;
        for (const auto& layerHits : hitsByLayerAndRow) {
            if (layerHits.second.size() > 3) { // More than 3 rows hit in this layer
                validEvent = true;
                break;
            }
        }

        // Save the event to the output tree if it meets the criteria
        if (validEvent) {
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
    outputTextFile << "Output file has    " << passed    << " events" << endl;
    outputTextFile << "Input  file has    " << nentries  << " events" << endl;
    outputTextFile << fixed << setprecision(5) << "Fraction of passed " << frac << endl;
    outputTextFile << " " << endl;
    outputTextFile.close();
}