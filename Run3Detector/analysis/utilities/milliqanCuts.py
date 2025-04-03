#!/usr/bin/python3

import awkward as ak
import numpy as np
import functools
import inspect
import itertools
import os
import json

# defining a decorator  
def mqCut(func):   
    modified_name = func.__name__
    
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):  
        cut=False
        if 'cut' in kwargs and kwargs['cut']:
            cut=True

        func_signature = inspect.signature(func)
        if 'branches' in func_signature.parameters:
            # Handle default value for branches dynamically
            if 'branches' not in kwargs or kwargs['branches'] is None:
                kwargs['branches'] = self.branches

        result = func(self, *args, **kwargs)

        self.cutflowCounter(modified_name, cut)

        return result

    wrapper.__name__ = modified_name
    return wrapper

#modifies arguments of methods and returns altered function
def getCutMod(func, myclass, name=None, *dargs, **dkwargs):
    modified_name = func.__name__
    if name is not None:
        modified_name = name
    func = func.__wrapped__
    setattr(myclass, modified_name, func)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_signature = inspect.signature(func)

        cut=False
        if 'cut' in dkwargs and dkwargs['cut']:
            cut=True

        if 'branches' in func_signature.parameters:
            
            # Handle default value for branches dynamically
            if 'branches' not in dkwargs or dkwargs['branches'] is None:
                dkwargs['branches'] = myclass.branches
        
        dkwargs['cutName'] = modified_name

        func(myclass, *dargs, **dkwargs)

        myclass.cutflowCounter(modified_name, cut)

    wrapper.__name__ = modified_name
    return wrapper

#class to handle all milliqan cuts
class milliqanCuts():

    def __init__(self):
        self.events = []
        self.cutflow = {}
        self.counter = 0
        self.branches = []
        self.configDir = '../../configuration/'
        self.debug = False
        self.selectionEfficiencies = False

    def to_binary(self, x):
        return bin(int(x))[2:]

    #method to keep count of events/pulses passing all cuts
    def cutflowCounter(self, name, cut):
        # Increments events passing each stage of the cutflow
        # Creates each stage during the first pass

        #use fileNumber because it is never 0 (ex event) and it always exists
        threshold = 1
        if name == 'totalEventCounter': threshold = 0

        skipSelectionEff = ['totalEventCounter', 'fullEventCounter', 'applyEnergyScaling']

        #option to print out selection efficiencies if no cuts are actually made
        if self.selectionEfficiencies and cut:
            remaining = ak.sum(self.events['fileNumber'][self.events[name]], axis=1) >= threshold
            remaining = self.events['fileNumber'][remaining]
        else:
            remaining = ak.sum(self.events['fileNumber'], axis=1) >= threshold
            remaining = self.events['fileNumber'][remaining]

        if name in self.cutflow:
            self.cutflow[name]['events'] += len(remaining)
            self.cutflow[name]['pulses'] += len(ak.flatten(self.events['fileNumber']))
    
        else:
            this_cutflow = {'events': len(remaining), 'pulses': len(ak.flatten(self.events['fileNumber'])), 'cut': cut}
            self.cutflow[name]=this_cutflow
            
        self.counter+=1

    #print out all of the cutflows
    #if blind is set to the name of a cutflow cut nothing from that cut on will print
    def getCutflowCounts(self, blind=None):
        nonSkip = ['totalEventCounter', 'fullEventCounter']
        # Prints the value after each batch of events
        print("----------------------------------Cutflow Table----------------------------------------------------------------------------------")
        print ("{:<25} {:<20} {:<25} {:<20} {:<25} {:<30}".format('Cut', 'N Passing Events', 'Cum Event Eff % (Prev)', 'N Passing Pulses', 'Cum Pulse Eff % (Prev)', 'Cut Applied'))
        print('---------------------------------------------------------------------------------------------------------------------------------')
        prevEvents = -1
        prevPulses = -1
        totalEvents = -1
        totalPulses = -1
        for ival, (key, value) in enumerate(self.cutflow.items()):

            if blind is not None and key == blind:
                break
            
            realCut = 'True' if value['cut'] else 'False'

            if not self.debug and not value['cut'] and key not in nonSkip: 
                continue

            evtEff, pulseEff = 1.0, 1.0
            cumEvtEff, cumPulseEff = 1.0, 1.0
            if prevEvents > 0:
                evtEff = value['events'] / prevEvents
            if prevPulses > 0:
                pulseEff = value['pulses'] / prevPulses
            if prevEvents == 0:
                evtEff = 0.0
            if prevPulses == 0:
                pulseEff = 0.0
            if key=='totalEventCounter':
                totalEvents = value['events']
                totalPulses = value['pulses']
            
            evtEff = round(evtEff*100, 3)
            pulseEff = round(pulseEff*100, 3)

            cumEvtEff = round(value['events']/totalEvents*100, 3)
            cumPulseEff = round(value['pulses']/totalPulses*100, 3)

            allEvt = f"{cumEvtEff} ({evtEff})"
            allPulse = f"{cumPulseEff} ({pulseEff})"

            print("{:<25} {:<20} {:<25} {:<20} {:<25} {:<30}".format(key, value['events'], allEvt, value['pulses'], allPulse, realCut))
            prevEvents = value['events']
            prevPulses = value['pulses']
        print("--------------------------------------------------------------------------------------------------------------------------------")
        # Resets the counter at the end of the cutflow
        self.counter=0

    #method to apply cut to a function, used by the decorator
    def cutBranches(self, branches, cutName):

        perChanBranches = ['sidebandRMS', 'sidebandMean']

        #self.events['fullSelection'] = self.events['fullSelection'] & self.events[cutName] #2/4

        if self.selectionEfficiencies: return

        for branch in branches:
            if branch in perChanBranches:
                continue
            elif branch not in self.events.fields:
                continue
            else:
                self.events[branch] = self.events[branch][self.events[cutName]]


    #function to allow multiple masks (cuts) to be combined together and saved as name
    @mqCut
    def combineCuts(self, name, cuts):
        for cut in cuts:
            if name in ak.fields(self.events):
                self.events[name] = self.events[name] & (self.events[cut])
            else:
                self.events[name] = self.events[cut]

    #depreciated method to alter cut arguments
    def getCut(self, func, name, *args, **kwargs):
        print("This method is depreciated, please use getCutMod instead...")
        if func.__name__ == 'combineCuts':
            lam_ = lambda: func(name, *args, **kwargs)
        else:
            lam_ = lambda: func(*args, cutName=name, **kwargs)
        lam_.__name__ = name
        lam_.__parent__ = func.__name__
        setattr(self, name, lam_)
        return lam_

    #counts the total number of events to add to cut flow counter
    @mqCut
    def totalEventCounter(self, cutName=None, cut=False, branches=None):
        #if cut: self.events = self.events
        #dummy function to just count total events
        dummy = False

    @mqCut
    def fullEventCounter(self, cutName=None, cut=False, branches=None):
        dummy = False

    #creates branch with mask for first event
    @mqCut
    def firstEvent(self, branches=None):
        events = ak.firsts(self.events['event'])
        mask = np.zeros(len(events), dtype=bool)
        mask[0] = True
        mask = ak.Array(mask)
        self.events['firsts'] = mask

    #############################
    ## Quality cuts selections
    #############################

    #selects events passing pickup cut
    @mqCut
    def pickupCut(self, cutName='pickupCut', cut=False, tight=False, branches=None):
        #need to define another cut so that the branch doesn't get cut first, alternatively can ensure it is last in the branches list
        if tight: mycut = ~self.events.pickupFlagTight
        else: mycut = ~self.events.pickupFlag
        self.events[cutName] = mycut

        if cut:
            self.cutBranches(branches, cutName)

    @mqCut
    def pickupCutCustom(self, cutName='pickupCutCustom', cut=False, branches=None):
        failRiseTime = self.events['riseSamples'] < 3
        failFallTime = self.events['fallSamples'] < 5
        #add height requirement to ensure saturating pulses with small rise/fall times are excluded
        heightReq = self.events['height'] < 450

        pickupFail = failRiseTime & failFallTime & heightReq
        self.events[cutName] = ~pickupFail

        if cut:
            self.cutBranches(branches, cutName)

    @mqCut
    def noiseCut(self, cutName='noiseCut', cut=False, branches=None):

        channelsHit = self.events['chan']

        #select  -5 <= prePulseMean <= 5
        passPrePulseMean = (self.events['prePulseMean'] >= -5) & (self.events['prePulseMean'] <= 5)

        #select prePulse RMS < 5
        passPrePulseRMS = self.events['prePulseRMS'] <= 5

        #select -5 <= sideband mean <= 5
        passSidebandMean = (self.events['sidebandMean'][channelsHit] >= -5) & (self.events['sidebandMean'][channelsHit] <= 5)

        #select sidebandRMS <= 5
        passSidebandRMS = self.events['sidebandRMS'][channelsHit] <= 5

        passNoise = passPrePulseMean & passSidebandRMS & passPrePulseRMS & passSidebandMean

        self.events['noiseCut'] = passNoise

        if cut:
            self.cutBranches(branches, cutName)

    @mqCut
    def darkRateCut(self, cutName='darkRateCut', cut=False, branches=None):

        #duration >= 50ns
        passDuration = self.events['duration'] >= 50

        #nPE > 0.3
        passNPE = self.events['nPE'] >= 0.3

        passDarkRate = passNPE & passDuration

        self.events[cutName] = passDarkRate

        if cut:
            self.cutBranches(branches, cutName)

    # selects events with matching digitizizer board times
    @mqCut
    def boardsMatched(self, cutName='boardsMatched', cut=False, branches=None):
        _, self.events[cutName] = ak.broadcast_arrays(self.events.pickupFlag, self.events.boardsMatched)
        
        if cut:
            self.cutBranches(branches, cutName)

    #creates mask to check if TDC times are matched (depreciated from boardsMatched)
    @mqCut
    def matchedTDCTimes(self, branches=None):
        board0 = self.events.v_groupTDC_g0[:, 0]
        board1 = self.events.v_groupTDC_g0[:, 1]
        board2 = self.events.v_groupTDC_g0[:, 2]
        board3 = self.events.v_groupTDC_g0[:, 3]
        board4 = self.events.v_groupTDC_g0[:, 4]

        self.events['tdcMatch'] = (board0 == board1) & (board0 == board2) & (board0 == board3) & (board0 == board4) 

    #creates mask/cut if there is a channel with a pulse and sidebandRMS > cutVal
    @mqCut
    def sidebandRMSCut(self, cutName='sidebandRMSCut', cutVal=2.0, cut=False, branches=None):

        sidebandVals = self.events['sidebandRMS']

        #cut only on channels with pulses in bars
        channelsHit = self.events['chan'][self.events['type'] == 0]
        sidebandsHit = sidebandVals[channelsHit]

        passCut = ak.any(sidebandsHit > cutVal, axis=1)

        self.events['sidebandsBeforeCut'] = sidebandsHit

        _, sidebandsHitMask = ak.broadcast_arrays(sidebandsHit, ~passCut)
        self.events['sidebandsAfterCut'] = sidebandsHit[sidebandsHitMask]

        _, passCut = ak.broadcast_arrays(self.events.npulses, passCut)
        self.events[cutName] = ~passCut

        if cut:
            self.cutBranches(branches, cutName)

    ############################################
    ## Trigger Cuts
    ############################################

    #creates branch counting number of triggers for given trigger number
    @mqCut
    def countTriggers(self, cutName='countTriggers', trigNum=2, branches=None):
        triggers = ak.firsts(self.events['tTrigger'])
        binary_trig = 1 << (trigNum-1)
        thisTrig = ak.count(triggers[triggers == binary_trig], axis=None)
        self.events[cutName] = thisTrig

    #creates mask/cut selecting trigger
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
            self.cutBranches(branches, cutName)

    #creates mask/cut selecting !trigger
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
            self.cutBranches(branches, cutName)

    #########################################
    ## Cuts on Layers/Number of Hits
    #########################################

    #creates branches with masks for each layer
    @mqCut
    def layerCut(self, branches=None):
        self.events['layer0'] = self.events.layer == 0
        self.events['layer1'] = self.events.layer == 1
        self.events['layer2'] = self.events.layer == 2
        self.events['layer3'] = self.events.layer == 3

    #cut on one hit per layer, if multipleHits==False cuts on exactly one hit per layer
    @mqCut
    def fourLayerCut(self, cutName=None, cut=False, branches=None):
        self.events['fourLayerCut'] =(ak.any(self.events.layer==0, axis=1) & 
                                      ak.any(self.events.layer==1, axis=1) & 
                                      ak.any(self.events.layer==2, axis=1) & 
                                      ak.any(self.events.layer==3, axis=1))
        if cut: 
            self.cutBranches(branches, cutName)

    #cut on one hit per layer, if multipleHits==False cuts on exactly one hit per layer
    @mqCut
    def oneHitPerLayerCut(self, cutName='oneHitPerLayer', cut=False, multipleHits=False, branches=None):

        barHits = self.events['layer'][self.events['type'] == 0]

        if multipleHits:
            nLayers = (
                ak.values_astype(ak.any(barHits==0, axis=1), np.int32) + 
                ak.values_astype(ak.any(barHits==1, axis=1), np.int32) + 
                ak.values_astype(ak.any(barHits==2, axis=1), np.int32) + 
                ak.values_astype(ak.any(barHits==3, axis=1), np.int32)
            )
        
        else:
            nLayers = (
                ak.values_astype(ak.count(barHits==0, axis=1) == 1, np.int32) + 
                ak.values_astype(ak.count(barHits==1, axis=1) == 1, np.int32) + 
                ak.values_astype(ak.count(barHits==2, axis=1) == 1, np.int32) + 
                ak.values_astype(ak.count(barHits==3, axis=1) == 1, np.int32)
            )

        layerCut = nLayers == 4

        self.events['nHitsPerLayerBefore'] = ak.concatenate([ak.count_nonzero(barHits==0, axis=1, keepdims=True), 
                                                                ak.count_nonzero(barHits==1, axis=1, keepdims=True),
                                                                ak.count_nonzero(barHits==2, axis=1, keepdims=True), 
                                                                ak.count_nonzero(barHits==3, axis=1, keepdims=True)], axis=1
                                                            )
        
        _, layerCutMod = ak.broadcast_arrays(self.events['nHitsPerLayerBefore'], layerCut[:, None])

        _, layerCut = ak.broadcast_arrays(self.events['npulses'], layerCut)

        self.events['nHitsPerLayerAfter'] = ak.mask(self.events['nHitsPerLayerBefore'], layerCutMod)

        self.events[cutName] = layerCut

        if cut:
            self.cutBranches(branches, cutName)  

    #cut on N layers hit in event
    @mqCut
    def nLayersCut(self, cutName='nLayers', nLayerCut=4, cut=False, branches=None):
        barHits = self.events['layer'][self.events['type'] == 0]
        nLayers = ak.values_astype(ak.any(barHits==0, axis=1), np.int32) + ak.values_astype(ak.any(barHits==1, axis=1), np.int32) + ak.values_astype(ak.any(barHits==2, axis=1), np.int32) + ak.values_astype(ak.any(barHits==3, axis=1), np.int32)
        _, nLayers = ak.broadcast_arrays(self.events.npulses, nLayers)
        self.events[cutName] = (nLayers == nLayerCut)
        if cutName not in self.branches:
            self.branches.append(cutName)

        if cut:
            self.cutBranches(branches, cutName)

    #creates mask/cut vetoing any event with > nBarsCut bars hit
    @mqCut
    def nBarsCut(self, cutName='nBarsCut', nBarsCut= 5, cut=False, branches=None):

        if 'countNBars' not in self.branches:
            barsCut = (self.events['type']==0)
            uniqueBars = ak.Array([np.unique(x) for x in self.events.chan[barsCut]])
            nBars = ak.count(uniqueBars, axis=1)
        else:
            nBars = self.events['countNBars']

        passCut = nBars <= nBarsCut
        _, passCut = ak.broadcast_arrays(self.events.npulses, passCut)
        self.events[cutName] = passCut

        if cut:
            self.cutBranches(branches, cutName)

    #inversion of nBarsCut, requires more than n bars hit
    @mqCut 
    def nBarsCutInvert(self, cutName='nBarsCutInvert', nBarsCut=6, cut=False, branches=None):
        if 'countNBars' not in self.branches:
            barsCut = (self.events['type']==0)
            uniqueBars = ak.Array([np.unique(x) for x in self.events.chan[barsCut]])
            nBars = ak.count(uniqueBars, axis=1)
        else:
            nBars = self.events['countNBars']

        passCut = nBars > nBarsCut
        _, passCut = ak.broadcast_arrays(self.events.npulses, passCut)
        self.events[cutName] = passCut

        if cut:
            self.cutBranches(branches, cutName)

    #########################################
    ## Cuts on Per Channel
    #########################################

    #creates branch with number of bars in event
    @mqCut
    def countNBars(self, cutName='countNBars'):
        barsCut = (self.events['type']==0)
        uniqueBars = ak.Array([np.unique(x) for x in self.events.chan[barsCut]])
        nBars = ak.count(uniqueBars, axis=1)
        _, nBars = ak.broadcast_arrays(self.events.npulses, nBars)
        self.events[cutName] = nBars
        if cutName not in self.branches:
            self.branches.append(cutName)

    #cuts on n bars with t window in an event
    @mqCut
    def nBarsDeltaTCut(self, cutName='nBarsDeltaTCut', nBarsCut=5, timeCut=100, cut=False, branches=None):

        times = self.events['timeFit_module_calibrated'][self.events['type']==0]

        combos = ak.combinations(times, nBarsCut)

        combinations = list(itertools.combinations(range(nBarsCut), 2))  # Get all combinations of 2

        passing = abs(combos["0"] - combos["1"]) < timeCut

        nBarsInWindow = ak.count_nonzero(passing, axis=1)

        for icut in combinations[1:]:
            this_pass = abs(combos[str(icut[0])] - combos[str(icut[1])]) < timeCut
            passing = passing & this_pass

        _, nBarsInWindow = ak.broadcast_arrays(self.events.npulses, nBarsInWindow)
        self.events['nBarsInWindowBefore'] = nBarsInWindow
        self.events['nBarsInWindow'] = nBarsInWindow
        if not 'nBarsInWindow' in self.branches:
            self.branches.append('nBarsInWindow')

        passCut = ak.any(passing, axis=1)  
        _, passCut = ak.broadcast_arrays(self.events.npulses, passCut)
        self.events[cutName] = ~passCut

        if cut:
            self.cutBranches(branches, cutName)

    #create mask/cut for pulses passing height cut
    @mqCut
    def heightCut(self, cutName='heightCut', heightCut=800, cut=False, branches=None):
        self.events[cutName] = self.events.height >= int(heightCut)
        if cut:
            self.cutBranches(branches, cutName)
                
    #create mask/cut for pulses passing area cuts
    @mqCut
    def areaCut(self, cutName='areaCut', areaCut=50000, barsOnly=False, cut=False, branches=None):

        if barsOnly:
            cutMask = (self.events['area'] < int(areaCut)) & (self.events['type'] == 0)
            cutMask = ~cutMask
        else:
            cutMask = self.events.area >= int(areaCut)
            
        self.events[cutName] = cutMask
        if cut:
            self.cutBranches(branches, cutName)

    #create mask/cut for pulses passing nPE cut
    @mqCut
    def nPECut(self, cutName='nPECut', nPECut=2, cut=False, branches=None):
        self.events[cutName] = self.events.nPE >= int(nPECut)
        if cut:
            self.cutBranches(branches, cutName)   

    @mqCut
    def nPEMaxCut(self, cutName='nPEMaxCut', nPECut=20, cut=False, branches=None):
        self.events[cutName] = self.events.nPE < int(nPECut)
        if cut:
            self.cutBranches(branches, cutName)

    @mqCut
    def energyMaxCut(self, cutName='energyMaxCut', energyCut=2.5, cut=False, branches=None):
        self.events[cutName] = self.events['energyCal'][self.events['type']==0] < energyCut
        if cut:
            self.cutBranches(branches, cutName)

    #creates mask/cut selecting bars only (no panels)
    @mqCut
    def barCut(self, cutName='barCut', cut=False, branches=None):
        self.events[cutName] = self.events['type'] == 0
        if cut:
            self.cutBranches(branches, cutName)

    ####################################
    ## Panel Selections
    #####################################

    #creates mask/cut selecting panels only (top/sides)
    @mqCut
    def panelCut(self, cutName='panelCut', cut=False, branches=None):
        self.events[cutName] = self.events['type'] == 2
        if cut:
            self.cutBranches(branches, cutName)

    #creates mask/cut selecting front/back panels (slabs)
    @mqCut
    def slabCut(self, cutName='slabCut', cut=False, branches=None):
        self.events[cutName] = self.events['type'] == 1
        if cut:
            self.cutBranches(branches, cutName)

    #creates mask/cut on panels in event, if nPECut!=None panels must also pass nPE cut
    @mqCut
    def panelVeto(self, cutName='panelVeto', nPECut=None, cut=False, branches=None):
        if nPECut:
            panelVeto = ak.any((self.events['type'] == 2) & (self.events['nPE'] > nPECut), axis=1)
        else:
            panelVeto = ak.any(self.events['type'] == 2, axis=1)

        panelVeto = ~panelVeto
        
        nPEBeforeCut = self.events['nPE'][self.events['type']==2]

        goodEvent = (ak.count(self.events['nPE'], axis=1) > 0)
        _, goodEvent = ak.broadcast_arrays(self.events.nPE, goodEvent)
        hitsBeforeCut = ak.where(goodEvent, ak.count(nPEBeforeCut, axis=1, keepdims=True), -1)

        self.events[cutName+'NPEBefore'] = nPEBeforeCut
        self.events[cutName+'HitsBefore'] = hitsBeforeCut
        
        _, cutAfter = ak.broadcast_arrays(nPEBeforeCut, panelVeto)
        _, panelVeto = ak.broadcast_arrays(self.events.npulses, panelVeto)

        nPEAfterCut = nPEBeforeCut[cutAfter]
        hitsAfterCut = ak.where(goodEvent&panelVeto, ak.count(nPEBeforeCut, axis=1, keepdims=True), -1)
        self.events[cutName+'NPEAfter']  = nPEAfterCut
        self.events[cutName+'HitsAfter'] = hitsAfterCut

        self.events[cutName] = panelVeto

        if cut:
            self.cutBranches(branches, cutName)

    #test allowing one panel to be hit
    @mqCut
    def panelVetoMod(self, cutName='panelVeto', areaCut=None, nPECut=None, cut=False, panelsAllowed=0, branches=None):

        panelNumVeto = ak.sum(self.events['type'] == 2, axis=1) > panelsAllowed
        if nPECut is not None:
            panelHitVeto = ak.any((self.events['type'] == 2) & (self.events['nPE'] > nPECut), axis=1)
            panelVeto = panelHitVeto | panelNumVeto
        elif areaCut is not None:
            panelHitVeto = ak.any((self.events['type'] == 2) & (self.events['area'] > areaCut), axis=1)
            panelVeto = panelHitVeto | panelNumVeto
        else:
            panelVeto = panelNumVeto

        panelVeto = ~panelVeto
        nPEBeforeCut = self.events['nPE'][self.events['type']==2]
        areaBeforeCut = self.events['area'][self.events['type']==2]

        goodEvent = (ak.count(self.events['nPE'], axis=1) > 0)
        _, goodEvent = ak.broadcast_arrays(self.events.nPE, goodEvent)
        hitsBeforeCut = ak.where(goodEvent, ak.count(nPEBeforeCut, axis=1, keepdims=True), -1)

        self.events[cutName+'NPEBefore'] = nPEBeforeCut
        self.events[cutName+'HitsBefore'] = hitsBeforeCut
        self.events[cutName+'AreaBefore'] = areaBeforeCut
        
        _, cutAfter = ak.broadcast_arrays(nPEBeforeCut, panelVeto)
        _, panelVeto = ak.broadcast_arrays(self.events.npulses, panelVeto)

        nPEAfterCut = nPEBeforeCut[cutAfter]
        areaAfterCut = areaBeforeCut[cutAfter]
        hitsAfterCut = ak.where(goodEvent&panelVeto, ak.count(nPEBeforeCut, axis=1, keepdims=True), -1)
        self.events[cutName+'NPEAfter']  = nPEAfterCut
        self.events[cutName+'HitsAfter'] = hitsAfterCut
        self.events[cutName+'AreaAfter'] = areaAfterCut

        self.events[cutName] = panelVeto

        if cut:
            self.cutBranches(branches, cutName)
    
    #test allowing one panel to be hit
    @mqCut
    def panelVetoMod(self, cutName='panelVeto', areaCut=None, nPECut=None, cut=False, panelsAllowed=0, branches=None):

        panelNumVeto = ak.sum(self.events['type'] == 2, axis=1) > panelsAllowed
        if nPECut is not None:
            panelHitVeto = ak.any((self.events['type'] == 2) & (self.events['nPE'] > nPECut), axis=1)
            panelVeto = panelHitVeto | panelNumVeto
        elif areaCut is not None:
            panelHitVeto = ak.any((self.events['type'] == 2) & (self.events['area'] > areaCut), axis=1)
            panelVeto = panelHitVeto | panelNumVeto
        else:
            panelVeto = panelNumVeto

        panelVeto = ~panelVeto
        nPEBeforeCut = self.events['nPE'][self.events['type']==2]
        areaBeforeCut = self.events['area'][self.events['type']==2]

        goodEvent = (ak.count(self.events['nPE'], axis=1) > 0)
        _, goodEvent = ak.broadcast_arrays(self.events.nPE, goodEvent)
        hitsBeforeCut = ak.where(goodEvent, ak.count(nPEBeforeCut, axis=1, keepdims=True), -1)

        self.events[cutName+'NPEBefore'] = nPEBeforeCut
        self.events[cutName+'HitsBefore'] = hitsBeforeCut
        self.events[cutName+'AreaBefore'] = areaBeforeCut
        
        _, cutAfter = ak.broadcast_arrays(nPEBeforeCut, panelVeto)
        _, panelVeto = ak.broadcast_arrays(self.events.npulses, panelVeto)

        nPEAfterCut = nPEBeforeCut[cutAfter]
        areaAfterCut = areaBeforeCut[cutAfter]
        hitsAfterCut = ak.where(goodEvent&panelVeto, ak.count(nPEBeforeCut, axis=1, keepdims=True), -1)
        self.events[cutName+'NPEAfter']  = nPEAfterCut
        self.events[cutName+'HitsAfter'] = hitsAfterCut
        self.events[cutName+'AreaAfter'] = areaAfterCut

        self.events[cutName] = panelVeto

        if cut:
            self.cutBranches(branches, cutName)
    
    #creates mask/cut vetoing any event with front/back panel hit w/ nPE > nPECut
    @mqCut
    def beamMuonPanelVeto(self, cutName='beamMuonPanelVeto', cut=False, nPECut=100, invert=False, branches=None):
        
        passNPECut = self.events['nPE'] > nPECut
        panelCut = self.events['type'] == 1

        finalCut = passNPECut & panelCut
        finalCut = ak.any(finalCut, axis=1)
        if not invert:
            finalCut = ~finalCut

        finalCut = ak.fill_none(finalCut, False)
        testIndex = ak.where(ak.num(self.events['nPE'][(self.events['layer'] == -1) & panelCut], axis=1) > 0)

        _, finalCut = ak.broadcast_arrays(self.events.npulses, finalCut)
        self.events[cutName] = finalCut

        self.events['frontPanelNPEBefore'] = self.events['nPE'][(self.events['layer'] == -1) & panelCut]
        self.events['backPanelNPEBefore'] = self.events['nPE'][(self.events['layer'] == 4) & panelCut]
        self.events['frontPanelNPEAfter'] = self.events['nPE'][(self.events['layer'] == -1) & panelCut & finalCut]
        self.events['backPanelNPEAfter'] = self.events['nPE'][(self.events['layer'] == 4) & panelCut & finalCut]
        self.events['maxPanelNPE'] = ak.max(self.events['nPE'][panelCut], axis=1)
        
        if cut:
            self.cutBranches(branches, cutName)

    #requirement to have at least one front/back panel hit in an event
    @mqCut
    def requireFrontBackPanel(self, cutName='frontBackPanelRequired', cut=False, branches=None):

        panelCut = ak.any(self.events['type'] == 1, axis=1)
        _, panelCut = ak.broadcast_arrays(self.events['npulses'], panelCut)

        self.events['frontBackPanelRequired'] = panelCut

        if cut:
            self.cutBranches(branches, cutName)

    @mqCut
    def panelInfo(self, cutName='panelInfo'):

        num_panels = ak.count(self.events['type'][self.events['type']==1], axis=1)

        #for events with no passing pulses set the number of panels to -1 (technically also zero but want to separate passing events)
        num_panels = ak.where(ak.count(self.events['type'], axis=1) == 0, -1, num_panels)

        frontNPE = self.events['nPE'][(self.events['type']==1) & (self.events['layer']==-1)]
        backNPE = self.events['nPE'][(self.events['type']==1) & (self.events['layer']==4)]

        frontNPE = ak.fill_none(ak.pad_none(frontNPE, 1), -1)
        backNPE = ak.fill_none(ak.pad_none(backNPE, 1), -1)

        self.events['nPanels'] = num_panels
        self.events['frontNPE'] = frontNPE
        self.events['backNPE'] = backNPE

        barEnergy = self.events['energyCal'][(self.events['type'] == 0)]
        barNPE = self.events['nPE'][(self.events['type'] == 0)]

        self.events['barEnergy'] = barEnergy
        self.events['barNPE'] =barNPE

    ######################################
    ## Geometric Selections
    #######################################

    #selection events that have hits in a straight path
    #option allowedMove will select events that only move one bar horizontally/vertically
    #option limitPaths requires only one straight line path through detector
    @mqCut
    def straightLineCut(self, cutName='straightLineCut', allowedMove=False, limitPaths=False, allowPanels=False, innerBars=False, outerBars=False, cut=False, cutPulse=False, branches=None):
        
        #allowed combinations of moving
        combos = []
        straight_cuts = []

        for i, x in enumerate(range(4)):
            for j, y in enumerate(range(4)):
                if innerBars and (i==0 or i==3 or j==0 or j==3): 
                    straight_cuts.append(ak.any(self.events['type']==100, axis=1)) #fill with false values
                    continue
                if outerBars and (i==1 or i==2 or j==1 or j==2): 
                    straight_cuts.append(ak.any(self.events['type']==100, axis=1)) #fill with false values
                    continue
                rowCut = (self.events['row'] == y) & (self.events['type']==0)
                colCut = (self.events['column'] == x) & (self.events['type']==0)

                r_tmp0 = (rowCut[self.events['layer']==0] & colCut[self.events['layer']==0])
                r_tmp1 = (rowCut[self.events['layer']==1] & colCut[self.events['layer']==1])
                r_tmp2 = (rowCut[self.events['layer']==2] & colCut[self.events['layer']==2])
                r_tmp3 = (rowCut[self.events['layer']==3] & colCut[self.events['layer']==3])


                row_pass = ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(r_tmp3, axis=1)

                if allowedMove:

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
                        straight_cuts.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(m3_c1_r0, axis=1)) #layer3 col decrease
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(m2_c1_r0, axis=1) & ak.any(m3_c1_r0, axis=1)) #layer2 col decrease
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(m1_c1_r0, axis=1) & ak.any(m2_c1_r0, axis=1) & ak.any(m3_c1_r0, axis=1)) #layer1 col decrease
                    if(y > 0):
                        straight_cuts.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(m3_c0_r1, axis=1)) #layer3 row decrease
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(m2_c0_r1, axis=1) & ak.any(m3_c0_r1, axis=1)) #layer2 row decrease
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(m1_c0_r1, axis=1) & ak.any(m2_c0_r1, axis=1) & ak.any(m3_c0_r1, axis=1)) #layer1 row decrease
                    if(x < 4):
                        straight_cuts.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(p3_c1_r0, axis=1)) #layer3 col increase
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(p2_c1_r0, axis=1) & ak.any(p3_c1_r0, axis=1)) #layer2 col increase
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(p1_c1_r0, axis=1) & ak.any(p2_c1_r0, axis=1) & ak.any(p3_c1_r0, axis=1)) #layer1 col increase
                    if(y < 4):
                        straight_cuts.append(ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(p3_c0_r1, axis=1)) #layer3 row increase
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(p2_c0_r1, axis=1) & ak.any(p3_c0_r1, axis=1)) #layer2 row increase
                        straight_cuts.append( ak.any(r_tmp0, axis=1) & ak.any(p1_c0_r1, axis=1) & ak.any(p2_c0_r1, axis=1) & ak.any(p3_c0_r1, axis=1)) #layer1 row increase

                    #straight_cuts.extend(combos)

                straight_cuts.append(row_pass)
        
        for ipath, path in enumerate(straight_cuts):
            if ipath == 0: straight_path = path
            else: straight_path = straight_path | path

        self.events[cutName+'Plot'] = straight_path

        _, straight_path = ak.broadcast_arrays(self.events['npulses'], straight_path)
        self.events[cutName] = straight_path

        remaining = ak.sum(self.events['fileNumber'], axis=1) >= 1
        self.events[cutName+'New'] = remaining
        self.events[cutName+'NewInvert'] = ~remaining

        for x in range(4):
            for y in range(4):
                _, this_straightCut = ak.broadcast_arrays(self.events['npulses'], straight_cuts[4*x+y])
                if(x == 0 and y == 0): straight_pulse = (this_straightCut) & (self.events['column'] == x) & (self.events['row'] == y) & (self.events['type'] == 0)
                else: straight_pulse = (straight_pulse) | ((this_straightCut) & (self.events['column'] == x) & (self.events['row'] == y) & (self.events['type'] == 0))


        self.events['numStraightPaths'] = ak.sum(straight_pulse, axis=1) / 4

        if allowPanels:
            straight_pulse = straight_pulse | (self.events['type']>0)

        if limitPaths:
            maskMultiple = self.events['numStraightPaths'] == 1
            _, maskMultiple = ak.broadcast_arrays(straight_pulse, maskMultiple)
            straight_pulse = straight_pulse[maskMultiple] #ak.mask(straight_pulse, maskMultiple)

        self.events[cutName+'Pulse'] = straight_pulse
        #print("straight pulses", straight_pulse[ak.where(ak.any(straight_pulse, axis=1))])

        #get self.events passing 1 bar allowedMove
        if allowedMove:
            for ipath, path in enumerate(combos):
                if ipath == 0: passing = path
                else: passing = passing | path

            self.events['moveOnePath'] = passing


        if cut:
            self.cutBranches(branches, cutName)
        elif cutPulse:
            self.cutBranches(branches, cutName+'Pulse')

    #modified version of straight line cut to allow any straight line path
    #allowed move=True will allow any straight line path through the detector
    @mqCut
    def straightLineCutMod(self, cutName='straightLineCutMod', timeCut=None, restrictPaths=True, allowedMove=False, cut=False, branches=None):

        #combos = ak.argcombinations(self.events['layer'], 4)
        
        newMask = self.events['layer'] == 100 #create false array intentionally
        allIndices = ak.Array([np.arange(len(x)) for x in newMask])

        layer0 = (self.events['layer'] == 0) & (self.events['type']==0)
        layer1 = (self.events['layer'] == 1) & (self.events['type']==0)
        layer2 = (self.events['layer'] == 2) & (self.events['type']==0)
        layer3 = (self.events['layer'] == 3) & (self.events['type']==0)

        ilayer0 = allIndices[layer0]
        ilayer1 = allIndices[layer1]
        ilayer2 = allIndices[layer2]
        ilayer3 = allIndices[layer3]

        #print(ak.to_list(ilayer0), ak.to_list(ilayer1), ak.to_list(ilayer2), ak.to_list(ilayer3))

        combos = ak.cartesian([ilayer0, ilayer1, ilayer2, ilayer3])

        #print(ak.to_list(combos))

        '''for i in range(4):
            this_layer = (self.events['layer'][combos['0']] == i) | \
                        (self.events['layer'][combos['1']] == i) | \
                        (self.events['layer'][combos['2']] == i) | \
                        (self.events['layer'][combos['3']] == i) 
            if i == 0:
                layer_req = this_layer
            else:
                layer_req = layer_req & this_layer

        type_req = (self.events['type'][combos['0']] == 0) & \
                    (self.events['type'][combos['1']] == 0) & \
                    (self.events['type'][combos['2']] == 0) & \
                    (self.events['type'][combos['3']] == 0)

        
        row01 = abs(self.events['row'][combos['0']] - self.events['row'][combos['1']]) <= allowedMove
        row02 = abs(self.events['row'][combos['0']] - self.events['row'][combos['2']]) <= allowedMove
        row03 = abs(self.events['row'][combos['0']] - self.events['row'][combos['3']]) <= allowedMove
        row12 = abs(self.events['row'][combos['1']] - self.events['row'][combos['2']]) <= allowedMove
        row13 = abs(self.events['row'][combos['1']] - self.events['row'][combos['3']]) <= allowedMove
        row23 = abs(self.events['row'][combos['2']] - self.events['row'][combos['3']]) <= allowedMove

        row_req = (ak.values_astype(row01, np.int32) + \
                ak.values_astype(row02, np.int32) + \
                ak.values_astype(row03, np.int32) + \
                ak.values_astype(row12, np.int32) + \
                ak.values_astype(row13, np.int32) + \
                ak.values_astype(row23, np.int32)) >= 4

        col01 = abs(self.events['column'][combos['0']] - self.events['column'][combos['1']]) <= allowedMove
        col02 = abs(self.events['column'][combos['0']] - self.events['column'][combos['2']]) <= allowedMove
        col03 = abs(self.events['column'][combos['0']] - self.events['column'][combos['3']]) <= allowedMove
        col12 = abs(self.events['column'][combos['1']] - self.events['column'][combos['2']]) <= allowedMove
        col13 = abs(self.events['column'][combos['1']] - self.events['column'][combos['3']]) <= allowedMove
        col23 = abs(self.events['column'][combos['2']] - self.events['column'][combos['3']]) <= allowedMove

        col_req = (ak.values_astype(col01, np.int32) + \
                   ak.values_astype(col02, np.int32) + \
                   ak.values_astype(col03, np.int32) + \
                   ak.values_astype(col12, np.int32) + \
                   ak.values_astype(col13, np.int32) + \
                   ak.values_astype(col23, np.int32)) >= 4'''

        row01 = self.events['row'][combos['1']] - self.events['row'][combos['0']]
        row12 = self.events['row'][combos['2']] - self.events['row'][combos['1']]
        row23 = self.events['row'][combos['3']] - self.events['row'][combos['2']]


        passRow = (abs(row01) > allowedMove) | (abs(row12) > allowedMove) | (abs(row23) > allowedMove)
        if restrictPaths:
            passRow = passRow | ((row12!=0) & (row01!=0) & (row12 != row01))
            passRow = passRow | ((row01!=0) & (row23 != row01))
            passRow = passRow | ((row12!=0) & (row23!=row12))
        passRow = ~passRow

        col01 = self.events['column'][combos['1']] - self.events['column'][combos['0']]
        col12 = self.events['column'][combos['2']] - self.events['column'][combos['1']]
        col23 = self.events['column'][combos['3']] - self.events['column'][combos['2']]

        passCol = (abs(col01) > allowedMove) | (abs(col12) > allowedMove) | (abs(col23) > allowedMove)
        if restrictPaths:
            passCol = passCol | ((col12!=0) & (col01!=0) & (col12 != col01))
            passCol = passCol | ((col01!=0) & (col23 != col01))
            passCol = passCol | ((col12!=0) & (col23 != col12))
        passCol = ~passCol

        if timeCut is not None:
            passTime = abs((self.events['timeFit_module_calibrated'][combos['3']] - self.events['timeFit_module_calibrated'][combos['0']])) < timeCut
            straightTest = passCol & passRow & passTime
        else:
            straightTest = passCol & passRow

        straightTestAny = ak.any(straightTest, axis=1)

        _, straightTestAny = ak.broadcast_arrays(self.events['npulses'], straightTestAny)

        passingCombos = combos[straightTest]
        
        newCombos = ak.concatenate([passingCombos['0'], passingCombos['1'], passingCombos['2'], passingCombos['3']], axis=1)

        newMask = self.events['layer'] == 100 #create false array intentionally

        indices = ak.Array([np.arange(len(x)) for x in newMask])
        newMask = ak.Array([np.isin(x, newCombos[i]) for i, x in enumerate(indices)])

        self.events[cutName+'Pulse'] = newMask

        if cut:
            self.cutBranches(branches, cutName+'Pulse')        

    #modified version of straight line cut to allow any straight line path
    #allowed move=True will allow any straight line path through the detector
    @mqCut
    def straightLineCutModWiggle(self, cutName='straightLineCutModWiggle', timeCut=None, allowedMove=False, cut=False, branches=None):
        
        combos = ak.argcombinations(self.events['row'], 4)

        for i in range(4):
            this_layer = (self.events['layer'][combos['0']] == i) | \
                        (self.events['layer'][combos['1']] == i) | \
                        (self.events['layer'][combos['2']] == i) | \
                        (self.events['layer'][combos['3']] == i) 
            if i == 0:
                layer_req = this_layer
            else:
                layer_req = layer_req & this_layer

        
        row01 = abs(self.events['row'][combos['0']] - self.events['row'][combos['1']]) <= allowedMove
        row02 = abs(self.events['row'][combos['0']] - self.events['row'][combos['2']]) <= allowedMove
        row03 = abs(self.events['row'][combos['0']] - self.events['row'][combos['3']]) <= allowedMove
        row12 = abs(self.events['row'][combos['1']] - self.events['row'][combos['2']]) <= allowedMove
        row13 = abs(self.events['row'][combos['1']] - self.events['row'][combos['3']]) <= allowedMove
        row23 = abs(self.events['row'][combos['2']] - self.events['row'][combos['3']]) <= allowedMove

        row_req = (ak.values_astype(row01, np.int32) + \
                ak.values_astype(row02, np.int32) + \
                ak.values_astype(row03, np.int32) + \
                ak.values_astype(row12, np.int32) + \
                ak.values_astype(row13, np.int32) + \
                ak.values_astype(row23, np.int32)) >= 4

        col01 = abs(self.events['column'][combos['0']] - self.events['column'][combos['1']]) <= allowedMove
        col02 = abs(self.events['column'][combos['0']] - self.events['column'][combos['2']]) <= allowedMove
        col03 = abs(self.events['column'][combos['0']] - self.events['column'][combos['3']]) <= allowedMove
        col12 = abs(self.events['column'][combos['1']] - self.events['column'][combos['2']]) <= allowedMove
        col13 = abs(self.events['column'][combos['1']] - self.events['column'][combos['3']]) <= allowedMove
        col23 = abs(self.events['column'][combos['2']] - self.events['column'][combos['3']]) <= allowedMove

        col_req = (ak.values_astype(col01, np.int32) + \
                   ak.values_astype(col02, np.int32) + \
                   ak.values_astype(col03, np.int32) + \
                   ak.values_astype(col12, np.int32) + \
                   ak.values_astype(col13, np.int32) + \
                   ak.values_astype(col23, np.int32)) >= 4
            

        straightTest = layer_req & col_req & row_req

        straightTestAny = ak.any(straightTest, axis=1)

        _, straightTestAny = ak.broadcast_arrays(self.events['npulses'], straightTestAny)

        passingCombos = combos[straightTest]
        
        newCombos = ak.concatenate([passingCombos['0'], passingCombos['1'], passingCombos['2'], passingCombos['3']], axis=1)

        newMask = self.events['layer'] == 100 #create false array intentionally

        indices = ak.Array([np.arange(len(x)) for x in newMask])
        newMask = ak.Array([np.isin(x, newCombos[i]) for i, x in enumerate(indices)])

        self.events[cutName+'Pulse'] = newMask

        if cut:
            self.cutBranches(branches, cutName+'Pulse') 


    #select self.events that have 3 area saturating pulses in a line
    @mqCut
    def threeAreaSaturatedInLine(self, areaCut=50000, branches=None):
        #make sure 3 layers have saturating hits
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= areaCut) & (self.events.straightLineCutPulse)]
        
        self.events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
        self.events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))
        
    #select self.events that have 3 height saturating pulses in a line
    @mqCut
    def threeHeightSaturatedInLine(self, heightCut=50000, branches=None):
        #make sure 3 layers have saturating hits
        sat_0 = self.events.area[(self.events.eventCuts) & (self.events.layer0) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        sat_1 = self.events.area[(self.events.eventCuts) & (self.events.layer1) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        sat_2 = self.events.area[(self.events.eventCuts) & (self.events.layer2) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        sat_3 = self.events.area[(self.events.eventCuts) & (self.events.layer3) & (self.events.area >= heightCut) & (self.events.straightLineCutPulse)]
        
        self.events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
        self.events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))

    #creates cut/mask on 3 pulses in a line
    @mqCut
    def threeInLine(self, cutName='threeInLine', cut=False, pulseCut=False, branches=None):
        npeCut = 0

        for path in range(16):

            row = path//4
            col = path%4

            outputName = 'threeHitPath{}'.format(path)

            layer0 = (self.events.layer == 0) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
            layer1 = (self.events.layer == 1) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
            layer2 = (self.events.layer == 2) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)
            layer3 = (self.events.layer == 3) & (self.events.nPE >= npeCut) & (self.events.row == row) & (self.events.column == col)

            threeStraight_f0 = ak.any(layer1, axis=1) & ak.any(layer2, axis=1) & ak.any(layer3, axis=1)
            threeStraight_f1 = ak.any(layer0, axis=1) & ak.any(layer2, axis=1) & ak.any(layer3, axis=1)
            threeStraight_f2 = ak.any(layer0, axis=1) & ak.any(layer1, axis=1) & ak.any(layer3, axis=1)
            threeStraight_f3 = ak.any(layer0, axis=1) & ak.any(layer1, axis=1) & ak.any(layer2, axis=1)

            #array for each "free" layer without required hit
            self.events[outputName+'_f0'] = threeStraight_f0
            self.events[outputName+'_f1'] = threeStraight_f1
            self.events[outputName+'_f2'] = threeStraight_f2
            self.events[outputName+'_f3'] = threeStraight_f3

            #get just the pulses that pass that made the selections
            _, b0 = ak.broadcast_arrays(self.events.nPE, threeStraight_f0)
            _, b1 = ak.broadcast_arrays(self.events.nPE, threeStraight_f1)
            _, b2 = ak.broadcast_arrays(self.events.nPE, threeStraight_f2)
            _, b3 = ak.broadcast_arrays(self.events.nPE, threeStraight_f3)

            #pulses in the "not free" layers
            self.events[outputName+'_p0'] = (b0) & ((layer1) | (layer2) | (layer3))
            self.events[outputName+'_p1'] = (b1) & ((layer0) | (layer2) | (layer3))
            self.events[outputName+'_p2'] = (b2) & ((layer0) | (layer1) | (layer3))
            self.events[outputName+'_p3'] = (b3) & ((layer0) | (layer1) | (layer2))

            #pulses in the free layer
            self.events[outputName+'_s0'] = (threeStraight_f0) & (self.events.layer == 0) & (self.events.nPE >= npeCut)
            self.events[outputName+'_s1'] = (threeStraight_f1) & (self.events.layer == 1) & (self.events.nPE >= npeCut)
            self.events[outputName+'_s2'] = (threeStraight_f2) & (self.events.layer == 2) & (self.events.nPE >= npeCut)
            self.events[outputName+'_s3'] = (threeStraight_f3) & (self.events.layer == 3) & (self.events.nPE >= npeCut)

            allPulses = (self.events[outputName+'_p0'] | self.events[outputName+'_p1'] | self.events[outputName+'_p2'] | self.events[outputName+'_p3'])

            if path == 0:
                allPaths = allPulses
            else:
                allPaths = allPaths | allPulses
        
        self.events[cutName+'Pulses'] = allPaths
        
        if pulseCut:
            self.events['threeHitPath_allPulses'] = allPaths
        else:
            _, mask = ak.broadcast_arrays(self.events['npulses'], ak.any(allPaths, axis=1))
            self.events['threeHitPath_allPulses'] = mask

        if cut:
            self.cutBranches(branches, 'threeHitPath_allPulses')


    #this cut selects out the central 4 bars in each layer only
    @mqCut
    def centralQuad(self, cutName='centralQuad', cut=False, branches=None):

        cutRow = (self.events['row'] == 1) | (self.events['row'] == 2)
        cutCol = (self.events['column'] == 1) | (self.events['column'] == 2)
        cutCombined = cutRow & cutCol

        cutCentral = ak.where(self.events['type']==0, cutCombined, True)

        self.events[cutName] = cutCentral

        if cut:
            self.cutBranches(branches, cutName)

    ##################################
    ## Pulse Timing Cuts
    ##################################xf

    #cut gets max time difference between pulses if there are 4 pulses in an event
    @mqCut
    def getPulseTimeDiff(self, branches=None):
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

    #creates mask/cut to check if pulse is in trigger window
    @mqCut
    def centralTime(self, cutName='centralTime', cut=False, branches=None):
        events = self.events
        timeCut = (events['timeFit_module_calibrated'] > 1100) & (events['timeFit_module_calibrated'] < 1400)
        drop_empty = ak.num(timeCut) > 0
        newEvents = drop_empty & timeCut

        self.events[cutName] = newEvents

        if cut:
            self.cutBranches(branches, cutName)    

    #creates cut/mask on first pulse in channel for event
    @mqCut
    def firstPulseCut(self, cutName='firstPulse', cut=False, branches=None):

        self.events[cutName] = self.events.ipulse == 0

        if cut:
            self.cutBranches(branches, cutName)

    #creates cut/mask selecting only pulses where first pulse is max pulse in event (per channel)
    @mqCut
    def firstPulseMax(self, cutName='firstPulseMax', cut=False, branches=None):

        for i in range(80):
            channelCut = self.events.chan == i
            channelNPE = self.events.nPE[channelCut]
            maxIndex = ak.argmax(channelNPE, axis=1, keepdims=True)
            ipulseCut = self.events.ipulse[maxIndex] == 0
            ipulseCut = ak.fill_none(ipulseCut, True, axis=1)
            if i ==0:
                firstPulseMax = ipulseCut
            else:
                firstPulseMax = firstPulseMax & ipulseCut

        _, firstPulseMax = ak.broadcast_arrays(self.events.npulses, ak.flatten(firstPulseMax, axis=1))
        
        self.events[cutName] = firstPulseMax
        if cut:
            self.cutBranches(branches, cutName)

    #creates mask/cut vetoing any event with a pulse occuring < timeCut
    @mqCut
    def vetoEarlyPulse(self, cutName="vetoEarlyPulse", timeCut=700, cut=False, branches=None):
        earlyPulse = ak.min(self.events['timeFit_module_calibrated'], axis=1) < timeCut
        earlyPulse = ak.fill_none(earlyPulse, False)
        _, earlyPulse = ak.broadcast_arrays(self.events.npulses, ~earlyPulse)
        self.events[cutName] = earlyPulse
        if cut:
            self.cutBranches(branches, cutName)

    #creates mask/cut vetoing any event with min/max pulse time difference < timeCut
    @mqCut
    def timeMaxMin(self, cutName='timeMaxMin', timeCut=40, straight=True, cut=False, branches=None):

        timesMask = (self.events['type']==0)

        times = self.events['timeFit_module_calibrated'][timesMask]
        if straight:
            timesMask = self.events['straightLineCutPulse']
            times = ak.where(ak.any(self.events['straightLineCutPulse'], axis=1), 
                             self.events['timeFit_module_calibrated'][self.events['straightLineCutPulse']], 
                             self.events['timeFit_module_calibrated'][timesMask])
        
        maxTime = ak.max(times, axis=1, keepdims=True)
        minTime = ak.min(times, axis=1, keepdims=True)

        self.events['minTimeBefore'] = minTime
        self.events['maxTimeBefore'] = maxTime

        timeDiff = maxTime - minTime
        timeCut = timeDiff < timeCut

        timeCut = ak.fill_none(timeCut, False)

        _, timeCutMod = ak.broadcast_arrays(maxTime, timeCut)
        self.events['minTimeAfter'] = minTime[timeCutMod] 
        self.events['maxTimeAfter'] = maxTime[timeCutMod]

        _, timeCut = ak.broadcast_arrays(self.events.npulses, timeCut)

        self.events[cutName] = timeCut
        self.events[cutName+'Diff'] = timeDiff

        timeDiffStraight = ak.mask(timeDiff, ak.firsts(self.events['straightLineCut'], axis=1))
        timeDiffNotStraight = ak.mask(timeDiff, ak.firsts(~self.events['straightLineCut'], axis=1))

        self.events[cutName+'DiffStraight'] = timeDiffStraight
        self.events[cutName+'DiffNotStraight'] = timeDiffNotStraight

        

        if cut:
            self.cutBranches(branches, cutName)

    #calculates time difference between bar hits in layers 0/3
    @mqCut
    def timeDiff(self, cutName='timeDiff', branches=None):

        times0 = self.events['timeFit_module_calibrated'][(self.events['layer']==0) & (self.events['type']==0)]
        times3 = self.events['timeFit_module_calibrated'][(self.events['layer']==3) & (self.events['type']==0)]

        combos = ak.cartesian([times0, times3], axis=1)

        diff = combos['1'] - combos['0']

        self.events[cutName] = diff

    ##############################
    ## Other
    ##############################
    
    #creates mask/cut vetoing any event where the min/max nPE ratio < nPECut
    @mqCut
    def nPEMaxMin(self, cutName='nPEMaxMin', cut=False, nPERatioCut = 10, straight=False, branches=None):
        
        if straight:
            maxNPE = ak.max(self.events['nPE'][self.events['straightLineMaxMinPulse']], axis=1, keepdims=True)
            minNPE = ak.min(self.events['nPE'][self.events['straightLineMaxMinPulse']], axis=1, keepdims=True)            
        else:
            maxNPE = ak.max(self.events['nPE'][self.events['type']==0], axis=1, keepdims=True)
            minNPE = ak.min(self.events['nPE'][self.events['type']==0], axis=1, keepdims=True)

        self.events['maxNPEBefore'] = maxNPE
        self.events['minNPEBefore'] = minNPE

        nPERatio = maxNPE/minNPE
        nPECut = nPERatio < nPERatioCut

        nPECut = ak.fill_none(nPECut, False)

        _, nPECutMod = ak.broadcast_arrays(maxNPE, nPECut)
        self.events['maxNPEAfter'] = maxNPE[nPECutMod] 
        self.events['minNPEAfter'] = minNPE[nPECutMod]
        self.events['nPERatio'] = nPERatio

        _, nPECut = ak.broadcast_arrays(self.events.npulses, nPECut)

        self.events[cutName] = nPECut
        if cut:
            self.cutBranches(branches, cutName)

    #creates mask/cut vetoing any event where the min/max nPE ratio < nPECut
    @mqCut
    def energyMaxMin(self, cutName='energyMaxMin', cut=False, energyRatioCut = 10, straight=False, branches=None):
        
        if straight:
            maxEnergy = ak.max(self.events['energyCal'][self.events['straightLineMaxMinPulse']], axis=1, keepdims=True)
            minEnergy = ak.min(self.events['energyCal'][self.events['straightLineMaxMinPulse']], axis=1, keepdims=True)            
        else:
            maxEnergy = ak.max(self.events['energyCal'][self.events['type']==0], axis=1, keepdims=True)
            minEnergy = ak.min(self.events['energyCal'][self.events['type']==0], axis=1, keepdims=True)

        #print(len(self.events['energyCal'][0]), len(self.events['area'][0]))
        self.events['maxEnergyBefore'] = maxEnergy
        self.events['minEnergyBefore'] = minEnergy

        energyRatio = maxEnergy/minEnergy
        energyCut = energyRatio < energyRatioCut

        #print(maxEnergy, minEnergy, energyRatio)

        energyCut = ak.fill_none(energyCut, False)

        _, energyCutMod = ak.broadcast_arrays(maxEnergy, energyCut)
        self.events['maxEnergyAfter'] = maxEnergy[energyCutMod] 
        self.events['minEnergyAfter'] = minEnergy[energyCutMod]
        self.events['energyRatio'] = energyRatio

        _, energyCut = ak.broadcast_arrays(self.events.npulses, energyCut)

        self.events[cutName] = energyCut
        if cut:
            self.cutBranches(branches, cutName)

    #cuts on std dev between max/min nPE pulses
    @mqCut
    def nPEStdDev(self, cutName='nPEStdDev', cut=False, std=5, branches=None):

        maxNPE = ak.max(self.events['nPE'][self.events['type']==0], axis=1, keepdims=True)
        minNPE = ak.min(self.events['nPE'][self.events['type']==0], axis=1, keepdims=True)
        
        self.events['maxNPEBefore'] = maxNPE
        self.events['minNPEBefore'] = minNPE

        nPEStdDev = np.sqrt(minNPE)
        nPEDiff = maxNPE - minNPE
        nPEMaxMinStd = nPEDiff / nPEStdDev

        nPECut = nPEMaxMinStd <= std

        nPECut = ak.fill_none(nPECut, False)

        _, nPECutMod = ak.broadcast_arrays(maxNPE, nPECut)
        self.events['maxNPEAfter'] = maxNPE[nPECutMod] 
        self.events['minNPEAfter'] = minNPE[nPECutMod]
        self.events['nPEStd'] = nPEMaxMinStd

        _, nPECut = ak.broadcast_arrays(self.events.npulses, nPECut)

        self.events[cutName] = nPECut
        if cut:
            self.cutBranches(branches, cutName)


    #prints out the run/file/event number of passing pulses
    @mqCut
    def printEvents(self):
        runs = ak.drop_none(ak.firsts(self.events['runNumber']))
        files = ak.drop_none(ak.firsts(self.events['fileNumber']))
        events = ak.drop_none(ak.firsts(self.events['event']))
        chans = ak.drop_none(ak.flatten(self.events['chan']))
        nPE = ak.drop_none(ak.flatten(self.events['nPE']))
        for i, (run, file, event) in enumerate(zip(runs, files, events)):
            print(f'{i}: run: {run}, file: {file}, event: {event}, channels: {chans}, nPE: {nPE}')        

    @mqCut
    def applyNPEScaling(self, cutName='nPEScaling', sim=False):

        if sim:
            #chan_calibrations = ak.full_like(self.events['area'], 4395.33) #older version
            chan_calibrations = ak.full_like(self.events['area'], 3336.77)

        else:
            extra_configs = ['configRun1173_1295.json', 'configRun1115_1172.json', 'configRun1097_1114.json', 'configRun1059_1096.json', 'configRun987_1058.json']
        
            with open(os.path.dirname(__file__)+f'{self.configDir}/barConfigs/configRun1296_present.json', 'r') as f_cal:
                calibrations = json.load(f_cal)['speAreas']
                _, calibrations = ak.broadcast_arrays(self.events['sidebandRMS'], ak.Array([calibrations]))

            chan_calibrations = calibrations[self.events['chan']]

            for config in extra_configs:
                with open(os.path.dirname(__file__)+f'{self.configDir}/barConfigs/{config}', 'r') as f_cal:
                    extra_cal = json.load(f_cal)['speAreas']
                    _, extra_cal = ak.broadcast_arrays(self.events['sidebandRMS'], ak.Array([extra_cal]))   

                    runs = config.split('_')
                    run_low = int(runs[0].replace('configRun', ''))
                    run_high = int(runs[1].split('.')[0])

                    extra_chanCalibrations = extra_cal[self.events['chan']]
                    
                    mask = (self.events['runNumber'] <= run_high) & (self.events['runNumber'] >= run_low)
                    chan_calibrations = ak.where(mask, extra_chanCalibrations, chan_calibrations)

        areas = self.events['area']
        npe = areas / chan_calibrations

        self.events['nPE'] = npe

    @mqCut
    def applyEnergyScaling(self, cutName='energyScaling', sim=False):

        extra_configs = ['configRun1173_1295.json', 'configRun1115_1172.json', 'configRun1097_1114.json', 'configRun1059_1096.json', 'configRun987_1058.json']
    
        with open(os.path.dirname(__file__)+f'{self.configDir}/barConfigs/configRun1296_present.json', 'r') as f_cal:
            calibrations = json.load(f_cal)['sourceNPE']
            _, calibrations = ak.broadcast_arrays(self.events['sidebandRMS'], ak.Array([calibrations]))

        chan_calibrations = calibrations[self.events['chan']]
        npe = self.events['nPE']

        if not sim:
            for config in extra_configs:
                with open(os.path.dirname(__file__)+f'{self.configDir}/barConfigs/{config}', 'r') as f_cal:
                    extra_cal = json.load(f_cal)['sourceNPE']
                    _, extra_cal = ak.broadcast_arrays(self.events['sidebandRMS'], ak.Array([extra_cal]))   

                    runs = config.split('_')
                    run_low = int(runs[0].replace('configRun', ''))
                    run_high = int(runs[1].split('.')[0])

                    extra_chanCalibrations = extra_cal[self.events['chan']]
                    
                    mask = (self.events['runNumber'] <= run_high) & (self.events['runNumber'] >= run_low)
                    chan_calibrations = ak.where(mask, extra_chanCalibrations, chan_calibrations)

        
        else:
            with open(os.path.dirname(__file__)+f'{self.configDir}/barConfigs/simConfig.json', 'r') as f_cal:
                calibrations = json.load(f_cal)['sourceNPE']
                _, calibrations = ak.broadcast_arrays(self.events['sidebandRMS'], ak.Array([calibrations]))

            chan_calibrations = calibrations[self.events['chan']]

        energyCal = (npe / chan_calibrations) * 22.1

        self.events['energyCal'] = energyCal

        if 'energyCal' not in self.branches:
            self.branches.append('energyCal')



