#!/usr/bin/python3

import awkward as ak
import numpy as np
import functools
#from wrapper import mqCut
#import copy

# defining a decorator  
def mqCut(func):   
    modified_name = func.__name__
    
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):  
        func(self, *args, **kwargs)
        self.cutflowCounter(modified_name)

    wrapper.__name__ = modified_name
    return wrapper

#def getCutMod(myclass=None, func=None, name=None, *args, **kwargs):
def getCutMod(func, myclass, name=None, *dargs, **dkwargs):
    modified_name = func.__name__
    if name is not None:
        modified_name = name
    func = func.__wrapped__
    setattr(myclass, modified_name, func)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #print("Inside wrapper", modified_name, args, kwargs)
        func(myclass, *dargs, **dkwargs)
        myclass.cutflowCounter(modified_name)

    wrapper.__name__ = modified_name
    return wrapper

class milliqanCuts():

    def __init__(self):
        self.events = []
        self.cutflow = {}
        self.counter = 0

    def cutflowCounter(self, name):
        # Increments events passing each stage of the cutflow
        # Creates each stage during the first pass

        #use fileNumber because it is never 0 (ex event) and it always exists

        threshold = 1
        if name == 'totalEventCounter': threshold = 0

        if name in self.cutflow:

            remaining = ak.sum(self.events['fileNumber'], axis=1) >= threshold
            remaining = self.events['fileNumber'][remaining]
            self.cutflow[name]['events'] += len(remaining)
            self.cutflow[name]['pulses'] += len(ak.flatten(self.events['fileNumber']))

        else:
            remaining = ak.sum(self.events['fileNumber'], axis=1) >= threshold
            remaining = self.events['fileNumber'][remaining]
            this_cutflow = {'events': len(remaining), 'pulses': len(ak.flatten(self.events['fileNumber']))}
            self.cutflow[name]=this_cutflow
        self.counter+=1

    def getCutflowCounts(self):
        # Prints the value after each batch of events
        # TODO: Only print at the very end
        print("----------------------------------Cutflow Table------------------------------------")
        print ("{:<25} {:<20} {:<10}".format('Cut', 'N Passing Events', 'N Passing Pulses'))
        print('-----------------------------------------------------------------------------------')
        for key, value in self.cutflow.items():
            #print(i, len(self.cutflow))
            print("{:<25} {:<20} {:<10}".format(key, value['events'], value['pulses']))
        print("-----------------------------------------------------------------------------------")
        # Resets the counter at the end of the cutflow
        self.counter=0

    #function to allow multiple masks (cuts) to be combined together and saved as name
    @mqCut
    def combineCuts(self, name, cuts):
        for cut in cuts:
            if name in ak.fields(self.events):
                self.events[name] = self.events[name] & (self.events[cut])
            else:
                self.events[name] = self.events[cut]

    @mqCut
    def totalEventCounter(self, cutName=None, cut=False):
        #if cut: self.events = self.events
        #dummy function to just count total events
        dummy = False

    @mqCut
    def pickupCut(self, cutName=None, cut=False, tight=False, branches=None):
        if cut and tight:
            for branch in branches:
                self.events[branch] = self.events[branch][~self.events.pickupFlag]
        elif cut and not tight:
            for branch in branches:
                if branch == 'boardsMatched': continue
                self.events[branch] = self.events[branch][~self.events.pickupFlag]

    @mqCut
    def boardsMatched(self, cutName=None, cut=False, branches=None):
        self.events['boardsMatched'], junk = ak.broadcast_arrays(self.events.boardsMatched, self.events.pickupFlag)
        
        if cut:
            for branch in branches:
                if branch == 'boardsMatched': continue
                self.events[branch] = self.events[branch][self.events.boardsMatched]

    @mqCut
    def countTriggers(self, cutName='countTriggers', trigNum=2):
        triggers = ak.firsts(self.events['tTrigger'])
        binary_trig = 1 << (trigNum-1)
        #print("Binary", trigNum, binary_trig)
        thisTrig = ak.count(triggers[triggers == binary_trig], axis=None)
        #print("instances of trigger {}, {}".format(trigNum, thisTrig))
        self.events[cutName] = thisTrig

    @mqCut
    def firstEvent(self):
        events = ak.firsts(self.events['event'])
        mask = np.zeros(len(events), dtype=bool)
        mask[0] = True
        mask = ak.Array(mask)
        self.events['firsts'] = mask
        #create mask for pulses in each layer

    @mqCut
    def layerCut(self):
        self.events['layer0'] = self.events.layer == 0
        self.events['layer1'] = self.events.layer == 1
        self.events['layer2'] = self.events.layer == 2
        self.events['layer3'] = self.events.layer == 3

    #event level mask selecting events with hits in 4 layers
    @mqCut
    def fourLayerCut(self, cutName=None, cut=False, branches=None):
        self.events['fourLayerCut'] =(ak.any(self.events.layer==0, axis=1) & 
                                      ak.any(self.events.layer==1, axis=1) & 
                                      ak.any(self.events.layer==2, axis=1) & 
                                      ak.any(self.events.layer==3, axis=1))
        if cut: 
            for branch in branches:
                self.events[branch] = self.events[branch][self.events.fourLayerCut]

    @mqCut
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
            self.events['oneHitPerLayerCut'] = (
                                            (ak.count_nonzero((self.events.layer==0) & (self.events['type']==0), axis=1)==1) &
                                            (ak.count_nonzero((self.events.layer==1) & (self.events['type']==0), axis=1)==1) &
                                            (ak.count_nonzero((self.events.layer==2) & (self.events['type']==0), axis=1)==1) &
                                            (ak.count_nonzero((self.events.layer==3) & (self.events['type']==0), axis=1)==1)
                                            )
        if cut: self.events = self.events[self.events.oneHitPerLayerCut]            
        self.cutflowCounter()

    #create mask for pulses passing area cuts
    @mqCut
    def areaCut(self, cutName='areaCut', areaCut=50000, cut=False, branches=None):
        self.events[cutName] = self.events.area >= int(areaCut)
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    @mqCut
    def heightCut(self, cutName='heightCut', heightCut=800, cut=False, branches=None):
        self.events[cutName] = self.events.height >= int(heightCut)
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    #First pulse in a given channel
    @mqCut
    def firstChanPulse(self):
        self.events['firstChanPulse'] = self.events.ipulse == 0

    @mqCut
    def barCut(self, cutName='barCut', cut=False, branches=None):
        self.events[cutName] = self.events['type'] == 0
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    @mqCut
    def panelCut(self, cutName='panelCut', cut=False, branches=None):
        self.events[cutName] = self.events['type'] == 2
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    @mqCut
    def slabCut(self, cutName='slabCut', cut=False, branches=None):
        self.events[cutName] = self.events['type'] == 1
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    #selection events that have hits in a straight path
    #option allowedMove will select events that only move one bar horizontally/vertically
    @mqCut
    def straightLineCut(self, cutName='straightLineCut', allowedMove=False, cut=False, branches=None):
        
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

                    print("Allowing move")
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

        self.events[cutName] = straight_path

        for x in range(4):
            for y in range(4):
                if(x == 0 and y == 0): straight_pulse = (straight_cuts[4*x+y]) & (self.events.column == x) & (self.events.row == y)
                else: straight_pulse = (straight_pulse) | ((straight_cuts[4*x+y]) & (self.events.column == x) & (self.events.row == y))

        self.events[cutName+'Pulse'] = straight_pulse

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

        if cut:
            for branch in branches:
                #print(branch)
                self.events[branch] = self.events[branch][self.events[cutName+'Pulse']]

    @mqCut
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
    @mqCut
    def threeAreaSaturatedInLine(self, areaCut=50000):
        #make sure 3 layers have saturating hits
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= areaCut) & (self.events.straightPulseCut)]
        
        self.events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
        self.events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))
        
    #select self.events that have 3 height saturating pulses in a line
    @mqCut
    def threeHeightSaturatedInLine(self, heightCut=50000):
        #make sure 3 layers have saturating hits
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= heightCut) & (self.events.straightPulseCut)]
        
        self.events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
        self.events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))

    @mqCut
    def matchedTDCTimes(self):
        board0 = self.events.v_groupTDC_g0[:, 0]
        board1 = self.events.v_groupTDC_g0[:, 1]
        board2 = self.events.v_groupTDC_g0[:, 2]
        board3 = self.events.v_groupTDC_g0[:, 3]
        board4 = self.events.v_groupTDC_g0[:, 4]

        self.events['tdcMatch'] = (board0 == board1) & (board0 == board2) & (board0 == board3) & (board0 == board4) 

    @mqCut
    def centralTime(self, cutName='centralTime', cut=False, branches=None):
        events = self.events
        timeCut = (events['timeFit_module_calibrated'] > 1100) & (events['timeFit_module_calibrated'] < 1400)
        drop_empty = ak.num(timeCut) > 0
        newEvents = drop_empty & timeCut

        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][newEvents]     

    def to_binary(self, x):
        return bin(int(x))[2:]

    @mqCut
    def triggerCut(self, cutName='triggerSelction', trigger=1, cut=False, branches=None):

        triggers = ak.firsts(self.events['tTrigger'])
        binary_trig = self.to_binary(trigger)

        # Apply the conversion function to each element in the Awkward Array
        triggers = ak.Array([self.to_binary(i) if i is not None else None for i in triggers])
        selection = triggers == binary_trig

        selection, _ = ak.broadcast_arrays(selection, self.events['tTrigger'])
        self.events[cutName] = selection

        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][selection]  

    @mqCut
    def triggerCutNot(self, cutName='triggerSelction', trigger=1, cut=False, branches=None):

        triggers = ak.firsts(self.events['tTrigger'])
        binary_trig = self.to_binary(trigger)

        # Apply the conversion function to each element in the Awkward Array
        triggers = ak.Array([self.to_binary(i) if i is not None else None for i in triggers])
        selection = (triggers != binary_trig)

        selection, _ = ak.broadcast_arrays(selection, self.events['tTrigger'])
        self.events[cutName] = selection

        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][selection]

    def getCut(self, func, name, *args, **kwargs):
        if func.__name__ == 'combineCuts':
            lam_ = lambda: func(name, *args, **kwargs)
        else:
            lam_ = lambda: func(*args, cutName=name, **kwargs)
        lam_.__name__ = name
        lam_.__parent__ = func.__name__
        setattr(self, name, lam_)
        return lam_
