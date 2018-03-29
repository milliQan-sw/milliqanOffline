#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip> // for setw()
#include <time.h>
#include <sys/stat.h>
#include <sys/types.h>


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
#include "TLegend.h"
#include "TColor.h"
#include "/net/cms26/cms26r0/milliqan/milliDAQ/interface/GlobalEvent.h"

#include <string>

#ifdef __MAKECINT__
#pragma link C++ class std::vector < std::vector<int> >+;
#pragma link C++ class std::vector < std::vector<float> >+;
#endif

using namespace std;

//////////////////////////////////////////

// Compile like this:
// g++ -o make_tree make_tree.C /net/cms26/cms26r0/milliqan/milliDAQ/libMilliDAQ.so `root-config --cflags --glibs` -Wno-narrowing

//////////////////////////////////////////

//gSystem->Load("/net/cms26/cms26r0/milliqan/MilliDAQ/libMilliDAQ.so");

//Configurable parameters
int numChan=32;
int maxEvents=-1; 
float sideband_range[2] = {0,50}; //in ns
float presampleStart= 17.5;
float presampleEnd = 2.5; 
//Measure presample from t0-17.5 to t0-2.5 ns

float sample_rate = 1.6;
bool debug=false;

//Read output from new format instead of interactiveDAQ
bool milliDAQ=true;

//Activated to display specific events
bool displayMode=false;

vector<TString> tubeSpecies = {"ET","ET","ET","ET",             // 0 1 2 3 
    "R878","R878","R878","ET",       // 4 5 6 7	
    "R878","R7725","R7725","R878",	// 8 9 10 11
    "R878","R878","R878","R878"};    // 12 13 14 15

// vector<int> layerMap = {1,1,1,1,    // 0 1 2 3 
//     2,2,2,2,   // 4 5 6 7	
//     3,3,3,3,	// 8 9 10 11
//     -2,0,-3,-1};    // 12 13 14 15

   


vector< vector<int> > chanMap =
//col,row,layer,type (xyz) 

//types- bars:0, slabs:1, sheets=2
//for sheets: column is -1,0,+1 for left, top, right
//for slabs: column is 0
//For slabs/sheets: row is redundant with type (= -1*type) 
{{1,3,1,0}, //0.0
 {2,3,1,0}, //0.1
 {1,3,3,0}, //0.2
 {2,3,3,0}, //0.3
 {1,1,3,0}, //0.4
 {2,1,3,0}, //0.5
 {1,3,2,0}, //0.6
 {2,3,2,0}, //0.7
 {1,1,1,0}, //0.8
 {2,1,1,0}, //0.9
 {0,-2,1,2}, //0.10
 {0,-2,2,2}, //0.11
 {1,1,2,0}, //0.12
 {2,1,2,0}, //0.13
 {0,-2,3,2}, //0.14
 {0,0,0,3}, //0.15, timing card
 {1,2,2,0}, //1.0
 {2,2,2,0}, //1.1
 {0,-1,0,1}, //1.2
 {1,-2,2,2}, //1.3
 {0,-1,1,1}, //1.4
 {0,-1,3,1}, //1.5
 {1,2,3,0}, //1.6
 {2,2,3,0}, //1.7
 {1,2,1,0}, //1.8
 {2,2,1,0}, //1.9
 {1,-2,3,2}, //1.10
 {-1,-2,1,2}, //1.11
 {0,-1,2,1}, //1.12
 {1,-2,1,2}, //1.13
 {-1,-2,2,2}, //1.14
 {-1,-2,3,2} //1.15
 };






//given channel number, this returns position index running through positions in physical order
   // this config corresponds to 
   // Layer 1   Layer 2    Layer 3
   // ch0 ch1   ch6 ch7    ch14 ch15
   // ch2 ch3   ch12 ch13  ch10 ch11
   // ch4 ch5   ch8 ch9    none none
 




/*vector<int> colors = {kBlack, kRed,
  kGreen+2, kBlue,
  kOrange-3, kPink-8,
  kAzure, kBlack,
  kGray+2, kBlue+1,
  kMagenta+1, kSpring+7,
  kBlack, kOrange+3,
  kBlue-7, kGreen-2};
  */



vector<float> reds ={255./255.,31./255.,235./255.,111./255.,219./255.,151./255.,185./255.,194./255.,127./255.,98./255.,211./255.,69./255.,220./255.,72./255.,225./255.,145./255.,233./255.,125./255.,147./255.,110./255.,209./255.,44};
vector<float> greens={255./255.,30./255.,205./255.,48./255.,106./255.,206./255.,32./255.,188./255.,128./255.,166./255.,134./255.,120./255.,132./255.,56./255.,161./255.,39./255.,232./255.,23./255.,173./255.,53./255.,45./255.,54};
vector<float> blues={255./255.,30./255.,62./255.,139./255.,41./255.,230./255.,54./255.,130./255.,129./255.,71./255.,178./255.,179./255.,101./255.,150./255.,49./255.,139./255.,87./255.,22./255.,60./255.,21./255.,39./255.,23};

vector<TColor *> palette;
vector<int> colors;


//Declare global variables
vector<TH1D*> waves;
// float intraModuleCalibrations[] = {0.,0.,-2.69,-7.25,0.5,0.,2.0,9.92,1.37,0.,-3.85,-3.67,-1.65,0.,-24.21,-5.05};
// float interModuleCalibrations[] = {0.,0.,0.,0.,-6.07,-6.07,-6.07,-6.07,8.38,8.38,8.38,8.38,-6.07,0.,8.38,0.};
float intraModuleCalibrations[] = {0.0, 0.0, -2.5, -7.5, 0.625, 0.0, 1.875, 10.0, 1.25, 0.0, -3.75, -3.75, -1.875, 0.0, -24.375, -5.0};
float interModuleCalibrations[] = {0.0, 0.0, 0.0, 0.0, -6.25, -6.25, -6.25, -6.25, 8.125, 8.125, 8.125, 8.125, -6.25, 0.0, 8.125, 0.0};
float channelCalibrations[16];
// float channelCalibrations[] = {0.,0.,-2.17,-7.49,0.48,0.,1.17,11.44,1.15,0.,-6.41,-4.81,1.2,0.,25.7,6.8};
TTree * inTree;
TTree * outTree;

Long64_t initTDC=-1;
Long64_t initSecs=-1;
Long64_t prevTDC=-1;

int nRollOvers=0;

int event = 0;
int fileNum=0;
int runNum=0;
Long64_t event_time_b0=0;
Long64_t event_time_b1=0;
double event_time_fromTDC=0;
bool present_b0;
bool present_b1;
int t_since_fill_start=0;
string event_t_string;
Long64_t event_trigger_time_tag_b0;
Long64_t event_trigger_time_tag_b1;
int fillNum;
bool beam;
mdaq::GlobalEvent * evt = new mdaq::GlobalEvent(); //for MilliDAQ output only
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

vector<float> * v_bx;
vector<float> * v_by;
vector<float> * v_bz;


float triggerThreshold = 5;
bool addTriggerTimes = true;


//Temporary sanity check
float max_0;
float max_1;
float max_2;
float max_3;
float max_4;
float max_5;
float max_6;
float max_7;
float max_8;
float max_9;
float max_10;
float max_11;
float max_12;
float max_13;
float max_14;
float max_15;
float max_16;
float max_17;
float max_18;
float max_19;
float max_20;
float max_21;
float max_22;
float max_23;
float max_24;
float max_25;
float max_26;
float max_27;
float max_28;
float max_29;
float max_30;
float max_31;

TString milliqanOfflineDir="/net/cms26/cms26r0/milliqan/milliqanOffline/";

void make_tree(TString fileName, int eventNum=-1, TString tag="",float rangeMin=-1.,float rangeMax=-1.);
void loadFillList(TString fillFile=milliqanOfflineDir+"collisionsTimeList.txt");
vector<TString> getFieldFileList(TString location);
void loadFieldList(TString fieldFile);
pair<int,int> findFill(int seconds);
int findField(int seconds);
void loadBranchesMilliDAQ();
void loadWavesMilliDAQ();
void loadBranchesInteractiveDAQ();
void prepareOutBranches();
void clearOutBranches();
vector< vector<float> > processChannel(int ic);
void prepareWave(int ic, float &sb_mean, float &sb_RMS);
vector< vector<float> > findPulses(int ic);
void findTriggerCandidates(int ic, float sb_mean);
vector< vector<float> > findPulses_inside_out(int ic);
void displayPulse(int ic, float begin, float end, int ipulse);
void displayEvent(vector<vector<vector<float> > > bounds,TString tag,float rangeMin,float rangeMax,bool calibrateDisplay);
void h1cosmetic(TH1D* hist,int ic);
void getFileCreationTime(const char *path);
vector<int> eventsPrinted(32,0);
TString displayDirectory;
void writeVersion();
string GetStdoutFromCommand(string cmd);

pair<float,float> measureSideband(int ic, float start, float end);

void defineColors(){
    for(int icolor=0;icolor<reds.size();icolor++){
	palette.push_back(new TColor(2000+icolor,reds[icolor],greens[icolor],blues[icolor]));
	colors.push_back(2000+icolor);
    }
    colors[9] = 419; //kGreen+3;
    colors[2] = 2009;
    //colors[3] = 2013;
    colors[12]= 30;
    colors[0]=28;

}

//Fill list tuple format:
//start time [s], end time [s], fill number, luminosity
vector<std::tuple<int, int, int, float>> fillList; 

//timestamp x1 y1 z1 ... x4 y4 z4
vector<std::tuple<int, float,float,float,float,float,float,float,float,float,float,float,float >> fieldList; 

# ifndef __CINT__  // the following code will be invisible for the interpreter
int main(int argc, char **argv)
{
    if(argc==2) make_tree(argv[1]);
    else if(argc==3) make_tree(argv[1],stoi(argv[2]));
    else if(argc==4) make_tree(argv[1],stoi(argv[2]),argv[3]);
    else if(argc==6) make_tree(argv[1],stoi(argv[2]),argv[3],stof(argv[4]),stof(argv[5]));

}
# endif


void make_tree(TString fileName, int eventNum, TString tag, float rangeMin,float rangeMax){
    //	gROOT->ProcessLine( "gErrorIgnoreLevel = kError");
    for (int i=0;i<=15;i++) {channelCalibrations[i] = interModuleCalibrations[i]+intraModuleCalibrations[i];}
    bool calibrateDisplay = true;
    defineColors();
    if(eventNum>=0) displayMode=true;
    if(displayMode) cout<<"Display tag is "<<tag<<endl;
    loadFillList();


    TString inFileName = fileName;
    TFile *f = TFile::Open(inFileName, "READ");


    TString baseFileName= ((TObjString*)inFileName.Tokenize("/")->Last())->String().Data();

    //Get run number from file name
    TString runNumber = ((TObjString*)baseFileName.Tokenize(".")->At(0))->String().Data();
    runNumber.ReplaceAll("MilliQan_Run","");
    runNum=atoi(runNumber.Data());

    //Get file number from file name
    TString fileNumber = ((TObjString*)baseFileName.Tokenize(".")->At(1))->String().Data();
    fileNumber = ((TObjString*)fileNumber.Tokenize("_")->At(0))->String().Data();
    fileNum=atoi(fileNumber.Data());

    //Get config name from filename
    TString configName = ((TObjString*)baseFileName.Tokenize(".")->At(1))->String().Data();
    configName = ((TObjString*)configName.Tokenize("_")->At(1))->String().Data();
    configName.ReplaceAll(".root","");


    baseFileName="UX5"+baseFileName;
    baseFileName.ReplaceAll(".root","");


    TString version = GetStdoutFromCommand("git describe --tag --abbrev=0");

    TString treeDirectory= milliqanOfflineDir+"trees_"+version+"/Run"+to_string(runNum)+"_"+configName+"/";
    TString linkDirectory= milliqanOfflineDir+"trees/Run"+to_string(runNum)+"_"+configName+"/";

    cout<<"Run "<<runNum<<", file "<<fileNum<<endl;
    if(milliDAQ) inTree = (TTree*)f->Get("Events"); 
    else inTree = (TTree*)f->Get("data"); 

    if(maxEvents<0) maxEvents=inTree->GetEntries();
    if(!displayMode) cout<<"Entries: "<<inTree->GetEntries()<<endl;
    if((int)tubeSpecies.size()!=numChan) cout<<"Tube species map does not match number of channels"<<endl;

    if(milliDAQ) loadBranchesMilliDAQ();
    else loadBranchesInteractiveDAQ();	


    gSystem->mkdir(milliqanOfflineDir+"trees_"+version);	
    gSystem->mkdir(treeDirectory);	
    gSystem->mkdir(linkDirectory);
    TString outFileName = treeDirectory+baseFileName+"_"+version+".root";
    TFile * outFile;

    if(!displayMode){
    	outFile = new TFile(outFileName,"recreate");
    	outTree = new TTree("t","t");
    	prepareOutBranches();
        writeVersion();
    }

   

    displayDirectory = milliqanOfflineDir+"displays/Run"+to_string(runNum)+"_"+configName+"/";
    gSystem->mkdir(displayDirectory);




    //if(!displayMode)
    cout<<"Starting event loop"<<endl;

    //Load entry 0 in order to get timestamp of first event to find corret field information
    inTree->GetEntry(0);
    TString fieldFileLocation ="/net/cms26/cms26r0/milliqan/EnvironSensorData";
    vector<TString> fieldFiles = getFieldFileList(fieldFileLocation);
    for(int i=0;i<fieldFiles.size();i++){
        loadFieldList(fieldFiles[i]);
    }

    for(int i=0;i<maxEvents;i++){
	if(displayMode && i!=eventNum) continue; //Find specified event
	if(i%1000==0) cout<<"Processing event "<<i<<endl;
	inTree->GetEntry(i);
	//cout<<"Got entry "<<i<<endl;
	if(milliDAQ) loadWavesMilliDAQ();
	//if(!displayMode) 
	clearOutBranches();
	event=i;

	if(milliDAQ){
	    //Waveforms are not inverted yet- done in processChannel
	    max_0= -1.*waves[0]->GetMinimum();
	    max_1= -1.*waves[1]->GetMinimum();
	    max_2= -1.*waves[2]->GetMinimum();
	    max_3= -1.*waves[3]->GetMinimum();
	    max_4= -1.*waves[4]->GetMinimum();
	    max_5= -1.*waves[5]->GetMinimum();
	    max_6= -1.*waves[6]->GetMinimum();
	    max_7= -1.*waves[7]->GetMinimum();
	    max_8= -1.*waves[8]->GetMinimum();
	    max_9= -1.*waves[9]->GetMinimum();
	    max_10= -1.*waves[10]->GetMinimum();
	    max_11= -1.*waves[11]->GetMinimum();
	    max_12= -1.*waves[12]->GetMinimum();
	    max_13= -1.*waves[13]->GetMinimum();
	    max_14= -1.*waves[14]->GetMinimum();
	    max_15= -1.*waves[15]->GetMinimum();
        max_16= -1.*waves[16]->GetMinimum();
        max_17= -1.*waves[17]->GetMinimum();
        max_18= -1.*waves[18]->GetMinimum();
        max_19= -1.*waves[19]->GetMinimum();
        max_20= -1.*waves[20]->GetMinimum();
        max_21= -1.*waves[21]->GetMinimum();
        max_22= -1.*waves[22]->GetMinimum();
        max_23= -1.*waves[23]->GetMinimum();
        max_24= -1.*waves[24]->GetMinimum();
        max_25= -1.*waves[25]->GetMinimum();
        max_26= -1.*waves[26]->GetMinimum();
        max_27= -1.*waves[27]->GetMinimum();
        max_28= -1.*waves[28]->GetMinimum();
        max_29= -1.*waves[29]->GetMinimum();
        max_30= -1.*waves[30]->GetMinimum();
        max_31= -1.*waves[31]->GetMinimum();

	}
    
	if(milliDAQ) {
        if(initSecs<0){ //if timestamps for first event are uninitialized
            if(evt->digitizers[0].DataPresent){ //If this event exists
                initSecs=evt->digitizers[0].DAQTimeStamp.GetSec();
                initTDC=evt->digitizers[0].TDC[0];
                prevTDC=initTDC;
            }
        }

        int secs = evt->digitizers[0].DAQTimeStamp.GetSec();
	    //This defines the time in seconds in standard unix epoch since 1970
	    event_time_b0 = secs;

        Long64_t thisTDC = evt->digitizers[0].TDC[0];
        
        //Check if rollover has happened since last event: if previous time is more than 10 minutes later than current time 
        //NB events are not written strictly in chronological order
        Long64_t diff = prevTDC - thisTDC;
        if(diff > 1.2e+11) nRollOvers++;
        //For each tDC rollover: add max value: pow(2,40)
        event_time_fromTDC = 5.0e-9*(thisTDC+nRollOvers*pow(2,40)-initTDC)+initSecs;
        //update previous TDC holder for next event
        prevTDC = thisTDC;


        //in case second digitizer has different time
        secs = evt->digitizers[1].DAQTimeStamp.GetSec();
        event_time_b1 = secs;


	    event_trigger_time_tag_b0 = evt->digitizers[0].TriggerTimeTag;
        event_trigger_time_tag_b1 = evt->digitizers[1].TriggerTimeTag;

	    //event_t_string = evt->digitizers[0].DAQTimeStamp.AsString("s");
        event_t_string = TTimeStamp(event_time_fromTDC).AsString("s");

	    for(int ig=0; ig<8; ig++){
    		v_groupTDC_b0->push_back(evt->digitizers[0].TDC[ig]);
            v_groupTDC_b1->push_back(evt->digitizers[1].TDC[ig]);
	    }	

        present_b0 = evt->digitizers[0].DataPresent;
        present_b1 = evt->digitizers[1].DataPresent;

        fillNum=0;
        t_since_fill_start= -1;
        secs = round(event_time_fromTDC);
        pair<int,int> fillInfo = findFill(secs);
        fillNum= fillInfo.first;
        t_since_fill_start=fillInfo.second;

        if(fillNum>0) beam=true;
        else beam = false;

       // cout<<"This secs "<<secs<<endl;
        int fieldPoint =  findField(secs);
        //cout<<"This field point "<<fieldPoint<<endl;
        if(fieldPoint>=0){
            v_bx->push_back(get<1>(fieldList[fieldPoint]));
            v_bx->push_back(get<4>(fieldList[fieldPoint]));
            v_bx->push_back(get<7>(fieldList[fieldPoint]));
            v_bx->push_back(get<10>(fieldList[fieldPoint]));

            v_by->push_back(get<2>(fieldList[fieldPoint]));
            v_by->push_back(get<5>(fieldList[fieldPoint]));
            v_by->push_back(get<8>(fieldList[fieldPoint]));
            v_by->push_back(get<11>(fieldList[fieldPoint]));

            v_bz->push_back(get<3>(fieldList[fieldPoint]));
            v_bz->push_back(get<6>(fieldList[fieldPoint]));
            v_bz->push_back(get<9>(fieldList[fieldPoint]));
            v_bz->push_back(get<12>(fieldList[fieldPoint]));
        }
        else{
            v_bx->push_back(-50);
            v_bx->push_back(-50);
            v_bx->push_back(-50);
            v_bx->push_back(-50);

            v_by->push_back(-50);
            v_by->push_back(-50);
            v_by->push_back(-50);
            v_by->push_back(-50);

            v_bz->push_back(-50);
            v_bz->push_back(-50);
            v_bz->push_back(-50);
            v_bz->push_back(-50);
        }
        //get<2>(fillList[index_of_first_fill_with_larger_start_time-1])


	}
	else{ event_time_b0=0;event_time_b1=0;event_t_string="";fillNum=0;beam=false;}

	vector<vector<vector<float> > > allPulseBounds;
	for(int ic=0;ic<numChan;ic++){
	    if(ic==15){//skip timing card channel
    		vector<vector<float> > empty;
    		allPulseBounds.push_back(empty);
    		continue;
	    }
	    //	cout<<Form("Chan %i min: ",ic)<<waves[ic]->GetMinimum()<<endl;

	    allPulseBounds.push_back(processChannel(ic));
	}
	if(displayMode) displayEvent(allPulseBounds,tag,rangeMin,rangeMax,calibrateDisplay);
	else outTree->Fill();
    }
    if(!displayMode) cout<<"Processed "<<maxEvents<<" events."<<endl;

    if(!displayMode){
	outTree->Write();
	outFile->Close();
    
	cout<<"Closed output tree."<<endl;
	//TString currentDir=gSystem->pwd();
	//TString target = currentDir+"/"+outFileName;
	TString target = outFileName;
	TString linkname =linkDirectory+baseFileName+".root";
	remove(linkname); //remove if already exists
	gSystem->Symlink(target,linkname);
	cout<<"Made link to "<<target<<" called "<<linkname<<endl;
    }
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

    //Find sideband
    pair<float,float> mean_rms = measureSideband(ic,sideband_range[0],sideband_range[1]);
    sb_mean = mean_rms.first;
    sb_RMS = mean_rms.second;
    //subtract sideband
    for(int ibin = 1; ibin <= waves[ic]->GetNbinsX(); ibin++){
	waves[ic]->SetBinContent(ibin,waves[ic]->GetBinContent(ibin)-sb_mean);
    }
}

//Measure mean and RMS of samples in range from start to end (in ns)
pair<float,float> measureSideband(int ic, float start, float end){

    float sum_sb=0.;
    float sum2_sb=0.;
    int startbin = waves[ic]->FindBin(start);
    int endbin = waves[ic]->FindBin(end);
    int n_sb = endbin-startbin+1;
    for(int ibin=startbin; ibin <= endbin; ibin++){
	sum_sb = sum_sb + waves[ic]->GetBinContent(ibin);
	sum2_sb = sum2_sb + pow(waves[ic]->GetBinContent(ibin),2);
	n_sb++;
    }
    if(n_sb == 0) n_sb = 1.;
    float mean = sum_sb/n_sb;
    float RMS =pow( sum2_sb/n_sb - pow(mean,2), 0.5);

    return make_pair(mean,RMS);

}


vector< vector<float> > processChannel(int ic){
    float sb_mean, sb_RMS;
    prepareWave(ic, sb_mean, sb_RMS);

    vector<vector<float> > pulseBounds;
    //if(tubeSpecies[ic]!="ET") 
    pulseBounds = findPulses(ic);
    if (addTriggerTimes) findTriggerCandidates(ic,sb_mean);
    //else pulseBounds = findPulses_inside_out(ic); //Use inside-out method for narrow ET pulses

    int npulses = pulseBounds.size();
    //float channelCalibrations[] = {0.,0.,-2.0,-7.5,0.5,0.,0.88,12.58,1.22,0.,-6.51,-4.75,1.2,0.,25.7,6.8};
    float channelSPEAreas[] = {60.,81.5,64.5,48.7,55.2,84.8,57.0,57.2,60.,181.6,576.6,60.,77.5,60.,52.6,50.4};
    //NB: v8 march13- currently approximate guess (60 nVs) for unmeasured ch0,ch8,ch11,ch13


    for(int ipulse = 0; ipulse<npulses; ipulse++){
	//Set waveform range to this pulse
	waves[ic]->SetAxisRange(pulseBounds[ipulse][0],pulseBounds[ipulse][1]);
	if(debug) cout<<"Chan "<<ic<<", pulse bounds: "<<pulseBounds[ipulse][0]<<" to "<<pulseBounds[ipulse][1]<<endl;
	//Fill branches


	v_chan->push_back(ic);
    //chanMap: col,row,layer,type
    v_column->push_back(chanMap[ic][0]);
    v_row->push_back(chanMap[ic][1]);
    v_layer->push_back(chanMap[ic][2]);
	v_type->push_back(chanMap[ic][3]);

	v_height->push_back(waves[ic]->GetMaximum());
	v_time->push_back(pulseBounds[ipulse][0]);
	v_time_module_calibrated->push_back(pulseBounds[ipulse][0]+channelCalibrations[ic]);
	v_area->push_back(waves[ic]->Integral());
	v_nPE->push_back(waves[ic]->Integral()/channelSPEAreas[ic]);
	v_ipulse->push_back(ipulse);
	v_npulses->push_back(npulses);
	v_duration->push_back(pulseBounds[ipulse][1] - pulseBounds[ipulse][0]);
	if(ipulse>0) v_delay->push_back(pulseBounds[ipulse][0] - pulseBounds[ipulse-1][1]); //interval between end of previous pulse and start of this one
	else v_delay->push_back(1999.);

	v_sideband_mean->push_back(sb_mean);
	v_sideband_RMS->push_back(sb_RMS);	

	//get presample info
	pair<float,float> presampleInfo = measureSideband(ic,pulseBounds[ipulse][0]-presampleStart,pulseBounds[ipulse][0]-presampleEnd);
	v_presample_mean->push_back(presampleInfo.first);
	v_presample_RMS->push_back(presampleInfo.second);	
	bool quiet = (fabs(presampleInfo.first)<1. && presampleInfo.second <2.0 )&& (pulseBounds[ipulse][1] < waves[ic]->GetBinLowEdge(waves[ic]->GetNbinsX())-0.01) ;
	v_quiet->push_back(quiet); //preliminary: mean between -1 and 1, and RMS<2

	//if(event<0 || eventsPrinted[ic]<0) displayPulse(ic,pulseBounds[ipulse][0],pulseBounds[ipulse][1],ipulse);
    }
    //if(event<0 || (event<0 && npulses>0) || eventsPrinted[ic]<0) {displayEvent(ic,pulseBounds); eventsPrinted[ic]++;}
    return pulseBounds;
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
    h1cosmetic(waves[ic],ic);	
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

void displayEvent(vector<vector<vector<float> > > bounds, TString tag,float rangeMin,float rangeMax,bool calibrateDisplay){
    TCanvas c("c1","",1400,800);
    gPad->SetRightMargin(0.39);
    gStyle->SetGridStyle(3);
    gStyle->SetGridColor(13);
    c.SetGrid();

    gStyle->SetTitleX(0.35);
    vector<int> chanList;
    float maxheight=0;
    float timeRange[2];
    timeRange[0]=1024./sample_rate; timeRange[1]=0.;
    vector<vector<vector<float>>> boundsShifted;
    vector<TH1D*> wavesShifted;
    for(uint ic=0;ic<bounds.size();ic++){
	vector<vector<float>> boundShifted = bounds[ic];
	TH1D * waveShifted = (TH1D*) waves[ic]->Clone();
	if(calibrateDisplay){
	    waveShifted->Reset();

	    for (uint iBin = 1;iBin <= waves[ic]->GetNbinsX();iBin++)
	    {
		float binLowEdgeShifted = waves[ic]->GetBinLowEdge(iBin) + channelCalibrations[ic];
		int iBinShifted = waveShifted->FindBin(binLowEdgeShifted + 1E-4);
		if (iBinShifted > 0 && iBinShifted <= waves[ic]->GetNbinsX()){
		    waveShifted->SetBinContent(iBinShifted,waves[ic]->GetBinContent(iBin));
		    waveShifted->SetBinError(iBinShifted,waves[ic]->GetBinError(iBin));
		}

	    }
	    for(uint iBoundVec =0;iBoundVec < bounds[ic].size();iBoundVec++)
		for(uint iBoundVec2 =0;iBoundVec2 < bounds[ic][iBoundVec].size();iBoundVec2++)
		    boundShifted[iBoundVec][iBoundVec2] += channelCalibrations[ic]; 
	}
	if(boundShifted.size()>0 || waveShifted->GetMaximum()>5){
	    chanList.push_back(ic);
	    //Reset range to find correct maxima
	    waveShifted->SetAxisRange(0,1024./sample_rate);
	    //Keep track of max amplitude
	    if(waveShifted->GetMaximum()>maxheight) maxheight=waveShifted->GetMaximum();
	    if(boundShifted.size()>0){
		//keep track of earliest pulse start time
		if(boundShifted[0][0]<timeRange[0]) timeRange[0]=boundShifted[0][0];
		//keep track of latest pulse end time (pulses are ordered chronologicaly for each channel)
		if(boundShifted[boundShifted.size()-1][1]>timeRange[1]) timeRange[1]=boundShifted[boundShifted.size()-1][1];
	    }
	    TString beamState = "off";
	    if(beam) beamState="on";
	    if (calibrateDisplay) waveShifted->SetTitle(Form("Run %i, File %i, Event %i (beam %s);Time [ns];Amplitude [mV];",runNum,fileNum,event,beamState.Data()));
	    else waveShifted->SetTitle(Form("Run %i, File %i, Event %i (beam %s);Uncalibrated Time [ns];Amplitude [mV];",runNum,fileNum,event,beamState.Data()));
	}
	wavesShifted.push_back(waveShifted);
	boundsShifted.push_back(boundShifted);
    }
    maxheight*=1.1;

    //maxheight=30;
    if (rangeMin < 0) timeRange[0]*=0.9;
    else timeRange[0] = rangeMin;
    if (rangeMax < 0) timeRange[1]= min(1.1*timeRange[1],1024./sample_rate);
    else timeRange[1] = rangeMax;

    float depth = 0.075*chanList.size();
    TLegend leg(0.45,0.9-depth,0.65,0.9);
    for(uint i=0;i<chanList.size();i++){
	int ic = chanList[i];	
    if(ic==15) continue;
	wavesShifted[ic]->SetAxisRange(timeRange[0],timeRange[1]);
	wavesShifted[ic]->SetMaximum(maxheight);
    int column= chanMap[ic][0];
    int row= chanMap[ic][1];
    int layer= chanMap[ic][2];
    int type= chanMap[ic][3];
    int oldChanPos = 4-2*(row-1)+column-1+6*(layer-1);
    if(type!=0) continue;
	h1cosmetic(wavesShifted[ic],oldChanPos);
	if(i==0) wavesShifted[ic]->Draw("hist");
	else wavesShifted[ic]->Draw("hist same");

	leg.AddEntry(wavesShifted[ic],Form("Channel %i",ic),"l");
	//Show boundaries of pulse

	TLine line; line.SetLineWidth(2); line.SetLineStyle(2);	line.SetLineColor(colors[oldChanPos]);
	for(uint ip=0; ip<boundsShifted[ic].size();ip++){
	    if (boundsShifted[ic][ip][0] > timeRange[0] && boundsShifted[ic][ip][1] < timeRange[1]){
		line.DrawLine(boundsShifted[ic][ip][0],0,boundsShifted[ic][ip][0],0.2*maxheight);
		line.DrawLine(boundsShifted[ic][ip][1],0,boundsShifted[ic][ip][1],0.2*maxheight);
	    }
	}
	//Display values stored for this pulse
    }
    float boxw= 0.025;
    float boxh=0.0438;
    float barw=0.03;
    float barh=0.53;
 //    vector<float> xpos = {0.93,0.96,0.93,0.96,0.93,0.96,
	// 0.815,0.845,0.815,0.845,0.815,0.845,
	// 0.7,0.73,0.7,0.73,0.7,0.73
 //    };

    vector<float> xstart = {0.66,0.78,0.9};
    vector<float> ystart= {0.798,0.851,0.904};

    float sheet_width = 0.006;
    float sheet_offset= 0.013+sheet_width/2.;
    float sheet_left_to_right = 4*0.006+barw+boxw+0.002;
    vector<float> xstart_leftsheets = {xstart[0]-sheet_offset,xstart[1]-sheet_offset,xstart[2]-sheet_offset}; 
    vector<float> xstart_topsheets = {xstart[0]-0.002,xstart[1]-0.002,xstart[2]-0.002};
    float ystart_topsheets = ystart[2]+boxh+0.017;
    float ystart_sidesheets = ystart[0]-0.006;
    float vert_sheet_length = ystart[2]-ystart[0]+boxh+0.01;
    float hori_sheet_length= barw+boxw+0.004;
    
    float slab_width = 0.015;
    vector<float> slab_xstart = {xstart_leftsheets[0]-0.008-slab_width,xstart_leftsheets[1]-0.008-slab_width,xstart_leftsheets[2]-0.008-slab_width,xstart_leftsheets[2]+0.01+sheet_left_to_right}; 
    float slab_height = vert_sheet_length-0.02;
    float slab_ystart = ystart_sidesheets+0.01;
    // vector<float> ypos = 
    // {0.924,0.924,0.871,0.871,0.818,0.818,
    //     0.924,0.924,0.871,0.871,0.818,0.818,
    //     0.924,0.924,0.871,0.871,0.818,0.818
    // };

    TPave L1frame(xstart[0]-0.006,ystart[0]-0.01,xstart[0]+barw+boxw+0.006,ystart[2]+boxh+0.01,1,"NDC");
    L1frame.SetFillColor(0);
    L1frame.SetLineWidth(2);
    L1frame.Draw();

    TPave L2frame(xstart[1]-0.006,ystart[0]-0.01,xstart[1]+barw+boxw+0.006,ystart[2]+boxh+0.01,1,"NDC");
    L2frame.SetFillColor(0);
    L2frame.SetLineWidth(2);
    L2frame.Draw();

    TPave L3frame(xstart[2]-0.006,ystart[0]-0.01,xstart[2]+barw+boxw+0.006,ystart[2]+boxh+0.01,1,"NDC");
    L3frame.SetFillColor(0);
    L3frame.SetLineWidth(2);
    L3frame.Draw();


    TLatex tla;
    tla.SetTextSize(0.04);
    tla.SetTextFont(42);
    float height= 0.06;
    //tla.DrawLatexNDC(0.13,0.83,Form("Number of pulses: %i",(int)bounds.size()));
    float currentYpos=0.737;
    float headerX=0.67;
    float rowX=0.69;
    int pulseIndex=0; // Keep track of pulse index, since all pulses for all channels are actually stored in the same 1D vectors
    int maxPerChannel = 10/chanList.size();

    for(int i=0;i<32;i++){
	if(boundsShifted[i].size()>0 || wavesShifted[i]->GetMaximum()>10 ){//if this channel has a pulse
	    if(i==15) continue;
        //xyz
        int column= chanMap[i][0];
        int row= chanMap[i][1];
        int layer= chanMap[i][2];
        int type= chanMap[i][3];
        if (type==1){
            float xpos,ypos;
            ypos = slab_ystart;
            xpos = slab_xstart[layer];
            TPave * pave = new TPave(xpos,ypos,xpos+slab_width,ypos+slab_height,0,"NDC");
            pave->SetFillColor(kBlack);
            //pave->Draw();
        }

        else if (type==2){
            float xpos,ypos;
            TPave * pave;
            if (column!=0){
                xpos= xstart_leftsheets[layer-1];
                if(column>0) xpos += sheet_left_to_right;
                ypos = ystart_sidesheets;
                pave = new TPave(xpos,ypos,xpos+sheet_width,ypos+vert_sheet_length,0,"NDC");
            }
            else{
                xpos = xstart_topsheets[layer-1];
                ypos = ystart_topsheets;
                pave = new TPave(xpos,ypos,xpos+hori_sheet_length,ypos+1.4/0.8*sheet_width,0,"NDC");
            }
           
            pave->SetFillColor(kBlack);
           // pave->Draw();

        }
        else if(type==0){
        float xpos = xstart[layer-1]+(column-1)*barw;
        float ypos= ystart[row-1];

        int oldChanPos = 4-2*(row-1)+column-1+6*(layer-1);
        

        TPave * pave = new TPave(xpos,ypos,xpos+boxw,ypos+boxh,0,"NDC");
	    pave->SetFillColor(colors[oldChanPos]);
	    pave->Draw();
	    tla.SetTextColor(colors[oldChanPos]);
	    tla.SetTextSize(0.04);
	    tla.DrawLatexNDC(headerX,currentYpos,Form("Channel %i, N_{pulses}= %i",i,(int)boundsShifted[i].size()));
	    tla.SetTextColor(kBlack);
	    currentYpos-=height;
	    tla.SetTextSize(0.035);
	    for(int ip=0;ip<boundsShifted[i].size();ip++){
		TString digis="%.1f";
		if(v_height->at(pulseIndex)>10) digis = "%.0f";
		TString row;
		if (calibrateDisplay) row = Form("%.0f ns: "+digis+" mV, %.0f pVs, %.0f ns",v_time_module_calibrated->at(pulseIndex),v_height->at(pulseIndex),v_area->at(pulseIndex),v_duration->at(pulseIndex));
		else row = Form("%.0f ns: "+digis+" mV, %.0f pVs, %.0f ns",v_time->at(pulseIndex),v_height->at(pulseIndex),v_area->at(pulseIndex),v_duration->at(pulseIndex));
		pulseIndex++; 
		if(ip < maxPerChannel){			
		    tla.DrawLatexNDC(rowX,currentYpos,row);
		    currentYpos-=height*0.8;
		}
	    }
	    currentYpos-=height*0.2;
	}
    }
    }


    // tla.DrawLatexNDC(0.13,0.78,Form("Area: %0.2f",v_area->back()));
    // tla.DrawLatexNDC(0.13,0.73,Form("Duration: %0.2f",v_duration->back()));
    // leg.Draw();
    cout<<"Display directory is "<<displayDirectory<<endl;
    c.Print(Form(displayDirectory+"Run%i_File%i_Event%i_%s.pdf",runNum,fileNum,event,tag.Data()));
}

void findTriggerCandidates(int ic,float sb_mean){
    float tstart = sideband_range[1]+1;
    int istart = waves[ic]->FindBin(tstart);
    float v;
    bool inTrigger = false;
    for (int i=istart; i<=waves[ic]->GetNbinsX(); i++) { // Loop over all samples looking for pulses
	v = waves[ic]->GetBinContent(i);
	// if (ic == 7) std::cout  << triggerThreshold << " "<< waves[ic]->GetMaximum()+ sb_mean << " "<< max_7  << std::endl;
	// std::cout << sb_mean << std::endl;
	// std::cout << waves[ic]->GetBinContent(i) << std::endl;
	// std::cout << triggerThreshold << std::endl;
	if (waves[ic]->GetBinContent(i) + sb_mean >= triggerThreshold){
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
}
vector< vector<float> > findPulses(int ic){
    //Configurable:
    int Nconsec = 4;
    int NconsecEnd = 3;
    float thresh = 2.5; //mV

    vector<vector<float> > bounds;
    float tstart = sideband_range[1]+1;
    int istart = waves[ic]->FindBin(tstart);

    // Now hunt for pulses
    bool inpulse = false;
    int nover = 0; // Number of samples seen consecutively over threshold
    int nunder = 0; // Number of samples seen consecutively under threshold
    int i_begin = istart;
    int i_stop_searching = waves[ic]->GetNbinsX()-Nconsec;
    int i_stop_final_pulse = waves[ic]->GetNbinsX();
    // int tWindow[2];
    for (int i=istart; i<i_stop_searching || (inpulse && i<i_stop_final_pulse); i++) { // Loop over all samples looking for pulses
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
	    if (nunder>NconsecEnd || i==(i_stop_final_pulse-1)) { // The end of a pulse, or pulse has reached the end of range 

		//cout<<"DEBUG: i_begin "<<i_begin<<endl;
		// cout<<"DEBUG: tWindow 0 and 1: "<<w.t[i_begin]<<" "<<w.t[i]<<endl;

		bounds.push_back({(float)waves[ic]->GetBinLowEdge(i_begin), (float)waves[ic]->GetBinLowEdge(i+1)-0.01}); //start and end of pulse
		if(debug) cout<<"i_begin, i: "<<i_begin<<" "<<i<<endl;

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


    //MAKE SURE TO ALWAYS ADD BRANCHES TO CLEAR FUNCTION AS WELL

    TBranch * b_event = outTree->Branch("event",&event,"event/I");
    TBranch * b_run = outTree->Branch("run",&runNum,"run/I");
    TBranch * b_file = outTree->Branch("file",&fileNum,"file/I");
    TBranch * b_fill = outTree->Branch("fill",&fillNum,"fill/I");
    TBranch * b_nRollOvers = outTree->Branch("nRollOvers",&nRollOvers,"nRollOvers/I");
    TBranch * b_beam = outTree->Branch("beam",&beam,"beam/O");
    TBranch * b_present_b0 = outTree->Branch("present_b0",&present_b0,"present_b0/O");
    TBranch * b_present_b1 = outTree->Branch("present_b1",&present_b1,"present_b1/O");
    TBranch * b_event_time_b0 = outTree->Branch("event_time_b0",&event_time_b0,"event_time_b0/L");
    TBranch * b_event_time_b1 = outTree->Branch("event_time_b1",&event_time_b1,"event_time_b1/L");
    TBranch * b_event_time_fromTDC = outTree->Branch("event_time_fromTDC",&event_time_fromTDC,"event_time_fromTDC/D");
    TBranch * b_t_since_fill_start = outTree->Branch("t_since_fill_start",&t_since_fill_start,"t_since_fill_start/I");
    TBranch * b_event_t_string = outTree->Branch("event_t_string",&event_t_string);
    TBranch * b_event_trigger_time_tag_b0 = outTree->Branch("event_trigger_time_tag_b0",&event_trigger_time_tag_b0,"event_trigger_time_tag_b0/L");
    TBranch * b_event_trigger_time_tag_b1 = outTree->Branch("event_trigger_time_tag_b1",&event_trigger_time_tag_b1,"event_trigger_time_tag_b1/L");

    TBranch * b_chan = outTree->Branch("chan",&v_chan);
    TBranch * b_triggerCandidates = outTree->Branch("triggerCandidates",&v_triggerCandidates);
    TBranch * b_triggerCandidatesEnd = outTree->Branch("triggerCandidatesEnd",&v_triggerCandidatesEnd);
    TBranch * b_triggerCandidatesChannel = outTree->Branch("triggerCandidatesChannel",&v_triggerCandidatesChannel);
    TBranch * b_layer = outTree->Branch("layer",&v_layer);
    TBranch * b_row = outTree->Branch("row",&v_row);
    TBranch * b_column = outTree->Branch("column",&v_column);
    TBranch * b_type = outTree->Branch("type",&v_type);
    TBranch * b_height = outTree->Branch("height",&v_height);
    TBranch * b_time = outTree->Branch("time",&v_time);
    TBranch * b_time_module_calibrated = outTree->Branch("time_module_calibrated",&v_time_module_calibrated);
    TBranch * b_delay = outTree->Branch("delay",&v_delay);
    TBranch * b_area = outTree->Branch("area",&v_area);
    TBranch * b_nPE = outTree->Branch("nPE",&v_nPE);
    TBranch * b_ipulse = outTree->Branch("ipulse",&v_ipulse);
    TBranch * b_npulses = outTree->Branch("npulses",&v_npulses);
    TBranch * b_duration = outTree->Branch("duration",&v_duration);
    TBranch * b_quiet = outTree->Branch("quiet",&v_quiet);
    TBranch * b_presample_mean = outTree->Branch("presample_mean",&v_presample_mean);
    TBranch * b_presample_RMS = outTree->Branch("presample_RMS",&v_presample_RMS);
    TBranch * b_sideband_mean = outTree->Branch("sideband_mean",&v_sideband_mean);
    TBranch * b_sideband_RMS = outTree->Branch("sideband_RMS",&v_sideband_RMS);

    TBranch * b_groupTDC_b0 = outTree->Branch("groupTDC_b0",&v_groupTDC_b0);
    TBranch * b_groupTDC_b1 = outTree->Branch("groupTDC_b1",&v_groupTDC_b1);

    TBranch * b_bx = outTree->Branch("bx",&v_bx);
    TBranch * b_by = outTree->Branch("by",&v_by);
    TBranch * b_bz = outTree->Branch("bz",&v_bz);

    TBranch * b_max_0 = outTree->Branch("max_0",&max_0,"max_0/F");	
    TBranch * b_max_1 = outTree->Branch("max_1",&max_1,"max_1/F");	
    TBranch * b_max_2 = outTree->Branch("max_2",&max_2,"max_2/F");	
    TBranch * b_max_3 = outTree->Branch("max_3",&max_3,"max_3/F");	
    TBranch * b_max_4 = outTree->Branch("max_4",&max_4,"max_4/F");	
    TBranch * b_max_5 = outTree->Branch("max_5",&max_5,"max_5/F");	
    TBranch * b_max_6 = outTree->Branch("max_6",&max_6,"max_6/F");	
    TBranch * b_max_7 = outTree->Branch("max_7",&max_7,"max_7/F");	
    TBranch * b_max_8 = outTree->Branch("max_8",&max_8,"max_8/F");	
    TBranch * b_max_9 = outTree->Branch("max_9",&max_9,"max_9/F");	
    TBranch * b_max_10 = outTree->Branch("max_10",&max_10,"max_10/F");	
    TBranch * b_max_11 = outTree->Branch("max_11",&max_11,"max_11/F");	
    TBranch * b_max_12 = outTree->Branch("max_12",&max_12,"max_12/F");	
    TBranch * b_max_13 = outTree->Branch("max_13",&max_13,"max_13/F");	
    TBranch * b_max_14 = outTree->Branch("max_14",&max_14,"max_14/F");	
    TBranch * b_max_15 = outTree->Branch("max_15",&max_15,"max_15/F");	
    TBranch * b_max_16 = outTree->Branch("max_16",&max_16,"max_16/F");  
    TBranch * b_max_17 = outTree->Branch("max_17",&max_17,"max_17/F");  
    TBranch * b_max_18 = outTree->Branch("max_18",&max_18,"max_18/F");  
    TBranch * b_max_19 = outTree->Branch("max_19",&max_19,"max_19/F");  
    TBranch * b_max_20 = outTree->Branch("max_20",&max_20,"max_20/F");  
    TBranch * b_max_21 = outTree->Branch("max_21",&max_21,"max_21/F");  
    TBranch * b_max_22 = outTree->Branch("max_22",&max_22,"max_22/F");  
    TBranch * b_max_23 = outTree->Branch("max_23",&max_23,"max_23/F");  
    TBranch * b_max_24 = outTree->Branch("max_24",&max_24,"max_24/F");  
    TBranch * b_max_25 = outTree->Branch("max_25",&max_25,"max_25/F");  
    TBranch * b_max_26 = outTree->Branch("max_26",&max_26,"max_26/F");  
    TBranch * b_max_27 = outTree->Branch("max_27",&max_27,"max_27/F");  
    TBranch * b_max_28 = outTree->Branch("max_28",&max_28,"max_28/F");  
    TBranch * b_max_29 = outTree->Branch("max_29",&max_29,"max_29/F");  
    TBranch * b_max_30 = outTree->Branch("max_30",&max_30,"max_30/F");  
    TBranch * b_max_31 = outTree->Branch("max_31",&max_31,"max_31/F");  




    outTree->SetBranchAddress("event",&event,&b_event);
    outTree->SetBranchAddress("run",&runNum,&b_run);
    outTree->SetBranchAddress("file",&fileNum,&b_file);
    outTree->SetBranchAddress("nRollOvers",&nRollOvers,&b_nRollOvers);
    outTree->SetBranchAddress("event_time_b0",&event_time_b0,&b_event_time_b0);
    outTree->SetBranchAddress("event_time_b1",&event_time_b1,&b_event_time_b1);
    outTree->SetBranchAddress("event_time_fromTDC",&event_time_fromTDC,&b_event_time_fromTDC);
    outTree->SetBranchAddress("t_since_fill_start",&t_since_fill_start,&b_t_since_fill_start);
    outTree->SetBranchAddress("fill",&fillNum,&b_fill);
    outTree->SetBranchAddress("beam",&beam,&b_beam);
    outTree->SetBranchAddress("present_b0",&present_b0,&b_present_b0);
    outTree->SetBranchAddress("present_b1",&present_b1,&b_present_b1);
    outTree->SetBranchAddress("event_trigger_time_tag_b0",&event_trigger_time_tag_b0,&b_event_trigger_time_tag_b0);
    outTree->SetBranchAddress("event_trigger_time_tag_b1",&event_trigger_time_tag_b1,&b_event_trigger_time_tag_b1);

    //outTree->SetBranchAddress("event_t_string",&event_t_string,&b_event_t_string);
    outTree->SetBranchAddress("chan",&v_chan,&b_chan);
    outTree->SetBranchAddress("triggerCandidates",&v_triggerCandidates,&b_triggerCandidates);
    outTree->SetBranchAddress("triggerCandidatesEnd",&v_triggerCandidatesEnd,&b_triggerCandidatesEnd);
    outTree->SetBranchAddress("triggerCandidatesChannel",&v_triggerCandidatesChannel,&b_triggerCandidatesChannel);
    outTree->SetBranchAddress("layer",&v_layer,&b_layer);
    outTree->SetBranchAddress("row",&v_row,&b_row);
    outTree->SetBranchAddress("column",&v_column,&b_column);
    outTree->SetBranchAddress("type",&v_type,&b_type);
    outTree->SetBranchAddress("height",&v_height,&b_height);
    outTree->SetBranchAddress("time_module_calibrated",&v_time_module_calibrated,&b_time_module_calibrated);
    outTree->SetBranchAddress("time",&v_time,&b_time);
    outTree->SetBranchAddress("delay",&v_delay,&b_delay);
    outTree->SetBranchAddress("area",&v_area,&b_area);
    outTree->SetBranchAddress("nPE",&v_nPE,&b_nPE);
    outTree->SetBranchAddress("ipulse",&v_ipulse,&b_ipulse);
    outTree->SetBranchAddress("npulses",&v_npulses,&b_npulses);
    outTree->SetBranchAddress("duration",&v_duration,&b_duration);
    outTree->SetBranchAddress("quiet",&v_quiet,&b_quiet);
    outTree->SetBranchAddress("presample_mean",&v_presample_mean,&b_presample_mean);
    outTree->SetBranchAddress("presample_RMS",&v_presample_RMS,&b_presample_RMS);
    outTree->SetBranchAddress("sideband_mean",&v_sideband_mean,&b_sideband_mean);
    outTree->SetBranchAddress("sideband_RMS",&v_sideband_RMS,&b_sideband_RMS);

    outTree->SetBranchAddress("groupTDC_b0",&v_groupTDC_b0,&b_groupTDC_b0);
    outTree->SetBranchAddress("groupTDC_b1",&v_groupTDC_b1,&b_groupTDC_b1);

    outTree->SetBranchAddress("bx",&v_bx,&b_bx);
    outTree->SetBranchAddress("by",&v_by,&b_by);
    outTree->SetBranchAddress("bz",&v_bz,&b_bz);

    outTree->SetBranchAddress("max_0",&max_0,&b_max_0);
    outTree->SetBranchAddress("max_1",&max_1,&b_max_1);
    outTree->SetBranchAddress("max_2",&max_2,&b_max_2);
    outTree->SetBranchAddress("max_3",&max_3,&b_max_3);
    outTree->SetBranchAddress("max_4",&max_4,&b_max_4);
    outTree->SetBranchAddress("max_5",&max_5,&b_max_5);
    outTree->SetBranchAddress("max_6",&max_6,&b_max_6);
    outTree->SetBranchAddress("max_7",&max_7,&b_max_7);
    outTree->SetBranchAddress("max_8",&max_8,&b_max_8);
    outTree->SetBranchAddress("max_9",&max_9,&b_max_9);
    outTree->SetBranchAddress("max_10",&max_10,&b_max_10);
    outTree->SetBranchAddress("max_11",&max_11,&b_max_11);
    outTree->SetBranchAddress("max_12",&max_12,&b_max_12);
    outTree->SetBranchAddress("max_13",&max_13,&b_max_13);
    outTree->SetBranchAddress("max_14",&max_14,&b_max_14);
    outTree->SetBranchAddress("max_15",&max_15,&b_max_15);
    outTree->SetBranchAddress("max_16",&max_16,&b_max_16);
    outTree->SetBranchAddress("max_17",&max_17,&b_max_17);
    outTree->SetBranchAddress("max_18",&max_18,&b_max_18);
    outTree->SetBranchAddress("max_19",&max_19,&b_max_19);
    outTree->SetBranchAddress("max_20",&max_20,&b_max_20);
    outTree->SetBranchAddress("max_21",&max_21,&b_max_21);
    outTree->SetBranchAddress("max_22",&max_22,&b_max_22);
    outTree->SetBranchAddress("max_23",&max_23,&b_max_23);
    outTree->SetBranchAddress("max_24",&max_24,&b_max_24);
    outTree->SetBranchAddress("max_25",&max_25,&b_max_25);
    outTree->SetBranchAddress("max_26",&max_26,&b_max_26);
    outTree->SetBranchAddress("max_27",&max_27,&b_max_27);
    outTree->SetBranchAddress("max_28",&max_28,&b_max_28);
    outTree->SetBranchAddress("max_29",&max_29,&b_max_29);
    outTree->SetBranchAddress("max_30",&max_30,&b_max_30);
    outTree->SetBranchAddress("max_31",&max_31,&b_max_31);


}

void clearOutBranches(){
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
    v_quiet->clear();
    v_presample_mean->clear();
    v_presample_RMS->clear();
    v_groupTDC_b0->clear();
    v_groupTDC_b1->clear();
    v_bx->clear();
    v_by->clear();
    v_bz->clear();


}


void h1cosmetic(TH1D *hist,int ic){
    hist->SetLineWidth(2);
    hist->SetLineColor(colors[ic]);
    hist->SetStats(0);
    hist->GetXaxis()->SetTitleSize(0.045);
    hist->GetXaxis()->SetLabelSize(0.04);
    hist->GetYaxis()->SetTitleSize(0.045);
    hist->GetYaxis()->SetLabelSize(0.04);
    hist->GetYaxis()->SetTitleOffset(1.01);
    hist->GetXaxis()->SetTitleOffset(0.96);

}

void writeVersion(){
    string version = GetStdoutFromCommand("git describe --tags --long");
    cout<<"Git tag is "<<version<<endl;
    TNamed v("tag",version);
    v.Write();

}

void loadBranchesMilliDAQ(){
    inTree->SetBranchAddress("event", &evt);
    for(int ic=0;ic<numChan;ic++) waves.push_back(new TH1D());

}

void loadWavesMilliDAQ(){
    int board,chan;
    for(int i=0;i<numChan;i++){
    	if(waves[i]) delete waves[i];
        //waves[i] = (TH1D*) evt->GetWaveform(i, Form("h%i",i));
        board = i<=15 ? 0 : 1;
        chan = i<=15 ? i : i-16;
        waves[i] = (TH1D*)evt->GetWaveform(board, chan, Form("h%i",i));
    }
}


void loadBranchesInteractiveDAQ(){
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

void getFileCreationTime(const char *path) {
    struct stat attr;
    stat(path, &attr);
    printf("Fill list last updated on %s", ctime(&attr.st_mtime));
}

void loadFillList(TString fillFile){

    int fillnumber, start,end;
    float lumi;
    string date,time;

    getFileCreationTime(fillFile.Data());

    ifstream infile;
    infile.open(fillFile); 

    while(infile >> fillnumber >> start >> end >> lumi >> date >> time){
	if(end<=start && end>0) cout<<"Error in fill time list"<<endl; //end == -1 indicates ongoing fill
	else{
	    //cout<<Form("Appending %i %i %i %0.2f",start,end,fillnumber,lumi)<<endl;
	    fillList.push_back(make_tuple(start,end,fillnumber,lumi));
	}
    }
    sort(fillList.begin(),fillList.end());
    cout<<"First fill "<<get<2>(fillList[0])<<endl;
    cout<<"Last fill "<<get<2>(fillList[fillList.size()-1])<<endl;

}

pair<int,int> findFill(int seconds){
    auto index_of_first_fill_with_larger_start_time = distance(fillList.begin(), lower_bound(fillList.begin(),fillList.end(), 
		make_tuple(seconds, seconds, 0, 0.) ));
    //cout<<"index "<<index_of_first_fill_with_larger_start_time<<endl;
    int this_fill=0;
    int time_since_start=-1;
    if(index_of_first_fill_with_larger_start_time > (int)fillList.size()) this_fill=-1;
    //This event is during a fill if its time is less than the end time of the fill before the first fill with a larger start time
    else if(seconds < get<1>(fillList[index_of_first_fill_with_larger_start_time-1]) || get<1>(fillList[index_of_first_fill_with_larger_start_time-1])==-1){
	//end time == -1 indicates ongoing fill 
	this_fill = get<2>(fillList[index_of_first_fill_with_larger_start_time-1]); //fill number
	time_since_start = seconds - get<0>(fillList[index_of_first_fill_with_larger_start_time-1]); //time of this event - start time of fill
    }
    return make_pair(this_fill,time_since_start);
}


vector<TString> getFieldFileList(TString location){
    vector<TString> files;
    TTimeStamp startOfFile = evt->digitizers[0].DAQTimeStamp;
    int date = startOfFile.GetDate();
    files.push_back(Form("%s/environ_data_%i.txt",location.Data(),date));

    //Also include day after, in case it spans two days.
    startOfFile.Add(86400); //add 24*3600 seconds
    date = startOfFile.GetDate();
    files.push_back(Form("%s/environ_data_%i.txt",location.Data(),date));
    return files;
}

void loadFieldList(TString fieldFile){
    string timestamp;
    int seconds;
    float x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4;
    

    ifstream infile;
    infile.open(fieldFile); 
    if(!infile.good()){
        cout<<"Field file doesn't exist: "<<fieldFile<<endl;
        return;}
    infile.ignore(10000,'\n'); //skip first line
    while(infile >> seconds>> timestamp >> x1>>y1>>z1>>x2>>y2>>z2>>x3>>y3>>z3>>x4>>y4>>z4){
//    if(end<=start && end>0) cout<<"Error in fill time list"<<endl; //end == -1 indicates ongoing fill
        //cout<<Form("Appending %i %i %i %0.2f",start,end,fillnumber,lumi)<<endl;
        fieldList.push_back(make_tuple(seconds,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4));
//        cout<<timestamp<<" "<< x1<<" "<<y1<<" "<<z1<<" "<<x2<<" "<<y2<<" "<<z2<<" "<<x3<<" "<<y3<<" "<<z3<<" "<<x4<<" "<<y4<<" "<<z4<<endl;
    }
    sort(fieldList.begin(),fieldList.end());
    cout<<"Loaded "<<fieldFile<<", "<<fieldList.size()<<" field measurements so far."<<endl;
    // for (int i=0;i<10;i++){
    //     cout<<get<0>(fieldList[i])<<" "<<get<1>(fieldList[i])<<" "<<get<2>(fieldList[i])<<endl;

    // }
}
int findField(int seconds){
    auto index_of_first_point_with_larger_time = distance(fieldList.begin(), lower_bound(fieldList.begin(),fieldList.end(), 
        make_tuple(seconds, 0., 0.,0., 0.,0., 0.,0., 0.,0., 0.,0., 0.) ));
    //cout<<"index "<<index_of_first_fill_with_larger_start_time<<endl;
    int this_point=0;

    if(fabs(seconds-get<0>(fieldList[index_of_first_point_with_larger_time -1])) < fabs(seconds-get<0>(fieldList[index_of_first_point_with_larger_time])))
        this_point = index_of_first_point_with_larger_time -1;
    else
        this_point = index_of_first_point_with_larger_time;

    //Give garbage value if closest point is more than an hour away.
    if(fabs(seconds - get<0>(fieldList[this_point])) > 3600) this_point=-1;

    return this_point;
}

static inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch) {
        return !std::isspace(ch);
    }).base(), s.end());
}
string GetStdoutFromCommand(string cmd) {
    string data;
    FILE * stream;
    const int max_buffer = 256;
    char buffer[max_buffer];
    cmd.append(" 2>&1");

    stream = popen(cmd.c_str(), "r");
    if (stream) {
    while (!feof(stream))
    if (fgets(buffer, max_buffer, stream) != NULL) data.append(buffer);
    pclose(stream);
    }

    //Strip new lines
    rtrim(data);
    return data;
}
