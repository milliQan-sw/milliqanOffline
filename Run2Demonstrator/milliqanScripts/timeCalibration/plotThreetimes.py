#!/usr/local/bin/python

import ROOT as r
import pickle
import os,sys
import pandas as pd
r.gROOT.SetBatch(True)
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


threetimes = pickle.load(open('threetimes.pkl'))

threetimes = np.array(threetimes)
deltaTimeFromFits = []
for row in threetimes:
    x = [1,2,3]
    # A = np.vstack([x, np.ones(len(x))]).T
    y = [0,row[1]-row[0],row[2]-row[0]]
    plt.plot(x[1:],y[1:])
    # m, c = np.linalg.lstsq(A, y)[0]
    # # w = [1./3.,1./3.,1./3.]
    # # result = np.polyfit(x,y,1,w=w)
    # slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    #
    # deltaTimeFromFit = slope*2
    # print row
    # if row[1] > (row[0]+row[1])/2 - 3:
    #     if row[1] < (row[0]+row[1])/2 + 3:
    #         deltaTimeFromFits.append(deltaTimeFromFit)


# plt.hist(threetimes[:,2] - threetimes[:,0],bins=20,range=(0,20),histtype='step')
# plt.hist(deltaTimeFromFits,bins=20,range=(0,20),histtype='step')
plt.show()

