#ifndef OFFLINE_FACTORY_H
#define OFFLINE_FACTORY_H

#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip>
#include <time.h>
#include <stdexcept>
#include <sys/stat.h>
#include <sys/types.h>
#include "./interface/json.h"
#include <chrono>
#include <ctime>

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

#include "interface/GlobalEvent.h"
#include "interface/DemonstratorConfiguration.h"
#include "interface/V1743Configuration.h"
#include "interface/V1743Event.h"

#include <string>
#include <sys/types.h>
#include <sys/stat.h>
#include <fstream>
#include <iostream>
using namespace std;
//Use struct to organise tree contents
struct offline_tree_{
    int event ;
    Long64_t runNumber;
    Long64_t fileNumber;
    std::vector<Long64_t> event_time;
    double event_time_fromTDC;
    std::vector<Long64_t> present;
    std::vector<Long64_t> event_trigger_time_tag;
    ulong daqFileOpen; //unix time
    ulong daqFileClose; //unix time
    int t_since_fill_start;
    int t_since_fill_end;
    int t_until_next_fill;
    string event_t_string;
    bool boardsMatched;
    int DAQEventNumber;
    int maxPulseIndex;
    bool goodRunLoose=false;
    bool goodRunMedium=false;
    bool goodRunTight=false;
    bool goodSingleTrigger=false;

    //Pulse Finding Info
    std::vector<int> nConsecSamples_;
    std::vector<int> nConsecSamplesEnd_;
    std::vector<float> highThreshold_;
    std::vector<float> lowThreshold_;

    //Luminosity Info
    float lumi;
    int fillId;
    TString beamType;
    float beamEnergy; 
    float betaStar;
    bool beamOn; 
    ulong fillStart; //milliseconds since unix epoch
    ulong fillEnd; //milliseconds since unix epoch
    bool beamInFill;

    //pulse vectors
    vector<int> v_pulseIndex;
    vector<int> v_npulses;
    vector<int> v_ipulse;
    vector<int> v_chan;
    vector<int> v_chanWithinBoard;
    vector<int> v_board;
    vector<int> v_layer;
    vector<int> v_row;
    vector<int> v_column;
    vector<int> v_type;
    vector<float> v_height;
    vector<float> v_time;
    vector<float> v_timeFit;
    vector<float> v_triggerCandidates;
    vector<float> v_triggerCandidatesEnd;
    vector<int> v_triggerCandidatesChannel;
    vector<float> v_time_module_calibrated;
    vector<float> v_timeFit_module_calibrated;
    vector<float> v_delay;
    vector<float> v_area;
    vector<bool> v_pickupFlag;
    vector<bool> v_pickupFlagTight;
    vector<float> v_nPE;
    vector<int> v_riseSamples;
    vector<int> v_fallSamples;
    vector<float> v_duration;
    vector<bool> v_quiet;
    vector<float> v_presample_mean;
    vector<float> v_presample_RMS;
    vector<float> v_dynamicPedestal;
    vector<float> v_sideband_mean;
    vector<float> v_sideband_RMS;
    vector<float> v_sideband_mean_perFile;
    vector<float> v_triggerBand_mean;
    vector<float> v_triggerBand_max;
    vector<float> v_triggerBand_maxTime;
    vector<float> v_triggerBand_RMS;
    vector<float> v_sideband_mean_raw;
    vector<float> v_sideband_RMS_raw;
    vector<Long64_t> v_groupTDC_g0;
    vector<Long64_t> v_groupTDC_g1;
    vector<Long64_t> v_groupTDC_g2;
    vector<Long64_t> v_groupTDC_g3;
    vector<Long64_t> v_groupTDC_g4;
    vector<Long64_t> v_groupTDC_g5;
    vector<Long64_t> v_groupTDC_g6;
    vector<Long64_t> v_groupTDC_g7;
    //vector<float> v_bx;
    //vector<float> v_by;
    //vector<float> v_bz;
    vector<float> v_max;
    //vector<float> v_min;
    vector<float> v_max_afterFilter;
    vector<float> v_max_threeConsec;
    vector<float> v_triggerThresholds;
    vector<bool> v_triggerEnable;
    vector<int> v_triggerLogic;
    vector<int> v_triggerMajority;
    vector<int> v_triggerPolarity;
    vector<float> v_min_afterFilter;
    vector<int> v_iMaxPulseLayer;
    vector<float> v_maxPulseTime;
    vector<float> v_prePulseMean;
    vector<float> v_prePulseRMS;

    ulong tClockCycles;
    float tTime;
    float tStartTime;
    float tTrigger;
    float tTimeDiff;
    float tMatchingTimeCut;
    int tEvtNum;
    int tRunNum;
    int tTBEvent;
    //Trigger tree members

    //for sim files
    Double_t eventWeight;

};
//Offline factory class used to produce offline tree output
class OfflineFactory {
public:
  OfflineFactory(TString,TString,TString,bool,bool,bool);
  OfflineFactory(TString,TString,TString, bool, bool, bool, int, int);
    // virtual ~OfflineFactory();
    void makeOutputTree();
    void loadJsonConfig(string);
    void getLumis(string);
    void checkGoodRunList(string);
    void getEventLumis();
    void setGoodRuns();
    void readMetaData();
    vector<vector<pair<float,float> > > readWaveDataPerEvent(int);
    //        void defineColors(vector<int>, vector<TColor*>, vector<float>, vector<float>, vector<float>);
    //vector<int>colors, vector<TColor*> palette, vector<float> reds, vector<float> greens, vector<float> blues
    void h1cosmetic(TH1D*,int,vector<int> &);
    void displayEvent(int,vector<vector<pair<float,float> > >&,TString);
    void displaychannelEvent(int,vector<vector<pair<float,float> > >&,TString);
    void displayEvents(vector<int> &,TString);
    void readWaveData();
    void addFriendTree();
    void setFriendFile(TString);
    void writeOutputTree();
    void process();
    void process(TString,TString);
    void process(TString,TString,int, int);
    void processDisplays(vector<int>&,TString);
    void processDisplays(vector<int>&,TString,TString);
    void processDisplays(vector<int>&,TString,TString,int, int);
    TString getVersion();
    std::vector<std::string> splitLumiContents(std::string);

private:
    void prepareOutBranches();
    void resetOutBranches();
    void prepareWave(int);
    pair<float,float> measureSideband(int);
    vector<pair<float,float>> findPulses(int);
    vector<pair<float,float>> processChannel(int);
    const pair<float, float> getPrePulseVar(TH1D*, float);
    void loadBranches();
    void loadWavesMilliDAQ();
    void loadWavesDRS();
    void validateInput();
    void writeVersion();
    ulong getUnixTime(TString&);
    void setTotalLumi();
    void findExtrema();


    float sideband_range[2] = {0,50};
    TString versionShort;
    TString versionLong = "asddsf";
    std::string goodRunTag;
    float sampleRate = 1.6;
    bool applyLPFilter = false;
    TString inFileName;
    TString outFileName;
    TString friendFileName = "";
    TString appendToTag;
    int runNumber;
    int fileNumber;
    bool isDRS;
    bool isSlab;
    bool isSim;
    mdaq::GlobalEvent * evt = new mdaq::GlobalEvent();
    mdaq::DemonstratorConfiguration * cfg = new mdaq::DemonstratorConfiguration();
    TString* fileOpenTime;
    TString* fileCloseTime;
    vector<float> highThresh = {15.}; //TODO: do these need to be vectors? They are the same for all channels currently
    vector<float> lowThresh = {5.};
    vector<int> nConsecSamples = {3};
    vector<int> nConsecSamplesEnd = {1};
    vector< vector<int> > chanMap;
    vector<float> timingCalibrations;
    vector<float> pedestals;
    vector<float> speAreas;
    TArrayI * chanArray;
    TArrayI * boardArray;
    int dynamicPedestalTotalSamples = 400;
    int dynamicPedestalConsecutiveSamples = 16;
    float dynamicPedestalGranularity = 0.25;
    float tdcCorrection[6] = {0}; //set to max number of boards
    int prePulseRange = 30; //number of samples to use when calculating prepulse mean/RMS

    bool goodRunLoose;
    bool goodRunMedium;
    bool goodRunTight;
    bool goodSingleTrigger;

    //file Lumi info
    vector<float> v_lumi;
    vector<int> v_fillId;
    vector<TString> v_beamType;
    vector<float> v_beamEnergy; 
    vector<float> v_betaStar;
    vector<bool> v_beamOn; 
    vector<ulong> v_fillStart; 
    vector<ulong> v_fillEnd;
    vector<ulong> v_stableBeamStart;
    vector<ulong> v_stableBeamEnd;
    vector<bool> v_beamInFill;

    //Declare global variables
    double arrayVoltageDRS[100][1024];
    int numChan;
    int numBoards;
    int boardsDRS[100];
    int chansDRS[100];
    Long64_t initTDC=-1;
    Long64_t initSecs=-1;
    Long64_t prevTDC=-1;
    int nRollOvers=0;
    vector<TH1D*> waves;
    TTree * inTree;
    TFile * inFile;
    TFile * outFile;
    TFile * matchedFile;
    TTree * outTree;
    TTree * trigMetaData;
    TTree * trigMetaDataCopy;

    bool writeTriggerMetaData=false;
    offline_tree_ outputTreeContents;
    bool triggerFileMatched;
    vector<TColor *> palette;
    vector<int> colors;
    //Trigger friend variables
    ulong tClockCycles = 0;
    float tTime = -1.;
    float tStartTime = -1.;
    float tTrigger = -1.;
    float tTimeDiff = -1.;
    float tMatchingTimeCut = -1.;
    int tEvtNum = 0;
    int tRunNum = 0;
    int tTBEvent = 0;
    int totalPulseCount = 0;

    Long64_t firstTDC_time=10e15;
    Long64_t lastTDC_time=-1;

    //bool to print only the first warning about file lumi
    bool firstWarning = true;

    //settings to turn on variable pulse finding height based on online threshold
    bool variableThresholds = true;
    int thresholdDecrease = 5;

    //variables for sim only
    Double_t eventWeight;
    
};
#endif
