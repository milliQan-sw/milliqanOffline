import os
import ROOT as r

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

    # Combine and convert to float
    return float(f"{integer_part}.{fractional_part}")

if __name__ == "__main__":

    beam = True
    skim = False
    sim = True 
    qualityLevel = 'override'
    maxEvents = None

    point_map = {0.1: [0.005, 1e-4], 0.3: [0.005, 1e-4], 0.35: [0.005, 1e-4], 0.4: [0.007, 1e-4], 0.5: [0.007, 1e-4], 0.7: [0.007, 1e-4], 0.9: [0.007, 1e-4], 
                 1: [0.007, 1e-4], 1.3: [0.007, 1e-4], 1.5: [0.06, 1e-4], 1.7: [0.06, 1e-4], 2: [0.06, 1e-2], 2.3: [0.06, 1e-2], 2.5: [0.06, 1e-2], 2.7: [0.06, 1e-2], 
                 3: [0.06, 1e-2], 3.5: [0.06, 1e-2], 3.7: [0.06, 1e-2], 4: [0.1, 1e-2], 4.5: [0.1, 1e-2], 4.7: [0.1, 1e-2],
                 5: [0.1, 1e-2], 5.5: [0.1, 1e-2], 6: [0.1, 1e-2], 6.5: [0.1, 1e-2], 7: [0.1, 1e-2], 8: [0.1, 1e-2], 9: [0.1, 5e-2], 10: [0.1, 5e-2], 
                 12: [0.1, 5e-2], 15: [0.1, 5e-2], 17: [0.1, 5e-2], 20: [0.1, 5e-2], 25: [0.1, 5e-2], 27: [0.1, 5e-2], 30: [0.1, 5e-2], 
                 33: [0.1, 5e-2], 35: [0.1, 5e-2], 40: [0.1, 5e-2] 
                }

    dataDir = '/eos/experiment/milliqan/sim/bar/signal/trees/'

    info_out = open('signalCutFlowInfo.txt', 'w+')

    processedFiles = 0

    for ifile, filename in enumerate(os.listdir(dataDir)):

        #if ifile > 2: break

        if not filename.endswith('root'):
            continue

        inputFile = '/'.join([dataDir, filename])
        
        charge_name = filename.split('_')[-1].replace('.root', '')
        mass_name = filename.split('_')[-2]
        outputFile = 'bgCutFlow_{}_{}.root'.format(charge_name, mass_name)

        mass = mass_to_float(mass_name)
        charge = charge_to_float(charge_name)

        if charge > point_map[mass][0] or charge < point_map[mass][1]: continue

        print("iFile: {}, Mass: {}, Charge: {}".format(processedFiles, mass, charge))

        cmd = 'python3 backgroundCutFlow.py {} {} {} {} {} {} {}'.format(beam, skim, sim, outputFile, qualityLevel, inputFile, maxEvents)

        print(cmd)
        os.system(cmd)

        fin = r.TFile.Open(outputFile, 'READ')
        h_eventCutFlow = fin.Get('eventCutFlow')
        nBins = h_eventCutFlow.GetNbinsX()
        totalEvents = h_eventCutFlow.GetBinContent(1)
        passingEvents = h_eventCutFlow.GetBinContent(nBins)

        ratio = passingEvents/totalEvents
        print("Total events: {}, Total passing: {} ({})".format(totalEvents, passingEvents, ratio))
        info_out.write(f'{totalEvents} {passingEvents} {ratio}\n')

        fin.Close

        processedFiles += 1
    
    info_out.close()

