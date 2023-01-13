// Make milliqan validation plots. D. Stuart, Oct. 2017.

#include "mq3Hists.h"
#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TH3F.h"
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <vector>
#include <string>
#include "TString.h"
#include "TVector3.h"
using namespace std;


void tree1r(TChain *chain, int RunNum)
{

  TString filename = "outputPlots_Run" + std::to_string(RunNum) + ".root";
  std::cout << filename << std::endl;
  //TString filename = "outputPlots_Run494.root";
  TFile* myfile = new TFile(filename, "recreate");
  TH1F* h_pulseHeight_0 = new TH1F("h_pulseHeight_0", "Pulse Height for Channel 0", 100, 0, 100);
  TH2F* h_pulse_wh = new TH2F("h_pulse_wh", "Pulse Width and Height", 100, 0, 100, 100, 0, 300);
  TH2F* h_pulse_first = new TH2F("h_pulse_first", "First Pulse Width and Height", 100, 0, 100, 100, 0, 300);
  TH2F* h_pulse_after = new TH2F("h_pulse_after", "After Pulse Width and Height", 100, 0, 100, 100, 0, 300);

  TH2F* h_pulse[64][3];
  TH1F* h_shortPulseTime[64][4];
  TH2F* h_shortPulseCoincidence = new TH2F("h_shortPulseCoincidence", "Coincidence Between Channels for Short Pulses", chain->GetEntries(), 0, chain->GetEntries(), 64, 0, 64);
  TH1F* h_pulseTimeDiff = new TH1F("h_pulseTimeDiff", "Min Time Difference Between Short Pulses in Same Event", 3000, 0, 3000);
  TH1F* h_nEventPulses = new TH1F("h_nEventPulses", "Number of Pulses Per Event", 100, 0, 100);
  TH1F* h_singleChanPulse = new TH1F("h_singleChanPulse", "Number of Events with One Even Per Channel", 80, 0, 80);
  TH1F* h_singleDigiPulse = new TH1F("h_singleDigiPulse", "Number of Events with One Event Per Digitizer", 5, 0, 5);

  TH1F* h_test = new TH1F("h_test", "Test", 100, 0, 300);

  ofstream f_out;
  f_out.open("singlePulseList.txt");

  for(int i=0; i < 64; i++){
    TString h_name1 = "h_pulse_chan" + TString(i);
    TString h_title1 = Form("Pulses for Channel %i", i);
    TString h_name2 = h_name1 + TString("_first");
    TString h_title2 = Form("First Pulse for Channel %i", i);
    TString h_name3 = h_name1 + TString("_after");
    TString h_title3 = Form("After Pulse for Channel %i", i);
    h_pulse[i][0] = new TH2F(h_name1, h_title1, 100, 0, 100, 100, 0, 300);
    h_pulse[i][1] = new TH2F(h_name2, h_title2, 100, 0, 100, 100, 0, 300);
    h_pulse[i][2] = new TH2F(h_name3, h_title3, 100, 0, 100, 100, 0, 300);

    TString h_name4 = "h_shortPulseTime_all" + TString(i);
    TString h_title4 = Form("Pulse Times in Event With Short Pulse, Channel %i", i);
    TString h_name5 = "h_shortPulseTime_short" + TString(i);
    TString h_title5 = Form("Short Pulse Times, Channel %i", i);
    TString h_name6 = "h_shortPulseTime_long" + TString(i);
    TString h_title6 = Form("Long Pulse Times in Event With Short Pulse, Channel %i", i);

    h_shortPulseTime[i][0] = new TH1F(h_name4, h_title4, 300, 0, 3000);
    h_shortPulseTime[i][1] = new TH1F(h_name5, h_title5, 300, 0, 3000);
    h_shortPulseTime[i][2] = new TH1F(h_name6, h_title6, 300, 0, 3000);

  }

  TCanvas* c1 = new TCanvas("c1", "c1", 1200, 800);

  int plotLayer = 0;
  int plotCol = 0;
  int plotRow = 0;

  int pulseDuration = 30;
  int shortPulseCount = 0;

  int debug=0; // Debugging level. 0=none, 100=trace, 300=detailed trace
  float VThresholds[4][4][4][3]; // Threshold for pulse height for layer, row, column, type. Type=0,1,2 for SPE,cosmic,ThruMuon.
  float AThresholds[4][4][4][3]; // Threshold for pulse area for layer, row, column, type. Type=0,1,2 for SPE,cosmic,ThruMuon.
  float DThresholds[4][4][4][3]; // Threshold for pulse duration for layer, row, column, type. Type=0,1,2 for SPE,cosmic,ThruMuon.
  float NPEThresholds[4][4][4][3]; // Threshold for pulse NPE for layer, row, column, type. Type=0,1,2 for SPE,cosmic,ThruMuon.
  for (int ilay=0;ilay<4;ilay++)
    for (int irow=0;irow<4;irow++)
      for (int icol=0;icol<4;icol++) {
	//cout << "Thr"<<ilay<<":"<<irow<<":"<<icol<<"\n"; cout.flush();
        VThresholds[ilay][irow][icol][0] = 15.; // SPE
        AThresholds[ilay][irow][icol][0] = 1.;
        DThresholds[ilay][irow][icol][0] = 10.;
        NPEThresholds[ilay][irow][icol][0] = 0.2;
        VThresholds[ilay][irow][icol][1] = 1200.; // Cosmic
        AThresholds[ilay][irow][icol][1] = 100.;
        DThresholds[ilay][irow][icol][1] = 100.;
        NPEThresholds[ilay][irow][icol][1] = 20.;
        VThresholds[ilay][irow][icol][2] = 1200.; // ThruMuon
        AThresholds[ilay][irow][icol][2] = 200.;
        DThresholds[ilay][irow][icol][2] = 200.;
        NPEThresholds[ilay][irow][icol][2] = 40.;
      }

  // Dump contents to a text file
  int firstEvt = 0; int lastEvt = 0;
  int maxFile = 0;

  //Main Event loop
  InitializeChain(chain);
  Int_t nentries = (Int_t)chain->GetEntries();
  for(int ia = 0; ia<nentries; ia++) {

    //Bool to track if there was a short pulse in event
    bool shortPulse[64]= {false};
    vector<float> v_shortPulseTime;
    vector<float> v_shortPulseDuration;
    bool realPulses = false;
    bool passedCuts = false;

    if (debug>=100 || (ia%1000 == 0)) {cout << "Entry #"<<ia<<"\n"; cout.flush();}
    chain->GetEntry(ia);

    //Check if there is only one pulse in event


    if(chan->size()==1 && boardsMatched){
      h_singleDigiPulse->Fill(board->at(0));
      cout << TString(Form("1 pulse in event %i, board %i, file %i, event %i", ia, board->at(0), fileNum, eventNum)) << endl;
      h_singleChanPulse->Fill(chan->at(0));
      f_out << TString(Form("%i %i \n", (void*)fileNum, (void*)eventNum));
    }

    if(chan->size()==0){
      cout << "Problem in event " << ia << "No pulses!" << endl;
    }

    h_nEventPulses->Fill(npulses->size());



    // Build a map of hits above thresholds appropriate for the passed event category, and record the pulse number; consider only the first pulse in each channel.
    //if (debug>=100) {cout << "Building hit map.\n";cout.flush();}
    bool HitChan[4][4][4][3]; // Simple flag showing existence of any hit in layer, row, column
    int ChanHitIndex[4][4][4][3]; // Index to the pulse with the hit
    int nHits=0; // Number of channels with hits
    for (int ilay=0; ilay<4; ilay++){
      for (int irow=0; irow<4; irow++){
        for (int icol=0; icol<4; icol++){
          for (int itype=0; itype<3; itype++) { // 0=SPE,1=cosmic,2=ThruMuon
            ChanHitIndex[ilay][irow][icol][itype] = -1; // No hit
            HitChan[ilay][irow][icol][itype] = false;
            //cout << "Hit"<<ilay<<":"<<irow<<":"<<icol<<" "<<chan->size()<<"\n"; cout.flush();
            for (int i=0; i<int(chan->size()); i++) { // Pulse loop 
              if ((chan->at(i) >= 0) && 
                  (layer->at(i) == ilay) &&
                  (row->at(i) == irow) &&
                  (column->at(i) == icol) ) { // Valid bar 
                
                if ((duration->at(i) >= DThresholds[ilay][irow][icol][itype]) &&
                    (height->at(i) >= VThresholds[ilay][irow][icol][itype]) &&
                    (area->at(i) >= AThresholds[ilay][irow][icol][itype]) &&
                    (nPE->at(i) >= NPEThresholds[ilay][irow][icol][itype]) ) {
                  if(itype==0){

                    if (duration->at(i) < pulseDuration) {
                      shortPulse[chan->at(i)] = true;
                      h_shortPulseCoincidence->Fill(ia, chan->at(i));
                      v_shortPulseTime.push_back(ptime->at(i));
                      v_shortPulseDuration.push_back(duration->at(i));
                    }
                    else realPulses=true;
                    if (shortPulse[chan->at(i)]) {
                      h_shortPulseTime[chan->at(i)][0]->Fill(ptime->at(i));
                      if(duration->at(i) < pulseDuration) h_shortPulseTime[chan->at(i)][1]->Fill(ptime->at(i));
                      else h_shortPulseTime[chan->at(i)][2]->Fill(ptime->at(i));
                    }
                    h_pulse[chan->at(i)][0]->Fill(height->at(i), duration->at(i));
                    if(!HitChan[ilay][irow][icol][itype]) h_pulse[chan->at(i)][1]->Fill(height->at(i), duration->at(i));
                    else h_pulse[chan->at(i)][2]->Fill(height->at(i), duration->at(i));
                  }
                  HitChan[ilay][irow][icol][itype] = true;
                  ChanHitIndex[ilay][irow][icol][itype] = i;
                  //h_pulseHeight_0->Fill(height->at(i));
                  //std::cout << "Event: " << ia << ", pulse: " << i <<", height: " << height->at(i) <<", width: " << duration->at(i) <<", ptime: " << ptime->at(i) <<std::endl;
                } //check thresholds
              } //check good bar
            } //loop over channels
          } //loop over types
        } //loop over columns
      } // loop over rows
    } // loop over layers

    //cout << "Checking bar hits\n"; cout.flush();
    // Count the number of bars with hits of each type
    int nBarsHit[3];
    for (int itype=0; itype<3; itype++) { // 0=SPE,1=cosmic,2=ThruMuon
     nBarsHit[itype] = 0;
     for (int ilay=0; ilay<4; ilay++)
      for (int irow=0; irow<4; irow++)
       for (int icol=0; icol<4; icol++) {
        if (HitChan[ilay][irow][icol][itype])
          nBarsHit[itype]++;
      }
    }

    // Determine the number of hits of each type in each layer
    int nHitsPerLayer[4][3];
    for (int itype=0; itype<3; itype++)
     for (int ilay=0; ilay<4; ilay++) {
      nHitsPerLayer[ilay][itype] = 0;
      for (int irow=0; irow<4; irow++)
       for (int icol=0; icol<4; icol++)
        if (HitChan[ilay][irow][icol][itype])
          nHitsPerLayer[ilay][itype]++;
    }

    // Plot time difference between short pulses
    if(v_shortPulseTime.size() > 1){
      for(int p1=0; p1 < v_shortPulseTime.size(); p1++){
        //cout << v_shortPulseTime[p1] << ", ";
        float minTime = 10e6;
        for(int p2=0; p2 < v_shortPulseTime.size(); p2++){
          if(p1==p2) continue;
          if(abs(v_shortPulseTime[p1]-v_shortPulseTime[p2]) < minTime) minTime = abs(v_shortPulseTime[p1]-v_shortPulseTime[p2]);
        }
        h_pulseTimeDiff->Fill(minTime);
      }
      //cout << endl;
    }

    for(int p=0; p < v_shortPulseDuration.size(); p++){
      if(ia==1005) {
        h_test->Fill(v_shortPulseDuration[p]);
      }
    }

    if(!realPulses && v_shortPulseTime.size() > 0) cout << A_BRIGHT_RED << TString(Form("Only found short pulses in event %i, file %i! Number of pulses %zu, and max duration %f", eventNum, fileNum, v_shortPulseDuration.size(), *max_element(v_shortPulseDuration.begin(), v_shortPulseDuration.end()))) << A_RESET << endl;
    if(!realPulses && v_shortPulseTime.size() > 0) shortPulseCount++;


  } //Main event loop

  c1->cd();
  c1->Divide(2, 2);
  c1->cd(1);
  std::cout << "Number of entries in 0: " << h_pulse[0][0]->GetEntries() << ", number of entries in 1: " << h_pulse[0][1]->GetEntries() << std::endl;
  h_pulse[0][0]->GetXaxis()->SetTitle("Height (mV)");
  h_pulse[0][0]->GetYaxis()->SetTitle("Width (ns)");
  h_pulse[0][0]->Draw("colz");
  c1->cd(2);
  h_pulse[0][1]->GetXaxis()->SetTitle("Height (mV)");
  h_pulse[0][1]->GetYaxis()->SetTitle("Width (ns)");
  h_pulse[0][1]->Draw("colz");
  c1->cd(3);
  h_pulse[0][2]->GetXaxis()->SetTitle("Height (mV)");
  h_pulse[0][2]->GetYaxis()->SetTitle("Width (ns)");
  h_pulse[0][2]->Draw("colz");

  myfile->cd();
  myfile->mkdir("channelPulses/");
  myfile->cd("channelPulses/");
  for(int i=0; i < 64; i++){
    h_pulse[i][0]->Write();
    h_pulse[i][1]->Write();
    h_pulse[i][2]->Write();
    h_shortPulseTime[i][0]->Write();
    h_shortPulseTime[i][1]->Write();
    h_shortPulseTime[i][2]->Write();
  }
  myfile->cd("../");
  h_shortPulseCoincidence->Write();
  h_pulseTimeDiff->Write();
  h_nEventPulses->Write();
  h_singleChanPulse->Write();
  h_singleDigiPulse->Write();
  
  cout << TString(Form("Number of events with one pulse: %i", (int)h_singleChanPulse->GetEntries())) << endl;

  myfile->Close();
  f_out.close();

  cout << "Number of event with all pulse durations < " << pulseDuration << ", " << shortPulseCount << endl;



}

void mq3Hists(){


  TChain* mychain = new TChain("t");
  //mychain->Add("/store/users/mcarrigan/trees/MilliQan_Run494.*_v23_firstPedestals.root");
  mychain->Add("/store/user/mcarrigan/trees/MilliQan_Run552.*_v24_firstPedestals.root");
  //mychain->Add("/store/user/mcarrigan/milliqan/test/trees/hist_589.root");

  std::cout << "Number of events: " << mychain->GetEntries() << std::endl;

  tree1r(mychain, 552);

  return 0;

}
