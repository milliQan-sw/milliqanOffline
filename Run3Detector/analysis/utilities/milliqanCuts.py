#!/usr/bin/python3

import awkward as ak
import numpy as np

class milliqanCuts():

    def __init__(self):
        self.events = []
        self.cutflow = []
        self.counter = 0

    def cutflowCounter(self):
        # Increments events passing each stage of the cutflow
        # Creates each stage during the first pass
        if len(self.cutflow) > self.counter:
            self.cutflow[self.counter]+=len(self.events)
        # Builds the array without knowledge of the number of cuts
        else:
            self.cutflow.append(len(self.events))
        self.counter+=1

    def getCutflowCounts(self):
        # Prints the value after each batch of events
        # TODO: Only print at the very end
        print("------------------Cutflow Table--------------------")
        print ("{:<15} {:<10}".format('Cut', 'N Passing Events'))
        for i in range(len(self.cutflow)):
            print("{:<15}{:<10}".format(i, self.cutflow[i]))
        print("----------------------------------------------------")
        # Resets the counter at the end of the cutflow
        self.counter=0

    #function to allow multiple masks (cuts) to be combined together and saved as name
    def combineCuts(self, name, cuts):
        for cut in cuts:
            if name in ak.fields(self.events):
                self.events[name] = self.events[name] & (self.events[cut])
            else:
                self.events[name] = self.events[cut]

    # Dummy cut for use while construcing the cutflow mechanics
    def neverCut(self, cutName=None, cut=False):
        if cut: self.events = self.events
        self.cutflowCounter()

    def pickupCut(self, cutName=None, cut=False, tight=False, branches=None):
        if cut and tight:
            for branch in branches:
                self.events[branch] = self.events[branch][~self.events.pickupFlag]
        elif cut and not tight:
            for branch in branches:
                if branch == 'boardsMatched': continue
                self.events[branch] = self.events[branch][~self.events.pickupFlag]

    def boardsMatched(self, cutName=None, cut=False, branches=None):
        self.events['boardsMatched'], junk = ak.broadcast_arrays(self.events.boardsMatched, self.events.pickupFlag)
        
        if cut:
            for branch in branches:
                if branch == 'boardsMatched': continue
                self.events[branch] = self.events[branch][self.events.boardsMatched]

    #create mask for pulses in each layer
    def layerCut(self):
        self.events['layer0'] = self.events.layer == 0
        self.events['layer1'] = self.events.layer == 1
        self.events['layer2'] = self.events.layer == 2
        self.events['layer3'] = self.events.layer == 3

    #event level mask selecting events with hits in 4 layers
    def fourLayerCut(self, cutName=None, cut=False):
        self.events['fourLayerCut'] =(ak.any(self.events.layer==0, axis=1) & 
                                      ak.any(self.events.layer==1, axis=1) & 
                                      ak.any(self.events.layer==2, axis=1) & 
                                      ak.any(self.events.layer==3, axis=1))
        if cut: self.events = self.events[self.events.fourLayerCut]
        self.cutflowCounter()

    def oneHitPerLayerCut(self, cutName=None, cut=False, multipleHits=False):
        if multipleHits:
            layer0 = (self.events.layer==0) & (self.events['type']==0)
            layer1 = (self.events.layer==1) & (self.events['type']==0)
            layer2 = (self.events.layer==2) & (self.events['type']==0)
            layer3 = (self.events.layer==3) & (self.events['type']==0)
    
            unique0 = ak.Array([np.unique(x) for x in self.events.chan[layer0]])
            unique1 = ak.Array([np.unique(x) for x in self.events.chan[layer1]])
            unique2 = ak.Array([np.unique(x) for x in self.events.chan[layer2]])
            unique3 = ak.Array([np.unique(x) for x in self.events.chan[layer3]])
    
            self.events['oneHitPerLayerCut'] = (
                                            (ak.count_nonzero(unique0, axis=1)==1) &
                                            (ak.count_nonzero(unique1, axis=1)==1) &
                                            (ak.count_nonzero(unique2, axis=1)==1) &
                                            (ak.count_nonzero(unique3, axis=1)==1)
                                            )
        else:
            print(self.events.layer==0)
            print(self.events['type']==0)
            print((self.events.layer==0) & (self.events['type']==0))
            self.events['oneHitPerLayerCut'] = (
                                            (ak.count_nonzero((self.events.layer==0) & (self.events['type']==0), axis=1)==1) &
                                            (ak.count_nonzero((self.events.layer==1) & (self.events['type']==0), axis=1)==1) &
                                            (ak.count_nonzero((self.events.layer==2) & (self.events['type']==0), axis=1)==1) &
                                            (ak.count_nonzero((self.events.layer==3) & (self.events['type']==0), axis=1)==1)
                                            )
        if cut: self.events = self.events[self.events.oneHitPerLayerCut]            
        self.cutflowCounter()
    #create mask for pulses passing height cut
    def heightCut(self, cutName='heightCut', cut=1200, branches=None):
        self.events[cutName] = self.events.height >= int(cut)
        if branches:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]
                
    #create mask for pulses passing area cuts
    def areaCut(self, cutName='areaCut', cut=50000):
        self.events[cutName] = self.events.area >= int(cut)

    #First pulse in a given channel
    def firstChanPulse(self):
        self.events['firstChanPulse'] = self.events.ipulse == 0

    def barCut(self):
        self.events['barCut'] = self.events['type'] == 0

    def panelCut(self):
        self.events['panelCut'] = self.events['type'] == 2

    def slabCut(self):
        self.events['slabCut'] = self.events['type'] == 1

    #selection events that have hits in a straight path
    #option allowedMove will select events that only move one bar horizontally/vertically
    def straightLineCut(self, allowedMove=False):
        
        #allowed combinations of moving
        combos = []
        straight_cuts = []

        #bool to decide if 1 bar movement should be found
        allowedMove = False

        debugEvt = 1191

        for i, x in enumerate(range(4)):
            for j, y in enumerate(range(4)):

                rowCut = self.events.row == y
                colCut = self.events.column == x

                r_tmp0 = (rowCut[self.events.layer0] & colCut[self.events.layer0])
                r_tmp1 = (rowCut[self.events.layer1] & colCut[self.events.layer1])
                r_tmp2 = (rowCut[self.events.layer2] & colCut[self.events.layer2])
                r_tmp3 = (rowCut[self.events.layer3] & colCut[self.events.layer3])


                row_pass = ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(r_tmp3, axis=1)

                if allowedMove:
                    rowCut_p1 = self.events.row == y+1
                    rowCut_m1 = self.events.row == y-1
                    colCut_p1 = self.events.column == x+1
                    colCut_m1 = self.events.column == x-1
                    if(y > 0): 
                        m1_c0_r1 = (rowCut_m1[self.events.layer1]) & (colCut[self.events.layer1])
                        m2_c0_r1 = (rowCut_m1[self.events.layer2]) & (colCut[self.events.layer2])
                        m3_c0_r1 = (rowCut_m1[self.events.layer3]) & (colCut[self.events.layer3])
                    if(x > 0): 
                        m1_c1_r0 = (rowCut[self.events.layer1]) & (colCut_m1[self.events.layer1])
                        m2_c1_r0 = (rowCut[self.events.layer2]) & (colCut_m1[self.events.layer2])
                        m3_c1_r0 = (rowCut[self.events.layer3]) & (colCut_m1[self.events.layer3])

                    if(y < 4): 
                        p1_c0_r1 = (rowCut_p1[self.events.layer1]) & (colCut[self.events.layer1])
                        p2_c0_r1 = (rowCut_p1[self.events.layer2]) & (colCut[self.events.layer2])
                        p3_c0_r1 = (rowCut_p1[self.events.layer3]) & (colCut[self.events.layer3])
                    if(x < 4): 
                        p1_c1_r0 = (rowCut[self.events.layer1]) & (colCut_p1[self.events.layer1])
                        p2_c1_r0 = (rowCut[self.events.layer2]) & (colCut_p1[self.events.layer2])
                        p3_c1_r0 = (rowCut[self.events.layer3]) & (colCut_p1[self.events.layer3])

                    if(x > 0):
                        combos.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(m3_c1_r0, axis=1)) #layer3 col decrease
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(m2_c1_r0, axis=1) & ak.any(m3_c1_r0, axis=1)) #layer2 col decrease
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(m1_c1_r0, axis=1) & ak.any(m2_c1_r0, axis=1) & ak.any(m3_c1_r0, axis=1)) #layer1 col decrease
                    if(y > 0):
                        combos.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(m3_c0_r1, axis=1)) #layer3 row decrease
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(m2_c0_r1, axis=1) & ak.any(m3_c0_r1, axis=1)) #layer2 row decrease
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(m1_c0_r1, axis=1) & ak.any(m2_c0_r1, axis=1) & ak.any(m3_c0_r1, axis=1)) #layer1 row decrease
                    if(x < 4):
                        combos.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(p3_c1_r0, axis=1)) #layer3 col increase
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(p2_c1_r0, axis=1) & ak.any(p3_c1_r0, axis=1)) #layer2 col increase
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(p1_c1_r0, axis=1) & ak.any(p2_c1_r0, axis=1) & ak.any(p3_c1_r0, axis=1)) #layer1 col increase
                    if(y < 4):
                        combos.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(p3_c0_r1, axis=1)) #layer3 row increase
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(p2_c0_r1, axis=1) & ak.any(p3_c0_r1, axis=1)) #layer2 row increase
                        combos.append( ak.any(r_tmp0, axis=1) & ak.any(p1_c0_r1, axis=1) & ak.any(p2_c0_r1, axis=1) & ak.any(p3_c0_r1, axis=1)) #layer1 row increase

                straight_cuts.append(row_pass)
        
        for ipath, path in enumerate(straight_cuts):
            if ipath == 0: straight_path = path
            else: straight_path = straight_path | path

        self.events['straightLineCut'] = straight_path

        for x in range(4):
            for y in range(4):
                if(x == 0 and y == 0): straight_pulse = (straight_cuts[4*x+y]) & (self.events.column == x) & (self.events.row == y)
                else: straight_pulse = (straight_pulse) | ((straight_cuts[4*x+y]) & (self.events.column == x) & (self.events.row == y))

        self.events['straightPulseCut'] = straight_pulse

        '''testEvt = 2
        tmp = ak.any(self.events['straightPulseCut'], axis=1)
        chans = self.events['chan'][tmp]
        pulses = self.events['straightPulseCut'][tmp]
        heights = self.events['height'][tmp]
        print(chans[testEvt])
        print(pulses[testEvt])
        print(chans[pulses][testEvt])
        print(heights[pulses][testEvt])
        print("Number of pulses passing", len(ak.flatten(chans[pulses])))
        print("Number of pulses in events passing", len(ak.flatten(chans)))'''


        #get self.events passing 1 bar movement
        if allowedMove:
            for ipath, path in enumerate(combos):
                if ipath == 0: passing = path
                else: passing = passing | path

            self.events['moveOnePath'] = passing

    def getPulseTimeDiff(self):
        times = self.events['timeFit_module_calibrated'][self.events['eventCuts']]
        passing = self.events['eventCuts'][self.events['eventCuts']]
        count = ak.count(times, keepdims=True, axis=1)
        count = count == 4
        count, times = ak.broadcast_arrays(count, times)
        times = times[count]
        diffs = ak.combinations(times, 2)
        t1, t2 = ak.unzip(diffs)
        t_out = abs(t1-t2)
        t_out = ak.max(t_out, axis=1, keepdims=True)
        self.events['timeDiff'] = t_out

    #select self.events that have 3 area saturating pulses in a line
    def threeAreaSaturatedInLine(self, areaCut=50000):
        #make sure 3 layers have saturating hits
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        
        self.events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
        self.events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))
        
    #select self.events that have 3 height saturating pulses in a line
    def threeHeightSaturatedInLine(self, heightCut=50000):
        #make sure 3 layers have saturating hits
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        
        self.events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
        self.events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))

    def matchedTDCTimes(self):
        board0 = self.events.v_groupTDC_g0[:, 0]
        board1 = self.events.v_groupTDC_g0[:, 1]
        board2 = self.events.v_groupTDC_g0[:, 2]
        board3 = self.events.v_groupTDC_g0[:, 3]
        board4 = self.events.v_groupTDC_g0[:, 4]

        self.events['tdcMatch'] = (board0 == board1) & (board0 == board2) & (board0 == board3) & (board0 == board4)

    def adjLayerData(self,layer0Cut,layer1Cut,layer2Cut,layer3Cut):
        """
        The layer*cut is event-based but in the size of pulses. 
        The goal of this function is to create an adjacent layer tag. The output tags are in the same format as the input tag. 
        This function can be used when you need to do adjacent layer analysis. For example, what is the pulse nPE distribution at the layer that is next to muon layer.
        I use this function with LayerContraint() to get a tag that which pulses are the adjacent layers.
        """
        #keep the array size 
        arrSize = ak.copy(layer0Cut)
    
    
        layer0Cut = ak.any(layer0Cut,axis =1)
        layer1Cut = ak.any(layer1Cut,axis =1)
        layer2Cut = ak.any(layer2Cut,axis =1)
        layer3Cut = ak.any(layer3Cut,axis =1)
        adjLayArrL0= []
        adjLayArrL1= []
        adjLayArrL2= []
        adjLayArrL3= []
        for L0, L1, L2, L3 in zip(layer0Cut,layer1Cut,layer2Cut,layer3Cut):
            innerArr = []
            adjLay = []
            if L0:
                innerArr.append(0)
            if L1:
                innerArr.append(1)
            if L2:
                innerArr.append(2)
            if L3:
                innerArr.append(3)
            
            if len(innerArr) == 1:
                if innerArr[0] == 4:
                    adjLay.append(3) 
                else:
                    adjLay.append(innerArr[0] + 1)
            elif len(innerArr) == 2:
                if 1 in innerArr and 0 in innerArr:
                    adjLay.append(3) 
                    adjLay.append(2) 
                elif 3 in innerArr and 2 in innerArr:
                    adjLay.append(0) 
                    adjLay.append(1)
                else:
                    for num in [0,1,2,3]:
                        if num not in innerArr:
                            adjLay.append(num)
            elif len(innerArr) == 3:
                for num in [0,1,2,3]:
                    if num not in innerArr:
                            adjLay.append(num)
            
            #check what is in the adjLay
            if 0 in adjLay:
                adjLayArrL0.append(True)
            else:
                adjLayArrL0.append(False)
            if 1 in adjLay:
                adjLayArrL1.append(True)
            else:
                adjLayArrL1.append(False)
            
            if 2 in adjLay:
                adjLayArrL2.append(True)
            else:
                adjLayArrL2.append(False)
            
            if 3 in adjLay:
                adjLayArrL3.append(True)
            else:
                adjLayArrL3.append(False)
    
        #convert the 
        adjLayArrL0, junk=ak.broadcast_arrays(adjLayArrL0, arrSize)
        adjLayArrL1, junk=ak.broadcast_arrays(adjLayArrL1, arrSize)
        adjLayArrL2, junk=ak.broadcast_arrays(adjLayArrL2, arrSize)
        adjLayArrL3, junk=ak.broadcast_arrays(adjLayArrL3, arrSize)
    
        return adjLayArrL0,adjLayArrL1,adjLayArrL2,adjLayArrL3


    def LayerContraint(self,layer0Cut,layer1Cut,layer2Cut,layer3Cut, layerConstraintEnable = None,branches = None,CutomizedEvents=None):
        """
        By default(without change any default argument) you can only get the copy of self.events array. 
        The goal for creating the copy of original array is to avoid data losing while removing some pulses to do the analysis. 
        You need to manually set the "layerConstraintEnable = adjacent" when doing the adjcent layer analysis, which create a new tag in the copy array. 
        
        use CutomizedEvents argument when people are not using all of the data from self.events array. 
        the CutomizedEvents is an awkward array.

        
        
        """
        if CutomizedEvents:
            SpecialArr = ak.copy(CutomizedEvents)
            if layerConstraintEnable == False:
                return SpecialArr
        else:
            specialArr = ak.copy(self.events)
            if layerConstraintEnable == "adjacent":
                layer0Cut,layer1Cut,layer2Cut,layer3Cut=adjLayerData (layer0Cut,layer1Cut,layer2Cut,layer3Cut)
    
            elif layerConstraintEnable  == False:
                return SpecialArr
        
        if layerConstraintEnable == "adjacent":
            layer0Cut,layer1Cut,layer2Cut,layer3Cut=adjLayerData (layer0Cut,layer1Cut,layer2Cut,layer3Cut)
            for b in branches:
                if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event": continue
                specialArr[b] = specialArr[b][((specialArr["layer"] ==0) & (layer0Cut)) | ((specialArr["layer"] ==1)  & (layer1Cut))  | ((specialArr["layer"] == 2) & (layer2Cut)) | ((specialArr["layer"] == 3) & (layer3Cut))]
            return specialArr
        
        specialArrCut = ((specialArr["layer"] ==0) & (layer0Cut)) | ((specialArr["layer"] ==1)  & (layer1Cut))  | ((specialArr["layer"] == 2) & (layer2Cut)) | ((specialArr["layer"] == 3) & (layer3Cut))
    
        for branch in branches:
          
            if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event" : continue
            
            specialArr[branch] = specialArr[branch][specialArrCut]
    
        return specialArr
    
    def NbarsHitsCount(self,cutName = "NBarsHits",cut = None, NPECut = 20):
        """
        Count the number of unique bar channels for each event with NPE threashold.

        If you need to use extra event-based tag, then "cut = your_tag".
        """

        bararr = ak.copy(self.events)
    
        bararr["chan"] = bararr["chan"][(bararr["type"]==0) & (bararr["nPE"]>=NPECut)]
    
        if cut:
            cutMask, junk = ak.broadcast_arrays(bararr.cut, bararr.layer)
    
            uniqueBarArr = ak.Array([np.unique(x) for x in bararr.chan[cutMask]])
            self.events[cutName] = ak.count(uniqueBarArr,axis = 1)
        else:
            uniqueBarArr = ak.Array([np.unique(x) for x in bararr["chan"]])
            self.events[cutName] = ak.count(uniqueBarArr, axis = 1)

    def BarNPERatioCalculate(self,cutName = "BarNPERatio",cut = None):
        """
        The function is to find the bar Npe ratio(max/min) for each event.
        Set cut = True only if you need to use with event based cut. Otherwise, it count npe ratio for all events.
        """
        if cut:
            cutMask, junk = ak.broadcast_arrays(self.events[cut], self.events.layer)
            self.events[cutName] = ((ak.max(self.events.nPE[(cutMask) & (self.events.barCut)],axis=1)/ak.min(self.events.nPE[(cutMask) & (self.events.barCut)],axis=1)))
        else:
            self.events[cutName] = ((ak.max(self.events.nPE[self.events.barCut],axis=1)/ak.min(self.events.nPE[self.events.barCut],axis=1)))

    def BarNPERatioCalculateV2(self,cutName = "BarNPERatio_P",cut = None):
        """
        The V2 is used with layer contrained (pulse based). In run3 projection NPE ratio was made with pulse at adjacnet layers(relative to layer can see muon event).
        """
        self.events[cutName] = ((ak.max(self.events.nPE[self.events[cut]],axis=1)/ak.min(self.events.nPE[self.events[cut]],axis=1)))

    
    def findCorrectTime(self,cutName = "DT_CorrectTime",cut = None,timeData = "time", offlineMode = False ,NPECut = 0):
        """
        Photon fly time (3.96ns) corrections are not being used in offline data when using TimeFit_module_calbrated branch.
        """
        
        if cut:
    
            cutMask, junk = ak.broadcast_arrays(self.events.cut, self.events.layer)
            TimeArrayL0 = self.events[timeData][cutMask & self.events.layer==0]
            TimeArrayL1 = self.events[timeData][cutMask & self.events.layer==1]
            TimeArrayL2 = self.events[timeData][cutMask & self.events.layer==2]
            TimeArrayL3 = self.events[timeData][cutMask & self.events.layer==3]
        
        elif offlineMode == True:
            #the time correction factor is already applied for offline data
            TimeArrayL0 = self.events[timeData][(self.events.layer==0) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] 
            TimeArrayL1 = self.events[timeData][(self.events.layer==1) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)]
            TimeArrayL2 = self.events[timeData][(self.events.layer==2) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)]
            TimeArrayL3 = self.events[timeData][(self.events.layer==3) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)]
    
            
        else:
            #for sim data
    
            TimeArrayL0 = self.events[timeData][(self.events.layer==0) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] 
            TimeArrayL1 = self.events[timeData][(self.events.layer==1) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 1)
            TimeArrayL2 = self.events[timeData][(self.events.layer==2) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 2)
            TimeArrayL3 = self.events[timeData][(self.events.layer==3) & (self.events["nPE"] >= NPECut) & (self.events[timeData] > 0)] - (3.96 * 3)
            
        
        #TimeArrayL2 and TimeArrayL1 will be used in the later case
        TimeArrayL0 = TimeArrayL0 [(TimeArrayL0 <= 2500)]
        TimeArrayL3 = TimeArrayL3[TimeArrayL3 <= 2500]
        TimeArrayL0_min = ak.min(TimeArrayL0,axis=1)
        TimeArrayL3_min = ak.min(TimeArrayL3,axis=1)
        diff1 = TimeArrayL3_min - TimeArrayL0_min
    
        
        #change array strturn for np concatination
        diff1 = [[x] for x in diff1]
        diff1=ak.fill_none(diff1,-6000.0)
    
        self.events["DTL0L3"] = diff1


    def EmptyListFilter(self,cutName=None):
        """
        add a tag for those none-empty events
        """
        self.events['None_empty_event'] = ak.num(self.events['layer']) > 0

    def MuonEvent(self, cutName = None, CutonBars = True, branches = None):
        """
        This method is only useful for simulation data.
        self.events.muonHit == 1 return a tag that indicates which channel got hit by muon.
        set CutonBars = True if you want to do the analysis on the data from channels that hit by muon. Otherwise it creates a event based tag that tells you which event contains muon hit.
        
        """
        if CutonBars:
            for branch in branches:
                if branch == 'boardsMatched' or branch == "runNumber" or branch == "fileNumber" or branch == "event": continue
                self.events[branch] = self.events[branch][self.events.muonHit == 1]
    
        #create a mask for event that contain muon hit
        else:
            self.events["muonEvent"] = ak.any(self.events.muonHit == 1, axis = 1) 

    def countEvent(self, cutName = None, Countobject='None_empty_event', debug = False):
        """
        this function is to count the the amount of non-empty events or events with specific tag.
        The to_pandas only work in some old version of awkward array. But it is helpful when doing debug.
        """
        if debug: 
            print(ak.to_pandas(self.events))
        if cutName:
            print(f"{Countobject} event: {len(self.events[self.events[Countobject]])}")
        else:
            print(f"current available events : {ak.count_nonzero(self.events['None_empty_event'])}")

    def sudo_straight(self, cutName = "StraghtCosmic",NPEcut = 20,time = "time"):
        """
        This function creates 3 event-based tags for cosmic muon events. When doing analysis with offline data offlinePreProcess is required before creating this tag.
        The first two tags only check the first bit hit from bars but the last one also check the big hit on top cosmic panels.
        StraghtCosmic: 36 possible muon stright pathes per layer. Column number shift are allowed. 
        Clean_MuonEvent: This is similar to StraghtCosmic. But if there are more than one layer can see the muon stright path, then it fails.
        downwardPath: Column number shift are not allowed. This means there are only 4 muon pathes per layer if tag return true. 
        """

        lxArr = ak.copy(self.events)
        
        eventList = []
        DownEventList = [] #save the save event that pass the downward tags.
    
    
    
        for layer in range(4):
            for row in range(4):
                for column in range(4):
                    #channel tag
                    lxArr[f"L{layer}_r{row}_c{column}_pre"]=(lxArr["layer"] == layer) & (lxArr["column"] == column) & (lxArr["row"] == row) & (lxArr["barCut"]) #if you see none in this array, then it means there is no hit in this array.
                    #use channel tag to get the time
                    ChanTime = lxArr[time][lxArr[f"L{layer}_r{row}_c{column}_pre"]]
                    #find the the time for first hit of associate channel
    
                    FirstHitTime = ak.min(ChanTime,axis = 1) 
                    #check if the first hit pass the npe cut
                    #assuming there is no two pulses can have same time. if FirstHitTime < 0 then it suggest this channel has no reading. 
                    lxArr[f"L{layer}_r{row}_c{column}"]=(lxArr["nPE"] >= NPEcut) & (lxArr[f"L{layer}_r{row}_c{column}_pre"]) & (lxArr[time] == FirstHitTime) & (FirstHitTime > 0)
                    #fill none. The none appears when the selected channel has no pulse.
                    lxArr[f"L{layer}_r{row}_c{column}"]  = ak.fill_none( lxArr[f"L{layer}_r{row}_c{column}"] , [False], axis =0) 
               
    
        #tag for big hit at the top cosmic panel. Channel is the old offline  channel mapping
        #top cosmic panel that covers layer 0 and layer 1
        lxArr[f"CosP01_pre"] = (lxArr["chan"] == 68)
        P01_Time = lxArr[time][lxArr[f"CosP01_pre"]]
        P01_FirstHitTime = ak.min(P01_Time , axis = 1)
        lxArr["Pre_CosP01"] =  (lxArr[f"CosP01_pre"]) & (lxArr["nPE"] >= (NPEcut/12))  &  (lxArr[time] == P01_FirstHitTime) & (P01_FirstHitTime > 0) 
        lxArr["Pre_CosP01"] = ak.fill_none(lxArr["Pre_CosP01"],[False], axis = 0) 
        lxArr["CosP01"] = ak.any ( lxArr["Pre_CosP01"],axis = 1)
        
        
        #top cosmic panel that covers layer 2 and layer 3
        lxArr[f"CosP23_pre"] = (lxArr["chan"] == 72)
        P23_Time = lxArr[time][lxArr[f"CosP23_pre"]]
        P23_FirstHitTime = ak.min(P23_Time , axis = 1)
        lxArr["Pre_CosP23"] = (lxArr[f"CosP23_pre"]) & (lxArr["nPE"] >= (NPEcut/12))  &  (lxArr[time] == P23_FirstHitTime) & (P23_FirstHitTime  > 0)  
        lxArr["Pre_CosP23"] = ak.fill_none(lxArr["Pre_CosP23"],[False], axis = 0) 
        lxArr["CosP23"] = ak.any ( lxArr["Pre_CosP23"] , axis = 1)
    
        for layer in range(4):
    
            #case 1: for muon passing straight across the detector and leave the hits along same column but different rows.
            for c in range(4):
                tag=(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1)) #FIXME: here an issue can occur. when a channel has no hit a event based "false" occur, the any(.., axis = 1) will crash is this true?
               
                eventList.append(tag)
                if layer <= 1:
                    #big hits along the rows at layer 0 and 1
                    DownEventList.append((tag) & (lxArr["CosP01"]) )
                else:
                    #big hits along the rows at layer 2 and 3
                    DownEventList.append((tag) & (lxArr["CosP23"]) )
    
    
            #case 2-1: for the  first three hits(count from the layer 3 to layer 0) are at the same column
            for c in range(3):
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
            
    
            #case 2-2: similar to case 2-1 but the hit at row 0 shift by -1
            for c in [1,2,3]:
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c}"], axis = 1))
    
            #path that cross three columns
            for c in [0,1]:
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c+2}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+2}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c+2}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c+1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c+2}"], axis = 1))
        
            for c in [2,3]:
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c-2}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-2}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c-2}"], axis = 1))
                eventList.append(ak.any(lxArr[f"L{layer}_r0_c{c}"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c{c-1}"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c{c-2}"], axis = 1))
                
    
            #diaganal path
            eventList.append(ak.any(lxArr[f"L{layer}_r0_c0"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c1"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c2"], axis = 1) & ak.any(lxArr[f"L{layer}_r3_c3"], axis = 1))
            eventList.append(ak.any(lxArr[f"L{layer}_r3_c0"], axis = 1) & ak.any(lxArr[f"L{layer}_r2_c1"], axis = 1) & ak.any(lxArr[f"L{layer}_r1_c2"], axis = 1) & ak.any(lxArr[f"L{layer}_r0_c3"], axis = 1))
       
    
        lay0Muon = []
        lay1Muon = []
        lay2Muon = []
        lay3Muon = []
    
        
        for index,path in enumerate(DownEventList):
            if index == 0: SpassArr = path 
            else: SpassArr = SpassArr | path
    
    
        for index, path in enumerate(eventList):
    
            #section for checking wether a event passes the muon cut
            if index == 0: passArr = path # create an intial array
            else: passArr = passArr | path #the events that have interesting path will be saved
    
            #section for checking which layer passes the muon cut
    
            #there are 36 muon paths. So the size(outtermost) of array eventList is 36 * 4. index / 36 = layer number
            if (index // 36) == 0: #// : division with round down
                if index == 0:
                    lay0Muon = path
                else: lay0Muon = lay0Muon | path
            elif (index // 36) == 1:
                if index == 36:
                    lay1Muon = path
                else: lay1Muon = lay1Muon | path
            elif (index // 36) == 2:
                if index == 72:
                    lay2Muon = path
                else: lay2Muon = lay2Muon | path
            elif (index // 36) == 3:
                if index == 108:
                    lay3Muon = path
                else: lay3Muon = lay3Muon | path
                
        
        #tag the bar pulses at layerX where muon event can be found
        l0Arr = (lay0Muon) & ((self.events["layer"]==0) & (self.events["barCut"]))
        l1Arr = (lay1Muon) & ((self.events["layer"]==1)  & (self.events["barCut"]))
        l2Arr = (lay2Muon) & ((self.events["layer"]==2)  & (self.events["barCut"]))
        l3Arr = (lay3Muon) & ((self.events["layer"]==3)  & (self.events["barCut"]))
        
        lay0Muon_T =  [[x] for x in lay0Muon]
        lay1Muon_T =  [[x] for x in lay1Muon]
        lay2Muon_T =  [[x] for x in lay2Muon]
        lay3Muon_T =  [[x] for x in lay3Muon]
        CleanEventTags = np.concatenate((lay0Muon_T,lay1Muon_T,lay2Muon_T,lay3Muon_T),axis = 1) 
        self.events["Clean_MuonEvent"] = ak.count_nonzero(CleanEventTags,axis = 1) == 1
        #print(ak.to_list(self.events["event"][self.events["Clean_MuonEvent"]])) #used for debug only to check which event pass this tag
    
       
        #tag the pulses that is at the adjacent layers where muon event can be found
        adj0,adj1,adj2,adj3=self.adjLayerData(l0Arr,l1Arr,l2Arr,l3Arr) 
    
        #put the layer constraint tags back to the array
        self.events["MuonL0"] = l0Arr
        self.events["MuonL1"] = l1Arr      
        self.events["MuonL2"] = l2Arr      
        self.events["MuonL3"] = l3Arr
        self.events["MuonLayers"] = l0Arr | l1Arr | l2Arr | l3Arr   #pulse based tag. it is used to collect all of the bar channel pulses at the muon event layer
        self.events["otherlayer"] = ~self.events["MuonLayers"] #tag for layers that can't find the muon event.
        self.events["MuonADJL0"] = (self.events["layer"]==0) & (adj0)
        self.events["MuonADJL1"] = (self.events["layer"]==1) & (adj1)      
        self.events["MuonADJL2"] = (self.events["layer"]==2) & (adj2)      
        self.events["MuonADJL3"] = (self.events["layer"]==3) & (adj3)
        self.events["MuonADJLayers"] = self.events["MuonADJL0"] | self.events["MuonADJL1"] | self.events["MuonADJL2"] | self.events["MuonADJL3"]
    
        #put the new straight muon tag back to arrays
        self.events["StraghtCosmic"] = passArr
        self.events["downwardPath"] = SpassArr #straight downward path. Hits 
        #check the number of events that can pass the cosmic straight cut
        print(f"cosmic straight : {len(self.events['event'][self.events['StraghtCosmic']])}")


    def offlinePreProcess(self,cutName = None, cut = None, startTime = 1250, endTime = 1350):
        """
        This function is to remove pulse outside specific window when doing comsic muon event offline analysis.
        """
        removePulse_T = (self.events["timeFit_module_calibrated"] >= startTime) & (self.events["timeFit_module_calibrated"] <=endTime)
        
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

    def findMaxNPE(self):
        """
        find the max pulse NPE for each channel or max pulse bar NPE for each event
        """
        self.events["MaxNPE"] = ak.max(self.events["nPE"][self.events["barCut"]], axis = 1)
        
    
        for layer in range(4):
            for row in range(4):
                for column in range(4):
                    tag=(self.events["layer"] == layer) & (self.events["column"] == column) & (self.events["row"] == row) & (self.events["barCut"])
                    #set the none to be  -100 so max can work
                    self.events[f"MAXNPE_l{layer}_r{row}_c{column}"] = self.events["nPE"][tag]
                    self.events[f"MAXNPE_l{layer}_r{row}_c{column}"] = ak.fill_none(self.events[f"MAXNPE_l{layer}_r{row}_c{column}"], -100)
                    self.events[f"MAXNPE_l{layer}_r{row}_c{column}"] = ak.max(self.events[f"MAXNPE_l{layer}_r{row}_c{column}"], axis = 1)
                    


    def getCut(self, func, name, *args, **kwargs):
        if func.__name__ == 'combineCuts':
            lam_ = lambda: func(name, args[0])
        else:
            lam_ = lambda: func(*args, **kwargs, cutName=name)
        lam_.__name__ = name
        lam_.__parent__ = func.__name__
        return lam_
