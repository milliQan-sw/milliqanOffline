#include <iostream>
#include "TTree.h"
#include "TFile.h"
#include "TBranch.h"

int main(){
  const char* data_directory = "/home/ryan/Documents/Data/MilliQan/";
  TFile* input_file = TFile::Open(data_directory + "Run805preProcessed.root");
  TTree* tree = dynamic_cast<TTree*>(input_file->Get("Events"));



  return 0;
}
