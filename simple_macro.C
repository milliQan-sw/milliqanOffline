#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip>
#include <time.h>
#include <exception>
#include <sys/stat.h>
#include <sys/types.h>


#include "TSystem.h"
#include "TRandom2.h"
#include "TROOT.h"
#include "TF1.h"
#include "TMath.h"
#include "TArray.h"
#include "TFile.h"
#include "TVirtualFFT.h"
#include "TTree.h"
#include "TChain.h"
#include <set>
#include "TMath.h"
#include "TH1F.h"
#include "TParameter.h"
#include "TH2F.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TDirectory.h"
#include "TBranch.h"
#include "TString.h"
#include "TObjString.h"
#include "TStyle.h"
#include "TPaveStats.h"
#include "TLatex.h"
#include "TSystemDirectory.h"
#include "TSystemFile.h"
#include "TGaxis.h"
#include "TLegend.h"
#include "TColor.h"
#include "TComplex.h"

#include "/home/milliqan/MilliDAQ/interface/GlobalEvent.h"
#include "/home/milliqan/MilliDAQ/interface/DemonstratorConfiguration.h"

#include <string>
#include <sys/types.h>
#include <sys/stat.h>
#include <fstream>
#include <iostream>

struct stat info1;
struct stat info2;

#ifdef __MAKECINT__
#pragma link C++ class std::vector < std::vector<int> >+;
#pragma link C++ class std::vector < std::vector<float> >+;
#endif

using namespace std;

//Configurable parameters
int numChan=16;
TArrayI* chanArray;
//int maxEvents=-1;
int maxEvents = 51000;  // need to change for combined files from calibration
//int time_window = 0.0885;
map<int, map<int,vector<float> > > sidebandPerFile;
float sideband_range[2] = {0,50};
float triggerBand_range[2] = {360,390};
float presampleStart= 17.5;
float presampleEnd = 2.5;

float sample_rate[] = {1.6,1.6};

bool debug=false;
bool darkRate=true;

bool milliDAQ=false;

TString configurationFolder = "/home/milliqan/milliqanOffline/configuration/";

vector< vector<int> > chanMap = {{1,3,1,0},{2,3,1,0},{1,3,3,0},{2,3,3,0},{1,1,3,0},{2,1,3,0},{1,3,2,0},{2,3,2,0},{1,1,1,0},{2,1,1,0},{0,-2,1,2},{0,-2,2,2},{1,1,2,0},{2,1,2,0},{0,-2,3,2},{1,2,4,0},{1,2,2,0},{2,2,2,0},{0,-1,0,1},{1,-2,2,2},{1,1,4,0},{0,-1,3,1},{1,2,3,0},{2,2,3,0},{1,2,1,0},{2,2,1,0},{1,-2,3,2},{-1,-2,1,2},{2,2,4,0},{1,-2,1,2},{-1,-2,2,2},{-1,-2,3,2}};

//Declare global variables
vector<TH1D*> waves;
float meanCalib[] = {-0.2453, 0.009, -0.007, -0.07, -0.661, -0.252, 0.080, -0.214, -1.04, -0.160, 1.18, -0.910, -0.3789, -1.09, -0.53, 0., -0.367, -0.837, -0.283, -0.275, -0.235, -0.295, -0.443, -0.606, -0.762, -0.201, -0.576, -0.440, -0.706, -0.426, -0.280, -0.458};
float rmsCalib[] = {0.8637, 0.7901, 0.9028, 0.7561, 0.8741, 0.7857, 0.8706, 0.7795, 0.8098, 0.7954, 0.9941, 0.7833, 0.9148, 0.7899, 0.9600, 1., 0.8829, 0.8828, 0.8908, 0.8005, 0.8400, 0.8863, 1.061, 0.8085, 0.9275, 0.8194, 0.9087, 0.7757, 0.8507, 0.9169, 0.9577, 0.8018};
float interModuleCalibrations[32] = { 33.125, 33.125, 13.75, 24.375, 23.75, 35.0, 30.625, 29.375, 24.375, 33.75, 3.75, 16.25, 26.875, 34.375, 9.375, 0.0, 27.5, 30.625, 0.0, 11.25, 7.5, 12.5, 28.125, 20.625, 33.75, 26.875, -3.125, 9.375, 13.75, 0.625, 15.625,10.625};
float channelCalibrations[32];
float channelSPEAreas[] = {62.,54.,73.,55.,62.,74.,68.,69.,92.,61.,85.,80.,51.,76.,65.,75.,52.,47.,80.,82.,58.,80.,86.,40.,51.,30.,60.,73.,59.,47.,75.,65.};

#ifndef _INCL_GUARD
TTree * inTree;
#endif
TTree * outTree;

Long64_t initTDC=-1;
Long64_t initSecs=-1;
Long64_t prevTDC=-1;

int nRollOvers=0;

int npulses_chan0 = 0;
int npulses_chan2 = 0;
int npulses_chan4 = 0;
int event = 0;
int fileNum=0;
Long64_t runNum=0;
int runNumOrig=0;
Long64_t event_time_b0=0;
Long64_t event_time_b1=0;
double event_time_fromTDC=0;
bool present_b0;
bool present_b1;
int t_since_fill_start=0;
int t_since_fill_end=0;
int t_until_next_fill=0;
string event_t_string;
Long64_t event_trigger_time_tag_b0;
Long64_t event_trigger_time_tag_b1;
int fillNum;
float fillAvgLumi=0;
float fillTotalLumi=0;
bool beam=false;
bool hardNoBeam=true;
mdaq::GlobalEvent * evt = new mdaq::GlobalEvent();

mdaq::DemonstratorConfiguration * cfg = new mdaq::DemonstratorConfiguration();

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
vector<float> * v_sideband_mean_perFile = new vector<float>();
vector<float> * v_triggerBand_mean = new vector<float>();
vector<float> * v_triggerBand_max = new vector<float>();
vector<float> * v_triggerBand_maxTime = new vector<float>();
vector<float> * v_triggerBand_RMS = new vector<float>();
vector<float> * v_sideband_mean_calib = new vector<float>();
vector<float> * v_sideband_RMS_calib = new vector<float>();

vector<Long64_t> * v_groupTDC_b0 = new vector<Long64_t>();
vector<Long64_t> * v_groupTDC_b1 = new vector<Long64_t>();

vector<float> * v_bx = new vector<float>();
vector<float> * v_by = new vector<float>();
vector<float> * v_bz = new vector<float>();
vector<float> * v_max = new vector<float>();
vector<float> * v_min = new vector<float>();
vector<float> * v_max_afterFilter = new vector<float>();
vector<float> * v_max_threeConsec = new vector<float>();
vector<float> * v_triggerThresholds = new vector<float>();
vector<bool> * v_triggerEnable = new vector<bool>();
vector<int> * v_triggerLogic = new vector<int>();
vector<int> * v_triggerMajority = new vector<int>();
vector<float> * v_min_afterFilter = new vector<float>();

Float_t         chan_muDist[32];
Int_t           chan_trueNPE[32];
Int_t           fileID = -1;
Float_t         scale1fb = -1.;
Int_t           orig_evt = -1;
Bool_t          mcTruth_fourSlab = false;
Bool_t          mcTruth_threeBarLine = false;

bool addTriggerTimes = true;

double timestampSecs = 0;

// Sanity check

TString milliqanOfflineDir="/home/milliqan/milliqanOffline/";

void make_tree(TString fileName, int eventNum=-1, TString tag="",float rangeMinX=-1.,float rangeMaxX=-1.,float rangeMinY=-1000.,float rangeMaxY=-1000., int displayPulseBounds=1, int onlyForceChans=0, int runFFT=0 , int applyLPFilter = 0,int injectPulses=0, float injectSignalQ=-1, int runDRS=0,std::set<int> forceChan={});
void loadBranchesMilliDAQ();
void loadWavesMilliDAQ();
void prepareOutBranches();
void clearOutBranches();
vector< vector<float> > processChannel(int ic,bool applyLPFilter, bool injectPulses, float injectSignalQ, int runDRS);
void prepareWave(int ic, float &sb_mean, float &sb_RMS, float &tb_mean, float &tb_RMS, float &tb_max, float &tb_maxTime, bool applyLPFilter, bool injectPulses, float injectSignalQ,int runDRS);
vector< vector<float> > findPulses(int ic,bool applyLPFilter, int runDRS);
void findTriggerCandidates(int ic, float sb_mean);


# ifndef __CINT__
#ifndef _INCL_GUARD
int main(int argc, char **argv)
{
    if(argc==2) make_tree(argv[1]);
    else if(argc==3) make_tree(argv[1],stoi(argv[2]));
    else if(argc==4) make_tree(argv[1],stoi(argv[2]),argv[3]);
    else if(argc==6) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]));
    else if(argc==7) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]));    else if(argc==8) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]));
    else if(argc==9) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]));
    else if(argc==10) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]),stoi(argv[9]));
    else if(argc==11) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]),stoi(argv[9]),stoi(argv[10]));
    else if(argc==12) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]),stoi(argv[9]),stoi(argv[10]),stoi(argv[11]));
    else if(argc==13) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]),stoi(argv[9]),stoi(argv[10]),stoi(argv[11]),stoi(argv[12]));
    else if(argc==14) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]),stoi(argv[9]),stoi(argv[10]),stoi(argv[11]),stoi(argv[12]),atof(argv[13]));
    else if(argc==15) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]),stoi(argv[9]),stoi(argv[10]),stoi(argv[11]),stoi(argv[12]),atof(argv[13]),stoi(argv[14]));
    else if(argc>=16) {
    set<int> forceChans;
        for(int i=15;i<argc;i++){
            forceChans.insert(stoi(argv[i]));
        }
        make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]),stoi(argv[6]),stoi(argv[7]),stoi(argv[8]),stoi(argv[9]),stoi(argv[10]),stoi(argv[11]),stoi(argv[12]),atof(argv[13]),stoi(argv[14]),forceChans);
    }

    cout<<"Number of pulses found in channel 0 = "<<npulses_chan0<<endl;
    cout<<"Number of pulses found in channel 2 = "<<npulses_chan2<<endl;
    cout<<"Number of pulses found in channel 4 = "<<npulses_chan4<<endl;
    //float np_ch0 = (float) npulses_chan0;
    //float np_ch2 = (float) npulses_chan2;
    //float np_ch4 = (float) npulses_chan4;
    //cout<<"Number of pulses found in channel 0 = "<<np_ch0<<endl;
    //float DarkRate_ch0 = np_ch0/time_window;
    //float DarkRate_ch2 = np_ch2/time_window;
    //float DarkRate_ch4 = np_ch4/time_window;
    //cout<<"Channel 0 Dark Rate = "<<DarkRate_ch0<<" Hz "<<endl;
    //cout<<"Channel 2 Dark Rate = "<<DarkRate_ch2<<" Hz "<<endl;
    //cout<<"Channel 4 Dark Rate = "<<DarkRate_ch4<<" Hz "<<endl;   

}
# endif 
# endif

void make_tree(TString fileName, int eventNum, TString tag, float rangeMinX,float rangeMaxX, float rangeMinY,float rangeMaxY, int displayPulseBounds, int onlyForceChans,int runFFT,int applyLPFilter,int injectPulses, float injectSignalQ,int runDRS, set<int> forceChan){

    TString inFileName = fileName;
    TFile *f = TFile::Open(inFileName, "READ");
    TString date;
    TTree * metadata;
    TString baseFileName= ((TObjString*)inFileName.Tokenize("/")->Last())->String().Data();
    TString runNumber = ((TObjString*)baseFileName.Tokenize(".")->At(0))->String().Data();
    runNumber.ReplaceAll("MilliQan_Run","");

    inTree = (TTree*)f->Get("Events");
    metadata = (TTree*)f->Get("Metadata");
    metadata->SetBranchAddress("configuration", &cfg);
    metadata->GetEntry(0);
    fstream file;
    runNum = atoi(runNumber.Data());
    file.open(configurationFolder+"Run"+runNum+".txt", ios::out);

    chanArray = new TArrayI(numChan);

    for (int i =0; i < numChan; i++){
        chanArray->SetAt(i,i);
        float triggerThresh = cfg->digitizers[i/16].channels[i % 16].triggerThreshold;
        bool triggerEnable = cfg->digitizers[i/16].channels[i % 16].triggerEnable;
        //std::cout << "5.4_" << endl;
        int triggerMajority = cfg->digitizers[i/16].GroupTriggerMajorityLevel;
        //std::cout << "5.5_" << endl;
        int triggerLogic = cfg->digitizers[i/16].GroupTriggerLogic;
        //std::cout << "5.6_" << endl;
        v_triggerThresholds->push_back(triggerThresh);
        v_triggerEnable->push_back(triggerEnable);
        v_triggerMajority->push_back(triggerMajority);
        v_triggerLogic->push_back(triggerLogic);
        //std::cout << "5.7_" << endl;
     }

     TString configName = "TripleCoincidence";
     TString treeDirectory = milliqanOfflineDir+"trees/";
     TString outFileName = treeDirectory+"_processed_"+baseFileName;

     

     if (!milliDAQ) loadBranchesMilliDAQ();

     //cout<<"5.8_"<<endl;

     //gSystem->mkdir(milliqanOfflineDir+"_trees");
     gSystem->mkdir(treeDirectory);
     TFile * outFile;
     outFile = new TFile(outFileName,"recreate");
     outTree = new TTree("t","t");
     prepareOutBranches(); 

     cout<<"Starting event loop"<<endl;
     for(int i=0;i<maxEvents;i++){
         clearOutBranches();
         event=i;
         inTree->GetEntry(i);
         if (!milliDAQ) loadWavesMilliDAQ();
         //Loop over channels
	 vector<vector<vector<float> > > allPulseBounds;
	 for(int ic=0;ic<numChan;ic++){
	     allPulseBounds.push_back(processChannel(ic,applyLPFilter,injectPulses,injectSignalQ,runDRS));
	     if (ic==2) v_max->push_back(1.*waves[ic]->GetMaximum());
             //The above if statement is used only for the PMT calibration studies
	 }    

         for(int ig=0; ig<8; ig++){
             v_groupTDC_b0->push_back(evt->digitizers[0].TDC[ig]);
             v_groupTDC_b1->push_back(evt->digitizers[1].TDC[ig]);
         }

         present_b0 = evt->digitizers[0].DataPresent;
	 present_b1 = evt->digitizers[1].DataPresent;

         event_time_b0 = evt->digitizers[0].DAQTimeStamp.GetSec();
         event_time_b1 = evt->digitizers[1].DAQTimeStamp.GetSec();

         outTree->Fill();

         //for (int ch = 0; ch < 8; ch++){
             //cout<<"i = "<<i<<" , ch = "<<ch<<" , v = "<<evt->digitizers[1].waveform[ch][i]<<endl;
        // }
     }

     
     //outTree->Fill();
     outTree->Write();
     outFile->Close();

     cout<<"Closed output tree."<<endl;
}

void convertXaxis(TH1D *h, int ic){
    TAxis * a = h->GetXaxis();
    a->Set( a->GetNbins(), a->GetXmin()/sample_rate[ic/16], a->GetXmax()/sample_rate[ic/16] );

    h->ResetStats();
}

void prepareWave(int ic, float &sb_meanPerEvent, float &sb_RMSPerEvent, float &sb_triggerMeanPerEvent, float &sb_triggerRMSPerEvent,
        float &sb_triggerMaxPerEvent,float &sb_timeTriggerMaxPerEvent,bool applyLPFilter, bool injectPulses, float injectSignalQ, int runDRS){

    //Invert waveform and convert x-axis to ns
    //waves[ic]->Scale(-1.0); // 
    if (runDRS <= 0){
        convertXaxis(waves[ic],ic);
    }

    //subtract calibrated mean
    //for(int ibin = 1; ibin <= waves[ic]->GetNbinsX(); ibin++){
    //    waves[ic]->SetBinContent(ibin,waves[ic]->GetBinContent(ibin)-meanCalib[ic]);
    //}

    // Other stuff here is just signal injection stuff (see make_tree.C)
}

vector< vector<float> > processChannel(int ic,bool applyLPFilter, bool injectPulses, float injectSignalQ, int runDRS){
    float sb_meanPerEvent, sb_RMSPerEvent, sb_triggerMeanPerEvent, sb_triggerRMSPerEvent,  sb_triggerMaxPerEvent, sb_timeTriggerMaxPerEvent;
    prepareWave(ic, sb_meanPerEvent, sb_RMSPerEvent,sb_triggerMeanPerEvent, sb_triggerRMSPerEvent, sb_triggerMaxPerEvent, sb_timeTriggerMaxPerEvent,applyLPFilter, injectPulses, injectSignalQ,runDRS);
    //float sb_mean = meanCalib[ic];
    //float sb_RMS = rmsCalib[ic];

    vector<vector<float> > pulseBounds;
    pulseBounds = findPulses(ic,applyLPFilter, runDRS);
    //if (addTriggerTimes) findTriggerCandidates(ic,sb_mean);

    int npulses = pulseBounds.size();
    //cout<<"npulses = "<<npulses<<endl;
    if (ic==0&&npulses>0) npulses_chan0 += npulses;
    if (ic==2&&npulses>0) npulses_chan2 += npulses;
    if (ic==4&&npulses>0) npulses_chan4 += npulses;

    v_sideband_mean->push_back(sb_meanPerEvent);
    //v_sideband_RMS->push_back(sb_RMSPerEvent);
    v_triggerBand_mean->push_back(sb_triggerMeanPerEvent);
    v_triggerBand_RMS->push_back(sb_triggerRMSPerEvent);
    v_triggerBand_max->push_back(sb_triggerMaxPerEvent);
    v_triggerBand_maxTime->push_back(sb_timeTriggerMaxPerEvent);
    //v_sideband_mean_calib->push_back(sb_mean);
    //v_sideband_RMS_calib->push_back(sb_RMS);
    float maxThreeConsec = -100;
    //cout<<"Channel number = "<<ic<<" wave vector zero entry =  "<<waves[ic]->GetBinContent(2)<<endl;  
    //cout<<"Channel number = "<<ic<<" raw wave value (zero entry) = "<<evt->digitizers[0].waveform[ic][2]<<endl;

    for (int iBin = 1; iBin < waves[ic]->GetNbinsX(); iBin++){
        float maxList[] = {waves[ic]->GetBinContent(iBin),waves[ic]->GetBinContent(iBin+1),waves[ic]->GetBinContent(iBin+2)};
        float tempMax = *std::min_element(maxList,maxList+3);
        if (maxThreeConsec < tempMax) maxThreeConsec = tempMax;

    }
    v_max_threeConsec->push_back(maxThreeConsec);
    v_max_afterFilter->push_back(waves[ic]->GetMaximum());
    v_min_afterFilter->push_back(waves[ic]->GetMinimum());

    for(int ipulse = 0; ipulse<npulses; ipulse++){
        waves[ic]->SetAxisRange(pulseBounds[ipulse][0],pulseBounds[ipulse][1]);
        if(debug) cout<<"Chan "<<ic<<", pulse bounds: "<<pulseBounds[ipulse][0]<<" to "<<pulseBounds[ipulse][1]<<endl;
        
        //cout<<"1.1"<<endl;
        v_chan->push_back(chanArray->GetAt(ic));
        //cout<<"1.2"<<endl;
        if (numChan == 32){
            v_column->push_back(chanMap[ic][0]);
            v_row->push_back(chanMap[ic][1]);
            v_layer->push_back(chanMap[ic][2]);
            v_type->push_back(chanMap[ic][3]);
        }
        else{
            v_column->push_back(0);
            v_row->push_back(0);
            v_layer->push_back(0);
            v_type->push_back(0);
        }

        v_height->push_back(waves[ic]->GetMaximum());
        v_time->push_back(pulseBounds[ipulse][0]);
        v_time_module_calibrated->push_back(pulseBounds[ipulse][0]+channelCalibrations[ic]);
        v_area->push_back(waves[ic]->Integral());
        v_nPE->push_back((waves[ic]->Integral()/(channelSPEAreas[ic]))*(1.6/sample_rate[ic/16]));
        v_ipulse->push_back(ipulse);
        v_npulses->push_back(npulses);
        v_duration->push_back(pulseBounds[ipulse][1] - pulseBounds[ipulse][0]);
        if(ipulse>0) v_delay->push_back(pulseBounds[ipulse][0] - pulseBounds[ipulse-1][1]);
        else v_delay->push_back(1999.);
        
        //get presample info
        //pair<float,float> presampleInfo = measureSideband(ic,pulseBounds[ipulse][0]-presampleStart,pulseBounds[ipulse][0]-presampleEnd);
        //v_presample_mean->push_back(presampleInfo.first);
        //v_presample_RMS->push_back(presampleInfo.second);
        //bool quiet = (fabs(presampleInfo.first)<1. && presampleInfo.second <2.0 )&& (pulseBounds[ipulse][1] < waves[ic]->GetBinLowEdge(waves[ic]->GetNbinsX())-0.01) ;
        //v_quiet->push_back(quiet);

    }    
    
    return pulseBounds;
 
}
/*
void findTriggerCandidates(int ic,float sb_mean){
    float tstart = sideband_range[1]+1;
    int istart = waves[ic]->FindBin(tstart);
    float v;
    bool inTrigger = false;
    for (int i=istart; i<=waves[ic]->GetNbinsX(); i++) {
        v = waves[ic]->GetBinContent(i);
        if (waves[ic]->GetBinContent(i) + sb_mean >= (v_triggerThresholds->at(ic)*-1000.)){
            if (!inTrigger){
                v_triggerCandidates->push_back((float)waves[ic]->GetBinLowEdge(i));
                v_triggerCandidatesChannel->push_back(ic);
                inTrigger = true;
            }
        }
        else {
            if (inTrigger) v_triggerCandidatesEnd->push_back((float)waves[ic]->GetBinLowEdge(i));
            inTrigger = false;
        }
    }
    if (inTrigger) v_triggerCandidatesEnd->push_back((float)waves[ic]->GetBinLowEdge(waves[ic]->GetNbinsX()));

} */

vector< vector<float> > findPulses(int ic, bool applyLPFilter, int runDRS){
    
    int NconsecConfig1p6[] = {7, 7, 9, 7, 7, 5, 7, 7, 7, 4, 7, 7, 7, 8, 9, 7, 7, 4, 8, 7, 7, 8, 5, 7, 4, 4, 7, 7, 7, 7, 7, 7};
    int NconsecEndConfig1p6[] = {13, 13, 13, 13, 13, 4, 13, 13, 13, 4, 13, 13, 13, 13, 13, 13, 13, 4, 13, 13, 13, 13, 4, 13, 4, 4, 13, 13, 13, 13, 13, 13};
    float threshConfig1p6[] = {2.0, 2.0, 2.3, 2.0, 2.2, 2.0, 2.0, 2.0, 2.0, 2.0, 2.2, 2.0, 2.0, 2.0, 2.3, 2.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.7, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0};

    int NconsecConfig1p6Filtered[] = {3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3};
    int NconsecEndConfig1p6Filtered[] = {8, 8, 8, 8, 8, 4, 8, 8, 8, 4, 8, 8, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 4, 8, 4, 4, 8, 8, 8, 8, 8, 8};
    float threshConfig1p6Filtered[] = {1.1,1.3,1.2,1.2,1.4,1.4,1.3,1.3,1.5,1.5,1.3,1.3,1.2,1.3,1.7,2.5,1.1,1.7,1.5,1.5,1.4,1.7,2.2,1.3,1.2,1.4,1.6,1.3,1.6,1.3,1.3,1.5};

    int NconsecConfig0p8[] = {3, 3, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 3, 3, 3, 3};
    int NconsecEndConfig0p8[] = {6, 6, 6, 6, 6, 3, 6, 6, 6, 3, 6, 6, 6, 6, 6, 6, 6, 3, 6, 6, 6, 6, 3, 6, 3, 3, 6, 6, 6, 6, 6, 6};
    float threshConfig0p8[] = {2.0, 2.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.0, 2.0, 2.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.5, 2.0, 2.0, 2.0, 2.0, 3.0, 2.0, 2.5, 2.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0};

    int Nconsec = 6;
    int NconsecEnd = 12;
    float thresh = 20.0;
    float lowThresh = 15.0;
    int istart = 80;
    /*
    if (darkRate){
        int Nconsec = 3;
        float thresh = 20.0;
        float lowThresh = 15.0;
        int istart = 80;
    }
    else{
        int Nconsec = 6;
        float thresh = 100.0;
        float lowThresh = 50.0;
	int istart = 0;
    }*/
    //float thresh = 2.0;
    //float lowThresh = 1.0;
    /*
    if (runDRS >= 0 || int(sample_rate[ic/16]/0.4+0.1) == 4)
    {
        Nconsec = NconsecConfig1p6[ic];
        NconsecEnd = NconsecEndConfig1p6[ic];
        thresh = threshConfig1p6[ic];
        lowThresh = thresh - rmsCalib[ic]/2;
    }
    else if (int(sample_rate[ic/16]/0.4+0.1) == 2)
    {
        Nconsec = NconsecConfig0p8[ic];
        NconsecEnd = NconsecEndConfig0p8[ic];
        thresh = threshConfig0p8[ic];
        lowThresh = thresh - rmsCalib[ic];
    }
    if (applyLPFilter){
        Nconsec = 3;
        if (Nconsec<2) Nconsec = 2;
        thresh = threshConfig1p6Filtered[ic];
        lowThresh = threshConfig1p6Filtered[ic];       
    }*/
     
    vector<vector<float> > bounds;
    //float tstart = sideband_range[1]+1;
    //int istart = waves[ic]->FindBin(tstart);
    //int istart = 0;

    bool inpulse = false;
    int nover = 0;
    int nunder = 0;
    int i_begin = istart;
    //int i_begin = 0;
    int i_stop_searching = waves[ic]->GetNbinsX()-Nconsec;
    int i_stop_final_pulse = waves[ic]->GetNbinsX();
   
    //cout<<"istart = "<<istart<<" , i_stop_searching = "<<i_stop_searching;
 

    for (int i=istart; i<i_stop_searching || (inpulse && i<i_stop_final_pulse); i++) {
        float v = waves[ic]->GetBinContent(i);
        //if (ic==0 && i==394) cout<<"ic = "<<ic<<" , i = "<<i<<" , v = "<<v<<endl;
        if (!inpulse) {
            if (v<lowThresh) {   
                nover = 0;     // If v dips below the low threshold, store the value of the sample index as i_begin
                i_begin = i;
            }
	    else if (v>=thresh){
                nover++;       // If v is above the threshold, start counting the number of sample indices
            }
            else{
                i_begin = i;
            }
            
            if (nover>=Nconsec){   // If v is above threshold for long enough, we now have a pulse!
		inpulse = true;    // Also reset the value of nunder
		nunder = 0;
            }
        }
	else {  // Called if we have a pulse
	    if (v<thresh) nunder++;   // If the pulse dips below the threshold, sum the number of sample indices for which this is true
	    else if (v >= thresh+rmsCalib[ic]/2){
	        nunder = 0;           // If the pulse stays above threshold, set nunder back to zero
	    }
            // If the nunder is above or equal to 12 (or we reach the end of the file) store the values of the pulse bounds
            if (nunder>=NconsecEnd || i==(i_stop_final_pulse-1)) { 
		bounds.push_back({(float)waves[ic]->GetBinLowEdge(i_begin), (float)waves[ic]->GetBinLowEdge(i+1)-0.01});
		if(debug) cout<<"i_begin, i: "<<i_begin<<" "<<i<<endl;       // i_begin is the 
                inpulse = false;
		nover = 0;
		nunder = 0;
		i_begin = i;

                
             
	    }
	}
    }

    return bounds;
}

void prepareOutBranches(){
    TBranch * b_triggerThresholds = outTree->Branch("triggerThreshold",&v_triggerThresholds);
    TBranch * b_triggerEnable = outTree->Branch("triggerEnable",&v_triggerEnable);
    TBranch * b_triggerMajority = outTree->Branch("triggerMajority",&v_triggerMajority);
    TBranch * b_triggerLogic = outTree->Branch("triggerLogic",&v_triggerLogic);
    TBranch * b_chan = outTree->Branch("chan",&v_chan);
    TBranch * b_height = outTree->Branch("height",&v_height);
    TBranch * b_area = outTree->Branch("area",&v_area);
    TBranch * b_nPE = outTree->Branch("nPE",&v_nPE);
    TBranch * b_ipulse = outTree->Branch("ipulse",&v_ipulse);
    TBranch * b_npulses = outTree->Branch("npulses",&v_npulses);
    TBranch * b_time = outTree->Branch("time",&v_time);
    TBranch * b_duration = outTree->Branch("duration",&v_duration);
    TBranch * b_delay = outTree->Branch("delay",&v_delay);
    TBranch * b_present_b0 = outTree->Branch("present_b0",&present_b0,"present_b0/O");
    TBranch * b_present_b1 = outTree->Branch("present_b1",&present_b1,"present_b1/O");
    TBranch * b_event_time_b0 = outTree->Branch("event_time_b0",&event_time_b0,"event_time_b0/L");
    TBranch * b_event_time_b1 = outTree->Branch("event_time_b1",&event_time_b1,"event_time_b1/L");
    TBranch * b_groupTDC_b0 = outTree->Branch("groupTDC_b0",&v_groupTDC_b0);
    TBranch * b_groupTDC_b1 = outTree->Branch("groupTDC_b1",&v_groupTDC_b1);
    TBranch * b_max = outTree->Branch("max",&v_max);

    outTree->SetBranchAddress("triggerThreshold",&v_triggerThresholds,&b_triggerThresholds);
    outTree->SetBranchAddress("triggerLogic",&v_triggerLogic,&b_triggerLogic);
    outTree->SetBranchAddress("triggerMajority",&v_triggerMajority,&b_triggerMajority);
    outTree->SetBranchAddress("triggerEnable",&v_triggerEnable,&b_triggerEnable);
    outTree->SetBranchAddress("chan",&v_chan,&b_chan);
    outTree->SetBranchAddress("height",&v_height,&b_height);
    outTree->SetBranchAddress("area",&v_area,&b_area); 
    outTree->SetBranchAddress("nPE",&v_nPE,&b_nPE);   
    outTree->SetBranchAddress("ipulse",&v_ipulse,&b_ipulse);
    outTree->SetBranchAddress("npulses",&v_npulses,&b_npulses);
    outTree->SetBranchAddress("time",&v_time,&b_time);
    outTree->SetBranchAddress("duration",&v_duration,&b_duration);
    outTree->SetBranchAddress("delay",&v_delay,&b_delay);
    outTree->SetBranchAddress("present_b0",&present_b0,&b_present_b0);
    outTree->SetBranchAddress("present_b1",&present_b1,&b_present_b1);
    outTree->SetBranchAddress("event_time_b0",&event_time_b0,&b_event_time_b0);
    outTree->SetBranchAddress("event_time_b1",&event_time_b1,&b_event_time_b1);
    outTree->SetBranchAddress("groupTDC_b0",&v_groupTDC_b0,&b_groupTDC_b0);
    outTree->SetBranchAddress("groupTDC_b1",&v_groupTDC_b1,&b_groupTDC_b1);
    outTree->SetBranchAddress("max",&v_max,&b_max);

}

void clearOutBranches(){
    v_max->clear();
    v_chan->clear();
    v_height->clear();
    v_area->clear();
    v_nPE->clear();
    v_ipulse->clear();
    v_npulses->clear();
    v_time->clear();
    v_duration->clear();
    v_delay->clear();
    v_groupTDC_b0->clear();
    v_groupTDC_b1->clear();
}

void loadBranchesMilliDAQ(){
    inTree->SetBranchAddress("event", &evt);
    for(int ic=0;ic<numChan;ic++) waves.push_back(new TH1D());

}

void loadWavesMilliDAQ(){
    int board,chan;
    for(int i=0;i<numChan;i++){
        if(waves[i]) delete waves[i];
	//board = i<=15 ? 0 : 1;
	board = 0;
        chan = i<=15 ? i : i-16;
        //waves[i] = (TH1D*)evt->GetWaveform(board, chan, Form("h%i",i));
        waves[i] = (TH1D*)evt->GetWaveform(board, chan, Form("digitizers[%i].waveform[%i]",board,i));  // Investigate this more....
        //waves[i] = (TH1D*)evt->GetWaveform(board,chan,evt->digitizers[board].waveform[chan]);
        //cout<<"board = "<<board<<" , chan = "<<chan<<" , waves  = "<<waves[i]<<endl;
        //cout<<"board = "<<board<<" , chan = "<<chan<<" , raw waveform = "<<evt->digitizers[1].waveform[i]<<endl;
    }
}


