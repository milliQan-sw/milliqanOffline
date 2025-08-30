import pandas as pd
import shutil
import json
import ROOT as r

def getRunFile(filename):
    run = filename.split('Run')[1].split('.')[0]
    file = filename.split('.')[1].split('_')[0]
    return [int(run), int(file)]

def getSkimLumis(filelist):

    totalLumi = 0.0
    totalTime = 0.0
    for filename in filelist:
        #try:
        fin = r.TFile.Open(filename, 'READ')
        if fin.IsZombie():
            print(f"{filename} is a zombie skipping...")
            continue
        for key in fin.GetListOfKeys():
            if key.GetName() =='luminosity':
                this_lumi = key.GetTitle()
                totalLumi += float(this_lumi)
            if key.GetName() == 'runTime':
                this_time = key.GetTitle()
                totalTime += float(this_time)
        #except:
        #    print(f"Unable to get the lumi/time from file {filename}")
        #    continue

    print("Total luminosity {} and run time {}s".format(totalLumi, totalTime))
    
    return totalLumi, totalTime


def getLumiofFileList(filelist):

    inputFiles = [getRunFile(x.split('/')[-1]) for x in filelist]

    mqLumis = shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', 'mqLumis.json')
    lumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')

    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])

    myfiles = lumis[lumis.apply(lambda row: [int(row['run']), int(row['file'])] in inputFiles, axis=1)]

    totalLumi = myfiles['lumiEst'].sum()

    runTime = getRunTimes(myfiles)

    print("Running over {} files \n total of {} pb^-1 \n total run time {}s".format(len(filelist), totalLumi, runTime))

    return totalLumi, runTime

def getRunTimes(df):

    runTimes = df['stop'] - df['start']

    total_time = runTimes.sum()

    return total_time

def loadJson(jsonFile):
    fin = open(jsonFile)
    data = json.load(fin)
    lumis = pd.DataFrame(data['data'], columns=data['columns'])
    return lumis

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

#################################################################
################ condor function definitions ####################

def getFileList(filelist, job):

    with open(filelist, 'r') as fin:
        data = json.load(fin)

    mylist = data[job]

    return mylist

def extract_tar_file(tar_file='milliqanProcessing.tar.gz'):
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall()

##################################################################