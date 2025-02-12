#include "TFile.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TChain.h"
#include "TDirectory.h"
#include "TGraph.h"
#include "TKey.h"
#include <iostream>
#include <utility>
#include <cmath>
#include <dirent.h>
#include <fnmatch.h>
#include <set>
#include "../../interface/json.h"

using namespace std;

struct globalHist{
    float max2, min2;
    float max3, min3;
    float maxRatio;
    float nPEMaxRatio;
    float maxRatioTripleRate, maxRatioDoubleRate;
    float maxRatioErr;
    float heightFitLambda, heightFitMu, heightFitSigma, heightFitChi;
    float heightFitLambdaErr, heightFitMuErr, heightFitSigmaErr, heightFitChiErr;
    float npeFitLambda, npeFitMu, npeFitSigma, npeFitChi;
    float npeFitLambdaErr, npeFitMuErr, npeFitSigmaErr, npeFitChiErr;
};

struct passingEvent{
    bool tripleCoincidence=false;
    vector<float> primaryNPE = {};
    vector<float> secondaryNPE = {};
    vector<float> primaryHeight = {};
    vector<float> secondaryHeight = {};
    vector<float> primaryChannel = {};
    vector<float> secondaryChannel = {};
    vector<pair<float, float> > primaryTime = {};
    vector<pair<float, float> > secondaryTime = {};
};

//double variableHeightBins[32] = {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 270, 280, 300, 350, 400, 450, 500, 550, 600, 700, 800, 1000, 1400};
//double variableHeightBins[28] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 40, 60, 80, 100, 150, 200, 250, 300, 400, 500, 1400};
double variableHeightBins[36] = {0, 5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 18, 19, 20, 22.5, 25, 27.5, 30, 50, 75, 100, 200, 300, 400, 500, 1400};

double variableNPEBins[15] = {0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0};

float heightFitBinsLow[64] = {10, 10, 10, 10, 10, 10, 12, 10,
                            10, 10, 10, 10, 10, 10, 10, 15,
                            10, 15, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10,
                            10, 12, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 12, 10, 10, 10, 10,
                            10, 10, 10, 10, 15, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10};

float heightFitBinsHigh[64] = {100, 100, 100, 100, 100, 100, 100, 100,
                            100, 100, 100, 100, 100, 100, 100, 500,
                            100, 500, 100, 100, 100, 100, 100, 100,
                            100, 100, 100, 100, 100, 100, 100, 100,
                            100, 500, 100, 100, 100, 100, 100, 100,
                            100, 100, 100, 500, 100, 100, 100, 100,
                            100, 100, 100, 100, 500, 100, 100, 100,
                            100, 100, 100, 100, 100, 100, 100, 100};

float npeFitBinsLow[64] = {0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1}; //normal nPE bins low

/*float npeFitBinsLow[64] = {0.1, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1};*/ //tight nPE bins low

/*float npeFitBinsLow[64] = {0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 0.0, 0.0, 
                        0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1};*/ //loose nPE bins low


float npeFitBinsHigh[64] = {10, 10, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10,
                            10, 10, 10, 10, 10, 10, 10, 10};

class channelHistsBase {
public:
    int channel;  // Common member variable
    TH1F* hTime;
    TH3F* h;      // Base pointer to the main histogram
    TH3F* hScaled;
    TH1F* hProbeNPE;
    TH1F* hTag1NPE;
    TH1F* hTag2NPE;
    TH3F* hHeight;
    TH2F* hnPEvHeight;

    // Constructor initializes the channel
    channelHistsBase(int channel) : channel(channel), h(nullptr) {}

    // Virtual destructor to ensure proper cleanup in derived classes
    virtual ~channelHistsBase() {}

    // Pure virtual function to enforce histogram initialization in derived classes
    virtual void initializeHistograms() = 0;
};

class channelHistsDouble : public channelHistsBase {
public:
    TH1F* hTimeDouble;
    TH3F* hDouble;
    TH3F* hDoubleScaled;
    TH1F* hProbeNPE2;
    TH1F* hTag1NPE2;
    TH1F* hTag2NPE2;
    TH3F* hDoubleHeight;
    TH2F* hDoubleNPEvHeight;

    channelHistsDouble(int channel) : channelHistsBase(channel), hDouble(nullptr) {
        initializeHistograms();
    }

    void initializeHistograms() override {
        hTimeDouble = new TH1F(TString::Format("hTimeDouble_%i", channel), "Time of Run (s)", 1, 0, 1); 
        hDouble = new TH3F(TString::Format("hDouble_%i", channel), "nPE Double Coincident Hits", sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins);
        hDoubleScaled = new TH3F(TString::Format("hDoubleScaled_%i", channel), "nPE Double Coincident Hits w/ Prescale", sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins);
        hProbeNPE2 = new TH1F(TString::Format("hProbeNPE2_%i", channel), "nPE of Probe Channel for Double Coincident Hits", 1000, 0, 100);
        hTag1NPE2 = new TH1F(TString::Format("hTag1NPE2_%i", channel), "nPE of 1st Tag Channel for Double Coincident Hits", 1000, 0, 100);
        hTag2NPE2 = new TH1F(TString::Format("hTag2NPE2_%i", channel), "nPE of 2nd Tag Channel for Double Coincident Hits", 1000, 0, 100);
        hDoubleHeight = new TH3F(TString::Format("hDoubleHeight_%i", channel), "Height of Double Coincident Hits", sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins, sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins, sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins);
        hDoubleNPEvHeight = new TH2F(TString::Format("hDoubleNPEvHeight_%i", channel), "nPE vs Height of Double Coincident Hits", sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins);
        hTime = hTimeDouble;
        h = hDouble;  // Set the base pointer to point to hDouble
        hScaled = hDoubleScaled;
        hProbeNPE = hProbeNPE2;
        hTag1NPE = hTag1NPE2;
        hTag2NPE = hTag2NPE2;
        hHeight = hDoubleHeight;
        hnPEvHeight = hDoubleNPEvHeight;

    }
};

class channelHistsTriple : public channelHistsBase {
public:
    TH1F* hTimeTriple;
    TH3F* hTriple;
    TH3F* hTripleScaled;
    TH1F* hProbeNPE3;
    TH1F* hTag1NPE3;
    TH1F* hTag2NPE3;
    TH3F* hTripleHeight;
    TH2F* hTripleNPEvHeight;

    channelHistsTriple(int channel) : channelHistsBase(channel), hTriple(nullptr) {
        initializeHistograms();
    }

    void initializeHistograms() override {
        hTimeTriple = new TH1F(TString::Format("hTimeTriple_%i", channel), "Time of Run (s)", 1, 0, 1); 
        hTriple = new TH3F(TString::Format("hTriple_%i", channel), "nPE Triple Coincident Hits", sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins);
        hTripleScaled = new TH3F(TString::Format("hTripleScaled_%i", channel), "nPE Triple Coincident Hits w/ Prescale", sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins);
        hProbeNPE3 = new TH1F(TString::Format("hProbeNPE3_%i", channel), "nPE of Probe Channel for Triple Coincident Hits", 1000, 0, 100);
        hTag1NPE3 = new TH1F(TString::Format("hTag1NPE3_%i", channel), "nPE of 1st Tag Channel for Triple Coincident Hits", 1000, 0, 100);
        hTag2NPE3 = new TH1F(TString::Format("hTag2NPE3_%i", channel), "nPE of 2nd Tag Channel for Triple Coincident Hits", 1000, 0, 100);
        hTripleHeight = new TH3F(TString::Format("hTripleHeight_%i", channel), "Height of Triple Coincident Hits", sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins, sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins, sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins);
        hTripleNPEvHeight = new TH2F(TString::Format("hTripleNPEvHeight_%i", channel), "nPE vs Height of Triple Coincident Hits", sizeof(variableNPEBins)/sizeof(variableNPEBins[0])-1, variableNPEBins, sizeof(variableHeightBins)/sizeof(variableHeightBins[0])-1, variableHeightBins);

        hTime = hTimeTriple;
        h = hTriple;  // Set the base pointer to point to hTriple
        hScaled = hTripleScaled;
        hProbeNPE = hProbeNPE3;
        hTag1NPE = hTag1NPE3;
        hTag2NPE = hTag2NPE3;
        hHeight = hTripleHeight;
        hnPEvHeight = hTripleNPEvHeight;
    }
};

float getRunTime(TChain* tchain, ULong_t* daqFileOpen, ULong_t* daqFileClose){
    ulong minTime = 10e15;
    ulong maxTime = 0;
    for (int ievent=0; ievent<tchain->GetEntries(); ievent++){
        tchain->GetEntry(ievent);
        if(*daqFileOpen < minTime) minTime = *daqFileOpen;
        if(*daqFileClose > maxTime) maxTime = *daqFileClose;
        //std::cout << "minTime: " << *daqFileOpen << ", maxTime: " << *daqFileClose << std::endl;
    }
    //std::cout << "max time: " << maxTime << ", min time: " << minTime << std::endl;
    float totalTime = (float)(maxTime - minTime);
    return totalTime;
}

std::pair<int, int> getCoincidentChannels(int chan){

    vector<pair<int, int> > doubleChannels = {
        {16, 32}, {17, 33}, {18, 34}, {19, 35}, {20, 36}, {21, 37}, {22, 38}, {23, 39},
        {24, 40}, {25, 41}, {26, 42}, {27, 43}, {28, 44}, {29, 45}, {30, 46}, {31, 47},

        {32, 48}, {33, 49}, {34, 50}, {35, 51}, {36, 52}, {37, 53}, {38, 54}, {39, 55},
        {40, 56}, {41, 57}, {42, 58}, {43, 59}, {44, 60}, {45, 61}, {46, 62}, {47, 63},

        {0, 16}, {1, 17}, {2, 18}, {3, 19}, {4, 20}, {5, 21}, {6, 22}, {7, 23},
        {8, 24}, {9, 25}, {10, 26}, {11, 27}, {12, 28}, {13, 29}, {14, 30}, {15, 31},

        {16, 32}, {17, 33}, {18, 34}, {19, 35}, {20, 36}, {21, 37}, {22, 38}, {23, 39},
        {24, 40}, {25, 41}, {26, 42}, {27, 43}, {28, 44}, {29, 45}, {30, 46}, {31, 47}
    };

    return doubleChannels[chan];
}

std::vector<std::vector<int> > loadChanMap(string configFileName){
    std::string json;
    std::vector<std::vector<int> > chanMap = {};

    if (configFileName.find("{") != std::string::npos){
        json = configFileName;
    }
    else{
        std::ifstream t(configFileName);
        std::stringstream buffer;
        buffer << t.rdbuf();
        json = buffer.str();
    }

    Json::Reader reader;
    Json::Value jsonRoot;
    bool parseSuccess = reader.parse(json, jsonRoot, false);
    if (parseSuccess)
        {
            if (json.find("chanMap") != std::string::npos){
                const Json::Value chan0 = jsonRoot["chanMap"];
                for ( int index = 0; index < chan0.size(); ++index ){
                    std::vector<int> chanMapPerChan;
                    for ( int index2 = 0; index2 < chan0[index].size(); ++index2 ){
                        chanMapPerChan.push_back(chan0[index][index2].asInt());
                    }
                    chanMap.push_back(chanMapPerChan);
                }
                std::cout << "Loaded channel map" << std::endl;
            }
        }
    else{
        cout << "Error loading the channel map " << configFileName << endl;
    }

    return chanMap;
}

bool checkTimingDistance(pair<float, float>& t1, pair<float, float>& t2, float threshold){
    // check if ranges overlap
    if(
        (t2.first <= t1.second && t2.first >= t1.first) || 
        (t1.first <= t2.second && t1.first >= t2.first) ||
        (t2.second <= t1.second && t2.second >= t1.first) ||
        (t1.second <= t2.second && t1.second >= t2.first)
    ){
        return true;
    }
    //check if within threshold
    if(
        abs(t1.first - t2.first) <= threshold ||
        abs(t1.second - t2.first) <= threshold ||
        abs(t1.first - t2.second) <= threshold ||
        abs(t1.second - t2.second) <= threshold
    ){
        return true;
    }
    return false;
}

float listMatchingFiles(TChain& mychain, const std::string& directory, const std::string& pattern, int numFiles=-1) {

    int fileCnt = 0;
    float totalTime = 0;


    std::cout << "Searching for files matching " << pattern << " in directory " << directory << std::endl;

    DIR* dir = opendir(directory.c_str());
    if (!dir) {
        std::cerr << "Failed to open directory: " << directory << std::endl;
        return totalTime;
    }

    ULong_t daqFileOpen;
    ULong_t daqFileClose;

    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        // Only process regular files (not directories)
        if(numFiles > 0 && fileCnt > numFiles) break;
        //std::cout << entry->d_name << std::endl;
        if (entry->d_type == DT_REG) {
            // Match filename with the given pattern using fnmatch
            if (fnmatch(pattern.c_str(), entry->d_name, 0) == 0) {
                //std::cout << "Found matching file: " << entry->d_name << std::endl;
                TFile* myfile = TFile::Open(TString(directory+entry->d_name));
                if (myfile->IsZombie()){
                    myfile->Close();
                    continue;
                }
                TTree* mytree = (TTree*)myfile->Get("t");
                mytree->SetBranchAddress("daqFileOpen", &daqFileOpen);
                mytree->SetBranchAddress("daqFileClose", &daqFileClose);
                mytree->GetEntry(0);
                totalTime = totalTime + (float)(daqFileClose - daqFileOpen);
                //std::cout << "total time " << totalTime << std::endl;
                mychain.Add(TString(directory + entry->d_name));
                myfile->Close();
                fileCnt++;
            }
        }
    }

    closedir(dir);

    return totalTime;
}

void coincidenceCounts(TFile *fout, int run, float prescale, std::vector<channelHistsBase*> &h_channels, std::vector<std::vector<int>> chanMap){
    // set time threshold for pulses to be within
    float threshold = 100.0;
    
    //output file for printing the times and counts
    std::ofstream outFile("outputTriggerEfficiency.txt", std::ios::app);

    //Define variables that will be used
    vector<float>* v_nPE = nullptr;
    vector<bool>* v_pickupFlagTight = nullptr;
    vector<float>* v_time = nullptr;
    vector<int>* v_chan = nullptr;
    vector<float>* v_duration = nullptr;
    vector<int>* v_ipulse = nullptr;
    vector<float>* v_height = nullptr;
    vector<int>* v_layer = nullptr;
    vector<int>* v_col = nullptr;
    vector<int>* v_row = nullptr;
    vector<int>* v_type = nullptr;
    float tTrigger;
    bool boardsMatched;
    ULong_t daqFileOpen;
    ULong_t daqFileClose;

    // General directory to get files
    TString s_directory = "/store/user/milliqan/triggerEfficiency/v2/";
    //TString s_directory = "/store/user/milliqan/trees/v35/bar/";

    //TString subDir = TString::Format("%i", (run / 100) * 100);

    //s_directory = s_directory + "/" + subDir + "/";

    // Find double coincidence
    TChain* mychain = new TChain("t");
    TString fileStr = TString::Format("MilliQan_Run%i.*.root", run);


    float runTime = listMatchingFiles(*mychain, s_directory.Data(), fileStr.Data());


    mychain->SetBranchAddress("nPE", &v_nPE);
    mychain->SetBranchAddress("pickupFlagTight", &v_pickupFlagTight);
    mychain->SetBranchAddress("boardsMatched", &boardsMatched);
    mychain->SetBranchAddress("daqFileOpen", &daqFileOpen);
    mychain->SetBranchAddress("daqFileClose", &daqFileClose);
    mychain->SetBranchAddress("timeFit_module_calibrated", &v_time);
    mychain->SetBranchAddress("chan", &v_chan);
    mychain->SetBranchAddress("ipulse", &v_ipulse);
    mychain->SetBranchAddress("duration", &v_duration);
    mychain->SetBranchAddress("tTrigger", &tTrigger);
    mychain->SetBranchAddress("height", &v_height);
    mychain->SetBranchAddress("layer", &v_layer);
    mychain->SetBranchAddress("row", &v_row);
    mychain->SetBranchAddress("column", &v_col);
    mychain->SetBranchAddress("type", &v_type);

    int nEntries = mychain->GetEntries();

    cout << "There are " << nEntries <<" coincidence events" << endl;
    if (nEntries == 0) return;

    cout << "Total Run Time: " << runTime <<  endl;

    for(int ievent=0; ievent < nEntries; ievent++){

        if (ievent%10000==0) std::cout << "Processing coincidence event " << ievent << std::endl;

        mychain->GetEntry(ievent);

        passingEvent savedPulses[64];
        
        if(!boardsMatched) continue;
        //if(tTrigger != 8192) continue;


        //check for pulses in double/triple coincidence
        for(int ipulse=0; ipulse < v_nPE->size(); ipulse++){

            bool this_pickup = v_pickupFlagTight->at(ipulse);
            if (this_pickup) continue;

            int this_pulse = v_ipulse->at(ipulse);
            if(this_pulse != 0) continue;

            if(v_height->at(ipulse) < 8) continue;

            if(v_height->at(ipulse) < 8) continue;

            float this_time = v_time->at(ipulse);
            if(this_time < 1000 || this_time > 1500) continue;
            //if(this_time < 500 || this_time > 2000) continue; //loose selection
            //if(this_time < 1200 || this_time > 1400) continue; //tight selection


            int this_chan = v_chan->at(ipulse);
            if (this_chan==78) this_chan = 24;
            if (this_chan==79) this_chan = 25;

            float this_duration = v_duration->at(ipulse);
            float end_time = this_time + this_duration;
            //cout << "time, duration, end time: " << this_time << ", " << this_duration << ", " << end_time << endl;

            int this_col = v_col->at(ipulse);
            int this_row = v_row->at(ipulse);
            int this_layer = v_layer->at(ipulse);
            int this_type = v_type->at(ipulse);

            if (this_type != 0) continue;

            int iLayer = -1;
            int iCol = -1;
            int iRow = -1;
            int iType = -1;
            for(int ichannel=0; ichannel < 64; ichannel++){

                //pair<int, int> double_coincidence = getCoincidentChannels(ichannel);
                
                //check for the same row/col layer and type==0, col, row, layer, type
                if(ichannel == 24){
                    iCol = chanMap[78][0];
                    iRow = chanMap[78][1];
                    iLayer = chanMap[78][2];
                    iType = chanMap[78][3];
                }
                else if (ichannel == 25){
                    iCol = chanMap[79][0];
                    iRow = chanMap[79][1];
                    iLayer = chanMap[79][2];
                    iType = chanMap[79][3];
                }
                else{
                    iCol = chanMap[ichannel][0];
                    iRow = chanMap[ichannel][1];
                    iLayer = chanMap[ichannel][2];
                    iType = chanMap[ichannel][3];
                }

                if (this_col != iCol) continue;
                if (this_row != iRow) continue;

                if(this_chan == ichannel){
                    savedPulses[ichannel].primaryTime.push_back(pair<float, float>(this_time, end_time));
                    savedPulses[ichannel].primaryNPE.push_back(v_nPE->at(ipulse));
                    savedPulses[ichannel].primaryHeight.push_back(v_height->at(ipulse));     
                    savedPulses[ichannel].primaryChannel.push_back(this_chan);            
                }
                else{
                    savedPulses[ichannel].secondaryTime.push_back(pair<float, float>(this_time, end_time));
                    savedPulses[ichannel].secondaryNPE.push_back(v_nPE->at(ipulse));
                    savedPulses[ichannel].secondaryHeight.push_back(v_height->at(ipulse));
                    savedPulses[ichannel].secondaryChannel.push_back(this_chan);            
                }

            }//end channel loop
        }//end pulse loop

        for(int ichannel=0; ichannel < 64; ichannel++){
            if(ievent==0) h_channels[ichannel]->hTime->Fill(0.0, (double)runTime);
            
            if (savedPulses[ichannel].primaryChannel.size() == 0) continue;

            std::set<int> uniqueElements(savedPulses[ichannel].secondaryChannel.begin(), savedPulses[ichannel].secondaryChannel.end());
            if (uniqueElements.size() < 2) continue;

            for(int p=0; p < savedPulses[ichannel].primaryTime.size(); p++){
                if (savedPulses[ichannel].tripleCoincidence) break;
                for(int s1=0; s1 < savedPulses[ichannel].secondaryTime.size(); s1++){
                    if (savedPulses[ichannel].tripleCoincidence) break;
                    //check for overlap
                    bool check1 = false;
                    bool check2 = false;
                    bool check3 = false;
                    check1 = checkTimingDistance(savedPulses[ichannel].primaryTime[p], savedPulses[ichannel].secondaryTime[s1], threshold);

                    if (!check1) continue;

                    for(int s2=0; s2 < savedPulses[ichannel].secondaryTime.size(); s2++ ){

                        //skip if this is the same pulse or pulses are from same channel (need two in line)
                        if (s1==s2) continue;
                        if (savedPulses[ichannel].secondaryChannel[s1] == savedPulses[ichannel].secondaryChannel[s2]) continue;
                        
                        //check if the first and 3rd pulse are in time
                        check2 = checkTimingDistance(savedPulses[ichannel].primaryTime[p], savedPulses[ichannel].secondaryTime[s2], threshold);
                        if (!check2) continue;

                        //check if the 2nd and 3rd pulses are in time
                        check3 = checkTimingDistance(savedPulses[ichannel].secondaryTime[s1], savedPulses[ichannel].secondaryTime[s2], threshold);
                        if (!check3) continue;

                        savedPulses[ichannel].tripleCoincidence = true;
                        h_channels[ichannel]->h->Fill(savedPulses[ichannel].primaryNPE[p], savedPulses[ichannel].secondaryNPE[s1], savedPulses[ichannel].secondaryNPE[s2]);
                        h_channels[ichannel]->hScaled->Fill(savedPulses[ichannel].primaryNPE[p], savedPulses[ichannel].secondaryNPE[s1], savedPulses[ichannel].secondaryNPE[s2], prescale);
                        h_channels[ichannel]->hProbeNPE->Fill(savedPulses[ichannel].primaryNPE[p]);
                        h_channels[ichannel]->hTag1NPE->Fill(savedPulses[ichannel].secondaryNPE[s1]);
                        h_channels[ichannel]->hTag2NPE->Fill(savedPulses[ichannel].secondaryNPE[s2]);
                        h_channels[ichannel]->hHeight->Fill(savedPulses[ichannel].primaryHeight[p], savedPulses[ichannel].secondaryHeight[s1], savedPulses[ichannel].secondaryHeight[s2]);
                        h_channels[ichannel]->hnPEvHeight->Fill(savedPulses[ichannel].primaryNPE[p], savedPulses[ichannel].primaryHeight[p]);
                        break;
            
                
                    } //secondary 2

                } //secondary 1

            } //end saved pulse loop

        } // end channel loop

    } //end event loop

    for(int ichannel=0; ichannel<64; ichannel++){
        outFile << run << " " << ichannel << " " << h_channels[ichannel]->h->GetEntries() << " " << h_channels[ichannel]->hTime->GetBinContent(1) << " " << prescale << std::endl;
    }

    outFile.close();
}

std::vector<globalHist> calculateRates(TFile* fout, TString pdf){

    // Set values of nPE cut to use
    vector<float> nPECuts;
    for (float i=0; i < 30; i++) nPECuts.push_back(0.1*i);

    //define histograms for all channels
    std::vector<channelHistsBase*> h_channelsDouble= {};
    for (int ichannel=0; ichannel < 64; ichannel++){
        h_channelsDouble.push_back(new channelHistsDouble(ichannel));
    }

    //define histograms for all channels
    std::vector<channelHistsBase*> h_channelsTriple = {};
    for (int ichannel=0; ichannel < 64; ichannel++){
        h_channelsTriple.push_back(new channelHistsTriple(ichannel));
    }

    std::vector<std::vector<int> > chanMap = loadChanMap("../../configuration/barConfigs/configRun1296_present.json");


    vector<int> nom_threshold = {1913, 1944, 1998, 2000, 2001};
    vector<int> low_threshold = {1963, 2003, 2006, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2021, 2022, 2024};

    //coincidenceCounts(fout, 1925, 10.0, h_channelsDouble, chanMap);
    //coincidenceCounts(fout, 1946, 10.0, h_channelsDouble, chanMap);
    //coincidenceCounts(fout, 1948, 20.0, h_channelsDouble, chanMap);
    //coincidenceCounts(fout, 1963, 1.0, h_channelsDouble, chanMap); //altered threshold run
    //coincidenceCounts(fout, 1913, 1.0, h_channelsTriple, chanMap);
    //coincidenceCounts(fout, 1944, 1.0, h_channelsTriple, chanMap);

    //coincidenceCounts(fout, 1931, 1.0, h_channelsTriple);
    //coincidenceCounts(fout, 1934, 1.0, h_channelsDouble);
    //coincidenceCounts(fout, 1935, 1.0, h_channelsDouble);
    //coincidenceCounts(fout, 1936, 1.0, h_channelsDouble);

    for(auto& run: nom_threshold){
        coincidenceCounts(fout, run, 1.0, h_channelsTriple, chanMap);
    }

    for(auto& run: low_threshold){
        coincidenceCounts(fout, run, 1.0, h_channelsDouble, chanMap);
    }

    std::cout << "Event selection finished... creating ratio plots" << std::endl;

    std::vector<globalHist> allChannels = {};

    for (int channel=0; channel < 64; channel++){

        fout->cd();

        globalHist thisChan;

        // Now calculate rate of pulses in channels passing nPE cuts
        TString title2 = TString::Format("Rate of Double Coincidence Passing nPE Cut (Channel %i)", channel);
        TGraphErrors* g_rate2 = new TGraphErrors();
        g_rate2->SetTitle(title2+";nPE Cut;# Pulses");

        TString title3 = TString::Format("Rate of Triple Coincidence Passing nPE Cut (Channel %i)", channel);
        TGraphErrors* g_rate3 = new TGraphErrors();
        g_rate3->SetTitle(title3+";nPE Cut;# Pulses");

        TString title = TString::Format("Ratio of Triple/Double Coincidence vs nPE Cut (Channel %i)", channel);
        TGraphErrors* g_rate = new TGraphErrors();
        g_rate->SetTitle(title+";nPE Cut;Ratio(Triple/Double)");

        TString titleB = TString::Format("Ratio of Triple/Double Coincidence vs nPE Cut Per Bin (Channel %i)", channel);
        TGraphErrors* g_rateBinned = new TGraphErrors();
        g_rateBinned->SetTitle(titleB+";nPE Cut;Ratio(Triple/Double)");

        TString titleB2 = TString::Format("Rate of Double Coincidence Passing nPE Cut Per Bin (Channel %i)", channel);
        TGraphErrors* g_rateBinned2 = new TGraphErrors();
        g_rateBinned2->SetTitle(titleB2+";nPE Cut;# Pulses");

        TString titleB3 = TString::Format("Rate of Triple Coincidence Passing nPE Cut Per Bin (Channel %i)", channel);
        TGraphErrors* g_rateBinned3 = new TGraphErrors();
        g_rateBinned3->SetTitle(titleB3+";nPE Cut;# Pulses");

        TString titleR2 = TString::Format("Double Coincidence Counts Rebinned (Channel %i)", channel);
        TGraphErrors* g_rebined2 = new TGraphErrors();
        g_rateBinned2->SetTitle(titleR2+";nPE Cut;# Pulses");

        TString titleR3 = TString::Format("Triple Coincidence Counts Rebined (Channel %i)", channel);
        TGraphErrors* g_rebined3= new TGraphErrors();
        g_rateBinned3->SetTitle(titleR3+";nPE Cut;# Pulses");

        TString titleH = TString::Format("Ratio of Rates vs Height (Channel %i)", channel);
        TGraphErrors* g_rateHeight= new TGraphErrors();
        g_rateHeight->SetTitle(titleH+";Height;# Pulses");

        TString titleH2 = TString::Format("Double Coincidence Rate vs Height (Channel %i)", channel);
        TGraphErrors* g_rateHeight2 = new TGraphErrors();
        g_rateHeight2->SetTitle(titleH2+";Height;# Pulses");

        TString titleH3 = TString::Format("Triple Coincidence Rate vs Height (Channel %i)", channel);
        TGraphErrors* g_rateHeight3= new TGraphErrors();
        g_rateHeight3->SetTitle(titleH3+";Height;# Pulses");

        float timeTriple = h_channelsTriple[channel]->hTime->GetBinContent(1);
        float timeDouble = h_channelsDouble[channel]->hTime->GetBinContent(1);

        TH3F* h_tripleBinned = (TH3F*) h_channelsTriple[channel]->hScaled->Clone();
        TH3F* h_doubleBinned = (TH3F*) h_channelsDouble[channel]->hScaled->Clone();

        float min2 = 10e12;
        float max2 = -1;
        float min3 = 10e12;
        float max3 = -1;
        float maxRatio = -1;
        float nPEMaxRatio = -1;
        float maxRatioTripleRate, maxRatioDoubleRate;
        float maxRatioErr = 0;

        int points = 0;
        for(auto& cut : nPECuts){
            double cutBin = (double)cut;
            int xbin_low = h_channelsTriple[channel]->hScaled->GetXaxis()->FindFixBin(cutBin);
            int xbin_high = h_channelsTriple[channel]->hScaled->GetNbinsX()+1;
            int ybin_low = h_channelsTriple[channel]->hScaled->GetYaxis()->FindFixBin(cutBin);
            int ybin_high = h_channelsTriple[channel]->hScaled->GetNbinsY()+1;
            int zbin_low = h_channelsTriple[channel]->hScaled->GetZaxis()->FindFixBin(cutBin);;
            int zbin_high = h_channelsTriple[channel]->hScaled->GetNbinsZ()+1;
            int nBinsY = h_channelsTriple[channel]->hScaled->GetNbinsY()+1;
            int nBinsZ = h_channelsTriple[channel]->hScaled->GetNbinsZ()+1;

            float countTriple = h_channelsTriple[channel]->hScaled->Integral(xbin_low, xbin_high, ybin_low, ybin_high, zbin_low, zbin_high);
            float countDouble = h_channelsDouble[channel]->hScaled->Integral(xbin_low, xbin_high, ybin_low, ybin_high, zbin_low, zbin_high);

            float rateTriple = countTriple / timeTriple;
            float rateDouble = countDouble / timeDouble;

            float doubleErr = sqrt(countDouble) / timeDouble;
            float tripleErr = sqrt(countTriple) / timeTriple;

            g_rate2->SetPoint(points, cut, rateDouble);
            g_rate2->SetPointError(points, 0, doubleErr);
            g_rate3->SetPoint(points, cut, rateTriple);
            g_rate3->SetPointError(points, 0, tripleErr);

            float ratio = 1.;
            float errRatio = 1;
            if (rateDouble > 0) {
                ratio = rateTriple/rateDouble;
                if(rateTriple>0) errRatio = ratio * sqrt(1/countTriple + 1/countDouble);
            }
            g_rate->SetPoint(points, cut, ratio);
            g_rate->SetPointError(points, 0, errRatio);

            points++;

            if (rateDouble < min2) min2 = rateDouble;
            if (rateDouble > max2) max2 = rateDouble;
            if (rateTriple < min3) min3 = rateTriple;
            if (rateTriple > max3) max3 = rateTriple;
            if (ratio > maxRatio) {
                maxRatio = ratio;
                nPEMaxRatio = cut;
                maxRatioTripleRate = rateTriple;
                maxRatioDoubleRate = rateDouble;
                maxRatioErr = errRatio;
            }
        }

        double x_val = 0;
        for(int ibin=1; ibin < h_tripleBinned->GetNbinsX()+1; ibin++){
            int nBinsYmin = h_tripleBinned->GetYaxis()->FindFixBin(2);
            int nBinsYmax = h_tripleBinned->GetNbinsY()+1;
            int nBinsZmin = h_tripleBinned->GetZaxis()->FindFixBin(2);
            int nBinsZmax = h_tripleBinned->GetNbinsZ()+1;

            float countTripleBin = h_tripleBinned->Integral(ibin, ibin, nBinsYmin, nBinsYmax, nBinsZmin, nBinsZmax);
            float countDoubleBin = h_doubleBinned->Integral(ibin, ibin, nBinsYmin, nBinsYmax, nBinsZmin, nBinsZmax);
            float rateTripleBin = countTripleBin / timeTriple;
            float rateDoubleBin = countDoubleBin / timeDouble;
            float doubleBinErr = sqrt(countDoubleBin) / timeDouble;
            float tripleBinErr = sqrt(countTripleBin) / timeTriple;
            x_val = h_tripleBinned->GetXaxis()->GetBinLowEdge(ibin);
            g_rateBinned2->SetPoint(ibin, x_val, rateDoubleBin);
            g_rateBinned2->SetPointError(ibin, 0, doubleBinErr);
            g_rateBinned3->SetPoint(ibin, x_val, rateTripleBin);
            g_rateBinned3->SetPointError(ibin, 0, tripleBinErr);
            g_rebined2->SetPoint(ibin, x_val, countDoubleBin);
            g_rebined2->SetPointError(ibin, 0, sqrt(countDoubleBin));
            g_rebined3->SetPoint(ibin, x_val, countTripleBin);
            g_rebined3->SetPointError(ibin, 0, sqrt(countTripleBin));

            float ratioBinned = 1.;
            float errRatioBinned = 1;
            if (rateDoubleBin > 0){
                ratioBinned = rateTripleBin / rateDoubleBin;
                if(rateTripleBin>0) errRatioBinned = ratioBinned * sqrt(1/countTripleBin + 1/countDoubleBin);
            }
            g_rateBinned->SetPoint(ibin, x_val, ratioBinned);
            g_rateBinned->SetPointError(ibin, 0, errRatioBinned);
        }

        int minY_h = h_channelsTriple[channel]->hHeight->GetYaxis()->FindFixBin(20);
        int minZ_h = h_channelsTriple[channel]->hHeight->GetZaxis()->FindFixBin(20);
        int maxY_h = h_channelsTriple[channel]->hHeight->GetNbinsY()+1;
        int maxZ_h = h_channelsTriple[channel]->hHeight->GetNbinsZ()+1;
        TH1D* h_tripleHeight = h_channelsTriple[channel]->hHeight->ProjectionX("h_tripleHeight", minY_h, maxY_h, minZ_h, maxZ_h);
        TH1D* h_doubleHeight = h_channelsDouble[channel]->hHeight->ProjectionX("h_doubleHeight", minY_h, maxY_h, minZ_h, maxZ_h);
        TH1D* h_countRatio = (TH1D*)h_tripleHeight->Clone("h_countRatio");
        h_countRatio->Divide(h_doubleHeight);
        h_countRatio->Scale(timeDouble/timeTriple);
        for (int ibin=1; ibin < h_tripleHeight->GetNbinsX()+1; ibin++){ 
        
            float countTripleHeight = h_tripleHeight->GetBinContent(ibin);
            float countDoubleHeight = h_doubleHeight->GetBinContent(ibin);

            x_val = h_tripleHeight->GetBinLowEdge(ibin);

            if(x_val < 10) continue;

            g_rateHeight2->SetPoint(ibin, x_val, countDoubleHeight/timeDouble);
            g_rateHeight3->SetPoint(ibin, x_val, countTripleHeight/timeTriple);

            g_rateHeight2->SetPointError(ibin, 0, sqrt(countDoubleHeight)/timeDouble);
            g_rateHeight3->SetPointError(ibin, 0, sqrt(countTripleHeight)/timeTriple);
            
            float ratioHeightBinned = 1.;
            float errRatioHeightBinned = 1;
            if (countDoubleHeight > 0){
                ratioHeightBinned = (countTripleHeight/timeTriple)/(countDoubleHeight/timeDouble);
                if(ratioHeightBinned>0) errRatioHeightBinned = ratioHeightBinned * sqrt(1/countTripleHeight + 1/countDoubleHeight);
                else errRatioHeightBinned = (1/timeTriple)/((countDoubleHeight+1)/timeDouble) * sqrt(1/(1) + 1/(countDoubleHeight+1));
            }

            std::cout << "Setting " << channel << " " << x_val << " " << ratioHeightBinned << " from bin " << ibin << std::endl;
            if(countDoubleHeight==0 && countTripleHeight==0) continue;

            g_rateHeight->SetPoint(ibin, x_val, ratioHeightBinned);
            g_rateHeight->SetPointError(ibin, 0, errRatioHeightBinned);

        }

        thisChan.min2 = min2;
        thisChan.max2 = max2;
        thisChan.min3 = min3;
        thisChan.max3 = max3;
        thisChan.maxRatio = maxRatio;
        thisChan.nPEMaxRatio = nPEMaxRatio;
        thisChan.maxRatioDoubleRate = maxRatioDoubleRate;
        thisChan.maxRatioTripleRate = maxRatioTripleRate;
        thisChan.maxRatioErr = maxRatioErr;

        std::cout << "Creating canvases and writing to file... " << std::endl;

        TString dir = TString::Format("channel%i", channel);
        fout->mkdir(dir);

        TCanvas* c1 = new TCanvas("individualRates", "Trigger Efficiencies", 800, 600);
        c1->cd();
        g_rate2->SetTitle(TString::Format("Coincidence Rates vs nPE Cut (Channel %i)", channel));
        g_rate2->SetMarkerStyle(8);
        g_rate2->SetMarkerSize(1);
        g_rate2->Draw("P");
        g_rate3->SetMarkerColor(kRed);
        g_rate3->SetMarkerStyle(8);
        g_rate3->SetMarkerSize(1);
        g_rate3->Draw("same P");
        c1->SetLogy();

        TLegend* l1 = new TLegend(0.7, 0.9, 0.7, 0.9);
        l1->AddEntry(g_rate2, "Double Coincidence Rate", "P");
        l1->AddEntry(g_rate3, "Triple Coincidence Rate", "P");
        l1->Draw();
        fout->cd(dir);
        c1->Write("individualRates");

        TCanvas* c2 = new TCanvas("ratioRates", "ratioRates", 800, 600);
        c2->cd();
        g_rate->SetMarkerStyle(8);
        g_rate->Draw("P");
        double maxY = TMath::MaxElement(g_rate->GetN(), g_rate->GetY());
        double minY = TMath::MinElement(g_rate->GetN(), g_rate->GetY());
        g_rate->GetYaxis()->SetRangeUser(minY*0.1, maxY*1.1);
        c2->SetLogy();
        fout->cd(dir);
        c2->Write("ratioRates");

        TCanvas* c3 = new TCanvas("individualRatesBinned", "Trigger Efficiencies", 800, 600);
        c3->cd();
        g_rateBinned2->SetTitle(TString::Format("Coincidence Rates vs nPE Cut (Channel %i)", channel));
        g_rateBinned2->SetMarkerStyle(8);
        g_rateBinned2->SetMarkerSize(1);
        g_rateBinned2->Draw("P");
        g_rateBinned3->SetMarkerColor(kRed);
        g_rateBinned3->SetMarkerStyle(8);
        g_rateBinned3->SetMarkerSize(1);
        g_rateBinned3->Draw("same P");
        c3->SetLogy();

        TLegend* l2 = new TLegend(0.7, 0.9, 0.7, 0.9);
        l2->AddEntry(g_rateBinned2, "Double Coincidence Rate", "P");
        l2->AddEntry(g_rateBinned3, "Triple Coincidence Rate", "P");
        l2->Draw();
        fout->cd(dir);
        c3->Write("individualRatesBinned");


        TCanvas* c4 = new TCanvas("ratioRatesBinned", "ratioRatesBinned", 800, 600);
        TF1 *f2 = new TF1("f2", "[0] * (0.5 * (1 + TMath::Erf((x - [1]) / ([2] * sqrt(2)))))", 0.001, 10);
        f2->SetParLimits(1, 0.0001, 20);
        f2->SetParLimits(2, 0.1, 1);
        f2->SetParLimits(0, 0.7, 1.3);
        f2->SetParameters(1, 1, 0.5);
        auto fitOut = g_rateBinned->Fit(f2, "SW", "", npeFitBinsLow[channel], npeFitBinsHigh[channel]);
        g_rateBinned->GetYaxis()->SetRangeUser(0, 2);
        f2->Draw("same");
        c4->cd();
        g_rateBinned->SetMarkerStyle(8);
        g_rateBinned->Draw("AP");

        int tEntries = h_channelsTriple[channel]->hHeight->GetEntries();
        int dEntries = h_channelsDouble[channel]->hHeight->GetEntries();

        float lamb = round(f2->GetParameter(0)*100)/100;
        float mu = round(f2->GetParameter(1)*100)/100;
        float sigma = round(f2->GetParameter(2)*100)/100;
        float chi = round(fitOut->Chi2() / fitOut->Ndf() * 100)/100;

        float lambErr = round(f2->GetParError(0)*100)/100;
        float muErr = round(f2->GetParError(0)*100)/100;
        float sigmaErr = round(f2->GetParError(0)*100)/100;
        //float chiErr = round(f2->GetParError(0)*100)/100;

        thisChan.npeFitLambda = lamb;
        thisChan.npeFitMu = mu;
        thisChan.npeFitSigma = sigma;
        thisChan.npeFitChi = chi;

        thisChan.npeFitLambdaErr = lambErr;
        thisChan.npeFitMuErr = muErr;
        thisChan.npeFitSigmaErr = sigmaErr;
        thisChan.npeFitChiErr = 0;
        
        TLatex* text1 = new TLatex();
        text1->SetTextSize(0.03);  
        text1->SetTextColor(kRed);  

        TLatex* text2 = new TLatex();
        text2->SetTextSize(0.03);  
        text2->SetTextColor(kRed);
        
        TLatex* text3 = new TLatex();
        text3->SetTextSize(0.03);  
        text3->SetTextColor(kBlue);
        
        TLatex* text4 = new TLatex();
        text4->SetTextSize(0.03);  
        text4->SetTextColor(kBlue);

        //text1->DrawLatex(3, 1.7, TString::Format("Double Coincidence Events: %i", dEntries));
        text1->DrawLatex(3, 1.7, TString::Format("Triple Coincidence Events (8mV): %i", dEntries));
        text2->DrawLatex(3, 1.6, TString::Format("Triple Coincidence Events (15mV): %i",tEntries));
        text3->DrawLatex(3, 0.4, TString::Format("#lambda: %f#pm %f, #mu %f",lamb, lambErr, mu));
        text4->DrawLatex(3, 0.3, TString::Format("#sigma %f, #chi^2/ndof %f",sigma, chi));
        //double maxYBin = TMath::MaxElement(g_rateBinned->GetN(), g_rateBinned->GetY());
        //double minYBin = TMath::MinElement(g_rateBinned->GetN(), g_rateBinned->GetY());
        //g_rateBinned->GetYaxis()->SetRangeUser(minYBin*0.1, maxYBin*1.1);
        //c4->SetLogy(0);
        //c4->SetLogx(1);
        fout->cd(dir);
        c4->Write("ratioRatesBinned");


        TCanvas* c5 = new TCanvas("individualRatesBinnedHeight", "Trigger Efficiencies", 800, 600);
        c5->cd();
        g_rateHeight2->SetTitle(TString::Format("Coincidence Rates vs Height Cut (Channel %i)", channel));
        g_rateHeight2->SetMarkerStyle(8);
        g_rateHeight2->SetMarkerSize(1);
        g_rateHeight2->Draw("P");
        g_rateHeight3->SetMarkerColor(kRed);
        g_rateHeight3->SetMarkerStyle(8);
        g_rateHeight3->SetMarkerSize(1);
        g_rateHeight3->Draw("same P");

        TLegend* l5 = new TLegend(0.7, 0.9, 0.7, 0.9);
        l5->AddEntry(g_rateHeight2, "Double Coincidence Rate", "P");
        l5->AddEntry(g_rateHeight3, "Triple Coincidence Rate", "P");
        l5->Draw();
        fout->cd(dir);
        c5->Write("individualRatesBinnedHeight");

        TCanvas* c6 = new TCanvas("ratioRatesBinnedHeight", "ratioRatesBinnedHeight", 800, 600);
        TF1 *f1 = new TF1("f1", "[0] * (0.5 * (1 + TMath::Erf((x - [1]) / ([2] * sqrt(2)))))", 5, 1000);
        f1->SetParLimits(0, 0.7, 1.3);
        f1->SetParLimits(1, 0.0001, 20);
        f1->SetParLimits(2, 0.5, 10);
        f1->SetParameters(1, 30, 100);
        c6->cd();
        g_rateHeight->SetMarkerStyle(8);
        g_rateHeight->Draw("AP");
        fitOut = g_rateHeight->Fit(f1, "SEWW", "", heightFitBinsLow[channel], heightFitBinsHigh[channel]);
        g_rateHeight->GetYaxis()->SetRangeUser(0, 2);
        f1->Draw("same");

        /*int tEntries = h_channelsTriple[channel]->hHeight->GetEntries();
        int dEntries = h_channelsDouble[channel]->hHeight->GetEntries();*/

        lamb = round(f1->GetParameter(0)*100)/100;
        mu = round(f1->GetParameter(1)*100)/100;
        sigma = round(f1->GetParameter(2)*100)/100;
        chi = round(fitOut->Chi2() / fitOut->Ndf() * 100)/100;

        lambErr = round(f1->GetParError(0)*100)/100;
        muErr = round(f1->GetParError(0)*100)/100;
        sigmaErr = round(f1->GetParError(0)*100)/100;
        //chiErr = round(fitOut->GetParError(0)*100)/100;

        thisChan.heightFitLambda = lamb;
        thisChan.heightFitMu = mu;
        thisChan.heightFitSigma = sigma;
        thisChan.heightFitChi = chi;

        thisChan.heightFitLambdaErr = lambErr;
        thisChan.heightFitMuErr = muErr;
        thisChan.heightFitSigmaErr = sigmaErr;
        thisChan.heightFitChiErr = 0;

        TLine* line1 = new TLine(15, 0, 15, 2);
        line1->SetLineStyle(2);
        line1->SetLineColor(kGreen);
        line1->SetLineWidth(3);
        line1->Draw("same");

        /*TLatex* text1 = new TLatex();
        text1->SetTextSize(0.03);  
        text1->SetTextColor(kRed);  

        TLatex* text2 = new TLatex();
        text2->SetTextSize(0.03);  
        text2->SetTextColor(kRed);
        
        TLatex* text3 = new TLatex();
        text3->SetTextSize(0.03);  
        text3->SetTextColor(kBlue);
        
        TLatex* text4 = new TLatex();
        text4->SetTextSize(0.03);  
        text4->SetTextColor(kBlue);*/

        //text1->DrawLatex(60, 1.7, TString::Format("Double Coincidence Events: %i", dEntries));
        text1->DrawLatex(60, 1.7, TString::Format("Triple Coincidence Events (8mV): %i", dEntries));
        text2->DrawLatex(60, 1.6, TString::Format("Triple Coincidence Events (15mV): %i",tEntries));
        text3->DrawLatex(60, 0.4, TString::Format("#lambda: %f #pm %f, #mu %f",lamb, lambErr, mu));
        text4->DrawLatex(60, 0.3, TString::Format("#sigma %f, #chi^2/ndof %f",sigma, chi));


        //maxYBin = TMath::MaxElement(g_rateHeight->GetN(), g_rateHeight->GetY());
        //minYBin = TMath::MinElement(g_rateHeight->GetN(), g_rateHeight->GetY());
        //g_rateHeight->GetYaxis()->SetRangeUser(minYBin*0.1, maxYBin*1.1);
        c6->SetLogy(0);
        c6->SetLogx(1);
        fout->cd(dir);
        c6->Write("ratioRatesBinnedHeight");

        /*TH1F* h_heightFitLambda = new TH1F("h_heightFitLambda", "#lambda Values of Fit;Channel;#lambda", 80, -1, 79);
        TH1F* h_heightFitMu = new TH1F("h_heightFitMu", "#mu Values of Fit;Channel;#mu", 80, -1, 79);
        TH1F* h_heightFitSigma = new TH1F("h_heightFitSigma", "#sigma Values of Fit;Channel;#sigma", 80, -1, 79);
        TH1F* h_heightFitChi = new TH1F("h_heightFitChi", "#chi^{2}/ndof Values of Fit;Channel;#chi^{2}/ndof", 80, -1, 79);

        TH1F* h_npeFitLambda = new TH1F("h_npeFitLambda", "#lambda Values of Fit;Channel;#lambda", 80, -1, 79);
        TH1F* h_npeFitMu = new TH1F("h_npeFitMu", "#mu Values of Fit;Channel;#mu", 80, -1, 79);
        TH1F* h_npeFitSigma = new TH1F("h_npeFitSigma", "#sigma Values of Fit;Channel;#sigma", 80, -1, 79);
        TH1F* h_npeFitChi = new TH1F("h_npeFitChi", "#chi^{2}/ndof Values of Fit;Channel;#chi^{2}/ndof", 80, -1, 79);

        for (int i=0; i<64; i++){
            h_heightFitLambda->Fill(heightFitLambda[i]);
            h_heightFitMu->Fill(heightFitMu[i]);
            h_heightFitSigma->Fill(heightFitSigma[i]);
            h_heightFitChi->Fill(heightFitChi[i]);

            h_npeFitLambda->Fill(npeFitLambda[i]);
            h_npeFitMu->Fill(npeFitMu[i]);
            h_npeFitSigma->Fill(npeFitSigma[i]);
            h_npeFitChi->Fill(npeFitChi[i]);
        }*/

        fout->cd(dir);
        h_channelsTriple[channel]->h->Write("tripleCoincidenceCount");
        h_channelsTriple[channel]->hScaled->Write("tripleCoincidenceCountPrescaled");
        h_channelsDouble[channel]->h->Write("doubleCoincidenceCount");
        h_channelsDouble[channel]->hScaled->Write("doubleCoincidenceCountPrescaled");
        h_channelsDouble[channel]->hProbeNPE->Write();
        h_channelsDouble[channel]->hTime->Write();
        h_channelsTriple[channel]->hProbeNPE->Write();
        h_channelsDouble[channel]->hTag1NPE->Write();
        h_channelsDouble[channel]->hTag2NPE->Write();
        h_channelsTriple[channel]->hTag1NPE->Write();
        h_channelsTriple[channel]->hTag2NPE->Write();
        h_channelsTriple[channel]->hTime->Write();
        h_channelsTriple[channel]->hHeight->Write();
        h_channelsDouble[channel]->hHeight->Write();
        h_channelsDouble[channel]->hnPEvHeight->Write();
        h_channelsTriple[channel]->hnPEvHeight->Write();
        h_countRatio->Write("h_ratioRateHeight");
        g_rate2->Write("doubleCoincidenceRate");
        g_rate3->Write("tripleCoincidenceRate");
        g_rate->Write("g_ratioRate");
        g_rateBinned2->Write("doubleCoincidenceRateBinned");
        g_rateBinned3->Write("tripleCoincidenceRateBinned");
        g_rateBinned->Write("g_ratioRateBinned");
        g_rebined2->Write("doubleCoincidenceCountsRebinned");
        g_rebined3->Write("tripleCoincidenceCountsRebinned");
        h_tripleBinned->Write("tripleBinnedCounts");
        h_doubleBinned->Write("doubleBinnedCounts");
        g_rateHeight->Write("g_ratioRateHeight");
        g_rateHeight2->Write("h_ratioRateHeight2");
        g_rateHeight3->Write("h_ratioRateHeight3");

        /*h_heightFitLambda->Write();
        h_heightFitMu->Write();
        h_heightFitSigma->Write();
        h_heightFitChi->Write();

        h_npeFitLambda->Write();
        h_npeFitMu->Write();
        h_npeFitSigma->Write();
        h_npeFitChi->Write();*/

        allChannels.push_back(thisChan);

        if(channel==0){
            c4->Print(pdf + "NPE.pdf(");
            c6->Print(pdf + "Height.pdf(");
        }
        else if(channel==63){
            c4->Print(pdf + "NPE.pdf)");
            c6->Print(pdf + "Height.pdf)");
        }
        else{
            c4->Print(pdf + "NPE.pdf");
            c6->Print(pdf + "Height.pdf");
        }

    }

    return allChannels;

}

void calculateTriggerEfficiencies(){

    //gStyle->SetOptStat(0);
    gROOT->SetBatch(1);

    //output file for plots
    TFile* fout = TFile::Open("triggerEfficiencyPlots.root", "RECREATE");
    TString pdf = "outputPlots";

    //initialize some global histograms
    TGraph* doubleRatesMax = new TGraph();
    TGraph* doubleRatesMin = new TGraph();
    TGraph* tripleRatesMax = new TGraph();
    TGraph* tripleRatesMin = new TGraph();
    TGraphErrors* allRatios = new TGraphErrors();
    TGraph* maxRatioVNPE = new TGraph();
    TGraph* maxNPECut = new TGraph();
    TGraph* maxRatioRatesGood = new TGraph();
    TGraph* maxRatioRatesBad = new TGraph();

    TGraphErrors* h_heightFitLambda = new TGraphErrors(); //"h_heightFitLambda", "#lambda Values of Fit;Channel;#lambda", 80, -1, 79);
    TGraphErrors* h_heightFitMu = new TGraphErrors(); //"h_heightFitMu", "#mu Values of Fit;Channel;#mu", 80, -1, 79);
    TGraphErrors* h_heightFitSigma = new TGraphErrors(); //"h_heightFitSigma", "#sigma Values of Fit;Channel;#sigma", 80, -1, 79);
    TGraphErrors* h_heightFitChi = new TGraphErrors(); //"h_heightFitChi", "#chi^{2}/ndof Values of Fit;Channel;#chi^{2}/ndof", 80, -1, 79);

    TGraphErrors* h_npeFitLambda = new TGraphErrors(); //"h_npeFitLambda", "#lambda Values of Fit;Channel;#lambda", 80, -1, 79);
    TGraphErrors* h_npeFitMu = new TGraphErrors();//"h_npeFitMu", "#mu Values of Fit;Channel;#mu", 80, -1, 79);
    TGraphErrors* h_npeFitSigma = new TGraphErrors();//"h_npeFitSigma", "#sigma Values of Fit;Channel;#sigma", 80, -1, 79);
    TGraphErrors* h_npeFitChi = new TGraphErrors();//"h_npeFitChi", "#chi^{2}/ndof Values of Fit;Channel;#chi^{2}/ndof", 80, -1, 79);

    vector<bool> goodRatio = {};
    float maxRate = -1;
    float minRate = 10e12;
    std::cout << "Going to calculate rates" << std::endl;
    std::vector<globalHist> thisChan = calculateRates(fout, pdf);

    //fout->Close();

    for(int ichan=0; ichan < 64; ichan++){
        //cout << "channel: " << ichan << ", max2 " << thisChan.max2 << ", min2 " << thisChan.min2 << endl;
        doubleRatesMax->SetPoint(ichan, ichan, thisChan[ichan].max2);
        doubleRatesMin->SetPoint(ichan, ichan, thisChan[ichan].min2);
        tripleRatesMax->SetPoint(ichan, ichan, thisChan[ichan].max3);
        tripleRatesMin->SetPoint(ichan, ichan, thisChan[ichan].min3);
        allRatios->SetPoint(ichan, ichan, thisChan[ichan].maxRatio);
        cout << "Error point " << ichan << ", " << thisChan[ichan].maxRatioErr << std::endl;
        allRatios->SetPointError(ichan, 0, thisChan[ichan].maxRatioErr);
        maxRatioVNPE->SetPoint(ichan, thisChan[ichan].nPEMaxRatio, thisChan[ichan].maxRatio);
        maxNPECut->SetPoint(ichan, ichan, thisChan[ichan].nPEMaxRatio);
        
        h_heightFitLambda->SetPoint(ichan, ichan, thisChan[ichan].heightFitLambda);
        h_heightFitLambda->SetPointError(ichan, 0, thisChan[ichan].heightFitLambdaErr);
        h_heightFitMu->SetPoint(ichan, ichan, thisChan[ichan].heightFitMu);
        h_heightFitMu->SetPointError(ichan, 0, thisChan[ichan].heightFitMuErr);
        h_heightFitSigma->SetPoint(ichan, ichan, thisChan[ichan].heightFitSigma);
        h_heightFitSigma->SetPointError(ichan, 0, thisChan[ichan].heightFitSigmaErr);
        h_heightFitChi->SetPoint(ichan, ichan, thisChan[ichan].heightFitChi);
        h_heightFitChi->SetPointError(ichan, 0, thisChan[ichan].heightFitChiErr);

        h_npeFitLambda->SetPoint(ichan, ichan, thisChan[ichan].npeFitLambda);
        h_npeFitLambda->SetPointError(ichan, 0, thisChan[ichan].npeFitLambdaErr);
        h_npeFitMu->SetPoint(ichan, ichan, thisChan[ichan].npeFitMu);
        h_npeFitMu->SetPointError(ichan, 0, thisChan[ichan].npeFitMuErr);
        h_npeFitSigma->SetPoint(ichan, ichan, thisChan[ichan].npeFitSigma);
        h_npeFitSigma->SetPointError(ichan, 0, thisChan[ichan].npeFitSigmaErr);
        h_npeFitChi->SetPoint(ichan, ichan, thisChan[ichan].npeFitChi);
        h_npeFitChi->SetPointError(ichan, 0, thisChan[ichan].npeFitChiErr);

        if (thisChan[ichan].min2 < minRate) minRate = thisChan[ichan].min2;
        if (thisChan[ichan].min3 < minRate) minRate = thisChan[ichan].min3;
        if (thisChan[ichan].max2 > maxRate) maxRate = thisChan[ichan].max2;
        if (thisChan[ichan].max3 > maxRate) maxRate = thisChan[ichan].max3;

        if(thisChan[ichan].maxRatio >= 1){
            maxRatioRatesGood->SetPoint(ichan, thisChan[ichan].maxRatioDoubleRate, thisChan[ichan].maxRatioTripleRate);
            goodRatio.push_back(true);
        } 
        else {
            goodRatio.push_back(false);
            maxRatioRatesBad->SetPoint(ichan, thisChan[ichan].maxRatioDoubleRate, thisChan[ichan].maxRatioTripleRate);
        }
    }

    doubleRatesMax->SetTitle("Max Double Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    doubleRatesMin->SetTitle("Min Double Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    tripleRatesMax->SetTitle("Max Triple Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    tripleRatesMin->SetTitle("Min Triple Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    allRatios->SetTitle("Max Triple/Double Coincidence Ratio per Channel; Channel; Coincidence Rate Ratio");
    maxRatioVNPE->SetTitle("Max Coincidence Ratio vs nPE Cut; nPE Cut; Coincidence Rate Ratio");
    maxNPECut->SetTitle("NPE Cut Giving Max Coincidence Ratio; Channel; nPE Cut");
    maxRatioRatesGood->SetTitle("Double and Triple Coincidence Rates for Max Ratio;Double Coincidence Rate;Triple Coincidence Rate");
    maxRatioRatesBad->SetTitle("Double and Triple Coincidence Rates for Max Ratio;Double Coincidence Rate;Triple Coincidence Rate");

    h_heightFitLambda->SetTitle("#lambda Fit Values;Channel;#lambda");
    h_heightFitMu->SetTitle("#mu Fit Values;Channel;#mu");
    h_heightFitSigma->SetTitle("#sigma Fit Values;Channel;#sigma");
    h_heightFitChi->SetTitle("#chi^{2}/ndof Fit Values;Channel;#chi^{2}/ndof");

    h_npeFitLambda->SetTitle("#lambda Fit Values;Channel;#lambda");
    h_npeFitMu->SetTitle("#mu Fit Values;Channel;#mu");
    h_npeFitSigma->SetTitle("#sigma Fit Values;Channel;#sigma");
    h_npeFitChi->SetTitle("#chi^{2}/ndof Fit Values;Channel;#chi^{2}/ndof");

    fout->cd();
    h_heightFitLambda->Write("heightFitLambda");
    h_heightFitMu->Write("heghtFitMu");
    h_heightFitSigma->Write("heightFitSigma");
    h_heightFitChi->Write("heightFitChi");

    h_npeFitLambda->Write("npeFitLambda");
    h_npeFitMu->Write("npeFitMu");
    h_npeFitSigma->Write("npeFitSigma");
    h_npeFitChi->Write("npeFitChi");

    TCanvas* c1 = new TCanvas("c1", "Max and Min Coincidence Rates", 1000, 800);
    c1->cd();
    doubleRatesMax->SetTitle("Max/Min Coincidence Rates Per Channel");
    doubleRatesMax->GetYaxis()->SetRangeUser(minRate*0.9, maxRate*1.1);
    doubleRatesMax->GetXaxis()->SetRangeUser(-2, 65);
    doubleRatesMin->GetXaxis()->SetRangeUser(-2, 65);
    tripleRatesMax->GetXaxis()->SetRangeUser(-2, 65);
    tripleRatesMin->GetXaxis()->SetRangeUser(-2, 65);
    allRatios->GetXaxis()->SetRangeUser(-2, 65);

    doubleRatesMax->SetMarkerStyle(23);
    doubleRatesMax->SetMarkerColor(kRed);
    doubleRatesMin->SetMarkerStyle(22);
    doubleRatesMin->SetMarkerColor(kRed);
    tripleRatesMax->SetMarkerStyle(23);
    tripleRatesMax->SetMarkerColor(kBlue);
    tripleRatesMin->SetMarkerStyle(22);
    tripleRatesMin->SetMarkerColor(kBlue);

    fout->cd();
    doubleRatesMax->Write("doubleRatesMax");
    doubleRatesMin->Write("doubleRatesMin");
    tripleRatesMax->Write("tripleRatesMax");
    tripleRatesMin->Write("tripleRatesMin");
    allRatios->Write("allRatios");

    doubleRatesMax->Draw("P");
    doubleRatesMin->Draw("same P");
    tripleRatesMax->Draw("same P");
    tripleRatesMin->Draw("same P");

    for(int i=0; i < doubleRatesMax->GetN(); i++){
        double x1, y1, x2, y2;
        doubleRatesMin->GetPoint(i, x1, y1); // Get point from graph1
        doubleRatesMax->GetPoint(i, x2, y2); // Get point from graph2

        // Create a line connecting the two points
        TLine* line1 = new TLine(x1, y1, x2, y2);
        line1->SetLineColor(kRed); // Set line color
        line1->Draw("SAME"); // Draw the line on the same canvas

        tripleRatesMin->GetPoint(i, x1, y1); // Get point from graph1
        tripleRatesMax->GetPoint(i, x2, y2); // Get point from graph2

        // Create a line connecting the two points
        TLine* line2 = new TLine(x1, y1, x2, y2);
        line2->SetLineColor(kBlue); // Set line color
        line2->Draw("SAME"); // Draw the line on the same canvas
    }

    TLegend* l1 = new TLegend(0.8, 0.9, 0.7, 0.9);
    l1->AddEntry(doubleRatesMax, "Max/Min Double Coincidence Rate", "P");
    l1->AddEntry(tripleRatesMax, "Max/Min Triple Coincidence Rate", "P");
    l1->Draw();

    TCanvas* c2 = new TCanvas("c2", "Max Coincidence Ratio", 1000, 800);
    c2->cd();
    allRatios->SetMarkerStyle(8); //make this a TError graph
    allRatios->Draw("P");
    TLine* line3 = new TLine(0, 1, 64, 1);
    line3->SetLineColor(kRed);
    line3->SetLineStyle(9);
    line3->Draw("same");

    TCanvas* c3 = new TCanvas("c3", "NPE Cut Max Ratio", 1000, 800);
    c3->cd();
    maxNPECut->SetMarkerStyle(8);
    maxNPECut->Draw("P");

    TCanvas* c4 = new TCanvas("c4", "NPE Cut Max vs Coincidence Ratio", 1000, 800);
    c4->cd();
    maxRatioVNPE->SetMarkerStyle(8);
    maxRatioVNPE->Draw("P");

    TCanvas* c5 = new TCanvas("c5", "All Triple Coincidence Rates", 1000, 800);
    TCanvas* c6 = new TCanvas("c6", "All Double Coincidence Rates", 1000, 800);

    // Get the list of keys in the file
    TIter next(fout->GetListOfKeys());
    TKey* key;

    int countDirs = 0;
    // Loop over all keys
    while ((key = (TKey*)next())) {
        // Check if the key is a directory
        if (strcmp(key->GetClassName(), "TDirectoryFile") == 0) {
            TDirectory* dir = (TDirectory*)key->ReadObj();

            bool goodChan = goodRatio[countDirs];

            TGraph* graph;
            TString s_dir = dir->GetName();
            fout->GetObject(s_dir+TString("/tripleCoincidenceRate"), graph);
            if (goodChan) graph->SetMarkerColor(kBlue);
            else graph->SetMarkerColor(kRed);
            c5->cd();
            graph->Draw("same");
            fout->GetObject(s_dir+TString("/doubleCoincidenceRate"), graph);
            if (goodChan) graph->SetMarkerColor(kBlue);
            else graph->SetMarkerColor(kRed);
            c6->cd();
            graph->Draw("same");

            // If you modify any objects, make sure to write them back
            dir->Write(); // Writes all objects in the current directory

            countDirs++;
        }
    }

    TCanvas* c7 = new TCanvas("c7", "c7", 1000, 800);
    c7->cd();
    maxRatioRatesGood->SetMarkerStyle(8);
    maxRatioRatesGood->SetMarkerColor(kBlue);
    maxRatioRatesGood->Draw("P");
    maxRatioRatesBad->SetMarkerStyle(8);
    maxRatioRatesBad->SetMarkerColor(kRed);
    maxRatioRatesBad->Draw("P");

    TLegend* l2 = new TLegend(0.7, 0.9, 0.7, 0.9);
    l2->AddEntry(maxRatioRatesGood, "Ratio >= 1", "P");
    l2->AddEntry(maxRatioRatesBad, "Ratio < 1", "P");
    l2->Draw("same");

    //save empty versions to file
    fout->cd();
    maxNPECut->Write("maxNPECut");
    maxRatioVNPE->Write("maxRatioVNPE");
    maxRatioRatesGood->Write("maxRatioRatesGood");
    maxRatioRatesBad->Write("maxRatioRatesBad");

    c1->Write("MaxCoincidenceRates");
    c2->Write("MaxCoincidenceRatio");
    c3->Write("MaxNPECutVChannel");
    c4->Write("MaxCoincidenceRateVNPE");
    c5->Write("AllTripleCoincidences");
    c6->Write("AllDoubleCoincidences");
    c7->Write("MaxRatioRates");
    fout->Close();

    return;
}