//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Oct  6 22:01:07 2017 by ROOT version 5.34/36
// from TTree t/t
// found on file: UX5MilliQan_Run25.root
//////////////////////////////////////////////////////////

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <iostream>

#define  A_BLACK    ("\033[30m")
#define  A_RED      ("\033[31m")
#define  A_GREEN    ("\033[32m")
#define  A_YELLOW   ("\033[33m")
#define  A_BLUE     ("\033[34m")
#define  A_MAGENTA  ("\033[35m")
#define  A_CYAN     ("\033[36m")
#define  A_WHITE    ("\033[37m")

#define  A_BRIGHT_BLACK    ("\033[1;30m")
#define  A_BRIGHT_RED      ("\033[1;31m")
#define  A_BRIGHT_GREEN    ("\033[1;32m")
#define  A_BRIGHT_YELLOW   ("\033[1;33m")
#define  A_BRIGHT_BLUE     ("\033[1;34m")
#define  A_BRIGHT_MAGENTA  ("\033[1;35m")
#define  A_BRIGHT_CYAN     ("\033[1;36m")
#define  A_BRIGHT_WHITE    ("\033[1;37m")

#define  A_RESET    ("\033[0m")

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   vector<float>   *triggerThreshold;
   vector<bool>    *triggerEnable;
   vector<int>     *triggerMajority;
   vector<int>     *triggerLogic;
   vector<int>     *chan;
   vector<int>     *row;
   vector<int>     *column;
   vector<int>     *layer;
   vector<int>     *type;
   vector<int>     *board;
   vector<float>   *height;
   vector<float>   *area;
   vector<float>   *nPE;
   vector<int>     *ipulse;
   vector<int>     *npulses;
   vector<float>   *ptime;
   vector<float>   *duration;
   vector<float>   *delay;
   vector<float>   *pmax;
   int     *fileNum;
   int     *eventNum;
   //bool    *boardsMatched;

   // List of branches
   TBranch        *b_triggerThreshold;   //!
   TBranch        *b_triggerEnable;   //!
   TBranch        *b_triggerMajority;   //!
   TBranch        *b_triggerLogic;   //!
   TBranch        *b_chan;   //!
   TBranch        *b_row;   //!
   TBranch        *b_column;   //!
   TBranch        *b_layer;   //!
   TBranch        *b_type;   //!
   TBranch        *b_board;   //!
   TBranch        *b_height;   //!
   TBranch        *b_area;   //!
   TBranch        *b_nPE;   //!
   TBranch        *b_ipulse;   //!
   TBranch        *b_npulses;   //!
   TBranch        *b_ptime;   //!
   TBranch        *b_duration;   //!
   TBranch        *b_delay;   //!
   TBranch        *b_pmax;   //!
   TBranch        *b_eventNum;
   TBranch        *b_fileNum;
   //TBranch        *b_boardsMatched;

void InitializeChain(TChain *fChain)
{

   // Set object pointer
   triggerThreshold = 0;
   triggerEnable = 0;
   triggerMajority = 0;
   triggerLogic = 0;
   chan = 0;
   row = 0;
   column = 0;
   layer = 0;
   type = 0;
   board = 0;
   height = 0;
   area = 0;
   nPE = 0;
   ipulse = 0;
   npulses = 0;
   ptime = 0;
   duration = 0;
   delay = 0;
   pmax = 0;

   fChain->SetBranchAddress("triggerThreshold", &triggerThreshold, &b_triggerThreshold);
   fChain->SetBranchAddress("triggerEnable", &triggerEnable, &b_triggerEnable);
   fChain->SetBranchAddress("triggerMajority", &triggerMajority, &b_triggerMajority);
   fChain->SetBranchAddress("triggerLogic", &triggerLogic, &b_triggerLogic);
   fChain->SetBranchAddress("chan", &chan, &b_chan);
   fChain->SetBranchAddress("row", &row, &b_row);
   fChain->SetBranchAddress("column", &column, &b_column);
   fChain->SetBranchAddress("layer", &layer, &b_layer);
   fChain->SetBranchAddress("type", &type, &b_type);
   fChain->SetBranchAddress("board", &board, &b_board);
   fChain->SetBranchAddress("height", &height, &b_height);
   fChain->SetBranchAddress("area", &area, &b_area);
   fChain->SetBranchAddress("nPE", &nPE, &b_nPE);
   fChain->SetBranchAddress("ipulse", &ipulse, &b_ipulse);
   fChain->SetBranchAddress("npulses", &npulses, &b_npulses);
   fChain->SetBranchAddress("time", &ptime, &b_ptime);
   fChain->SetBranchAddress("duration", &duration, &b_duration);
   fChain->SetBranchAddress("delay", &delay, &b_delay);
   fChain->SetBranchAddress("max", &pmax, &b_pmax);
   fChain->SetBranchAddress("event", &eventNum, &b_eventNum);
   fChain->SetBranchAddress("fileNumber", &fileNum, &b_fileNum);
   //fChain->SetBranchAddress("boardsMatched", &boardsMatched, &b_boardsMatched);
}


