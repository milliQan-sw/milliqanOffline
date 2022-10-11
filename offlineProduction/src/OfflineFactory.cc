#include "./interface/OfflineFactory.h"

OfflineFactory::OfflineFactory(TString inFileName, TString outFileName, TString appendToTag, bool isDRS, int runNumber, int fileNumber) : 
    inFileName(inFileName),
    outFileName(outFileName),
    appendToTag(appendToTag),
    isDRS(isDRS),
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
    colors.push_back(800); colors.push_back(400-10); colors.push_back(632-2); colors.push_back(880+1); 
    colors.push_back(432); colors.push_back(600-6); colors.push_back(416); colors.push_back(920); 
    colors.push_back(800-7); colors.push_back(400); colors.push_back(840); colors.push_back(632); 
    colors.push_back(860); colors.push_back(400-2); colors.push_back(416+2); colors.push_back(880); 
    colors.push_back(800-1); colors.push_back(632-10); colors.push_back(632+3); colors.push_back(616-1); 
    colors.push_back(432+1); colors.push_back(600-5); colors.push_back(416-7); colors.push_back(920+1); 
    colors.push_back(800+6); colors.push_back(400-9); colors.push_back(840-5); colors.push_back(632-7); 
    colors.push_back(860-2); colors.push_back(400-8); colors.push_back(416-3); colors.push_back(880-1); 
    colors.push_back(800-5); colors.push_back(820-9); colors.push_back(632-6); colors.push_back(616-9);
    colors.push_back(432-10); colors.push_back(600-9); colors.push_back(416-9); colors.push_back(920+2); 
    colors.push_back(800+1); colors.push_back(400+1); colors.push_back(840-4); colors.push_back(632-9); 
    colors.push_back(860-4); colors.push_back(400+3); colors.push_back(416-6); colors.push_back(880-4); 
    colors.push_back(800-9); colors.push_back(600-2); colors.push_back(632-3); colors.push_back(616-10); 
    colors.push_back(432-8); colors.push_back(600-10); colors.push_back(416-10); colors.push_back(1);
    colors.push_back(800-4); colors.push_back(400-6); colors.push_back(840-8); colors.push_back(632+1); 
    colors.push_back(860-9); colors.push_back(400-5); colors.push_back(416-8); colors.push_back(880-8); 
};

OfflineFactory::OfflineFactory(TString inFileName, TString outFileName, TString appendToTag, bool isDRS) {
    OfflineFactory(inFileName,outFileName,appendToTag,isDRS,-1,-1);
};
void OfflineFactory::setFriendFile(TString friendFileNameIn){
    friendFileName = friendFileNameIn;
}
void OfflineFactory::addFriendTree(){
    inTree->AddFriend("matchedTrigEvents",friendFileName);
    inTree->SetBranchAddress("clockCount", &tClockCount);
    inTree->SetBranchAddress("time", &tTime);
    inTree->SetBranchAddress("startTime", &tStartTime);
    inTree->SetBranchAddress("triggerNumber", &tTriggerNumber);
    inTree->SetBranchAddress("timeDiff", &tTimeDiff);
    inTree->SetBranchAddress("matchingTimeCut", &tMatchingTimeCut);
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
	    std::cout << "Loaded channel map" << std::endl;
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
	    std::cout << "Loaded pulse finding params" << std::endl;
	}
	if (json.find("timingCalibrations") != std::string::npos){
	    const Json::Value timingCalibrationsJson = jsonRoot["timingCalibrations"];
	    for (int index = 0; index < timingCalibrationsJson.size(); index ++){
		timingCalibrations.push_back(timingCalibrationsJson[index].asFloat());
	    }
	    std::cout << "Loaded timing calibrations" << std::endl;
	}
	if (json.find("speAreas") != std::string::npos){
	    const Json::Value speAreasJson = jsonRoot["speAreas"];
	    for (int index = 0; index < speAreasJson.size(); index ++){
		speAreas.push_back(speAreasJson[index].asFloat());
	    }
	    std::cout << "Loaded spe areas" << std::endl;
	}
	if (json.find("pedestals") != std::string::npos){
	    const Json::Value pedestalsJson = jsonRoot["pedestals"];
	    for (int index = 0; index < pedestalsJson.size(); index ++){
		pedestals.push_back(pedestalsJson[index].asFloat());
	    }
	    std::cout << "Loaded pedestal corrections" << std::endl;
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
    }
    if (nConsecSamplesEnd.size() > 1){
	if (nConsecSamplesEnd.size() != numChan) throw length_error("nConsecSamplesEnd should be length "+std::to_string(numChan) + "or 1");
    }
    else{ 
	for (int ic = 0; ic < numChan-1; ic++) nConsecSamplesEnd.push_back(nConsecSamplesEnd.at(0));
    }
    if (lowThresh.size() > 1){
	if (lowThresh.size() != numChan) throw length_error("lowThresh should be length "+std::to_string(numChan) + "or 1");
    }
    else{ 
	for (int ic = 0; ic < numChan-1; ic++) lowThresh.push_back(lowThresh.at(0));
    }
    if (highThresh.size() > 1){
	if (highThresh.size() != numChan) throw length_error("highThresh should be length "+std::to_string(numChan) + "or 1");
    }
    else{ 
	for (int ic = 0; ic < numChan-1; ic++) highThresh.push_back(highThresh.at(0));
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
    // May need to change for DRS input
    outTree->Branch("triggerThreshold",&outputTreeContents.v_triggerThresholds);
    outTree->Branch("triggerEnable",&outputTreeContents.v_triggerEnable);
    outTree->Branch("triggerMajority",&outputTreeContents.v_triggerMajority);
    outTree->Branch("triggerLogic",&outputTreeContents.v_triggerLogic);
    outTree->Branch("chan",&outputTreeContents.v_chan);
    outTree->Branch("row",&outputTreeContents.v_row);
    outTree->Branch("column",&outputTreeContents.v_column);
    outTree->Branch("layer",&outputTreeContents.v_layer);
    outTree->Branch("type",&outputTreeContents.v_type);
    outTree->Branch("board",&outputTreeContents.v_board);
    outTree->Branch("height",&outputTreeContents.v_height);
    outTree->Branch("area",&outputTreeContents.v_area);
    outTree->Branch("nPE",&outputTreeContents.v_nPE);
    outTree->Branch("ipulse",&outputTreeContents.v_ipulse);
    outTree->Branch("npulses",&outputTreeContents.v_npulses);
    outTree->Branch("time",&outputTreeContents.v_time);
    outTree->Branch("duration",&outputTreeContents.v_duration);
    outTree->Branch("delay",&outputTreeContents.v_delay);
    outTree->Branch("max",&outputTreeContents.v_max);

    outTree->Branch("tClockCount", &outputTreeContents.tClockCount);
    outTree->Branch("tTime", &outputTreeContents.tTime);
    outTree->Branch("tStartTime", &outputTreeContents.tStartTime);
    outTree->Branch("tTriggerNumber", &outputTreeContents.tTriggerNumber);
    outTree->Branch("tTimeDiff", &outputTreeContents.tTimeDiff);
    outTree->Branch("tMatchingTimeCut", &outputTreeContents.tMatchingTimeCut);
}
//Clear vectors and reset 
void OfflineFactory::resetOutBranches(){
    // May need to change for DRS input
    outputTreeContents.v_triggerThresholds.clear();
    outputTreeContents.v_triggerEnable.clear();
    outputTreeContents.v_triggerMajority.clear();
    outputTreeContents.v_triggerLogic.clear();
    outputTreeContents.v_chan.clear();
    outputTreeContents.v_row.clear();
    outputTreeContents.v_column.clear();
    outputTreeContents.v_layer.clear();
    outputTreeContents.v_type.clear();
    outputTreeContents.v_board.clear();
    outputTreeContents.v_height.clear();
    outputTreeContents.v_area.clear();
    outputTreeContents.v_nPE.clear();
    outputTreeContents.v_ipulse.clear();
    outputTreeContents.v_npulses.clear();
    outputTreeContents.v_time.clear();
    outputTreeContents.v_duration.clear();
    outputTreeContents.v_delay.clear();
    outputTreeContents.v_max.clear();
}
//Read meta data from configuration
void OfflineFactory::readMetaData(){
    //May need to change for DRS input
    TTree * metadata;
    metadata = (TTree*) inFile->Get("Metadata");
    if (!isDRS){
	metadata->SetBranchAddress("configuration", &cfg);
	metadata->GetEntry(0);
	//Currently run and fill set to zero - I think should be given as input
	outputTreeContents.runNumber = runNumber;
	outputTreeContents.fileNumber = fileNumber;
	int numBoards = cfg->digitizers.size();
	numChan = numBoards*16;
	chanArray = new TArrayI(numChan);
	boardArray = new TArrayI(numChan);
        //Read sampling rate from the metadata
        double secondsPerSample = cfg->digitizers[0].secondsPerSample;
        sampleRate = 1.0/(secondsPerSample*1e+09);
	cout << "Overwriting sample rate from metadata: " << sampleRate <<" GHz" << endl; 
        //cout<<"secondspersample = "<<secondsPerSample<<" samplingrate="<<1.0/(secondsPerSample*1e+09)<< "GHz"<<endl;
            
        //Read trigger info and set channel array
	for (int ic =0; ic < numChan; ic++){
	    chanArray->SetAt(ic % 16,ic);
	    boardArray->SetAt(ic/16,ic);
	    float triggerThresh = cfg->digitizers[ic/16].channels[ic % 16].triggerThreshold;
	    bool triggerEnable = cfg->digitizers[ic/16].channels[ic % 16].triggerEnable;
	    int triggerMajority = cfg->digitizers[ic/16].GroupTriggerMajorityLevel;
	    int triggerLogic = cfg->digitizers[ic/16].GroupTriggerLogic;
            outputTreeContents.v_triggerThresholds.push_back(triggerThresh);
	    outputTreeContents.v_triggerEnable.push_back(triggerEnable);
	    outputTreeContents.v_triggerMajority.push_back(triggerMajority);
	    outputTreeContents.v_triggerLogic.push_back(triggerLogic);
	}
    }
    else{
	//ADD SOMETHING TO DRS INPUT SUCH THAT THIS CAN BE EASILY READ!
	//output_trees_test/CMS31.root
	metadata->SetBranchAddress("boards", &boardsDRS);
	metadata->SetBranchAddress("channels", &chansDRS);
	metadata->SetBranchAddress("numChan", &numChan);
	metadata->GetEntry(0);
	chanArray = new TArrayI(numChan);
	boardArray = new TArrayI(numChan);
	for (int ic =0; ic < numChan; ic++){
	    chanArray->AddAt(chansDRS[ic],ic);
	    boardArray->AddAt(boardsDRS[ic],ic);
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
    gPad->SetRightMargin(0.39);
    gStyle->SetGridStyle(3);
    gStyle->SetGridColor(13);
    c.SetGrid();
    
    float drawThresh=5;

    gStyle->SetTitleX(0.35);
    vector<int> chanList;
    float maxheight=0; float minheight=0;
    float timeRange[2];
    timeRange[1]=1024./sampleRate; timeRange[0]=0.;
    //Get the waves
    vector<vector<pair<float,float>>> boundsShifted;
    vector<TH1D*> wavesShifted;
    float originalMaxHeights[80];
    //cout<<3<<endl;
    for(uint ic=0;ic<bounds.size();ic++){
        int chan = chanArray->GetAt(ic);
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
        
        if(boundShifted.size()>0 || waveShifted->GetMaximum()>drawThresh){
            chanList.push_back(ic);
            //FIX here: Check for the run for beam state. By default set to on for now
            TString beamState = "on";
            waveShifted->SetTitle(Form("Run %i, File %i, Event %i;Uncalibrated Time [ns];Amplitude [mV];",runNumber,fileNumber,event));
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
    //cout<<5<<endl;
    
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
    //cout<<"timeRange="<<timeRange[1]<<endl;
    
    if (rangeMaxX < 0) timeRange[1]= min(0.9*timeRange[1],1024./sampleRate);
    else timeRange[1] = max(1.1*timeRange[1],1024./sampleRate);
    //cout<<"timeRange="<<timeRange[1]<<endl;
    
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
        //cout<<"Channel,ic,column,row,layer,type: "<<i<<" "<<ic<<" "<<column<<" "<<row<<" "<<layer<<" "<<type<<endl;
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
                line.DrawLine(boundsShifted[ic][ip].first,0,boundsShifted[ic][ip].first,0.2*maxheight);
                line.DrawLine(boundsShifted[ic][ip].second,0,boundsShifted[ic][ip].second,0.2*maxheight);
            }
        }
    } //channel loop close
    //cout<<7<<endl;
     
    float boxw= 0.0438;
    float boxh=0.0438;
    float barw=0.017;
    float barh=0.017;
    //    float barw=0.017;
    //    float barh=0.017;
    vector<float> xstart = {0.63,0.72,0.81,0.90};
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
    float currentYpos=0.737;
    float headerX=0.67;
    float rowX=0.69;
    int pulseIndex=0; // Keep track of pulse index, since all pulses for all channels are actually stored in the same 1D vectors
    int maxPerChannel = 0;
    if (chanList.size() > 0) maxPerChannel = 10/chanList.size();
    //cout<<8<<endl;
    
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
            pave = new TPave(xstart_leftsheets[0],ystart_sidesheets,xstart_leftsheets[0]+(sheet_width*1.0),ystart_sidesheets+(vert_sheet_length),0,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            //cout<<"column,row,layer,type: Draw "<<column<<" "<<row<<" "<<layer<<" "<<type<<endl;
            pave->Draw();
        }
        if(column==0 && row==0 && layer==4 && type==1){
            pave = new TPave(xstart_leftsheets[4],ystart_sidesheets,xstart_leftsheets[4]+(sheet_width*1.0),ystart_sidesheets+vert_sheet_length,0,"NDC");
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
            pave = new TPave(xstart[2]-0.006,ystart[3]+boxh+0.015+(sheet_width*2.5),xstart[3]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*4.5),1,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillStyle(3154);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==4 && row==0 && layer==2 && type==2){
            pave = new TPave(xstart[2]-0.006,ystart[3]+boxh+0.015+(sheet_width*5.0),xstart[3]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*7.0),1,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillStyle(3145);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==-1 && row==0 && layer==0 && type==2){
            pave = new TPave(xstart[0]-0.006,ystart[3]+boxh+0.015+(sheet_width*2.5),xstart[1]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*4.5),1,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillStyle(3154);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        if(column==4 && row==0 && layer==0 && type==2){
            pave = new TPave(xstart[0]-0.006,ystart[3]+boxh+0.015+(sheet_width*5.0),xstart[1]+barw+boxw+0.006,ystart[3]+boxh+0.015+(sheet_width*7.0),1,"NDC");
            pave->SetFillColor(colors[colorIndex]);
            pave->SetFillStyle(3145);
            pave->SetFillColor(colors[colorIndex]);
            pave->Draw();
        }
        
        //cout<<"pave: i,ic,column,row,layer,type: Draw "<<i<<" "<<ic<<" "<<column<<" "<<row<<" "<<layer<<" "<<type<<" "<<colorIndex<<endl;
        
        tla.SetTextColor(colors[colorIndex]);
        tla.SetTextSize(0.015);
        //tla.DrawLatexNDC(headerX,currentYpos,Form("Channel %i, V_{max} = %0.0f, N_{pulses}= %i",ic,originalMaxHeights[ic],(int)boundsShifted[ic].size()));
        tla.DrawLatexNDC(headerX,currentYpos,Form("Channel %i, V_{max} = %0.0f, N_{pulses}= %i (%i,%i,%i,%i)",ic,originalMaxHeights[ic],(int)boundsShifted[ic].size(),column,row,layer,type));
        tla.SetTextColor(kBlack);
        currentYpos=currentYpos-(height*0.4);
        //currentYpos-=height;
        tla.SetTextSize(0.02);
        
        for(int ip=0;ip<boundsShifted[ic].size();ip++){
            TString row;
            row = Form("Channel number = %d",ip);
            pulseIndex++; 
            if(ip < maxPerChannel){
                tla.DrawLatexNDC(rowX,currentYpos,row);
                currentYpos-=height*0.8;
            }
        }
        currentYpos-=height*0.2;
    } //channel loop closed
    //cout<<9<<endl;
    
    //cout<<"Display directory is "<<displayDirectory<<endl;
    TString displayName;
    displayName=Form(displayDirectory+"Run%i_File%i_Event%i_Version_%s.pdf",runNumber,fileNumber,event,"shorttagplaceholder"); 
    c.SaveAs(displayName);
    displayName=Form(displayDirectory+"Run%i_File%i_Event%i_Version_%s.png",runNumber,fileNumber,event,"shorttagplaceholder"); 
    c.SaveAs(displayName);

    for(uint i=0;i<chanList.size();i++){
	delete wavesShifted[i];
    }
    //cout<<10<<endl;
    
}

vector<vector<pair<float,float>>> OfflineFactory::readWaveDataPerEvent(int i){
    inTree->GetEntry(i);
    if (!isDRS) loadWavesMilliDAQ();
    else loadWavesDRS();
    //Loop over channels
    vector<vector<pair<float,float> > > allPulseBounds;
    for(int ic=0;ic<numChan;ic++){
        //Pulse finding
        allPulseBounds.push_back(processChannel(ic));
    }   
    
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
    for(auto iEvent: eventsToDisplay){
	resetOutBranches();	
        vector<vector<pair<float,float> > > allPulseBounds;
        allPulseBounds = readWaveDataPerEvent(iEvent);
	displayEvent(iEvent,allPulseBounds,displayDirectoryForRun);
    }
    inFile->Close();
}
//Pulse finding and per channel processing
void OfflineFactory::readWaveData(){
    validateInput();
    inTree = (TTree*)inFile->Get("Events"); 
    if (friendFileName != "") addFriendTree();
    loadBranches();
    // int maxEvents = 1;
    int maxEvents = inTree->GetEntries();
    cout<<"Processing "<<maxEvents<<" events in this file"<<endl;
    cout<<"Starting event loop"<<endl;
    bool showBar = true;

    for(int i=0;i<maxEvents;i++){

	resetOutBranches();	
        //Process each event
        vector<vector<pair<float,float> > > allPulseBounds;
	outputTreeContents.event=i;	
        allPulseBounds = readWaveDataPerEvent(i);
	outputTreeContents.tClockCount = tClockCount;
	outputTreeContents.tTime = tTime;
	outputTreeContents.tStartTime = tStartTime;
	outputTreeContents.tTriggerNumber = tTriggerNumber;
	outputTreeContents.tTimeDiff = tTimeDiff;
	outputTreeContents.tMatchingTimeCut = tMatchingTimeCut;
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
    std::cout << std::endl;
    
}

void OfflineFactory::writeOutputTree(){
    outFile->cd();
    outTree->Write();
    writeVersion();
    outFile->Close();
    if (inFile) inFile->Close();
}
void OfflineFactory::prepareWave(int ic){
    TAxis * a = waves[ic]->GetXaxis();
    // a->Set( a->GetNbins(), a->GetXmin()/sampleRate, a->GetXmax()/sampleRate);
    // waves[ic]->ResetStats();
    //subtract calibrated mean
    for(int ibin = 1; ibin <= waves[ic]->GetNbinsX(); ibin++){
	waves[ic]->SetBinContent(ibin,waves[ic]->GetBinContent(ibin)-pedestals[ic]);
    }
    //Need to add sideband measurements and subtraction here
}
vector< pair<float,float> > OfflineFactory::findPulses(int ic){

    vector<pair<float,float> > bounds;
    //float tstart = sideband_range[1]+1;
    //int istart = waves[ic]->FindBin(tstart);
    int istart = 1;
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
		// cout<<"i_begin, i: "<<i_begin<<" "<<i<<endl;       // i_begin is the 
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
    outputTreeContents.v_max_threeConsec.push_back(maxThreeConsec);
    //FIXME Need to add low pass filter option back
    outputTreeContents.v_max_afterFilter.push_back(waves[ic]->GetMaximum());
    outputTreeContents.v_min_afterFilter.push_back(waves[ic]->GetMinimum());

    for(int ipulse = 0; ipulse<npulses; ipulse++){
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
	outputTreeContents.v_chan.push_back(chanArray->GetAt(ic));
	outputTreeContents.v_board.push_back(boardArray->GetAt(ic));
	outputTreeContents.v_height.push_back(waves[ic]->GetMaximum());
	outputTreeContents.v_time.push_back(pulseBounds[ipulse].first);
	outputTreeContents.v_time_module_calibrated.push_back(pulseBounds[ipulse].first+timingCalibrations[ic]);
	outputTreeContents.v_area.push_back(waves[ic]->Integral());
	outputTreeContents.v_nPE.push_back((waves[ic]->Integral()/(speAreas[ic]))*(1.6/sampleRate));
	outputTreeContents.v_ipulse.push_back(ipulse);
	outputTreeContents.v_npulses.push_back(npulses);
	outputTreeContents.v_duration.push_back(pulseBounds[ipulse].second - pulseBounds[ipulse].first);
	if(ipulse>0) outputTreeContents.v_delay.push_back(pulseBounds[ipulse].first - pulseBounds[ipulse-1].second);
	else outputTreeContents.v_delay.push_back(9999.);

    }    

    return pulseBounds;
}

void OfflineFactory::loadBranches(){
    int lenDRS = sizeof(arrayVoltageDRS)/sizeof(arrayVoltageDRS[0]);
    if (!isDRS) {
	inTree->SetBranchAddress("event", &evt);
	for(int ic=0;ic<numChan;ic++) waves.push_back(new TH1D());
    }
    else{
	for(int ic=0;ic<numChan;ic++) waves.push_back(new TH1D(TString(ic),"",lenDRS,0,lenDRS*1./sampleRate));
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
	waves[ic] = (TH1D*)evt->GetWaveform(board, chan, Form("digitizers[%i].waveform[%i]",board,ic));  
    }

}    
// Need to add a separate loop here in the case we have DRS data

void OfflineFactory::loadWavesDRS(){
    int lenDRS = sizeof(arrayVoltageDRS)/sizeof(arrayVoltageDRS[0]);
    for(int ic=0;ic<numChan;ic++){
	int chan =  chanArray->GetAt(ic);
	int board = boardArray->GetAt(ic);
	inTree->SetBranchAddress(Form("voltages_%i_%i",board,chan),arrayVoltageDRS);
	for(int it=0;it<lenDRS;it++){
	    waves[ic]->SetBinContent(it,arrayVoltageDRS[it]);
	}
    }
}
void OfflineFactory::writeVersion(){
    //This is very hacky but it works
    cout<<"Git tag is "<<"longtagplaceholder"<<endl;
    TNamed v;
    v = TNamed("tag","longtagplaceholder");
    v.Write();
}
TString OfflineFactory::getVersion(){
    return versionLong;
}
