import json
import pandas as pd
import matplotlib.pyplot as plt 
from datetime import datetime
import os

def loadLumis():
    lumis = pd.read_json('/eos/experiment/milliqan/Configs/mqLumis.json', orient = 'split', compression = 'infer')
    return lumis

def loadGoodRuns():
    goodRuns = pd.read_json('/eos/experiment/milliqan/Configs/goodRunsList.json', orient = 'split', compression = 'infer')
    return goodRuns

def loadRawLumis():
    rawLumis = pd.read_json('/eos/experiment/milliqan/Configs/rawLumis.json',  orient = 'split', compression = 'infer')
    return rawLumis


def plotLumis(lumis, x=0.4, y=0.7, var_x='stop', var_y='lumiSum', outDir=None, name=None, title=None, fill=True):

    plt.figure(figsize=(10, 6))  # width, height in inches

    if fill:
        plt.plot(lumis[var_x], lumis[var_y])
        plt.fill_between(lumis[var_x], lumis[var_y], color='lightblue', alpha=0.3)
    else:
        plt.scatter(lumis[var_x], lumis[var_y], marker='o', linestyle='-', color='blue', s=5)

    if not title is None:
        plt.title(title, fontsize=20)
    else:
        plt.title('Recorded Luminosity by MilliQan Bar Detector', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Recorded Luminosity (fb^-1)', fontsize=16)

    print(lumis.iloc[-1])
    totalLumi = round(lumis.iloc[-1][var_y], 2)
    textStr = 'Total Luminosity Recorded: {}'.format(totalLumi)

    if fill:
        plt.text(x, y, textStr+' $fb^{-1}$', fontsize=16, color='blue', ha='center', va='center', transform=plt.gca().transAxes)

    if outDir and name:
        plt.savefig(outDir+name+'.png')
        plt.yscale('log')
        plt.savefig(outDir+name+'_logy.png')

def plotMQRawTogether(lumis, raw, var_y1='lumiSum', var_y2='lumiSum', x=0.4, y=0.7, outDir=None, name=None, title=None, fill=True):

    plt.figure(figsize=(10, 6))  # width, height in inches

    if fill:
        plt.plot(raw['end_stable_beam'], raw[var_y2], color='red')
        plt.fill_between(raw['end_stable_beam'], raw[var_y2], color='red', alpha=0.3)
    else:
        plt.scatter(raw['end_stable_beam'], raw[var_y2], marker='o', linestyle='-', color='red', s=5)

    plt.title('Run3 LHC Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Stable Beam Luminosity (fb^-1)', fontsize=16)

    totalLumi = round(raw.iloc[-1][var_y2], 2)
    textStr = 'Total Delivered Luminosity: {}'.format(totalLumi)

    if fill:
        plt.text(x, y, textStr+' $fb^{-1}$', fontsize=16, color='red', ha='center', va='center', transform=plt.gca().transAxes)

    if fill:
        plt.plot(lumis['stop'], lumis[var_y1])
        plt.fill_between(lumis['stop'], lumis[var_y1], color='lightblue', alpha=0.3)
    else:
        plt.scatter(lumis['stop'], lumis[var_y1], marker='o', linestyle='-', color='blue', s=5)

    if not title is None:
        plt.title(title, fontsize=20)
    else:
        plt.title('Delivered Luminosity and MilliQan Recorded Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Recorded Luminosity (fb^-1)', fontsize=16)

    totalLumi = round(lumis.iloc[-1][var_y1], 2)
    textStr = 'Total Luminosity Recorded: {}'.format(totalLumi)
    print(textStr)

    if fill:
        plt.text(x, y-0.1, textStr+' $fb^{-1}$', fontsize=16, color='blue', ha='center', va='center', transform=plt.gca().transAxes)
    
    if outDir and name:
        plt.savefig(outDir+name+'.png')
        plt.yscale('log')
        plt.savefig(outDir+name+'_logy.png')


def plotAllGoodRuns(tight, med, loose, raw, x=0.4, y=0.7, outDir=None, name=None, title=None, fill=True):

    plt.figure(figsize=(10, 6))  # width, height in inches
    var_y1 = 'lumiSum'
    var_y2 = 'lumiSum'


    if fill:
        plt.plot(raw['end_stable_beam'], raw[var_y2], color='red')
        plt.fill_between(raw['end_stable_beam'], raw[var_y2], color='red', alpha=0.3)
    else:
        plt.scatter(raw['end_stable_beam'], raw[var_y2], marker='o', linestyle='-', color='red', s=5)

    plt.title('Run3 LHC Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Stable Beam Luminosity (fb^-1)', fontsize=16)

    totalLumi = round(raw.iloc[-1][var_y2], 2)
    textStr = 'Total Delivered Luminosity: {}'.format(totalLumi)

    if fill:
        plt.text(x, y, textStr+' $fb^{-1}$', fontsize=16, color='red', ha='center', va='center', transform=plt.gca().transAxes)

    if fill:
        plt.plot(tight['stop'], tight[var_y1], color='blue')
        plt.fill_between(tight['stop'], tight[var_y1], color='lightblue', alpha=0.3)
        plt.plot(med['stop'], med[var_y1], color='green')
        plt.fill_between(med['stop'], med[var_y1], color='lightgreen', alpha=0.3)
        plt.plot(loose['stop'], loose[var_y1], color='darkviolet')
        plt.fill_between(loose['stop'], loose[var_y1], color='darkviolet', alpha=0.3)
    else:
        plt.scatter(tight['stop'], tight[var_y1], marker='o', linestyle='-', color='blue', s=5)
        plt.scatter(med['stop'], med[var_y1], marker='o', linestyle='-', color='green', s=5)
        plt.scatter(loose['stop'], loose[var_y1], marker='o', linestyle='-', color='darkviolet', s=5)


    if not title is None:
        plt.title(title, fontsize=20)
    else:
        plt.title('Delivered Luminosity and MilliQan Recorded Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Recorded Luminosity (fb^-1)', fontsize=16)

    tightLumi = round(tight.iloc[-1][var_y1], 2)
    medLumi = round(med.iloc[-1][var_y1], 2)
    looseLumi = round(loose.iloc[-1][var_y1], 2)

    textStr = 'Good Run Luminosity'
    textStrTight = f"Tight: {tightLumi}"
    textStrMedium = f"Medium: {medLumi}"
    textStrLoose = f"Loose: {looseLumi}"

    print(textStr, textStrTight, textStrMedium, textStrLoose)

    if fill:
        plt.text(x, y-0.1, textStr, fontsize=16, color='black', ha='center', va='center', transform=plt.gca().transAxes)
        plt.text(x, y-0.2, textStrTight+' $fb^{-1}$', fontsize=16, color='blue', ha='center', va='center', transform=plt.gca().transAxes)
        plt.text(x, y-0.3, textStrMedium+' $fb^{-1}$', fontsize=16, color='green', ha='center', va='center', transform=plt.gca().transAxes)
        plt.text(x, y-0.4, textStrLoose+' $fb^{-1}$', fontsize=16, color='violet', ha='center', va='center', transform=plt.gca().transAxes)
    
    if outDir and name:
        plt.savefig(outDir+name+'.png')
        plt.yscale('log')
        plt.savefig(outDir+name+'_logy.png')


def plotRawLumis(raw, var_y='lumiSum', x=0.4, y=0.7, outDir=None, name=None, title=None, fill=True):

    plt.figure(figsize=(10, 6))  # width, height in inches

    if fill:
        plt.plot(raw['end_stable_beam'], raw[var_y], color='red')
        plt.fill_between(raw['end_stable_beam'], raw[var_y], color='red', alpha=0.3)
    else:
        plt.scatter(raw['end_stable_beam'], raw[var_y], marker='o', linestyle='-', color='red', s=5)

    if not title is None:
        plt.title(title, fontsize=20)
    else:
        plt.title('Run3 LHC Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Stable Beam Luminosity (fb^-1)', fontsize=16)

    totalLumi = round(raw.iloc[-1][var_y], 2)
    textStr = 'Total Delivered Luminosity: {}'.format(totalLumi)

    if fill:
        plt.text(x, y, textStr+' $fb^{-1}$', fontsize=16, color='red', ha='center', va='center', transform=plt.gca().transAxes)
    
    if outDir and name:
        plt.savefig(outDir+name+'.png')
        plt.yscale('log')
        plt.savefig(outDir+name+'_logy.png')

def plotFileOpenTimes(lumis, outDir=None):

    lumis['mqTime'] = (pd.to_datetime(lumis['stop']) - pd.to_datetime(lumis['start'])).dt.total_seconds()
    average_values = lumis.groupby('run')['mqTime'].mean()

    average_values = average_values.reset_index()

    #get only runs with >=10 files
    grouped = lumis.groupby('run')
    filtered_df = grouped.filter(lambda x: len(x) >= 10)
    selected = filtered_df.groupby('run')['mqTime'].mean()

    selected = selected.reset_index()

    plt.figure(figsize=(10, 6))
    plt.scatter(average_values['run'], average_values['mqTime'], marker='o', linestyle='-', color='red')
    plt.scatter(selected['run'], selected['mqTime'], marker='o', linestyle='-')
    plt.xlabel('Run')
    plt.ylabel('Average File Open Time in Run (Average 1k events/s)')
    plt.title('Average File Open Time vs. Run')
    plt.yscale('log')
    plt.grid(True)
    plt.legend(loc='upper left', labels=['All Runs', 'Runs >= 10 Files'], title='Legend', fontsize=12)


    if outDir:
        plt.savefig(outDir+'averageFileOpenTime.png')

    lumis['avgLumi'] = lumis['lumiEst'] / lumis['mqTime']

    avg = lumis.groupby('run')['avgLumi'].mean()
    filtered_df = grouped.filter(lambda x: len(x) >= 10)
    selected = filtered_df.groupby('run')['mqTime'].mean()

    selected = selected.reset_index()
    avg = avg.reset_index()

    plt.figure(figsize=(10, 6))
    plt.scatter(avg['run'], avg['avgLumi'], marker='o', linestyle='-', color='red')
    plt.scatter(selected['run'], selected['mqTime'], marker='o', linestyle='-')
    plt.xlabel('Run')
    plt.ylabel('Lumi/s')
    plt.title('Average Lumi per Second vs. Run')
    plt.yscale('log')
    plt.grid(True)
    plt.legend(loc='lower left', labels=['All Runs', 'Runs >= 10 Files'], title='Legend', fontsize=12)

    if outDir:
        plt.savefig(outDir+'averageLumiPerSecond.png')

if __name__ == "__main__":

    pltDir = '/home/milliqan/scratch0/milliqanOffline/Run3Detector/scripts/plots/'
    goodRunDir = pltDir + 'goodRuns/'
    rawLumiDir = pltDir + 'rawLumis/'
    perRunDir = pltDir + 'perRun/'
    totalLumiDir = pltDir + 'totalLumis/'

    if not os.path.exists(pltDir): os.mkdir(pltDir)
    if not os.path.exists(rawLumiDir): os.mkdir(rawLumiDir)
    if not os.path.exists(perRunDir): os.mkdir(perRunDir)
    if not os.path.exists(totalLumiDir): os.mkdir(totalLumiDir)

    print("Trying to get latest files")
    lumis = loadLumis() #mqLumis
    print("Loaded lumis")
    goodRuns = loadGoodRuns() #good runs list
    rawLumis = loadRawLumis() #cms oms lumi data

    ########################
    #organize mq lumis 
    #########################

    #filter out negative lumis for now
    lumis = lumis[lumis['lumiEst'] >= 0]

    #convert from pb to fb
    lumis['lumiEst'] = lumis['lumiEst'] / 1000

    #convert start and stop times to datetimes
    lumis['start'] = pd.to_datetime(lumis['start'])
    lumis['stop'] = pd.to_datetime(lumis['stop'])

    #make sure values are in chronological order
    lumis = lumis.sort_values(by='stop')

    #separate out by year
    lumis23 = lumis[lumis['start'].dt.year == 2023].copy()
    lumis24 = lumis[lumis['start'].dt.year == 2024].copy()

    #get cumulative sum of lumi
    lumis['lumiSum'] = lumis['lumiEst'].cumsum()
    lumis23['lumiSum'] = lumis23['lumiEst'].cumsum()
    lumis24['lumiSum'] = lumis24['lumiEst'].cumsum()

    #Per run lumis
    perRun = lumis.copy()
    perRun = perRun.groupby('run')['lumiEst'].sum()
    perRunTime = lumis.groupby('run')['stop'].first()
    perRun = perRun.reset_index()
    perRunTime = perRunTime.reset_index()
    perRun['stop'] = perRunTime['stop'] 

    ######################
    # Organize raw lumis
    #######################
    
    raw = rawLumis[rawLumis['delivered_lumi_stablebeams'] > 0]

    #convert from pb to fb
    raw['delivered_lumi_stablebeams'] = raw['delivered_lumi_stablebeams'] / 1000

    #convert start and end times to datetimes
    raw['start_stable_beam'] = pd.to_datetime(raw['start_stable_beam'])
    raw['end_stable_beam'] = pd.to_datetime(raw['end_stable_beam'])

    #make sure values are in chronological order
    raw = raw.sort_values(by='end_stable_beam')

    #get versions by year
    raw23 = raw[raw['start_stable_beam'].dt.year == 2023]
    raw24 = raw[raw['start_stable_beam'].dt.year == 2024]

    #get cumulative sum of lumi
    raw['lumiSum'] = raw['delivered_lumi_stablebeams'].cumsum()
    raw23['lumiSum'] = raw23['delivered_lumi_stablebeams'].cumsum()
    raw24['lumiSum'] = raw24['delivered_lumi_stablebeams'].cumsum()

    ###########################
    ## Make Good Run Selections
    ############################

    #select out runs passing goodRunsTight
    selected_rows = lumis.merge(goodRuns, on=['run', 'file'])
    selected_rows23 = lumis23.merge(goodRuns, on=['run', 'file'])
    selected_rows24 = lumis24.merge(goodRuns, on=['run', 'file'])

    selected_rowsTight = selected_rows[selected_rows['goodRunTight']==True]
    selected_rowsTight23 = selected_rows23[selected_rows23['goodRunTight']==True]
    selected_rowsTight24 = selected_rows24[selected_rows24['goodRunTight']==True]

    selected_rowsTight['lumiSum'] = selected_rowsTight['lumiEst'].cumsum()
    selected_rowsTight23['lumiSum'] = selected_rowsTight23['lumiEst'].cumsum()
    selected_rowsTight24['lumiSum'] = selected_rowsTight24['lumiEst'].cumsum()

    selected_rowsMed = selected_rows[selected_rows['goodRunMedium']==True]
    selected_rowsMed23 = selected_rows23[selected_rows23['goodRunMedium']==True]
    selected_rowsMed24 = selected_rows24[selected_rows24['goodRunMedium']==True]

    selected_rowsMed['lumiSum'] = selected_rowsMed['lumiEst'].cumsum()
    selected_rowsMed23['lumiSum'] = selected_rowsMed23['lumiEst'].cumsum()
    selected_rowsMed24['lumiSum'] = selected_rowsMed24['lumiEst'].cumsum()

    selected_rowsLoose = selected_rows[selected_rows['goodRunLoose']==True]
    selected_rowsLoose23 = selected_rows23[selected_rows23['goodRunLoose']==True]
    selected_rowsLoose24 = selected_rows24[selected_rows24['goodRunLoose']==True]

    selected_rowsLoose['lumiSum'] = selected_rowsLoose['lumiEst'].cumsum()
    selected_rowsLoose23['lumiSum'] = selected_rowsLoose23['lumiEst'].cumsum()
    selected_rowsLoose24['lumiSum'] = selected_rowsLoose24['lumiEst'].cumsum()

    ############################
    # Make Plots
    ###########################

    #plot all mq recorded lumi
    print("Plotting the total lumis", lumis.size, lumis24.size, lumis23.size)
    plotLumis(lumis, outDir=totalLumiDir, name='totalLumis')
    plotLumis(lumis24, outDir=totalLumiDir, name='totalLumis2024')
    plotLumis(lumis23, outDir=totalLumiDir, name='totalLumis2023')

    print("Plotting the lumis per file")
    plotLumis(lumis, var_y='lumiEst', outDir=perRunDir, name='LumisPerFile', fill=False)
    plotLumis(lumis24, var_y='lumiEst', outDir=perRunDir, name='LumisPerFile2024', fill=False)
    plotLumis(lumis23, var_y='lumiEst', outDir=perRunDir, name='LumisPerFile2023', fill=False)

    print("Plotting the lumis per run")
    plotLumis(perRun, var_x='run', var_y='lumiEst', outDir=perRunDir, name='LumisPerRun', fill=False)
    plotLumis(perRun, var_x='run', var_y='lumiEst', outDir=perRunDir, name='LumisPerRun2024', fill=False)
    plotLumis(perRun, var_x='run', var_y='lumiEst', outDir=perRunDir, name='LumisPerRun2023', fill=False)

    #plot mq recorded lumi w/ runs marked as good
    print("Plotting the good run lumis")
    plotLumis(selected_rowsTight, x=0.5, outDir=totalLumiDir, name='goodRunLumis', title='MilliQan Good Runs Recorded Luminosity')
    plotLumis(selected_rowsTight24, outDir=totalLumiDir, name='goodRunLumis2024', title='MilliQan Good Runs Recorded Luminosity 2024')
    plotLumis(selected_rowsTight23, outDir=totalLumiDir, name='goodRunLumis2023', title='MilliQan Good Runs Recorded Luminosity 2023')
   
    print("Plotting the good run lumis per file")     
    plotLumis(selected_rowsTight, var_y='lumiEst', x=0.5, outDir=perRunDir, name='goodRunLumisPerFile', title='MilliQan Good Runs Recorded Luminosity', fill=False)
    plotLumis(selected_rowsTight24, var_y='lumiEst', outDir=perRunDir, name='goodRunLumisPerFile2024', title='MilliQan Good Runs Recorded Luminosity 2024', fill=False)
    plotLumis(selected_rowsTight23, var_y='lumiEst', outDir=perRunDir, name='goodRunLumisPerFile2023', title='MilliQan Good Runs Recorded Luminosity 2023', fill=False)

    print("Plotting the good run lumis")
    plotLumis(selected_rowsMed, x=0.5, outDir=totalLumiDir, name='goodRunMedLumis', title='MilliQan Good Runs Recorded Luminosity')
    plotLumis(selected_rowsMed24, outDir=totalLumiDir, name='goodRunMedLumis2024', title='MilliQan Good Runs Recorded Luminosity 2024')
    plotLumis(selected_rowsMed23, outDir=totalLumiDir, name='goodRunMedLumis2023', title='MilliQan Good Runs Recorded Luminosity 2023')

    print("Plotting the good run lumis per file")
    plotLumis(selected_rowsMed, var_y='lumiEst', x=0.5, outDir=perRunDir, name='goodRunMedLumisPerFile', title='MilliQan Good Runs Recorded Luminosity', fill=False)
    plotLumis(selected_rowsMed24, var_y='lumiEst', outDir=perRunDir, name='goodRunMedLumisPerFile2024', title='MilliQan Good Runs Recorded Luminosity 2024', fill=False)
    plotLumis(selected_rowsMed23, var_y='lumiEst', outDir=perRunDir, name='goodRunMedLumisPerFile2023', title='MilliQan Good Runs Recorded Luminosity 2023', fill=False)

    print("Plotting the good run lumis")
    plotLumis(selected_rowsLoose, x=0.5, outDir=totalLumiDir, name='goodRunLooseLumis', title='MilliQan Good Runs Recorded Luminosity')
    plotLumis(selected_rowsLoose24, outDir=totalLumiDir, name='goodRunLooseLumis2024', title='MilliQan Good Runs Recorded Luminosity 2024')
    plotLumis(selected_rowsLoose23, outDir=totalLumiDir, name='goodRunLooseLumis2023', title='MilliQan Good Runs Recorded Luminosity 2023')

    print("Plotting the good run lumis per file")
    plotLumis(selected_rowsLoose, var_y='lumiEst', x=0.5, outDir=perRunDir, name='goodRunLooseLumisPerFile', title='MilliQan Good Runs Recorded Luminosity', fill=False)
    plotLumis(selected_rowsLoose24, var_y='lumiEst', outDir=perRunDir, name='goodRunLooseLumisPerFile2024', title='MilliQan Good Runs Recorded Luminosity 2024', fill=False)
    plotLumis(selected_rowsLoose23, var_y='lumiEst', outDir=perRunDir, name='goodRunLooseLumisPerFile2023', title='MilliQan Good Runs Recorded Luminosity 2023', fill=False)

    #plot raw delivered lumis
    plotRawLumis(raw, outDir=rawLumiDir, name='deliveredLumi')
    plotRawLumis(raw24, outDir=rawLumiDir, name='deliveredLumi2024')
    plotRawLumis(raw23, outDir=rawLumiDir, name='deliveredLumi2023')

    plotRawLumis(raw, var_y='delivered_lumi_stablebeams', outDir=rawLumiDir, name='deliveredLumiPerFill', fill=False)
    plotRawLumis(raw24, var_y='delivered_lumi_stablebeams', outDir=rawLumiDir, name='deliveredLumiPerFill2024', fill=False)
    plotRawLumis(raw23, var_y='delivered_lumi_stablebeams', outDir=rawLumiDir, name='deliveredLumiPerFill2023', fill=False)

    #plot mq recorded lumis w/ raw lumis
    plotMQRawTogether(lumis, raw, outDir=totalLumiDir, name='mqLumisPlusRaw')
    plotMQRawTogether(lumis24, raw24, outDir=totalLumiDir, name='mqLumisPlusRaw2024')
    plotMQRawTogether(lumis23, raw23, outDir=totalLumiDir, name='mqLumisPlusRaw2023')

    #plot mq good run lumi w/ raw lumis
    plotMQRawTogether(selected_rowsTight, raw, outDir=totalLumiDir, name='mqLumisGoodPlusRaw')
    plotMQRawTogether(selected_rowsTight24, raw24, outDir=totalLumiDir, name='mqLumisGoodPlusRaw2024')
    plotMQRawTogether(selected_rowsTight23, raw23, outDir=totalLumiDir, name='mqLumisGoodPlusRaw2023')

    plotMQRawTogether(selected_rowsMed, raw, outDir=totalLumiDir, name='mqLumisGoodMedPlusRaw')
    plotMQRawTogether(selected_rowsMed24, raw24, outDir=totalLumiDir, name='mqLumisGoodMedPlusRaw2024')
    plotMQRawTogether(selected_rowsMed23, raw23, outDir=totalLumiDir, name='mqLumisGoodMedPlusRaw2023')

    plotMQRawTogether(selected_rowsLoose, raw, outDir=totalLumiDir, name='mqLumisGoodLoosePlusRaw')
    plotMQRawTogether(selected_rowsLoose24, raw24, outDir=totalLumiDir, name='mqLumisGoodLoosePlusRaw2024')
    plotMQRawTogether(selected_rowsLoose23, raw23, outDir=totalLumiDir, name='mqLumisGoodLoosePlusRaw2023')

    plotAllGoodRuns(selected_rowsTight, selected_rowsMed, selected_rowsLoose, raw, outDir=totalLumiDir, name='mqLumisAllGoodRunsPlusRaw')

    #plot the average time files are open in runs and average lumis/s in runs
    plotFileOpenTimes(lumis, outDir=perRunDir)
