"""
This file is created to check pulse within trigger window(1000-1500ns). Pickup and boardmatching are applied



"""


from OLCosmicMuonTag_V2 import *

if __name__ == "__main__":

    numRun = str(sys.argv[1])
    fileNum = str(sys.argv[2])
    filelist =[f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_Run{numRun}.{fileNum}_v34.root:t']
    print(filelist)



    Bar_pulseArea = r.TH1F("Bar_pulseArea", "area bar; area ; pulse", 7000, 0, 700000)
    Bar_pulseNPE = r.TH1F("Bar_pulseNPE", "nPE bar; nPE ; pulse", 500, 0, 1000)
    Slab_pulseArea = r.TH1F("Slab_pulseArea", "area Slab; area ; pulse", 7000, 0, 700000)
    #for offline file V34, the npe is the same as pulse area. So I only draw the 2D histogram for bars
    Bar_NPE_Area = r.TH2F("Bar_NPE_Area", "bar channels; nPE; area",20,0,1000,20, 0, 700000)
    
    myplotter.addHistograms(Bar_pulseNPE, 'nPE', 'barCut')
    myplotter.addHistograms(Bar_pulseArea, 'area', 'barCut')
    myplotter.addHistograms(Slab_pulseArea, 'area', 'panelCut')
    myplotter.addHistograms(Bar_NPE_Area, ['nPE','area'], 'barCut')



    


    cutflow = [mycuts.offlinePreProcess,mycuts.boardsMatched,mycuts.pickupCut,mycuts.countEvent,mycuts.barCut,mycuts.panelCut,,myplotter.dict['Bar_pulseNPE'],myplotter.dict['Slab_pulseArea'],myplotter.dict['Bar_NPE_Area']]

    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

    myiterator.run()


    f = r.TFile(f"{outputPath}/Run{numRun}_file{fileNum}_NPE_area.root", "RECREATE")

    # Write the histograms to the file
    Bar_pulseArea.Write()
    Bar_pulseNPE.Write()
    Slab_pulseArea.Write()
    Bar_NPE_Area.Write()

    # Close the file
    f.Close()



