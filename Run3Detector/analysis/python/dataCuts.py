 #########################################################################################################################################################
 # Original Author: Ryan De Los Santos                                                                                                                   #
 # Use: Use to handle the data files and apply any necessary cuts for your analysis. When using this function make sure that you instantiate DataHandler #
 # then input what cuts you would like to use in applyCuts(). Call DataHandler.applyCuts() to apply all of your cuts.
 # Example:
 # data = DataHandler("datapath")          # Replace datapath with where your data is stored
 # data.applyCuts([data.npeCut, data.timingCut])       # Any of the functions within the class containing cut in the name can be used
 #
 # The code should return a few events that pass all of the cuts we expect small numbers for printed to screen for the number of events
 #########################################################################################################################################################

import ROOT as r
from DetectorGeometry import *
# Create Data Class
class DataHandler():
    def __init__(self, dataPath, debug=False):
        self.data = self.initializeData(dataPath)
        self.debug = debug
    # Create TChain with all data you will need for your analysis
    # wildcards can be used in datapath
    def initializeData(self, datapath):
       treeChain = r.TChain('t')
       treeChain.Add(datapath)
       return treeChain


    # Print out certain datafile statistics
    # FIXME: Implement way to viewData or get rid of function
    def viewData(self):
        return

    # For a millicharged particle it is expected that the ratio between the maximum and minimum nPE is less than 10
    # This function removes events that don't satisfy this cut
    def npeCut(self, event, cut_ratio):
        # FIXME: How do we reconcile the issue where some values are negative
        nPEratio = max(event.nPE)/min(event.nPE)
        if nPEratio > cut_ratio:
            return
        if self.debug:
            print(event.nPE)
            print(nPEratio)
        return event

    # Removes events that have a hit in the cosmic veto panels labeled by channel 68, 69, 70, 72, 73, 74.
    def cosmicPanelVeto(self, event):
        # Getting list of channels for each event
        channels = event.chan
        # vetoPanels is defined in DetectorGeometry.py
        if any(veto in channels for veto in vetoPanels):
            return
        if self.debug:
            print(channels)
        return event


    # Removes events that have more than a single hit per layer, ensuring particle travels in straight line
    def singleHitPerLayer(self, event):
        layers = event.layer
        # Sets have no repeated values so if the lenghts are not the same, there is some repeated value
        if len(set(layers)) != len(layers):
            return
        if self.debug:
            print(layers)
        return event


    #MuonSelection is base on NeHa's idea
    #this will not work in run 591 because there is not much hit in the end pannels
    def muonSelection(self,event):
        
        height_list = event.height
        chan_list = event.chan

        # if there is no hit on the end pannels, then we can't claims that this 
        # event is muon event
        if not(all(endCapValue in chan_list for endCapValue in endCaps)):
            return
        frontPannelHeight = []
        backPannelHeight = []
        #She claim if both end pannals has a big hit(>1.1V), then it is muon event
        for chan, height in zip(chan_list,height_list):

            if chan == endCaps[0]:
                frontPannelHeight.append(height)
            elif chan == endCaps[1]:
                backPannelHeight.append(height)
            
            if any(x >= height_threshold for x in frontPannelHeight) and any(x >= height_threshold for x in backPannelHeight):
                return event
            else:
                return

    def npeCheck(self,event):
        nPE_list = event.nPE
        DAQNum = event.DAQEventNumber
        if min(nPE_list) >= npeCutoff:
            #print(DAQNum)
            return event
        else:
            return None


    #this method is used with ThreeInLine()
    def layerCheck(self,lists):
        i = 0 
        for list in lists:
            if len(set(list)) >= 3: #return true if it contain 3 unique layers(3 in a line)
                i += 1
        return i


   # TODO Convert to NInLine where you can choose how many hits you want in a row
   # NOTE This function will currently allow for skipped layers ie. hits in layers 0,1,3 will pass
    def ThreeInLine(self,event):
        row_list = event.row
        column_list = event.column
        layer_list = event.layer

        # We need to check that there are at least 3 unique layers and that there are no repeated layers to ensure
        # that a layer list like [0,0,1,2] does not make it's way through the cut
        if (len(set(layer_list)) >= 3) and (len(set(layer_list)) == len(layer_list)) :
            pass
        else:
            return

        hits_dict = {layer:[row, column] for (layer, row, column) in zip(layer_list, row_list, column_list)}
        compare_value = list(hits_dict.values())[0]

        # Checks if the row and column are the same for all values in dictionary aka they are in a row
        if not(all(val == compare_value for val in hits_dict.values())):
            return
        return event


    def noPickup(self, event):
        height_list = event.height
        if any(height >= pickupCutoff for height in height_list):
            return event
        else:
            return
        

    def timingCut(self, event):
        time = event.time_module_calibrated


        if len(time) >= 2:
            #print("len(time):"+str(len(time))) #debug
            sorted_time = sorted (enumerate(time),key=lambda x: x[1])   #return (index,time)
            #print("sorted_time"+str(sorted_time)) #debug
            time = []
            index_list = []
            for index,t in sorted_time:
                time.append(t)
                index_list.append(index)

            ajacent_time = [y - x for x, y in zip(time[:], time[1:])]
            #print("ajacent_time"+str(ajacent_time)) # debug
        else:  # it requires at least two hit to find the time passing two layers.
            return 
        
        if self.debug:
            print("Adjacent Time", ajacent_time)

        # check if the particle passing through ajecent layer is 15 ns
        # if the minimun value of time passing through ajcent layers is bigger than 15ns, 
        # then it is different from the expected data.
        if min(ajacent_time) > 15: 
            #print("ajacent time is not satified") #debug
            return
        
        
        if self.debug:
            print(time)

        return event
    
    def applyCuts(self, cuts):
        lc=len(cuts)
        cutData = []

        # Run over all events
        for event in self.data:
            # Run over all cuts in list given to applyCuts
            None_check = []
            for cut in cuts:

                event= cut(event) # Apply given cut
                if event is None: 
                    break
                None_check.append(event.DAQEventNumber)


            if None in None_check:
                break
            if len(None_check) == lc: # if there are two cuts then len(None_check) should be 2
                cutData.append(None_check[0])
                
            
        return cutData

if __name__ == "__main__":
    data = DataHandler('/home/rsantos/Data/RunData/MilliQan_Run588.*_v29.root')
    cutData = data.applyCuts([data.muonSelection])
    #cutData = data.applyCuts([data.npeCheck]) 
    #cutData = data.applyCuts([data.ThreeInLine,data.npeCheck])  #use mutiple cuts
    print(len(cutData))
    print(cutData) #use DaqEventNumber to identify the event
    
    
