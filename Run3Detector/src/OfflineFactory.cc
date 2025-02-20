#include "./interface/OfflineFactory.h"

OfflineFactory::OfflineFactory(TString inFileName, TString outFileName, TString appendToTag, bool isDRS, bool isSlab, bool isSim, int runNumber, int fileNumber) : 
    inFileName(inFileName),
    outFileName(outFileName),
    appendToTag(appendToTag),
    isDRS(isDRS),
    isSlab(isSlab),
    isSim(isSim),
    runNumber(runNumber),
    fileNumber(fileNumber)
{
    versionShort = "shorttagplaceholder";
    versionLong = "longtagplaceholder";
    /*
    vector<float> reds ={255./255.,31./255.,235./255.,111./255.,219./255.,151./255.,185./255.,194./255.,127./255.,98./255.,211./255.,69./255.,220./255.,72./255.,225./255.,145./255.,233./255.,125./255.,147./255.,110./255.,209./255.,44};
    vector<float> greens={255./255.,30./255.,205./255.,48./255.,106./255.,206./255.,32./255.,188./255.,128./255.,166./255.,134./255.,120./255.,132./255.,56./255.,161./255.,39./255.,232./255.,23./255.,173./255.,53./255.,45./255.,54};
    vector<float> blues={255./255.,30./255.,62./255.,139./255.,41./255.,230./255.,54./255.,130./255.,129./255.,71./255.,178./255.,179./255.,101./255.,150./255.,49./255.,139./255.,87./255.,22./255.,60./255.,21./255.,39./255.,23};
    
    for(int icolor=0;icolor<reds.size();icolor++){
        palette.push_back(new TColor(2000+icolor,reds[icolor],greens[icolor],blues[icolor]));
        colors.push_back(2000+icolor);
    }
    colors[9] = 419; //kGreen+3;
    colors[2] = 2009;
    //colors[3] = 2013;
    colors[12]= 30;
    colors[0]=28;
    //cout<<2<<endl;
    */
    colors.push_back(800); colors.push_back(400-1); colors.push_back(632-2); colors.push_back(880+1);
    colors.push_back(432); colors.push_back(600-6); colors.push_back(416); colors.push_back(920+2);
    colors.push_back(800-7); colors.push_back(400); colors.push_back(840); colors.push_back(632); 
    colors.push_back(860); colors.push_back(400-2); colors.push_back(416+2); colors.push_back(880); 
    colors.push_back(800-1); colors.push_back(632-10); colors.push_back(632+3); colors.push_back(616-1); 
    colors.push_back(432+1); colors.push_back(600-5); colors.push_back(416-7); colors.push_back(920+1); 
    colors.push_back(800+6); colors.push_back(400-9); colors.push_back(840-5); colors.push_back(632-7); 
    colors.push_back(860-2); colors.push_back(400-8); colors.push_back(416-3); colors.push_back(880-1); 
    colors.push_back(800-5); colors.push_back(820-9); colors.push_back(632-6); colors.push_back(616-9);
    colors.push_back(432-10); colors.push_back(600-9); colors.push_back(416-9); colors.push_back(920); 
    colors.push_back(800+1); colors.push_back(400+1); colors.push_back(840-4); colors.push_back(632-9); 
    colors.push_back(860-4); colors.push_back(400+3); colors.push_back(416-6); colors.push_back(880-4); 
    colors.push_back(800-9); colors.push_back(600-2); colors.push_back(632-3); colors.push_back(616-10); 
    colors.push_back(432-8); colors.push_back(600-10); colors.push_back(416-10); colors.push_back(1);
    colors.push_back(800-4); colors.push_back(400-6); colors.push_back(840-8); colors.push_back(632+1); 
    colors.push_back(860-9); colors.push_back(400-5); colors.push_back(416-8); colors.push_back(880-8); 
};

OfflineFactory::OfflineFactory(TString inFileName, TString outFileName, TString appendToTag, bool isDRS, bool isSlab, bool isSim) {
  OfflineFactory(inFileName,outFileName,appendToTag,isDRS,isSlab, isSim, -1,-1);
};
void OfflineFactory::setFriendFile(TString friendFileNameIn){
    friendFileName = friendFileNameIn;
}
void OfflineFactory::addFriendTree(){
    inTree->AddFriend("matchedTrigEvents",friendFileName);
    inTree->SetBranchAddress("clockCycles", &tClockCycles);
    inTree->SetBranchAddress("time", &tTime);
    inTree->SetBranchAddress("startTime", &tStartTime);
    inTree->SetBranchAddress("trigger", &tTrigger);
    inTree->SetBranchAddress("timeDiff", &tTimeDiff);
    inTree->SetBranchAddress("matchingTimeCut", &tMatchingTimeCut);
    inTree->SetBranchAddress("eventNum", &tEvtNum);
    inTree->SetBranchAddress("runNum", &tRunNum);
    inTree->SetBranchAddress("tbEvent", &tTBEvent);

    //Add trigger board meta data
    matchedFile = TFile::Open(friendFileName, "read");
    if (matchedFile->GetListOfKeys()->Contains("MetaData")){
        trigMetaData = (TTree*) matchedFile->Get("MetaData");
        trigMetaDataCopy = trigMetaData->CloneTree();
        trigMetaDataCopy->SetDirectory(0);
        writeTriggerMetaData=true;
    }
    matchedFile->Close();

}

// OfflineFactory::~OfflineFactory() {
//     if (inFile) inFile->Close();
//     if (outFile) outFile->Close();
// }
void OfflineFactory::loadJsonConfig(string configFileName){
    std::string json;
    // configFileName = "{\"chanMap\":[[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7]]}";
    if (configFileName.find("{") != std::string::npos){
        json = configFileName;
    }
    else{
        std::ifstream t(configFileName);
        std::stringstream buffer;
        buffer << t.rdbuf();
        json = buffer.str();
    }

    Json::Reader reader;
    Json::Value jsonRoot;
    bool parseSuccess = reader.parse(json, jsonRoot, false);
    if (parseSuccess)
        {
            if (json.find("chanMap") != std::string::npos){
                const Json::Value chan0 = jsonRoot["chanMap"];
                for ( int index = 0; index < chan0.size(); ++index ){
                    std::vector<int> chanMapPerChan;
                    for ( int index2 = 0; index2 < chan0[index].size(); ++index2 ){
                        chanMapPerChan.push_back(chan0[index][index2].asInt());
                    }
                    chanMap.push_back(chanMapPerChan);
                }
            }
            if (json.find("pulseParams") != std::string::npos){
                nConsecSamples.clear();
                nConsecSamplesEnd.clear();
                lowThresh.clear();
                highThresh.clear();
                const Json::Value pulseParams = jsonRoot["pulseParams"];
                const Json::Value nConsecSamplesJson = pulseParams["nConsecSamples"];
                const Json::Value nConsecSamplesEndJson = pulseParams["nConsecSamplesEnd"];
                const Json::Value highThreshJson = pulseParams["highThresh"];
                const Json::Value lowThreshJson = pulseParams["lowThresh"];
                for (int index = 0; index < nConsecSamplesJson.size(); index ++){
                    nConsecSamples.push_back(nConsecSamplesJson[index].asInt());
                }
                for (int index = 0; index < nConsecSamplesEndJson.size(); index ++){
                    nConsecSamplesEnd.push_back(nConsecSamplesEndJson[index].asInt());
                }
                for (int index = 0; index < highThreshJson.size(); index ++){
                    highThresh.push_back(highThreshJson[index].asFloat());
                }
                for (int index = 0; index < lowThreshJson.size(); index ++){
                    lowThresh.push_back(lowThreshJson[index].asFloat());
                }
            }
            if (json.find("timingCalibrations") != std::string::npos){
                const Json::Value timingCalibrationsJson = jsonRoot["timingCalibrations"];
                for (int index = 0; index < timingCalibrationsJson.size(); index ++){
                    timingCalibrations.push_back(timingCalibrationsJson[index].asFloat());
                }
            }
            if (json.find("speAreas") != std::string::npos){
                const Json::Value speAreasJson = jsonRoot["speAreas"];
                for (int index = 0; index < speAreasJson.size(); index ++){
                    speAreas.push_back(speAreasJson[index].asFloat());
                }
            }
            if (json.find("pedestals") != std::string::npos){
                const Json::Value pedestalsJson = jsonRoot["pedestals"];
                for (int index = 0; index < pedestalsJson.size(); index ++){
                    pedestals.push_back(pedestalsJson[index].asFloat());
                }
            }
            if (json.find("sampleRate") != std::string::npos){
                sampleRate = jsonRoot["sampleRate"].asFloat();
                std::cout << "Loaded sample rate: " << sampleRate << " GHz" << std::endl;
                std::cout << "This will be overwritten by metadata if available" << std::endl;
            }
        }
    else{
        throw invalid_argument(configFileName);
    }
}

//Function to separate all lumi contents when run is across multiple fills
std::vector<std::string> OfflineFactory::splitLumiContents(std::string input){
    std::vector<std::string> output;

    std::string substr = input;
    substr.erase(remove(substr.begin(), substr.end(), ']'), substr.end()); 
    substr.erase(remove(substr.begin(), substr.end(), '['), substr.end()); 

    //substr.remove(substr.begin(), substr.end(), '[');
    //substr.remove(substr.begin(), substr.end(), ']');

    while(substr.find(',') != std::string::npos){
        std::string newOut = substr.substr(0, substr.find(','));
        output.push_back(newOut);
        substr = substr.substr(substr.find(','), substr.size());
        std::cout << "found new substr: " << newOut << ", cut down old substr: " << substr << std::endl;
    }
    
    output.push_back(substr);
    return output;
}

//Function to load good runs list and check if this file is "good"
void OfflineFactory::checkGoodRunList(std::string goodRunList){
    if (isSlab) return; //temporary while no good runs
    std::string json;
    if (goodRunList.find("{") != std::string::npos){
        json = goodRunList;
    }
    else{
        std::ifstream t(goodRunList);
        std::stringstream buffer;
        buffer << t.rdbuf();
        json = buffer.str();
    }

    Json::Reader reader;
    Json::Value jsonRoot;
    bool parseSuccess = reader.parse(json, jsonRoot, false);
    if (parseSuccess){

        if(json.find("data") != std::string::npos){
            const Json::Value data = jsonRoot["data"];
            for (int index = 0; index < data.size(); index ++){
                if ( data[index][0].asInt() == runNumber && stoi(data[index][1].asString()) == fileNumber){
                    goodRunLoose = data[index][2].asBool();
                    goodRunMedium = data[index][3].asBool();
                    goodRunTight = data[index][4].asBool();
                    goodSingleTrigger = data[index][5].asBool();
                    goodRunTag = data[index][6].asString();
                    break;
                }
            }
        }
    }
    else{
        std::cout << "Error: OfflineFactory::checkGoodRunList" << std::endl;
        throw invalid_argument(goodRunList);
    }
}

//Function to load lumis json file
void OfflineFactory::getLumis(std::string lumiFile){
    if(isSlab) return; //temporary while there are no lumis
    std::string json;
    if (lumiFile.find("{") != std::string::npos){
        json = lumiFile;
    }
    else{
        std::ifstream t(lumiFile);
        std::stringstream buffer;
        buffer << t.rdbuf();
        json = buffer.str();
    }

    Json::Reader reader;
    Json::Value jsonRoot;
    bool parseSuccess = reader.parse(json, jsonRoot, false);
    if (parseSuccess){
        if(json.find("data") != std::string::npos){
            const Json::Value data = jsonRoot["data"];
            for (int index = 0; index < data.size(); index ++){
                //TODO fix it so that the filenumber is an int
                if ( data[index][0].asInt() == runNumber && stoi(data[index][1].asString()) == fileNumber){
                    if (data[index][3].isArray()){
                        std::cout << "Run split among multiple fills" << std::endl;

                        for (int ifill=0; ifill < data[index][3].size(); ifill++){
                            v_fillId.push_back(data[index][3][ifill].asInt());
                            v_beamType.push_back(data[index][10][ifill].asString());
                            v_fillStart.push_back(data[index][13][ifill].asUInt64());
                            v_fillEnd.push_back(data[index][14][ifill].asUInt64());
                            v_beamInFill.push_back(data[index][5][ifill].asBool());
                            if (data[index][11][ifill].isNull() || data[index][12][ifill].isNull() || data[index][2][ifill].isNull()){
                                v_beamEnergy.push_back(-1);
                                v_betaStar.push_back(-1);
                                v_stableBeamStart.push_back(0);
                                v_stableBeamEnd.push_back(0);
                                v_lumi.push_back(0);
                            }
                            else{
                                v_beamEnergy.push_back(data[index][11][ifill].asFloat());
                                v_betaStar.push_back(data[index][12][ifill].asFloat());
                                v_stableBeamStart.push_back(data[index][15][ifill].asUInt64());
                                v_stableBeamEnd.push_back(data[index][16][ifill].asUInt64());
                                v_lumi.push_back(data[index][2][ifill].asFloat());
                            }
                        }
                    }
                    else{
                        v_lumi.push_back(data[index][2].asFloat());
                        v_fillId.push_back(data[index][3].asInt());
                        v_beamType.push_back(data[index][10].asString());
                        v_beamEnergy.push_back(data[index][11].asFloat()); 
                        v_betaStar.push_back(data[index][12].asFloat());
                        v_fillStart.push_back(data[index][13].asUInt64()); 
                        v_fillEnd.push_back(data[index][14].asUInt64());
                        v_stableBeamStart.push_back(data[index][15].asUInt64());
                        v_stableBeamEnd.push_back(data[index][16].asUInt64());
                        v_beamInFill.push_back(data[index][5].asBool());

                    }
                }
                /*if (!v_lumi.empty()) std::cout << "lumi: " << v_lumi.back() << std::endl;
                if (!v_fillId.empty())std::cout<< "\n fill: " << v_fillId.back() << std::endl;
                if (!v_beamType.empty())std::cout<< "\n type: " << v_beamType.back() << std::endl;
                if (!v_beamEnergy.empty())std::cout<< "\n energy: " << v_beamEnergy.back()  << std::endl;
                if (!v_betaStar.empty())std::cout<< "\n beta star: " << v_betaStar.back() << std::endl;
                if (!v_fillStart.empty())std::cout<< "\n fill start: " << v_fillStart.back()<< std::endl;
                if (!v_fillEnd.empty())std::cout<< "\n fill end: " << v_fillEnd.back()<< std::endl;
                if (!v_stableBeamStart.empty())std::cout<< "\n stable beam start: " << v_stableBeamStart.back() << std::endl;
                if (!v_stableBeamEnd.empty())std::cout<< "\n stable beam end: " << v_stableBeamEnd.back() << std::endl;
                if (!v_beamInFill.empty())std::cout<< "\n beam in fill: " << v_beamInFill.back() << std::endl;*/
            }

        }
    }
    else{
        std::cout << "Error: OfflineFactory::getLumis" << std::endl;
        throw invalid_argument(lumiFile);
    }
}

void OfflineFactory::setGoodRuns(){
    outputTreeContents.goodRunLoose = goodRunLoose;
    outputTreeContents.goodRunMedium = goodRunMedium;
    outputTreeContents.goodRunTight = goodRunTight;
    outputTreeContents.goodSingleTrigger = goodSingleTrigger;
}

void OfflineFactory::getEventLumis(){
    Long64_t event_time = outputTreeContents.event_time_fromTDC;

    if (v_fillEnd.size() > 0 && v_fillStart.size() > 0){
        auto maxFillEnd = std::max_element(v_fillEnd.begin(), v_fillEnd.end());
        auto minFillBegin = std::min_element(v_fillStart.begin(), v_fillStart.end());
      

        if (event_time > *maxFillEnd){
            outputTreeContents.beamOn=false;
            outputTreeContents.lumi = -1;
            outputTreeContents.fillId = -1;
            outputTreeContents.beamType = TString("None");
            outputTreeContents.beamEnergy = -1;
            outputTreeContents.betaStar = -1;
            outputTreeContents.fillStart = 0;
            outputTreeContents.fillEnd = 0;
            outputTreeContents.beamInFill = false;
            if(firstWarning) {
                cout << "Warning some events occured after last fill time in mqLumis" << endl;
                firstWarning=false;
            }
            return;
        }

        if (event_time < *minFillBegin){
            outputTreeContents.beamOn=false;
            outputTreeContents.lumi = -1;
            outputTreeContents.fillId = -1;
	    outputTreeContents.beamType = TString("None");
	    outputTreeContents.beamEnergy = -1;
	    outputTreeContents.betaStar = -1;
	    outputTreeContents.fillStart = 0;
	    outputTreeContents.fillEnd = 0;
	    outputTreeContents.beamInFill = false;        
	    if(firstWarning){
	        cout << "Warning some event occured before first fill time in mqLumis" << endl;
	        firstWarning=false;
            }
	    return;
	}
    }

    for(int ifill=0; ifill < v_fillId.size(); ifill++){
        //cout << "event time: " << event_time << ", fill start: " << v_fillStart[ifill]/long(1e3) << ", fill end: " << v_fillEnd[ifill]/long(1e3) << endl;
        if (event_time >= v_fillStart[ifill] && event_time <= v_fillEnd[ifill]){
            //cout << "Found good fill" << endl;
            outputTreeContents.lumi = v_lumi[ifill];
            outputTreeContents.fillId = v_fillId[ifill];
            outputTreeContents.beamType = v_beamType[ifill];
            outputTreeContents.beamEnergy = v_beamEnergy[ifill];
            outputTreeContents.betaStar = v_betaStar[ifill];
            outputTreeContents.fillStart = v_fillStart[ifill];
            outputTreeContents.fillEnd = v_fillEnd[ifill];
            outputTreeContents.beamInFill = v_beamInFill[ifill];
            if(event_time >= v_stableBeamStart[ifill] && event_time <= v_stableBeamEnd[ifill]) outputTreeContents.beamOn=true;
            else outputTreeContents.beamOn=false;
            return;
        }
    }
    outputTreeContents.beamOn=false;
    outputTreeContents.lumi = -1;
    outputTreeContents.fillId = -1;
    outputTreeContents.beamType = TString("None");
    outputTreeContents.beamEnergy = -1;
    outputTreeContents.betaStar = -1;
    outputTreeContents.fillStart = 0;
    outputTreeContents.fillEnd = 0;   
    outputTreeContents.beamInFill = false; 
    if(firstWarning){
        cout << "Warning did not find matching fill time for some events" << endl;
        firstWarning=false;
    }
    return;
}

void OfflineFactory::setTotalLumi(){
    float totalLumi = 0;
    for(int ifill=0; ifill < v_fillId.size(); ifill++){
        if (v_stableBeamStart[ifill]==0 && v_stableBeamEnd[ifill]==0) continue;
        else if (firstTDC_time > v_stableBeamEnd[ifill] && lastTDC_time > v_stableBeamEnd[ifill]) continue;
        else if (firstTDC_time < v_stableBeamStart[ifill] && lastTDC_time < v_stableBeamStart[ifill]) continue;
        else if (firstTDC_time < v_stableBeamStart[ifill] && lastTDC_time >= v_stableBeamEnd[ifill]){
            totalLumi+=v_lumi[ifill];
        }
        else if(firstTDC_time < v_stableBeamStart[ifill] && lastTDC_time < v_stableBeamEnd[ifill]){
            ulong stable_duration = v_stableBeamEnd[ifill] - v_stableBeamStart[ifill];
            ulong mq_duration = (ulong)lastTDC_time - v_stableBeamStart[ifill];
            totalLumi+=v_lumi[ifill] * ((double)mq_duration/(double)stable_duration);
        }
        else if(firstTDC_time > v_stableBeamStart[ifill] && lastTDC_time >= v_stableBeamEnd[ifill]){
            ulong stable_duration = v_stableBeamEnd[ifill] - v_stableBeamStart[ifill];
            ulong mq_duration = v_stableBeamEnd[ifill] - (ulong)firstTDC_time;
            totalLumi+=v_lumi[ifill] * ((double)mq_duration/(double)stable_duration);
        }
        else if(firstTDC_time > v_stableBeamStart[ifill] && lastTDC_time < v_stableBeamEnd[ifill]){
            ulong stable_duration = v_stableBeamEnd[ifill] - v_stableBeamStart[ifill];
            ulong mq_duration = lastTDC_time - firstTDC_time;
            totalLumi += v_lumi[ifill] * ((double)mq_duration/(double)stable_duration);
        }
    }
    cout << "Total lumi in this file: " << totalLumi << endl;

    TBranch* b_fileLumi = outTree->Branch("totalFileLumi", &totalLumi);
    for(int i=0; i<inTree->GetEntries(); i++){
        outTree->GetEntry(i);
        b_fileLumi->Fill();
    }
}


//Validate json input
void OfflineFactory::validateInput(){
    //HACKY check if tag has been added
    if(versionShort.Contains("placeholder")) throw runtime_error("This macro was compiled incorrectly. Please compile this macro using compile.sh");
    if (chanMap.size()) 
        {
            if (chanMap.size() != numChan) throw length_error("Number of channels ("+std::to_string(numChan)+") does not match channel map length: "+std::to_string(chanMap.size()));
        }
    if (nConsecSamples.size() > 1){
        if (nConsecSamples.size() != numChan) throw length_error("nConsecSamples should be length "+std::to_string(numChan) + "or 1");
    }
    else{ 
        for (int ic = 0; ic < numChan-1; ic++) nConsecSamples.push_back(nConsecSamples.at(0));
        outputTreeContents.nConsecSamples_ = nConsecSamples;

    }
    if (nConsecSamplesEnd.size() > 1){
        if (nConsecSamplesEnd.size() != numChan) throw length_error("nConsecSamplesEnd should be length "+std::to_string(numChan) + "or 1");
    }
    else{ 
        for (int ic = 0; ic < numChan-1; ic++) nConsecSamplesEnd.push_back(nConsecSamplesEnd.at(0));
        outputTreeContents.nConsecSamplesEnd_ = nConsecSamplesEnd;
    }
    if (lowThresh.size() > 1){
        if (lowThresh.size() != numChan) throw length_error("lowThresh should be length "+std::to_string(numChan) + "or 1");
    }
    else{ 
        for (int ic = 0; ic < numChan-1; ic++) lowThresh.push_back(lowThresh.at(0));
        outputTreeContents.lowThreshold_ = lowThresh;
    }
    if (highThresh.size() > 1){
        if (highThresh.size() != numChan) throw length_error("highThresh should be length "+std::to_string(numChan) + "or 1");
    }
    else {
        for (int ic = 0; ic < numChan-1; ic++) highThresh.push_back(highThresh.at(0));
        if(variableThresholds && !isSlab && !isSim){
            for (int ic = 0; ic < numChan; ic++){
                if (outputTreeContents.v_triggerThresholds[ic]*10e3 > 50) continue; //if pannel keep default
                highThresh[ic] = outputTreeContents.v_triggerThresholds[ic]*10e3 - thresholdDecrease;
            }
        }
        outputTreeContents.highThreshold_ = highThresh;
    }
    ////Calibrations
    if (timingCalibrations.size() > 0){
        if (timingCalibrations.size() != numChan) throw length_error("timingCalibrations should be length "+std::to_string(numChan));
    }
    else{ 
        for (int ic = 0; ic < numChan; ic++) timingCalibrations.push_back(0);
    }
    if (pedestals.size() > 0){
        if (pedestals.size() != numChan) throw length_error("pedestals should be length "+std::to_string(numChan));
        for (int ic = 0; ic < numChan; ic++) pedestals[ic] = 0;
    }
    else{ 
        for (int ic = 0; ic < numChan; ic++) pedestals.push_back(0);
    }
    if (speAreas.size() > 0){
        if (speAreas.size() != numChan) throw length_error("speAreas should be length "+std::to_string(numChan));
    }
    else{ 
        for (int ic = 0; ic < numChan; ic++) speAreas.push_back(1);
    }
}

//Get pulse mean and RMS for 30 samples before pulse
const pair<float, float> OfflineFactory::getPrePulseVar(TH1D* wave, float time){
    int startbin = wave->FindBin(time-prePulseRange);
    int endbin = wave->FindBin(time);
    int n_sb = 0;
    float sum_sb=0.;
    float sum2_sb=0.;
    for(int ibin=startbin; ibin <= endbin; ibin++){
        sum_sb = sum_sb + wave->GetBinContent(ibin);
        sum2_sb = sum2_sb + pow(wave->GetBinContent(ibin),2);
        n_sb++;
    }
    if(n_sb == 0) n_sb = 1.;
    float mean = sum_sb/n_sb;
    float RMS =pow( sum2_sb/n_sb - pow(mean,2), 0.5);

    return pair<float, float>(mean, RMS);
}

//Convenience function to produce offline tree output
//Makedisplays and then not save the output tree //makeoutputtree is not called
void OfflineFactory::processDisplays(vector<int> & eventsToDisplay,TString displayDirectory){
    inFile = TFile::Open(inFileName,"READ");
    readMetaData();
    displayEvents(eventsToDisplay,displayDirectory);
}
void OfflineFactory::processDisplays(vector<int> & eventsToDisplay,TString displayDirectory,TString inFileName)
{
    inFileName = inFileName;
    runNumber = -1;
    fileNumber = -1;
    processDisplays(eventsToDisplay,displayDirectory);
}
void OfflineFactory::processDisplays( vector<int> & eventsToDisplay,TString displayDirectory,TString inFileName,int runNumber,int fileNumber)
{
    inFileName = inFileName;
    runNumber = runNumber;
    fileNumber = fileNumber;
    processDisplays(eventsToDisplay,displayDirectory);
}
void OfflineFactory::process(){

    // Testing json stuff
    makeOutputTree();
    inFile = TFile::Open(inFileName, "READ");
    readMetaData();
    readWaveData();
    writeOutputTree();
}
void OfflineFactory::process(TString inFileName,TString outFileName)
{
    inFileName = inFileName;
    outFileName = outFileName;
    runNumber = -1;
    fileNumber = -1;
    process();
}
void OfflineFactory::process(TString inFileName,TString outFileName,int runNumber,int fileNumber)
{
    inFileName = inFileName;
    outFileName = outFileName;
    runNumber = runNumber;
    fileNumber = fileNumber;
    process();
}
//Declare branches for offline tree output
void OfflineFactory::prepareOutBranches(){
    //Meta
    outTree->Branch("event", &outputTreeContents.event);
    outTree->Branch("runNumber", &outputTreeContents.runNumber);
    outTree->Branch("fileNumber", &outputTreeContents.fileNumber);
    outTree->Branch("boardsMatched", &outputTreeContents.boardsMatched);
    outTree->Branch("DAQEventNumber", &outputTreeContents.DAQEventNumber);
    outTree->Branch("daqFileOpen", &outputTreeContents.daqFileOpen);
    outTree->Branch("daqFileClose", &outputTreeContents.daqFileClose);
    outTree->Branch("maxPulseIndex", &outputTreeContents.maxPulseIndex);

    outTree->Branch("nConsecSamples", &outputTreeContents.nConsecSamples_);
    outTree->Branch("nConsecSamplesEnd", &outputTreeContents.nConsecSamplesEnd_);
    outTree->Branch("highThreshold", &outputTreeContents.highThreshold_);
    outTree->Branch("lowThreshold", &outputTreeContents.lowThreshold_);

    outTree->Branch("totalFillLumi",&outputTreeContents.lumi);
    outTree->Branch("fillId",&outputTreeContents.fillId);
    outTree->Branch("beamType",&outputTreeContents.beamType);
    outTree->Branch("beamEnergy",&outputTreeContents.beamEnergy);
    outTree->Branch("betaStar",&outputTreeContents.betaStar);
    outTree->Branch("beamOn",&outputTreeContents.beamOn);
    outTree->Branch("fillStart",&outputTreeContents.fillStart);
    outTree->Branch("fillEnd",&outputTreeContents.fillEnd);
    outTree->Branch("beamInFill",&outputTreeContents.beamInFill);

    outTree->Branch("goodRunLoose", &outputTreeContents.goodRunLoose);
    outTree->Branch("goodRunMedium", &outputTreeContents.goodRunMedium);
    outTree->Branch("goodRunTight", &outputTreeContents.goodRunTight);
    outTree->Branch("goodSingleTrigger", &outputTreeContents.goodSingleTrigger);    

    // May need to change for DRS input
    outTree->Branch("triggerThreshold",&outputTreeContents.v_triggerThresholds);
    outTree->Branch("triggerEnable",&outputTreeContents.v_triggerEnable);
    outTree->Branch("triggerMajority",&outputTreeContents.v_triggerMajority);
    outTree->Branch("triggerPolarity",&outputTreeContents.v_triggerPolarity);
    outTree->Branch("triggerLogic",&outputTreeContents.v_triggerLogic);
    outTree->Branch("dynamicPedestal",&outputTreeContents.v_dynamicPedestal);
    outTree->Branch("sidebandMean",&outputTreeContents.v_sideband_mean);
    outTree->Branch("sidebandRMS",&outputTreeContents.v_sideband_RMS);
    outTree->Branch("sidebandMeanRaw",&outputTreeContents.v_sideband_mean_raw);
    outTree->Branch("sidebandRMSRaw",&outputTreeContents.v_sideband_RMS_raw);
    outTree->Branch("maxThreeConsec",&outputTreeContents.v_max_threeConsec);
    outTree->Branch("chan",&outputTreeContents.v_chan);
    outTree->Branch("chanWithinBoard",&outputTreeContents.v_chanWithinBoard);
    outTree->Branch("row",&outputTreeContents.v_row);
    outTree->Branch("column",&outputTreeContents.v_column);
    outTree->Branch("layer",&outputTreeContents.v_layer);
    outTree->Branch("type",&outputTreeContents.v_type);
    outTree->Branch("board",&outputTreeContents.v_board);
    outTree->Branch("height",&outputTreeContents.v_height);
    outTree->Branch("area",&outputTreeContents.v_area);
    outTree->Branch("pickupFlag",&outputTreeContents.v_pickupFlag);
    outTree->Branch("pickupFlagTight",&outputTreeContents.v_pickupFlagTight);
    outTree->Branch("nPE",&outputTreeContents.v_nPE);
    outTree->Branch("riseSamples",&outputTreeContents.v_riseSamples);
    outTree->Branch("fallSamples",&outputTreeContents.v_fallSamples);
    outTree->Branch("ipulse",&outputTreeContents.v_ipulse);
    outTree->Branch("npulses",&outputTreeContents.v_npulses);
    outTree->Branch("pulseIndex",&outputTreeContents.v_pulseIndex);
    outTree->Branch("time",&outputTreeContents.v_time);
    outTree->Branch("timeFit",&outputTreeContents.v_timeFit);
    outTree->Branch("time_module_calibrated",&outputTreeContents.v_time_module_calibrated);
    outTree->Branch("timeFit_module_calibrated",&outputTreeContents.v_timeFit_module_calibrated);
    outTree->Branch("duration",&outputTreeContents.v_duration);
    outTree->Branch("delay",&outputTreeContents.v_delay);
    outTree->Branch("max",&outputTreeContents.v_max);
    outTree->Branch("iMaxPulseLayer",&outputTreeContents.v_iMaxPulseLayer);
    outTree->Branch("maxPulseTime",&outputTreeContents.v_maxPulseTime);
    outTree->Branch("prePulseMean", &outputTreeContents.v_prePulseMean);
    outTree->Branch("prePulseRMS", &outputTreeContents.v_prePulseRMS);

    outTree->Branch("present",&outputTreeContents.present);
    outTree->Branch("event_trigger_time_tag",&outputTreeContents.event_trigger_time_tag);
    outTree->Branch("event_time",&outputTreeContents.event_time);
    outTree->Branch("event_time_fromTDC",&outputTreeContents.event_time_fromTDC);
    outTree->Branch("v_groupTDC_g0",&outputTreeContents.v_groupTDC_g0);
    outTree->Branch("v_groupTDC_g1",&outputTreeContents.v_groupTDC_g1);
    outTree->Branch("v_groupTDC_g2",&outputTreeContents.v_groupTDC_g2);
    outTree->Branch("v_groupTDC_g3",&outputTreeContents.v_groupTDC_g3);
    outTree->Branch("v_groupTDC_g4",&outputTreeContents.v_groupTDC_g4);
    outTree->Branch("v_groupTDC_g5",&outputTreeContents.v_groupTDC_g5);
    outTree->Branch("v_groupTDC_g6",&outputTreeContents.v_groupTDC_g6);
    outTree->Branch("v_groupTDC_g7",&outputTreeContents.v_groupTDC_g7);

    outTree->Branch("tClockCycles", &outputTreeContents.tClockCycles);
    outTree->Branch("tTime", &outputTreeContents.tTime);
    outTree->Branch("tStartTime", &outputTreeContents.tStartTime);
    outTree->Branch("tTrigger", &outputTreeContents.tTrigger);
    outTree->Branch("tTimeDiff", &outputTreeContents.tTimeDiff);
    outTree->Branch("tMatchingTimeCut", &outputTreeContents.tMatchingTimeCut);
    outTree->Branch("tEvtNum", &outputTreeContents.tEvtNum);
    outTree->Branch("tRunNum", &outputTreeContents.tRunNum);
    outTree->Branch("tTBEvent", &outputTreeContents.tTBEvent);

    if (isSim){
        outTree->Branch("eventWeight", &outputTreeContents.eventWeight);
    }
}
//Clear vectors and reset 
void OfflineFactory::resetOutBranches(){
    // May need to change for DRS input
    outputTreeContents.v_dynamicPedestal.clear();
    outputTreeContents.v_sideband_mean.clear();
    outputTreeContents.v_sideband_RMS.clear();
    outputTreeContents.v_sideband_mean_raw.clear();
    outputTreeContents.v_sideband_RMS_raw.clear();
    outputTreeContents.v_max_threeConsec.clear();
    outputTreeContents.v_chan.clear();
    outputTreeContents.v_chanWithinBoard.clear();
    outputTreeContents.v_row.clear();
    outputTreeContents.v_column.clear();
    outputTreeContents.v_layer.clear();
    outputTreeContents.v_type.clear();
    outputTreeContents.v_board.clear();
    outputTreeContents.v_height.clear();
    outputTreeContents.v_area.clear();
    outputTreeContents.v_pickupFlag.clear();
    outputTreeContents.v_pickupFlagTight.clear();
    outputTreeContents.v_nPE.clear();
    outputTreeContents.v_riseSamples.clear();
    outputTreeContents.v_fallSamples.clear();
    outputTreeContents.v_ipulse.clear();
    outputTreeContents.v_npulses.clear();
    outputTreeContents.v_pulseIndex.clear();
    outputTreeContents.v_time.clear();
    outputTreeContents.v_time_module_calibrated.clear();
    outputTreeContents.v_timeFit.clear();
    outputTreeContents.v_timeFit_module_calibrated.clear();
    outputTreeContents.v_duration.clear();
    outputTreeContents.v_delay.clear();
    outputTreeContents.v_max.clear();
    outputTreeContents.v_maxPulseTime.clear();
    outputTreeContents.v_iMaxPulseLayer.clear();
    outputTreeContents.present.clear();
    outputTreeContents.event_trigger_time_tag.clear();
    outputTreeContents.event_time.clear();
    outputTreeContents.v_groupTDC_g0.clear();
    outputTreeContents.v_groupTDC_g1.clear();
    outputTreeContents.v_groupTDC_g2.clear();
    outputTreeContents.v_groupTDC_g3.clear();
    outputTreeContents.v_groupTDC_g4.clear();
    outputTreeContents.v_groupTDC_g5.clear();
    outputTreeContents.v_groupTDC_g6.clear();
    outputTreeContents.v_groupTDC_g7.clear();
    outputTreeContents.v_prePulseMean.clear();
    outputTreeContents.v_prePulseRMS.clear();
}

ulong OfflineFactory::getUnixTime(TString& timeIn){
    const char* timeStr = timeIn.Data();

    std::tm tm_ = {};
    if (strptime(timeStr, "%Y-%m-%d_%Hh%Mm%Ss", &tm_) == nullptr) {
        std::cerr << "Failed to parse the time." << std::endl;
        return 1;
    }

    std::time_t unixTime = std::mktime(&tm_);

    if (unixTime == -1) {
        std::cerr << "Failed to convert to Unix timestamp." << std::endl;
        return 1;
    }

    return unixTime;
}

//Read meta data from configuration
void OfflineFactory::readMetaData(){
    //May need to change for DRS input
    TTree * metadata;
    metadata = (TTree*) inFile->Get("Metadata");
    if (!isDRS && !isSim){
        metadata->SetBranchAddress("configuration", &cfg);
        metadata->SetBranchAddress("fileOpenTime", &fileOpenTime);
        metadata->SetBranchAddress("fileCloseTime", &fileCloseTime);
        metadata->GetEntry(0);

        outputTreeContents.runNumber = runNumber;
        outputTreeContents.fileNumber = fileNumber;
        numBoards = cfg->digitizers.size();
        numChan = numBoards*16;
        chanArray = new TArrayI(numChan);
        boardArray = new TArrayI(numChan);
        //Read sampling rate from the metadata
        double secondsPerSample = cfg->digitizers[0].secondsPerSample;
        sampleRate = 1.0/(secondsPerSample*1e+09);
        cout << "Overwriting sample rate from metadata: " << sampleRate <<" GHz" << endl; 
        //cout<<"secondspersample = "<<secondsPerSample<<" samplingrate="<<1.0/(secondsPerSample*1e+09)<< "GHz"<<endl;

        outputTreeContents.daqFileOpen = getUnixTime(*fileOpenTime);
        outputTreeContents.daqFileClose = getUnixTime(*fileCloseTime);
            
        //Read trigger info and set channel array
        for (int ic =0; ic < numChan; ic++){
            chanArray->SetAt(ic % 16,ic);
            boardArray->SetAt(ic/16,ic);
            float triggerThresh = cfg->digitizers[ic/16].channels[ic % 16].triggerThreshold;
            bool triggerEnable = cfg->digitizers[ic/16].channels[ic % 16].triggerEnable;
            int triggerPolarity = cfg->digitizers[ic/16].channels[ic % 16].triggerPolarity;
            int triggerMajority = cfg->digitizers[ic/16].GroupTriggerMajorityLevel;
            int triggerLogic = cfg->digitizers[ic/16].GroupTriggerLogic;
            outputTreeContents.v_triggerThresholds.push_back(triggerThresh);
            outputTreeContents.v_triggerEnable.push_back(triggerEnable);
            outputTreeContents.v_triggerMajority.push_back(triggerMajority);
            outputTreeContents.v_triggerLogic.push_back(triggerLogic);
            outputTreeContents.v_triggerPolarity.push_back(triggerPolarity);

            /*if (true){
                std::cout << "high thresh " << highThresh[ic] << std::endl;
                highThresh[ic] = triggerThresh*10e3 - 5;
            }*/
        }
    }
    else if(!isSim){
        //ADD SOMETHING TO DRS INPUT SUCH THAT THIS CAN BE EASILY READ!
        //output_trees_test/CMS31.root
        metadata->SetBranchAddress("samplingRate", &sampleRate);
        cout << "Overwriting sample rate from metadata: " << sampleRate <<" GHz" << endl; 
        metadata->SetBranchAddress("numChan", &numChan);
        metadata->SetBranchAddress("board_ids", &boardsDRS);
        metadata->SetBranchAddress("channels", &chansDRS);
        metadata->GetEntry(0);
        chanArray = new TArrayI(numChan);
        boardArray = new TArrayI(numChan);
        for (int ic =0; ic < numChan; ic++){
            chanArray->AddAt(chansDRS[ic],ic);
            boardArray->AddAt(boardsDRS[ic],ic);
        }
    }
    // For sim data
    else{
      outputTreeContents.runNumber = runNumber;
      outputTreeContents.fileNumber = fileNumber;
      float secondsPerSample;
      metadata->SetBranchAddress("secondsPerSample", &secondsPerSample);
      metadata->SetBranchAddress("numChan", &numChan);
      metadata->GetEntry(0);
      chanArray = new TArrayI(numChan);
      boardArray = new TArrayI(numChan);
      sampleRate = 1.0/(secondsPerSample*1e+09);
      for (int ic=0; ic < numChan; ++ic){
        chanArray->SetAt(ic % 16, ic);
        boardArray->SetAt(ic/16,ic);
      }
    }
      
}

void OfflineFactory::makeOutputTree(){
    outFile = new TFile(outFileName,"recreate");
    outTree = new TTree("t","t");
    prepareOutBranches(); 
}

//Plots cosmetic changes
void OfflineFactory::h1cosmetic(TH1D* hist,int ic, vector<int> & colors){
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
/*
void defineColors(vector<int>colors, vector<TColor*> palette, vector<float> reds, vector<float> greens, vector<float> blues){
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
*/
//Display making
void OfflineFactory::displayEvent(int event, vector<vector<pair<float,float> > >& bounds,TString displayDirectory){
    TCanvas c("c1","",1400,800);
    gPad->SetRightMargin(0.45);
    gStyle->SetGridStyle(3);
    gStyle->SetGridColor(13);
    c.SetGrid();

    float drawThresh=15;

    gStyle->SetTitleX(0.35);
    vector<int> chanList;
    float maxheight=0; float minheight=0;
    float timeRange[2];
    timeRange[1]=1024./sampleRate; timeRange[0]=0.;
    //Get the waves                                                                             
    vector<vector<pair<float,float>>> boundsShifted;
    vector<TH1D*> wavesShifted;
    vector<int> index;
    float originalMaxHeights[80]; // FIXME: This is hardcoded to be the number of channels in the bar detector (?)
    for(uint ic=0;ic<bounds.size();ic++){
        int chan = chanArray->GetAt(ic);
        index.push_back(ic);
        vector<pair<float,float>> boundShifted = bounds[ic];
        TH1D * waveShifted = (TH1D*) waves[ic]->Clone(TString(waves[ic]->GetName())+" shifted");
        //FIX here: Add calibration for the timing
        /*
          waveShifted->Reset();
          for (uint iBin = 1;iBin <= waves[ic]->GetNbinsX();iBin++)
            {
                float binLowEdgeShifted = waves[ic]->GetBinLowEdge(iBin) + timingCalibrations[ic];
                int iBinShifted = waveShifted->FindBin(binLowEdgeShifted + 1E-4);
                if (iBinShifted > 0 && iBinShifted <= waves[ic]->GetNbinsX()){
                    waveShifted->SetBinContent(iBinShifted,waves[ic]->GetBinContent(iBin));
                    waveShifted->SetBinError(iBinShifted,waves[ic]->GetBinError(iBin));
                }
                
            }
        for(uint iBoundVec =0;iBoundVec < bounds[ic].size();iBoundVec++){
        //Equivalent code needs modification here
            boundShifted[iBoundVec].second += timingCalibrations[ic]; 
            boundShifted[iBoundVec].first += timingCalibrations[ic]; 
            
        }
        */
        //FIX above if needed

        /*
          Obtain maximum and minimum heights as well as maximum and minimum times to
          shift the waveforms together on the same canvas
         */ 
        if(boundShifted.size()>0 || waveShifted->GetMaximum()>drawThresh){
            chanList.push_back(ic);
            //FIX here: Check for the run for beam state. By default set to on for now
            TString beamState = "on";
            waveShifted->SetTitle(Form("Run %i, File %i, Event %i;Calibrated Time [ns];Amplitude [mV];",runNumber,fileNumber,event));
            waveShifted->SetAxisRange(0,1024.*1.1/sampleRate);
            //Keep track of max amplitude
            if(waveShifted->GetMaximum()>maxheight) maxheight=waveShifted->GetMaximum();
            if(waveShifted->GetMinimum()<minheight) minheight=waveShifted->GetMinimum();
            
            if(boundShifted.size()>0){
                //keep track of earliest pulse start time
                //if(boundShifted[0].first<timeRange[0]) timeRange[0]=boundShifted[0].first;
                //keep track of latest pulse end time (pulses are ordered chronologicaly for each channel)
                //if(boundShifted[boundShifted.size()-1].second>timeRange[1]) timeRange[1]=boundShifted[boundShifted.size()-1].second;
                //In case the pulses are not time ordered in each channel
                if(boundShifted[ic].first<timeRange[0]) timeRange[0]=boundShifted[ic].first;
                if(boundShifted[ic].second>timeRange[1]) timeRange[1]=boundShifted[ic].second;
            }
        }
        wavesShifted.push_back(waveShifted);
        boundsShifted.push_back(boundShifted);
    } //channel loop

    //Check the top 10 channels
    for(uint ic=0;ic<index.size()-1;ic++){
        for(uint ic1=ic+1;ic1<index.size();ic1++){
            int dummy=-1;
            if(wavesShifted[index[ic]]->GetMaximum() < wavesShifted[index[ic1]]->GetMaximum()){
                dummy=index[ic];
                index[ic]=index[ic1];
                index[ic1]=dummy;
            }
        }
    }
    int maxheightbin = -1;
    maxheight*=1.1;
    if(minheight<0) minheight=minheight*1.1;
    else minheight=minheight*0.9;

    //maxheight=30;
    float rangeMaxX = timeRange[1];
    float rangeMinX = timeRange[0];
    float rangeMaxY = maxheight;
    float rangeMinY = minheight;

    // FIXME: This makes no sense if you just set the values to be equal
    if (rangeMaxY > -999) maxheight = rangeMaxY;

    if (rangeMinX < 0) timeRange[0]*=1.1;
    else timeRange[0] = rangeMinX*0.9;
    
    if (rangeMaxX < 0) timeRange[1]= min(0.9*timeRange[1],1024./sampleRate);
    else timeRange[1] = max(1.1*timeRange[1],1024./sampleRate);
    
    float depth = 0.075*chanList.size();
    TLegend leg(0.45,0.9-depth,0.65,0.9);
    for(uint i=0;i<chanList.size();i++){
        int ic = chanList[i];
        int chan = chanArray->GetAt(ic);
        originalMaxHeights[ic] = wavesShifted[ic]->GetMaximum();
        if (rangeMinY > -999) wavesShifted[ic]->SetMinimum(rangeMinY);
	wavesShifted[ic]->SetMaximum(maxheight);
	wavesShifted[ic]->SetAxisRange(timeRange[0],timeRange[1],"X");
        
        int column= chanMap[ic][0];
        int row= chanMap[ic][1];
        int layer= chanMap[ic][2];
        int type= chanMap[ic][3];
        int colorIndex = ic;
        if(ic>63) colorIndex=ic-64;
        h1cosmetic(wavesShifted[ic],colorIndex,colors);
        if(type==1) wavesShifted[ic]->SetLineStyle(3);
        if(type==2) wavesShifted[ic]->SetLineStyle(7);
        if(i==0) wavesShifted[ic]->Draw("hist");
	else wavesShifted[ic]->Draw("hist same");
        
        TLatex tlabelpeak;
        if(wavesShifted[ic]->GetMaximum()>50){
            tlabelpeak.SetTextSize(0.05);
            tlabelpeak.SetTextFont(42);
            tlabelpeak.DrawLatexNDC(wavesShifted[ic]->GetBinWidth(1)*wavesShifted[ic]->GetMaximumBin(),wavesShifted[ic]->GetMaximum()*1.1,Form("%i",ic));
        }
        
        leg.AddEntry(wavesShifted[ic],Form("Channel %i",ic),"l");
        wavesShifted[ic]->SetAxisRange(timeRange[0],timeRange[1],"X");
        //Show boundaries of pulse
        TLine line; line.SetLineWidth(2); line.SetLineStyle(3);line.SetLineColor(colors[colorIndex]);
        for(uint ip=0; ip<boundsShifted[ic].size();ip++){
            //cout<<timeRange[1]<<endl;    
            if (boundsShifted[ic][ip].first > timeRange[0] && boundsShifted[ic][ip].second < timeRange[1]){
                int draw_bounds = 0;
                for(int index_check=0; index_check<10;index_check++){ 
                    if(ic==index[index_check]) draw_bounds++;}
                if(draw_bounds>0){
                    line.DrawLine(boundsShifted[ic][ip].first,0,boundsShifted[ic][ip].first,0.2*maxheight);
                    line.DrawLine(boundsShifted[ic][ip].second,0,boundsShifted[ic][ip].second,0.2*maxheight);
                }
            }
        }
    } //channel loop close
     
    float boxw= 0.0438;
    float boxh=0.0438;
    float barw=0.017;
    float barh=0.017;
    //    float barw=0.017;
    //    float barh=0.017;
    //vector<float> xstart = {0.63,0.72,0.81,0.90};
    vector<float> xstart = {0.60,0.68,0.80,0.88};
    //vector<float> ystart= {0.798,0.851,0.904,0.957};
    vector<float> ystart= {0.79,0.824,0.858,0.8662};

    float sheet_width = 0.006;
    float sheet_offset= 0.013+sheet_width/2.;
    float sheet_left_to_right = 4*0.006+barw+boxw+0.002;
    vector<float> xstart_leftsheets = {xstart[0]-sheet_offset,xstart[1]-sheet_offset,xstart[2]-sheet_offset,xstart[3]-sheet_offset,xstart[3]+barw+boxw+0.009}; 
    vector<float> xstart_topsheets = {xstart[0]-0.002,xstart[1]-0.002,xstart[2]-0.002,xstart[3]-0.002,xstart[4]-0.002};
    float ystart_topsheets = ystart[2]+boxh+0.017;
    float ystart_sidesheets = ystart[0]-0.006;
    float vert_sheet_length = ystart[2]-ystart[0]+boxh+0.01;
    float hori_sheet_length= barw+boxw+0.004;
    float slab_width = 0.015;
    vector<float> slab_xstart = {xstart_leftsheets[0]-0.008-slab_width,xstart_leftsheets[1]-0.008-slab_width,xstart_leftsheets[2]-0.008-slab_width,xstart_leftsheets[3]-0.008-slab_width,xstart_leftsheets[3]+0.01+sheet_left_to_right}; 
    float slab_height = vert_sheet_length-0.02;
    float slab_ystart = ystart_sidesheets+0.01;

    TPave L1frame(xstart[0]-0.006,ystart[0]-0.01,xstart[0]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
    L1frame.SetFillColor(0);
    L1frame.SetLineWidth(2);
    L1frame.Draw();

    TPave L2frame(xstart[1]-0.006,ystart[0]-0.01,xstart[1]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
    L2frame.SetFillColor(0);
    L2frame.SetLineWidth(2);
    L2frame.Draw();

    TPave L3frame(xstart[2]-0.006,ystart[0]-0.01,xstart[2]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
    L3frame.SetFillColor(0);
    L3frame.SetLineWidth(2);
    L3frame.Draw();
    
    TPave L4frame(xstart[3]-0.006,ystart[0]-0.01,xstart[3]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
    L4frame.SetFillColor(0);
    L4frame.SetLineWidth(2);
    L4frame.Draw();
    
    TLatex tla;
    tla.SetTextSize(0.04);
    tla.SetTextFont(42);
    float height= 0.06;
    //tla.DrawLatexNDC(0.13,0.83,Form("Number of pulses: %i",(int)bounds.size()));
    float currentYpos=0.70;
    float headerX=0.67;
    float rowX=0.69;
    int pulseIndex=0; // Keep track of pulse index, since all pulses for all channels are actually stored in the same 1D vectors
    int maxPerChannel = 0;
    if (chanList.size() > 0) maxPerChannel = 10/chanList.size();
    
    for(uint i=0;i<chanList.size();i++){
        int ic = chanList[i];
        int chan = chanArray->GetAt(ic);
        //cout<<ic<<" ic,chan "<<chan<<endl;
        int column= chanMap[ic][0];
        int row= chanMap[ic][1];
        int layer= chanMap[ic][2];
        int type= chanMap[ic][3];

        int colorIndex=ic;
        if(ic>63) colorIndex=ic-64;
        
        TPave * pave;
        /*
        if (type==1){
            float xpos,ypos;
            ypos = slab_ystart;
            xpos = slab_xstart[layer];
            pave = new TPave(xpos,ypos,xpos+slab_width,ypos+slab_height,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            //pave->Draw();
        }

        cout<<"pave: i,ic,column,row,layer,type: Draw "<<i<<" "<<ic<<" "<<column<<" "<<row<<" "<<layer<<" "<<type<<" "<<colorIndex<<endl;
        if (type==2){
            float xpos,ypos;

            if (column!=0){
                xpos= xstart_leftsheets[layer-1];
                if(column>0) xpos += sheet_left_to_right;
                ypos = ystart_sidesheets;
                //pave = new TPave(xpos,ypos,xpos+sheet_width,ypos+vert_sheet_length,0,"NDC");
            }
            else{
                xpos = xstart_topsheets[layer-1];
                ypos = ystart_topsheets;
                //pave = new TPave(xpos,ypos,xpos+hori_sheet_length,ypos+1.4/0.8*sheet_width,0,"NDC");
            }

            pave->SetFillColor(colors[colorIndex]);
            //pave->Draw();

        }
        */
        if(type==0){
            //cout<<"Column="<<column<<" , Row="<<row<<" layer="<<layer<<" type="<<type<<" colorindex="<<colorIndex<<endl;
            float xpos = xstart[layer]+((column)*0.017)-0.002;
            float ypos = ystart[row]-0.005;
            if(row==3) ypos = ystart[row-1]+0.03;
            pave = new TPave(xpos,ypos,xpos+0.015,ypos+0.03,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        //Draw panels
        if(column==0 && row==0 && layer==-1 && type==1){
            pave = new TPave(xstart_leftsheets[0]-0.02,ystart_sidesheets-0.01,xstart_leftsheets[0]-0.02+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length)+0.01,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        if(column==0 && row==0 && layer==4 && type==1){
            pave = new TPave(xstart_leftsheets[4]+0.02,ystart_sidesheets-0.01,xstart_leftsheets[4]+0.02+(sheet_width*1.0),ystart_sidesheets+vert_sheet_length+0.01,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        if(column==0 && row==4 && layer==0 && type==2){
            pave = new TPave(xstart[0]-0.006,ystart[3]+boxh+0.015,xstart[1]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*2.0),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        if(column==0 && row==4 && layer==2 && type==2){
            pave = new TPave(xstart[2]-0.006,ystart[3]+boxh+0.015,xstart[3]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*2.0),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==-1 && row==0 && layer==2 && type==2){
            pave = new TPave(xstart[2]-0.02,ystart_sidesheets,xstart[2]-0.02+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
            
            /*Double_t xdraw[4] = {xstart[2]-0.04,xstart[2]-0.04+(sheet_width*1.0),xstart[2]-0.02,xstart[2]-0.02+(sheet_width*1.0)};
            Double_t ydraw[4] = {ystart_sidesheets,ystart_sidesheets,ystart_sidesheets+(vert_sheet_length),ystart_sidesheets+(vert_sheet_length)};
            TPolyLine *pline = new TPolyLine(4,xdraw,ydraw);
            pline->SetFillColor(colors[colorIndex]);
            pline->SetLineColor(colors[colorIndex]);
            pline->SetLineWidth(2);
            pline->Draw("f");
            pline->Draw();*/
            
        }
        
        if(column==4 && row==0 && layer==2 && type==2){
            pave = new TPave(xstart_leftsheets[4],ystart_sidesheets,xstart_leftsheets[4]+(sheet_width*1.0),ystart_sidesheets+vert_sheet_length,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==-1 && row==0 && layer==0 && type==2){
            pave = new TPave(xstart_leftsheets[0],ystart_sidesheets,xstart_leftsheets[0]+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==4 && row==0 && layer==0 && type==2){
            pave = new TPave(xstart[2]-0.05,ystart_sidesheets,xstart[2]-0.05+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        int draw_bounds = 0;
        for(int index_check=0; index_check<10;index_check++){ 
            if(ic==index[index_check]) draw_bounds++;}
        if(draw_bounds>0){
            tla.SetTextColor(colors[colorIndex]);
            tla.SetTextSize(0.04);
            //tla.DrawLatexNDC(headerX,currentYpos,Form("Channel %i, V_{max} = %0.0f, N_{pulses}= %i",ic,originalMaxHeights[ic],(int)boundsShifted[ic].size()));
        
            tla.DrawLatexNDC(headerX-0.05,currentYpos,Form("Channel %i, V_{max} = %0.0f, N_{pulses}= %i",ic,originalMaxHeights[ic],(int)boundsShifted[ic].size()));
            tla.SetTextColor(kBlack);
            currentYpos=currentYpos-(height*0.6);
            //currentYpos-=height;
            tla.SetTextSize(0.04);
            /*
            for(int ip=0;ip<boundsShifted[ic].size();ip++){
                TString row;
                row = Form("Channel number = %d",ip);
                pulseIndex++; 
                if(ip < maxPerChannel){
                    tla.DrawLatexNDC(rowX,currentYpos,row);
                    currentYpos-=height*1.0;
                }
            }
            */
            currentYpos-=height*0.35;
        } //added
    } //channel loop closed
    
    //cout<<"Display directory is "<<displayDirectory<<endl;
    TString displayName;
    displayName=TString(Form(displayDirectory+"Run%i_File%i_Event%i_Version_",runNumber,fileNumber,event))+TString("shorttagplaceholder_")+appendToTag+".pdf"; 
    c.SaveAs(displayName);
    displayName=TString(Form(displayDirectory+"Run%i_File%i_Event%i_Version_",runNumber,fileNumber,event))+TString("shorttagplaceholder_")+appendToTag+".png"; 
    c.SaveAs(displayName);

    for(uint i=0;i<chanList.size();i++){
        delete wavesShifted[i];
    }
    
}

void OfflineFactory::displaychannelEvent(int event, vector<vector<pair<float,float> > >& bounds,TString displayDirectory){
    
    vector<int> chanList;
    float maxheight=0; float minheight=0;
    float timeRange[2];
    timeRange[1]=1024./sampleRate; timeRange[0]=0.;
    //Get the waves
    vector<vector<pair<float,float>>> boundsShifted;
    vector<TH1D*> wavesShifted;
    vector<int> index;
    float originalMaxHeights[80];
    float drawThresh=0;
        
    for(uint ic=0;ic<bounds.size();ic++){
        int chan = chanArray->GetAt(ic);
        index.push_back(ic);
        vector<pair<float,float>> boundShifted = bounds[ic];
        TH1D * waveShifted = (TH1D*) waves[ic]->Clone(TString(waves[ic]->GetName())+" shifted");
    
        if(boundShifted.size()>0 || waveShifted->GetMaximum()>drawThresh){
            chanList.push_back(ic);
            //FIX here: Check for the run for beam state. By default set to on for now
            TString beamState = "on";
            waveShifted->SetTitle(Form("Run %i, File %i, Event %i, Channel %i;Calibrated Time [ns];Amplitude [mV];",runNumber,fileNumber,event,ic));
	    waveShifted->SetAxisRange(0,1024.*1.1/sampleRate);
	    //Keep track of max amplitude
            if(waveShifted->GetMaximum()>maxheight) maxheight=waveShifted->GetMaximum();
            if(waveShifted->GetMinimum()<minheight) minheight=waveShifted->GetMinimum();
            
            if(boundShifted.size()>0){
                if(boundShifted[ic].first<timeRange[0]) timeRange[0]=boundShifted[ic].first;
                if(boundShifted[ic].second>timeRange[1]) timeRange[1]=boundShifted[ic].second;
            }
        }
        wavesShifted.push_back(waveShifted);
        boundsShifted.push_back(boundShifted);
    } //channel loop

    int maxheightbin = -1;
    maxheight*=1.1;
    if(minheight<0) minheight=minheight*1.1;
    else minheight=minheight*0.9;

    //maxheight=30;
    float rangeMaxX = timeRange[1];
    float rangeMinX = timeRange[0];
    float rangeMaxY = maxheight;
    float rangeMinY = minheight;
    
    if (rangeMaxY > -999) maxheight = rangeMaxY;

    if (rangeMinX < 0) timeRange[0]*=1.1;
    else timeRange[0] = rangeMinX*0.9;
    
    if (rangeMaxX < 0) timeRange[1]= min(0.9*timeRange[1],1024./sampleRate);
    else timeRange[1] = max(1.1*timeRange[1],1024./sampleRate);
    
    float depth = 0.075*chanList.size();
    TLegend leg(0.45,0.9-depth,0.65,0.9);
    /*
    for(uint i=0;i<chanList.size();i++){
        int ic = chanList[i];
        int chan = chanArray->GetAt(ic);
        originalMaxHeights[ic] = wavesShifted[ic]->GetMaximum();
        if (rangeMinY > -999) wavesShifted[ic]->SetMinimum(rangeMinY);
        wavesShifted[ic]->SetMaximum(maxheight);
        wavesShifted[ic]->SetAxisRange(timeRange[0],timeRange[1],"X");
        int column= chanMap[ic][0]; int row= chanMap[ic][1]; int layer= chanMap[ic][2]; int type= chanMap[ic][3]; int colorIndex = ic;
        if(ic>63) colorIndex=ic-64;
        h1cosmetic(wavesShifted[ic],colorIndex,colors); if(type==1) wavesShifted[ic]->SetLineStyle(3); if(type==2) wavesShifted[ic]->SetLineStyle(7);
        wavesShifted[ic]->Draw("hist");
        leg.AddEntry(wavesShifted[ic],Form("Channel %i",ic),"l");
        wavesShifted[ic]->SetAxisRange(timeRange[0],timeRange[1],"X");
        TLine line; line.SetLineWidth(2); line.SetLineStyle(3);line.SetLineColor(colors[colorIndex]);
        for(uint ip=0; ip<boundsShifted[ic].size();ip++){
            if (boundsShifted[ic][ip].first > timeRange[0] && boundsShifted[ic][ip].second < timeRange[1]){
                    line.DrawLine(boundsShifted[ic][ip].first,0,boundsShifted[ic][ip].first,0.2*maxheight);
                    line.DrawLine(boundsShifted[ic][ip].second,0,boundsShifted[ic][ip].second,0.2*maxheight);
            }    
        }
    } //channel loop close
    */
    
    for(uint i=0;i<chanList.size();i++){
        TCanvas c("c1","",1400,800);
        gPad->SetRightMargin(0.45);
        gStyle->SetGridStyle(3);
        gStyle->SetGridColor(13);
        c.SetGrid();
        
        gStyle->SetTitleX(0.35);
    
        float boxw= 0.0438;
        float boxh=0.0438;
        float barw=0.017;
        float barh=0.017;
        vector<float> xstart = {0.60,0.68,0.80,0.88};
        vector<float> ystart= {0.79,0.824,0.858,0.8662};

        float sheet_width = 0.006;
        float sheet_offset= 0.013+sheet_width/2.;
        float sheet_left_to_right = 4*0.006+barw+boxw+0.002;
        vector<float> xstart_leftsheets = {xstart[0]-sheet_offset,xstart[1]-sheet_offset,xstart[2]-sheet_offset,xstart[3]-sheet_offset,xstart[3]+barw+boxw+0.009}; 
        vector<float> xstart_topsheets = {xstart[0]-0.002,xstart[1]-0.002,xstart[2]-0.002,xstart[3]-0.002,xstart[4]-0.002};
        float ystart_topsheets = ystart[2]+boxh+0.017;
        float ystart_sidesheets = ystart[0]-0.006;
        float vert_sheet_length = ystart[2]-ystart[0]+boxh+0.01;
        float hori_sheet_length= barw+boxw+0.004;
        float slab_width = 0.015;
        vector<float> slab_xstart = {xstart_leftsheets[0]-0.008-slab_width,xstart_leftsheets[1]-0.008-slab_width,xstart_leftsheets[2]-0.008-slab_width,xstart_leftsheets[3]-0.008-slab_width,xstart_leftsheets[3]+0.01+sheet_left_to_right}; 
        float slab_height = vert_sheet_length-0.02;
        float slab_ystart = ystart_sidesheets+0.01;

    
        TLatex tla;
        tla.SetTextSize(0.04);
        tla.SetTextFont(42);
        float height= 0.06;
        //tla.DrawLatexNDC(0.13,0.83,Form("Number of pulses: %i",(int)bounds.size()));
        float currentYpos=0.70;
        float headerX=0.67;
        float rowX=0.69;
        int pulseIndex=0; // Keep track of pulse index, since all pulses for all channels are actually stored in the same 1D vectors
        int maxPerChannel = 0;
        if (chanList.size() > 0) maxPerChannel = 10/chanList.size();
    
    
        float drawThresh=15;
        int ic = chanList[i];
        int chan = chanArray->GetAt(ic);
        int column= chanMap[ic][0];
        int row= chanMap[ic][1];
        int layer= chanMap[ic][2];
        int type= chanMap[ic][3];

        int colorIndex=ic;
        if(ic>63) colorIndex=ic-64;
        
        
        TPave * pave;
        /*
        if (type==1){
            float xpos,ypos;
            ypos = slab_ystart;
            xpos = slab_xstart[layer];
            pave = new TPave(xpos,ypos,xpos+slab_width,ypos+slab_height,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            //pave->Draw();
        }

        cout<<"pave: i,ic,column,row,layer,type: Draw "<<i<<" "<<ic<<" "<<column<<" "<<row<<" "<<layer<<" "<<type<<" "<<colorIndex<<endl;
        if (type==2){
            float xpos,ypos;

            if (column!=0){
                xpos= xstart_leftsheets[layer-1];
                if(column>0) xpos += sheet_left_to_right;
                ypos = ystart_sidesheets;
                //pave = new TPave(xpos,ypos,xpos+sheet_width,ypos+vert_sheet_length,0,"NDC");
            }
            else{
                xpos = xstart_topsheets[layer-1];
                ypos = ystart_topsheets;
                //pave = new TPave(xpos,ypos,xpos+hori_sheet_length,ypos+1.4/0.8*sheet_width,0,"NDC");
            }

            pave->SetFillColor(colors[colorIndex]);
            //pave->Draw();

        }
        */
        
        if(wavesShifted[ic]->GetMaximum()<=drawThresh) continue;
        
        originalMaxHeights[ic] = wavesShifted[ic]->GetMaximum();
        if (rangeMinY > -999) wavesShifted[ic]->SetMinimum(wavesShifted[ic]->GetMinimum()*0.9);
        wavesShifted[ic]->SetMaximum(wavesShifted[ic]->GetMaximum()*1.1);
        wavesShifted[ic]->SetAxisRange(timeRange[0],timeRange[1],"X");
        //int column= chanMap[ic][0]; int row= chanMap[ic][1]; int layer= chanMap[ic][2]; int type= chanMap[ic][3]; int colorIndex = ic;
        if(ic>63) colorIndex=ic-64;
        h1cosmetic(wavesShifted[ic],colorIndex,colors); if(type==1) wavesShifted[ic]->SetLineStyle(3); if(type==2) wavesShifted[ic]->SetLineStyle(7);
        wavesShifted[ic]->Draw("hist");
        leg.AddEntry(wavesShifted[ic],Form("Channel %i",ic),"l");
        wavesShifted[ic]->SetAxisRange(timeRange[0],timeRange[1],"X");
        TLine line; line.SetLineWidth(2); line.SetLineStyle(3);line.SetLineColor(colors[colorIndex]);
        
        TPave L1frame(xstart[0]-0.006,ystart[0]-0.01,xstart[0]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
        L1frame.SetFillColorAlpha(0,1.0);
        L1frame.SetLineWidth(2);
        L1frame.SetLineColor(1);
        L1frame.Draw();
        
        TPave L2frame(xstart[1]-0.006,ystart[0]-0.01,xstart[1]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
        L2frame.SetFillColorAlpha(0,1.0);
        L2frame.SetLineWidth(2);
        L2frame.SetLineColor(1);
        L2frame.Draw();
        
        TPave L3frame(xstart[2]-0.006,ystart[0]-0.01,xstart[2]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
        L3frame.SetFillColorAlpha(0,1.0);
        L3frame.SetLineWidth(2);
        L3frame.SetLineColor(1);
        L3frame.Draw();
        
        TPave L4frame(xstart[3]-0.006,ystart[0]-0.01,xstart[3]+barw+boxw+0.006,ystart[3]+boxh+0.01,1,"NDC");
        L4frame.SetFillColorAlpha(0,1.0);
        L4frame.SetLineWidth(2);
        L4frame.SetLineColor(1);
        L4frame.Draw();
        

        

        /*r(uint ip=0; ip<boundsShifted[ic].size();ip++){
      if (boundsShifted[ic][ip].first > timeRange[0] && boundsShifted[ic][ip].second < timeRange[1]){
      line.DrawLine(boundsShifted[ic][ip].first,0,boundsShifted[ic][ip].first,0.2*maxheight);
      line.DrawLine(boundsShifted[ic][ip].second,0,boundsShifted[ic][ip].second,0.2*maxheight);
      }    
      }*/
        
        if(type==0){
            float xpos = xstart[layer]+((column)*0.017)-0.002;
            float ypos = ystart[row]-0.005;
            if(row==3) ypos = ystart[row-1]+0.03;
            pave = new TPave(xpos,ypos,xpos+0.015,ypos+0.03,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        //Draw panels
        if(column==0 && row==0 && layer==-1 && type==1){
            pave = new TPave(xstart_leftsheets[0]-0.02,ystart_sidesheets-0.01,xstart_leftsheets[0]-0.02+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length)+0.01,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        if(column==0 && row==0 && layer==4 && type==1){
            pave = new TPave(xstart_leftsheets[4]+0.02,ystart_sidesheets-0.01,xstart_leftsheets[4]+0.02+(sheet_width*1.0),ystart_sidesheets+vert_sheet_length+0.01,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        if(column==0 && row==4 && layer==0 && type==2){
            pave = new TPave(xstart[0]-0.006,ystart[3]+boxh+0.015,xstart[1]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*2.0),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        if(column==0 && row==4 && layer==2 && type==2){
            pave = new TPave(xstart[2]-0.006,ystart[3]+boxh+0.015,xstart[3]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*2.0),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==-1 && row==0 && layer==2 && type==2){
            pave = new TPave(xstart[2]-0.02,ystart_sidesheets,xstart[2]-0.02+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
            
            /*Double_t xdraw[4] = {xstart[2]-0.04,xstart[2]-0.04+(sheet_width*1.0),xstart[2]-0.02,xstart[2]-0.02+(sheet_width*1.0)};
            Double_t ydraw[4] = {ystart_sidesheets,ystart_sidesheets,ystart_sidesheets+(vert_sheet_length),ystart_sidesheets+(vert_sheet_length)};
            TPolyLine *pline = new TPolyLine(4,xdraw,ydraw);
            pline->SetFillColor(colors[colorIndex]);
            pline->SetLineColor(colors[colorIndex]);
            pline->SetLineWidth(2);
            pline->Draw("f");
            pline->Draw();*/
            
        }
        
        if(column==4 && row==0 && layer==2 && type==2){
            pave = new TPave(xstart_leftsheets[4],ystart_sidesheets,xstart_leftsheets[4]+(sheet_width*1.0),ystart_sidesheets+vert_sheet_length,0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==-1 && row==0 && layer==0 && type==2){
            pave = new TPave(xstart_leftsheets[0],ystart_sidesheets,xstart_leftsheets[0]+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==4 && row==0 && layer==0 && type==2){
            pave = new TPave(xstart[2]-0.05,ystart_sidesheets,xstart[2]-0.05+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }

        
        
        tla.SetTextColor(colors[colorIndex]);
        tla.SetTextSize(0.04);
        //tla.DrawLatexNDC(headerX,currentYpos,Form("Channel %i, V_{max} = %0.0f, N_{pulses}= %i",ic,originalMaxHeights[ic],(int)boundsShifted[ic].size()));
        
        tla.DrawLatexNDC(headerX-0.05,currentYpos,Form("Channel %i, V_{max} = %0.0f, N_{pulses}= %i",ic,originalMaxHeights[ic],(int)boundsShifted[ic].size()));
        tla.SetTextColor(kBlack);
        currentYpos=currentYpos-(height*0.6);
        //currentYpos-=height;
        tla.SetTextSize(0.04);
        
        for(int ip=0;ip<boundsShifted[ic].size();ip++){
            TString row;
            row = Form("Channel number = %d",ip);
            pulseIndex++; 
            if(ip < maxPerChannel){
                tla.DrawLatexNDC(rowX,currentYpos,row);
                currentYpos-=height*1.0;
            }
        }
        
        currentYpos-=height*0.35;
        //added
        //channel loop closed
    
        TString displayName;
        displayName=Form(displayDirectory+"Run%i_File%i_Event%i_Version_%s_channel_%i.pdf",runNumber,fileNumber,event,"shorttagplaceholder",ic); 
        c.SaveAs(displayName);
        displayName=Form(displayDirectory+"Run%i_File%i_Event%i_Version_%s_channel_%i.png",runNumber,fileNumber,event,"shorttagplaceholder",ic); 
        c.SaveAs(displayName);
    
    
    }
    for(uint i=0;i<chanList.size();i++){
        delete wavesShifted[i];
    }
    
}

vector<vector<pair<float,float>>> OfflineFactory::readWaveDataPerEvent(int i){

    inTree->GetEntry(i);
    if ( i % 1000 == 0) clog << "Processing event " << i << endl;
    if (isSim){
        outputTreeContents.eventWeight = eventWeight;
    }
    if (!isDRS) {
        //Read timing information
        if(initSecs<0){ //if timestamps for first event are uninitialized
            if(evt->digitizers[0].DataPresent){ //If this event exists
                initSecs=evt->digitizers[0].DAQTimeStamp.GetSec();
                initTDC=evt->digitizers[0].TDC[0];
                prevTDC=initTDC;
            }
        }
        Long64_t thisTDC;
        if(evt->digitizers[0].DataPresent) thisTDC = evt->digitizers[0].TDC[0];
        else thisTDC=prevTDC;

        //Check if rollover has happened since last event: if previous time is more than 10 minutes later than current time 
        //NB events are not written strictly in chronological order
        //TODO this is not perfect because events can come out of order occasionally
        Long64_t diff = prevTDC - thisTDC;
        if(diff > 1.2e+11) nRollOvers++;
        //For each tDC rollover: add max value: pow(2,40)
        outputTreeContents.event_time_fromTDC = 5.0e-9*(thisTDC+nRollOvers*pow(2,40)-initTDC)+initSecs;
        // outputTreeContents.event_t_string = TTimeStamp(outputTreeContents.event_time_fromTDC).AsString("s");
        //update previous TDC holder for next event
        prevTDC = thisTDC;
        if (!isSim){
            for (int ib =0; ib < numBoards; ib++){

                int secs = evt->digitizers[ib].DAQTimeStamp.GetSec();
                //This defines the time in seconds in standard unix epoch since 1970
                outputTreeContents.event_time.push_back(secs);

                outputTreeContents.event_trigger_time_tag.push_back(evt->digitizers[ib].TriggerTimeTag);
                //
                //event_t_string = evt->digitizers[0].DAQTimeStamp.AsString("s");
                //
                // Can probably uncomment this bit once all groups connected?
                outputTreeContents.v_groupTDC_g0.push_back(evt->digitizers[ib].TDC[0]);
                outputTreeContents.v_groupTDC_g1.push_back(evt->digitizers[ib].TDC[1]);
                outputTreeContents.v_groupTDC_g2.push_back(evt->digitizers[ib].TDC[2]);
                outputTreeContents.v_groupTDC_g3.push_back(evt->digitizers[ib].TDC[3]);
                outputTreeContents.v_groupTDC_g4.push_back(evt->digitizers[ib].TDC[4]);
                outputTreeContents.v_groupTDC_g5.push_back(evt->digitizers[ib].TDC[5]);
                outputTreeContents.v_groupTDC_g6.push_back(evt->digitizers[ib].TDC[6]);
                outputTreeContents.v_groupTDC_g7.push_back(evt->digitizers[ib].TDC[7]);

                outputTreeContents.present.push_back(evt->digitizers[ib].DataPresent);
            }
        }
        loadWavesMilliDAQ();
    }
    else loadWavesDRS();
    //Loop over channels
    vector<vector<pair<float,float> > > allPulseBounds;
    outputTreeContents.boardsMatched = true;
    if(!isSim){
        for(int idig=0; idig < nDigitizers; idig++){

            //correct all pulses to the TDC time of digitizer 0
            float thisCorrection = (float)5*((int64_t)evt->digitizers[idig].TDC[0] - (int64_t)evt->digitizers[0].TDC[0]);
            tdcCorrection[idig] = thisCorrection; //5ns per TDC clock
            if(evt->digitizers[idig].TDC[0] == 0) {
                outputTreeContents.boardsMatched = false;
            }

        }
        //if boards are not matched don't overcorrect times (will throw out these events offline anyway)
        if (outputTreeContents.boardsMatched == false) {
            for(int i=0; i < sizeof(tdcCorrection)/sizeof(tdcCorrection[0]); i++){
                tdcCorrection[i] = 0;
            }
        }
    }
    totalPulseCount = 0;
    for(int ic=0;ic<numChan;ic++){
        //Pulse finding
        allPulseBounds.push_back(processChannel(ic));
    }   

    outputTreeContents.DAQEventNumber = evt->DAQEventNumber;
    return allPulseBounds;
}
    

void OfflineFactory::displayEvents(std::vector<int> & eventsToDisplay,TString displayDirectory){
    validateInput();
    inTree = (TTree*)inFile->Get("Events"); 
    loadBranches();
    //Display directory
    //argv, argv + argc,
    TString displayDirectoryForRun = displayDirectory+"/Run"+to_string(runNumber)+"/";
    gSystem->mkdir(displayDirectoryForRun,true);
    TString displayDirectoryForRun1 = displayDirectory+"/Run"+to_string(runNumber)+"allchannels100events/";
    gSystem->mkdir(displayDirectoryForRun1,true);
    for(auto iEvent: eventsToDisplay){
        resetOutBranches();
        vector<vector<pair<float,float> > > allPulseBounds;
        allPulseBounds = readWaveDataPerEvent(iEvent);
        displayEvent(iEvent,allPulseBounds,displayDirectoryForRun);
        //displaychannelEvent(iEvent,allPulseBounds,displayDirectoryForRun1);
    }
    inFile->Close();
}
//Pulse finding and per channel processing
void OfflineFactory::readWaveData(){
    validateInput();
    inTree = (TTree*)inFile->Get("Events"); 
    if (inTree->GetEntries() == 0){
        throw runtime_error("There are no entries in this tree... exiting");
    }
    triggerFileMatched = false;
    if (friendFileName != "") {
	  addFriendTree();
	  triggerFileMatched = true;
    }
    loadBranches();
    // int maxEvents = 1;
    int maxEvents = inTree->GetEntries();
    cout<<"Processing "<<maxEvents<<" events in this file"<<endl;
    bool showBar = false;

    for(int i=0;i<maxEvents;i++){

        //for(int i=825;i<826;i++){
        //cout<<"------------- Event="<<i<<"  -----------------"<<endl;
        resetOutBranches();
        //Process each event
        vector<vector<pair<float,float> > > allPulseBounds;
        outputTreeContents.event=i;
        allPulseBounds = readWaveDataPerEvent(i);
        outputTreeContents.tClockCycles = tClockCycles;
        outputTreeContents.tTime = tTime;
        outputTreeContents.tStartTime = tStartTime;
        outputTreeContents.tTrigger = tTrigger;
        outputTreeContents.tTimeDiff = tTimeDiff;
        outputTreeContents.tMatchingTimeCut = tMatchingTimeCut;
        outputTreeContents.tEvtNum = tEvtNum;
        outputTreeContents.tRunNum = tRunNum;
        outputTreeContents.tTBEvent = tTBEvent;
        findExtrema();

        if (!isSlab && !isSim){ //temporary while slab has no lumi/good runs
            getEventLumis();
            setGoodRuns();
        } 

        if (outputTreeContents.event_time_fromTDC < firstTDC_time) firstTDC_time = outputTreeContents.event_time_fromTDC; 
        if (outputTreeContents.event_time_fromTDC > lastTDC_time) lastTDC_time = outputTreeContents.event_time_fromTDC;

        outTree->Fill();
        //Totally necessary progress bar
        float progress = 1.0*i/maxEvents; 
        if (showBar){
            int barWidth = 70;
            std::cout << "[";
            int pos = barWidth * progress;
            for (int i = 0; i < barWidth; ++i) {
                if (i < pos) std::cout << "=";
                else if (i == pos) std::cout << ">";
                else std::cout << " ";
            }
            std::cout << "] " << round(progress * 100.0) << " %\r";
            std::cout.flush();
        }
        
    }

    setTotalLumi();
    
}

void OfflineFactory::writeOutputTree(){
    outFile->cd();
    outTree->Write();
    if (writeTriggerMetaData) trigMetaDataCopy->Write();
    writeVersion();
    outFile->Close();
    if (inFile) inFile->Close();
}
void OfflineFactory::prepareWave(int ic){
    TAxis * a = waves[ic]->GetXaxis();
    // a->Set( a->GetNbins(), a->GetXmin()/sampleRate, a->GetXmax()/sampleRate);
    // waves[ic]->ResetStats();

    //Measure the sideband before corrections
    pair<float,float> mean_rms_raw = measureSideband(ic);
    outputTreeContents.v_sideband_mean_raw.push_back(mean_rms_raw.first);
    outputTreeContents.v_sideband_RMS_raw.push_back(mean_rms_raw.second);

    //subtract calibrated mean
    for(int ibin = 1; ibin <= waves[ic]->GetNbinsX(); ibin++){
        waves[ic]->SetBinContent(ibin,waves[ic]->GetBinContent(ibin)-pedestals[ic]);        
    }

    //Get dynamical pedestal per channel in a particular event
    double pedestal_mV = 0.0; //Final pedestal correction to be applied
    float rms_variation_max = 4.0;
    float pedestal_variation_max = 80.0;
    TH1D * histTemp = new TH1D("temp","temp",1+int(pedestal_variation_max/dynamicPedestalGranularity+1E-3)*2,-pedestal_variation_max-dynamicPedestalGranularity/2,pedestal_variation_max+dynamicPedestalGranularity/2);
    //Iteratively check if the variation in amplitude is less than 4 mV within 16 consecutive samples. Use only first 1000ns (400 samples) to avoid trigger.
    for(int ibin = 1; ibin <= dynamicPedestalTotalSamples; ibin+=dynamicPedestalConsecutiveSamples){
        double checkheightvariation=0, rms_variation=0.0;
        for( int jbin=ibin;jbin<ibin+dynamicPedestalConsecutiveSamples;jbin++){
            checkheightvariation+=waves[ic]->GetBinContent(jbin);
        }
        for( int jbin=ibin;jbin<ibin+dynamicPedestalConsecutiveSamples;jbin++){
            rms_variation+=pow(waves[ic]->GetBinContent(jbin)- (checkheightvariation/dynamicPedestalConsecutiveSamples),2.0);
        }
        
        rms_variation=fabs(sqrt(rms_variation/dynamicPedestalConsecutiveSamples));
        if( (fabs(checkheightvariation/dynamicPedestalConsecutiveSamples)<pedestal_variation_max) && rms_variation <  rms_variation_max){
            float baselineRound = round((checkheightvariation/dynamicPedestalConsecutiveSamples)/dynamicPedestalGranularity)*dynamicPedestalGranularity;
            histTemp->Fill(baselineRound);
        }
    }
    //Calculate most probable value of the pedestal correction
    if (histTemp->GetEntries()) pedestal_mV = histTemp->GetBinCenter(histTemp->GetMaximumBin());
    delete histTemp;
    
    //Correct the waveform after applying the dynamic pedestal correction
    for(int ibin = 1; ibin <= waves[ic]->GetNbinsX(); ibin++){
        waves[ic]->SetBinContent(ibin,waves[ic]->GetBinContent(ibin)-pedestal_mV);        
    }

    //Need to add sideband measurements and subtraction here
    pair<float,float> mean_rms = measureSideband(ic);
    outputTreeContents.v_dynamicPedestal.push_back(pedestal_mV);
    outputTreeContents.v_sideband_mean.push_back(mean_rms.first);
    outputTreeContents.v_sideband_RMS.push_back(mean_rms.second);
}
//Measure mean and RMS of samples in range from start to end (in ns)
pair<float,float> OfflineFactory::measureSideband(int ic){

    float sum_sb=0.;
    float sum2_sb=0.;
    int startbin = waves[ic]->FindBin(sideband_range[0]);
    int endbin = waves[ic]->FindBin(sideband_range[1]);
    int n_sb = 0;
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
vector< pair<float,float> > OfflineFactory::findPulses(int ic){
    vector<pair<float,float> > bounds;
    float tstart = sideband_range[1]+1;
    int istart = waves[ic]->FindBin(tstart);
    // int istart = 1;
    bool inpulse = false;
    int nover = 0;
    int nunder = 0;
    int i_begin = istart;
    //int i_begin = 0;
    int i_stop_searching = waves[ic]->GetNbinsX()-nConsecSamples[ic];
    int i_stop_final_pulse = waves[ic]->GetNbinsX();
    for (int i=istart; i<i_stop_searching || (inpulse && i<i_stop_final_pulse); i++) {
        float v = waves[ic]->GetBinContent(i);

        if (!inpulse) {
            if (v<lowThresh[ic]) {   
                nover = 0;     // If v dips below the low threshold, store the value of the sample index as i_begin
                i_begin = i;
            }
            else if (v>=highThresh[ic]){
                nover++;       // If v is above the threshold, start counting the number of sample indices
            }
            else{
                i_begin = i;
            }
            if (nover>=nConsecSamples[ic]){   // If v is above threshold for long enough, we now have a pulse!
                inpulse = true;    // Also reset the value of nunder
                nunder = 0;
            }
        }
        else {  // Called if we have a pulse
            if (v<highThresh[ic]) nunder++;   // If the pulse dips below the threshold, sum the number of sample indices for which this is true
            else if (v >= highThresh[ic]){
                nunder = 0;           // If the pulse stays above threshold, set nunder back to zero
            }
            // If the nunder is above or equal to 12 (or we reach the end of the file) store the values of the pulse bounds
            if (nunder>=nConsecSamplesEnd[ic] || i==(i_stop_final_pulse-1)) { 
                bounds.push_back({(float)waves[ic]->GetBinLowEdge(i_begin), (float)waves[ic]->GetBinLowEdge(i+1)-0.01});
                inpulse = false;
                nover = 0;
                nunder = 0;
                i_begin = i;
            }
        }
    }
    return bounds;
}
//Pulse finding and per channel processing
vector< pair<float,float> > OfflineFactory::processChannel(int ic){
  prepareWave(ic); 
    //Pulse finding
    vector<pair<float,float>> pulseBounds = findPulses(ic);
    int npulses = pulseBounds.size();

    //Useful variable for defining pulses
    float maxThreeConsec = -100;
    for (int iBin = 1; iBin < waves[ic]->GetNbinsX(); iBin++){
        float maxList[] = {waves[ic]->GetBinContent(iBin),waves[ic]->GetBinContent(iBin+1),waves[ic]->GetBinContent(iBin+2)};
        float tempMax = *std::min_element(maxList,maxList+3);
        if (maxThreeConsec < tempMax) maxThreeConsec = tempMax;

    }
    outputTreeContents.v_max.push_back(waves[ic]->GetMaximum());
    outputTreeContents.v_maxPulseTime.push_back(waves[ic]->GetBinLowEdge(waves[ic]->GetMaximumBin()));
    outputTreeContents.v_max_threeConsec.push_back(maxThreeConsec);
    //FIXME Need to add low pass filter option back
    outputTreeContents.v_max_afterFilter.push_back(waves[ic]->GetMaximum());
    outputTreeContents.v_min_afterFilter.push_back(waves[ic]->GetMinimum());
    
    for(int ipulse = 0; ipulse<npulses; ipulse++){
        std::pair<float, float> prePulse = getPrePulseVar(waves[ic], pulseBounds[ipulse].first);
        outputTreeContents.v_prePulseMean.push_back(prePulse.first);
        outputTreeContents.v_prePulseRMS.push_back(prePulse.second);
        waves[ic]->SetAxisRange(pulseBounds[ipulse].first,pulseBounds[ipulse].second);
        if (chanMap.size() > 0 and ic < chanMap.size()){
            outputTreeContents.v_column.push_back(chanMap[ic][0]);
            outputTreeContents.v_row.push_back(chanMap[ic][1]);
            outputTreeContents.v_layer.push_back(chanMap[ic][2]);
            outputTreeContents.v_type.push_back(chanMap[ic][3]);
        }
        else{
            outputTreeContents.v_column.push_back(0);
            outputTreeContents.v_row.push_back(0);
            outputTreeContents.v_layer.push_back(0);
            outputTreeContents.v_type.push_back(0);
        }

        //FIXME need to add calibrations (when available)
        outputTreeContents.v_chanWithinBoard.push_back(chanArray->GetAt(ic));
        outputTreeContents.v_chan.push_back(ic);
        outputTreeContents.v_board.push_back(boardArray->GetAt(ic));
        float height = waves[ic]->GetMaximum();
        outputTreeContents.v_height.push_back(height);
        int above20 = -2;
        int above80 = -1;
        float meanX = 0;
        float meanY = 0;
        for (int iStart = waves[ic]->FindBin(pulseBounds[ipulse].first); iStart <= waves[ic]->FindBin(pulseBounds[ipulse].second); iStart++){
            if (waves[ic]->GetBinContent(iStart) > height*0.2 && above20 < 0){
                above20 = iStart;
            }
            if (above20 >=0){
                meanX += waves[ic]->GetBinLowEdge(iStart);
                meanY += waves[ic]->GetBinContent(iStart);
            }
            if (waves[ic]->GetBinContent(iStart) > height*0.8 && above80 < 0){
                above80 = iStart;
            }
            if (above80 >= 0) break;
        }
        int riseSamples = above80-above20;
        float gradNum = 0;
        float gradDenom = 0;
        float timeFit = -1;
        if (riseSamples > 0){
            meanX /= riseSamples+1;
            meanY /= riseSamples+1;
            for (int iStart = above20; iStart < above80; iStart++){
                gradNum += (waves[ic]->GetBinLowEdge(iStart)-meanX)*(waves[ic]->GetBinContent(iStart)-meanY);
                gradDenom += (waves[ic]->GetBinLowEdge(iStart)-meanX)*(waves[ic]->GetBinLowEdge(iStart)-meanX);
            }
            float grad = gradNum/gradDenom;
            float intercept = meanY-grad*meanX;
            timeFit = -intercept/grad;
        }
        outputTreeContents.v_riseSamples.push_back(above80-above20);
        above20 = -2;
        above80 = -1;
        if (timeFit < 0) timeFit = pulseBounds[ipulse].first;

        for (int iFall = waves[ic]->FindBin(pulseBounds[ipulse].second); iFall >= waves[ic]->FindBin(pulseBounds[ipulse].first); iFall--){
            if (waves[ic]->GetBinContent(iFall) > height*0.2 && above20 < 0){
                above20 = iFall;
            }
            if (waves[ic]->GetBinContent(iFall) > height*0.8 && above80 < 0){
                above80 = iFall;
            }
            if (above80 >= 0) break;
        }
        int fallSamples = above20-above80;
        outputTreeContents.v_fallSamples.push_back(above20-above80);
        outputTreeContents.v_time.push_back(pulseBounds[ipulse].first);
        outputTreeContents.v_timeFit.push_back(timeFit);
        outputTreeContents.v_time_module_calibrated.push_back(pulseBounds[ipulse].first+timingCalibrations[ic]+tdcCorrection[ic/16]);
        outputTreeContents.v_timeFit_module_calibrated.push_back(timeFit+timingCalibrations[ic]+tdcCorrection[ic/16]);
        float area = waves[ic]->Integral("width");
        outputTreeContents.v_area.push_back(area);


        outputTreeContents.v_nPE.push_back((waves[ic]->Integral("width")/(speAreas[ic]))*(0.4/sampleRate));
        outputTreeContents.v_ipulse.push_back(ipulse);
        outputTreeContents.v_npulses.push_back(npulses);
        outputTreeContents.v_pulseIndex.push_back(totalPulseCount+ipulse);
        float duration = pulseBounds[ipulse].second - pulseBounds[ipulse].first;
        outputTreeContents.v_duration.push_back(duration);
        if(ipulse>0) outputTreeContents.v_delay.push_back(pulseBounds[ipulse].first - pulseBounds[ipulse-1].second);
        else outputTreeContents.v_delay.push_back(9999.);
        bool qual = true;
        if (fallSamples < 2) qual=false;
        if (qual && riseSamples < 2) qual=false;
        if (qual && (height > 17. && height<100.) && (0.001*area < 0.04*(height-17.))) qual=false;
        if (qual && height < 25. && duration < 4.6*(height-12.)) qual=false;
        if (qual && height >= 25. && duration < 60. && fallSamples < 6) qual=false;
        if (qual && 0.001*area < 0.4 && duration < 150.*(0.001*area)) qual=false;
        if (qual && 0.001*area >= 0.4 && duration < 60.) qual=false;
        //Tight pickup flag criteria
        bool qual_tight = false;
        if(!qual && riseSamples >= fallSamples && pulseBounds[ipulse].first>70.0 && pulseBounds[ipulse].first<2400.0 && npulses<3 && duration < 100.0) qual_tight = true;
        outputTreeContents.v_pickupFlag.push_back(!qual);
        outputTreeContents.v_pickupFlagTight.push_back(qual_tight);
    }

    totalPulseCount += npulses;

    return pulseBounds;
}

void OfflineFactory::loadBranches(){
    if (!isDRS) {
        inTree->SetBranchAddress("event", &evt);
        if (isSim) inTree->SetBranchAddress("eventWeight", &eventWeight);
        for(int ic=0;ic<numChan;ic++) waves.push_back(new TH1D());
    }
    else{
        for(int ic=0;ic<numChan;ic++) {
            int chan =  chanArray->GetAt(ic);
            int board = boardArray->GetAt(ic);
            int lenDRS = sizeof(arrayVoltageDRS[ic])/sizeof(arrayVoltageDRS[ic][0]);
            inTree->SetBranchAddress(Form("voltages_%i_%i",board,chan),arrayVoltageDRS[ic]);
            waves.push_back(new TH1D(TString(ic),"",lenDRS,0,lenDRS*1./sampleRate));
        }
    }
}

void OfflineFactory::loadWavesMilliDAQ(){

    int board,chan;
    //FIXME does this work if > 1 board?
    for(int ic=0;ic<numChan;ic++){
        if(waves[ic]) delete waves[ic];
        //board = ic<=15 ? 0 : 1;
        board = boardArray->GetAt(ic);
        chan = chanArray->GetAt(ic);
        // FIXME: Not grabbing waveforms for sim data correctly 
        waves[ic] = (TH1D*)evt->GetWaveform(board, chan, Form("digitizers[%i].waveform[%i]",board,ic));  

        if (isSlab) waves[ic]->Scale(-1);
    }
}

    
// Need to add a separate loop here in the case we have DRS data

void OfflineFactory::loadWavesDRS(){
    for(int ic=0;ic<numChan;ic++){
        int chan =  chanArray->GetAt(ic);
        int board = boardArray->GetAt(ic);
        waves[ic]->Reset();
        int lenDRS = sizeof(arrayVoltageDRS[ic])/sizeof(arrayVoltageDRS[ic][0]);
        for(int it=0;it<lenDRS;it++){
            waves[ic]->SetBinContent(it,arrayVoltageDRS[ic][it]);
        }
    }
}
void OfflineFactory::writeVersion(){
    //This is very hacky but it works
    cout<<"Git tag is "<<"longtagplaceholder"<<endl;
    TNamed v;
    v = TNamed("tag_"+to_string(runNumber)+"_"+to_string(fileNumber),"longtagplaceholder");
    v.Write();
    string triggerString = "false";
    if (triggerFileMatched) triggerString = "true";
    TNamed v2("triggerMatched_"+triggerString,"triggerMatched_"+triggerString);
    v2.Write();

    TString goodRunName("goodRunList_"+goodRunTag);
    TNamed v3(goodRunName, goodRunName);
    v3.Write();
}
TString OfflineFactory::getVersion(){
    return versionLong;
}

void OfflineFactory::findExtrema(){
    
    //find the max pulse in a given layer and the index of the max pulse in event
    outputTreeContents.v_iMaxPulseLayer = {-1, -1, -1, -1};
    std::vector<float> v_maxPulseHeight = {-1, -1, -1, -1};
    outputTreeContents.maxPulseIndex = 0;
    float maxPulseHeight = -1;

    for (int ipulse=0; ipulse < outputTreeContents.v_height.size(); ++ipulse){
        if (outputTreeContents.v_layer[ipulse] < 0 || outputTreeContents.v_layer[ipulse] > 3) continue;
        if (outputTreeContents.v_height[ipulse] > v_maxPulseHeight[outputTreeContents.v_layer[ipulse]]){
            outputTreeContents.v_iMaxPulseLayer[outputTreeContents.v_layer[ipulse]] = ipulse;
            v_maxPulseHeight[outputTreeContents.v_layer[ipulse]] = outputTreeContents.v_height[ipulse];
        }
        if (outputTreeContents.v_height[ipulse] > maxPulseHeight){
            outputTreeContents.maxPulseIndex = ipulse;
            maxPulseHeight = outputTreeContents.v_height[ipulse];
        }
    }

}
