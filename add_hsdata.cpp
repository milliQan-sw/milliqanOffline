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
void getHSSyncRange(std::vector<hsData> &hsDataLoaded, std::vector<double> &dt_low, std::vector<double> &dt_high, int ifile, TTree * inTree, TString hs_file_dir);
int getHSSyncEvent(std::vector<hsData> &hsDataLoaded, std::vector<double> dt_low, std::vector<double> dt_high, double event_time_fromTDC);
void add_hsdata(TString inputFile, int runNumber, int fileNumber);
void signalHandler(int signum);

vector<double> nPE_corrs_data = {
	1.3888888888888888, 1.111111111111111, 1.226505256451099, 0.937950937950938, 1.1424731182795698, 1.207590569292697, 1.3544891640866874, 1.0254306808859721, 1.646903820816864, 0.8915731952832903,  0.9523809523809523,  0.5,  1.1312217194570136,  1.524390243902439,  0.8333333333333333,  20.0,  0.7444168734491315,  1.0411951109099138,  1.3333333333333335,  0.4444444444444445,  1.0256410256410255,  0.975609756097561,  3.610771113831089,  1.7105263157894732,  1.0249554367201426,  0.7619047619047619,  0.4,  0.4444444444444445,  2.1052631578947367,  0.8,  0.3076923076923077,  0.4
};

int maxEvents=-1;

void add_hsdata(TString inputFile, TString outFileName, int runNumber, int fileNumber, TString hs_file_dir){

	TFile * f = TFile::Open(inputFile, "read");

	if(f == nullptr){ return; }

	TTree * inTree = (TTree*)f->Get("t");
	SetAddresses_nohs(inTree);
	maxEvents = inTree->GetEntries();

	TFile * fOut = TFile::Open(outFileName, "recreate");
	TTree * outTree = inTree->CloneTree(0);
	prepareOutBranches(outTree);
	SetAddresses(outTree);

	std::vector<hsData> hsDataLoaded;
	std::vector<double> dt_low;
	std::vector<double> dt_high;

	getHSSyncRange(hsDataLoaded,dt_low,dt_high,fileNumber,inTree, hs_file_dir);

	for(auto c: nPE_corrs_data){ v_nPECorr->push_back(c); }

	cout << " Combining tuple event:"; 
	for(int i=0; i<maxEvents; i++){

		if(i%(maxEvents/5)==0) cout << i << std::flush;
		inTree->GetEntry(i);

		int sync_hs_event_index = getHSSyncEvent(hsDataLoaded,dt_low,dt_high,event_time_fromTDC);

		if (sync_hs_event_index>0){

			for(unsigned int j=0; j<hsDataLoaded.at(sync_hs_event_index).getHSData().size(); j++){
				if(hsDataLoaded.at(sync_hs_event_index).getHSData().at(j)==1){
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

		outTree->Fill();
		clearOutBranches();
		ClearVectors();

		fillNum=0;
		beam=false;
		hardNoBeam=false;
		fillAvgLumi=-1;
		fillTotalLumi=-1;
	} // end event for loop

	fOut->cd();
	outTree->Write();
	fOut->Close();

	hsDataLoaded.clear();
	dt_low.clear();
	dt_high.clear();
}



void prepareOutBranches(TTree * & outTree){

	TBranch * b_extrg   = outTree->Branch("extrg",&extrg,"extrg/I");
	TBranch * b_hs_time = outTree->Branch("hs_time",&hs_time,"hs_time/D");
	TBranch * b_v_hs      = outTree->Branch("hs",&v_hs);
	TBranch * b_v_tp      = outTree->Branch("tp",&v_tp);
	TBranch * b_v_nPECorr = outTree->Branch("nPECorr", &v_nPECorr);

	outTree->SetBranchAddress("extrg",    &extrg,     &b_extrg);
	outTree->SetBranchAddress("hs_time",  &hs_time,   &b_hs_time);
	outTree->SetBranchAddress("hs",     &v_hs,      &b_v_hs);
	outTree->SetBranchAddress("tp",     &v_tp,      &b_v_tp);
	outTree->SetBranchAddress("nPECorr", &v_nPECorr, &b_v_nPECorr);  
}


void clearOutBranches(){
	v_hs->clear();
	v_tp->clear();
}



void getHSSyncRange(std::vector<hsData> &hsDataLoaded, std::vector<double> &dt_low, 
					std::vector<double> &dt_high, int ifile, TTree* inTree, TString hs_file_dir){

	// get mq time stamp in the mq first event
	double event_time_fromTDC_evt0 = -1;

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

	// 1. if near boundary then look at two adjacent file
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


void signalHandler( int signum ) {
   cout << "Interrupt signal (" << signum << ") received.\n";
   exit(signum);  
}