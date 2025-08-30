#include "TFile.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TChain.h"
#include "TDirectory.h"
#include "TGraph.h"
#include "TKey.h"
#include <iostream>
#include <utility>
#include <cmath>

using namespace std;

struct globalHist{
    float max2, min2;
    float max3, min3;
    float maxRatio;
    float nPEMaxRatio;
    float maxRatioTripleRate, maxRatioDoubleRate;
    float maxRatioErr;
};

float getRunTime(TChain* tchain, ULong_t* daqFileOpen, ULong_t* daqFileClose){
    float minTime = 10e12;
    float maxTime = 0;
    for (int ievent=0; ievent<tchain->GetEntries(); ievent++){
        tchain->GetEntry(ievent);
        if(*daqFileOpen < minTime) minTime = *daqFileOpen;
        if(*daqFileClose > maxTime) maxTime = *daqFileClose;
    }

    float totalTime = maxTime - minTime;
    return totalTime;
}

std::pair<int, int> getRun(int chan){

    //triple and double coincidence run for the given channel (index)
    vector<pair<int, int> > run_pairs = {
        /*{1703, 1808}, {1703, 1837}, {1703, 1809}, {1703, 1838}, {1703, 1810}, {1703, 1839}, {1703, 1811}, {1703, 1842},
        {1796, 1813}, {1872, 1843}, {1797, 1814}, {1873, 1845}, {1798, 1815}, {1874, 1846}, {1799, 1816}, {1875, 1847},

        {1703, 1817}, {1703, 1848}, {1703, 1818}, {1703, 1849}, {1703, 1820}, {1703, 1851}, {1703, 1821}, {1703, 1852},
        {1804, 1822}, {1880, 1853}, {1805, 1823}, {1881, 1855}, {1806, 1824}, {1889, 1856}, {1807, 1825}, {1883, 1857},

        {1703, 1827}, {1703, 1858}, {1703, 1828}, {1703, 1859}, {1703, 1829}, {1703, 1860}, {1703, 1830}, {1703, 1862},
        {1796, 1892}, {1872, 1890}, {1797, 1832}, {1873, 1864}, {1798, 1833}, {1874, 1865}, {1799, 1835}, {1875, 1866},

        {1703, 1808}, {1703, 1837}, {1703, 1809}, {1703, 1838}, {1703, 1810}, {1703, 1839}, {1703, 1811}, {1703, 1842},
        {1703, 1813}, {1703, 1843}, {1703, 1814}, {1703, 1845}, {1703, 1815}, {1703, 1846}, {1703, 1816}, {1703, 1847}*/

        {1792, 1808}, {1867, 1837}, {1793, 1809}, {1869, 1838}, {1794, 1810}, {1870, 1839}, {1795, 1811}, {1871, 1842},
        {1796, 1813}, {1872, 1843}, {1797, 1814}, {1873, 1845}, {1798, 1815}, {1874, 1846}, {1799, 1816}, {1875, 1847},

        {1800, 1817}, {1876, 1848}, {1801, 1818}, {1877, 1849}, {1802, 1820}, {1878, 1851}, {1803, 1821}, {1879, 1852},
        {1804, 1822}, {1880, 1853}, {1805, 1823}, {1881, 1855}, {1806, 1824}, {1889, 1856}, {1807, 1825}, {1883, 1857},

        {1792, 1827}, {1867, 1858}, {1793, 1828}, {1868, 1859}, {1794, 1829}, {1870, 1860}, {1795, 1830}, {1871, 1862},
        {1796, 1892}, {1872, 1890}, {1797, 1832}, {1873, 1864}, {1798, 1833}, {1874, 1865}, {1799, 1835}, {1875, 1866},

        {1800, 1808}, {1876, 1837}, {1801, 1809}, {1877, 1838}, {1802, 1810}, {1878, 1839}, {1803, 1811}, {1879, 1842},
        {1804, 1813}, {1880, 1843}, {1805, 1814}, {1881, 1845}, {1806, 1815}, {1889, 1846}, {1807, 1816}, {1883, 1847}
    };

    return run_pairs[chan];
}

std::pair<int, int> getCoincidentChannels(int chan){

    vector<pair<int, int> > doubleChannels = {
        {16, 32}, {17, 33}, {18, 34}, {19, 35}, {20, 36}, {21, 37}, {22, 38}, {23, 39},
        {78, 40}, {79, 41}, {26, 42}, {27, 43}, {28, 44}, {29, 45}, {30, 46}, {31, 47},

        {32, 48}, {33, 49}, {34, 50}, {35, 51}, {36, 52}, {37, 53}, {38, 54}, {39, 55},
        {40, 56}, {41, 57}, {42, 58}, {43, 59}, {44, 60}, {45, 61}, {46, 62}, {47, 63},

        {0, 16}, {1, 17}, {2, 18}, {3, 19}, {4, 20}, {5, 21}, {6, 22}, {7, 23},
        {8, 24}, {9, 25}, {10, 26}, {11, 27}, {12, 28}, {13, 29}, {14, 30}, {15, 31},

        {16, 32}, {17, 33}, {18, 34}, {19, 35}, {20, 36}, {21, 37}, {22, 38}, {23, 39},
        {78, 40}, {79, 41}, {26, 42}, {27, 43}, {28, 44}, {29, 45}, {30, 46}, {31, 47}
    };

    return doubleChannels[chan];
}

bool checkTimingDistance(pair<float, float>& t1, pair<float, float>& t2, float threshold){
    // check if ranges overlap
    if(
        (t2.first <= t1.second && t2.first >= t1.first) || 
        (t1.first <= t2.second && t1.first >= t2.first) ||
        (t2.second <= t1.second && t2.second >= t1.first) ||
        (t1.second <= t2.second && t1.second >= t2.first)
    ){
        return true;
    }
    //check if within threshold
    if(
        abs(t1.first - t2.first) <= threshold ||
        abs(t1.second - t2.first) <= threshold ||
        abs(t1.first - t2.second) <= threshold ||
        abs(t1.second - t2.second) <= threshold
    ){
        return true;
    }
    return false;
}

globalHist calculateRates(TFile* fout, int channel){

    //Initialize struct to return
    globalHist thisChan;

    // set time threshold for pulses to be within
    float threshold = 80.0;

    //Define variables that will be used
    vector<float>* v_nPE = nullptr;
    vector<bool>* v_pickupFlagTight = nullptr;
    vector<float>* v_time = nullptr;
    vector<int>* v_chan = nullptr;
    vector<float>* v_duration = nullptr;
    float tTrigger;
    bool boardsMatched;
    ULong_t daqFileOpen;
    ULong_t daqFileClose;

    // Set values of nPE cut to use
    vector<float> nPECuts;
    for (float i=0; i < 30; i++) nPECuts.push_back(0.1*i);

    // Set cuts used
    TString cutString = TString::Format("chan==%i && boardsMatched && timeFit_module_calibrated > 1100 && timeFit_module_calibrated < 1400 && ipulse==0", channel);

    // General directory to get files
    TString s_directory = "/store/user/milliqan/trees/v35/bar/";

    // Get the run numbers needed for this channel
    pair<int, int> run_pair = getRun(channel);

    // Get the double coincidence channels
    pair<int, int> double_coincidence = getCoincidentChannels(channel);

    // Find double coincidence
    TChain* c_double = new TChain("t");
    TString s_double = s_directory;
        if (run_pair.second >= 1700 && run_pair.second < 1800) s_double = s_double + "1700/";
        else if (run_pair.second >= 1800 && run_pair.second < 1900) s_double = s_double + "1800/";
        else {
            cout << "Error run is out of range 1700-1800" << endl;
            return thisChan;
        }
    s_double = s_double + TString::Format("MilliQan_Run%i.*.root", run_pair.second);

    c_double->Add(s_double);

    c_double->SetBranchAddress("nPE", &v_nPE);
    c_double->SetBranchAddress("pickupFlagTight", &v_pickupFlagTight);
    c_double->SetBranchAddress("boardsMatched", &boardsMatched);
    c_double->SetBranchAddress("daqFileOpen", &daqFileOpen);
    c_double->SetBranchAddress("daqFileClose", &daqFileClose);
    c_double->SetBranchAddress("timeFit_module_calibrated", &v_time);
    c_double->SetBranchAddress("chan", &v_chan);
    c_double->SetBranchAddress("duration", &v_duration);
    c_double->SetBranchAddress("tTrigger", &tTrigger);

    cout << "There are " << c_double->GetEntries() <<" double coincidence events" << endl;

    float timeDouble = getRunTime(c_double, &daqFileOpen, &daqFileClose);

    cout << "Total Run Time Double " << timeDouble <<  endl;

    //c_double->Draw("nPE>>hDouble(1000, 0, 100)", cutString);
    //TH1F* hDouble = (TH1F*)gDirectory->Get("hDouble");

    TH3F* hDouble = new TH3F("hDouble", "nPE Double Coincident Hits", 100, 0, 10, 100, 0, 10, 100, 0, 10);
    TH1F* hProbeNPE2 = new TH1F("hProbeNPE2", "nPE of Probe Channel for Double Coincident Hits", 1000, 0, 100);
    TH1F* hTag1NPE2 = new TH1F("hTag1NPE2", "nPE of 1st Tag Channel for Double Coincident Hits", 1000, 0, 100);
    TH1F* hTag2NPE2 = new TH1F("hTag2NPE2", "nPE of 2nd Tag Channel for Double Coincident Hits", 1000, 0, 100);

    for(int ievent=0; ievent < c_double->GetEntries(); ievent++){
        c_double->GetEntry(ievent);

        bool tripleCoincidence=false;
        vector<float> primaryNPE = {};
        vector<float> secondaryNPE1 = {};
        vector<float> secondaryNPE2 = {};
        vector<pair<float, float> > primaryChannel = {};
        vector<pair<float, float> > secondary1 = {};
        vector<pair<float, float> > secondary2 = {};
        
        if(!boardsMatched) continue;
        for(int ipulse=0; ipulse < v_nPE->size(); ipulse++){
            int this_chan = v_chan->at(ipulse);
            float this_time = v_time->at(ipulse);
            float this_duration = v_duration->at(ipulse);

            float end_time = this_time + this_duration;
            //cout << "time, duration, end time: " << this_time << ", " << this_duration << ", " << end_time << endl;

            if(this_chan != channel && this_chan != double_coincidence.first && this_chan != double_coincidence.second) continue;
            if(this_time < 1100 || this_time > 1500) continue;

            if(this_chan == channel){ 
                primaryChannel.push_back(pair<float, float>(this_time, end_time));
                primaryNPE.push_back(v_nPE->at(ipulse));
            }
            if(this_chan == double_coincidence.first) {
                secondary1.push_back(pair<float, float>(this_time, end_time));
                secondaryNPE1.push_back(v_nPE->at(ipulse));
            }
            if(this_chan == double_coincidence.second) {
                secondary2.push_back(pair<float, float>(this_time, end_time));
                secondaryNPE2.push_back(v_nPE->at(ipulse));
            }
        }

        for(int p=0; p < primaryChannel.size(); p++){
            for(auto& s1: secondary1){
                if (tripleCoincidence) break;
                //check for overlap
                bool checkThirdPulse = false;
                checkThirdPulse = checkTimingDistance(primaryChannel[p], s1, threshold);
                //if(checkThirdPulse) cout << "Found pulses within range: " << primaryChannel[p].first << "-" << primaryChannel[p].second << ", and " << s1.first << "-" << s1.second << endl;

                if (!checkThirdPulse) continue;

                for(auto& s2: secondary2){
                    bool coincident1 = checkTimingDistance(primaryChannel[p], s2, threshold);
                    if (!coincident1) continue;
                    bool coincident2 = checkTimingDistance(s1, s2, threshold);
                    if(coincident1 && coincident2){
                        tripleCoincidence = true;
                        break;
                    }
                }
            }
            if (tripleCoincidence){
                hDouble->Fill(primaryNPE[p], secondaryNPE1[p], secondaryNPE2[p]);
                hProbeNPE2->Fill(primaryNPE[p]);
                hTag1NPE2->Fill(secondaryNPE1[p]);
                hTag2NPE2->Fill(secondaryNPE2[p]);
                //cout << TString::Format("Filling Double with %f, %f, %f", primaryNPE[p], secondaryNPE1[p], secondaryNPE2[p]) << endl;
                break;
            }

        }

    }

    /////////////////////////////////////////////////
    // Now do same thing for triple coincidence
    /////////////////////////////////////////////////
    TChain* c_triple = new TChain("t");
    TString s_triple = s_directory;
    if (run_pair.first >= 1700 && run_pair.first < 1800) s_triple = s_triple + "1700/";
    else if (run_pair.first >= 1800 && run_pair.first < 1900) s_triple = s_triple + "1800/";
    else {
        cout << "Error run is out of range 1700-1800" << endl;
        return thisChan;
    }
    s_triple = s_triple + TString::Format("MilliQan_Run%i.*.root", run_pair.first);
    c_triple->Add(s_triple);

    c_triple->SetBranchAddress("nPE", &v_nPE);
    c_triple->SetBranchAddress("pickupFlagTight", &v_pickupFlagTight);
    c_triple->SetBranchAddress("boardsMatched", &boardsMatched);
    c_triple->SetBranchAddress("daqFileOpen", &daqFileOpen);
    c_triple->SetBranchAddress("daqFileClose", &daqFileClose);
    c_triple->SetBranchAddress("timeFit_module_calibrated", &v_time);
    c_triple->SetBranchAddress("chan", &v_chan);
    c_triple->SetBranchAddress("duration", &v_duration);
    c_triple->SetBranchAddress("tTrigger", &tTrigger);

    cout << "There are " << c_triple->GetEntries() <<" triple coincidence events" << endl;
    
    float timeTriple = getRunTime(c_triple, &daqFileOpen, &daqFileClose);

    cout << "Total Run Time Triple " << timeTriple << endl;

    //c_triple->Draw("nPE>>hTriple(1000, 0, 100)", cutString);
    //TH1F* hTriple = (TH1F*)gDirectory->Get("hTriple");

    TH3F* hTriple = new TH3F("hTriple", "nPE Triple Coincident Hits", 100, 0, 10, 100, 0, 10, 100, 0, 10);
    TH1F* hProbeNPE3 = new TH1F("hProbeNPE3", "nPE of Probe Channel for Triple Coincident Hits", 1000, 0, 100);
    TH1F* hTag1NPE3 = new TH1F("hTag1NPE3", "nPE of 1st Tag Channel for Triple Coincident Hits", 1000, 0, 100);
    TH1F* hTag2NPE3 = new TH1F("hTag2NPE3", "nPE of 2nd Tag Channel for Triple Coincident Hits", 1000, 0, 100);

    for(int ievent=0; ievent < c_triple->GetEntries(); ievent++){
        c_triple->GetEntry(ievent);

        bool tripleCoincidence=false;
        vector<float> primaryNPE = {};
        vector<float> secondaryNPE1 = {};
        vector<float> secondaryNPE2 = {};
        vector<pair<float, float> > primaryChannel = {};
        vector<pair<float, float> > secondary1 = {};
        vector<pair<float, float> > secondary2 = {};
        
        if(!boardsMatched) continue;
        //if(tTrigger != 2) continue;
        for(int ipulse=0; ipulse < v_nPE->size(); ipulse++){
            int this_chan = v_chan->at(ipulse);
            float this_time = v_time->at(ipulse);
            float this_duration = v_duration->at(ipulse);

            float end_time = this_time + this_duration;
            //cout << "time, duration, end time: " << this_time << ", " << this_duration << ", " << end_time << endl;

            if(this_chan != channel && this_chan != double_coincidence.first && this_chan != double_coincidence.second) continue;
            if(this_time < 1100 || this_time > 1500) continue;

            if(this_chan == channel){ 
                primaryChannel.push_back(pair<float, float>(this_time, end_time));
                primaryNPE.push_back(v_nPE->at(ipulse));
            }
            if(this_chan == double_coincidence.first) {
                secondary1.push_back(pair<float, float>(this_time, end_time));
                secondaryNPE1.push_back(v_nPE->at(ipulse));
            }
            if(this_chan == double_coincidence.second) {
                secondary2.push_back(pair<float, float>(this_time, end_time));
                secondaryNPE2.push_back(v_nPE->at(ipulse));
            }
        }

        for(int p=0; p < primaryChannel.size(); p++){
            for(auto& s1: secondary1){
                if (tripleCoincidence) break;
                //check for overlap
                bool checkThirdPulse = false;
                checkThirdPulse = checkTimingDistance(primaryChannel[p], s1, threshold);
                //if(checkThirdPulse) cout << "Found pulses within range: " << primaryChannel[p].first << "-" << primaryChannel[p].second << ", and " << s1.first << "-" << s1.second << endl;

                if (!checkThirdPulse) continue;

                for(auto& s2: secondary2){
                    bool coincident1 = checkTimingDistance(primaryChannel[p], s2, threshold);
                    if (!coincident1) continue;
                    bool coincident2 = checkTimingDistance(s1, s2, threshold);
                    if(coincident1 && coincident2){
                        tripleCoincidence = true;
                        break;
                    }
                }
            }
            if (tripleCoincidence){
                hTriple->Fill(primaryNPE[p], secondaryNPE1[p], secondaryNPE2[p]);
                hProbeNPE3->Fill(primaryNPE[p]);
                hTag1NPE3->Fill(secondaryNPE1[p]);
                hTag2NPE3->Fill(secondaryNPE2[p]);
                //cout << TString::Format("Filling hTriple with %f, %f, %f", primaryNPE[p], secondaryNPE1[p], secondaryNPE2[p]) << endl;
                break;
            }

        }

    }

    std::cout << "Event selection finished... creating ratio plots" << std::endl;

    // Now calculate rate of pulses in channels passing nPE cuts
    TString title2 = TString::Format("Rate of Double Coincidence Passing nPE Cut (Channel %i)", channel);
    TGraph* g_rate2 = new TGraph();
    g_rate2->SetTitle(title2+";nPE Cut;# Pulses");

    TString title3 = TString::Format("Rate of Triple Coincidence Passing nPE Cut (Channel %i)", channel);
    TGraph* g_rate3 = new TGraph();
    g_rate3->SetTitle(title3+";nPE Cut;# Pulses");

    TString title = TString::Format("Ratio of Triple/Double Coincidence vs nPE Cut (Channel %i)", channel);
    TGraph* g_rate = new TGraph();
    g_rate->SetTitle(title+";nPE Cut;Ratio(Triple/Double)");


    float min2 = 10e12;
    float max2 = -1;
    float min3 = 10e12;
    float max3 = -1;
    float maxRatio = -1;
    float nPEMaxRatio = -1;
    float maxRatioTripleRate, maxRatioDoubleRate;
    float maxRatioErr = 0;

    int points = 0;
    for(auto& cut : nPECuts){
        double cutBin = (double)cut;
        int xbin_low = hTriple->GetXaxis()->FindFixBin(cutBin);
        int xbin_high = hTriple->GetNbinsX()+1;
        int ybin_low = hTriple->GetYaxis()->FindFixBin(cutBin);
        int ybin_high = hTriple->GetNbinsY()+1;
        int zbin_low = hTriple->GetZaxis()->FindFixBin(cutBin);;
        int zbin_high = hTriple->GetNbinsZ()+1;
        float countTriple = hTriple->Integral(xbin_low, xbin_high, ybin_low, ybin_high, zbin_low, zbin_high);
        float countDouble = hDouble->Integral(xbin_low, xbin_high, ybin_low, ybin_high, zbin_low, zbin_high);
        //float totalTriple = hTriple->Integral(0, hTriple->GetNbinsX()+1, 0, hTriple->GetNbinsY()+1, 0, hTriple->GetNbinsZ()+1);
        //cout << TString::Format("Cut: %f, countDouble %f, coundTriple %f, binx %i, biny %i, binz %i, totalIntegral %f", cutBin, countDouble, countTriple, xbin_low, ybin_low, zbin_low, totalTriple) << std::endl;

        float rateTriple = countTriple / timeTriple;
        float rateDouble = countDouble / timeDouble;

        g_rate2->SetPoint(points, cut, rateDouble);
        g_rate3->SetPoint(points, cut, rateTriple);
        float ratio = 1.;
        float errRatio = 0;
        if (rateDouble > 0) {
            ratio = rateTriple/rateDouble;
            if(rateTriple>0) errRatio = ratio * sqrt(pow(1/sqrt(rateTriple), 2) + pow(1/sqrt(rateDouble), 2));
            else errRatio = 0;
        }
        g_rate->SetPoint(points, cut, ratio);
        points++;

        if (rateDouble < min2) min2 = rateDouble;
        if (rateDouble > max2) max2 = rateDouble;
        if (rateTriple < min3) min3 = rateTriple;
        if (rateTriple > max3) max3 = rateTriple;
        if (ratio > maxRatio) {
            maxRatio = ratio;
            nPEMaxRatio = cut;
            maxRatioTripleRate = rateTriple;
            maxRatioDoubleRate = rateDouble;
            maxRatioErr = errRatio;
        }
    }

    thisChan.min2 = min2;
    thisChan.max2 = max2;
    thisChan.min3 = min3;
    thisChan.max3 = max3;
    thisChan.maxRatio = maxRatio;
    thisChan.nPEMaxRatio = nPEMaxRatio;
    thisChan.maxRatioDoubleRate = maxRatioDoubleRate;
    thisChan.maxRatioTripleRate = maxRatioTripleRate;
    thisChan.maxRatioErr = maxRatioErr;

    std::cout << "Creating canvases and writing to file... " << std::endl;

    TCanvas* c1 = new TCanvas("c1", "Trigger Efficiencies", 800, 600);
    c1->cd();
    g_rate2->SetTitle(TString::Format("Coincidence Rates vs nPE Cut (Channel %i)", channel));
    g_rate2->SetMarkerStyle(8);
    g_rate2->SetMarkerSize(1);
    g_rate2->Draw("P");
    g_rate3->SetMarkerColor(kRed);
    g_rate3->SetMarkerStyle(8);
    g_rate3->SetMarkerSize(1);
    g_rate3->Draw("same P");
    c1->SetLogy();

    TLegend* l1 = new TLegend(0.7, 0.9, 0.7, 0.9);
    l1->AddEntry(g_rate2, "Double Coincidence Rate", "P");
    l1->AddEntry(g_rate3, "Triple Coincidence Rate", "P");
    l1->Draw();

    TCanvas* c2 = new TCanvas("c2", "c2", 800, 600);
    c2->cd();
    g_rate->SetMarkerStyle(8);
    g_rate->Draw("P");
    c2->SetLogy();

    TString dir = TString::Format("channel%i", channel);
    fout->mkdir(dir);
    fout->cd(dir);
    hTriple->Write("tripleCoincidenceCount");
    hDouble->Write("doubleCoincidenceCount");
    hProbeNPE2->Write();
    hProbeNPE3->Write();
    hTag1NPE2->Write();
    hTag2NPE2->Write();
    hTag1NPE3->Write();
    hTag2NPE3->Write();
    g_rate2->Write("doubleCoincidenceRate");
    g_rate3->Write("tripleCoincidenceRate");
    c1->Write("individualRates");
    c2->Write("ratioRates");

    return thisChan;

}

void calculateTriggerEfficienciesMod(){

    //gStyle->SetOptStat(0);
    gROOT->SetBatch(1);

    //output file for plots
    TFile* fout = TFile::Open("triggerEfficiencyPlots.root", "RECREATE");

    //initialize some global histograms
    TGraph* doubleRatesMax = new TGraph();
    TGraph* doubleRatesMin = new TGraph();
    TGraph* tripleRatesMax = new TGraph();
    TGraph* tripleRatesMin = new TGraph();
    TGraphErrors* allRatios = new TGraphErrors();
    TGraph* maxRatioVNPE = new TGraph();
    TGraph* maxNPECut = new TGraph();
    TGraph* maxRatioRatesGood = new TGraph();
    TGraph* maxRatioRatesBad = new TGraph();

    vector<bool> goodRatio = {};
    float maxRate = -1;
    float minRate = 10e12;
    for(int ichan=0; ichan < 64; ichan++){
        //if (ichan > 10) break;
        globalHist thisChan = calculateRates(fout, ichan);
        //cout << "channel: " << ichan << ", max2 " << thisChan.max2 << ", min2 " << thisChan.min2 << endl;
        doubleRatesMax->SetPoint(ichan, ichan, thisChan.max2);
        doubleRatesMin->SetPoint(ichan, ichan, thisChan.min2);
        tripleRatesMax->SetPoint(ichan, ichan, thisChan.max3);
        tripleRatesMin->SetPoint(ichan, ichan, thisChan.min3);
        allRatios->SetPoint(ichan, ichan, thisChan.maxRatio);
        cout << "Error point " << ichan << ", " << thisChan.maxRatioErr << std::endl;
        allRatios->SetPointError(ichan, 0, thisChan.maxRatioErr);
        maxRatioVNPE->SetPoint(ichan, thisChan.nPEMaxRatio, thisChan.maxRatio);
        maxNPECut->SetPoint(ichan, ichan, thisChan.nPEMaxRatio);

        if (thisChan.min2 < minRate) minRate = thisChan.min2;
        if (thisChan.min3 < minRate) minRate = thisChan.min3;
        if (thisChan.max2 > maxRate) maxRate = thisChan.max2;
        if (thisChan.max3 > maxRate) maxRate = thisChan.max3;

        if(thisChan.maxRatio >= 1){
            maxRatioRatesGood->SetPoint(ichan, thisChan.maxRatioDoubleRate, thisChan.maxRatioTripleRate);
            goodRatio.push_back(true);
        } 
        else {
            goodRatio.push_back(false);
            maxRatioRatesBad->SetPoint(ichan, thisChan.maxRatioDoubleRate, thisChan.maxRatioTripleRate);
        }
    }

    doubleRatesMax->SetTitle("Max Double Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    doubleRatesMin->SetTitle("Min Double Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    tripleRatesMax->SetTitle("Max Triple Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    tripleRatesMin->SetTitle("Min Triple Coincidence Rate per Channel; Channel; Coincidence Rate (1/s)");
    allRatios->SetTitle("Max Triple/Double Coincidence Ratio per Channel; Channel; Coincidence Rate Ratio");
    maxRatioVNPE->SetTitle("Max Coincidence Ratio vs nPE Cut; nPE Cut; Coincidence Rate Ratio");
    maxNPECut->SetTitle("NPE Cut Giving Max Coincidence Ratio; Channel; nPE Cut");
    maxRatioRatesGood->SetTitle("Double and Triple Coincidence Rates for Max Ratio;Double Coincidence Rate;Triple Coincidence Rate");
    maxRatioRatesBad->SetTitle("Double and Triple Coincidence Rates for Max Ratio;Double Coincidence Rate;Triple Coincidence Rate");


    TCanvas* c1 = new TCanvas("c1", "Max and Min Coincidence Rates", 1000, 800);
    c1->cd();
    doubleRatesMax->SetTitle("Max/Min Coincidence Rates Per Channel");
    doubleRatesMax->GetYaxis()->SetRangeUser(minRate*0.9, maxRate*1.1);
    doubleRatesMax->GetXaxis()->SetRangeUser(-2, 65);
    doubleRatesMin->GetXaxis()->SetRangeUser(-2, 65);
    tripleRatesMax->GetXaxis()->SetRangeUser(-2, 65);
    tripleRatesMin->GetXaxis()->SetRangeUser(-2, 65);
    allRatios->GetXaxis()->SetRangeUser(-2, 65);

    doubleRatesMax->SetMarkerStyle(23);
    doubleRatesMax->SetMarkerColor(kRed);
    doubleRatesMin->SetMarkerStyle(22);
    doubleRatesMin->SetMarkerColor(kRed);
    tripleRatesMax->SetMarkerStyle(23);
    tripleRatesMax->SetMarkerColor(kBlue);
    tripleRatesMin->SetMarkerStyle(22);
    tripleRatesMin->SetMarkerColor(kBlue);

    fout->cd();
    doubleRatesMax->Write("doubleRatesMax");
    doubleRatesMin->Write("doubleRatesMin");
    tripleRatesMax->Write("tripleRatesMax");
    tripleRatesMin->Write("tripleRatesMin");
    allRatios->Write("allRatios");

    doubleRatesMax->Draw("P");
    doubleRatesMin->Draw("same P");
    tripleRatesMax->Draw("same P");
    tripleRatesMin->Draw("same P");

    for(int i=0; i < doubleRatesMax->GetN(); i++){
        double x1, y1, x2, y2;
        doubleRatesMin->GetPoint(i, x1, y1); // Get point from graph1
        doubleRatesMax->GetPoint(i, x2, y2); // Get point from graph2

        // Create a line connecting the two points
        TLine* line1 = new TLine(x1, y1, x2, y2);
        line1->SetLineColor(kRed); // Set line color
        line1->Draw("SAME"); // Draw the line on the same canvas

        tripleRatesMin->GetPoint(i, x1, y1); // Get point from graph1
        tripleRatesMax->GetPoint(i, x2, y2); // Get point from graph2

        // Create a line connecting the two points
        TLine* line2 = new TLine(x1, y1, x2, y2);
        line2->SetLineColor(kBlue); // Set line color
        line2->Draw("SAME"); // Draw the line on the same canvas
    }

    TLegend* l1 = new TLegend(0.8, 0.9, 0.7, 0.9);
    l1->AddEntry(doubleRatesMax, "Max/Min Double Coincidence Rate", "P");
    l1->AddEntry(tripleRatesMax, "Max/Min Triple Coincidence Rate", "P");
    l1->Draw();

    TCanvas* c2 = new TCanvas("c2", "Max Coincidence Ratio", 1000, 800);
    c2->cd();
    allRatios->SetMarkerStyle(8); //make this a TError graph
    allRatios->Draw("P");
    TLine* line3 = new TLine(0, 1, 64, 1);
    line3->SetLineColor(kRed);
    line3->SetLineStyle(9);
    line3->Draw("same");

    TCanvas* c3 = new TCanvas("c3", "NPE Cut Max Ratio", 1000, 800);
    c3->cd();
    maxNPECut->SetMarkerStyle(8);
    maxNPECut->Draw("P");

    TCanvas* c4 = new TCanvas("c4", "NPE Cut Max vs Coincidence Ratio", 1000, 800);
    c4->cd();
    maxRatioVNPE->SetMarkerStyle(8);
    maxRatioVNPE->Draw("P");

    TCanvas* c5 = new TCanvas("c5", "All Triple Coincidence Rates", 1000, 800);
    TCanvas* c6 = new TCanvas("c6", "All Double Coincidence Rates", 1000, 800);

    // Get the list of keys in the file
    TIter next(fout->GetListOfKeys());
    TKey* key;

    int countDirs = 0;
    // Loop over all keys
    while ((key = (TKey*)next())) {
        // Check if the key is a directory
        if (strcmp(key->GetClassName(), "TDirectoryFile") == 0) {
            TDirectory* dir = (TDirectory*)key->ReadObj();

            bool goodChan = goodRatio[countDirs];

            TGraph* graph;
            TString s_dir = dir->GetName();
            fout->GetObject(s_dir+TString("/tripleCoincidenceRate"), graph);
            if (goodChan) graph->SetMarkerColor(kBlue);
            else graph->SetMarkerColor(kRed);
            c5->cd();
            graph->Draw("same");
            fout->GetObject(s_dir+TString("/doubleCoincidenceRate"), graph);
            if (goodChan) graph->SetMarkerColor(kBlue);
            else graph->SetMarkerColor(kRed);
            c6->cd();
            graph->Draw("same");

            // If you modify any objects, make sure to write them back
            dir->Write(); // Writes all objects in the current directory

            countDirs++;
        }
    }

    TCanvas* c7 = new TCanvas("c7", "c7", 1000, 800);
    c7->cd();
    maxRatioRatesGood->SetMarkerStyle(8);
    maxRatioRatesGood->SetMarkerColor(kBlue);
    maxRatioRatesGood->Draw("P");
    maxRatioRatesBad->SetMarkerStyle(8);
    maxRatioRatesBad->SetMarkerColor(kRed);
    maxRatioRatesBad->Draw("P");

    TLegend* l2 = new TLegend(0.7, 0.9, 0.7, 0.9);
    l2->AddEntry(maxRatioRatesGood, "Ratio >= 1", "P");
    l2->AddEntry(maxRatioRatesBad, "Ratio < 1", "P");
    l2->Draw("same");

    //save empty versions to file
    fout->cd();
    maxNPECut->Write("maxNPECut");
    maxRatioVNPE->Write("maxRatioVNPE");
    maxRatioRatesGood->Write("maxRatioRatesGood");
    maxRatioRatesBad->Write("maxRatioRatesBad");

    c1->Write("MaxCoincidenceRates");
    c2->Write("MaxCoincidenceRatio");
    c3->Write("MaxNPECutVChannel");
    c4->Write("MaxCoincidenceRateVNPE");
    c5->Write("AllTripleCoincidences");
    c6->Write("AllDoubleCoincidences");
    c7->Write("MaxRatioRates");
    fout->Close();

    return;
}