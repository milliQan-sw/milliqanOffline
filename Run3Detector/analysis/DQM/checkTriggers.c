#include "checkTriggers.h"

using namespace std;

CheckTriggers::CheckTriggers(int runNum) {};
CheckTriggers::~CheckTriggers() {};


bool CheckTriggers::checkFourLayers(int iEvent){

    bool layersHit[4] = {false};

    mychain->GetEntry(iEvent);

    if(chan->size() < 4) return false;

    for(int ihit=0; ihit < int(chan->size()); ihit++){

        if(type->at(ihit) != 0) continue; //Require hit is from a bar

        if(board->at(ihit) <= 4) layersHit[board->at(ihit)] = true;
    }

    if(debug) cout << "Layers: " << layersHit[0] << ", " << layersHit[1] << ", " << layersHit[2] << ", " << layersHit[3] << endl;
    if(layersHit[0] && layersHit[1] && layersHit[2] && layersHit[3]) return true;

    return false;

}

/*bool CheckTriggers::checkThreeInRow(int iEvent){

    mychain->GetEntry(iEvent);

    if(chan->size() < 3) return false;

    vector<int> layersHit;
    for(int ihit=0; ihit < (int)chan->size(); ihit++){

        if(type->at(ihit) != 0) continue; //Require hit is from a bar

        if(find(layersHit.begin(), layersHit.end(), layer->at(ihit)) == layersHit.end()){
            layersHit.push_back(layer->at(ihit));
        }
    }

    if(layersHit.size() < 3) return false;

    sort(layersHit.begin(), layersHit.end());

    if(debug){
        cout << "Hit Layers: ";
        for(auto& hit : layersHit) cout << hit << " ";
        cout << endl;
    }

    if(layersHit[0]==0 && layersHit[1]==1 && layersHit[2]==2) return true;
    else if(layersHit[1] == 1 && layersHit[2] == 2 && layersHit[3]) return true;
    else return false;
}*/

bool CheckTriggers::checkThreeInRow(int iEvent){

    mychain->GetEntry(iEvent);

    if(chan->size() < 3) return false;

    std::vector<int> hitMap[8]; // groups per layer
    std::vector<int> channelMap[8];

    for(int ihit=0; ihit < (int)chan->size(); ihit++){

        if(type->at(ihit) != 0) continue; //Require hit is from a bar

        int thisChan = chan->at(ihit);
        int group = (thisChan % 16) / 2;

        if(find(hitMap[group].begin(), hitMap[group].end(), layer->at(ihit)) == hitMap[group].end()){
            hitMap[group].push_back(layer->at(ihit));
            channelMap[group].push_back(chan->at(ihit));
        }
    }

    for(int igroup=0; igroup < 8; igroup++){
        if(hitMap[igroup].size() >= 3){
            if(debug){
                cout << TString(Form("Three in a row, file: %i, event: %i, hits: ", fileNum, eventNum));
                for(auto& hit3 : channelMap[igroup]) cout << hit3 << " ";
                cout << endl;
            }
            return true;
        }
    }

    return false;

}

bool CheckTriggers::checkTwoSeparateLayers(int iEvent){

    mychain->GetEntry(iEvent);

    if(chan->size() < 2) return false;

    for(int ihit1=0; ihit1 < (int)chan->size(); ihit1++){

        if(type->at(ihit1) != 0) continue; //Require hit is from a bar

        int firstLayer = layer->at(ihit1);
        for(int ihit2=0; ihit2 < (int)chan->size(); ihit2++){

            if(type->at(ihit2) != 0) continue; //Require hit is from a bar
            if(ihit1==ihit2) continue;
            if(abs(firstLayer - layer->at(ihit2)) > 1) {
                if(debug) cout << "Layers hit: " << firstLayer << ", " << layer->at(ihit2) << endl;
                return true;
            }
        }
    }

    return false;
}

bool CheckTriggers::checkTwoAdjacentLayers(int iEvent){
        
    mychain->GetEntry(iEvent);

    if(chan->size() < 2) return false;

    for(int ihit1=0; ihit1 < (int)chan->size(); ihit1++){

        if(type->at(ihit1) != 0) continue; //Require hit is from a bar

        int firstLayer = layer->at(ihit1);
        for(int ihit2=0; ihit2 < (int)chan->size(); ihit2++){

            if(type->at(ihit2) != 0) continue; //Require hit is from a bar
            if(ihit1==ihit2) continue;
            if(abs(firstLayer - layer->at(ihit2)) == 1) {
                if(debug) cout << "Layers hit: " << firstLayer << ", " << layer->at(ihit2) << endl;
                return true;
            }
        }
    }

    return false;
}

//Below functions need to be completed
//CheckNLayers and checkNHits need the thresholds from the triggerConfig file
bool CheckTriggers::checkNLayers(int iEvent){

    return false;
}

bool CheckTriggers::checkExternal(){

    return false;
}

bool CheckTriggers::checkNHits(){

    return false;
}

bool CheckTriggers::checkInternal(){

    return false;
}



int checkTriggers(TString runNum = ""){

    TChain* mychain = new TChain("t");

    TString filename = "/store/user/mcarrigan/trees/MilliQan_Run" + runNum + "*.root";
    cout << filename << endl;
    mychain->Add(filename);

    CheckTriggers mycheck(mychain);
    InitializeChain(mychain);

    mycheck.debug = false;

    int numFourLayers = 0;
    int numThreeInRow = 0;
    int numSeparate = 0;
    int numAdjacent = 0;

    bool fourLayersHit = false;
    bool threeInRow = false;
    bool separateLayers = false;
    bool adjacentLayers = false;

    int totalEvents = mychain->GetEntries();

    cout << "Total Number of Events: " << mychain->GetEntries() << endl;

    for(int ievt=0; ievt < mychain->GetEntries(); ievt++){
        fourLayersHit = mycheck.checkFourLayers(ievt);
        if(fourLayersHit) {
            if(mycheck.debug) cout << A_BRIGHT_RED << "Four Layers Hit!" << A_RESET << endl;
            numFourLayers++;
        }
        threeInRow = mycheck.checkThreeInRow(ievt);
        if(threeInRow) {
            if(mycheck.debug) cout << A_BRIGHT_RED << "Three In A Row!" << A_RESET << endl;
            numThreeInRow++;
        }
        separateLayers = mycheck.checkTwoSeparateLayers(ievt);
        if(separateLayers){
            if(mycheck.debug) cout << A_BRIGHT_RED << "Two separate layers" << A_RESET << endl;
            numSeparate++;
        }
        adjacentLayers = mycheck.checkTwoAdjacentLayers(ievt);
        if(adjacentLayers){
            if(mycheck.debug) cout << A_BRIGHT_RED << "Two adjacent layers" << A_RESET << endl;
            numAdjacent++;
        }
    }

    cout << "Number of events with four layers hit: " << numFourLayers << ", fraction of events: " << (float)numFourLayers / (float)totalEvents << endl;
    cout << "Number of events with three hits in a row: " << numThreeInRow << ", fraction of events: " << (float)numThreeInRow / (float)totalEvents << endl;
    cout << "Number of events with hits in two separate layers: " << numSeparate << ", fraction of events: " << (float)numSeparate / (float)totalEvents << endl;
    cout << "Number of events with hits in two adjacent layers: " << numAdjacent << ", fraction of events: " << (float)numAdjacent / (float)totalEvents << endl;
    //cout << mycheck.checkFourLayers(10) << endl;

    ofstream triggerFile;
    triggerFile.open("triggerCounts.txt", ios::app);
    triggerFile << runNum << " " << (float)numFourLayers / (float)totalEvents << " " << 
                                    (float)numThreeInRow / (float)totalEvents << " " << 
                                    (float)numSeparate / (float)totalEvents << " " << 
                                    (float)numAdjacent / (float)totalEvents << endl;   
    triggerFile.close();

    return 1;
}
