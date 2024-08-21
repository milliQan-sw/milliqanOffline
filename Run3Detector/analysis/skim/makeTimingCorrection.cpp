#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include <string>

using namespace std;

int makeTimingCorrection(){

    TString filename = "MilliQan_Run1500_v34_skim.root";

    TFile* fin = TFile::Open(filename, "read");

    TTree* mytree = (TTree*)fin->Get("t");

    TFile* fout = TFile::Open("MilliQan_Run1500_v34_skim_correction.root", "RECREATE");
    TTree* new_tree = mytree->CloneTree(0);  //Create an empty clone of the original tree

    int nentries = mytree->GetEntries();

    std::cout << "There are  " << nentries << " in my file" << std::endl;

    vector<Long64_t> *v_groupTDC_g0 = nullptr;
    vector<Long64_t> *v_groupTDC_g1 = nullptr;
    vector<Long64_t> *v_groupTDC_g2 = nullptr;
    vector<Long64_t> *v_groupTDC_g3 = nullptr;
    vector<Long64_t> *v_groupTDC_g4 = nullptr;
    vector<Long64_t> *v_groupTDC_g5 = nullptr;
    vector<Long64_t> *v_groupTDC_g6 = nullptr;
    vector<Long64_t> *v_groupTDC_g7 = nullptr;
    vector<float>   *time_module_calibrated = nullptr;
    vector<float>   *timeFit_module_calibrated = nullptr;
    vector<int> *board = nullptr;

    TBranch        *b_time_module_calibrated = nullptr;   //!
    TBranch        *b_timeFit_module_calibrated = nullptr;
    TBranch        *b_v_groupTDC_g0 = nullptr;   //!
    TBranch        *b_v_groupTDC_g1 = nullptr;   //!
    TBranch        *b_v_groupTDC_g2 = nullptr;   //!
    TBranch        *b_v_groupTDC_g3 = nullptr;   //!
    TBranch        *b_v_groupTDC_g4 = nullptr;   //!
    TBranch        *b_v_groupTDC_g5 = nullptr;   //!
    TBranch        *b_v_groupTDC_g6 = nullptr;   //!
    TBranch        *b_v_groupTDC_g7 = nullptr;   //!
    TBranch        *b_board = nullptr;

    mytree->SetBranchAddress("time_module_calibrated", &time_module_calibrated, &b_time_module_calibrated);
    mytree->SetBranchAddress("timeFit_module_calibrated", &timeFit_module_calibrated, &b_timeFit_module_calibrated);
    mytree->SetBranchAddress("v_groupTDC_g0", &v_groupTDC_g0, &b_v_groupTDC_g0);
    mytree->SetBranchAddress("v_groupTDC_g1", &v_groupTDC_g1, &b_v_groupTDC_g1);
    mytree->SetBranchAddress("v_groupTDC_g2", &v_groupTDC_g2, &b_v_groupTDC_g2);
    mytree->SetBranchAddress("v_groupTDC_g3", &v_groupTDC_g3, &b_v_groupTDC_g3);
    mytree->SetBranchAddress("v_groupTDC_g4", &v_groupTDC_g4, &b_v_groupTDC_g4);
    mytree->SetBranchAddress("v_groupTDC_g5", &v_groupTDC_g5, &b_v_groupTDC_g5);
    mytree->SetBranchAddress("v_groupTDC_g6", &v_groupTDC_g6, &b_v_groupTDC_g6);
    mytree->SetBranchAddress("v_groupTDC_g7", &v_groupTDC_g7, &b_v_groupTDC_g7);
    mytree->SetBranchAddress("board", &board, &b_board);


    vector<float> timeFit_module_calibrated_mod;
    timeFit_module_calibrated_mod.resize(timeFit_module_calibrated->size());

    //std::vector<float>* new_timeFit_module_calibrated_mod = &timeFit_module_calibrated_mod;
    //TBranch* newBranch = new_tree->Branch("timeFit_module_calibrated_corrected", &new_timeFit_module_calibrated_mod);
    TBranch* newBranch = new_tree->Branch("timeFit_module_calibrated_corrected", &timeFit_module_calibrated_mod);

    for (int ientry=0; ientry < nentries; ientry++){

        mytree->GetEntry(ientry);

        //std::copy(timeFit_module_calibrated->begin(), timeFit_module_calibrated->end(), timeFit_module_calibrated_mod.begin());
        timeFit_module_calibrated_mod = *timeFit_module_calibrated;

        //std::cout << "Entry: " << ientry << ", time fit: " << timeFit_module_calibrated->at(0) << 
        //    " Number of pulses: " << timeFit_module_calibrated->size() << 
        //    " group TDC: " << v_groupTDC_g0->at(0) << " group TDC: " << v_groupTDC_g0->at(1) << std::endl;
            
        /*bool boardsMatched = true;
        float correction = 0.0;
        for (int board=1; board < 5; board++){
            //std::cout << "board: " << board << ", time: " << v_groupTDC_g0->at(1) << std::endl;
            if (v_groupTDC_g0->at(board) != v_groupTDC_g0->at(0)){
                boardsMatched=false;
                correction = 5*(v_groupTDC_g0->at(board) - v_groupTDC_g0->at(0));
            }
        }*/

        //if (!boardsMatched){
            //std::cout << "boards not matched, event: " << ientry << std::endl;
        for(int ipulse=0; ipulse < timeFit_module_calibrated->size(); ipulse++){
            auto ib = board->at(ipulse);
            float correction = 0.0;
            if (v_groupTDC_g0->at(ib) != v_groupTDC_g0->at(0)) correction = 5*(v_groupTDC_g0->at(ib) - v_groupTDC_g0->at(0));
            float newTime = timeFit_module_calibrated->at(ipulse) + correction;
            //std::cout << "boards not matched, event: " << ientry << ", old time: " << timeFit_module_calibrated->at(ipulse) << ", new time: " << newTime << std::endl;
            timeFit_module_calibrated_mod[ipulse] = newTime;
        }
        //}

        new_tree->Fill();
    }

    fout->cd();
    new_tree->Write();
    //fout->Close();
    //fin->Close();

    return 0;
}
