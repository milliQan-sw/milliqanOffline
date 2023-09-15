import ROOT as r
from DetectorGeometry import *
from triggerConstants import *

class DataHandler():
    def __init__(self, dataPath,run,cuts,debug=False):
        #self.data = self.initializeData(dataPath,run)
        self.cuts = cuts
        self.initializeData(dataPath,run)
        self.debug = debug

    #data path might need to change
    #datapath "/store/user/mcarrigan/skim/muon/v29/"
    #runnumber: 588


    def initializeData(self, datapath,run):
        filesOfsameRun=[]
        
        for filename in os.listdir(datapath):
            if filename.startswith(base_name) and filename.endswith(".root"):
                filesOfsameRun.append(directory+filename)

        for file in filesOfsameRun:
            fin = uproot.open(file)
            tree = fin['t']
            singleData = tree.arrays(uprootInputs, library='pd')
            applyCuts(self.cuts,singleData)

    def applyCuts(self,cuts,singleData):
        
        lc=len(cuts)
        cutData = [] #save the event that pass the cuts with DaqNumber as identication.
        None_check = []
        #select a specifc event
        NumEvent=singleData["event"].max() + 1
        #quit if there is no data in the file
        if np.isnan(NumEvent): return
        #start the event based analysis
        for event in range(NumEvent):
            selected_data = singleData[(singleData["event"] == event) & (singleData["pickupFlag"] == False)] #select the data with specified event and filter out with tag "pickupFlag" == False

            for cut in cuts:
                result= cut(selected_data)
                if result is None: 
                    break
                None_check.append(event.DAQEventNumber)

            if None in None_check:
                break
            if len(None_check) == lc: # if there are two cuts then len(None_check) should be 2
                cutData.append(None_check[0])

        return cutData
        

        #exactly one hit per layer cut
        def exOneHit(self,selected_data):
            layerList=selected_data["layer"]
            if len(set(layerList)) != len(layerList):
                return
            if self.debug:
                print(layerList)
            return event




if __name__ == "__main__":
    cuts=[exOneHit]
    DaqNumber = DataHandler("/store/user/milliqan/trees/v31/",1026,cuts)


        