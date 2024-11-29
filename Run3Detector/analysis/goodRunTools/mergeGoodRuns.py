
import pandas as pd 
import numpy as np 
import awkward as ak 
import ROOT as r 
import os
import json
import sys
from checkMatching import fileChecker


#this file is used to merge all good runs and checks lists created by grid jobs

if __name__ == "__main__":
    
    #input directory will all good run lists
    dataDir = '/data/users/milliqan/log/goodRunLists/currentVersion/11_27_10/'

    goodRuns = pd.DataFrame()
    checks = pd.DataFrame()

    for filename in os.listdir(dataDir):
        if filename.endswith('.json') and filename.startswith('checks_'):
            fin = open(dataDir+filename)
            data = json.load(fin)
            tmp = pd.DataFrame(data['data'], columns=data['columns'])
            checks = pd.concat([checks, tmp])
        if filename.endswith('.json') and filename.startswith('goodRuns_'):
            print(filename)
            fin = open(dataDir+filename)
            data = json.load(fin)
            tmp = pd.DataFrame(data['data'], columns=data['columns'])
            goodRuns = pd.concat([goodRuns, tmp])        

    goodRuns = goodRuns.sort_values(by=['run', 'file'])
    checks = checks.sort_values(by=['run', 'file'])

    goodRuns.to_json('goodRunsMerged.json', orient = 'split', compression = 'infer', index = 'true')
    checks.to_json('checksMerged.json', orient = 'split', compression = 'infer', index = 'true')

    checks.to_csv('checksMerged.csv')
