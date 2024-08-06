"""
select sim and offline when doing the demonstration

with cosmic muon events

Follow david's suggestion find the sample muon event


Todo
When making the straight track, it should add an extra offset factor -0.5


usage:

currently the big hit threashold and the file number are hard code in the script

python3 FillingTest.py 378(event number)




"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import awkward as ak
import ROOT as r
import matplotlib.patches as patches
import math

def filling(typeArr,layerArr,rowArr,columnArr,npeArr,timeArr,NpeT):
    block = np.zeros((5, 22))
    MaxNPEArr = np.zeros((5, 22))
    MaxPTimeArr = np.zeros((5, 22)) #pulse time for each channels that corresponding to the max pulse in the event
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
            block[rowoffset][fillingColumn_offset] += 1  
            if (type == 2):
                if (column == 0): #top cosmic panel

                    block[rowoffset][fillingColumn_offset+1] += 1
                    block[rowoffset][fillingColumn_offset+2] += 1  
                    block[rowoffset][fillingColumn_offset+3] += 1  
                    block[rowoffset][fillingColumn_offset+4] += 1 
                    block[rowoffset][fillingColumn_offset+5] += 1
                    block[rowoffset][fillingColumn_offset+6] += 1
                    block[rowoffset][fillingColumn_offset+7] += 1
                    block[rowoffset][fillingColumn_offset+8] += 1
         
                else: #side cosmic panels
                    block[rowoffset-1][fillingColumn_offset] += 1  
                    block[rowoffset-2][fillingColumn_offset] += 1  
                    block[rowoffset-3][fillingColumn_offset] += 1  



        if npe > MaxNPEArr[rowoffset][fillingColumn_offset]:
            MaxNPEArr[rowoffset][fillingColumn_offset] = npe
            MaxPTimeArr[rowoffset][fillingColumn_offset] = time
    #print(block) 
    return MaxPTimeArr,MaxNPEArr,block

def findTackWeight(MaxNPEArr):
    #find the possible muon with the weight of max pulse npe
    # arr stores the number pulse above specific threashold for each channel
    # MaxNPEArr stores the max pulse npe for each channel

    rowTempL0 = list()
    columnTempL0 = list()

    rowTempL1 = list()
    columnTempL1 = list()

    rowTempL2 = list()
    columnTempL2 = list()

    rowTempL3 = list()
    columnTempL3 = list()

    ROWarrST = list()
    ColumnarrST = list()


    #find the weight postion with the pulse npe at layer 0 row 4
    for row in range(4):
        
        L0sumWeight = 0
        L0sumTerm = 0

        L1sumWeight = 0
        L1sumTerm = 0

        L2sumWeight = 0
        L2sumTerm = 0

        L3sumWeight = 0
        L3sumTerm = 0

        #layer 0 row 3 in the bar corresponds to (row = 1) in MaxNPEArr
        for column in [2,3,4,5]:

            L0sumWeight += (MaxNPEArr[row+1][column])*(column)
            L0sumTerm += MaxNPEArr[row+1][column]
        
        for column in [7,8,9,10]:

            L1sumWeight += (MaxNPEArr[row+1][column])*(column)
            L1sumTerm += MaxNPEArr[row+1][column]

        
        for column in [12,13,14,15]:

            L2sumWeight += (MaxNPEArr[row+1][column])*(column)
            L2sumTerm += MaxNPEArr[row+1][column]

        for column in [17,18,19,20]:

            L3sumWeight += (MaxNPEArr[row+1][column])*(column)
            L3sumTerm += MaxNPEArr[row+1][column]

        L0 = 0
        L1 = 0
        L2 = 0
        L3 = 0
        
        
        if L0sumTerm >= 1:
            L0 = L0sumWeight/L0sumTerm

        if L1sumTerm >= 1:
            L1 = L1sumWeight/L1sumTerm
        
        if L2sumTerm >= 1:
            L2 = L2sumWeight/L2sumTerm

        if L3sumTerm >= 1:
            L3 = L3sumWeight/L3sumTerm


            

        columnTempL0.append(L0)
        rowTempL0.append(3-row)
        columnTempL1.append(L1)
        rowTempL1.append(3-row)
        columnTempL2.append(L2)
        rowTempL2.append(3-row)
        columnTempL3.append(L3)
        rowTempL3.append(3-row)

    #record the track only if there is at least one hit in each row in a give layer 

    if all(x > 0 for x in columnTempL0):
        ROWarrST.append(rowTempL0)
        ColumnarrST.append(columnTempL0)

    
    if all(x > 0 for x in columnTempL1):
        ROWarrST.append(rowTempL1)
        ColumnarrST.append(columnTempL1)

    if all(x > 0 for x in columnTempL2):
        ROWarrST.append(rowTempL2)
        ColumnarrST.append(columnTempL2)

    if all(x > 0 for x in columnTempL3):
        ROWarrST.append(rowTempL3)
        ColumnarrST.append(columnTempL3)
    

    return ColumnarrST,ROWarrST




def findTrack(arr):
    print(arr)
    print(arr.shape)
    
    #straightLineArr = np.array([])
    ROWarrST = list()
    ColumnarrST = list()

    
    for column in range(4):
        straightLineArrL0 = 0
        straightLineArrL1 = 0
        straightLineArrL2 = 0
        straightLineArrL3 = 0


        rowTempL0 = list()
        columnTempL0 = list()

        rowTempL1 = list()
        columnTempL1 = list()


        rowTempL2 = list()
        columnTempL2 = list()


        rowTempL3 = list()
        columnTempL3 = list()
        for row in range(4):
            #layer zero
            if arr[row+1][column+2]>= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL0.append(row)
                columnTempL0.append(column+2)
                straightLineArrL0 += 1

            #layer one
            if arr[row+1][column+7] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL1.append(row)
                columnTempL1.append(column+7)
                straightLineArrL1 += 1
            
            #layer two
            if arr[row+1][column+12] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL2.append(row)
                columnTempL2.append(column+12)
                straightLineArrL2 += 1
            
            #layer three
            if arr[row+1][column+17] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL3.append(row)
                columnTempL3.append(column+17)
                straightLineArrL3 += 1



        if straightLineArrL0 == 4:
            #straightLineArr.append([rowTempL0,columnTempL0])
            ROWarrST.append(rowTempL0)
            ColumnarrST.append(columnTempL0)

        
        if straightLineArrL1 == 4:
            #straightLineArr.append([rowTempL1,columnTempL1])
            ROWarrST.append(rowTempL1)
            ColumnarrST.append(columnTempL1)

        if straightLineArrL2 == 4:
            #straightLineArr.append([rowTempL2,columnTempL2])
            ROWarrST.append(rowTempL2)
            ColumnarrST.append(columnTempL2)

        if straightLineArrL3 == 4:
            #straightLineArr.append([rowTempL3,columnTempL3])
            ROWarrST.append(rowTempL3)
            ColumnarrST.append(columnTempL3)
    
    #end of straight down path (no column shifting)


    #diagonal ST line
    #DGpath1Column = np.array([])
    #DGpath1Row = np.array([])
    #DGpath2Column = np.array([])
    #DGpath2Row = np.array([])

    for column in [2,7,12,17]:
        if (arr[1][column] >= 1) and (arr[2][column+1] >= 1) and (arr[3][column+2] >= 1) and (arr[4][column+3] >= 1):
            ColumnarrST.append([column,column+1,column+2,column+3])
            ROWarrST.append([3,2,1,0])
    
    for column in [5,10,15,20]:
        if (arr[1][column] >= 1) and (arr[2][column-1] >= 1) and (arr[3][column-2] >= 1) and (arr[4][column-3] >= 1):
            ColumnarrST.append([column,column-1,column-2,column-3])
            ROWarrST.append([3,2,1,0])

    #shifting to the right
    #shift1Column = np.array([])
    #shift1Row = np.array([])
    for column in [2,3,4,7,8,9,12,13,14,17,18,19]:
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column] >= 1) and (arr[4][column+1] >= 1):
            ColumnarrST.append([column,column,column,column+1])
            ROWarrST.append([3,2,1,0])

        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column+1] >= 1) and (arr[4][column+1] >= 1):
            ColumnarrST.append([column,column,column+1,column+1])
            ROWarrST.append([3,2,1,0])

        if (arr[1][column] >= 1) and (arr[2][column+1] >= 1) and (arr[3][column+1] >= 1) and (arr[4][column+1] >= 1):
            ColumnarrST.append([column,column+1,column+1,column+1])
            ROWarrST.append([3,2,1,0])

    for column in [2,3,7,8,12,13,17,18]:  
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column+1] >= 1) and (arr[4][column+2] >= 1):
            ColumnarrST.append([column,column,column+1,column+2])
            ROWarrST.append([3,2,1,0])

        if (arr[1][column] >= 1) and (arr[2][column+1] >= 1) and (arr[3][column+2] >= 1) and (arr[4][column+2] >= 1):
            ColumnarrST.append([column,column+1,column+2,column+2])
            ROWarrST.append([3,2,1,0])

    #shifting to the left
    for column in [3,4,5,8,9,10,13,14,15,18,19,20]:
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column] >= 1) and (arr[4][column-1] >= 1):
            ColumnarrST.append([column,column,column,column-1])
            ROWarrST.append([3,2,1,0])

        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column-1] >= 1) and (arr[4][column-1] >= 1):
            ColumnarrST.append([column,column,column-1,column-1])
            ROWarrST.append([3,2,1,0])

        if (arr[1][column] >= 1) and (arr[2][column-1] >= 1) and (arr[3][column-1] >= 1) and (arr[4][column-1] >= 1):
            ColumnarrST.append([column,column-1,column-1,column-1])
            ROWarrST.append([3,2,1,0])
        
    for column in [4,5,9,10,14,15,19,20]: 
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column-1] >= 1) and (arr[4][column-2] >= 1):
            ColumnarrST.append([column,column,column-1,column-2])
            ROWarrST.append([3,2,1,0])

        if (arr[1][column] >= 1) and (arr[2][column-1] >= 1) and (arr[3][column-2] >= 1) and (arr[4][column-2] >= 1):
            ColumnarrST.append([column,column-1,column-2,column-2])
            ROWarrST.append([3,2,1,0])

    return ColumnarrST,ROWarrST

"""
def MakeLego(arr):
    row,column = arr.shape
    fig = plt.figure()
    for r in range(row):
        for c in range(column):
            NumHits = arr[r][c]
            fig.bar3d(c, r, 0, 1, 1, NumHits, color='green')
"""




if __name__ == "__main__":
    import uproot
    #uptree = uproot.open("/Users/haoliangzheng/CERN_ana/MilliQan_Run1500.11_v35.root:t")
    #uptree = uproot.open("/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run1190.1_v34.root:t") #event 472/   are a sample event
    uptree = uproot.open("/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run1500.1_v35.root:t") # event 527 for this file
    branches = uptree.arrays(["type","layer","row","column","nPE","event","area","timeFit_module_calibrated","chan"], entry_stop=100000)

    EventNum = int(sys.argv[1])
    #remove pulses outside the trigger window 1200-1500ns


    removePulse_T = (branches["timeFit_module_calibrated"] >= 1200) & (branches["timeFit_module_calibrated"] <= 1350 )
    """
    for branch in ["type","layer","row","column","nPE","area","timeFit_module_calibrated"]:
        branches[branch] = branches[branch][removePulse_T]
    """


    typeArr= branches["type"][branches["event"]==EventNum]
    layerArr = branches["layer"][branches["event"]==EventNum]
    rowArr = branches["row"][branches["event"]==EventNum]
    columnArr = branches["column"][branches["event"]==EventNum]
    npeArr = branches["nPE"][branches["event"]==EventNum]
    timeArr = branches["timeFit_module_calibrated"][branches["event"]==EventNum]


    

    
    EventArr = branches[branches["event"]==EventNum]
    Lar0barArea=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 0)]
    Lar1barArea=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 1)]
    Lar2barArea=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 2)]
    
    Lar3barArea=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 3)]
    FrBeamPanArea=EventArr["area"][(EventArr["type"] == 2) &  (EventArr["layer"] == -1)]
    BkBeamPanArea=EventArr["area"][(EventArr["type"] == 2) &  (EventArr["layer"] == 4)]
    TpFrontCospArea=EventArr["area"][(EventArr["layer"] == 0) & (EventArr["row"] == 4)]
    TpBackCospArea=EventArr["area"][(EventArr["row"] == 4) & (EventArr["layer"] == 2)]
    print(f"TpBackCosp:{TpBackCospArea}")
    print(f"TpBackCosp area :{EventArr['area'][(EventArr['row'] == 4)]}")
    c1 = r.TCanvas("c1","c1",800,1000)
    c1.Divide(2,4)

    l0BarAreaHist = r.TH1F("l0BarArea","layer 0 bar Area",100,0,1000000)
    l1BarAreaHist = r.TH1F("l1BarArea","layer 1 bar Area",100,0,1000000)
    l2BarAreaHist = r.TH1F("l2BarArea","layer 2 bar Area",100,0,1000000)
    l3BarAreaHist = r.TH1F("l3BarArea","layer 3 bar Area",100,0,1000000)
    FrBeampanelAreaHist = r.TH1F("FbeamPanel","Front beam panel Area",100,0,1000000)
    BkBeampanelAreaHist = r.TH1F("BkeamPanel","Back beam panel Area",100,0,1000000)
    TpFrontPanelAreaHist = r.TH1F("TpFrontCosPanel","top front cos panel Area",100,0,1000000)
    TpBackPanelAreaHist = r.TH1F("TpBackCosPanel","top back cos panel Area",100,0,1000000)



    def HistFilling(data, hist):
        for subdata in data:
            hist.Fill(subdata)

    HistFilling(Lar0barArea[0],l0BarAreaHist)
    HistFilling(Lar1barArea[0],l1BarAreaHist)
    HistFilling(Lar2barArea[0],l2BarAreaHist)
    HistFilling(Lar3barArea[0],l3BarAreaHist)
    HistFilling(BkBeamPanArea[0],BkBeampanelAreaHist)
    HistFilling(FrBeamPanArea[0],FrBeampanelAreaHist)
    HistFilling(TpFrontCospArea[0],TpFrontPanelAreaHist)
    HistFilling(TpBackCospArea[0],TpBackPanelAreaHist)

    c1.cd(1)
    l0BarAreaHist.Draw()
    c1.cd(2)
    #draw with differe colors and draw beam panel NPE disgtribution
    l1BarAreaHist.Draw()
    c1.cd(3)
    l2BarAreaHist.Draw()
    c1.cd(4)
    l3BarAreaHist.Draw()
    c1.cd(5)
    BkBeampanelAreaHist.Draw()
    c1.cd(6)
    FrBeampanelAreaHist.Draw()
    c1.cd(7)
    TpFrontPanelAreaHist.Draw()
    c1.cd(8)
    TpBackPanelAreaHist.Draw()


    c1.SaveAs("Histtest.png")
    
    
    print(len(npeArr))

    print(typeArr)
    print(layerArr)
    NpeT = 20
    MaxPTimeArr,MAXNPEarr,arr=filling(typeArr[0],layerArr[0],rowArr[0],columnArr[0],npeArr[0],timeArr[0],NpeT)
    #ColumnarrST,ROWarrST=findTrack(arr)
    ColumnarrST,ROWarrST=findTackWeight(MAXNPEarr)
    print(f"ColumnarrST {ColumnarrST}") 
    print(f"ROWarrST {ROWarrST}") 
    

    #plot the muon track (hard code version)

    #"""
    for column,row in zip(ColumnarrST,ROWarrST):
        column = [x + 0.5 for x in column]
        row = [x + 0.5 for x in row]
        #print(f"track ColumnarrST {column}") 
        #print(f"track ROWarrST {row}") 
        
        plt.plot(column, row, color='red')
    #"""
    
    
    #display the the max NPE for each channel
    
    for row in range(5):
        for column in range(22):
            if MAXNPEarr[row,column] > NpeT:
                MaxNPEText = plt.text(column,4-row,f"{MAXNPEarr[row,column]:.0e}", color="red",fontsize=8)
                PulseTimeMText = plt.text(column,4-row + 0.5,f"{MaxPTimeArr[row,column]:.3e}ns", color="red",fontsize=8)
    
    #outline the panel

    # Get the current axes
    ax = plt.gca()

    #beam panels have the red outline
    beamF = patches.Rectangle((0, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none')
    beamB = patches.Rectangle((21, 0), 1, 1, linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(beamF)
    ax.add_patch(beamB)
    #cosmic panel have the white outline
    COS70 = patches.Rectangle((1, 0), 1, 4, linewidth=2, edgecolor='white', facecolor='none')
    COS72 = patches.Rectangle((6, 0), 1, 4, linewidth=2, edgecolor='white', facecolor='none')
    COS71 = patches.Rectangle((11, 0), 1, 4, linewidth=2, edgecolor='white', facecolor='none')
    COS73 = patches.Rectangle((16, 0), 1, 4, linewidth=2, edgecolor='white', facecolor='none')
    Cos68 = patches.Rectangle((2, 4), 9, 1, linewidth=2, edgecolor='white', facecolor='none')
    Cos69 = patches.Rectangle((12, 4), 9, 1, linewidth=2, edgecolor='white', facecolor='none')
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


    


    plt.imshow(arr, cmap='viridis', origin='upper', extent=[0, 22, 0, 5]) 
    plt.colorbar(label= f'number of hits above {NpeT} pulse NPE')
    #plt.grid(True) #if possible can I create the grid manually to outline the position of panel?
    #plt.show()


    #plot the 3d lego plot with number pulse above NPE 
    fig = plt.figure(figsize=(8, 3))
    ax1 = fig.add_subplot(121, projection='3d')
    row,column = arr.shape
    for r in range(row):
        for c in range(column):
            NumHits = arr[r][c]
            if NumHits > 0:
                if (c <= 1) or (r==0) or (c == 6) or (c == 11) or (c == 16) or (c==21):
                    ax1.bar3d(c, 4-r, 0, 1, 1, NumHits, color='red') #panel
                

                else:
                    ax1.bar3d(c, 4-r, 0, 1, 1, NumHits, color='green') #bar

    plt.show()