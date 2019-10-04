//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Oct  2 10:33:12 2019 by ROOT version 6.06/01
// from TTree SimTree/
// found on file: exampleInjectionInput.root
//////////////////////////////////////////////////////////

#ifndef SimTree_h
#define SimTree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class SimTree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           fileID;
   Float_t         mu_initE;
   Int_t           chan_nPE[32];
   Float_t         chan_fracMuon[32];
   Float_t         chan_fracElScint[32];
   Float_t         chan_fracElAl[32];
   Float_t         chan_fracElRock[32];
   Float_t         chan_fracElPb[32];
   Float_t         chan_fracOther[32];
   Float_t         chan_firstTime[32];
   Float_t         chan_meanTime[32];
   Float_t         chan_timeCalib[32];
   Float_t         chan_muDist[32];
   Float_t         chan_muTime[32];
   Int_t           chan_type[32];
   Int_t           mcTruth_nMuSlabHits;
   Int_t           mcTruth_nMuPanelHits;
   Int_t           mcTruth_nMuBarHits;
   Bool_t          mcTruth_fourSlab;
   Bool_t          mcTruth_threeBarLine;
   Bool_t          mcTruth_noBar;
   Bool_t          mcTruth_noChan;
   Int_t           mcTruth_verticalCosmic;
   Float_t         chan0_PEtimes[100];
   Float_t         chan1_PEtimes[100];
   Float_t         chan2_PEtimes[100];
   Float_t         chan3_PEtimes[100];
   Float_t         chan4_PEtimes[100];
   Float_t         chan5_PEtimes[100];
   Float_t         chan6_PEtimes[100];
   Float_t         chan7_PEtimes[100];
   Float_t         chan8_PEtimes[100];
   Float_t         chan9_PEtimes[100];
   Float_t         chan10_PEtimes[100];
   Float_t         chan11_PEtimes[100];
   Float_t         chan12_PEtimes[100];
   Float_t         chan13_PEtimes[100];
   Float_t         chan14_PEtimes[100];
   Float_t         chan15_PEtimes[100];
   Float_t         chan16_PEtimes[100];
   Float_t         chan17_PEtimes[100];
   Float_t         chan18_PEtimes[100];
   Float_t         chan19_PEtimes[100];
   Float_t         chan20_PEtimes[100];
   Float_t         chan21_PEtimes[100];
   Float_t         chan22_PEtimes[100];
   Float_t         chan23_PEtimes[100];
   Float_t         chan24_PEtimes[100];
   Float_t         chan25_PEtimes[100];
   Float_t         chan26_PEtimes[100];
   Float_t         chan27_PEtimes[100];
   Float_t         chan28_PEtimes[100];
   Float_t         chan29_PEtimes[100];
   Float_t         chan30_PEtimes[100];
   Float_t         chan31_PEtimes[100];

   // List of branches
   TBranch        *b_fileID;   //!
   TBranch        *b_mu_initE;   //!
   TBranch        *b_chan_nPE;   //!
   TBranch        *b_chan_fracMuon;   //!
   TBranch        *b_chan_fracElScint;   //!
   TBranch        *b_chan_fracElAl;   //!
   TBranch        *b_chan_fracElRock;   //!
   TBranch        *b_chan_fracElPb;   //!
   TBranch        *b_chan_fracOther;   //!
   TBranch        *b_chan_firstTime;   //!
   TBranch        *b_chan_meanTime;   //!
   TBranch        *b_chan_timeCalib;   //!
   TBranch        *b_chan_muDist;   //!
   TBranch        *b_chan_muTime;   //!
   TBranch        *b_chan_type;   //!
   TBranch        *b_mcTruth_nMuSlabHits;   //!
   TBranch        *b_mcTruth_nMuPanelHits;   //!
   TBranch        *b_mcTruth_nMuBarHits;   //!
   TBranch        *b_mcTruth_fourSlab;   //!
   TBranch        *b_mcTruth_threeBarLine;   //!
   TBranch        *b_mcTruth_noBar;   //!
   TBranch        *b_mcTruth_noChan;   //!
   TBranch        *b_mcTruth_verticalCosmic;   //!
   TBranch        *b_chan0_PEtimes;   //!
   TBranch        *b_chan1_PEtimes;   //!
   TBranch        *b_chan2_PEtimes;   //!
   TBranch        *b_chan3_PEtimes;   //!
   TBranch        *b_chan4_PEtimes;   //!
   TBranch        *b_chan5_PEtimes;   //!
   TBranch        *b_chan6_PEtimes;   //!
   TBranch        *b_chan7_PEtimes;   //!
   TBranch        *b_chan8_PEtimes;   //!
   TBranch        *b_chan9_PEtimes;   //!
   TBranch        *b_chan10_PEtimes;   //!
   TBranch        *b_chan11_PEtimes;   //!
   TBranch        *b_chan12_PEtimes;   //!
   TBranch        *b_chan13_PEtimes;   //!
   TBranch        *b_chan14_PEtimes;   //!
   TBranch        *b_chan15_PEtimes;   //!
   TBranch        *b_chan16_PEtimes;   //!
   TBranch        *b_chan17_PEtimes;   //!
   TBranch        *b_chan18_PEtimes;   //!
   TBranch        *b_chan19_PEtimes;   //!
   TBranch        *b_chan20_PEtimes;   //!
   TBranch        *b_chan21_PEtimes;   //!
   TBranch        *b_chan22_PEtimes;   //!
   TBranch        *b_chan23_PEtimes;   //!
   TBranch        *b_chan24_PEtimes;   //!
   TBranch        *b_chan25_PEtimes;   //!
   TBranch        *b_chan26_PEtimes;   //!
   TBranch        *b_chan27_PEtimes;   //!
   TBranch        *b_chan28_PEtimes;   //!
   TBranch        *b_chan29_PEtimes;   //!
   TBranch        *b_chan30_PEtimes;   //!
   TBranch        *b_chan31_PEtimes;   //!

   SimTree(TTree *tree=0);
   virtual ~SimTree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef SimTree_cxx
SimTree::SimTree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("exampleInjectionInput.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("exampleInjectionInput.root");
      }
      f->GetObject("Events",tree);

   }
   Init(tree);
}

SimTree::~SimTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t SimTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t SimTree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void SimTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("fileID", &fileID, &b_fileID);
   fChain->SetBranchAddress("mu_initE", &mu_initE, &b_mu_initE);
   fChain->SetBranchAddress("chan_nPE", chan_nPE, &b_chan_nPE);
   fChain->SetBranchAddress("chan_fracMuon", chan_fracMuon, &b_chan_fracMuon);
   fChain->SetBranchAddress("chan_fracElScint", chan_fracElScint, &b_chan_fracElScint);
   fChain->SetBranchAddress("chan_fracElAl", chan_fracElAl, &b_chan_fracElAl);
   fChain->SetBranchAddress("chan_fracElRock", chan_fracElRock, &b_chan_fracElRock);
   fChain->SetBranchAddress("chan_fracElPb", chan_fracElPb, &b_chan_fracElPb);
   fChain->SetBranchAddress("chan_fracOther", chan_fracOther, &b_chan_fracOther);
   fChain->SetBranchAddress("chan_firstTime", chan_firstTime, &b_chan_firstTime);
   fChain->SetBranchAddress("chan_meanTime", chan_meanTime, &b_chan_meanTime);
   fChain->SetBranchAddress("chan_timeCalib", chan_timeCalib, &b_chan_timeCalib);
   fChain->SetBranchAddress("chan_muDist", chan_muDist, &b_chan_muDist);
   fChain->SetBranchAddress("chan_muTime", chan_muTime, &b_chan_muTime);
   fChain->SetBranchAddress("chan_type", chan_type, &b_chan_type);
   fChain->SetBranchAddress("mcTruth_nMuSlabHits", &mcTruth_nMuSlabHits, &b_mcTruth_nMuSlabHits);
   fChain->SetBranchAddress("mcTruth_nMuPanelHits", &mcTruth_nMuPanelHits, &b_mcTruth_nMuPanelHits);
   fChain->SetBranchAddress("mcTruth_nMuBarHits", &mcTruth_nMuBarHits, &b_mcTruth_nMuBarHits);
   fChain->SetBranchAddress("mcTruth_fourSlab", &mcTruth_fourSlab, &b_mcTruth_fourSlab);
   fChain->SetBranchAddress("mcTruth_threeBarLine", &mcTruth_threeBarLine, &b_mcTruth_threeBarLine);
   fChain->SetBranchAddress("mcTruth_noBar", &mcTruth_noBar, &b_mcTruth_noBar);
   fChain->SetBranchAddress("mcTruth_noChan", &mcTruth_noChan, &b_mcTruth_noChan);
   fChain->SetBranchAddress("mcTruth_verticalCosmic", &mcTruth_verticalCosmic, &b_mcTruth_verticalCosmic);
   fChain->SetBranchAddress("chan0_PEtimes", chan0_PEtimes, &b_chan0_PEtimes);
   fChain->SetBranchAddress("chan1_PEtimes", chan1_PEtimes, &b_chan1_PEtimes);
   fChain->SetBranchAddress("chan2_PEtimes", chan2_PEtimes, &b_chan2_PEtimes);
   fChain->SetBranchAddress("chan3_PEtimes", chan3_PEtimes, &b_chan3_PEtimes);
   fChain->SetBranchAddress("chan4_PEtimes", chan4_PEtimes, &b_chan4_PEtimes);
   fChain->SetBranchAddress("chan5_PEtimes", chan5_PEtimes, &b_chan5_PEtimes);
   fChain->SetBranchAddress("chan6_PEtimes", chan6_PEtimes, &b_chan6_PEtimes);
   fChain->SetBranchAddress("chan7_PEtimes", chan7_PEtimes, &b_chan7_PEtimes);
   fChain->SetBranchAddress("chan8_PEtimes", chan8_PEtimes, &b_chan8_PEtimes);
   fChain->SetBranchAddress("chan9_PEtimes", chan9_PEtimes, &b_chan9_PEtimes);
   fChain->SetBranchAddress("chan10_PEtimes", chan10_PEtimes, &b_chan10_PEtimes);
   fChain->SetBranchAddress("chan11_PEtimes", chan11_PEtimes, &b_chan11_PEtimes);
   fChain->SetBranchAddress("chan12_PEtimes", chan12_PEtimes, &b_chan12_PEtimes);
   fChain->SetBranchAddress("chan13_PEtimes", chan13_PEtimes, &b_chan13_PEtimes);
   fChain->SetBranchAddress("chan14_PEtimes", chan14_PEtimes, &b_chan14_PEtimes);
   fChain->SetBranchAddress("chan15_PEtimes", chan15_PEtimes, &b_chan15_PEtimes);
   fChain->SetBranchAddress("chan16_PEtimes", chan16_PEtimes, &b_chan16_PEtimes);
   fChain->SetBranchAddress("chan17_PEtimes", chan17_PEtimes, &b_chan17_PEtimes);
   fChain->SetBranchAddress("chan18_PEtimes", chan18_PEtimes, &b_chan18_PEtimes);
   fChain->SetBranchAddress("chan19_PEtimes", chan19_PEtimes, &b_chan19_PEtimes);
   fChain->SetBranchAddress("chan20_PEtimes", chan20_PEtimes, &b_chan20_PEtimes);
   fChain->SetBranchAddress("chan21_PEtimes", chan21_PEtimes, &b_chan21_PEtimes);
   fChain->SetBranchAddress("chan22_PEtimes", chan22_PEtimes, &b_chan22_PEtimes);
   fChain->SetBranchAddress("chan23_PEtimes", chan23_PEtimes, &b_chan23_PEtimes);
   fChain->SetBranchAddress("chan24_PEtimes", chan24_PEtimes, &b_chan24_PEtimes);
   fChain->SetBranchAddress("chan25_PEtimes", chan25_PEtimes, &b_chan25_PEtimes);
   fChain->SetBranchAddress("chan26_PEtimes", chan26_PEtimes, &b_chan26_PEtimes);
   fChain->SetBranchAddress("chan27_PEtimes", chan27_PEtimes, &b_chan27_PEtimes);
   fChain->SetBranchAddress("chan28_PEtimes", chan28_PEtimes, &b_chan28_PEtimes);
   fChain->SetBranchAddress("chan29_PEtimes", chan29_PEtimes, &b_chan29_PEtimes);
   fChain->SetBranchAddress("chan30_PEtimes", chan30_PEtimes, &b_chan30_PEtimes);
   fChain->SetBranchAddress("chan31_PEtimes", chan31_PEtimes, &b_chan31_PEtimes);
   Notify();
}

Bool_t SimTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void SimTree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t SimTree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef SimTree_cxx
