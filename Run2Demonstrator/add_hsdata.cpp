#include "treesV19Template.h"
#include <csignal>

struct stat info1;
struct stat info2;


#ifdef __MAKECINT__
#pragma link C++ class std::vector < std::vector<int> >+;
#pragma link C++ class std::vector < std::vector<float> >+;
#endif

using namespace std;


void prepareOutBranches(TTree * & outTree);
void clearOutBranches();
void getHSSyncRange(std::vector<hsData> &hsDataLoaded, std::vector<double> &dt_low, std::vector<double> &dt_high, int ifile, TTree * inTree);
int getHSSyncEvent(std::vector<hsData> &hsDataLoaded, std::vector<double> dt_low, std::vector<double> dt_high, double event_time_fromTDC);
TTree * combine_hs_ntuples(TTree * inTree, int fileNumber);
TTree * splitTree(TTree * tree, int file, int events);  
void add_hsdata(int run);
void signalHandler(int signum);

/* NOTE: if you want to compile uncomment these lines
# ifndef __CINT__  // the following code will be invisible for the interpreter
int main(int charc, char* charv[])
{
	gROOT->ProcessLine(".L add_hsdata.cpp++");
	add_hsdata();
}
# endif
*/

vector<float> corrs = {
	0.9433962264150942, 1.5669515669515668, 1.226505256451099, 
	0.9848484848484849, 1.3709677419354838, 0.8868243243243243, 1.5597147950089127, 0.9211495946941782, 
	1.6983695652173914, 0.8066614623991674, 0.9523809523809523, 0.5, 1.2515644555694618, 
	1.838235294117647,  0.8333333333333333, 1.0,  0.5128205128205129,  0.9986973512809377, 
	1.3333333333333335, 0.4444444444444445, 1.0256410256410255, 0.975609756097561, 
	2.982810920121335, 1.7105263157894732, 0.6263616557734205, 0.8333333333333333, 0.4, 
	0.4444444444444445, 2.1052631578947367, 0.8, 0.3076923076923077, 0.4
};

int maxEvents=-1;
TString year = "2018"; // must be changed for corresponding hs data
TString hs_file_dir= "/data/HSdata/" + year;

void add_hsdata(int runNumber){
	signal(SIGINT, signalHandler); 

	TString runFile = "/data/trees_v19/Run"+to_string(runNumber)+".root";
	TString outFileName = "/data/trees_v19/HS_Run"+to_string(runNumber)+".root";
	TString tmpFilesDir = "/data/trees_v19/Run"+to_string(runNumber)+"/";

    // Get input tree from file
	cout << "Input file: " << runFile << endl;
	cout << "Output file: " << outFileName << endl;
	TFile * f = TFile::Open(runFile, "read");
	if(f == nullptr){return;}

	TTree * inputTree = (TTree*)f->Get("t");
	SetAddresses_nohs(inputTree);

	int inputTreeEvents = inputTree->GetEntries();

	if(inputTreeEvents == 0) inputTreeEvents =inputTree->GetEntries();
	if(inputTreeEvents == 0){
		cerr << "ERROR: No events added" << endl;
		return;
	}
	cout<< "Entries added: " << inputTreeEvents  << endl;

	//how many files in each tree?           //FIXME: load fileNums directly this may be too slow
	// vector<int> files = {};
	// for(int iE=0; iE < maxEvents; iE++){
	// 	inputTree->GetEntry(iE);

	// 	bool duplicate_file = false;
	// 	for(int iFile = 0; iFile < files.size(); iFile++){
	// 		if(fileNum == files[iFile]){
	// 			duplicate_file = true;
	// 		}
	// 	}
	// 	if(!duplicate_file) files.push_back(fileNum);
	// }
	// int n_files = files.size();

	int n_files = 0;
	if(inputTreeEvents % 1000 == 0){ n_files = inputTreeEvents/1000; }
	else{ n_files = (inputTreeEvents/1000)+1; }

	/* loop over files, split input tree based on file
	add hs data for each split tree
	recombine each hs addded tree */

	cout << "Number of files to run over: " << n_files << endl;

	// create temp trees directory
	gSystem->Exec("mkdir "+tmpFilesDir);

	for(int iFile = 1; iFile < n_files + 1 ; iFile++){
		// if(iFile > 3){ continue;} // testing 

		cout << "\nWorking on file: " << iFile << endl;
		TFile * tmp_tree_file = new TFile(tmpFilesDir+"HS_tree"+toTstring(to_string(iFile))+".root", "recreate");
		
		TTree * temp_tree = splitTree(inputTree, iFile, inputTreeEvents);
		maxEvents = temp_tree->GetEntries();

		TTree * temp_tree_hsadded = combine_hs_ntuples(temp_tree, iFile);
		temp_tree_hsadded->SetName("t");

		tmp_tree_file->cd();
		temp_tree_hsadded->Write();
		tmp_tree_file->Close();

		delete tmp_tree_file;
	}


	cout << "\nMerging trees..." << endl;
	TChain * finalChain = new TChain("t");
	finalChain->Add(tmpFilesDir+"*.root");
	SetAddresses(finalChain);
	finalChain->Merge(outFileName);

	// remove tmp files
	gSystem->Exec("rm "+tmpFilesDir+"*.root");

	delete finalChain;
}


TTree * combine_hs_ntuples(TTree * inTree, int fileNumber){

	TTree * outTree = inTree->CloneTree(0);
	prepareOutBranches(outTree);
	SetAddresses(outTree);


	std::vector<hsData> hsDataLoaded;
	std::vector<double> dt_low;
	std::vector<double> dt_high;
	getHSSyncRange(hsDataLoaded,dt_low,dt_high,fileNumber,inTree);

	for(auto c: corrs){
		v_nPECorr->push_back(c);
	}

	cout << " Combining tuple event:";
	for(int i=0; i<maxEvents; i++){

		if(i%(maxEvents/5)==0) cout << i << std::flush;
		inTree->GetEntry(i);

		int sync_hs_event_index = getHSSyncEvent(hsDataLoaded,dt_low,dt_high,event_time_fromTDC);

		if (sync_hs_event_index>0){

			for(unsigned int j=0; j<hsDataLoaded.at(sync_hs_event_index).getHSData().size(); j++){
				if(hsDataLoaded.at(sync_hs_event_index).getHSData().at(j)==1){
					// cout << std::flush << "j: " << j << endl;
					v_hs->push_back(j);
				}
			}

			for(unsigned int j=0; j<hsDataLoaded.at(sync_hs_event_index).getTPData().size(); j++){
				if(hsDataLoaded.at(sync_hs_event_index).getTPData().at(j)==1){
					v_tp->push_back(j);
				}
			}
			
			hs_time = hsDataLoaded.at(sync_hs_event_index).getMicroTime();
			extrg   = hsDataLoaded.at(sync_hs_event_index).isMQEvent();
		}
		else{
			extrg   =  0;
			hs_time = -1;
			v_hs->push_back(-1);
			v_tp->push_back(-1);
		}

		if (sync_hs_event_index>0){
			// Tracking
			// get fit parameter
			vector<double> parFit = doFit(v_hs);

			if(parFit.size()>0){
				//cout << parFit[0] << " " << parFit[1] << endl;
				//cout << parFit[2] << " " << parFit[3] << endl;

				v_fit_xz->push_back(parFit[0]);
				v_fit_xz->push_back(parFit[1]);
				v_fit_yz->push_back(parFit[2]);
				v_fit_yz->push_back(parFit[3]);
			}
			parFit.clear();
		}
		outTree->Fill();
		clearOutBranches();
		ClearVectors();

		fillNum=0;
		beam=false;
		hardNoBeam=false;
		fillAvgLumi=-1;
		fillTotalLumi=-1;
	} // end event for loop

	hsDataLoaded.clear();
	dt_low.clear();
	dt_high.clear();

	return outTree;
}



void prepareOutBranches(TTree * & outTree){

	TBranch * b_extrg   = outTree->Branch("extrg",&extrg,"extrg/I");
	TBranch * b_hs_time = outTree->Branch("hs_time",&hs_time,"hs_time/D");
	TBranch * b_v_hs      = outTree->Branch("hs",&v_hs);
	TBranch * b_v_tp      = outTree->Branch("tp",&v_tp);
	TBranch * b_v_fit_xz  = outTree->Branch("fit_xz",&v_fit_xz);
	TBranch * b_v_fit_yz  = outTree->Branch("fit_yz",&v_fit_yz);

	TBranch * b_v_nPECorr = outTree->Branch("nPECorr", &v_nPECorr);

	outTree->SetBranchAddress("extrg",    &extrg,     &b_extrg);
	outTree->SetBranchAddress("hs_time",  &hs_time,   &b_hs_time);
	outTree->SetBranchAddress("hs",     &v_hs,      &b_v_hs);
	outTree->SetBranchAddress("tp",     &v_tp,      &b_v_tp);
	outTree->SetBranchAddress("fit_xz", &v_fit_xz,  &b_v_fit_xz);
	outTree->SetBranchAddress("fit_yz", &v_fit_yz,  &b_v_fit_yz); 

	outTree->SetBranchAddress("nPECorr", &v_nPECorr, &b_v_nPECorr);  
}


void clearOutBranches(){
	v_hs->clear();
	v_tp->clear();
	v_fit_xz->clear();
	v_fit_yz->clear();
}



void getHSSyncRange(std::vector<hsData> &hsDataLoaded, std::vector<double> &dt_low, 
					std::vector<double> &dt_high, int ifile, TTree* inTree) {
	// get mq time stamp in the mq first event
	double event_time_fromTDC_evt0 = -1;

	// int nEntries = inTree->GetEntries();

	for(int i=0; i < maxEvents; i++){
		inTree->GetEntry(i);
		if(event==0){
			event_time_fromTDC_evt0 = event_time_fromTDC;
		}
	}


	// ------------------------------------------------------------------------------------
	//  Find HS files to look at
	// ------------------------------------------------------------------------------------
	// 1 hour before

	time_t epoch_previous_file = static_cast<int>(event_time_fromTDC_evt0-3600);

	struct tm *date_previous_file = gmtime(&epoch_previous_file);
	TString hs_previous_file = Form("data_%d%02d%02d%02d.txt", date_previous_file->tm_year+1900, date_previous_file->tm_mon+1, date_previous_file->tm_mday,   date_previous_file->tm_hour);

	// 1 hour after
	time_t epoch_next_file = static_cast<int>(event_time_fromTDC_evt0+3600);
	struct tm *date_next_file = gmtime(&epoch_next_file);
	TString hs_next_file = Form("data_%d%02d%02d%02d.txt", date_next_file->tm_year+1900, date_next_file->tm_mon+1, date_next_file->tm_mday, date_next_file->tm_hour);

	// current
	time_t epoch = static_cast<int>(event_time_fromTDC_evt0);
	struct tm *date = gmtime(&epoch);
	TString hs_current_file = Form("data_%d%02d%02d%02d.txt", date->tm_year+1900, date->tm_mon+1, date->tm_mday, date->tm_hour);

	// std::cout << "HS files in consideration: " << std::endl;
	// std::cout << hs_previous_file << std::endl;
	// std::cout << hs_current_file << std::endl;
	// std::cout << hs_next_file << std::endl;

	// std::cout <<  Form("Time: %d%02d%02d %02d:%02d:%02d", date->tm_year+1900, date->tm_mon+1, date->tm_mday, date->tm_hour, date->tm_min, date->tm_sec) <<    std::endl;
	// ------------------------------------------------------------------------------------
	//  Store HS data in memory
	// ------------------------------------------------------------------------------------

	// 1. if near boundary then look at two adjacent files
	if(date->tm_min<3 && ifile>1) {
		loadHSData(hs_file_dir, hs_previous_file, hsDataLoaded, -1);
	}

	// 2. load events in the main file
	loadHSData(hs_file_dir, hs_current_file, hsDataLoaded, 0);

	// 3. if the end time is in the next file, add events to memory
	if(date->tm_min>57) {
		loadHSData(hs_file_dir, hs_next_file, hsDataLoaded, 1);
	}

	std::cout << "Number of loaded HS events: " << hsDataLoaded.size() << std::endl;

	// make a histogram of delta(hs time, mq time)
	TH1D *h1_dt  = new TH1D("h1_dt", "h1_dt", 100000, -10, 10);
	double mq_current_time=event_time_fromTDC_evt0;
	double mq_previous_time=event_time_fromTDC_evt0;
	cout << "Synching HS evt:" << std::flush; 

	for(int i=0; i<maxEvents; i++) {
		inTree->GetEntry(i);
		if(i% (maxEvents/5) == 0) cout << i << std::flush; 
		
		mq_current_time = event_time_fromTDC;

		// Loop over selected HS events
		double hs_current_time=0;
		double hs_previous_time=0;
		for(unsigned int ihs=0; ihs<hsDataLoaded.size(); ihs++){
			// only extrg events
			//if(!hsDataLoaded.at(ihs).isMQEvent()) continue;

			hs_current_time = hsDataLoaded.at(ihs).getMicroTime();
			// cout << std::fixed;

			double dt_of_dt = (mq_current_time-mq_previous_time) - (hs_current_time-hs_previous_time);
			dt_of_dt = 0; // not using dt_of_dt in the syncing decision
			if(TMath::Abs(dt_of_dt)<0.00001) h1_dt->Fill(mq_current_time-hs_current_time);

			hs_previous_time = hs_current_time;
		}

		mq_previous_time = mq_current_time;

	}

	// extract dT ranges
	for(int i=1; i<=h1_dt->GetXaxis()->GetNbins(); i++){

		if(h1_dt->GetBinContent(i)>100){

			double range_low = h1_dt->GetBinLowEdge(i-2);
			double range_high = h1_dt->GetBinLowEdge(i+2);
			// std::cout << "dT synch range: " << range_low << " - " << range_high << std::endl;
			dt_low.push_back(range_low);
			dt_high.push_back(range_high);
		}
	}

	delete h1_dt;
}


int getHSSyncEvent(std::vector<hsData> &hsDataLoaded, std::vector<double> dt_low, std::vector<double> dt_high, double event_time_fromTDC) {

	double mq_current_time = event_time_fromTDC;

	// Get the window of HS events to compare
	//double hs_begin_time = hsDataLoaded.at(0).getMicroTime();
	//double hs_end_time = hsDataLoaded.at(hsDataLoaded.size()-1).getMicroTime();
	//double hs_total_time = hs_end_time-hs_begin_time;

	//int sync_window_sec = 30;

	// get the indices for synching window
	//int first_hs_evt = hsDataLoaded.size() * (mq_current_time-sync_window_sec-hs_begin_time)/hs_total_time;
	//int last_hs_evt  = hsDataLoaded.size() * (mq_current_time+sync_window_sec-hs_begin_time)/hs_total_time;

	int synched=-1;
	// Loop over selected HS events
	double hs_current_time=0;
	//for(int ihs=first_hs_evt; ihs<=last_hs_evt; ++ihs)
	for(unsigned int ihs=0; ihs<hsDataLoaded.size(); ++ihs)
	{
		hs_current_time = hsDataLoaded.at(ihs).getMicroTime();

		for(unsigned int irange=0; irange<dt_low.size(); irange++)
		{
			//cout << dt_low.at(irange) << " " << dt_high.at(irange) << " " << mq_current_time-hs_current_time << endl;
			if( mq_current_time-hs_current_time>dt_low.at(irange) &&
				mq_current_time-hs_current_time<dt_high.at(irange)
				) synched = ihs;
		}
		if(synched>0)
		{
			break;
		}
	}

	return synched;
}

//create a tree with events from one fileNum
//useful for loading matching HS data file
TTree * splitTree(TTree* tree, int file, int events){

	TTree * tsplit = tree->CloneTree(0);

	for(int iE = 0; iE<events ;iE++){
		tree->GetEntry(iE);
		if(fileNum == file){
			tsplit->Fill();
		}
	}

	return tsplit;
}


void signalHandler( int signum ) {
   cout << "Interrupt signal (" << signum << ") received.\n";
   exit(signum);  
}