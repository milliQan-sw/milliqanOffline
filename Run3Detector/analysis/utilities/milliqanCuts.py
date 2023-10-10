#!/usr/bin/python3

import awkward as ak

#function to allow multiple masks (cuts) to be combined together and saved as name
def combineCuts(events, cuts, name):
    name = name.replace("'", "").strip()
    for cut in eval(cuts):
        if name in ak.fields(events):
            events[name] = events[name] & (events[cut])
        else:
            events[name] = events[cut]
    return events

#create mask for pulses in each layer
def layerCut(events):
    events['layer0'] = events.layer == 0
    events['layer1'] = events.layer == 1
    events['layer2'] = events.layer == 2
    events['layer3'] = events.layer == 3
    return events

#event level mask selecting events with hits in 4 layers
def fourLayerCut(events):
    events['fourLayers'] = ak.any(events.layer0, axis=1) & ak.any(events.layer1, axis=1) & ak.any(events.layer2, axis=1) & ak.any(events.layer3, axis=1)
    return events

#create mask for pulses passing height cut
def heightCut(events, heightCut=1200):
    events['heightCut'] = events.height >= int(heightCut)
    return events

#selection events that have hits in a straight path
#option allowedMove will select events that only move one bar horizontally/vertically
def straightLineCut(events, allowedMove=False):
    
    #allowed combinations of moving
    combos = []
    straight_cuts = []

    #bool to decide if 1 bar movement should be found
    allowedMove = False

    debugEvt = 1191

    for i, x in enumerate(range(4)):
        for j, y in enumerate(range(4)):

            rowCut = events.row == y
            colCut = events.column == x

            r_tmp0 = (rowCut[events.layer0] & colCut[events.layer0])
            r_tmp1 = (rowCut[events.layer1] & colCut[events.layer1])
            r_tmp2 = (rowCut[events.layer2] & colCut[events.layer2])
            r_tmp3 = (rowCut[events.layer3] & colCut[events.layer3])


            row_pass = ak.any(r_tmp0, axis=1) & ak.any(r_tmp1, axis=1) & ak.any(r_tmp2, axis=1) & ak.any(r_tmp3, axis=1)

            if allowedMove:
                rowCut_p1 = events.row == y+1
                rowCut_m1 = events.row == y-1
                colCut_p1 = events.column == x+1
                colCut_m1 = events.column == x-1
                if(y > 0): 
                    m1_c0_r1 = (rowCut_m1[events.layer1]) & (colCut[events.layer1])
                    m2_c0_r1 = (rowCut_m1[events.layer2]) & (colCut[events.layer2])
                    m3_c0_r1 = (rowCut_m1[events.layer3]) & (colCut[events.layer3])
                if(x > 0): 
                    m1_c1_r0 = (rowCut[events.layer1]) & (colCut_m1[events.layer1])
                    m2_c1_r0 = (rowCut[events.layer2]) & (colCut_m1[events.layer2])
                    m3_c1_r0 = (rowCut[events.layer3]) & (colCut_m1[events.layer3])

                if(y < 4): 
                    p1_c0_r1 = (rowCut_p1[events.layer1]) & (colCut[events.layer1])
                    p2_c0_r1 = (rowCut_p1[events.layer2]) & (colCut[events.layer2])
                    p3_c0_r1 = (rowCut_p1[events.layer3]) & (colCut[events.layer3])
                if(x < 4): 
                    p1_c1_r0 = (rowCut[events.layer1]) & (colCut_p1[events.layer1])
                    p2_c1_r0 = (rowCut[events.layer2]) & (colCut_p1[events.layer2])
                    p3_c1_r0 = (rowCut[events.layer3]) & (colCut_p1[events.layer3])

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

    events['straightPath'] = straight_path

    for x in range(4):
        for y in range(4):
            if(x == 0 and y == 0): straight_pulse = (straight_cuts[4*x+y]) & (events.column == x) & (events.row == y)
            else: straight_pulse = (straight_pulse) | ((straight_cuts[4*x+y]) & (events.column == x) & (events.row == y))

    events['straightPulses'] = straight_pulse

    #get events passing 1 bar movement
    if allowedMove:
        for ipath, path in enumerate(combos):
            if ipath == 0: passing = path
            else: passing = passing | path

        events['moveOnePath'] = passing

    return events

#select events that have 3 area saturating pulses in a line
def threeAreaSaturatedInLine(events, areaCut=50000):
    #make sure 3 layers have saturating hits
    saturating_cut = 500000
    sat_0 = events.area[(events.eventCuts) & (events.layer0) & (events.area >= saturating_cut) & (events.straightPulses)]
    sat_1 = events.area[(events.eventCuts) & (events.layer1) & (events.area >= saturating_cut) & (events.straightPulses)]
    sat_2 = events.area[(events.eventCuts) & (events.layer2) & (events.area >= saturating_cut) & (events.straightPulses)]
    sat_3 = events.area[(events.eventCuts) & (events.layer3) & (events.area >= saturating_cut) & (events.straightPulses)]
    
    events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
    events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))
    return events
    
#select events that have 3 height saturating pulses in a line
def threeAreaSaturatedInLine(events, areaCut=50000):
    #make sure 3 layers have saturating hits
    saturating_cut = 500000
    sat_0 = events.area[(events.eventCuts) & (events.layer0) & (events.area >= saturating_cut) & (events.straightPulses)]
    sat_1 = events.area[(events.eventCuts) & (events.layer1) & (events.area >= saturating_cut) & (events.straightPulses)]
    sat_2 = events.area[(events.eventCuts) & (events.layer2) & (events.area >= saturating_cut) & (events.straightPulses)]
    sat_3 = events.area[(events.eventCuts) & (events.layer3) & (events.area >= saturating_cut) & (events.straightPulses)]
    
    events['three_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) | (ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_0, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1)) | (ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & ak.any(sat_3, axis=1))
    events['four_sat'] = ak.any(sat_0, axis=1) & ak.any(sat_1, axis=1) & ak.any(sat_2, axis=1) & (ak.any(sat_3, axis=1))
    return events

def matchedTDCTimes(events):
    board0 = events.v_groupTDC_g0[:, 0]
    board1 = events.v_groupTDC_g0[:, 1]
    board2 = events.v_groupTDC_g0[:, 2]
    board3 = events.v_groupTDC_g0[:, 3]
    board4 = events.v_groupTDC_g0[:, 4]

    events['tdcMatch'] = (board0 == board1) & (board0 == board2) & (board0 == board3) & (board0 == board4)
    return events
