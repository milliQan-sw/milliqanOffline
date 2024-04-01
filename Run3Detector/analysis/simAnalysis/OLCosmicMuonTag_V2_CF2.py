from SimCosmicMuonTag_V2 import *

branches = ["chan","runNumber","event","fileNumber",'boardsMatched',"pickupFlag","layer","nPE","type","row","area"]





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
    #fileNum = 1
    #filelist =[f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_Run{numRun}.{fileNum}_v34.root:t']


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
    cutflow1 = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,P_TBBigHitCut,P_TBBigHitCutCount]

    #Cut flow 2. This one is for testing the cut efficiency of different tags. TB big hits - > 4 rows big hits
    cutflow2 = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,CosmuonTagIntialization,TBBigHitCut,TBBigHitCutCount,fourRowBigHitsCut,fourRowBigHitsCutCount]

    #cut flow 3. This one is for testing the cut efficiency of different tags. B + panel big hits  - > TB + panel big hits 
    cutflow3 = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.EmptyListFilter,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,CosmuonTagIntialization,P_BBigHitCut,P_BBigHitCutCount,TBBigHitCut,P_TBBigHitCut,P_TBBigHitCutCount]

    cutflow = cutflow2

    myschedule = milliQanScheduler(cutflow, mycuts,myplotter)

    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts)

    #myiterator.run() # comment this out when checking cut efficiency

    #--------------section for using to check cut efficiency-----------------------------
    print(outputPath)
    if outputPath == '':
        myiterator.run()

    #output result to txt file
    else:
        with open(f'{outputPath}/Run{numRun}_file{fileNum}CutFlow2.txt', 'w') as cfFile:
            sys.stdout = cfFile  # Change the standard output to the file
            myiterator.run() #output from counting function will be saved in the txt file above.



        # After the block, stdout will return to its default (usually the console)
        # reset stdout to its original state
        sys.stdout = sys.__stdout__



    #-------------------------------------output histograms and save in root file. Please comment it out if you dont need it------------------------------------------------

    """
    #f_out = r.TFile(f"Run{numRun}TagV2_condorJob.root", "RECREATE")
    #f_out = r.TFile(f"Run{numRun}TagV2_testOnly.root", "RECREATE")
    #f_out.cd()
    """
