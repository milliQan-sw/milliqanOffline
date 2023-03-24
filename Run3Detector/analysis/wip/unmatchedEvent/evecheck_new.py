#V3.0
#3/18/23 Collin
#usage:
#1.'python3 evecheck_new.py all_run' # mutiple runs & need to specify number of processes.
#2.'python3 evecheck_new.py single_run --runNum MilliQan_Run570' this is an example for specific run

#3/20 single run debug finished
#--------------------------------------------------------------------------
#3/23 remove multiprocessing
#

#---------------------------------------------------------------------------
import ROOT as r
import os
import sys
import numpy as np

from array import array
import argparse
import time
import csv


def initializeTree(run):

    treeChain = r.TChain("t")
    treeChain.Add('/store/user/mcarrigan/trees/v29/' + run + '.*_v29_firstPedestals.root')
    return treeChain


variables=[] #used to save the open. Is this a better alternative.

def count(run):
    info=[]#used to store the construtable events
    Num_C=0 #use to count the contrutable event
    
    #board times can be off by some value (try 200ns)
    maxDiff = 200 

    unmatchedEvents = []
    trees = initializeTree(run)
    #make list of unmatched events
    for ievent, event in enumerate(trees):
        if 0 in event.v_groupTDC_g0: 
            unmatchedEvents.append(np.array(event.v_groupTDC_g0))   
    
                                   #all events are matched in a run
    if len(unmatchedEvents) == 0:
        return None
    
    unmatchedEvents.sort(key=lambda x: max(x))  #sort the unmatchedEvents based on its max TDC
    
    print("unmatchedEvents:"+str(unmatchedEvents)) #debug

    maxTDC_list = []
    
    for event in unmatchedEvents:
        maxTDC_list.append(max(event))
    print("maxTDC_list:"+str(maxTDC_list)) #debug
    ajacent_time = [y - x for x, y in zip(maxTDC_list[:], maxTDC_list[1:])]

    print("ajacent_time:" + str(ajacent_time)) #debug
    
    list1 = [] #used for storing the event to check if they are construtable



    j = 0
    for index,num in enumerate(ajacent_time):
        if  j == 0 & num <= maxDiff:
            list1.append(unmatchedEvents[index])
            list1.append(unmatchedEvents[index+1])
            j += 1
        if num <= maxDiff & j > 0:
            
            list1.append(unmatchedEvents[index+1])
            print("list1 debug"+str(list1))
            
        #elif num > maxDiff:
        else:
            Construtable_info=check_constutabl(list1,unmatchedEvents)
            print("Construtable_info:" + str(Construtable_info))
            if Construtable_info is not None:
                info.append(Construtable_info)
                Num_C += 1
            #return some info
            j = 0 #reset
            list1 = [] #clean the list1 and prepare for next iteration
            #list1.append(num)
            
    #after loop over all events
    Num_u=len(unmatchedEvents) 
    #info  #just in case we are interest in which event are construtable
    #Num_C=len(info)#
    T_event =trees.GetEntries()        
    #+ variable.append() section
    ratio1 = Num_u/T_event  #unmatched events/ total events
    ratio2 = Num_C/T_event  #constructable events/ total events
    
    #variables.append((ratio1,ratio2,Num_C,info)) #debug
    variables.append((run,ratio1,ratio2))


def check_constutabl(list1,unmatchedEvents):
    if len(list1) <= 1: return None
    
    else:
        
        T = [0,0,0,0,0]
        print("list debug:" + str(list1)) #debug
        for event in list1:
            print("event debug:" + str(event)) #debug
            for index,tdcTime in enumerate(event):
                if tdcTime != 0:
                    T[index]=1
                else:
                    continue
        if 0 not in T:
            print("construtable found!")
            return list1 #list of construtable event
        else:
            return None

def single_run(run):
    count(run)
    print(variables)



def mutiple_run(run):

    count(run)


def Main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    single_run_arg = subparser.add_parser('single_run')
    all_run = subparser.add_parser('all_run')
    

    single_run_arg.add_argument('--runNum',type = str, required = True)

    
    args = parser.parse_args()
    
    if args.command == 'single_run':
        print(args.runNum)
        runNum = args.runNum
        single_run(args.runNum)

    if args.command == 'all_run':

        A=os.listdir('/store/user/mcarrigan/trees/v29/')
        #extract the run number
        b = [s.split(".")[0] for s in A]
        unique_run = sorted(list(set(b))) 
        print("mutiple run start") 
        for run in unique_run:
            #check empty run
            NOE=run.GetEntries()
            if NOE == 0:
                continue #throw away the empty run
            else:
                mutiple_run(run)
        
        print(run) #debug
        with open('my_file.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(my_list)

        tot_run=len(unique_run)
        mutiple_run(unique_run)
        

if __name__ == "__main__":
    Main()
