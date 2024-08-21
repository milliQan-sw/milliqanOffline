//#include "myLooper.h"  
//#include "TChain.h"
//#include <fstream>


{
  TString sRun, outFile, inFile;
  TString inDir  = "/net/cms18/cms18r0/claudio/v34_hadd/";
  TString outDir = "/net/cms18/cms18r0/claudio/skim/v34/";
  TString inName = "MilliQan_RunXXXX_all.root";

  for (int i=1000; i< 1131; i++) {

    inFile = inDir + inName;
    sRun.Form("%d", i);
    inFile.ReplaceAll("XXXX",sRun);
    outFile = inFile;
    outFile.ReplaceAll(inDir,outDir);
    outFile.ReplaceAll("all","skimmed");

    // Check if the input file exists.  (Yes, it seems backwards...)
    if (gSystem->AccessPathName(inFile)) {
      std::cout << inFile << " does not exist" << std::endl;
      continue;
    }

    std::cout << "Input:  " << inFile << std::endl;
    std::cout << "Output: " << outFile << std::endl;
 
  // gROOT->ProcessLine(".L myLooper.C+");
  //TString inFile  = "/net/cms26/cms26r0/claudio/v34_hadd/MilliQan_Run1200_all.root";
  //TString outFile = "outfile.root";

    TChain *ch = new TChain("t");

    std::ofstream outputTextFile("skim_results.txt", std::ios::app);
    outputTextFile << inFile << endl;
    outputTextFile.close();

    ch->Add(inFile);
    myLooper t(ch);
    t.Loop(outFile);
  }
}

