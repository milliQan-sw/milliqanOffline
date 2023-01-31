 #########################################################################################################################################################
 # Original Author: Ryan De Los Santos                                                                                                                   #
 # Use: Use to handle the data files and apply any necessary cuts for your analysis. When using this function make sure that you instantiate DataHandler #
 # then input what cuts you would like to use in applyCuts(). Call DataHandler.applyCuts() to apply all of your cuts.
 # Example:
 # data = DataHandler("datapath")          # Replace datapath with where your data is stored
 # data.applyCuts([data.npeCut, data.timingCut])       # Any of the functions within the class containing cut in the name can be used
 #
 #   # The code should return a few events that pass all of the cuts we expect small numbers for printed to screen for the number of events
 # Edit the  timingCut() by Collin                                   #
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
    # FIXME ValueError: min() arg is an empty sequence for one of the events
    #'''
    def timingCut(self, event):
        time = event.time_module_calibrated

        '''#original code
        def timingCut(self, event):
        time = event.time_module_calibrated
    
        if abs(min(time)-max(time)) > 15:
           return
        '''

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
        cutData = []
        # Run over all events
        for event in self.data:
            # Run over all cuts in list given to applyCuts
            for cut in cuts:
                event = cut(event) # Apply given cut

                if event is not None: # If there are no events that pass all of the cuts, skip
                    cutData.append(event)
                    if self.debug:
                        print("Event after cut \n ", event)
                else:
                    break
        return cutData

if __name__ == "__main__":
    data = DataHandler('/store/user/mcarrigan/trees/v29/MilliQan_Run591.*_v29_firstPedestals.root')
    cutData = data.applyCuts([data.timingCut])
    print(len(cutData))
