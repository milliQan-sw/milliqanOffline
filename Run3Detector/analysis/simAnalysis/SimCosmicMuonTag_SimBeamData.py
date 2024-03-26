from SimCosmicMuonTag_V2 import *



if __name__ == "__main__":
    #beam data
    #Maybe Ryan can provide more infor about what are details in these file like how they are made
    fileName1 = "BeamsimFlat_dy_nophoton"
    fileName2 = "BeamsimFlat_qcd_nophoton"
    fileName3 = "BeamsimFlat_w_nophoton"

    

    branches = ["time","chan","runNumber","event","layer","nPE","type","row","muonHit"]

    fourRowBigHitsCut = mycuts.getCut(mycuts.fourRowBigHits, "fourRowBigHitsCut",cut=False)
    TBBigHitCut = mycuts.getCut(mycuts.TBBigHit,"placeholder", cut = False)
    P_TBBigHitCut= mycuts.getCut(mycuts.P_TBBigHit, "P_TBBigHitCut",cut = False)
    P_BBigHitCut= mycuts.getCut(mycuts.P_BBigHit, "P_BBigHitCut",cut = False)
    MuonCut = mycuts.getCut(mycuts.MuonEvent, "placeholder", CutonBars =True, branches=branches)
    MuonEventCut = mycuts.getCut(mycuts.MuonEvent, "placeholder", CutonBars =False, branches=branches)


    TBBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "TBBigHit")
    fourRowBigHitsCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "fourRowBigHits")
    P_TBBigHitCutCount= mycuts.getCut(mycuts.countEvent,"placeholder"  ,Countobject = "P_TBBigHit")
    P_BBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "P_BBigHit")

    #when the intial mask is MuonEventCut in the cutflow, then use the combined cut(mask) at below to do the counting and making polt.
    TBBigHit_M = mycuts.getCut(mycuts.combineCuts, 'TBBigHit_M', ["TBBigHit", "muonEvent"])
    fourRowBigHits_M = mycuts.getCut(mycuts.combineCuts, 'fourRowBigHits_M', ["fourRowBigHits", "muonEvent"])
    P_TBBigHit_M = mycuts.getCut(mycuts.combineCuts, 'P_TBBigHit_M', ["P_TBBigHit", "muonEvent"])
    P_BBigHit_M = mycuts.getCut(mycuts.combineCuts, 'P_BBigHit_M', ["P_BBigHit", "muonEvent"])


    TBBigHitCutCount_m = mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "TBBigHit_M")
    fourRowBigHitsCutCount_m = mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "fourRowBigHits_M")
    P_TBBigHitCutCount_m = mycuts.getCut(mycuts.countEvent,"placeholder"  ,Countobject = "P_TBBigHit_M")
    P_BBigHitCutCount_m = mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "P_BBigHit_M")



    #-------------------------section for making histograms---------------------------------------
    
    #plot for cutflow 1_default
    ChanVsbarNpe_TBBigHit_1D = r.TH2F("ChanVsbarNpe_TBBigHit_1D","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
    ChanVsbarNpe_P_TBBigHit_1D = r.TH2F("ChanVsbarNpe_P_TBBigHit_1D","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)

    myplotter.addHistograms(ChanVsbarNpe_TBBigHit_1D, ['chan','nPE'], 'TBBigHit')
    myplotter.addHistograms(ChanVsbarNpe_P_TBBigHit_1D, ['chan','nPE'], 'P_TBBigHit')

    #plot for cutflow 1_A
    ChanVsbarNpe_TBBigHit_1A = r.TH2F("ChanVsbarNpe_TBBigHit_1A","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
    ChanVsbarNpe_P_TBBigHit_1A = r.TH2F("ChanVsbarNpe_P_TBBigHit_1A","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)

    myplotter.addHistograms(ChanVsbarNpe_TBBigHit_1A, ['chan','nPE'], 'TBBigHit_M')
    myplotter.addHistograms(ChanVsbarNpe_P_TBBigHit_1A, ['chan','nPE'], 'P_TBBigHit_M')

    #plot for cutflow 1_B
    ChanVsbarNpe_TBBigHit_1B = r.TH2F("ChanVsbarNpe_TBBigHit_1B","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
    ChanVsbarNpe_P_TBBigHit_1B = r.TH2F("ChanVsbarNpe_P_TBBigHit_1B","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)

    myplotter.addHistograms(ChanVsbarNpe_TBBigHit_1B, ['chan','nPE'], 'TBBigHit')
    myplotter.addHistograms(ChanVsbarNpe_P_TBBigHit_1B, ['chan','nPE'], 'P_TBBigHit')
    



    



    #muon pdg number cut is not being used

    #muonCut remove the non-muon data. There is no need to change the counting script and tag for making the plot compared with cutflow3
    cutflow1_D = [MuonCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount,myplotter.dict['ChanVsbarNpe_TBBigHit_1D'],myplotter.dict['ChanVsbarNpe_P_TBBigHit_1D']]
    
    #counting script and drawing tag need to check if the current event is muon event.
    cutflow1_A = [MuonEventCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHit_M,TBBigHitCutCount_m,P_TBBigHitCut,P_TBBigHit_M,P_TBBigHitCutCount_m,myplotter.dict['ChanVsbarNpe_TBBigHit_1A'],myplotter.dict['ChanVsbarNpe_P_TBBigHit_1A']]

    cutflow1_B = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount,myplotter.dict['ChanVsbarNpe_TBBigHit_1B'],myplotter.dict['ChanVsbarNpe_P_TBBigHit_1B']]


    cutflow1_D_dict = {'cutflow1_D': cutflow1_D}
    cutflow1_A_dict = {'cutflow1_A': cutflow1_A}
    cutflow1_B_dict = {'cutflow1_B': cutflow1_B}

    def analysis(cutflow_dict,fileName,*args):

        cutflowName=next(iter(cutflow_dict.keys())) #retrieve the first key from the iterator returned by cutflow1_dict.keys()
        
        cutflow=cutflow_dict[cutflowName]
        
        print(f"the current cutflow is {cutflowName} with file {fileName}")


        myschedule = milliQanScheduler(cutflow, mycuts)

        filelist = [f'/mnt/hadoop/se/store/user/czheng/SimFlattree/beamSimFlat/{fileName}.root:t']

        myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)


        myiterator.run()
        f_out = r.TFile(f"BeamDatademo.root", "RECREATE")
        f_out.cd()
        for hist in args:
            hist.Write()
        f_out.Close()


   

    analysis(cutflow1_D_dict,fileName1,ChanVsbarNpe_TBBigHit_1D,ChanVsbarNpe_P_TBBigHit_1D)
    analysis(cutflow1_D_dict,fileName2)
    analysis(cutflow1_D_dict,fileName3)
    analysis(cutflow1_A_dict,fileName1)
    analysis(cutflow1_A_dict,fileName2)
    analysis(cutflow1_A_dict,fileName3)
    analysis(cutflow1_B_dict,fileName1)
    analysis(cutflow1_B_dict,fileName2)
    analysis(cutflow1_B_dict,fileName3)






