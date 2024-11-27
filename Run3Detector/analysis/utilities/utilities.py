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