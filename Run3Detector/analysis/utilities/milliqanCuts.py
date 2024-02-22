#!/usr/bin/python3

import awkward as ak

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
                self.events[branch] = self.events[branch][self.events.pickupFlag]
        elif cut and not tight:
            for branch in branches:
                if branch == 'boardsMatched': continue
                self.events[branch] = self.events[branch][self.events.pickupFlag]

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

    #event level mask selecting events with 1 hit in each layer
    def oneHitPerLayerCut(self, cutName=None, cut=False):
        #find the number of unique bar channels get hit
        #I assume the bar trimming is done, so the self.events.chan only has the the data from bar channel
        UniqueBarHits = []
        for barData in self.events.chan:
            UniqueBarHits.append(len(set(barData)))
        
        self.events["uniqueBarHits"] = UniqueBarHits

        self.events['oneHitPerLayerCut'] =((self.events.uniqueBarHits==4) & 
                                           self.events['fourLayerCut'])
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

    def getCut(self, func, name, *args, **kwargs):
        if func.__name__ == 'combineCuts':
            lam_ = lambda: func(name, args[0])
        else:
            lam_ = lambda: func(*args, **kwargs, cutName=name)
        lam_.__name__ = name
        lam_.__parent__ = func.__name__
        return lam_
