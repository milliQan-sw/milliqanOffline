import os
import sys

from milliqanProcessor import *
from milliqanScheduler import *
from milliqanCuts import *
from milliqanPlotter import *



filelist =['/mnt/hadoop/se/store/user/milliqan/trees/v34/MilliQan_Run1190.155_v34.root:t']
branches = ['boardsMatched', 'height', 'layer','type','chan','pickupFlag']
for events in uproot.iterate(

            #files
            filelist,

            #branches
            branches,
            step_size=1000
    
            ):
    
    
    
    #print(len(events))
    #print(events)
    intialdf = ak.to_pandas(events)
    print(intialdf)
    
    
    #print(type(events))
    for branch in branches:
        if branch == 'boardsMatched': continue
        events[branch] = events[branch][events.boardsMatched]
    afterdf = ak.to_pandas(events)
    #print(afterdf)
    
    for branch in branches:
        if branch == 'boardsMatched': continue
        events[branch] = events[branch][events.pickupFlag]
    
    
    lastdf = ak.to_pandas(events)
    #print(lastdf)
    
    
    #type cut
    barCut = events['type'] == 0 # create pulse base T/F table
    for branch in branches:
        if branch == 'boardsMatched': continue   #this is needed to avoid too many jacked slice in array.(dont know the meaing)
        events[branch] = events[branch][barCut]
    
    
    typpecutdf = ak.to_pandas(events)
    #print(typpecutdf)
    
    #print the key name for high level akw array
    field_names = events.fields
    #print(field_names)

    
    
    
    #print(type(events))
    #print(str(events))
    
    
    #pulse height cut 1 npe
    heightcut = events.height > 36
    #print(heightcut)
    
    
    for branch in branches:
        if branch == 'boardsMatched': continue
        events[branch] = events[branch][heightcut]
    
    heightCutdf = ak.to_pandas(events)
    #print(heightCutdf)
    
    
    #1 hit + per layer
    
    events['fourLayerCut'] = ak.any(events.layer==0, axis=1) & ak.any(events.layer==1, axis=1) & ak.any(events.layer==2, axis=1) & ak.any(events.layer==3, axis=1)
    #print(ak.to_pandas(events))#event based
    events = events[events['fourLayerCut']]
    print("final result")
    print(ak.to_pandas(events))
    
    
    
    
    
    #FLcut,events=ak.broadcast_arrays(FLcut,events)
    #print(FLcut)
    #print(events)
    #seems doesn't work
    #need to used broadcase
    
    #FLcut = events[events['fourLayerCut']]
    
    #print(events)
    #for branch in branches:
    #    if branch == 'boardsMatched': continue
    #    events = events[branch][FLcut]
    
    
        
    #FLcutdf = ak.to_pandas(events)
    #print(FLcutdf)
    

        
    #events["heightCut"] = events.height >= int(1200)  #pulse based table
    #events['fourLayerCut'] = ak.any(events.layer==0, axis=1) & ak.any(events.layer==1, axis=1) & ak.any(events.layer==2, axis=1) & ak.any(events.layer==3, axis=1) 
    #expanded_array = ak.to_pandas(events)
    #print(expanded_array)
    
    print("next")
    break