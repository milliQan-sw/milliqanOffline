#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip>
#include <time.h>
#include <string>
#include <cmath>
#include <utility>
#include <map>
#include <stdio.h>
#include <cstdlib>
#include <sys/stat.h>
#include <unistd.h>

#include "TROOT.h"
#include "TSystem.h"
#include "TRandom.h"
#include "TF1.h"
#include "TFile.h"
#include "TVirtualFFT.h"
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
#include "TLegend.h"
#include "TColor.h"
#include "TComplex.h"
#include "TObjArray.h"
#include "TObjString.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TGraphAsymmErrors.h"
#include "utilities.h"

using namespace std;

// Set addresses of ROOT tree branches

int nRollOvers=0;
int runNumOrig=0;
int event = 0;
int fileNum=0;
int runNum=0;
int fileID = 0;
Long64_t event_time_b0=0;
Long64_t event_time_b1=0;
double event_time_fromTDC=0;
bool present_b0;
bool present_b1;
int t_since_fill_start=0;
int t_since_fill_end=0;
int t_until_next_fill=0;
string * event_t_string;
Long64_t event_trigger_time_tag_b0;
Long64_t event_trigger_time_tag_b1;
int fillNum = 0;
float fillAvgLumi=0;
float fillTotalLumi=0;
bool beam;
bool hardNoBeam;
float chan_muDist[32];
int chan_trueNPE[32];
float scale1fb=0;
int orig_evt=0;
bool mcTruth_threeBarLine;
bool mcTruth_fourSlab;

vector<int> * v_npulses = new vector<int>();
vector<int> * v_ipulse = new vector<int>();
vector<int> * v_chan = new vector<int>();
vector<int> * v_layer = new vector<int>();
vector<int> * v_row = new vector<int>();
vector<int> * v_column = new vector<int>();
vector<int> * v_type = new vector<int>();
vector<float> * v_height = new vector<float>();
vector<float> * v_time = new vector<float>();
vector<float> * v_triggerCandidates = new vector<float>();
vector<float> * v_triggerCandidatesEnd = new vector<float>();
vector<int> * v_triggerCandidatesChannel = new vector<int>();
vector<float> * v_time_module_calibrated = new vector<float>();
vector<float> * v_delay = new vector<float>();
vector<float> * v_area = new vector<float>();
vector<float> * v_nPE = new vector<float>();
vector<float> * v_duration =  new vector<float>();
vector<bool> * v_quiet = new vector<bool>();
vector<float> * v_presample_mean = new vector<float>();
vector<float> * v_presample_RMS = new vector<float>();
vector<float> * v_sideband_mean = new vector<float>();
vector<float> * v_sideband_RMS = new vector<float>();
vector<Long64_t> * v_groupTDC_b0 = new vector<Long64_t>();
vector<Long64_t> * v_groupTDC_b1 = new vector<Long64_t>();
vector<float> * v_bx = new vector<float>();
vector<float> * v_by = new vector<float>();
vector<float> * v_bz = new vector<float>();
vector<float> * v_max = new vector<float>();
vector<float> * v_min = new vector<float>();
vector<float> * v_triggerBand_mean = new vector<float>();
vector<float> * v_triggerBand_max = new vector<float>();
vector<float> * v_triggerBand_maxTime = new vector<float>();
vector<float> * v_triggerBand_RMS = new vector<float>();
vector<float> * v_sideband_mean_calib = new vector<float>();
vector<float> * v_sideband_RMS_calib = new vector<float>();
vector<float> * v_maxAfterFilter = new vector<float>();
vector<float> * v_maxThreeConsec = new vector<float>();
vector<float> * v_minAfterFilter = new vector<float>();
vector<float> * v_sideband_mean_perFile = new vector<float>();
vector<float> * v_triggerThreshold = new vector<float>();
vector<bool> * v_triggerEnable = new vector<bool>();
vector<int> * v_triggerMajority = new vector<int>();
vector<int> * v_triggerLogic = new vector<int>();

// nPE corrections directly from Matthew
vector<float> * v_nPECorr = new vector<float> ();


// hodoscope data
int extrg;
double hs_time;
vector<int> * v_hs = new vector<int>();
vector<int> * v_tp = new vector<int>();
vector<double> * v_fit_xz = new vector<double>();
vector<double> * v_fit_yz = new vector<double>();

// function to set branch addresses for everything above
void SetAddresses(TChain *& tree) {

	tree->SetBranchAddress("triggerBand_mean", &v_triggerBand_mean);
	tree->SetBranchAddress("triggerBand_max", &v_triggerBand_max);
	tree->SetBranchAddress("triggerBand_maxTime", &v_triggerBand_maxTime);
	tree->SetBranchAddress("triggerBand_RMS", &v_triggerBand_RMS);
	tree->SetBranchAddress("sideband_mean_calib", &v_sideband_mean_calib);
	tree->SetBranchAddress("sideband_RMS_calib", &v_sideband_RMS_calib);
	tree->SetBranchAddress("max", &v_max);
	tree->SetBranchAddress("min", &v_min);
	tree->SetBranchAddress("maxAfterFilter", &v_maxAfterFilter);
	tree->SetBranchAddress("minAfterFilter", &v_minAfterFilter);
	tree->SetBranchAddress("maxThreeConsec", &v_maxThreeConsec);
	tree->SetBranchAddress("hardNoBeam", &hardNoBeam);
	tree->SetBranchAddress("t_until_next_fill", &t_until_next_fill);
	tree->SetBranchAddress("event_t_string", &event_t_string);
	tree->SetBranchAddress("event", &event);
	tree->SetBranchAddress("run", &runNum);
	tree->SetBranchAddress("file", &fileNum);
	tree->SetBranchAddress("nRollOvers", &nRollOvers);
	tree->SetBranchAddress("beam", &beam);
	tree->SetBranchAddress("fillAvgLumi", &fillAvgLumi);
	tree->SetBranchAddress("fillTotalLumi", &fillTotalLumi);
	tree->SetBranchAddress("event_time_b0", &event_time_b0);
	tree->SetBranchAddress("event_time_b1", &event_time_b1);
	tree->SetBranchAddress("t_since_fill_start", &t_since_fill_start);
	tree->SetBranchAddress("t_since_fill_end", &t_since_fill_end);
	tree->SetBranchAddress("file", &fileNum);
	tree->SetBranchAddress("fill", &fillNum);
	tree->SetBranchAddress("event_trigger_time_tag_b0", &event_trigger_time_tag_b0);
	tree->SetBranchAddress("event_trigger_time_tag_b1", &event_trigger_time_tag_b1);
	tree->SetBranchAddress("present_b0", &present_b0);
	tree->SetBranchAddress("present_b1", &present_b1);
	tree->SetBranchAddress("triggerCandidates", &v_triggerCandidates);
	tree->SetBranchAddress("triggerCandidatesEnd", &v_triggerCandidatesEnd);
	tree->SetBranchAddress("triggerCandidatesChannel", &v_triggerCandidatesChannel);
	tree->SetBranchAddress("chan", &v_chan);
	tree->SetBranchAddress("layer", &v_layer);
	tree->SetBranchAddress("row", &v_row);
	tree->SetBranchAddress("column", &v_column);
	tree->SetBranchAddress("type", &v_type);
	tree->SetBranchAddress("height", &v_height);
	tree->SetBranchAddress("time_module_calibrated", &v_time_module_calibrated);
	tree->SetBranchAddress("time", &v_time);
	tree->SetBranchAddress("delay", &v_delay);
	tree->SetBranchAddress("area", &v_area);
	tree->SetBranchAddress("nPE", &v_nPE);
	tree->SetBranchAddress("ipulse", &v_ipulse);
	tree->SetBranchAddress("npulses", &v_npulses);
	tree->SetBranchAddress("duration", &v_duration);
	tree->SetBranchAddress("quiet", &v_quiet);
	tree->SetBranchAddress("presample_mean", &v_presample_mean);
	tree->SetBranchAddress("presample_RMS", &v_presample_RMS);
	tree->SetBranchAddress("sideband_mean", &v_sideband_mean);
	tree->SetBranchAddress("sideband_RMS", &v_sideband_RMS);
	tree->SetBranchAddress("groupTDC_b0", &v_groupTDC_b0);
	tree->SetBranchAddress("groupTDC_b1", &v_groupTDC_b1);
	tree->SetBranchAddress("event_time_fromTDC", &event_time_fromTDC);
	tree->SetBranchAddress("bx", &v_bx);
	tree->SetBranchAddress("by", &v_by);
	tree->SetBranchAddress("bz", &v_bz);
	tree->SetBranchAddress("sideband_mean_perFile",&v_sideband_mean_perFile);
	tree->SetBranchAddress("triggerThreshold",&v_triggerThreshold);
	tree->SetBranchAddress("triggerEnable",&v_triggerEnable);
	tree->SetBranchAddress("triggerMajority",&v_triggerMajority);
	tree->SetBranchAddress("triggerLogic",&v_triggerLogic);
	tree->SetBranchAddress("chan_muDist",&chan_muDist);
	tree->SetBranchAddress("chan_trueNPE",&chan_trueNPE);
	tree->SetBranchAddress("scale1fb",&scale1fb);
	tree->SetBranchAddress("orig_evt",&orig_evt);
	tree->SetBranchAddress("mcTruth_threeBarLine", &mcTruth_threeBarLine);
	tree->SetBranchAddress("mcTruth_fourSlab", &mcTruth_fourSlab);

	// hodoscope data
	tree->SetBranchAddress("extrg", &extrg);
	tree->SetBranchAddress("hs_time", &hs_time);
	tree->SetBranchAddress("hs", &v_hs);
	tree->SetBranchAddress("tp", &v_tp);
	tree->SetBranchAddress("fit_xz", &v_fit_xz);
	tree->SetBranchAddress("fit_yz", &v_fit_yz);

	tree->SetBranchAddress("nPECorr", &v_nPECorr);
	
}


void SetAddresses(TTree *& tree) {

	tree->SetBranchAddress("event", &event);
	tree->SetBranchAddress("run", &runNum);
	tree->SetBranchAddress("file", &fileNum);
	tree->SetBranchAddress("fill", &fillNum);
	tree->SetBranchAddress("nRollOvers", &nRollOvers);
	tree->SetBranchAddress("beam", &beam);
	tree->SetBranchAddress("hardNoBeam", &hardNoBeam);
	tree->SetBranchAddress("fillAvgLumi", &fillAvgLumi);
	tree->SetBranchAddress("fillTotalLumi", &fillTotalLumi);
	tree->SetBranchAddress("present_b0", &present_b0);
	tree->SetBranchAddress("present_b1", &present_b1);
	tree->SetBranchAddress("event_time_b0", &event_time_b0);
	tree->SetBranchAddress("event_time_b1", &event_time_b1);
	tree->SetBranchAddress("event_time_fromTDC", &event_time_fromTDC);
	tree->SetBranchAddress("t_since_fill_start", &t_since_fill_start);
	tree->SetBranchAddress("t_since_fill_end", &t_since_fill_end);
	tree->SetBranchAddress("t_until_next_fill", &t_until_next_fill);
	tree->SetBranchAddress("event_t_string", &event_t_string);
	tree->SetBranchAddress("event_trigger_time_tag_b0", &event_trigger_time_tag_b0);
	tree->SetBranchAddress("event_trigger_time_tag_b1", &event_trigger_time_tag_b1);
	tree->SetBranchAddress("chan", &v_chan);
	tree->SetBranchAddress("triggerCandidates", &v_triggerCandidates);
	tree->SetBranchAddress("triggerCandidatesEnd", &v_triggerCandidatesEnd);
	tree->SetBranchAddress("triggerCandidatesChannel", &v_triggerCandidatesChannel);
	tree->SetBranchAddress("layer", &v_layer);
	tree->SetBranchAddress("row", &v_row);
	tree->SetBranchAddress("column", &v_column);
	tree->SetBranchAddress("type", &v_type);
	tree->SetBranchAddress("height", &v_height);
	tree->SetBranchAddress("time", &v_time);
	tree->SetBranchAddress("time_module_calibrated", &v_time_module_calibrated);
	tree->SetBranchAddress("delay", &v_delay);
	tree->SetBranchAddress("area", &v_area);
	tree->SetBranchAddress("nPE", &v_nPE);
	tree->SetBranchAddress("ipulse", &v_ipulse);
	tree->SetBranchAddress("npulses", &v_npulses);
	tree->SetBranchAddress("duration", &v_duration);
	tree->SetBranchAddress("quiet", &v_quiet);
	tree->SetBranchAddress("presample_mean", &v_presample_mean);
	tree->SetBranchAddress("presample_RMS", &v_presample_RMS);
	tree->SetBranchAddress("sideband_mean", &v_sideband_mean);
	tree->SetBranchAddress("sideband_RMS", &v_sideband_RMS);
	tree->SetBranchAddress("sideband_mean_perFile",&v_sideband_mean_perFile);
	tree->SetBranchAddress("triggerBand_mean", &v_triggerBand_mean);
	tree->SetBranchAddress("triggerBand_max", &v_triggerBand_max);
	tree->SetBranchAddress("triggerBand_maxTime", &v_triggerBand_maxTime);
	tree->SetBranchAddress("triggerBand_RMS", &v_triggerBand_RMS);
	tree->SetBranchAddress("sideband_mean_calib", &v_sideband_mean_calib);
	tree->SetBranchAddress("sideband_RMS_calib", &v_sideband_RMS_calib);
	tree->SetBranchAddress("groupTDC_b0", &v_groupTDC_b0);
	tree->SetBranchAddress("groupTDC_b1", &v_groupTDC_b1);
	tree->SetBranchAddress("max", &v_max);
	tree->SetBranchAddress("min", &v_min);
	tree->SetBranchAddress("maxAfterFilter", &v_maxAfterFilter);
	tree->SetBranchAddress("maxThreeConsec", &v_maxThreeConsec);
	tree->SetBranchAddress("minAfterFilter", &v_minAfterFilter);
	tree->SetBranchAddress("triggerThreshold",&v_triggerThreshold);
	tree->SetBranchAddress("triggerEnable",&v_triggerEnable);
	tree->SetBranchAddress("triggerMajority",&v_triggerMajority);
	tree->SetBranchAddress("triggerLogic",&v_triggerLogic);
	tree->SetBranchAddress("bx", &v_bx);
	tree->SetBranchAddress("by", &v_by);
	tree->SetBranchAddress("bz", &v_bz);
	tree->SetBranchAddress("chan_muDist",&chan_muDist);
	tree->SetBranchAddress("chan_trueNPE",&chan_trueNPE);
	tree->SetBranchAddress("scale1fb",&scale1fb);
	tree->SetBranchAddress("fileID", &fileID);
	tree->SetBranchAddress("orig_evt",&orig_evt);
	tree->SetBranchAddress("mcTruth_threeBarLine", &mcTruth_threeBarLine);
	tree->SetBranchAddress("mcTruth_fourSlab", &mcTruth_fourSlab);

	// hodoscope data
	tree->SetBranchAddress("extrg", &extrg);
	tree->SetBranchAddress("hs_time", &hs_time);
	tree->SetBranchAddress("hs", &v_hs);
	tree->SetBranchAddress("tp", &v_tp);
	tree->SetBranchAddress("fit_xz", &v_fit_xz);
	tree->SetBranchAddress("fit_yz", &v_fit_yz);

	tree->SetBranchAddress("nPECorr", &v_nPECorr);
	
}


void SetAddresses_nohs(TTree *& tree) {

	tree->SetBranchAddress("event", &event);
	tree->SetBranchAddress("run", &runNum);
	tree->SetBranchAddress("file", &fileNum);
	tree->SetBranchAddress("fill", &fillNum);
	tree->SetBranchAddress("nRollOvers", &nRollOvers);
	tree->SetBranchAddress("beam", &beam);
	tree->SetBranchAddress("hardNoBeam", &hardNoBeam);
	tree->SetBranchAddress("fillAvgLumi", &fillAvgLumi);
	tree->SetBranchAddress("fillTotalLumi", &fillTotalLumi);
	tree->SetBranchAddress("present_b0", &present_b0);
	tree->SetBranchAddress("present_b1", &present_b1);
	tree->SetBranchAddress("event_time_b0", &event_time_b0);
	tree->SetBranchAddress("event_time_b1", &event_time_b1);
	tree->SetBranchAddress("event_time_fromTDC", &event_time_fromTDC);
	tree->SetBranchAddress("t_since_fill_start", &t_since_fill_start);
	tree->SetBranchAddress("t_since_fill_end", &t_since_fill_end);
	tree->SetBranchAddress("t_until_next_fill", &t_until_next_fill);
	tree->SetBranchAddress("event_t_string", &event_t_string);
	tree->SetBranchAddress("event_trigger_time_tag_b0", &event_trigger_time_tag_b0);
	tree->SetBranchAddress("event_trigger_time_tag_b1", &event_trigger_time_tag_b1);
	tree->SetBranchAddress("chan", &v_chan);
	tree->SetBranchAddress("triggerCandidates", &v_triggerCandidates);
	tree->SetBranchAddress("triggerCandidatesEnd", &v_triggerCandidatesEnd);
	tree->SetBranchAddress("triggerCandidatesChannel", &v_triggerCandidatesChannel);
	tree->SetBranchAddress("layer", &v_layer);
	tree->SetBranchAddress("row", &v_row);
	tree->SetBranchAddress("column", &v_column);
	tree->SetBranchAddress("type", &v_type);
	tree->SetBranchAddress("height", &v_height);
	tree->SetBranchAddress("time", &v_time);
	tree->SetBranchAddress("time_module_calibrated", &v_time_module_calibrated);
	tree->SetBranchAddress("delay", &v_delay);
	tree->SetBranchAddress("area", &v_area);
	tree->SetBranchAddress("nPE", &v_nPE);
	tree->SetBranchAddress("ipulse", &v_ipulse);
	tree->SetBranchAddress("npulses", &v_npulses);
	tree->SetBranchAddress("duration", &v_duration);
	tree->SetBranchAddress("quiet", &v_quiet);
	tree->SetBranchAddress("presample_mean", &v_presample_mean);
	tree->SetBranchAddress("presample_RMS", &v_presample_RMS);
	tree->SetBranchAddress("sideband_mean", &v_sideband_mean);
	tree->SetBranchAddress("sideband_RMS", &v_sideband_RMS);
	tree->SetBranchAddress("sideband_mean_perFile",&v_sideband_mean_perFile);
	tree->SetBranchAddress("triggerBand_mean", &v_triggerBand_mean);
	tree->SetBranchAddress("triggerBand_max", &v_triggerBand_max);
	tree->SetBranchAddress("triggerBand_maxTime", &v_triggerBand_maxTime);
	tree->SetBranchAddress("triggerBand_RMS", &v_triggerBand_RMS);
	tree->SetBranchAddress("sideband_mean_calib", &v_sideband_mean_calib);
	tree->SetBranchAddress("sideband_RMS_calib", &v_sideband_RMS_calib);
	tree->SetBranchAddress("groupTDC_b0", &v_groupTDC_b0);
	tree->SetBranchAddress("groupTDC_b1", &v_groupTDC_b1);
	tree->SetBranchAddress("max", &v_max);
	tree->SetBranchAddress("min", &v_min);
	tree->SetBranchAddress("maxAfterFilter", &v_maxAfterFilter);
	tree->SetBranchAddress("maxThreeConsec", &v_maxThreeConsec);
	tree->SetBranchAddress("minAfterFilter", &v_minAfterFilter);
	tree->SetBranchAddress("triggerThreshold",&v_triggerThreshold);
	tree->SetBranchAddress("triggerEnable",&v_triggerEnable);
	tree->SetBranchAddress("triggerMajority",&v_triggerMajority);
	tree->SetBranchAddress("triggerLogic",&v_triggerLogic);
	tree->SetBranchAddress("bx", &v_bx);
	tree->SetBranchAddress("by", &v_by);
	tree->SetBranchAddress("bz", &v_bz);
	tree->SetBranchAddress("chan_muDist",&chan_muDist);
	tree->SetBranchAddress("chan_trueNPE",&chan_trueNPE);
	tree->SetBranchAddress("scale1fb",&scale1fb);
	tree->SetBranchAddress("fileID", &fileID);
	tree->SetBranchAddress("orig_evt",&orig_evt);
	tree->SetBranchAddress("mcTruth_threeBarLine", &mcTruth_threeBarLine);
	tree->SetBranchAddress("mcTruth_fourSlab", &mcTruth_fourSlab);
}


void ClearVectors() {

	v_max->clear();
	v_maxAfterFilter->clear();
	v_maxThreeConsec->clear();
	v_min->clear();
	v_minAfterFilter->clear();
	v_chan->clear();
	v_triggerCandidates->clear();
	v_triggerCandidatesEnd->clear();
	v_triggerCandidatesChannel->clear();
	v_layer->clear();
	v_row->clear();
	v_column->clear();
	v_type->clear();
	v_height->clear();
	v_time->clear();
	v_time_module_calibrated->clear();
	v_area->clear();
	v_nPE->clear();
	v_ipulse->clear();
	v_npulses->clear();
	v_duration->clear();
	v_delay->clear();
	v_sideband_mean->clear();
	v_sideband_RMS->clear();
	v_triggerBand_mean->clear();
	v_triggerBand_max->clear();
	v_triggerBand_maxTime->clear();
	v_triggerBand_RMS->clear();
	v_sideband_mean_calib->clear();
	v_sideband_RMS_calib->clear();
	v_quiet->clear();
	v_presample_mean->clear();
	v_presample_RMS->clear();
	v_groupTDC_b0->clear();
	v_groupTDC_b1->clear();
	v_bx->clear();
	v_by->clear();
	v_bz->clear();
	v_sideband_mean_perFile->clear();
	v_triggerThreshold->clear();
	v_triggerEnable->clear();
	v_triggerMajority->clear();
	v_triggerLogic->clear();

	// hodoscope
	v_hs->clear();
	v_tp->clear();
	v_fit_xz->clear();
	v_fit_yz->clear();
}


////////////////////////////////////////////////////
////////////////////////////////////////////////////
////////////////////////////////////////////////////
////////////////////////////////////////////////////
////////////////////////////////////////////////////
// USEFUL FUNCTIONS:

int LAYERS=3;
int HEIGHT=3;
int WIDTH=2;
int LEFT=0;
int RIGHT=1;
int BOTTOM=0;
int MIDDLE=1;
int TOP=2;
int NUM_CHAN = 32;
enum typeList {kBar = 0, kSlab = 1, kSheet = 2};

void SetAddressesEventComp(TChain *& tree){
	tree->SetBranchAddress("run", &runNum);
	tree->SetBranchAddress("event", &event);
	tree->SetBranchAddress("file", &fileNum);
}

void SetAddressesEventComp(TTree *& tree){
	tree->SetBranchAddress("run", &runNum);
	tree->SetBranchAddress("event", &event);
	tree->SetBranchAddress("file", &fileNum);
}

double divison(double a, double b){
	if(b == 0){
		throw "Error: divison by zero occured";
		printf(" at line number %d \n",__LINE__);
	}
	return (a/b);
}

string tostr(int x){
	stringstream str;
	str << x;
	return str.str();
}

string tostr(double x){
	stringstream str;
	str << x;
	return str.str();
}

int toint(string text){
	int number;
	std::istringstream iss (text);
	iss >> number;
	return number;
}


//layer map

/*    L  T  R
* 2:  31 14 26
* 1:  11 30 19
* 0:  27 10 29f
*/

//first index is layer=0,1,2
//second index is column: L=0,R=1
//third index is height in column: bottom=0, top=2


vector<int> bars = {};
void fillBars(){
	for (int i=0; i<LAYERS; i++){
		for (int j=0; j<WIDTH; j++){
			for (int k=0; k<HEIGHT; k++){
				bars.push_back(channelMap[i][j][k]);
			}
		}
	}
}

//first index is layer=0,1,2
//second index is L=0,T=1,R=2
int sheetMap[3][3] = {
	{ 27, 10, 29 },
	{ 11, 30, 19 },
	{ 31, 14, 26 }
};

//first index is layer=0,1,2
//second index is F=0, B=1       "Front" is defined to be toward the IP
int slabMap[3][2] = {
	{ 18, 20 },
	{ 20, 28 },
	{ 28, 21 }
};


vector<double> cosmicCuts(32, -1.0);
void setCosmicCuts(){
 cosmicCuts[2] = 4900;
 cosmicCuts[22] = 5100;
 cosmicCuts[4] = 5000;
 cosmicCuts[3] = 4853;
 cosmicCuts[23] = 2700;
 cosmicCuts[5] = 4139;
 cosmicCuts[6] = 4700;
 cosmicCuts[16] = 5200;
 cosmicCuts[12] = 5000;
 cosmicCuts[7] = 4750;
 cosmicCuts[17] = 2650;                  //changed it from 26500 to 2650, assuming typo
 cosmicCuts[13] = 4000;
 cosmicCuts[0] = 4900;
 cosmicCuts[24] = 5010;
 cosmicCuts[8] = 0;
 cosmicCuts[1] = 4850;
 cosmicCuts[25] = 2700;
 cosmicCuts[9] = 4100;

 cosmicCuts[10] = 2000;
 cosmicCuts[30] = 3000;
 cosmicCuts[14] = 1000;
}

string rowName(int row){
	if (row==0) return "Bottom";
	else if (row==1) return "Middle";
	else if (row==2) return "Top";
	else return "Error";
}

string columnName(int column){
	if (column==0) return "Left";
	else if (column==1) return "Right";
	else return "Error";
}

string sheetName(int num){
	if (num==0) return "Left";
	else if (num==1) return "Top";
	else if (num==2) return "Right";
	else return "Error";
}

string printVector(vector<int> myVector){
	string myString = "";
	for (unsigned int z=0; z<myVector.size(); z++){
		myString += tostr(myVector[z]);
		myString += ",";
	}
	return myString;
}

string printVector(vector<double> myVector){
	string myString = "";
	for (unsigned int z=0; z<myVector.size(); z++){
		myString += tostr(myVector[z]);
		myString += ",";
	}
	return myString;
}

double maxElement(vector<double> thing){
	double max = -1e99;
	if(thing.size() > 0) max = thing[0];
	for(unsigned int i=0; i<thing.size(); ++i){
		if(thing[i]>max) max = thing[i];
	}
	return max;
}

int maxElement(vector<int> thing){
	int max = -2147483648;
	if(thing.size() > 0) max = thing[0];
	for(unsigned int i=0; i<thing.size(); ++i){
		if(thing[i]>max) max = thing[i];
	}
	return max;
}

double minElement(vector<double> thing){
	double min = 1e99;
	if(thing.size() > 0) min = thing[0];
	for(unsigned int i=0; i<thing.size(); ++i){
		if(thing[i]<min) min = thing[i];
	}
	return min;
}

int minElement(vector<int> thing){
	double min = 1e99;
	if(thing.size() > 0) min = thing[0];
	for(unsigned int i=0; i<thing.size(); ++i){
		if(thing[i]<min) min = thing[i];
	}
	return min;
}

// sorts vector with thing[0] being smallest element
vector<int> sort_vector(vector<int> thing){
	vector<int> temp_vector = {};
	vector<int> sorted_vector = {};
	int min = minElement(thing);
	int temp_min = min;
	temp_vector = thing;

	for(unsigned int j=0; j<thing.size(); ++j){
		temp_min = minElement(temp_vector);
		sorted_vector.push_back(temp_min);
		for(unsigned int i=0; i<temp_vector.size(); ++i){
			if(temp_vector[i] == temp_min){
				temp_vector.erase(temp_vector.begin()+i);
				break;
			}
		}
	}
	return sorted_vector;
}

vector<double> sort_vector(vector<double> thing){
	vector<double> temp_vector = {};
	vector<double> sorted_vector = {};
	double min = minElement(thing);
	double temp_min = min;
	temp_vector = thing;

	for(unsigned int j=0; j<thing.size(); ++j){
		temp_min = minElement(temp_vector);
		sorted_vector.push_back(temp_min);
		for(unsigned int i=0; i<temp_vector.size(); ++i){
			if(temp_vector[i] == temp_min){
				temp_vector.erase(temp_vector.begin() +i);
				break;
			}
		}
	}
	return sorted_vector;
}


TString toTstring(string thing){
		TString thingT = thing;
		return thingT;
}


double poissRateError(double a, double b, double epsilon = 0.000000000001){
	double error = 0;
	double diff = b - 0;
	if((diff > epsilon) && (-diff < -1*epsilon)) {
		error = sqrt( ((a)/(pow(b,2)) ) + ( (pow(a,2)) / (pow(b,3))));
	}
	else{
		error = 0;
	}
	return error;
}


int getLayer(int chan){
	int layer = -2;
	// slabs
	if(chan == 18) layer = 0;
	if(chan == 20) layer = 0;
	if(chan == 28) layer = 0;
	if(chan == 21) layer = 0;

	// layer 1 bars
	if(chan == 0) layer = 1;
	if(chan == 1) layer = 1;
	if(chan == 24) layer = 1;
	if(chan == 25) layer = 1;
	if(chan == 8) layer = 1;
	if(chan == 9) layer = 1;
	// layer 1 sheets
	if(chan == 29) layer = 1;
	if(chan == 10) layer = 1;
	if(chan == 27) layer = 1;

	// layer 2 bars
	if(chan == 6) layer = 2;
	if(chan == 7) layer = 2;
	if(chan == 16) layer = 2;
	if(chan == 17) layer = 2;
	if(chan == 12) layer = 2;
	if(chan == 13) layer = 2;
	// layer 2 sheets
	if(chan == 19) layer = 2;
	if(chan == 11) layer = 2;
	if(chan == 30) layer = 2;

	// layer 3 bars
	if(chan == 2) layer = 3;
	if(chan == 3) layer = 3;
	if(chan == 22) layer = 3;
	if(chan == 23) layer = 3;
	if(chan == 4) layer = 3;
	if(chan == 5) layer = 3;
	// layer 3 sheets
	if(chan == 14) layer = 3;
	if(chan == 26) layer = 3;
	if(chan == 31) layer = 3;

	if(layer == -2){
		cout << "Not a valid channel" << endl;
	}

	return layer;
}


// NB: displayProgress adds ~20% of overhead
void displayProgress(int i, int entries){
	cout << std::fixed << std::setprecision(1) << "\r\033[1;35m[" << (i/static_cast<double>(entries-1/100.0))*100 << "%]\033[0m";
}

// cout debugging
inline void debug(bool flag, int line){if(flag) cout<<"line "<<line<<" "<<endl;}
inline void debugVar(bool flag, int line, int var){if(flag) cout<<line<<" "<<var<<endl;}
inline void debugVar(bool flag, int line, double var){if(flag) cout<<line<<" "<<var<<endl;}
inline void debugVar(bool flag, int line, string var){if(flag) cout<<line<<" "<<var<<endl;}
inline void debugVar(bool flag, int line, float var){if(flag) cout<<line<<" "<<var<<endl;}
inline void debugVar(bool flag, int line, TString var){if(flag) cout<<line<<" "<<var<<endl;}
inline void debugVar(bool flag, int line, bool var){if(flag) cout<<line<<" "<<var<<endl;}

Long64_t GetTreeIndex(TChain *tree, int runVar, int fileVar, int eventVar, int entries){
	auto nentries = entries;
	TString draw_selection = TString::Format("run==%d && file==%d && event==%d",runVar,fileVar, eventVar);
	TString draw_command = TString::Format("Entry$ >> hist(%d,0,%d)",nentries,nentries);
	tree->Draw(draw_command,draw_selection,"goff");
	TH1I *hist = (TH1I*)gDirectory->Get("hist");
	Long64_t iEntry = hist->GetBinLowEdge(hist->FindFirstBinAbove(0));
	delete hist;
	return iEntry;
}

inline bool file_exists(const std::string& name) {
	struct stat buffer;   
	return (stat (name.c_str(), &buffer) == 0); 
}