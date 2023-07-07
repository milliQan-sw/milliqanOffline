 #########################################################################################################################################################
 # modified from dataCut.py
 # Add threeinaline() cut by Collin 2/12/23  
 # For trigger test, create a method that remove specific hit when it doesn't sastisfy the E and T threashold.  by Collin 6-25-23
 # debug continue at line 192
 # listManipulation method is created, looks working fine 6/27/23
 # the element delete base on index might have issue. as long as the do sort(reverse=True) for rmList then it should be fine
 # adding 3 in row
 # 4 layers
 # >2 hits
 # separeate layer
 # ajacent layer
 # clearn the old cut? or updata them to work with trigger analysis?
 #########################################################################################################################################################

import ROOT as r
from DetectorGeometry import *
import numpy as np

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
    

    def listConvertion(self,list):
        List1 = []
        for item in list:
            List1.append(item)
        return List1
    
    
    def listManipulation(self,EList,TList):
        #find the first pulse that is above 15mV
        # does return the index that need to be remove will be better? yes, because other cuts might also contain layer list....!
        #need to rewrite it by assuming time is unique. your index append method is not good.
        # the better solution is to find out which time element being removed, and find the correspond index
        


        TCopy = list() 
        for time in TList:
            TCopy.append(time)
        ECopy = list()
        for E in EList:
            ECopy.append(E)
        #might need to fix the code at above

        
        removeIndex = list()
        EremoveIndex = list()
        #remove the pulse base on E,
        for index,energy in reversed(list(enumerate(ECopy))):
            if energy < ETthreashold:
                #del ECopy[index]
                #del TCopy[index]  #I doubt if this is correct
                #removeIndex.append(index)
                #print("height index remove"+ str(index))
                EremoveIndex.append(index)
        
        EremoveIndex.sort(reverse=True)

        for index in EremoveIndex:
            del ECopy[index]
            del TCopy[index]
        
        #print("ECopy debug "+ str(ECopy))
        
        if len(TCopy) < 1:
            return None

        minT = min(TCopy)
        
        #find the last pulse withint the window 160ns
        T = minT + 160

        TremoveList = list()
        for index, time in enumerate(TCopy):
            if time >= T:
                #del TCopy[index]
                #removeIndex.append(index+num1+num2)
                TremoveList.append(index)

        TremoveList.sort(reverse=True)
        for index in TremoveList:
            del TCopy[index]

        


        #print("min time debug" + str(minT))
        #print("TCopy debug "+ str(TCopy))
        #find out the index of pulse that being removed
        for index,time in enumerate(TList):
            if time not in TCopy:
                removeIndex.append(index)
            

        return removeIndex # use to remove the data


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
    def muonSelection(self,event, height_threshold):
        
        height_list = event.height
        chan_list = event.chan

        # if there is no hit on the end pannels, then we can't claims that this 
        # event is muon event
        if 71 not in chan_list:
            return
        elif 75 not in chan_list:
            return
        frontPannelHeight = []
        backPannelHeight = []
        #She claim if both end pannals has a big hit(>1.1V), then it is muon event
        for chan, height in zip(chan_list,height_list):

            if chan == 71:  
                frontPannelHeight.append(height)
            elif chan == 75:
                backPannelHeight.append(height)
            
            if any(x >= height_threshold for x in frontPannelHeight) and any(x >= height_threshold for x in backPannelHeight):
                return event
            else:
                return

    def npeCheck(self,event):
        nPE_list = event.nPE
        DAQNum = event.DAQEventNumber
        #nPEthreashold is define in DetectorGeometry.py
        if min(nPE_list) >= nPEthreashold:
            #print(DAQNum)
            return event
        else:
            return None

    def twoSepLayers(self,event):
        layer_list = self.listConvertion(event.layer)
        time_list = self.listConvertion(event.timeFit)
        height_list = self.listConvertion(event.height)
        sorted_time_list = sorted(enumerate(time_list), key=lambda x: x[1]) #reutnr [(original index before sortting, value)]
        
        layer_rmE_lst = list() #remove the layer whose corresponding energy is less than the ETthreashold
        new_time_list = list() #after sortting the time, remove the time whose corresponding energy is less than the ETthreashold
        for index, time in sorted_time_list:
            if height_list[index] > ETthreashold:
                layer_rmE_lst.append(layer_list[index])
                new_time_list.append(time)
        
        for index1,time1 in enumerate(new_time_list):
            t1 = time1 + 160 # in unit ns
            new_list_layer = list() #used to store the data of layer within 160ns trigger time
            new_list_layer.append(layer_rmE_lst[index1])

            for index2,time2 in enumerate(new_time_list):
                if time2 <= t1 and time2 > time1 :
                    new_list_layer.append(layer_rmE_lst[index2])
            
            new_list_layer=set(new_list_layer)
            diff = max(new_list_layer) - min(new_list_layer)
            if len(new_list_layer) == 2 and diff > 1:
                return event
        
        return
    
    def twoAdjacentLayers(self,event):
        layer_list = self.listConvertion(event.layer)
        time_list = self.listConvertion(event.timeFit)
        height_list = self.listConvertion(event.height)
        sorted_time_list = sorted(enumerate(time_list), key=lambda x: x[1]) #reutnr [(original index before sortting, value)]
        
        layer_rmE_lst = list() #remove the layer whose corresponding energy is less than the ETthreashold
        new_time_list = list() #after sortting the time, remove the time whose corresponding energy is less than the ETthreashold
        for index, time in sorted_time_list:
            if height_list[index] > ETthreashold:
                layer_rmE_lst.append(layer_list[index])
                new_time_list.append(time)
        
        for index1,time1 in enumerate(new_time_list):
            t1 = time1 + 160 # in unit ns
            new_list_layer = list() #used to store the data of layer within 160ns trigger time
            new_list_layer.append(layer_rmE_lst[index1])

            for index2,time2 in enumerate(new_time_list):
                if time2 <= t1 and time2 > time1 :
                    new_list_layer.append(layer_rmE_lst[index2])
            
            new_list_layer=set(new_list_layer)
            diff = max(new_list_layer) - min(new_list_layer)
            if len(new_list_layer) == 2 and diff == 1:
                return event
        
        return



    #this method is used with ThreeInLine()
    def layerCheck(self,lists):
        i = 0 
        for list in lists:
            if len(set(list)) >= 3: #return true if it contain 3 unique layers(3 in a line)
                i += 1
        return i

    #bigger than two hits
    def btTwohits(self,event):
        
        layer_list = self.listConvertion(event.layer)
        time_list = self.listConvertion(event.timeFit)
        height_list = self.listConvertion(event.height)
        sorted_time_list = sorted(enumerate(time_list), key=lambda x: x[1]) #reutnr [(original index before sortting, value)]
        #print(layer_list)
        layer_rmE_lst = list() #remove the layer whose corresponding energy is less than the ETthreashold
        new_time_list = list() #after sortting the time, remove the time whose corresponding energy is less than the ETthreashold
        if len(sorted_time_list) > 1:
            
            for index, time in sorted_time_list:
                if height_list[index] > ETthreashold:
                    layer_rmE_lst.append(layer_list[index])
                    new_time_list.append(time)
            
            if len(new_time_list)> 0:

                for index1,time1 in enumerate(new_time_list):
                    t1 = time1 + 160 # in unit ns
                    new_list_layer = list() #used to store the data of layer within 160ns trigger time
                    new_list_layer.append(layer_rmE_lst[index1])

                    for index2,time2 in enumerate(new_time_list):
                        if time2 <= t1 and time2 > time1 :
                            new_list_layer.append(layer_rmE_lst[index2])
                
                if len(new_list_layer) > 2:
                    return event
        
        return

    #bigger than or equal to 3 layers    
    def btThreeLayer(self,event):
        #debug
        dq = event.DAQEventNumber
        layer_list = self.listConvertion(event.layer)
        time_list = self.listConvertion(event.timeFit)
        height_list = self.listConvertion(event.height)
        sorted_time_list = sorted(enumerate(time_list), key=lambda x: x[1]) #reutnr [(original index before sortting, value)]
        
        layer_rmE_lst = list() #remove the layer whose corresponding energy is less than the ETthreashold
        new_time_list = list() #after sortting the time, remove the time whose corresponding energy is less than the ETthreashold
        for index, time in sorted_time_list:
            if height_list[index] > ETthreashold:
                layer_rmE_lst.append(layer_list[index])
                new_time_list.append(time)
        #finish data preparation

        #start the data anlysis
        for index1,time1 in enumerate(new_time_list):
            t1 = time1 + 160 # in unit ns
            new_list_layer = list() #used to store the data of layer within 160ns trigger time
            new_list_layer.append(layer_rmE_lst[index1])

            for index2,time2 in enumerate(new_time_list):
                if time2 <= t1 and time2 > time1 :
                    new_list_layer.append(layer_rmE_lst[index2])
            
            new_list_layer=set(new_list_layer)

            if len(new_list_layer) >= 3:
                return event
        print("dq:"+ str(dq) + "events doesn't satisfy four layers")
        return
            

            


    def FourLayers(self,event):
        #debug
        dq = event.DAQEventNumber
        layer_list = self.listConvertion(event.layer)
        time_list = self.listConvertion(event.timeFit)
        height_list = self.listConvertion(event.height)
        sorted_time_list = sorted(enumerate(time_list), key=lambda x: x[1]) #reutnr [(original index before sortting, value)]
        
        layer_rmE_lst = list() #remove the layer whose corresponding energy is less than the ETthreashold
        new_time_list = list() #after sortting the time, remove the time whose corresponding energy is less than the ETthreashold
        for index, time in sorted_time_list:
            if height_list[index] > ETthreashold:
                layer_rmE_lst.append(layer_list[index])
                new_time_list.append(time)
        #finish data preparation

        #start the data anlysis
        for index1,time1 in enumerate(new_time_list):
            t1 = time1 + 160 # in unit ns
            new_list_layer = list() #used to store the data of layer within 160ns trigger time
            new_list_layer.append(layer_rmE_lst[index1])

            for index2,time2 in enumerate(new_time_list):
                if time2 <= t1 and time2 > time1 :
                    new_list_layer.append(layer_rmE_lst[index2])
            
            #four layers check
            new_list_layer=set(new_list_layer)
            if 0 in new_list_layer:
                if 1 in new_list_layer:
                    if 2 in new_list_layer:
                        if 3 in new_list_layer:
                            return event
        
        #print("dq:"+ str(dq) + "events doesn't satisfy four layers")
        return                
                
        
        

    def ThreeInRow(self,event):
        dq = event.DAQEventNumber
        row_list = self.listConvertion(event.row)
        time_list = self.listConvertion(event.timeFit)
        height_list = self.listConvertion(event.height)
        sorted_time_list = sorted(enumerate(time_list), key=lambda x: x[1])


        row_rmE_lst = list()
        new_time_list = list()
        for index, time in sorted_time_list:
            if height_list[index] > ETthreashold:
                row_rmE_lst.append(row_list[index])
                new_time_list.append(time)

        for index1,time1 in enumerate(new_time_list):
            t1 = time1 + 160 # in unit ns
            new_list_row = list()
            new_list_row.append(row_rmE_lst)

            for index2,time2 in enumerate(new_time_list):
                if time2 <= t1 and time2 > time1 :
                    new_list_row.append(row_rmE_lst[index2])

            #three in a row check
            rowCount0 = 0
            rowCount1 = 0
            rowCount2 = 0
            rowCount3 = 0

            for row in new_list_row:
                if row == 0:
                    rowCount0 += 1
                if row == 1:
                    rowCount1 += 1
                if row == 2:
                    rowCount2 += 1
                if row == 3:
                    rowCount3 += 1
            
            if rowCount3>=3 or rowCount2>= 3 or rowCount1 >= 3 or rowCount0 >= 3:
                return event

        print("dq:"+ str(dq) + "events doesn't satisfy four layers")
        return

            




    
    def ThreeInLine(self,event):
        #note: it would be greate to create the empty list and then do append one by one
        
        time_list = self.listConvertion(event.timeFit) #convert the data from vector flot to list
        height_list = self.listConvertion(event.height)

        #row_list = list(event.row)
        #column_list = list(event.column)
        #layer_list = list(event.layer)


        row_list = self.listConvertion(event.row)
        column_list = self.listConvertion(event.column)
        layer_list = self.listConvertion(event.layer)


        #print("type" +str(type(height_list)))

        #debug print
        rmList=self.listManipulation(height_list,time_list)
        if rmList == None:
            return
        print("rmList:"+str(rmList))
        print("len time_list:" + str(len(time_list)))
        print("time_list:" + str(time_list))
        print("height_list:" + str(height_list))
        #del height_list[0]
        print("type row_list" + str(type(row_list)))
        print("rowlist" + str(row_list))
        rmList.sort(reverse=True)
        for index in rmList:
            print("index" +  str(index))
            #height_list = height_list.pop(index) #debug: remove the stuff outoff range, might need to add a test file to see what is wrong
            #debug : or recrease the matrix with remove index,
            del row_list[index]
            del column_list[index]
            del layer_list[index]

            #row_list=row_list.pop(index)
            #layer_list=layer_list.pop(index)
            #column_list=column_list.pop(index)
        print(str(column_list))
        #to here looks like debug tbd(start at here) 
        # four in a line is very rare impossible to find in run 591
        # use three in a line instead!
        if len(set(layer_list)) >= 3:  #three in a line
            pass
        else:
            return

        
        # the list at below save the information about the pulse passing through difference layers
        # For example, List0 is used for saving the infomation pulse passing through the position of
        # row is three and column is one. "0" correspond to the position of the 0th channal, whose location
        # is at the third row and first column.

        #numbers at below are index number. So 3rd(index) row mean the 4th row in my notation
        list0 = [] # correspond to 3rd row, 0st column
        list1 = [] # correspond to 3rd row, 1st column
        list2 = [] # correspond to 2rd row, 0th column
        list3 = [] # correspond to 2rd row, 1st column
        list4 = [] #list 4-7 should not contain any hit in run 591 due to the last Super model is yet to install
        list5 = []
        list6 = [] 
        list7 = [] 
        list8 = []
        list9 = []
        list10 = []
        list11 = []
        list12 = []
        list13 = []
        list14 = []
        list15 = []

        for row, column, layer in zip(row_list,column_list,layer_list):
            if row == 3 and column == 0:
                list0.append(layer)
            elif row == 3 and column == 1:
                list1.append(layer)
            elif row == 2 and column == 0:
                list2.append(layer)
            elif row == 2 and column == 1:
                list3.append(layer)
            elif row == 3 and column == 2:
                list4.append(layer)
            elif row == 3 and column == 3:
                list5.append(layer)
            elif row == 2 and column == 2:
                list6.append(layer)
            elif row == 2 and column == 3:
                list7.append(layer)
            elif row == 1 and column == 0:
                list8.append(layer)
            elif row == 1 and column == 1:
                list9.append(layer)
            elif row == 0 and column == 0:
                list10.append(layer)
            elif row == 0 and column == 1:
                list11.append(layer)
            elif row == 1 and column == 2:
                list12.append(layer)
            elif row == 1 and column == 3:
                list13.append(layer)
            elif row == 0 and column == 2:
                list14.append(layer)
            elif row == 0 and column == 3:
                list15.append(layer)
        
        # check where does the 4 in a row locate
        lists=[list0,list1,list2,list3,list4,list5,list6,list7,list8,list9,list10,list11,list12,list13,list14,list15]
        #print("lists:"+str(lists)) #for debugs
        i = self.layerCheck(lists) #i is the number list in lists are 3 in a row
        if i >= 1:
            return event
        
        else:
            return
        
    def noPickup(self, event):
        height_list = event.height
        if any(height >= 500 for height in height_list):
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

        #timebL: timebl:time it take for particle pass through layer. Defined in DetectorGeometry.py
        if min(ajacent_time) > timebL: 
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
    #data = DataHandler('/store/user/milliqan/trees/v31/MilliQan_Run1000.*_v31_firstPedestals.root')
    data = DataHandler('/store/user/milliqan/trees/v31/MilliQan_Run1050.*_v31_firstPedestals.root')
    #cutData = data.applyCuts([data.ThreeInLine]) 
    #cutData = data.applyCuts([data.npeCheck]) 
    cutData = data.applyCuts([data.btTwohits])  #use mutiple cuts
    print(len(cutData))
    #print(cutData) #use DaqEventNumber to identify the event
    
    
