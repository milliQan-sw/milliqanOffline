#V3.0
#3/18/23 Collin
#usage:
#1.'python3 evecheck_new.py all_run --NumOfProcesses NOP' # mutiple runs & need to specify number of processes.
#2.'python3 evecheck_new.py single_run --runNum MilliQan_Run570' this is an example for specific run

#3/20 single run debug finished



#---------------------------------------------------------------------------
import ROOT as r
import os
import sys
import numpy as np

from array import array
from multiprocessing import Process, Manager
import argparse
import time


def initializeTree(run):

    treeChain = r.TChain("t")
    treeChain.Add('/store/user/mcarrigan/trees/v29/' + run + '.*_v29_firstPedestals.root')
    return treeChain






def count(run, variables):
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


    #check the following code it has bug
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
    manager = Manager()
    variables = manager.list() #created shared variable
    processes = []

    p = Process(target = count, args=(run,variables))
    processes.append(p)
    p.start()
    p.join()

    #print("the construtable events are" + str(list1))
    print("variabls"+str(variables)) #debug
    #TBDadd more print



def mutiple_run(unique_run,NOP):
    num_processes = NOP  #add parser
    manager = multiprocessing.Manager()
    variables = manager.list()
    processes = []
    for i in range(10):
        p = multiprocessing.Process(target=count, args=(run, variables))
        processes.append(p)
        if len(processes) == num_processes:
            for p in processes:
                p.start()
            for p in processes:
                p.join()
            processes = []
    
    # do the remaining process
    if processes:
        for p in processes:
            p.start()
        for p in processes:
            p.join()
    #plot1(variables) # number of constructible unmatched event / number of unique unmatched event(based on TDCtime)
    #plot2(variables) # number of repeated event / number of unique event




def Main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    single_run_arg = subparser.add_parser('single_run')
    all_run = subparser.add_parser('all_run')
    

    single_run_arg.add_argument('--runNum',type = str, required = True)
    all_run.add_argument('--NumOfProcesses',type = str, required = True)
    
    args = parser.parse_args()
    
    if args.command == 'single_run':
        print(args.runNum)
        runNum = args.runNum
        single_run(args.runNum)
        #run with python eventcheck1_1V29.py single_run --runNum 'MilliQan_Run570'
    if args.command == 'all_run':
        NOP = args.NumOfProcesses
        
        
        A=os.listdir('/store/user/mcarrigan/trees/v29/')
        #extract the run number
        b = [s.split(".")[0] for s in A]
        # keep the unique elements in array with 'set()' and sort them base on run number.
        unique_run = sorted(list(set(b)))
        tot_run=len(unique_run)
        mutiple_run(unique_run,NOP)
        #print("mutiple run start") #test

if __name__ == "__main__":
    Main()
