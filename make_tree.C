#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip> // for setw()

#include "TSystem.h"
#include "TROOT.h"
#include "TF1.h"
#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TMath.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TDirectory.h"
#include "TBranch.h"
#include "TString.h"
#include "TStyle.h"
#include "TPaveStats.h"
#include "TLatex.h"
#include "TSystemDirectory.h"
#include "TSystemFile.h"
#include "TGaxis.h"


#include <string>

#ifdef __MAKECINT__
#pragma link C++ class std::vector < std::vector<int> >+;
#pragma link C++ class std::vector < std::vector<float> >+;
#endif

using namespace std;


//Configurable parameters
int numChan=16;
int maxEvents=-1; 
int sideband_range[2] = {0,50}; //in ns
float sample_rate = 0.8;
bool debug=false;

vector<TString> tubeSpecies = {"ET","ET","ET","ET",             // 0 1 2 3 
							   "R878","R878","R878","ET",       // 4 5 6 7	
							   "R7725","R7725","R7725","R7725",	// 8 9 10 11
							   "R878","R878","R878","R878"};    // 12 13 14 15



//Declare global variables
vector<TH1D*> waves;
TTree * inTree;
TTree * outTree;
int event = 0;
vector<int> * v_npulses;
vector<int> * v_ipulse;
vector<int> * v_chan;
vector<float> * v_height;
vector<float> * v_time;
vector<float> * v_area;
vector<float> * v_duration;
vector<float> * v_sideband_mean;
vector<float> * v_sideband_RMS;




void loadBranches();
void prepareOutBranches();
void clearOutBranches();
void processChannel(int ic);
void prepareWave(int ic, float &sb_mean, float &sb_RMS);
vector< vector<float> > findPulses(int ic);
vector< vector<float> > findPulses_inside_out(int ic);
void displayPulse(int ic, float begin, float end, int ipulse);
void displayEvent(int ic, vector<vector<float> > bounds);
void h1cosmetic(TH1D* hist);

vector<int> eventsPrinted(16,0);
TString displayDirectory;

void make_tree(TString runNum){
	TString inFileName = "Run"+runNum+".root";
	TFile *f = TFile::Open(inFileName, "READ");
	inTree = (TTree*)f->Get("data"); 
	if(maxEvents<0) maxEvents=inTree->GetEntries();
	cout<<"Entries: "<<inTree->GetEntries()<<endl;
	if((int)tubeSpecies.size()!=numChan) cout<<"Tube species map does not match number of channels"<<endl;
	loadBranches();	

	TString outFileName = inFileName.ReplaceAll(".root","_output.root");
	TFile * outFile = new TFile(outFileName,"recreate");

	displayDirectory = "displays/Run"+runNum+"/";
	gSystem->mkdir(displayDirectory);

	outTree = new TTree("t","t");

	prepareOutBranches();

	cout<<"Starting event loop"<<endl;
	cout<<"Length of waves: "<<waves.size()<<endl;

	for(int i=0;i<maxEvents;i++){
		if(i%1000==0) cout<<"Processing event "<<i<<endl;
		inTree->GetEntry(i);
		clearOutBranches();
		event=i;

		for(int ic=0;ic<numChan;ic++){
		//	cout<<Form("Chan %i min: ",ic)<<waves[ic]->GetMinimum()<<endl;
			processChannel(ic);		
		}

		outTree->Fill();
	}

	outTree->Write();
	outFile->Close();
}


void convertXaxis(TH1D *h){
	TAxis * a = h->GetXaxis();
	a->Set( a->GetNbins(), a->GetXmin()/sample_rate, a->GetXmax()/sample_rate );
	h->ResetStats();
}

void prepareWave(int ic, float &sb_mean, float &sb_RMS){
	//Invert waveform and convert x-axis to ns
	waves[ic]->Scale(-1.0);
	convertXaxis(waves[ic]);

	//Subtract sideband. Return sideband mean and RMS
	float sum_sb=0.;
	float sum2_sb=0.;
	int start = waves[ic]->FindBin(sideband_range[0]);
	int end = waves[ic]->FindBin(sideband_range[1]);
	int n_sb = end-start+1;
	for(int ibin=start; ibin <= end; ibin++){
		sum_sb = sum_sb + waves[ic]->GetBinContent(ibin);
		sum2_sb = sum2_sb + pow(waves[ic]->GetBinContent(ibin),2);
		n_sb++;
	}
	if(n_sb == 0) n_sb = 1.;
	sb_mean = sum_sb/n_sb;
	sb_RMS =pow( sum2_sb/n_sb - pow(sb_mean,2), 0.5);

	for(int ibin = 1; ibin <= waves[ic]->GetNbinsX(); ibin++){
		waves[ic]->SetBinContent(ibin,waves[ic]->GetBinContent(ibin)-sb_mean);
	}
}
	

void processChannel(int ic){
	float sb_mean, sb_RMS;
	prepareWave(ic, sb_mean, sb_RMS);

	vector<vector<float> > pulseBounds;
	if(tubeSpecies[ic]!="ET") pulseBounds = findPulses(ic);
	else pulseBounds = findPulses_inside_out(ic); //Use inside-out method for narrow ET pulses

	int npulses = pulseBounds.size();
	for(int ipulse = 0; ipulse<npulses; ipulse++){
		//Set waveform range to this pulse
		waves[ic]->SetAxisRange(pulseBounds[ipulse][0],pulseBounds[ipulse][1]);
		if(debug) cout<<"Chan "<<ic<<", pulse bounds: "<<pulseBounds[ipulse][0]<<" to "<<pulseBounds[ipulse][1]<<endl;
		//Fill branches
		v_chan->push_back(ic);
		v_height->push_back(waves[ic]->GetMaximum());
		v_time->push_back(pulseBounds[ipulse][0]);
		v_area->push_back(waves[ic]->Integral());
		v_ipulse->push_back(ipulse);
		v_npulses->push_back(npulses);
		v_duration->push_back(pulseBounds[ipulse][1] - pulseBounds[ipulse][0]);
		v_sideband_mean->push_back(sb_mean);
		v_sideband_RMS->push_back(sb_RMS);	


		if(event<20 || eventsPrinted[ic]<10) displayPulse(ic,pulseBounds[ipulse][0],pulseBounds[ipulse][1],ipulse);
	}
	if(event<10 || (event<20 && npulses>0) || eventsPrinted[ic]<10) {displayEvent(ic,pulseBounds); eventsPrinted[ic]++;}
}

void displayPulse(int ic, float begin, float end, int ipulse){
	//This must be called inside the pulse loop, after branches are filled,
	// since it displays the last value of each branch as a sanity check.

	TCanvas c;
	gStyle->SetGridStyle(3);
	gStyle->SetGridColor(13);
	c.SetGrid();

	waves[ic]->SetAxisRange(begin-130,end+130);
	waves[ic]->SetLineWidth(2);
	waves[ic]->SetTitle(Form("Zoom on event %i, channel %i, pulse %i (%s);Time [ns];Amplitude [mV];",event,ic,ipulse,tubeSpecies[ic].Data()));
	h1cosmetic(waves[ic]);	
	waves[ic]->Draw("hist");



	//Show boundaries of pulse
	TLine line; line.SetLineColor(1); line.SetLineWidth(4); line.SetLineStyle(7);	
	line.DrawLine(begin,0,begin,0.4*waves[ic]->GetMaximum());
	line.DrawLine(end,0,end,0.4*waves[ic]->GetMaximum());

	//Display values stored for this pulse
	TLatex tla;
	tla.SetTextSize(0.045);
	tla.SetTextFont(42);
	tla.DrawLatexNDC(0.13,0.83,Form("Height: %0.2f mV",v_height->back()));
	tla.DrawLatexNDC(0.13,0.78,Form("Area: %0.2f nVs",v_area->back()));
	tla.DrawLatexNDC(0.13,0.73,Form("Duration: %0.2f ns",v_duration->back()));

	c.Print(displayDirectory+Form("Event%i_Chan%i_begin%0.0f.pdf",event,ic,begin));
}

void displayEvent(int ic, vector<vector<float> > bounds){
	TCanvas c;
	gStyle->SetGridStyle(3);
	gStyle->SetGridColor(13);
	c.SetGrid();

	waves[ic]->SetAxisRange(0,1024./sample_rate);
	waves[ic]->SetLineWidth(2);
	waves[ic]->SetMaximum(100.);
	waves[ic]->SetTitle(Form("Event %i, channel %i (%s);Time [ns];Amplitude [mV];",event,ic,tubeSpecies[ic].Data()));

	h1cosmetic(waves[ic]);
	waves[ic]->Draw("hist");


	//Show boundaries of pulse
	TLine line; line.SetLineWidth(4); line.SetLineStyle(7);	
	for(uint ip=0; ip<bounds.size();ip++){
		line.SetLineColor(kGreen-3);
		line.DrawLine(bounds[ip][0],0,bounds[ip][0],0.4*waves[ic]->GetMaximum());
		line.SetLineColor(kRed-4);
		line.DrawLine(bounds[ip][1],0,bounds[ip][1],0.4*waves[ic]->GetMaximum());
	}
	//Display values stored for this pulse
	 TLatex tla;
	tla.SetTextSize(0.045);
	tla.SetTextFont(42);
	tla.DrawLatexNDC(0.13,0.83,Form("Number of pulses: %i",(int)bounds.size()));
	// tla.DrawLatexNDC(0.13,0.78,Form("Area: %0.2f",v_area->back()));
	// tla.DrawLatexNDC(0.13,0.73,Form("Duration: %0.2f",v_duration->back()));

	c.Print(Form(displayDirectory+"Full_Event%i_Chan%i_npulses%i.pdf",event,ic,(int)bounds.size()));
}

vector< vector<float> > findPulses(int ic){
	//Configurable:
	int Nconsec = 3;
	int NconsecEnd = 3;
	float thresh = 5; //mV

	vector<vector<float> > bounds;
	float tstart = sideband_range[1]+1;
	int istart = waves[ic]->FindBin(tstart);

	// Now hunt for pulses
	bool inpulse = false;
	int nover = 0; // Number of samples seen consecutively over threshold
	int nunder = 0; // Number of samples seen consecutively under threshold
	int i_begin = istart;

	// int tWindow[2];
	for (int i=istart; i<waves[ic]->GetNbinsX()-Nconsec; i++) { // Loop over all samples looking for pulses
	  float v = waves[ic]->GetBinContent(i);
		if (!inpulse) { // Not in a pulse?
			if (v<thresh) {
				// Reset any prepulse counters
				nover = 0;
				i_begin = i; // most recent sample below threshold
			}
			else{		
				nover++; // Another sample over threshold
				//cout << "DEBUG: Over pulse, t = "<< w.t[i] <<", v = "<<v<<", nover = "<<nover<<endl;
			}

			if (nover>Nconsec) {
				//cout << "DEBUG: Starting pulse, t = "<< w.t[i] <<", v = "<<v<<endl;
				inpulse = true; // Start a pulse
				nunder = 0; // Counts number of samples underthreshold to end a pulse
			}
		} // Not in a pulse?
		else { // In a pulse?
			if (v<thresh) nunder++;
			else{
				//nover++;
				nunder = 0;
			}
			//cout << "DEBUG: Inside pulse, t = "<< w.t[i] <<", v = "<<v<<", nunder = "<<nunder<<endl;
			if (nunder>NconsecEnd) { // The end of a pulse
				// Record the pulse window
				// tWindow[0] = waves[ic]->GetBinCenter(i_begin);
				// tWindow[1] = waves[ic]->GetBinCenter(i);
			 
				//cout<<"DEBUG: i_begin "<<i_begin<<endl;
				// cout<<"DEBUG: tWindow 0 and 1: "<<w.t[i_begin]<<" "<<w.t[i]<<endl;

				bounds.push_back({(float)waves[ic]->GetBinLowEdge(i_begin+1), (float)waves[ic]->GetBinLowEdge(i+1)}); //start and end of pulse
				if(debug) cout<<"i_begin, i: "<<i_begin<<" "<<i<<endl;
				// tWindow[0]=0; tWindow[1]=0;
		    	inpulse = false; // End the pulse
	      		nover = 0;
	      		nunder = 0;
	      		i_begin = i;
			}
	 	}
	}
	return bounds;
}

vector< vector<float> > findPulses_inside_out(int ic){

	//Configurable
	float thresh = 7; //mV. Threshold to identify a pulse
	float thresh_noise = 3.5; //mV. Threshold to end a pulse


	vector<vector<float> > bounds;
	float tstart = sideband_range[1]+1;
	int istart = waves[ic]->FindBin(tstart);
	
	int i_begin, i_end;

	for (int i=istart; i<waves[ic]->GetNbinsX(); i++) { // Loop over all samples looking for pulses
		float v = waves[ic]->GetBinContent(i);
	  	if(v>thresh){
	  		//Add a pulse, adding bins on either side starting from i
	  		i_begin=i;
	  		i_end=i;

	  		//loop to find last previous sample beneath noise threshold
	  		while(v>thresh_noise && i_begin>0){
	  			i_begin--;
	  			v = waves[ic]->GetBinContent(i_begin);
	  		}
	  		i_begin++; //start pulse at first sample ABOVE threshold.

	  		//loop to find next sample beneath noise threshold
	  		v = waves[ic]->GetBinContent(i);
	  		while(v>thresh_noise && i_end<=waves[ic]->GetNbinsX()){
	  			i_end++;
	  			v = waves[ic]->GetBinContent(i_end);
	  		}
	  		i_end--; //end pulse at last sample ABOVE threshold.

	  		i=i_end+1; //Start where we left off next time

	  		bounds.push_back({(float)waves[ic]->GetBinLowEdge(i_begin), (float)waves[ic]->GetBinLowEdge(i_end+1)});
	  	}
	}

	return bounds;
}

void prepareOutBranches(){

	TBranch * b_event = outTree->Branch("event",&event,"event/I");
	TBranch * b_chan = outTree->Branch("chan",&v_chan);
	TBranch * b_height = outTree->Branch("height",&v_height);
	TBranch * b_time = outTree->Branch("time",&v_time);
	TBranch * b_area = outTree->Branch("area",&v_area);
	TBranch * b_ipulse = outTree->Branch("ipulse",&v_ipulse);
	TBranch * b_npulses = outTree->Branch("npulses",&v_npulses);
	TBranch * b_duration = outTree->Branch("duration",&v_duration);
	TBranch * b_sideband_mean = outTree->Branch("sideband_mean",&v_sideband_mean);
	TBranch * b_sideband_RMS = outTree->Branch("sideband_RMS",&v_sideband_RMS);

	outTree->SetBranchAddress("event",&event,&b_event);
	outTree->SetBranchAddress("chan",&v_chan,&b_chan);
	outTree->SetBranchAddress("height",&v_height,&b_height);
	outTree->SetBranchAddress("time",&v_time,&b_time);
	outTree->SetBranchAddress("area",&v_area,&b_area);
	outTree->SetBranchAddress("ipulse",&v_ipulse,&b_ipulse);
	outTree->SetBranchAddress("npulses",&v_npulses,&b_npulses);
	outTree->SetBranchAddress("duration",&v_duration,&b_duration);
	outTree->SetBranchAddress("sideband_mean",&v_sideband_mean,&b_sideband_mean);
	outTree->SetBranchAddress("sideband_RMS",&v_sideband_RMS,&b_sideband_RMS);

}

void clearOutBranches(){
	v_chan->clear();
	v_height->clear();
	v_time->clear();
	v_area->clear();
	v_ipulse->clear();
	v_npulses->clear();
	v_duration->clear();
	v_sideband_mean->clear();
	v_sideband_RMS->clear();
}


void h1cosmetic(TH1D *hist){
   
  hist->GetXaxis()->SetTitleSize(0.045);
  hist->GetXaxis()->SetLabelSize(0.04);
  hist->GetYaxis()->SetTitleSize(0.045);
  hist->GetYaxis()->SetLabelSize(0.04);
  hist->GetYaxis()->SetTitleOffset(1.01);
  hist->GetXaxis()->SetTitleOffset(0.96);

}


void loadBranches(){
	for(int ic=0;ic<numChan;ic++) waves.push_back(new TH1D());

	auto branch0 = inTree->GetBranch("channel_0");
	auto branch1 = inTree->GetBranch("channel_1");
	auto branch2 = inTree->GetBranch("channel_2");
	auto branch3 = inTree->GetBranch("channel_3");
	auto branch4 = inTree->GetBranch("channel_4");
	auto branch5 = inTree->GetBranch("channel_5");
	auto branch6 = inTree->GetBranch("channel_6");
	auto branch7 = inTree->GetBranch("channel_7");
	auto branch8 = inTree->GetBranch("channel_8");
	auto branch9 = inTree->GetBranch("channel_9");
	auto branch10 = inTree->GetBranch("channel_10");
	auto branch11 = inTree->GetBranch("channel_11");
	auto branch12 = inTree->GetBranch("channel_12");
	auto branch13 = inTree->GetBranch("channel_13");
	auto branch14 = inTree->GetBranch("channel_14");
	auto branch15 = inTree->GetBranch("channel_15");

	branch0->SetAddress(&(waves[0]));
	branch1->SetAddress(&(waves[1]));
	branch2->SetAddress(&(waves[2]));
	branch3->SetAddress(&(waves[3]));
	branch4->SetAddress(&(waves[4]));
	branch5->SetAddress(&(waves[5]));
	branch6->SetAddress(&(waves[6]));
	branch7->SetAddress(&(waves[7]));
	branch8->SetAddress(&(waves[8]));
	branch9->SetAddress(&(waves[9]));
	branch10->SetAddress(&(waves[10]));
	branch11->SetAddress(&(waves[11]));
	branch12->SetAddress(&(waves[12]));
	branch13->SetAddress(&(waves[13]));
	branch14->SetAddress(&(waves[14]));
	branch15->SetAddress(&(waves[15]));

}
