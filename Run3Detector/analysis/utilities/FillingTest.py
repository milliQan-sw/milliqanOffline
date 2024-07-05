"""
select sim and offline when doing the demonstration

with cosmic muon events

Follow david's suggestion find the sample muon event


Todo
When making the straight track, it should add an extra offset factor -0.5
"""


import numpy as np
import matplotlib.pyplot as plt


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
                fillingColumn_offset = 0 
                rowoffset = 21
        #panel (cosmic)

        

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
                rowTempL0.append(row+1)
                columnTempL0.append(column+2)
                straightLineArrL0 += 1

            #layer one
            if arr[row+1][column+7] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL1.append(row+1)
                columnTempL1.append(column+7)
                straightLineArrL1 += 1
            
            #layer two
            if arr[row+1][column+12] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL2.append(row+1)
                columnTempL2.append(column+12)
                straightLineArrL2 += 1
            
            #layer three
            if arr[row+1][column+17] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL3.append(row+1)
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
            ROWarrST.append([1,2,3,4])
    
    for column in [5,10,15,20]:
        if (arr[1][column] >= 1) and (arr[2][column-1] >= 1) and (arr[3][column-2] >= 1) and (arr[4][column-3] >= 1):
            ColumnarrST.append([column,column-1,column-2,column-3])
            ROWarrST.append([1,2,3,4])

    #shifting to the right
    #shift1Column = np.array([])
    #shift1Row = np.array([])
    for column in [2,3,4,7,8,9,12,13,14,17,18,19]:
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column] >= 1) and (arr[4][column+1] >= 1):
            ColumnarrST.append([column,column,column,column+1])
            ROWarrST.append([1,2,3,4])

        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column+1] >= 1) and (arr[4][column+1] >= 1):
            ColumnarrST.append([column,column,column+1,column+1])
            ROWarrST.append([1,2,3,4])

        if (arr[1][column] >= 1) and (arr[2][column+1] >= 1) and (arr[3][column+1] >= 1) and (arr[4][column+1] >= 1):
            ColumnarrST.append([column,column+1,column+1,column+1])
            ROWarrST.append([1,2,3,4])

    for column in [2,3,7,8,12,13,17,18]:  
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column+1] >= 1) and (arr[4][column+2] >= 1):
            ColumnarrST.append([column,column,column+1,column+2])
            ROWarrST.append([1,2,3,4])

        if (arr[1][column] >= 1) and (arr[2][column+1] >= 1) and (arr[3][column+2] >= 1) and (arr[4][column+2] >= 1):
            ColumnarrST.append([column,column+1,column+2,column+2])
            ROWarrST.append([1,2,3,4])

    #shifting to the left
    for column in [3,4,5,8,9,10,13,14,15,18,19,20]:
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column] >= 1) and (arr[4][column-1] >= 1):
            ColumnarrST.append([column,column,column,column-1])
            ROWarrST.append([1,2,3,4])

        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column-1] >= 1) and (arr[4][column-1] >= 1):
            ColumnarrST.append([column,column,column-1,column-1])
            ROWarrST.append([1,2,3,4])

        if (arr[1][column] >= 1) and (arr[2][column-1] >= 1) and (arr[3][column-1] >= 1) and (arr[4][column-1] >= 1):
            ColumnarrST.append([column,column-1,column-1,column-1])
            ROWarrST.append([1,2,3,4])
        
    for column in [4,5,9,10,14,15,19,20]: 
        if (arr[1][column] >= 1) and (arr[2][column] >= 1) and (arr[3][column-1] >= 1) and (arr[4][column-2] >= 1):
            ColumnarrST.append([column,column,column-1,column-2])
            ROWarrST.append([1,2,3,4])

        if (arr[1][column] >= 1) and (arr[2][column-1] >= 1) and (arr[3][column-2] >= 1) and (arr[4][column-2] >= 1):
            ColumnarrST.append([column,column-1,column-2,column-2])
            ROWarrST.append([1,2,3,4])

    return ColumnarrST,ROWarrST


if __name__ == "__main__":
    import uproot
    #uptree = uproot.open("/Users/haoliangzheng/CERN_ana/MilliQan_Run1500.11_v35.root:t")
    uptree = uproot.open("/Users/haoliangzheng/CERN_ana/EventDisplay/MilliQan_Run1190.1_v34.root:t")
    branches = uptree.arrays(["type","layer","row","column","nPE","event"], entry_stop=100000)
    typeArr= branches["type"][branches["event"]==472]
    layerArr = branches["layer"][branches["event"]==472]
    rowArr = branches["row"][branches["event"]==472]
    columnArr = branches["column"][branches["event"]==472]
    npeArr = branches["nPE"][branches["event"]==472]
    print(len(npeArr))

    print(typeArr)
    print(layerArr)
    NpeT = 20
    arr=filling(typeArr[0],layerArr[0],rowArr[0],columnArr[0],npeArr[0],NpeT)
    ColumnarrST,ROWarrST=findTrack(arr)
    print(f"ColumnarrST {ColumnarrST}") 
    print(f"ROWarrST {ROWarrST}") 

    for column,row in zip(ColumnarrST,ROWarrST):
        plt.plot(column, row, color='red')



    plt.imshow(arr, cmap='viridis', origin='upper', extent=[0, 22, 0, 5]) 
    plt.colorbar(label='Height')
    plt.grid(True)
    plt.show()
