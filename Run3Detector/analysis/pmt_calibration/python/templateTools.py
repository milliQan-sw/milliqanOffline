#!/usr/bin/env python3
import numpy as np

def averageOfLists(otherLists : list ) -> list:
    """Find the average item by item in a list of lists:
    Ex. averageOfLists([[1,2,3],[4,5,6]]) -> [5/2, 7/2, 9/2]"""

    sumList =  [sum(x) for x in zip(*otherLists)]
    print(len(otherLists))
    return [ x/len(otherLists) for x in sumList ]

def movingAverage(inputList : list, window: int) -> list:
    """ Take moving average of list"""
    return np.convolve(inputList, np.ones(window)/window, mode='valid')
