"""
This file is used to check if the trigger exist in specific timing window
1.plot the pulse area at 1000-1400ns.
2.require area cut >200 or 300 k and check the timing distribution

"""

from OLCosmicMuonTag_V2 import *
if __name__ == "__main__":
    numRun = str(sys.argv[1])
    fileNum = str(sys.argv[2])
    filelist =[f'/home/czheng/SimCosmicFlatTree/offlinefile/MilliQan_Run{numRun}.{fileNum}_v34.root:t']
    print(filelist)
    outputPath = str(sys.argv[3])
    print(f"output {outputPath}")
 


    def T_Tag(self):
        self.events["timingWindow"] = (self.events["barCut"]) & (self.events["timeFit_module_calibrated"] > 1000) & (self.events["timeFit_module_calibrated"] < 1400)

    def area_Tag(self):
        self.events["areaTag"] = (self.events["barCut"]) & (self.events["area"] > 200000)

    setattr(milliqanCuts, 'T_Tag',T_Tag)  
    setattr(milliqanCuts, 'area_Tag',area_Tag)  


    TimeDistribution = r.TH1F("TimeDistribution", "timing distribution when bar area is above 200k ; area ; pulse", 100, 0, 2500)
    AreaDistribution = r.TH1F("AreaDistribution", "area bar within 1000-1400ns; area ; pulse", 7000, 0, 700000)



    myplotter.addHistograms(TimeDistribution, 'timeFit_module_calibrated', 'areaTag')
    myplotter.addHistograms(AreaDistribution, 'area', 'timingWindow')

    cutflow = [mycuts.boardsMatched,mycuts.pickupCut,mycuts.barCut,mycuts.T_Tag,mycuts.area_Tag,myplotter.dict['TimeDistribution'],myplotter.dict['AreaDistribution'])
    myschedule = milliQanScheduler(cutflow, mycuts, myplotter)

    myiterator = milliqanProcessor(filelist, branches, myschedule, mycuts, myplotter)

    myiterator.run()

    f = r.TFile(f"{outputPath}/Run{numRun}_file{fileNum}_time_area.root", "RECREATE")

    # Write the histograms to the file
    AreaDistribution.Write()
    TimeDistribution.Write()

    # Close the file
    f.Close()