import ROOT as r
import os

directory = '/store/user/milliqan/trees/v34/1000/'

mychain = r.TChain('t')

for ifile, filename in enumerate(os.listdir(directory)):
    #if ifile > 100: break
    if not filename.endswith('root'): continue
    print(filename)
    mychain.Add(directory+filename)



outputName = 'MilliQan_Run1000_v34_skim.root'

print("There are {} events in the chain".format(mychain.GetEntriesFast()))

r.gROOT.LoadMacro("myLooper.C")

mylooper = r.myLooper(mychain)

mylooper.Loop(outputName)
