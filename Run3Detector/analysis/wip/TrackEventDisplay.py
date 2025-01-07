import numpy as np
import matplotlib.pyplot as plt
import awkward as ak
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import uproot
import re
import argparse
import os


def filling(typeArr,layerArr,rowArr,columnArr,npeArr,timeArr,NpeT,oFFline=False):
    PulseNumArr = np.zeros((5, 22)) #count the number of pulse in each channel
    NPEArr = np.zeros((5, 22))
    TimeArr = np.zeros((5, 22)) #pulse time for each channels that corresponding to the max pulse in the event
    for type,layer,row,column,npe,time in zip (typeArr,layerArr,rowArr,columnArr,npeArr,timeArr):
        #bar channel data filling
        if type == 0:

            if layer == 0:
                fillingColumn_offset = 2 + column
                rowoffset = 4-row
            elif layer == 1:
                fillingColumn_offset = 7 + column
                rowoffset = 4-row
            
            elif layer == 2:
                fillingColumn_offset = 12 + column
                rowoffset = 4-row
            
            elif layer == 3:
                fillingColumn_offset = 17 + column
                rowoffset = 4-row

        #slab (beam)
        elif type == 1:
            if layer == -1:
                fillingColumn_offset = 0 
                rowoffset = 4

            if layer  == 4:
                fillingColumn_offset = 21
                rowoffset = 4
        #panel (cosmic)
        elif type == 2:
            if layer == 0:
                if column == -1:
                    fillingColumn_offset = 1
                    rowoffset = 4
                elif column == 0:
                    fillingColumn_offset = 2
                    rowoffset = 0
                elif column == 4:
                    fillingColumn_offset = 6
                    rowoffset = 4

            if layer  == 2:
                if column == -1:
                    fillingColumn_offset = 11
                    rowoffset = 4
                elif column == 0:
                    print("find it")
                    fillingColumn_offset = 12
                    rowoffset = 0
                elif column == 4:
                    fillingColumn_offset = 16
                    rowoffset = 4

        

        if npe > NpeT:
            PulseNumArr[rowoffset][fillingColumn_offset] += 1  
            if (type == 2):
                if (column == 0): #top cosmic panel

                    PulseNumArr[rowoffset][fillingColumn_offset+1] += 1
                    PulseNumArr[rowoffset][fillingColumn_offset+2] += 1  
                    PulseNumArr[rowoffset][fillingColumn_offset+3] += 1  
                    PulseNumArr[rowoffset][fillingColumn_offset+4] += 1 
                    PulseNumArr[rowoffset][fillingColumn_offset+5] += 1
                    PulseNumArr[rowoffset][fillingColumn_offset+6] += 1
                    PulseNumArr[rowoffset][fillingColumn_offset+7] += 1
                    PulseNumArr[rowoffset][fillingColumn_offset+8] += 1
         
                else: #side cosmic panels
                    PulseNumArr[rowoffset-1][fillingColumn_offset] += 1  
                    PulseNumArr[rowoffset-2][fillingColumn_offset] += 1  
                    PulseNumArr[rowoffset-3][fillingColumn_offset] += 1  


        #find the max pulse of current channel
        if npe > NPEArr[rowoffset][fillingColumn_offset]:
            if oFFline:
                if (type != 0) and (npe/1000 > NPEArr[rowoffset][fillingColumn_offset]) :
                    NPEArr[rowoffset][fillingColumn_offset] = (npe/1000)
                    TimeArr[rowoffset][fillingColumn_offset] = time
                else:
                    NPEArr[rowoffset][fillingColumn_offset] = npe
                    TimeArr[rowoffset][fillingColumn_offset] = time
                

            else:
                NPEArr[rowoffset][fillingColumn_offset] = npe
                TimeArr[rowoffset][fillingColumn_offset] = time
    #print(block) 
    
    return TimeArr,NPEArr,PulseNumArr

def MakePlot(filenumber,EventNumber,filelocation,NpeT=0.6):
    
    if os.path.isfile(filelocation): pass
    else:
        print("can't find the file")
        print(f"current file location:{filelocation}")
        print(f"please change file location in TrackEventDisplay.py")
        return
    
    EventNumber = int(EventNumber)
    uptree = uproot.open(f"{filelocation}:t")#consider the case for merge file
    branches = uptree.arrays(["type","layer","row","column","nPE","event","area","timeFit_module_calibrated","chan","ipulse","fileNumber"])
    if filenumber != None: #if I use specific file instead of merge file then there is no need to select the fileNumber
        branches = branches[branches["fileNumber"]==filenumber]
    typeArr= (branches["type"][branches["ipulse"]==0])[branches["event"]==EventNumber]
    layerArr = (branches["layer"][branches["ipulse"]==0])[branches["event"]==EventNumber]
    rowArr = (branches["row"][branches["ipulse"]==0])[branches["event"]==EventNumber]
    columnArr = (branches["column"][branches["ipulse"]==0])[branches["event"]==EventNumber]
    npeArr = (branches["nPE"][branches["ipulse"]==0])[branches["event"]==EventNumber]
    timeArr = (branches["timeFit_module_calibrated"][branches["ipulse"]==0])[branches["event"]==EventNumber]
    
    
    PTimeArr,NPEarr,arr=filling(typeArr[0],layerArr[0],rowArr[0],columnArr[0],npeArr[0],timeArr[0],NpeT)
    #display the the  NPE and pulse time for the first hit at each channel
    LargestNPE = np.max(NPEarr) # find the largest hit among all of the channel. I need to use this value to change color of text to increase contrast.

    for row in range(5):
        for column in range(22):
            if (NPEarr[row,column] > NpeT) and (NPEarr[row,column] <= (LargestNPE*0.6)):
                MaxNPEText = plt.text(column,4-row,f"{int(NPEarr[row,column])} PE", color="white",fontsize=3)
                PulseTimeMText = plt.text(column,4-row + 0.5,f"{round(PTimeArr[row,column], 1)}ns", color="white",fontsize=3)
                
            elif (NPEarr[row,column] > NpeT) and (NPEarr[row,column] > (LargestNPE*0.6)):
                MaxNPEText = plt.text(column,4-row,f"{int(NPEarr[row,column])} PE", color="black",fontsize=3)
                PulseTimeMText = plt.text(column,4-row + 0.5,f"{round(PTimeArr[row,column], 1)}ns", color="black",fontsize=3)

            if NPEarr[row,column] < NpeT:
                NPEarr[row,column] = np.nan #remove the pulse under threshold

    
    # Get the current axes
    ax = plt.gca()

    #beam panels have the red outline
    beamF = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none')
    beamB = patches.Rectangle((21, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(beamF)
    ax.add_patch(beamB)
    #cosmic panel have the white outline
    COS70 = patches.Rectangle((1, 0), 1, 4, linewidth=2, edgecolor='grey', facecolor='none')
    COS72 = patches.Rectangle((6, 0), 1, 4, linewidth=2, edgecolor='grey', facecolor='none')
    COS71 = patches.Rectangle((11, 0), 1, 4, linewidth=2, edgecolor='grey', facecolor='none')
    COS73 = patches.Rectangle((16, 0), 1, 4, linewidth=2, edgecolor='grey', facecolor='none')
    Cos68 = patches.Rectangle((2, 4), 9, 1, linewidth=2, edgecolor='grey', facecolor='none')
    Cos69 = patches.Rectangle((12, 4), 9, 1, linewidth=2, edgecolor='grey', facecolor='none')
    ax.add_patch(COS70)
    ax.add_patch(COS72)
    ax.add_patch(COS73)
    ax.add_patch(COS71)
    ax.add_patch(Cos68)
    ax.add_patch(Cos69)
    #bar channel with 
    L0b= patches.Rectangle((2, 0), 4, 4, linewidth=2, edgecolor='orange', facecolor='none')
    L1b= patches.Rectangle((7, 0), 4, 4, linewidth=2, edgecolor='orange', facecolor='none')
    L2b= patches.Rectangle((12, 0), 4, 4, linewidth=2, edgecolor='orange', facecolor='none')
    L3b= patches.Rectangle((17, 0), 4, 4, linewidth=2, edgecolor='orange', facecolor='none')
    ax.add_patch(L0b)
    ax.add_patch(L1b)
    ax.add_patch(L2b)
    ax.add_patch(L3b)


    plt.imshow(NPEarr, cmap='viridis', origin='upper', norm=mcolors.Normalize(vmin=0.001), extent=[0, 22, 0, 5]) 
    plt.colorbar(label= f'NPE of first pulse. Display TH {NpeT}NPE')
    #plt.show() #uncomment this if you want to draw the graph in interactively
    match = re.search(r"Run(\d+)\.(\d+)", filelocation)
    plt.savefig(f"displays/Run{match.group(1)}/run{match.group(1)}file{match.group(2)}Event{EventNumber}_Track.png", dpi=300, bbox_inches="tight")




if __name__ == "__main__":

    #you can also run the script without command-line arguments.
    filenumber = None # specify the file numer if you are using the merged file.
    # file at eos space test
    #EventNumber = 972
    #filelocation = "/eos/experiment/milliqan/trees/v35/1100/MilliQan_Run1176.83_v35.root"

    #local file test
    #EventNumber = 972
    #filelocation = "/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run1176.133_v34.root"
    #MakePlot(filenumber,EventNumber,filelocation,NpeT=0.6)

    parser = argparse.ArgumentParser(description="event display for the first pulse at each channel")

    # Add arguments
    parser.add_argument('--event', help='event number')
    parser.add_argument('--file_num', help='file number', required=True)
    parser.add_argument('--run', help='run number')

    args = parser.parse_args()

    #filelocation = f"/eos/experiment/milliqan/trees/v35/{(args.run)[:2]}00/MilliQan_Run{args.run}.{args.file_num}_v35.root" #EOS space
    #filelocation = f"/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run{args.run}.{args.file_num}_v34.root" #local test
    filelocation = f"/store/user/milliqan/trees/v35/bar/{(args.run)[:2]}00/MilliQan_Run{args.run}.{args.file_num}_v35.root" #OSU T3 
    MakePlot(filenumber,args.event,filelocation,NpeT=0.6)
