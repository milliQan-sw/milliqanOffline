#!/usr/bin/env python3

# Input a list of lists
def averageOfLists(otherLists : list ) -> list:
    sumList =  [sum(x) for x in zip(*otherLists)]
    print(len(otherLists))
    return [ x/len(otherLists) for x in sumList ]
