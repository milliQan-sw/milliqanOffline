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
        cut=False
        if 'cut' in kwargs and kwargs['cut']:
            cut=True
        self.cutflowCounter(modified_name, cut)

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
        cut=False
        if 'cut' in dkwargs and dkwargs['cut']:
            cut=True
        myclass.cutflowCounter(modified_name, cut)

    wrapper.__name__ = modified_name
    return wrapper

class milliqanCuts():

    def __init__(self):
        self.events = []
        self.cutflow = {}
        self.counter = 0

    def cutflowCounter(self, name, cut):
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
            this_cutflow = {'events': len(remaining), 'pulses': len(ak.flatten(self.events['fileNumber'])), 'cut': cut}
            self.cutflow[name]=this_cutflow
        self.counter+=1

        '''if name=='firstPulseMax':
            print("firstPulseMax")
            print(self.cutflow[name])
            print(remaining)
        if name=='pickupCut':
            print("pickupCut")
            print(self.cutflow[name])
            print(remaining)'''

    def getCutflowCounts(self):
        # Prints the value after each batch of events
        print("----------------------------------Cutflow Table------------------------------------")
        print ("{:<25} {:<20} {:<20} {:<30}".format('Cut', 'N Passing Events', 'N Passing Pulses', 'Cut Applied'))
        print('-----------------------------------------------------------------------------------')
        for key, value in self.cutflow.items():
            #print(i, len(self.cutflow))
            realCut = 'True' if value['cut'] else 'False'
            print("{:<25} {:<20} {:<20} {:<30}".format(key, value['events'], value['pulses'], realCut))
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
    def fullEventCounter(self, cutName=None, cut=False):
        dummy = False

    @mqCut
    def pickupCut(self, cutName='pickupCut', cut=False, tight=False, branches=None):
        #need to define another cut so that the branch doesn't get cut first, alternatively can ensure it is last in the branches list
        if tight: mycut = ~self.events.pickupFlagTight
        else: mycut = ~self.events.pickupFlag
        self.events[cutName] = mycut
        '''if 'pickupFlag' in branches: 
            branches.remove('pickupFlag')
            branches.append('pickupFlag')
        if 'pickupFlagTight' in branches:
            branches.remove('pickupFlagTight')
            branches.append('pickupFlagTight')
        '''
        if cut and tight:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]
        elif cut and not tight:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    @mqCut
    def boardsMatched(self, cutName=None, cut=False, branches=None):
        _, self.events['boardsMatched'] = ak.broadcast_arrays(self.events.pickupFlag, self.events.boardsMatched)
        
        if cut:
            for branch in branches:
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
    def fourLayerCut(self, cutName='fourLayerCut', cut=False, branches=None):
        allLayers =(ak.any(self.events.layer==0, axis=1) & 
                    ak.any(self.events.layer==1, axis=1) & 
                    ak.any(self.events.layer==2, axis=1) & 
                    ak.any(self.events.layer==3, axis=1))
        _, allLayers = ak.broadcast_arrays(self.events.npulses, allLayers)
        self.events[cutName] = allLayers
        if cut: 
            for branch in branches:
                self.events[branch] = self.events[branch][self.events.fourLayerCut]

    @mqCut
    def oneHitPerLayerCut(self, cutName='oneHitPerLayerCut', cut=False, multipleHits=False, branches=None):
        if multipleHits:
            layer0 = (self.events.layer==0) & (self.events['type']==0)
            layer1 = (self.events.layer==1) & (self.events['type']==0)
            layer2 = (self.events.layer==2) & (self.events['type']==0)
            layer3 = (self.events.layer==3) & (self.events['type']==0)
    
            unique0 = ak.Array([np.unique(x) for x in self.events.chan[layer0]])
            unique1 = ak.Array([np.unique(x) for x in self.events.chan[layer1]])
            unique2 = ak.Array([np.unique(x) for x in self.events.chan[layer2]])
            unique3 = ak.Array([np.unique(x) for x in self.events.chan[layer3]])
    
            layerCut = (
                        (ak.count_nonzero(unique0, axis=1)==1) &
                        (ak.count_nonzero(unique1, axis=1)==1) &
                        (ak.count_nonzero(unique2, axis=1)==1) &
                        (ak.count_nonzero(unique3, axis=1)==1)
                        )
        else:
            layerCut = (
                        (ak.count_nonzero((self.events.layer==0) & (self.events['type']==0), axis=1)==1) &
                        (ak.count_nonzero((self.events.layer==1) & (self.events['type']==0), axis=1)==1) &
                        (ak.count_nonzero((self.events.layer==2) & (self.events['type']==0), axis=1)==1) &
                        (ak.count_nonzero((self.events.layer==3) & (self.events['type']==0), axis=1)==1)
                        )

        #because this is an event level cut, need to broadcast to pulses
        _, layerCut = ak.broadcast_arrays(self.events.npulses, layerCut)
        self.events[cutName] = layerCut

        if cut: 
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]           

    #create mask for pulses passing height cut
    def heightCut(self, cutName='heightCut', heightCut=1200, cut=False, branches=None):
        self.events[cutName] = self.events.height >= int(heightCut)
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]
                
    #create mask for pulses passing area cuts
    @mqCut
    def areaCut(self, cutName='areaCut', areaCut=50000, cut=False, branches=None):
        self.events[cutName] = self.events.area >= int(areaCut)
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    @mqCut
    def nPECut(self, cutName='nPECut', nPECut=2, cut=False, branches=None):
        self.events[cutName] = self.events.nPE >= int(nPECut)
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

    @mqCut
    def panelVeto(self, cutName='panelVeto', nPECut=None, cut=False, branches=None):
        if nPECut:
            panelVeto = ak.any((self.events['type'] == 2) & (self.events['nPE'] > nPECut), axis=1)
        else:
            panelVeto = ak.any(self.events['type'] == 2, axis=1)
        _, self.events[cutName] = ak.broadcast_arrays(self.events.npulses, ~panelVeto)
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

        for i, x in enumerate(range(4)):
            for j, y in enumerate(range(4)):

                rowCut = self.events.row == y
                colCut = self.events.column == x

                r_tmp0 = (rowCut[self.events.layer==0] & colCut[self.events.layer==0])
                r_tmp1 = (rowCut[self.events.layer==1] & colCut[self.events.layer==1])
                r_tmp2 = (rowCut[self.events.layer==2] & colCut[self.events.layer==2])
                r_tmp3 = (rowCut[self.events.layer==3] & colCut[self.events.layer==3])


                row_pass = ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(r_tmp3, axis=1)

                if allowedMove:

                    print("Allowing move")
                    rowCut_p1 = self.events.row == y+1
                    rowCut_m1 = self.events.row == y-1
                    colCut_p1 = self.events.column == x+1
                    colCut_m1 = self.events.column == x-1
                    if(y > 0): 
                        m1_c0_r1 = (rowCut_m1[self.events.layer==1]) & (colCut[self.events.layer==1])
                        m2_c0_r1 = (rowCut_m1[self.events.layer==2]) & (colCut[self.events.layer==2])
                        m3_c0_r1 = (rowCut_m1[self.events.layer==3]) & (colCut[self.events.layer==3])
                    if(x > 0): 
                        m1_c1_r0 = (rowCut[self.events.layer==1]) & (colCut_m1[self.events.layer==1])
                        m2_c1_r0 = (rowCut[self.events.layer==2]) & (colCut_m1[self.events.layer==2])
                        m3_c1_r0 = (rowCut[self.events.layer==3]) & (colCut_m1[self.events.layer==3])

                    if(y < 4): 
                        p1_c0_r1 = (rowCut_p1[self.events.layer==1]) & (colCut[self.events.layer==1])
                        p2_c0_r1 = (rowCut_p1[self.events.layer==2]) & (colCut[self.events.layer==2])
                        p3_c0_r1 = (rowCut_p1[self.events.layer==3]) & (colCut[self.events.layer==3])
                    if(x < 4): 
                        p1_c1_r0 = (rowCut[self.events.layer==1]) & (colCut_p1[self.events.layer==1])
                        p2_c1_r0 = (rowCut[self.events.layer==2]) & (colCut_p1[self.events.layer==2])
                        p3_c1_r0 = (rowCut[self.events.layer==3]) & (colCut_p1[self.events.layer==3])

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
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        
        self.events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
        self.events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))
        
    #select self.events that have 3 height saturating pulses in a line
    @mqCut
    def threeHeightSaturatedInLine(self, heightCut=50000):
        #make sure 3 layers have saturating hits
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        
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
        triggers = ak.to_numpy(triggers, allow_missing=True)
        selection = ak.Array((triggers == binary_trig))
        selection = ak.fill_none(selection, False)

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
        triggers = ak.to_numpy(triggers, allow_missing=True)
        selection = ak.Array((triggers != binary_trig))
        selection = ak.fill_none(selection, False)

        selection, _ = ak.broadcast_arrays(selection, self.events['tTrigger'])
        self.events[cutName] = selection

        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][selection]

    @mqCut
    def firstPulseCut(self, cutName='firstPulse', cut=False, branches=None):

        self.events[cutName] = self.events.ipulse == 0

        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]

    @mqCut
    def threeInLine(self, cutName='threeInLine', cut=False, branches=None):
        npeCut = 2

        for path in range(16):

            row = path//4
            col = path%4

            outputName = 'threeHitPath{}'.format(path)

            #print("Checking three in line for path {}, row {}, col {}, with area cut {}".format(path, row, col, areaCut))

            layer0 = (self.events.layer == 0) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
            layer1 = (self.events.layer == 1) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
            layer2 = (self.events.layer == 2) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
            layer3 = (self.events.layer == 3) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)

            threeStraight_f0 = ak.any(layer1, axis=1) & ak.any(layer2, axis=1) & ak.any(layer3, axis=1)
            threeStraight_f1 = ak.any(layer0, axis=1) & ak.any(layer2, axis=1) & ak.any(layer3, axis=1)
            threeStraight_f2 = ak.any(layer0, axis=1) & ak.any(layer1, axis=1) & ak.any(layer3, axis=1)
            threeStraight_f3 = ak.any(layer0, axis=1) & ak.any(layer1, axis=1) & ak.any(layer2, axis=1)

            self.events[outputName+'_f0'] = threeStraight_f0
            self.events[outputName+'_f1'] = threeStraight_f1
            self.events[outputName+'_f2'] = threeStraight_f2
            self.events[outputName+'_f3'] = threeStraight_f3

            #get just the pulses that pass that made the selections
            _, b0 = ak.broadcast_arrays(self.events.nPE, threeStraight_f0)
            _, b1 = ak.broadcast_arrays(self.events.nPE, threeStraight_f1)
            _, b2 = ak.broadcast_arrays(self.events.nPE, threeStraight_f2)
            _, b3 = ak.broadcast_arrays(self.events.nPE, threeStraight_f3)

            self.events[outputName+'_p0'] = (b0) & ((layer1) | (layer2) | (layer3))
            self.events[outputName+'_p1'] = (b1) & ((layer0) | (layer2) | (layer3))
            self.events[outputName+'_p2'] = (b2) & ((layer0) | (layer1) | (layer3))
            self.events[outputName+'_p3'] = (b3) & ((layer0) | (layer1) | (layer2))

            self.events[outputName+'_s0'] = (threeStraight_f0) & (self.events.layer == 0) & (self.events.nPE >= npeCut)
            self.events[outputName+'_s1'] = (threeStraight_f1) & (self.events.layer == 1) & (self.events.nPE >= npeCut)
            self.events[outputName+'_s2'] = (threeStraight_f2) & (self.events.layer == 2) & (self.events.nPE >= npeCut)
            self.events[outputName+'_s3'] = (threeStraight_f3) & (self.events.layer == 3) & (self.events.nPE >= npeCut)

            allPulses = (self.events[outputName+'_p0'] | self.events[outputName+'_p1'] | self.events[outputName+'_p2'] | self.events[outputName+'_p3'])

            if path == 0:
                allPaths = allPulses
            else:
                allPaths = allPaths | allPulses

        self.events['threeHitPath_allPulses'] = allPaths

    def getCut(self, func, name, *args, **kwargs):
        if func.__name__ == 'combineCuts':
            lam_ = lambda: func(name, *args, **kwargs)
        else:
            lam_ = lambda: func(*args, cutName=name, **kwargs)
        lam_.__name__ = name
        lam_.__parent__ = func.__name__
        setattr(self, name, lam_)
        return lam_