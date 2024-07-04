import numpy as np
import matplotlib.pyplot as plt


def filling(typeArr,layerArr,rowArr,columnArr,npeArr,NpeT):
    block = np.zeros((5, 22))
    for type,layer,row,column,npe in zip (typeArr,layerArr,rowArr,columnArr,npeArr):
        #bar channel data filling
        if type == 0:

            if layer == 0:
                fillingColumn_offset = 2
                rowoffset = 4-row
            elif layer == 1:
                fillingColumn_offset = 7
                rowoffset = 4-row
            
            elif layer == 2:
                fillingColumn_offset = 11
                rowoffset = 4-row
            
            elif layer == 3:
                fillingColumn_offset = 16
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

    return block

def findTrack(arr):
    
    #straightLineArr = np.array([])
    ROWarrST = np.array([])
    ColumnarrST = np.array([])

    
    for column in range(4):
        straightLineArrL0 = 0
        straightLineArrL1 = 0
        straightLineArrL2 = 0
        straightLineArrL3 = 0


        rowTempL0 = np.array([])
        columnTempL0 = np.array([])

        rowTempL1 = np.array([])
        columnTempL1 = np.array([])


        rowTempL2 = np.array([])
        columnTempL2 = np.array([])


        rowTempL3 = np.array([])
        columnTempL3 = np.array([])
        for row in range(4):
            #layer zero
            if arr[column+2][row+1] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL0.append(row)
                columnTempL0.append(column)
                straightLineArrL0 += 1

            #layer one
            if arr[column+7][row+1] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL1.append(row)
                columnTempL1.append(column)
                straightLineArrL1 += 1
            
            #layer two
            if arr[column+12][row+1] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL2.append(row)
                columnTempL2.append(column)
                straightLineArrL2 += 1
            
            #layer three
            if arr[column+17][row+1] >= 1:
                #STDPath.append(arr[column+2][row+1])
                rowTempL3.append(row)
                columnTempL3.append(column)
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
        if (arr[column][1] >= 1) and (arr[column+1][2] >= 1) and (arr[column+2][3] >= 1) and (arr[column+3][4] >= 1):
            ColumnarrST.append[[column,column+1,column+2,column+3]]
            ROWarrST.append([1,2,3,4])
    
    for column in [2,7,12,17]:
        if (arr[column][4] >= 1) and (arr[column+1][3] >= 1) and (arr[column+2][2] >= 1) and (arr[column+3][1] >= 1):
            ColumnarrST.append[[column+2,column+3,column+4,column+5]]
            ROWarrST.append([4,3,2,1])

    #shifting to the right
    shift1Column = np.array([])
    shift1Row = np.array([])
    for column in [2,3,4,7,8,9,12,13,14,17,18,19]:
        if (arr[column][1] >= 1) and (arr[column][2] >= 1) and (arr[column][3] >= 1) and (arr[column+1][4] >= 1):
            ColumnarrST.append([column,column,column,column+1])
            ROWarrST.append([1,2,3,4])

        if (arr[column][1] >= 1) and (arr[column][2] >= 1) and (arr[column+1][3] >= 1) and (arr[column+1][4] >= 1):
            ColumnarrST.append([column,column,column+1,column+1])
            ROWarrST.append([1,2,3,4])

        if (arr[column][1] >= 1) and (arr[column+1][2] >= 1) and (arr[column+1][3] >= 1) and (arr[column+1][4] >= 1):
            ColumnarrST.append([column,column+1,column+1,column+1])
            ROWarrST.append([1,2,3,4])

    for column in [2,3,7,8,12,13,17,18]:  
        if (arr[column][1] >= 1) and (arr[column][2] >= 1) and (arr[column+1][3] >= 1) and (arr[column+2][4] >= 1):
            ColumnarrST.append([column,column,column+1,column+2])
            ROWarrST.append([1,2,3,4])

        if (arr[column][1] >= 1) and (arr[column+1][2] >= 1) and (arr[column+2][3] >= 1) and (arr[column+2][4] >= 1):
            ColumnarrST.append([column,column+1,column+2,column+2])
            ROWarrST.append([1,2,3,4])

    #shifting to the left
    for column in [3,4,5,8,9,10,13,14,15,18,19,20]:
        if (arr[column][1] >= 1) and (arr[column][2] >= 1) and (arr[column][3] >= 1) and (arr[column-1][4] >= 1):
            ColumnarrST.append([column,column,column,column-1])
            ROWarrST.append([1,2,3,4])

        if (arr[column][1] >= 1) and (arr[column][2] >= 1) and (arr[column-1][3] >= 1) and (arr[column-1][4] >= 1):
            ColumnarrST.append([column,column,column-1,column-1])
            ROWarrST.append([1,2,3,4])

        if (arr[column][1] >= 1) and (arr[column-1][2] >= 1) and (arr[column-1][3] >= 1) and (arr[column-1][4] >= 1):
            ColumnarrST.append([column,column-1,column-1,column-1])
            ROWarrST.append([1,2,3,4])
        
    for column in [4,5,9,10,14,15,19,20]: 
        if (arr[column][1] >= 1) and (arr[column][2] >= 1) and (arr[column-1][3] >= 1) and (arr[column-2][4] >= 1):
            ColumnarrST.append([column,column,column-1,column-2])
            ROWarrST.append([1,2,3,4])

        if (arr[column][1] >= 1) and (arr[column-1][2] >= 1) and (arr[column-2][3] >= 1) and (arr[column-2][4] >= 1):
            ColumnarrST.append([column,column-1,column-2,column-2])
            ROWarrST.append([1,2,3,4])

    return ColumnarrST,ROWarrST

