import json
import pandas as pd
import matplotlib.pyplot as plt 
from datetime import datetime


def loadLumis():
    lumis = pd.read_json('/eos/experiment/milliqan/Configs/mqLumis.json', orient = 'split', compression = 'infer')
    return lumis

def loadGoodRuns():
    goodRuns = pd.read_json('/eos/experiment/milliqan/Configs/goodRunsList.json', orient = 'split', compression = 'infer')
    return goodRuns

def loadRawLumis():
    rawLumis = pd.read_json('/eos/experiment/milliqan/Configs/rawLumis.json',  orient = 'split', compression = 'infer')
    return rawLumis


def plotLumis(lumis, x=0.4, y=0.7, outDir=None, name=None, title=None):

    plt.figure(figsize=(10, 6))  # width, height in inches

    plt.plot(lumis['stop'], lumis['lumiSum'])
    if not title is None:
        plt.title(title, fontsize=20)
    else:
        plt.title('Recorded Luminosity by MilliQan Bar Detector', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Recorded Luminosity (fb^-1)', fontsize=16)

    plt.fill_between(lumis['stop'], lumis['lumiSum'], color='lightblue', alpha=0.3)


    totalLumi = round(lumis.iloc[-1]['lumiSum'], 2)
    textStr = 'Total Luminosity Recorded: {}'.format(totalLumi)

    plt.text(x, y, textStr+' $fb^{-1}$', fontsize=16, color='blue', ha='center', va='center', transform=plt.gca().transAxes)

    if outDir and name:
        plt.savefig(outDir+name+'.png')

def plotMQRawTogether(lumis, raw,  x=0.4, y=0.7, outDir=None, name=None, title=None):

    plt.figure(figsize=(10, 6))  # width, height in inches

    plt.plot(raw['end_stable_beam'], raw['lumiSum'], color='red')
    plt.title('Run3 LHC Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Stable Beam Luminosity (fb^-1)', fontsize=16)

    plt.fill_between(raw['end_stable_beam'], raw['lumiSum'], color='red', alpha=0.3)

    totalLumi = round(raw.iloc[-1]['lumiSum'], 2)
    textStr = 'Total Delivered Luminosity: {}'.format(totalLumi)

    plt.text(x, y, textStr+' $fb^{-1}$', fontsize=16, color='red', ha='center', va='center', transform=plt.gca().transAxes)

    plt.plot(lumis['stop'], lumis['lumiSum'])
    if not title is None:
        plt.title(title, fontsize=20)
    else:
        plt.title('Delivered Luminosity and MilliQan Recorded Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Recorded Luminosity (fb^-1)', fontsize=16)

    plt.fill_between(lumis['stop'], lumis['lumiSum'], color='lightblue', alpha=0.3)

    totalLumi = round(lumis.iloc[-1]['lumiSum'], 2)
    textStr = 'Total Luminosity Recorded: {}'.format(totalLumi)

    plt.text(x, y-0.1, textStr+' $fb^{-1}$', fontsize=16, color='blue', ha='center', va='center', transform=plt.gca().transAxes)
    
    if outDir and name:
        plt.savefig(outDir+name+'.png')

def plotRawLumis(raw, x=0.4, y=0.7, outDir=None, name=None, title=None):

    plt.figure(figsize=(10, 6))  # width, height in inches

    plt.plot(raw['end_stable_beam'], raw['lumiSum'], color='red')
    if not title is None:
        plt.title(title, fontsize=20)
    else:
        plt.title('Run3 LHC Luminosity', fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Stable Beam Luminosity (fb^-1)', fontsize=16)

    plt.fill_between(raw['end_stable_beam'], raw['lumiSum'], color='red', alpha=0.3)


    totalLumi = round(raw.iloc[-1]['lumiSum'], 2)
    textStr = 'Total Delivered Luminosity: {}'.format(totalLumi)

    plt.text(x, y, textStr+' $fb^{-1}$', fontsize=16, color='red', ha='center', va='center', transform=plt.gca().transAxes)
    
    if outDir and name:
        plt.savefig(outDir+name+'.png')

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

    pltDir = 'plots/'

    lumis = loadLumis() #mqLumis
    goodRuns = loadGoodRuns() #good runs list
    rawLumis = loadRawLumis() #cms oms lumi data

    ########################
    #organize mq lumis 
    #########################

    #filter out negative lumis for now
    lumis = lumis[lumis['lumiEst'] >= 0]

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

    #convert pb to fb
    lumis['lumiSum'] = lumis['lumiSum'] / 1000
    lumis23['lumiSum'] = lumis23['lumiSum'] / 1000
    lumis24['lumiSum'] = lumis24['lumiSum'] / 1000


    ######################
    # Organize raw lumis
    #######################
    
    raw = rawLumis[rawLumis['delivered_lumi_stablebeams'] > 0]

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


    #convert pb to fb
    raw['lumiSum'] = raw['lumiSum'] / 1000
    raw23['lumiSum'] = raw23['lumiSum'] / 1000
    raw24['lumiSum'] = raw24['lumiSum'] / 1000


    ###########################
    ## Make Good Run Selections
    ############################

    #select tight good runs
    goodRunsTight = goodRuns[goodRuns['goodRunTight']==True]

    #select out runs passing goodRunsTight
    selected_rows = lumis[lumis['run'].isin(goodRuns['run']) & lumis['file'].isin(goodRuns['file'])]
    selected_rows23 = lumis23[lumis23['run'].isin(goodRuns['run']) & lumis23['file'].isin(goodRuns['file'])]
    selected_rows24 = lumis24[lumis24['run'].isin(goodRuns['run']) & lumis24['file'].isin(goodRuns['file'])]


    ############################
    # Make Plots
    ###########################

    #plot all mq recorded lumi
    plotLumis(lumis, outDir=pltDir, name='totalLumis')
    plotLumis(lumis24, outDir=pltDir, name='totalLumis2024')
    plotLumis(lumis23, outDir=pltDir, name='totalLumis2023')


    #plot mq recorded lumi w/ runs marked as good
    plotLumis(selected_rows, x=0.5, outDir=pltDir, name='goodRunLumis', title='MilliQan Good Runs Recorded Luminosity')
    plotLumis(selected_rows24, outDir=pltDir, name='goodRunLumis2024', title='MilliQan Good Runs Recorded Luminosity 2024')
    plotLumis(selected_rows23, outDir=pltDir, name='goodRunLumis2023', title='MilliQan Good Runs Recorded Luminosity 2023')


    #plot raw delivered lumis
    plotRawLumis(raw, outDir=pltDir, name='deliveredLumi')
    plotRawLumis(raw24, outDir=pltDir, name='deliveredLumi2024')
    plotRawLumis(raw23, outDir=pltDir, name='deliveredLumi2023')


    #plot mq recorded lumis w/ raw lumis
    plotMQRawTogether(lumis, raw, outDir=pltDir, name='mqLumisPlusRaw')
    plotMQRawTogether(lumis24, raw24, outDir=pltDir, name='mqLumisPlusRaw2024')
    plotMQRawTogether(lumis23, raw23, outDir=pltDir, name='mqLumisPlusRaw2023')


    #plot mq good run lumi w/ raw lumis
    plotMQRawTogether(selected_rows, raw, outDir=pltDir, name='mqLumisGoodPlusRaw')
    plotMQRawTogether(selected_rows24, raw24, outDir=pltDir, name='mqLumisGoodPlusRaw2024')
    plotMQRawTogether(selected_rows23, raw23, outDir=pltDir, name='mqLumisGoodPlusRaw2023')

    #plot the average time files are open in runs and average lumis/s in runs
    plotFileOpenTimes(lumis, outDir=pltDir)