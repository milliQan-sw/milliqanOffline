from SimCosmicMuonTag_V2 import *

branches = ["height","timeFit_module_calibrated","chan","runNumber","column","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row","area"]

#use this one after pickup and board matching cut
def offlinePreProcess(self,cutName = None, cut = None, startTime = 1000, endTime = 1500):
    removePulse_T = (self.events["timeFit_module_calibrated"] >= startTime) & (self.events["timeFit_module_calibrated"] <=endTime)
    #debug:
    #print(f"before removing the pulse time data is {self.events['timeFit_module_calibrated']}")
    


    """
    for branch in branches:
        print(f"i am in for loop {branch}")
        if branch == "runNumber" or "event" or "fileNumber" or "boardsMatched"  or "timeFit_module_calibrated":
            continue
        
        print("reach here")
        print(branch)
        self.events[branch] = self.events[branch][removePulse_T]
    """
    #for loop doesn't work for unknown reason.
    self.events["height"] = self.events["height"][removePulse_T]
    self.events["chan"] = self.events["chan"][removePulse_T]
    self.events["column"] = self.events["column"][removePulse_T]
    self.events["pickupFlag"] = self.events["pickupFlag"][removePulse_T]
    self.events["layer"] = self.events["layer"][removePulse_T]
    self.events["nPE"] = self.events["nPE"][removePulse_T]
    self.events["type"] = self.events["type"][removePulse_T]
    self.events["row"] = self.events["row"][removePulse_T]
    self.events["area"] = self.events["area"][removePulse_T]
    self.events["timeFit_module_calibrated"] = self.events["timeFit_module_calibrated"][removePulse_T]
    #print(ak.count(
    #print(f"after removing the pulse time data is {self.events['timeFit_module_calibrated']}")

setattr(milliqanCuts, 'offlinePreProcess',offlinePreProcess)  

if __name__ == "__main__":

    #FIXME: The offline file path need to be fixed
    """
    def getFile(processNum, fileList):

        filelist = open(fileList)
        files = json.load(filelist)['filelist']
        filelist.close()

        return files[processNum]

    #run number, filelist
    processNum = int(sys.argv[1])
    fileList = sys.argv[2]


    #get the filename to run over
    filename = getFile(processNum, fileList)

    if('.root' in filename and 'output' in filename):
        numRun = filename.split('_')[1].split('.')[0].replace('Run', '')

    #filelist =['/mnt/hadoop/se/store/user/czheng/SimFlattree/offlinefile/output_1.root:t']
    filelist =[f'{filename}:t']
    """

    #----------------------------------------------------------------------------------------------------------------------------------- OSU T3
    #signle file test
    #numRun = 1190
    #fileNum = 2
    #numRun = str(sys.argv[1])
    #fileNum = str(sys.argv[2])
    #filelist =[f'/store/user/milliqan/trees/v34/1100/MilliQan_Run{numRun}.{fileNum}_v34.root:t']


    #------------------------------------------------------------------------------------------------
    #path for the milliqan machine

    #print("this is numRun" + str(sys.argv[1]) )


    numRun = str(sys.argv[1])
    fileNum = str(sys.argv[2])
    filelist =[f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_Run{numRun}.{fileNum}_v34.root:t']
    print(filelist)

    outputPath = str(sys.argv[3]) # the path is used at the very end for the output txt file
    print(outputPath)
    #-----------------------------------OSU T3--------------------------------------------------------
    #FIXME: The offline file path need to be fixed
    #multiple file test(non recommend to use due to time consuming)
    """
    filelist = []

    def appendRun(filelist):
        directory = "/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhoton/"
        for filename in os.listdir(directory):
            if filename.startswith("output") and filename.endswith(".root"):
                filelist.append(directory+filename+":t")


    appendRun(filelist)
    """
    

    



    #test cut flow. Check if the mask can be made
    #cutflow = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,mycuts.fourRowBigHits,mycuts.TBBigHit,mycuts.P_TBBigHit,mycuts.P_BBigHit]
    
    #"""
    #FIXME: removing entired events in array leads to MQplotter failure to work. I comment this out temporaly.
    #based on prior research, we concluded that we should use the muon straight line to tag muon event instead of the the following cuts.


    fourRowBigHitsCut = mycuts.getCut(mycuts.fourRowBigHits, "fourRowBigHitsCut",cut=True)
    TBBigHitCut = mycuts.getCut(mycuts.TBBigHit,"placeholder", cut = True)
    P_TBBigHitCut= mycuts.getCut(mycuts.P_TBBigHit, "P_TBBigHitCut",cut = True)
    P_BBigHitCut= mycuts.getCut(mycuts.P_BBigHit, "P_BBigHitCut",cut = True)
    CosmuonTagIntialization = mycuts.getCut(mycuts.CosmuonTagIntialization,"placeholder",cut = None, NPEcut = 20,offline= True)

    TBBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "TBBigHit")
    fourRowBigHitsCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "fourRowBigHits")
    P_TBBigHitCutCount= mycuts.getCut(mycuts.countEvent,"placeholder"  ,Countobject = "P_TBBigHit")
    P_BBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "P_BBigHit")
    #NbarsHitsCount1= mycuts.getCut(mycuts.P_BBigHit, "NBarsHits",cut = None,hist = NBarsHitTag1)#FIXME: getCut can't take hist as argument. Maybe I should remove it
    #cutflowSTD = [mycuts.MuonEvent,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,mycuts.NbarsHitsCount ,myplotter.dict['NBarsHitTag2']] #default analysis cutflow
    



    #Cut flow 1. This one is for testing the cut efficiency of different tags. TB big hits - > TB + panel big hits 
    
    cutflow1 = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount,mycuts.sudo_straight]
  


    #Cut flow 2. This one is for testing the cut efficiency of different tags. TB big hits - > 4 rows big hits
    cutflow2 = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,fourRowBigHitsCut,fourRowBigHitsCutCount]

    #cut flow 3. This one is for testing the cut efficiency of different tags. B + panel big hits  - > TB + panel big hits 
    cutflow3 = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,CosmuonTagIntialization,P_BBigHitCut,P_BBigHitCutCount,TBBigHitCut,P_TBBigHitCut,P_TBBigHitCutCount]
    #"""

    #-----------------------------muon straight line cut-------------------
    M_NPE = r.TH1F("M_NPE", "nPE muon event layer", 100, 0, 100)
    M_adj_NPE = r.TH1F("M_adj_NPE", "nPE muon event adjacnet layer", 100, 0, 100)
    myplotter.addHistograms(M_NPE, 'nPE', 'MuonLayers')
    myplotter.addHistograms(M_adj_NPE, 'nPE', 'MuonADJLayers')
    NuniqueBar = r.TH1F("NuniqueBar" , "NuniqueBar;number of unique bar;events",50,0,50)
    myplotter.addHistograms(NuniqueBar, 'NBarsHits', 'StraghtCosmic')
    CorrectTime =  r.TH1F("CorrectTime" , "D_t Max with correction w;D_t Max; Events",5000,0,5000)
    myplotter.addHistograms(CorrectTime, 'DT_CorrectTime', 'StraghtCosmic')
    NPERatio = r.TH1F("NPERatio","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    myplotter.addHistograms(NPERatio, 'BarNPERatio', 'StraghtCosmic')
   

    
    findCorrectTimeOL = mycuts.getCut(mycuts.findCorrectTime,"DT_CorrectTime", cut = False, timeData = "timeFit_module_calibrated")    
    myplotter.addHistograms(CorrectTime, 'DT_CorrectTime', 'StraghtCosmic')
    #data missing occurs
    cutflow6 = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.BarNPERatioCalculate,mycuts.NbarsHitsCount,findCorrectTimeOL,mycuts.sudo_straight,myplotter.dict['CorrectTime'],myplotter.dict['M_NPE'],myplotter.dict['M_adj_NPE'],myplotter.dict["NuniqueBar"],myplotter.dict["NPERatio"]]
    
    
    #cutflow 7 for finding the clean muon events
    cleanMuon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'Clean_MuonEvent')
    clean_Muon_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_layer', ["MuonLayers","Clean_MuonEvent"])
    clean_Muon_adj_layer = mycuts.getCut(mycuts.combineCuts, 'clean_Muon_adj_layer', ["MuonADJLayers","Clean_MuonEvent"])
    clean_Muon_Dt = mycuts.getCut(mycuts.findCorrectTime, 'placeholder',cut = None,timeData = "timeFit_module_calibrated")
    M_NPE_C = r.TH1F("M_NPE_C", "nPE muon event layer", 100, 0, 100)
    M_adj_NPE_C = r.TH1F("M_adj_NPE_C", "nPE muon event adjacnet layer", 100, 0, 100)
    myplotter.addHistograms(M_NPE_C, 'nPE', 'clean_Muon_layer')
    myplotter.addHistograms(M_adj_NPE_C	, 'nPE', 'clean_Muon_adj_layer')
    NuniqueBar_C = r.TH1F("NuniqueBar_C" , "NuniqueBar;number of unique bar;events",50,0,50)
    myplotter.addHistograms(NuniqueBar_C, 'NBarsHits', 'Clean_MuonEvent')

    #npe ratio with hits from adjacent layers 
    #
    NpeRatio_adj = r.TH1F("NpeRatio_adj","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    NpeRatio_adj_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_adj_tag",cut = "MuonADJLayers") 
    myplotter.addHistograms(NpeRatio_adj, 'NpeRatio_adj_tag', 'Clean_MuonEvent')

    #non- muon layer
    NpeRatio_ot_tag= mycuts.getCut(mycuts.BarNPERatioCalculateV2, "NpeRatio_ot_tag",cut = "MuonADJLayers")
    NpeRatio_ot = r.TH1F("NpeRatio_ot","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    myplotter.addHistograms(NpeRatio_ot, 'NpeRatio_ot_tag', 'Clean_MuonEvent')


    
    #extra histogram for Offline data
    CorrectTime_OL =  r.TH1F("CorrectTime_OL" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
    myplotter.addHistograms(CorrectTime_OL, 'DTL0L3', 'Clean_MuonEvent') 
    #CorrectTime_default_OL is to check what does CorrectTime should look like without the Clean muon cut
    CorrectTime_default_OL =  r.TH1F("CorrectTime_default_OL" , "D_t Max with correction w;D_t Max; Events",6000,-3000,3000)
    myplotter.addHistograms(CorrectTime_default_OL, 'DTL0L3', 'StraghtCosmic') 



    NPERatio_C = r.TH1F("NPERatio_C","NPE ratio;max NPE/min NPE;Events",5000,0,5000)
    myplotter.addHistograms(NPERatio_C, 'BarNPERatio', 'Clean_MuonEvent')
    #FIXME:mycuts.offlinePreProcess   this method cause the find correctTime crash 
    cutflow7 = [mycuts.offlinePreProcess,mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.BarNPERatioCalculate,mycuts.NbarsHitsCount,mycuts.sudo_straight,NpeRatio_adj_tag,NpeRatio_ot_tag,clean_Muon_layer,clean_Muon_adj_layer,cleanMuon_count,clean_Muon_Dt,myplotter.dict['M_NPE_C'],myplotter.dict['M_adj_NPE_C'],myplotter.dict["NuniqueBar_C"],myplotter.dict["NPERatio_C"],myplotter.dict["CorrectTime_OL"],myplotter.dict["CorrectTime_default_OL"],myplotter.dict["NpeRatio_adj"],myplotter.dict["NpeRatio_ot"]]    
    

    #cutflow 8 check the NPE and area distribution with tag downwardPath, StraghtCosmic,Clean_MuonEvent. Please beware panel hit are not being checked. When making the NPE and area plot wtih run 1163, I used first 200 files.
  
    #new count for downwardPath
    DW_Muon_count = mycuts.getCut(mycuts.countEvent,'placeholder', Countobject= 'downwardPath')

    #histograms for downwardPath
    Bar_Area_DW = r.TH1F("Bar_Area_DW", "area bar; area ; pulse", 7000, 0, 700000)
    Bar_NPE_DW = r.TH1F("Bar_NPE_DW", "nPE bar; nPE ; pulse", 500, 0, 1000)
    Slab_Area_DW = r.TH1F("Slab_Area_DW", "area Slab; area ; pulse", 7000, 0, 700000)
    #for offline file V34, the npe is the same as pulse area. So I only draw the 2D histogram for bars
    Bar_NPE_Area_DW = r.TH2F("Bar_NPE_Area_DW", "bar channels; nPE; area",20,0,1000,20, 0, 700000)
    NuniqueBar_DW = r.TH1F("NuniqueBar_DW" , "NuniqueBar DW;number of unique bar;events",50,0,50)
    myplotter.addHistograms(NuniqueBar_DW, 'NBarsHits', 'downwardPath')


    #histograms for StraghtCosmic
    Bar_Area_St = r.TH1F("Bar_Area_St", "area bar; area ; pulse", 7000, 0, 700000)
    Bar_NPE_St = r.TH1F("Bar_NPE_St", "nPE bar; nPE ; pulse", 500, 0, 1000)
    Slab_Area_St = r.TH1F("Slab_Area_St", "area Slab; area ; pulse", 7000, 0, 700000)
    Bar_NPE_Area_St = r.TH2F("Bar_NPE_Area_St", "bar channels; nPE; area",20,0,1000,20, 0, 700000)

    #histograms for Clean_MuonEvent
    Bar_Area_CL = r.TH1F("Bar_Area_CL", "area bar; area ; pulse", 7000, 0, 700000)
    Bar_NPE_CL = r.TH1F("Bar_NPE_CL", "nPE bar; nPE ; pulse", 500, 0, 1000)
    Slab_Area_CL = r.TH1F("Slab_Area_CL", "area Slab; area ; pulse", 7000, 0, 700000)
    Bar_NPE_Area_CL = r.TH2F("Bar_NPE_Area_CL", "bar channels; nPE; area",20,0,1000,20, 0, 700000)


    #adding combine cuts for downwardPath
    dw_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'dw_bar_cf8', ["downwardPath", "barCut"])
    dw_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'dw_panel_cf8', ["downwardPath", "panelCut"])

    #adding combine cuts for StraghtCosmic
    St_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'St_bar_cf8', ["StraghtCosmic", "barCut"])
    St_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'St_panel_cf8', ["StraghtCosmic", "panelCut"])

    #adding combine cuts for Clean_MuonEvent
    CL_bar_cf8 = mycuts.getCut(mycuts.combineCuts, 'CL_bar_cf8', ["Clean_MuonEvent", "barCut"])
    CL_panel_cf8 = mycuts.getCut(mycuts.combineCuts, 'CL_panel_cf8', ["Clean_MuonEvent", "panelCut"])




    #add hists with tags
    myplotter.addHistograms(Bar_Area_DW, 'area', 'dw_bar_cf8')
    myplotter.addHistograms(Bar_NPE_DW, 'nPE', 'dw_bar_cf8')
    myplotter.addHistograms(Slab_Area_DW, 'area', 'dw_panel_cf8')
    myplotter.addHistograms(Bar_NPE_Area_DW, ['nPE','area'], 'dw_bar_cf8')

    myplotter.addHistograms(Bar_Area_St, 'area', 'St_bar_cf8')
    myplotter.addHistograms(Bar_NPE_St, 'nPE', 'St_bar_cf8')
    myplotter.addHistograms(Slab_Area_St, 'area', 'St_panel_cf8')
    myplotter.addHistograms(Bar_NPE_Area_St, ['nPE','area'], 'St_bar_cf8')


    myplotter.addHistograms(Bar_Area_CL, 'area', 'CL_bar_cf8')
    myplotter.addHistograms(Bar_NPE_CL, 'nPE', 'CL_bar_cf8')
    myplotter.addHistograms(Slab_Area_CL, 'area', 'CL_panel_cf8')
    myplotter.addHistograms(Bar_NPE_Area_CL, ['nPE','area'], 'CL_bar_cf8')


  









    cutflow8 = [mycuts.offlinePreProcess,mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.NbarsHitsCount,mycuts.sudo_straight,dw_bar_cf8,dw_panel_cf8,St_bar_cf8,St_panel_cf8,CL_bar_cf8,CL_panel_cf8,DW_Muon_count,cleanMuon_count,myplotter.dict['NuniqueBar_DW'],myplotter.dict['Bar_Area_DW'],myplotter.dict['Bar_NPE_DW'],myplotter.dict['Slab_Area_DW'],myplotter.dict['Bar_NPE_Area_DW'],myplotter.dict['Bar_Area_St'],myplotter.dict['Bar_NPE_St'],myplotter.dict['Slab_Area_St'],myplotter.dict['Bar_NPE_Area_St'],myplotter.dict['Bar_Area_CL'],myplotter.dict['Bar_NPE_CL'],myplotter.dict['Slab_Area_CL'],myplotter.dict['Bar_NPE_Area_CL']]
    


    cutflow = cutflow8

    myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

    #myiterator.run() # comment this out when checking cut efficiency

    #--------------section for using to check cut efficiency-----------------------------
    print(outputPath)
    if outputPath == '':
        myiterator.run()

    #output result to txt file
    else:
        with open(f'{outputPath}/Run{numRun}_file{fileNum}CutFlow8.txt', 'w') as cfFile:
            sys.stdout = cfFile  # Change the standard output to the file
            myiterator.run() #output from counting function will be saved in the txt file above.



        # After the block, stdout will return to its default (usually the console)
        # reset stdout to its original state
        sys.stdout = sys.__stdout__

        f_out = r.TFile(f"{outputPath}/Run{numRun}_file{fileNum}_CutFlow8.root", "RECREATE")
        """#histograms for cutflow 7
        M_adj_NPE_C.Write()
        M_NPE_C.Write()
        NPERatio_C.Write()
        CorrectTime_OL.Write()
        CorrectTime_default_OL.Write()
        NpeRatio_adj.Write()
        NpeRatio_ot.Write()
        NuniqueBar_C.Write()
        """
        Bar_Area_DW.Write()
        Bar_NPE_DW.Write()
        Slab_Area_DW.Write()
        Bar_NPE_Area_DW.Write()
        Bar_Area_St.Write()
        Bar_NPE_St.Write()
        Slab_Area_St.Write()
        Bar_NPE_Area_St.Write()
        Bar_Area_CL.Write()
        Bar_NPE_CL.Write()
        Slab_Area_CL.Write()
        Bar_NPE_Area_CL.Write()
        NuniqueBar_DW.Write()


        f_out.Close()




    #-------------------------------------output histograms and save in root file. Please comment it out if you dont need it------------------------------------------------

    """
    #f_out = r.TFile(f"Run{numRun}TagV2_condorJob.root", "RECREATE")
    #f_out = r.TFile(f"Run{numRun}TagV2_testOnly.root", "RECREATE")
    #f_out.cd()
    """