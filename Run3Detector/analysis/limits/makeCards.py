import numpy as np
import sys
import os
import pandas as pd

SR1_input_file = "weightsSR1.txt"
SR2_input_file = "weightsSR2.txt"

SR1_sigMC = np.loadtxt(SR1_input_file, skiprows=1)
SR2_sigMC = np.loadtxt(SR2_input_file, skiprows=1)

SR1_obs = 0
SR2_obs = 0

SR1_sideband = 3
SR1_scalefactor = round(5.0/152.0,4)
SR2_sideband = 13
SR2_scalefactor = round(81.0/1203.0,4)
SR1_bkg = round(SR1_sideband*SR1_scalefactor,3)
SR2_bkg = round(SR2_sideband*SR2_scalefactor,3)

print(SR2_sideband,SR2_scalefactor)
print(SR2_sideband*SR2_scalefactor)

def makeCard(SR1sigYield,SR1bkg,SR2sigYield,SR2bkg,SR1_sideband,SR1_scalefactor,SR2_sideband,SR2_scalefactor,k_down,k_up):
    cardString = """
 imax 2  number of channels 
 jmax *  number of backgrounds 
 kmax *  number of nuisance parameters (sources of systematical uncertainties) 
 ------------ 
 bin SR1 SR2 
 observation 0 2
 ------------ 
 bin              SR1   SR1   SR2  SR2
 process          mCP   bkgd  mCP  bkgd
 process          0     1     0    1
 rate             {0}   {1}   {2}  {3}
 ------------ 
 SR1BkgErr gmN {4}   -    {5}  -     -
 SR2BkgErr gmN {6}  -      -    -   {7}
 sigErr lnN      {8}/{9}   -    {8}/{9}  -  estimated error of signal lnN = lognormal 
""".format(SR1sigYield,SR1bkg,SR2sigYield,SR2bkg,SR1_sideband,SR1_scalefactor,SR2_sideband,SR2_scalefactor,k_down,k_up)
    return cardString



masses = SR1_sigMC[:, 0]
charges = SR1_sigMC[:, 1]
SR1_MC_yields = SR1_sigMC[:,2]
SR2_MC_yields = SR2_sigMC[:,2]

misalignment = 0.88
lumi = 124.73
#lumi = (124.73 + 180)   #Full run 3 expectation
scale = lumi/140 * misalignment
SR1_MC_yields = np.round(SR1_MC_yields*scale,3)
SR2_MC_yields = np.round(SR2_MC_yields*scale,3)
#Scaling sidebands and scalefactors
"""
SR1_sideband = round(SR1_sideband * 2.5)
SR2_sideband = round(SR2_sideband * 2.5)
SR1_bkg = round(SR1_bkg*(lumi/124.73)/10,4)
SR2_bkg = round(SR2_bkg*(lumi/124.73)/10,4)
SR1_scalefactor = round(SR1_bkg/SR1_sideband,4) 
SR2_scalefactor = round(SR2_bkg/SR2_sideband,4)
"""
outputDir = sys.argv[1]
if not os.path.exists(outputDir):
    os.makedirs(outputDir)

systs = pd.read_csv('syst_uncs.csv')

for index, mass in enumerate(masses):
    charge = charges[index]
    if(SR1_MC_yields[index] < 0.01 and SR2_MC_yields[index] < 0.01): continue
    if(SR1_MC_yields[index] > 100 or SR2_MC_yields[index] > 100): continue
    print(mass,charge,SR1_MC_yields[index], SR2_MC_yields[index])
    cardName = "signalCardMass{0}Charge{1}.txt".format(str(mass).replace(".","p"),str(charge).replace(".","p"))
    
    idx = (systs['mass'] - mass).abs().argmin()
    systrow = systs.iloc[idx]
    up = systrow["up_unc"]
    down = systrow["down_unc"]
    k_up = round(1 + up,3)
    k_down = round(1 - down,3)
    
    card = makeCard(SR1_MC_yields[index], SR1_bkg, SR2_MC_yields[index], SR2_bkg,SR1_sideband,SR1_scalefactor,SR2_sideband,SR2_scalefactor,k_down,k_up)

    with open(outputDir+"/"+cardName,'w') as f:
        f.write(card)


