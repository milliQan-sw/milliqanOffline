 #########################################################################################################################################################
 # Original Author: Ryan De Los Santos                                                                                                                   #
 # Use: Use to handle the data files and apply any necessary cuts for your analysis. When using this function make sure that you instantiate DataHandler #
 # then input what cuts you would like to use in applyCuts(). Call DataHandler.applyCuts() to apply all of your cuts.                                    #
 #########################################################################################################################################################

import ROOT as r

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
    def viewData(self):
        return

    # For a millicharged particle it is expected that the ratio between the maximum and minimum nPE is less than 10
    # This function removes events that don't satisfy this cut
    def npeCut(self, event):
        # FIXME: How do we reconcile the issue where some values are negative
        nPEratio = max(event.nPE)/min(event.nPE)
        if nPEratio > 10:
            return
        if self.debug:
            print(event.nPE)
            print(nPEratio)
        return event

    # Removes events that have a hit in the cosmic veto panels labeled by channel 68, 69, 70, 72, 73, 74.
    def cosmicPanelVeto(self, event):
        panels = [68, 69, 70, 72, 73, 74] # The channel numbers for the cosmic veto panels
        # Getting list of channels for each event
        channels = event.chan
        if any(veto in channels for veto in panels):
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

    # Removes events that don't pass the timing cut of -15ns < delta t < 15ns between each pulse
    #
    def timingCut(self, event):
        time = event.time_module_calibrated
        if abs(min(time)-max(time)) > 15:
            return

        if self.debug:
            print(time)

        return event

    def applyCuts(self, cuts):
        cutData = []
        for event in self.data:
            for cut in cuts:
                #FIXME Ensure that if None is returned that the loop does not continue
                event = cut(event)
            if event is not None:
                cutData.append(event)
        return cutData

if __name__ == "__main__":
    data = DataHandler('/store/user/mcarrigan/trees/v29/MilliQan_Run591.*_v29_firstPedestals.root')
    cutData = data.applyCuts([data.npeCut, data.timingCut])
    print(len(cutData))
