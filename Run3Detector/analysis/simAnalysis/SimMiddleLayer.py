"""
this file is created to study the NPE distribution when a event pass the cosmic muon event tag.

There are 3 candidate tags don't require the big hits in the middle layer. what is the NPE distribution for bar at the those layers?

I expect the most of low energy particles unable to reach the middle layer. 

To do
collect the NPE distribution at layer 2 and 3 by remove non-muon hit bars vs without the muon cut.

"""

from SimCosmicMuonTag_V2 import *





if __name__ == "__main__":

    branches = ["chan","runNumber","event","layer","nPE","type","row","muonHit"]

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
    #fileNum = 1
    #filelist =[f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_Run{numRun}.{fileNum}_v34.root:t']


    #------------------------------------------------------------------------------------------------
    #path for the milliqan machine

    #print("this is numRun" + str(sys.argv[1]) )


    numRun = str(sys.argv[1])
    filelist =[f'/mnt/hadoop/se/store/user/czheng/SimFlattree/withPhotonMuontag/output_{numRun}.root:t']
    print(filelist)

    outputPath = str(sys.argv[2]) # the path is used at the very end for the output txt file
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
    #--------------------------------------plotting function --------------------------
    def layerMask(self):
        self.events["lay0"] = self.events.layer == 0 & self.events.type == 0
        self.events["lay1"] = self.events.layer == 1 & self.events.type == 0
        self.events["lay2"] = self.events.layer == 2 & self.events.type == 0
        self.events["lay3"] = self.events.layer == 3 & self.events.type == 0


    setattr(milliqanCuts, 'layerMask', layerMask)



    #test cut flow. Check if the mask can be made
    #cutflow = [mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,mycuts.fourRowBigHits,mycuts.TBBigHit,mycuts.P_TBBigHit,mycuts.P_BBigHit]


    #create root histogram 
    h_nPEL0 = r.TH1F("h_nPEL0", "bar nPE distribution at layer 0", 10000, 0, 100000)
    #create root histogram 
    h_nPEL1 = r.TH1F("h_nPEL1", "bar nPE distribution at layer 1", 10000, 0, 100000)
    h_nPEL2 = r.TH1F("h_nPEL2", "bar nPE distribution at layer 2", 10000, 0, 100000)
    h_nPEL3 = r.TH1F("h_nPEL3", "bar nPE distribution at layer 3", 10000, 0, 100000)

    #add root histogram to plotter
    myplotter.addHistograms(h_nPEL0, 'h_nPEL0', 'lay0')
    myplotter.addHistograms(h_nPEL1, 'h_nPEL1', 'lay1')
    myplotter.addHistograms(h_nPEL2, 'h_nPEL2', 'lay2')
    myplotter.addHistograms(h_nPEL3, 'h_nPEL3', 'lay3')



    TBBigHitCut = mycuts.getCut(mycuts.TBBigHit,"placeholder", cut = True)
    P_TBBigHitCut= mycuts.getCut(mycuts.P_TBBigHit, "P_TBBigHitCut",cut = True)
    P_BBigHitCut= mycuts.getCut(mycuts.P_BBigHit, "P_BBigHitCut",cut = True)
    MuonCut = mycuts.getCut(mycuts.MuonEvent, "placeholder", CutonBars =True, branches=branches) 

    TBBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "TBBigHit")
    fourRowBigHitsCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "fourRowBigHits")
    P_TBBigHitCutCount= mycuts.getCut(mycuts.countEvent,"placeholder"  ,Countobject = "P_TBBigHit")
    P_BBigHitCutCount= mycuts.getCut(mycuts.countEvent, "placeholder" ,Countobject = "P_BBigHit")
    #NbarsHitsCount1= mycuts.getCut(mycuts.P_BBigHit, "NBarsHits",cut = None,hist = NBarsHitTag1)#FIXME: getCut can't take hist as argument. Maybe I should remove it
    #cutflowSTD = [mycuts.MuonEvent,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,mycuts.NbarsHitsCount ,myplotter.dict['NBarsHitTag2']] #default analysis cutflow



    #Cut flow 1. This one is for testing the cut efficiency of different tags. TB big hits - > TB + panel big hits 
    cutflow1 = [MuonCut,mycuts.EmptyListFilter,mycuts.layerMask,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,myplotter.dict['h_nPEL0'],myplotter.dict['h_nPEL1'],myplotter.dict['h_nPEL2'],myplotter.dict['h_nPEL3']]

    #Cut flow 2. This one is for testing the cut efficiency of different tags. TB big hits - > 4 rows big hits
    cutflow2 = [MuonCut,mycuts.EmptyListFilter,mycuts.layerMask,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,myplotter.dict['h_nPEL0'],myplotter.dict['h_nPEL1'],myplotter.dict['h_nPEL2'],myplotter.dict['h_nPEL3']]

    #cut flow 3. This one is for testing the cut efficiency of different tags. B + panel big hits  - > TB + panel big hits 
    cutflow3 = [MuonCut,mycuts.EmptyListFilter,mycuts.layerMask,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,mycuts.CosmuonTagIntialization,P_BBigHitCut,P_BBigHitCutCount,myplotter.dict['h_nPEL0'],myplotter.dict['h_nPEL1'],myplotter.dict['h_nPEL2'],myplotter.dict['h_nPEL3']]




    cutflow = cutflow1

    myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

    #myiterator.run() # comment this out when checking cut efficiency

    #--------------section for using to check cut efficiency-----------------------------
    print(outputPath)
    if outputPath == '':
        myiterator.run()

    #output result to txt file
    else:
        with open(f'{outputPath}/Run{numRun}_fileCutFlow1.txt', 'w') as cfFile:
            sys.stdout = cfFile  # Change the standard output to the file
            myiterator.run() #output from counting function will be saved in the txt file above.



        # After the block, stdout will return to its default (usually the console)
        # reset stdout to its original state
        sys.stdout = sys.__stdout__


    #-------------------------------------output file at milliqan machine--------------------
    f_out = r.TFile(f"{outputPath}/Run{numRun}cosmicEventNPEdist.root", "RECREATE")
    f_out.cd()
    h_nPEL0.Write()
    h_nPEL1.Write()
    h_nPEL2.Write()
    h_nPEL3.Write()
    f_out.Close()



    #-------------------------------------output histograms and save in root file. Please comment it out if you dont need it------------------------------------------------

    


    """
    #f_out = r.TFile(f"Run{numRun}TagV2_condorJob.root", "RECREATE")
    #f_out = r.TFile(f"Run{numRun}TagV2_testOnly.root", "RECREATE")
    #f_out.cd()
    """