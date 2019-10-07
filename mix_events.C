#define SimTree_cxx
#include "SimTree.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

#ifndef _INCL_GUARD
#define _INCL_GUARD
#endif
#include "TTree.h"
#include "TChain.h"
TChain * inTree = new TChain("Events");
#include "make_tree.C"


void mix_events(TString runToMixName="1372", TString inFileName = "exampleInjectionInput.root", TString tag = "example",int fileNumber = 1, int startEvent = 0, int maxEvents = -1, int seed = 0);
void clearOutBranchesMix();
void prepareOutBranchesMix();

vector<TBranch *> b_times;
vector<TBranch *> b_voltages;
TBranch * b_timestamp;
double timestamp;

Double_t times_0[1024];
Double_t times_1[1024];
Double_t times_2[1024];
Double_t times_3[1024];
Double_t times_4[1024];
Double_t times_5[1024];
Double_t times_6[1024];
Double_t times_7[1024];
Double_t times_8[1024];
Double_t times_9[1024];
Double_t times_10[1024];
Double_t times_11[1024];
Double_t times_12[1024];
Double_t times_13[1024];
Double_t times_14[1024];
Double_t times_15[1024];
Double_t times_16[1024];
Double_t times_17[1024];
Double_t times_18[1024];
Double_t times_19[1024];
Double_t times_20[1024];
Double_t times_21[1024];
Double_t times_22[1024];
Double_t times_23[1024];
Double_t times_24[1024];
Double_t times_25[1024];
Double_t times_26[1024];
Double_t times_27[1024];
Double_t times_28[1024];
Double_t times_29[1024];
Double_t times_30[1024];
Double_t times_31[1024];

TBranch * b_times_0;
TBranch * b_times_1;
TBranch * b_times_2;
TBranch * b_times_3;
TBranch * b_times_4;
TBranch * b_times_5;
TBranch * b_times_6;
TBranch * b_times_7;
TBranch * b_times_8;
TBranch * b_times_9;
TBranch * b_times_10;
TBranch * b_times_11;
TBranch * b_times_12;
TBranch * b_times_13;
TBranch * b_times_14;
TBranch * b_times_15;
TBranch * b_times_16;
TBranch * b_times_17;
TBranch * b_times_18;
TBranch * b_times_19;
TBranch * b_times_20;
TBranch * b_times_21;
TBranch * b_times_22;
TBranch * b_times_23;
TBranch * b_times_24;
TBranch * b_times_25;
TBranch * b_times_26;
TBranch * b_times_27;
TBranch * b_times_28;
TBranch * b_times_29;
TBranch * b_times_30;
TBranch * b_times_31;

Double_t voltages_0[1024];
Double_t voltages_1[1024];
Double_t voltages_2[1024];
Double_t voltages_3[1024];
Double_t voltages_4[1024];
Double_t voltages_5[1024];
Double_t voltages_6[1024];
Double_t voltages_7[1024];
Double_t voltages_8[1024];
Double_t voltages_9[1024];
Double_t voltages_10[1024];
Double_t voltages_11[1024];
Double_t voltages_12[1024];
Double_t voltages_13[1024];
Double_t voltages_14[1024];
Double_t voltages_15[1024];
Double_t voltages_16[1024];
Double_t voltages_17[1024];
Double_t voltages_18[1024];
Double_t voltages_19[1024];
Double_t voltages_20[1024];
Double_t voltages_21[1024];
Double_t voltages_22[1024];
Double_t voltages_23[1024];
Double_t voltages_24[1024];
Double_t voltages_25[1024];
Double_t voltages_26[1024];
Double_t voltages_27[1024];
Double_t voltages_28[1024];
Double_t voltages_29[1024];
Double_t voltages_30[1024];
Double_t voltages_31[1024];

TBranch * b_voltages_0;
TBranch * b_voltages_1;
TBranch * b_voltages_2;
TBranch * b_voltages_3;
TBranch * b_voltages_4;
TBranch * b_voltages_5;
TBranch * b_voltages_6;
TBranch * b_voltages_7;
TBranch * b_voltages_8;
TBranch * b_voltages_9;
TBranch * b_voltages_10;
TBranch * b_voltages_11;
TBranch * b_voltages_12;
TBranch * b_voltages_13;
TBranch * b_voltages_14;
TBranch * b_voltages_15;
TBranch * b_voltages_16;
TBranch * b_voltages_17;
TBranch * b_voltages_18;
TBranch * b_voltages_19;
TBranch * b_voltages_20;
TBranch * b_voltages_21;
TBranch * b_voltages_22;
TBranch * b_voltages_23;
TBranch * b_voltages_24;
TBranch * b_voltages_25;
TBranch * b_voltages_26;
TBranch * b_voltages_27;
TBranch * b_voltages_28;
TBranch * b_voltages_29;
TBranch * b_voltages_30;
TBranch * b_voltages_31;

uint maxNPEForSample = 20;

void mix_events(TString runToMixName, TString inFileName , TString tag, int fileNumber, int startEvent, int maxEvents, int seed){

    vector<double> distanceToBottomSlab;
    vector<double> tubeTimeCorr;

    for (int ic=0;ic<=31;ic++) {
	distanceToBottomSlab.push_back(zPosition[ic]-zPosition[18]);
	if (tubeSpecies[ic] == "ET") tubeTimeCorr.push_back(-11.5);
	else if (tubeSpecies[ic] == "R7725") tubeTimeCorr.push_back(-11.5);
	else if (tubeSpecies[ic] == "R878") tubeTimeCorr.push_back(-22.5);
    }

    TFile * inFile = new TFile(inFileName);
    TTree * simTreeInput = (TTree *) inFile->Get("Events");
    uint totEvents = simTreeInput->GetEntries();
    // totEvents -= startEvent;
    if (totEvents > maxEvents && maxEvents >= 0) totEvents = maxEvents;
    SimTree sTree = SimTree(simTreeInput);
    // uint fileNumber = 2;
    TString mixFileName;
    while (true){
	mixFileName =  "/net/cms26/cms26r0/milliqan/UX5/Run"+runToMixName+"_software/MilliQan_Run"+runToMixName+"."+to_string(fileNumber)+"_software.root";
	inTree->Add(mixFileName);
	int totEventsMix = inTree->GetEntries();
	if (totEventsMix >= totEvents-startEvent) break;
	fileNumber++;
    }
    TFile * f = new TFile(mixFileName);
    gRandom->SetSeed(seed);


    TString milliqanMixDir="/net/cms26/cms26r0/milliqan/milliqanOffline/mixTrees";
    TString outFileName = milliqanMixDir+"/"+tag+".root";
    TFile * outFile = new TFile(outFileName,"recreate");
    outTree = new TTree("Events","Events");
    outTree->SetDirectory(outFile);
    prepareOutBranchesMix();
    TTree * metadata = (TTree*)f->Get("Metadata");
    metadata->SetBranchAddress("configuration", &cfg);
    metadata->GetEntry(0);
    sample_rate[0] = 3.2 / pow(2,cfg->digitizers[0].SAMFrequency);
    sample_rate[1] = 3.2 / pow(2,cfg->digitizers[1].SAMFrequency);

    speR878[0] = new SPE("r878",sample_rate[0],false,-1);
    speR878[1] = new SPE("r878",sample_rate[1],false,-1);
    speR7725[0] = new SPE("r7725",sample_rate[0],false,-1);
    speR7725[1] = new SPE("r7725",sample_rate[1],false,-1);
    speET[0] = new SPE("et",sample_rate[0],false,-1);
    speET[1] = new SPE("et",sample_rate[1],false,-1);

    loadBranchesMilliDAQ();
    // sTree.fChain->SetBranchStatus("*",1);  
    Long64_t nbytes = 0, nb = 0;
    for(int i=startEvent;i<totEvents;i++){
	if(i%100==0) cout<<"Processing event "<<i<<endl;
	TDatime time = TDatime();
	timestamp = time.GetSecond()+60*time.GetMinute()+3600*time.GetHour();
	sTree.LoadTree(i);
	nb = sTree.fChain->GetEntry(i);   nbytes += nb;
	inTree->GetEntry(i);
	loadWavesMilliDAQ();
	clearOutBranchesMix();
	for (uint iChan = 0; iChan < 32; iChan++){
	    waves[iChan]->Scale(-1.);
	    convertXaxis(waves[iChan],iChan);
	}
	TH1D * generatedTemplate = NULL;
	// std::cout << sTree.chan0_PEtimes->size() << std::endl;
	int nPhoton[32];
	for (uint photonTime = 0; photonTime < 100; photonTime++){

	    nPhoton[0] = sTree.chan0_PEtimes[photonTime]; 
	    nPhoton[1] = sTree.chan1_PEtimes[photonTime]; 
	    nPhoton[2] = sTree.chan2_PEtimes[photonTime]; 
	    nPhoton[3] = sTree.chan3_PEtimes[photonTime]; 
	    nPhoton[4] = sTree.chan4_PEtimes[photonTime]; 
	    nPhoton[5] = sTree.chan5_PEtimes[photonTime]; 
	    nPhoton[6] = sTree.chan6_PEtimes[photonTime]; 
	    nPhoton[7] = sTree.chan7_PEtimes[photonTime]; 
	    nPhoton[8] = sTree.chan8_PEtimes[photonTime]; 
	    nPhoton[9] = sTree.chan9_PEtimes[photonTime]; 
	    nPhoton[10] = sTree.chan10_PEtimes[photonTime]; 
	    nPhoton[11] = sTree.chan11_PEtimes[photonTime]; 
	    nPhoton[12] = sTree.chan12_PEtimes[photonTime]; 
	    nPhoton[13] = sTree.chan13_PEtimes[photonTime]; 
	    nPhoton[14] = sTree.chan14_PEtimes[photonTime]; 
	    nPhoton[15] = sTree.chan15_PEtimes[photonTime]; 
	    nPhoton[16] = sTree.chan16_PEtimes[photonTime]; 
	    nPhoton[17] = sTree.chan17_PEtimes[photonTime]; 
	    nPhoton[18] = sTree.chan18_PEtimes[photonTime]; 
	    nPhoton[19] = sTree.chan19_PEtimes[photonTime]; 
	    nPhoton[20] = sTree.chan20_PEtimes[photonTime]; 
	    nPhoton[21] = sTree.chan21_PEtimes[photonTime]; 
	    nPhoton[22] = sTree.chan22_PEtimes[photonTime]; 
	    nPhoton[23] = sTree.chan23_PEtimes[photonTime]; 
	    nPhoton[24] = sTree.chan24_PEtimes[photonTime]; 
	    nPhoton[25] = sTree.chan25_PEtimes[photonTime]; 
	    nPhoton[26] = sTree.chan26_PEtimes[photonTime]; 
	    nPhoton[27] = sTree.chan27_PEtimes[photonTime]; 
	    nPhoton[28] = sTree.chan28_PEtimes[photonTime]; 
	    nPhoton[29] = sTree.chan29_PEtimes[photonTime]; 
	    nPhoton[30] = sTree.chan30_PEtimes[photonTime]; 
	    nPhoton[31] = sTree.chan31_PEtimes[photonTime]; 

	    for (uint iChan = 0; iChan < 32; iChan++){
		if (nPhoton[iChan] == 0) continue;
		if (nPhoton[iChan] < maxNPEForSample){
		    for (uint arb = 0; arb < nPhoton[iChan]; arb++){
			generatedTemplate = SPEGen(sample_rate[iChan/16],tubeSpecies[iChan],channelSPEAreas[iChan],iChan/16);
			int signalPulsesStartBin = waves[iChan]->FindBin(380+photonTime-channelCalibrations[iChan]+tubeTimeCorr[iChan]);
			for(int ibin = 1; ibin <= 1024; ibin++){
			    if (ibin+signalPulsesStartBin > waves[iChan]->GetNbinsX()) break;
			    waves[iChan]->SetBinContent(ibin+signalPulsesStartBin,waves[iChan]->GetBinContent(ibin+signalPulsesStartBin)+generatedTemplate->GetBinContent(ibin));
			}
			generatedTemplate->Delete();
		    }
		}
		else{
		    generatedTemplate = SPEGenLargeN(sample_rate[iChan/16],tubeSpecies[iChan],channelSPEAreas[iChan],iChan/16,nPhoton[iChan]);
		    int signalPulsesStartBin = waves[iChan]->FindBin(380+photonTime-channelCalibrations[iChan]+tubeTimeCorr[iChan]);
		    for(int ibin = 1; ibin <= 1024; ibin++){
			if (ibin+signalPulsesStartBin > waves[iChan]->GetNbinsX()) break;
			waves[iChan]->SetBinContent(ibin+signalPulsesStartBin,waves[iChan]->GetBinContent(ibin+signalPulsesStartBin)+generatedTemplate->GetBinContent(ibin));
		    }
		    generatedTemplate->Delete();
		}
	    }
	}
	for (uint iChan = 0; iChan < 32; iChan++){
	    waves[iChan]->Scale(-1.);
	}
	for(int ibin = 1; ibin <= 1024; ibin++){
	    times_0[ibin-1] = waves[0]->GetBinCenter(ibin);
	    voltages_0[ibin-1] = waves[0]->GetBinContent(ibin);
	    times_1[ibin-1] = waves[1]->GetBinCenter(ibin);
	    voltages_1[ibin-1] = waves[1]->GetBinContent(ibin);
	    times_2[ibin-1] = waves[2]->GetBinCenter(ibin);
	    voltages_2[ibin-1] = waves[2]->GetBinContent(ibin);
	    times_3[ibin-1] = waves[3]->GetBinCenter(ibin);
	    voltages_3[ibin-1] = waves[3]->GetBinContent(ibin);
	    times_4[ibin-1] = waves[4]->GetBinCenter(ibin);
	    voltages_4[ibin-1] = waves[4]->GetBinContent(ibin);
	    times_5[ibin-1] = waves[5]->GetBinCenter(ibin);
	    voltages_5[ibin-1] = waves[5]->GetBinContent(ibin);
	    times_6[ibin-1] = waves[6]->GetBinCenter(ibin);
	    voltages_6[ibin-1] = waves[6]->GetBinContent(ibin);
	    times_7[ibin-1] = waves[7]->GetBinCenter(ibin);
	    voltages_7[ibin-1] = waves[7]->GetBinContent(ibin);
	    times_8[ibin-1] = waves[8]->GetBinCenter(ibin);
	    voltages_8[ibin-1] = waves[8]->GetBinContent(ibin);
	    times_9[ibin-1] = waves[9]->GetBinCenter(ibin);
	    voltages_9[ibin-1] = waves[9]->GetBinContent(ibin);
	    times_10[ibin-1] = waves[10]->GetBinCenter(ibin);
	    voltages_10[ibin-1] = waves[10]->GetBinContent(ibin);
	    times_11[ibin-1] = waves[11]->GetBinCenter(ibin);
	    voltages_11[ibin-1] = waves[11]->GetBinContent(ibin);
	    times_12[ibin-1] = waves[12]->GetBinCenter(ibin);
	    voltages_12[ibin-1] = waves[12]->GetBinContent(ibin);
	    times_13[ibin-1] = waves[13]->GetBinCenter(ibin);
	    voltages_13[ibin-1] = waves[13]->GetBinContent(ibin);
	    times_14[ibin-1] = waves[14]->GetBinCenter(ibin);
	    voltages_14[ibin-1] = waves[14]->GetBinContent(ibin);
	    times_15[ibin-1] = waves[15]->GetBinCenter(ibin);
	    voltages_15[ibin-1] = waves[15]->GetBinContent(ibin);
	    times_16[ibin-1] = waves[16]->GetBinCenter(ibin);
	    voltages_16[ibin-1] = waves[16]->GetBinContent(ibin);
	    times_17[ibin-1] = waves[17]->GetBinCenter(ibin);
	    voltages_17[ibin-1] = waves[17]->GetBinContent(ibin);
	    times_18[ibin-1] = waves[18]->GetBinCenter(ibin);
	    voltages_18[ibin-1] = waves[18]->GetBinContent(ibin);
	    times_19[ibin-1] = waves[19]->GetBinCenter(ibin);
	    voltages_19[ibin-1] = waves[19]->GetBinContent(ibin);
	    times_20[ibin-1] = waves[20]->GetBinCenter(ibin);
	    voltages_20[ibin-1] = waves[20]->GetBinContent(ibin);
	    times_21[ibin-1] = waves[21]->GetBinCenter(ibin);
	    voltages_21[ibin-1] = waves[21]->GetBinContent(ibin);
	    times_22[ibin-1] = waves[22]->GetBinCenter(ibin);
	    voltages_22[ibin-1] = waves[22]->GetBinContent(ibin);
	    times_23[ibin-1] = waves[23]->GetBinCenter(ibin);
	    voltages_23[ibin-1] = waves[23]->GetBinContent(ibin);
	    times_24[ibin-1] = waves[24]->GetBinCenter(ibin);
	    voltages_24[ibin-1] = waves[24]->GetBinContent(ibin);
	    times_25[ibin-1] = waves[25]->GetBinCenter(ibin);
	    voltages_25[ibin-1] = waves[25]->GetBinContent(ibin);
	    times_26[ibin-1] = waves[26]->GetBinCenter(ibin);
	    voltages_26[ibin-1] = waves[26]->GetBinContent(ibin);
	    times_27[ibin-1] = waves[27]->GetBinCenter(ibin);
	    voltages_27[ibin-1] = waves[27]->GetBinContent(ibin);
	    times_28[ibin-1] = waves[28]->GetBinCenter(ibin);
	    voltages_28[ibin-1] = waves[28]->GetBinContent(ibin);
	    times_29[ibin-1] = waves[29]->GetBinCenter(ibin);
	    voltages_29[ibin-1] = waves[29]->GetBinContent(ibin);
	    times_30[ibin-1] = waves[30]->GetBinCenter(ibin);
	    voltages_30[ibin-1] = waves[30]->GetBinContent(ibin);
	    times_31[ibin-1] = waves[31]->GetBinCenter(ibin);
	    voltages_31[ibin-1] = waves[31]->GetBinContent(ibin);
	}
	outTree->Fill();
    }
    outFile->cd();
    TNamed testDate = TNamed(TString("date"),TString(tag));
    TParameter<float> sampleRate0 = TParameter<float>("sampleRate0",sample_rate[0]);
    TParameter<float> sampleRate1 = TParameter<float>("sampleRate1",sample_rate[1]);
    TArrayI * chanArray =  new TArrayI(32);
    for(uint ic=0;ic<32;ic++){
	chanArray->SetAt(ic,ic);
    }
    sampleRate0.Write();
    sampleRate1.Write();
    testDate.Write();
    outFile->WriteObject(chanArray,TString("chans"));
    outTree->Write();
    outFile->Close();
    return;
}
void clearOutBranchesMix(){
}
void prepareOutBranchesMix(){
    b_timestamp = outTree->Branch("timestamp",&timestamp,"timestamp/D");
    // times.push_back(time);
    // voltages.push_back(voltage);
    b_times_0 = outTree->Branch("times_0",times_0,"times_0[1024]/D");
    b_times_1 = outTree->Branch("times_1",times_1,"times_1[1024]/D");
    b_times_2 = outTree->Branch("times_2",times_2,"times_2[1024]/D");
    b_times_3 = outTree->Branch("times_3",times_3,"times_3[1024]/D");
    b_times_4 = outTree->Branch("times_4",times_4,"times_4[1024]/D");
    b_times_5 = outTree->Branch("times_5",times_5,"times_5[1024]/D");
    b_times_6 = outTree->Branch("times_6",times_6,"times_6[1024]/D");
    b_times_7 = outTree->Branch("times_7",times_7,"times_7[1024]/D");
    b_times_8 = outTree->Branch("times_8",times_8,"times_8[1024]/D");
    b_times_9 = outTree->Branch("times_9",times_9,"times_9[1024]/D");
    b_times_10 = outTree->Branch("times_10",times_10,"times_10[1024]/D");
    b_times_11 = outTree->Branch("times_11",times_11,"times_11[1024]/D");
    b_times_12 = outTree->Branch("times_12",times_12,"times_12[1024]/D");
    b_times_13 = outTree->Branch("times_13",times_13,"times_13[1024]/D");
    b_times_14 = outTree->Branch("times_14",times_14,"times_14[1024]/D");
    b_times_15 = outTree->Branch("times_15",times_15,"times_15[1024]/D");
    b_times_16 = outTree->Branch("times_16",times_16,"times_16[1024]/D");
    b_times_17 = outTree->Branch("times_17",times_17,"times_17[1024]/D");
    b_times_18 = outTree->Branch("times_18",times_18,"times_18[1024]/D");
    b_times_19 = outTree->Branch("times_19",times_19,"times_19[1024]/D");
    b_times_20 = outTree->Branch("times_20",times_20,"times_20[1024]/D");
    b_times_21 = outTree->Branch("times_21",times_21,"times_21[1024]/D");
    b_times_22 = outTree->Branch("times_22",times_22,"times_22[1024]/D");
    b_times_23 = outTree->Branch("times_23",times_23,"times_23[1024]/D");
    b_times_24 = outTree->Branch("times_24",times_24,"times_24[1024]/D");
    b_times_25 = outTree->Branch("times_25",times_25,"times_25[1024]/D");
    b_times_26 = outTree->Branch("times_26",times_26,"times_26[1024]/D");
    b_times_27 = outTree->Branch("times_27",times_27,"times_27[1024]/D");
    b_times_28 = outTree->Branch("times_28",times_28,"times_28[1024]/D");
    b_times_29 = outTree->Branch("times_29",times_29,"times_29[1024]/D");
    b_times_30 = outTree->Branch("times_30",times_30,"times_30[1024]/D");
    b_times_31 = outTree->Branch("times_31",times_31,"times_31[1024]/D");

    b_voltages_0 = outTree->Branch("voltages_0",voltages_0,"voltages_0[1024]/D");
    b_voltages_1 = outTree->Branch("voltages_1",voltages_1,"voltages_1[1024]/D");
    b_voltages_2 = outTree->Branch("voltages_2",voltages_2,"voltages_2[1024]/D");
    b_voltages_3 = outTree->Branch("voltages_3",voltages_3,"voltages_3[1024]/D");
    b_voltages_4 = outTree->Branch("voltages_4",voltages_4,"voltages_4[1024]/D");
    b_voltages_5 = outTree->Branch("voltages_5",voltages_5,"voltages_5[1024]/D");
    b_voltages_6 = outTree->Branch("voltages_6",voltages_6,"voltages_6[1024]/D");
    b_voltages_7 = outTree->Branch("voltages_7",voltages_7,"voltages_7[1024]/D");
    b_voltages_8 = outTree->Branch("voltages_8",voltages_8,"voltages_8[1024]/D");
    b_voltages_9 = outTree->Branch("voltages_9",voltages_9,"voltages_9[1024]/D");
    b_voltages_10 = outTree->Branch("voltages_10",voltages_10,"voltages_10[1024]/D");
    b_voltages_11 = outTree->Branch("voltages_11",voltages_11,"voltages_11[1024]/D");
    b_voltages_12 = outTree->Branch("voltages_12",voltages_12,"voltages_12[1024]/D");
    b_voltages_13 = outTree->Branch("voltages_13",voltages_13,"voltages_13[1024]/D");
    b_voltages_14 = outTree->Branch("voltages_14",voltages_14,"voltages_14[1024]/D");
    b_voltages_15 = outTree->Branch("voltages_15",voltages_15,"voltages_15[1024]/D");
    b_voltages_16 = outTree->Branch("voltages_16",voltages_16,"voltages_16[1024]/D");
    b_voltages_17 = outTree->Branch("voltages_17",voltages_17,"voltages_17[1024]/D");
    b_voltages_18 = outTree->Branch("voltages_18",voltages_18,"voltages_18[1024]/D");
    b_voltages_19 = outTree->Branch("voltages_19",voltages_19,"voltages_19[1024]/D");
    b_voltages_20 = outTree->Branch("voltages_20",voltages_20,"voltages_20[1024]/D");
    b_voltages_21 = outTree->Branch("voltages_21",voltages_21,"voltages_21[1024]/D");
    b_voltages_22 = outTree->Branch("voltages_22",voltages_22,"voltages_22[1024]/D");
    b_voltages_23 = outTree->Branch("voltages_23",voltages_23,"voltages_23[1024]/D");
    b_voltages_24 = outTree->Branch("voltages_24",voltages_24,"voltages_24[1024]/D");
    b_voltages_25 = outTree->Branch("voltages_25",voltages_25,"voltages_25[1024]/D");
    b_voltages_26 = outTree->Branch("voltages_26",voltages_26,"voltages_26[1024]/D");
    b_voltages_27 = outTree->Branch("voltages_27",voltages_27,"voltages_27[1024]/D");
    b_voltages_28 = outTree->Branch("voltages_28",voltages_28,"voltages_28[1024]/D");
    b_voltages_29 = outTree->Branch("voltages_29",voltages_29,"voltages_29[1024]/D");
    b_voltages_30 = outTree->Branch("voltages_30",voltages_30,"voltages_30[1024]/D");
    b_voltages_31 = outTree->Branch("voltages_31",voltages_31,"voltages_31[1024]/D");
}
int main(int argc, char **argv)
{
    if(argc==1) mix_events();
    else if(argc==2) mix_events(argv[1]);
    else if(argc==3) mix_events(argv[1],argv[2]);
    else if(argc==4) mix_events(argv[1],argv[2],argv[3]);
    else if(argc==5) mix_events(argv[1],argv[2],argv[3],stoi(argv[4]));
    else if(argc==6) mix_events(argv[1],argv[2],argv[3],stoi(argv[4]),stoi(argv[5]));
    else if(argc==7) mix_events(argv[1],argv[2],argv[3],stoi(argv[4]),stoi(argv[5]),stoi(argv[6]));
    else if(argc==8) mix_events(argv[1],argv[2],argv[3],stoi(argv[4]),stoi(argv[5]),stoi(argv[6]),stoi(argv[7]));
}
void SimTree::Loop()
{
    //   In a ROOT session, you can do:
    //      root> .L SimTree.C
    //      root> SimTree t
    //      root> t.GetEntry(12); // Fill t data members with entry number 12
    //      root> t.Show();       // Show values of entry 12
    //      root> t.Show(16);     // Read and show values of entry 16
    //      root> t.Loop();       // Loop on all entries
    //

    //     This is the loop skeleton where:
    //    jentry is the global entry number in the chain
    //    ientry is the entry number in the current Tree
    //  Note that the argument to GetEntry must be:
    //    jentry for TChain::GetEntry
    //    ientry for TTree::GetEntry and TBranch::GetEntry
    //
    //       To read only selected branches, Insert statements like:
    // METHOD1:
    //    fChain->SetBranchStatus("*",0);  // disable all branches
    //    fChain->SetBranchStatus("branchname",1);  // activate branchname
    // METHOD2: replace line
    //    fChain->GetEntry(jentry);       //read all branches
    //by  b_branchname->GetEntry(ientry); //read only this branch
    if (fChain == 0) return;

    Long64_t nentries = fChain->GetEntriesFast();

    Long64_t nbytes = 0, nb = 0;
    for (Long64_t jentry=0; jentry<nentries;jentry++) {
	Long64_t ientry = LoadTree(jentry);
	if (ientry < 0) break;
	nb = fChain->GetEntry(jentry);   nbytes += nb;
	// if (Cut(ientry) < 0) continue;
    }
}

