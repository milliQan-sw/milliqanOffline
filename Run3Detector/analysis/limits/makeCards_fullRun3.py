import numpy as np
import sys
import os
import pandas as pd

def makeCard(SR1sigE,SR1bkgE,SR2sigE,SR2bkgE,SR1sigL,SR1bkgL,SR2sigL,SR2bkgL,SR1sbE,SR1sfE,SR2sbE,SR2sfE,SR1sbL,SR1sfL,SR2sbL,SR2sfL,k_down,k_up):
    cardString = """
 imax 4  number of channels 
 jmax *  number of backgrounds 
 kmax *  number of nuisance parameters (sources of systematical uncertainties) 
 ------------ 
 bin SR1early SR2early SR1late SR2late
 observation 0 2 0 0
 ------------ 
 bin              SR1early   SR1early   SR2early  SR2early SR1late SR1late SR2late SR2late
 process          mCP        bkgd       mCP       bkgd     mCP     bkgd    mCP     bkgd
 process          0          1          0         1        0       1       0       1
 rate             {0}        {1}        {2}       {3}      {4}     {5}     {6}     {7}
 ------------ 
 SR1earlyBkg gmN {8}    -    {9}        -         -        -       -       -       -
 SR2earlyBkg gmN {10}   -    -          -         {11}     -       -       -       -
 SR1lateBkg gmN  {12}   -    -          -         -        -       {13}    -       -
 SR2lateBkg gmN  {14}   -    -          -         -        -       -       -       {15}
 sigErr lnN      {16}/{17}   -       {16}/{17}    -      {16}/{17}  -    {16}/{17}  -         estimated error of signal lnN = lognormal 
""".format(SR1sigE,SR1bkgE,SR2sigE,SR2bkgE,SR1sigL,SR1bkgL,SR2sigL,SR2bkgL,SR1sbE,SR1sfE,SR2sbE,SR2sfE,SR1sbL,SR1sfL,SR2sbL,SR2sfL,k_down,k_up)
    return cardString

SR1_input_file = "weightsSR1.txt"
SR2_input_file = "weightsSR2.txt"

SR1_sigMC = np.loadtxt(SR1_input_file, skiprows=1)
SR2_sigMC = np.loadtxt(SR2_input_file, skiprows=1)

masses = SR1_sigMC[:, 0]
charges = SR1_sigMC[:, 1]
SR1_MC_yields = SR1_sigMC[:,2]
SR2_MC_yields = SR2_sigMC[:,2]

misalignment = 0.88
lumiE = 124.73
lumiL = 180   #Remaining run 3 expectation
scaleE = lumiE/140 * misalignment
scaleL = lumiL/140
SR1_MC_yieldsE = np.round(SR1_MC_yields*scaleE,3)
SR2_MC_yieldsE = np.round(SR2_MC_yields*scaleE,3)
SR1_MC_yieldsL = np.round(SR1_MC_yields*scaleL,3)
SR2_MC_yieldsL = np.round(SR2_MC_yields*scaleL,3)

SR1_obs = 0
SR2_obs = 0

#sb = sideband, sf = scale factor (B/C regions), E = early (124/fb data), L = late (remaining 180/fb)
SR1sbE = 3
SR1sfE = round(5.0/152.0,4)
SR2sbE = 13
SR2sfE = round(81.0/1203.0,4)
SR1bkgE = round(SR1sbE*SR1sfE,3)
SR2bkgE = round(SR2sbE*SR2sfE,3)

#Scaling sidebands and scalefactors for rest of run 3
SR1sbL = round(SR1sbE * lumiL/lumiE)
SR2sbL = round(SR2sbE * lumiL/lumiE)
SR1bkgL = round(SR1bkgE*(lumiL/lumiE)/10,4)   #Optimistic: factor of 10 less background
SR2bkgL = round(SR2bkgE*(lumiL/lumiE)/10,4)
SR1sfL = round(SR1bkgL/SR1sbL,4) 
SR2sfL = round(SR2bkgL/SR2sbL,4)

outputDir = sys.argv[1]
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

systs = pd.read_csv('syst_uncs.csv')

for index, mass in enumerate(masses):
    charge = charges[index]
    if(SR1_MC_yieldsE[index] < 0.01 and SR2_MC_yieldsE[index] < 0.01): continue
    if(SR1_MC_yieldsE[index] > 100 or SR2_MC_yieldsE[index] > 100): continue
    if(SR1_MC_yieldsL[index] < 0.01 and SR2_MC_yieldsL[index] < 0.01): continue
    if(SR1_MC_yieldsL[index] > 100 or SR2_MC_yieldsL[index] > 100): continue
    print(mass,charge,SR1_MC_yieldsE[index], SR2_MC_yieldsE[index], SR2_MC_yieldsL[index], SR2_MC_yieldsL[index])
    cardName = "signalCardMass{0}Charge{1}.txt".format(str(mass).replace(".","p"),str(charge).replace(".","p"))
    
    idx = (systs['mass'] - mass).abs().argmin()
    systrow = systs.iloc[idx]
    up = systrow["up_unc"]
    down = systrow["down_unc"]
    k_up = round(1 + up,3)
    k_down = round(1 - down,3)
    
    card = makeCard(SR1_MC_yieldsE[index],SR1bkgE,SR2_MC_yieldsE[index],SR2bkgE,SR1_MC_yieldsL[index],SR1bkgL,SR2_MC_yieldsL[index],SR2bkgL,SR1sbE,SR1sfE,SR2sbE,SR2sfE,SR1sbL,SR1sfL,SR2sbL,SR2sfL,k_down,k_up)

    with open(outputDir+"/"+cardName,'w') as f:
        f.write(card)

