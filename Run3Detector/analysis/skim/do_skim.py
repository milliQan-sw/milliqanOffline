import ROOT as r
import os

directory = '/store/user/milliqan/trees/v35/1100/'

mychain = r.TChain('t')

for ifile, filename in enumerate(os.listdir(directory)):
    #if ifile > 100: break
    if not filename.endswith('root'): continue
    print(filename)
    fin = r.TFile.Open(directory+filename)
    if fin.IsZombie(): 
        print("File {} is a zombie".format(filename))
        fin.Close()
        continue
    fin.Close()
    mychain.Add(directory+filename)



outputName = 'MilliQan_Run1100_v35_skim.root'

print("There are {} events in the chain".format(mychain.GetEntriesFast()))

r.gROOT.LoadMacro("myLooper.C")

mylooper = r.myLooper(mychain)

mylooper.Loop(outputName)
