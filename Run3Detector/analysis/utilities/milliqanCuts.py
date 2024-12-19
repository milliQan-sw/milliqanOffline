#!/usr/bin/python3

import awkward as ak
import numpy as np
import functools
import inspect
import itertools

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

    #method to keep count of events/pulses passing all cuts
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

    #print out all of the cutflows
    def getCutflowCounts(self):
        # Prints the value after each batch of events
        print("----------------------------------Cutflow Table----------------------------------------------------------------------------------")
        print ("{:<25} {:<20} {:<25} {:<20} {:<25} {:<30}".format('Cut', 'N Passing Events', 'Cum Event Eff % (Prev)', 'N Passing Pulses', 'Cum Pulse Eff % (Prev)', 'Cut Applied'))
        print('---------------------------------------------------------------------------------------------------------------------------------')
        prevEvents = -1
        prevPulses = -1
        totalEvents = -1
        totalPulses = -1
        for ival, (key, value) in enumerate(self.cutflow.items()):
            #print(i, len(self.cutflow))
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

            realCut = 'True' if value['cut'] else 'False'
            print("{:<25} {:<20} {:<25} {:<20} {:<25} {:<30}".format(key, value['events'], allEvt, value['pulses'], allPulse, realCut))
            prevEvents = value['events']
            prevPulses = value['pulses']
        print("--------------------------------------------------------------------------------------------------------------------------------")
        # Resets the counter at the end of the cutflow
        self.counter=0

    #method to apply cut to a function, used by the decorator
    def cutBranches(self, branches, cutName):

        perChanBranches = ['sidebandRMS']

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

    #counts the number of events with pulses
    @mqCut
    def fullEventCounter(self, cutName=None, cut=False, branches=None):
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

    #creates branch with mask for first event
    @mqCut
    def firstEvent(self, branches=None):
        events = ak.firsts(self.events['event'])
        mask = np.zeros(len(events), dtype=bool)
        mask[0] = True
        mask = ak.Array(mask)
        self.events['firsts'] = mask

    #########################################
    ## Quality Cuts
    #########################################

    #cuts on pickup flag
    @mqCut
    def pickupCut(self, cutName='pickupCut', cut=False, tight=False, branches=None):
        #need to define another cut so that the branch doesn't get cut first, alternatively can ensure it is last in the branches list
        if tight: mycut = ~self.events.pickupFlagTight
        else: mycut = ~self.events.pickupFlag
        self.events[cutName] = mycut

        if cut:
            self.cutBranches(branches, cutName)

    #cuts on DAQ board matching
    @mqCut
    def boardsMatched(self, cutName='boardsMatched', cut=False, branches=None):
        _, self.events['boardsMatched'] = ak.broadcast_arrays(self.events.pickupFlag, self.events.boardsMatched)
        
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
            self.cutBranches(branches, cutName)
    
    #event level mask selecting  cosmic throught going events with hits at the top cosmic panel at all layers
    @mqCut
    def CosmicTG(self, cutName='CosmicTG', cut=False, branches=None , nPECutpan = 2):
        cospanel = ak.any((self.events.row==4) & (self.events.nPE >= nPECutpan ), axis=1)
        allLayers =(ak.any(self.events.layer==0, axis=1) & 
                    ak.any(self.events.layer==1, axis=1) & 
                    ak.any(self.events.layer==2, axis=1) & 
                    ak.any(self.events.layer==3, axis=1))

        self.events[cutName] = allLayers & cospanel
        if cut:
            self.cutBranches(branches, cutName)

    #cut on one hit per layer, if multipleHits==False cuts on exactly one hit per layer
    @mqCut
    def oneHitPerLayerCut(self, cutName='oneHitPerLayerCut', cut=False, multipleHits=False, branches=None):

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
        self.events[cutName] = nLayers
        if cutName not in self.branches:
            self.branches.append(cutName)

        if cut:
            self.cutBranches(branches, cutName+'Cut')

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

    #########################################
    ## Cuts on Per Channel
    #########################################

    #creates branch with number of bars in event
    @mqCut
    def countNBars(self, cutName='countNBars',pulseBase = True):
        barsCut = (self.events['type']==0)
        uniqueBars = ak.Array([np.unique(x) for x in self.events.chan[barsCut]])
        nBars = ak.count(uniqueBars, axis=1)
        if pulseBase:
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
    def nPECut(self, cutName='nPECut', nPECut=2, cut=False, branches=None):
        self.events[cutName] = self.events.nPE >= int(nPECut)
        if cut:
            for branch in branches:
                self.events[branch] = self.events[branch][self.events[cutName]]        

    @mqCut
    def heightCut(self, cutName='heightCut', heightCut=800, cut=False, branches=None):
        self.events[cutName] = self.events.height >= int(heightCut)
        if cut:
            self.cutBranches(branches, cutName)
                
    #create mask/cut for pulses passing area cuts
    @mqCut
    def areaCut(self, cutName='areaCut', areaCut=50000, cut=False, branches=None):
        self.events[cutName] = self.events.area >= int(areaCut)
        if cut:
            self.cutBranches(branches, cutName)

    #create mask/cut for pulses passing nPE cut
    @mqCut
    def nPECut(self, cutName='nPECut', nPECut=2, cut=False, branches=None):
        self.events[cutName] = self.events.nPE >= int(nPECut)
        if cut:
            self.cutBranches(branches, cutName)   

    #creates mask/cut selecting bars only (no panels)
    @mqCut
    def barCut(self, cutName='barCut', cut=False, branches=None):
        self.events[cutName] = self.events['type'] == 0
        if cut:
            self.cutBranches(branches, cutName)

    #find the largest pulse nPE at each layer for bar(used for cosmic sim validation)
    @mqCut
    def lnPE(self, cutName='lnPE', cut=False, branches=None):
        l0MaxnPE = ak.max(self.events['nPE'][(self.events['type'] == 0) & (self.events['layer'] == 0)])
        l1MaxnPE = ak.max(self.events['nPE'][(self.events['type'] == 0) & (self.events['layer'] == 1)])
        l2MaxnPE = ak.max(self.events['nPE'][(self.events['type'] == 0) & (self.events['layer'] == 2)])
        l3MaxnPE = ak.max(self.events['nPE'][(self.events['type'] == 0) & (self.events['layer'] == 3)])
        self.events[cutName] = ak.concatenate([l0MaxnPE,l1MaxnPE,l2MaxnPE,l3MaxnPE],axis=1)
        print(ak.to_list(self.events[cutName]))



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
    
    #creates mask/cut vetoing any event with front/back panel hit w/ nPE > nPECut
    @mqCut
    def beamMuonPanelVeto(self, cutName='beamMuonPanelVeto', cut=False, nPECut=100, branches=None):
        
        passNPECut = self.events['nPE'] > nPECut
        panelCut = self.events['type'] == 1

        finalCut = passNPECut & panelCut
        finalCut = ak.any(finalCut, axis=1)
        finalCut = ~finalCut

        finalCut = ak.fill_none(finalCut, False)
        testIndex = ak.where(ak.num(self.events['nPE'][(self.events['layer'] == -1) & panelCut], axis=1) > 0)

        _, finalCut = ak.broadcast_arrays(self.events.npulses, finalCut)
        self.events[cutName] = finalCut

        self.events['frontPanelNPEBefore'] = self.events['nPE'][(self.events['layer'] == -1) & panelCut]
        self.events['backPanelNPEBefore'] = self.events['nPE'][(self.events['layer'] == 4) & panelCut]
        self.events['frontPanelNPEAfter'] = self.events['nPE'][(self.events['layer'] == -1) & panelCut & finalCut]
        self.events['backPanelNPEAfter'] = self.events['nPE'][(self.events['layer'] == 4) & panelCut & finalCut]


        if cut:
            self.cutBranches(branches, cutName)

    ######################################
    ## Geometric Selections
    #######################################

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

                rowCut = (self.events['row'] == y) & (self.events['type']==0)
                colCut = (self.events['column'] == x) & (self.events['type']==0)

                r_tmp0 = (rowCut[self.events['layer']==0] & colCut[self.events['layer']==0])
                r_tmp1 = (rowCut[self.events['layer']==1] & colCut[self.events['layer']==1])
                r_tmp2 = (rowCut[self.events['layer']==2] & colCut[self.events['layer']==2])
                r_tmp3 = (rowCut[self.events['layer']==3] & colCut[self.events['layer']==3])


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
                if(x == 0 and y == 0): straight_pulse = (straight_cuts[4*x+y]) & (self.events['column'] == x) & (self.events['row'] == y) & (self.events['type'] == 0)
                else: straight_pulse = (straight_pulse) ^ ((straight_cuts[4*x+y]) & (self.events['column'] == x) & (self.events['row'] == y) & (self.events['type'] == 0))

        self.events['numStraightPaths'] = ak.sum(straight_pulse, axis=1) / 4
        self.events[cutName+'Pulse'] = straight_pulse

        #get self.events passing 1 bar movement
        if allowedMove:
            for ipath, path in enumerate(combos):
                if ipath == 0: passing = path
                else: passing = passing | path

            self.events['moveOnePath'] = passing

        if cut:
            self.cutBranches(branches, cutName+"Pulse")
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
    def threeInLine(self, cutName='threeInLine', cut=False, branches=None):
        npeCut = 2

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

    ##################################
    ## Pulse Timing Cuts
    ##################################

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

    def to_binary(self, x):
        return bin(int(x))[2:]

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
    def timeMaxMin(self, cutName='timeMaxMin', timeCut=20, cut=False, branches=None):
        maxTime = ak.max(self.events['timeFit_module_calibrated'][self.events['type']==0], axis=1, keepdims=True)
        minTime = ak.min(self.events['timeFit_module_calibrated'][self.events['type']==0], axis=1, keepdims=True)

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

    @mqCut
    #method for simulation 
    def timeDiff_simValid(self, cutName='timeDiff_simValid', branches=None):
        times0 = self.events['timeFit_module_calibrated'][(self.events['layer']==0) & (self.events['type']==0)]
        times3 = self.events['timeFit_module_calibrated'][(self.events['layer']==3) & (self.events['type']==0)]
        diff = ak.min(times3,axis = 1) - ak.min(times0,axis = 1)

        self.events[cutName] = diff

    ##############################
    ## Other
    ##############################
    
    #creates mask/cut vetoing any event where the min/max nPE ratio < nPECut
    @mqCut
    def nPEMaxMin(self, cutName='nPEMaxMin', cut=False, nPECut = 10, branches=None):
        maxNPE = ak.max(self.events['nPE'][self.events['type']==0], axis=1, keepdims=True)
        minNPE = ak.min(self.events['nPE'][self.events['type']==0], axis=1, keepdims=True)

        self.events['maxNPEBefore'] = maxNPE
        self.events['minNPEBefore'] = minNPE

        nPERatio = maxNPE/minNPE
        nPECut = nPERatio < nPECut

        nPECut = ak.fill_none(nPECut, False)

        _, nPECutMod = ak.broadcast_arrays(maxNPE, nPECut)
        self.events['maxNPEAfter'] = maxNPE[nPECutMod] 
        self.events['minNPEAfter'] = minNPE[nPECutMod]

        _, nPECut = ak.broadcast_arrays(self.events.npulses, nPECut)

        self.events[cutName] = nPECut
        if cut:
            self.cutBranches(branches, cutName)






