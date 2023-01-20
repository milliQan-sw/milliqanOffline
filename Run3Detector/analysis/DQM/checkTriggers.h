#ifndef CHECKTRIGGERS_H
#define CHECKTRIGGERS_H

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <iostream>
#include "mq3Hists.h"

using namespace std;

class CheckTriggers{

public:

    CheckTriggers(TChain* chain) : mychain(chain) {};
    CheckTriggers(int runNum);

    virtual ~CheckTriggers();

    bool checkFourLayers(int iEvent); //bit 0
    bool checkThreeInRow(int iEvent); //bit 1
    bool checkTwoSeparateLayers(int iEvent); //bit 2
    bool checkTwoAdjacentLayers(int iEvent); //bit 3
    bool checkNLayers(int iEvent); //bit 4
    bool checkExternal(); //bit 5
    bool checkNHits(); //bit 6
    bool checkInternal(); //bit 7

    vector<bool> checkAll();

    bool debug = false;



private:

    TChain* mychain;

};

#endif
