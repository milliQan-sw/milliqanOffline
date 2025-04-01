import os
import json
import ROOT as r
import pandas as pd

def mass_to_float(s):
    """
    Converts a string of the form 'mXpY' into a float.
    
    Args:
        s (str): The input string in the format 'mXpY', where X and Y are digits.
    
    Returns:
        float: The corresponding float value.
    """
    if not s.startswith("m") or "p" not in s:
        raise ValueError("Input string must be in the format 'mXpY'.")

    # Extract parts
    integer_part = s[1:s.index("p")]  # Part after 'm' and before 'p'
    fractional_part = s[s.index("p") + 1:]  # Part after 'p'

    # Combine and convert to float
    return float(f"{integer_part}.{fractional_part}")

def charge_to_float(s):
    """
    Converts a string of the form 'mXpY' into a float.
    
    Args:
        s (str): The input string in the format 'mXpY', where X and Y are digits.
    
    Returns:
        float: The corresponding float value.
    """
    if not s.startswith("c") or "p" not in s:
        raise ValueError("Input string must be in the format 'cXpY'.")

    # Extract parts
    integer_part = s[1:s.index("p")]  # Part after 'm' and before 'p'
    fractional_part = s[s.index("p") + 1:]  # Part after 'p'

    # Combine and convert to float?
    return float(f"{integer_part}.{fractional_part}")


if __name__ == "__main__":

    dataDir = '/data/user/mcarrigan/milliqan/bgCutFlow_signalSim_SR2_v6/'

    #fout = open('weightsSR2.txt', 'w+')

    #fout.write('mass\tcharge\tyield\n')

    df = pd.DataFrame(columns=["mass", "charge", "yield"])

    for filename in os.listdir(dataDir):
        if not filename.endswith('.root') or not filename.startswith('bgCutFlow'): continue

        mass_s = filename.split('_')[2]
        charge_s = filename.split('_')[3]

        print(filename, mass_s, charge_s)

        mass = mass_to_float(mass_s)
        charge = charge_to_float(charge_s)

        fin = r.TFile.Open('/'.join([dataDir, filename]), 'READ')
        weights = fin.Get('h_eventWeights')

        count = weights.GetBinContent(1) 
        weight = count* charge**2

        df.loc[len(df)] = [mass, charge, weight]
    
    df = df.sort_values(by=['mass', 'charge'])
    
    df.to_csv('weightsSR2.txt', sep=' ', index=False)
    #fout.close()

