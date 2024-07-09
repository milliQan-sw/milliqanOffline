"""
select sim and offline when doing the demonstration

with cosmic muon events

Follow david's suggestion find the sample muon event


Todo
When making the straight track, it should add an extra offset factor -0.5
"""


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import hist
import awkward as ak
import ROOT as r

def filling(typeArr,layerArr,rowArr,columnArr,npeArr,NpeT):
    block = np.zeros((5, 22))
    for type,layer,row,column,npe in zip (typeArr,layerArr,rowArr,columnArr,npeArr):
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
    #print(block)
    return block

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
    #uptree = uproot.open("/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run1190.1_v34.root:t") event 472 is a sample event
    uptree = uproot.open("/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run1500.1_v35.root:t")
    branches = uptree.arrays(["type","layer","row","column","nPE","event","area"], entry_stop=100000)

    EventNum = int(sys.argv[1])
    typeArr= branches["type"][branches["event"]==EventNum]
    layerArr = branches["layer"][branches["event"]==EventNum]
    rowArr = branches["row"][branches["event"]==EventNum]
    columnArr = branches["column"][branches["event"]==EventNum]
    npeArr = branches["nPE"][branches["event"]==EventNum]

    
    EventArr = branches[branches["event"]==EventNum]
    Lar0barNpe=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 0)]
    Lar1barNpe=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 1)]
    Lar2barNpe=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 2)]
    Lar3barNpe=EventArr["area"][(EventArr["type"] == 0) &  (EventArr["layer"] == 3)]
    FrBeamPanNpe=EventArr["area"][(EventArr["type"] == 2) &  (EventArr["layer"] == -1)]
    BkBeamPanNpe=EventArr["area"][(EventArr["type"] == 2) &  (EventArr["layer"] == 4)]
    TpFrontCosp=EventArr["area"][(EventArr["row"] == 4)]
    TpBackCosp=EventArr["area"][(EventArr["row"] == 4)]
    print(f"TpBackCosp:{TpBackCosp}")
    print(f"TpBackCosp area :{EventArr['area'][(EventArr['row'] == 4)]}")
    c1 = r.TCanvas("c1","c1",800,1000)
    c1.Divide(2,4)

    l0BarNpeHist = r.TH1F("l0BarNpe","layer 0 bar npe",100,0,1000000)
    l1BarNpeHist = r.TH1F("l1BarNpe","layer 1 bar npe",100,0,1000000)
    l2BarNpeHist = r.TH1F("l2BarNpe","layer 2 bar npe",100,0,1000000)
    l3BarNpeHist = r.TH1F("l3BarNpe","layer 3 bar npe",100,0,1000000)
    FrBeampanelNpeHist = r.TH1F("FbeamPanel","Front beam panel npe",100,0,1000000)
    BkBeampanelNpeHist = r.TH1F("BkeamPanel","Back beam panel npe",100,0,1000000)
    TpFrontPanelNpeHist = r.TH1F("TpFrontCosPanel","top front cos panel npe",100,0,1000000)
    TpBackPanelNpeHist = r.TH1F("BkFrontCosPanel","Back front cos panel npe",100,0,1000000)


    print(Lar0barNpe[0])

    def HistFilling(data, hist):
        for subdata in data:
            hist.Fill(subdata)

    HistFilling(Lar0barNpe[0],l0BarNpeHist)
    HistFilling(Lar1barNpe[0],l1BarNpeHist)
    HistFilling(Lar2barNpe[0],l2BarNpeHist)
    HistFilling(Lar3barNpe[0],l3BarNpeHist)
    HistFilling(BkBeamPanNpe[0],BkBeampanelNpeHist)
    HistFilling(FrBeamPanNpe[0],FrBeampanelNpeHist)
    HistFilling(TpFrontCosp[0],TpFrontPanelNpeHist)
    HistFilling(TpBackCosp[0],TpBackPanelNpeHist)

    c1.cd(1)
    l0BarNpeHist.Draw()
    c1.cd(2)
    #draw with differe colors and draw beam panel NPE disgtribution
    l1BarNpeHist.Draw()
    c1.cd(3)
    l2BarNpeHist.Draw()
    c1.cd(4)
    l3BarNpeHist.Draw()
    c1.cd(5)
    BkBeampanelNpeHist.Draw()
    c1.cd(6)
    FrBeampanelNpeHist.Draw()
    c1.cd(7)
    TpFrontPanelNpeHist.Draw()
    c1.cd(8)
    TpBackPanelNpeHist.Draw()


    c1.SaveAs("Histtest.png")
    
    
    print(len(npeArr))

    print(typeArr)
    print(layerArr)
    NpeT = 20
    arr=filling(typeArr[0],layerArr[0],rowArr[0],columnArr[0],npeArr[0],NpeT)
    ColumnarrST,ROWarrST=findTrack(arr)
    print(f"ColumnarrST {ColumnarrST}") 
    print(f"ROWarrST {ROWarrST}") 
    
    for column,row in zip(ColumnarrST,ROWarrST):
        column = [x + 0.5 for x in column]
        row = [x + 0.5 for x in row]
        #print(f"track ColumnarrST {column}") 
        #print(f"track ROWarrST {row}") 
        
        plt.plot(column, row, color='red')
    
    


    plt.imshow(arr, cmap='viridis', origin='upper', extent=[0, 22, 0, 5]) 
    plt.colorbar(label='Height')
    plt.grid(True)
    #plt.show()


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