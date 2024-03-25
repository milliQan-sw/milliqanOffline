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


    #-------------------------section for making histograms---------------------------------------
    ChanVsbarNpe_TBBigHit = r.TH2F("ChanVsbarNpe_TBBigHit","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)
    ChanVsbarNpe_P_TBBigHit = r.TH2F("ChanVsbarNpe_P_TBBigHit","bar chanvsmpe tag1;chan; bar NPE", 80,0,80,200,0,100000)

    myplotter.addHistograms(ChanVsbarNpe_TBBigHit, ['chan','nPE'], 'TBBigHit')
    myplotter.addHistograms(ChanVsbarNpe_P_TBBigHit, ['chan','nPE'], 'P_TBBigHit')

    #muon pdg number cut is not being used
    cutflow1 = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount,myplotter.dict['ChanVsbarNpe_TBBigHit'],myplotter.dict['ChanVsbarNpe_P_TBBigHit']]
    
    cutflow1_dict = {'cutflow1': cutflow1}

    def analysis(cutflow_dict,fileName):

        cutflowName=next(iter(cutflow1_dict.keys())) #retrieve the first key from the iterator returned by cutflow1_dict.keys()
        
        cutflow=cutflow_dict[cutflowName]
        
        myschedule = milliQanScheduler(cutflow, mycuts)

        filelist = [f'/mnt/hadoop/se/store/user/czheng/SimFlattree/beamSimFlat/{fileName}.root:t']

        myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)


        myiterator.run()
        f_out = r.TFile(f"BeamDatademo.root", "RECREATE")
        f_out.cd()
        if cutflowName == cutflow1:
            ChanVsbarNpe_TBBigHit.Write()
            ChanVsbarNpe_P_TBBigHit.Write()
        #change the else statement to other cutflows
        else:
            pass
        f_out.Close()



    analysis(cutflow1_dict,fileName1)






