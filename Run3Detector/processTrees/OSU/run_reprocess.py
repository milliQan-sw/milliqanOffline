import os
import numpy as np
import datetime
import argparse
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../../scripts/')
from mongoConnect import *
import pandas as pd
import shutil
import htcondor 

#this file will be run in a cron job to automatically process all match files
#in the same job as a run is matched the offline files will then be reproduced
#to ensure jobs are not reprocessed multiple times while waiting in the queue output the condor job number to the run list
#if the condor job is no longer processing remove the run list
#otherwise if the run/files are in the run list do not reprocess

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--runDir', type=str, help='Primary directory to be processed')
    parser.add_argument('-s', '--subDir', type=str, help='Subdirectory to be processed')
    parser.add_argument('-a', '--all', action='store_true', help='Find all non processed files and create offline trees')
    parser.add_argument('-f', '--reprocess', action='store_true', help='Reprocess all files')
    parser.add_argument('-v', '--version', type=str, default='33', help='Set the version of offline trees')
    parser.add_argument('-S', '--single', type=str, default='-1', help='Single file to be submitted')
    parser.add_argument('-R', '--run', type=str, help='Single run to be submitted')
    parser.add_argument('-o', '--outputDir', type=str, help='Output directory for files')
    parser.add_argument('--slab', action='store_true', help='Option to run on slab data')
    parser.add_argument('--site', type=str, default='OSU', help='Site that you are running on, will be used when adding to mongoDB')
    #parser.add_argument('--reprocess', type=str, default='missingOfflineFiles.txt', help='reprocess files in given txt file')
    args = parser.parse_args()
    return args

def getRunsToMatch():

    db = mongoConnect()

    #get all files that exist as raw
    raw_query = {'site': 'OSU', 'type': 'MilliQan'}
    raw_out = db.milliQanRawDatasets.find(raw_query)

    #raw file location initially has full path of file to run3 dir before being moved to appropriate sub dir, don't process these files yet
    raw_files = np.array([[int(x['run']), int(x['file']), float(f"{x['run']}.{x['file']}"), x['location']] for x in raw_out if not x['location'].endswith('root')])
    print("There are {} raw files".format(len(raw_files)))

    #check if matched files exist for the unmatched offline files
    match_query = {'site': 'OSU', 'type': 'MatchedEvents'}
    match_out = db.milliQanRawDatasets.find(match_query)
    match_files = np.array([[int(x['run']), int(x['file']), float(f"{x['run']}.{x['file']}"), x['location']] for x in match_out])
    print("There are {} matched files".format(len(match_files)))
    match = raw_files[~np.isin(raw_files[:, 2], match_files[:, 2])]
    print("There are {} raw files that need to be matched".format(len(match)))

    match = pd.DataFrame(match[:, [0, 3]], columns=['run', 'location'])
    match['run'] = match['run'].astype(int)
    match = match.drop_duplicates(subset='run')
    match = match.sort_values(by='run')

    #check if trigger files exist
    run_values = match['run'].astype(int).tolist()
    trigger_query = {'site': 'OSU', 'type': 'TriggerBoard', 'run': {'$in': run_values}}
    trig_out = db.milliQanRawDatasets.find(trigger_query)
    trig_files = np.array([int(x['run'])for x in trig_out])
    trig_files = np.unique(trig_files)
    trig_files = pd.DataFrame(trig_files, columns=['run'])
    match = match.merge(trig_files[['run']], on='run')

    #TODO add another query to check if matching is under some threshold and rematch

    return match

def checkCondorJobs():
    logDir = 'condorLogs/'
    current_jobs = {}
    for filename in os.listdir(logDir):
        try:
            with open(logDir+filename, 'r') as fin:
                last_line = fin.readlines()[-1].strip()
                if len(last_line) == 0: continue
                condor_job = last_line.split()[-1].replace('.', '')
                current_jobs[filename] = int(condor_job)
        except Exception as e:
            print("Error reading {}, with exception {}".format(logDir+filename, e))
    return current_jobs

def getRunningJobs(username='milliqan'):

    jobIds = []

    schedd = htcondor.Schedd()

    constraint = 'Owner == "{}" && (JobStatus == 1 || JobStatus == 2)'.format(username)
    info = ['ClusterId', 'Cmd']

    query = schedd.query(constraint=constraint, projection=["ClusterId", "Cmd"])

    clusters = {}

    for job in query:
        if not job['Cmd'].endswith('update.sh'): continue
        clusters[job['ClusterId']] = job['Cmd']
    
    return clusters

def cleanupCondorDir(oldJobs):
    condorLogDir = 'condorLogs/'
    matchDir = 'matchLists/'
    for file, id in oldJobs.items():
        filelist = 'matchlist_update_{}.txt'.format(file.split('log_')[-1].split('.')[0])
        if os.path.exists(condorLogDir + file):
            os.remove(condorLogDir + file)
        if os.path.exists(matchDir+filelist):
            os.remove(matchDir+filelist)

def sortJobs():
    jobIds = getRunningJobs()
    current_jobs = checkCondorJobs()

    running_jobs = {}
    completed_jobs = {}

    for d, id in current_jobs.items():
        if id in jobIds.keys():
            running_jobs[d] = id
        else:
            completed_jobs[d] = id

    cleanupCondorDir(completed_jobs)

    return running_jobs

def getProcessingRuns(running_jobs):
    matchlistDir = 'matchLists/'

    col_names = ['run', 'location']

    df = pd.DataFrame(columns=col_names)

    for key in running_jobs.keys():
        matchlist = "matchlist_update_{}.txt".format(key.split('log_')[-1].split('.')[0])
        if not os.path.exists(matchlistDir+matchlist): continue
        this_df = pd.read_csv(matchlistDir+matchlist, names=col_names, delimiter='\t', header=None)
        df = pd.concat([df, this_df])

    df = df.drop_duplicates(subset='run')
    df = df.sort_values(by='run')

    return df

if __name__=="__main__":

    if shutil.which('root') is None:
        print("Need to source a root version before proceeding... exiting")
        sys.exit(1)

    args = parse_args()

    d = datetime.datetime.now()

    force = args.reprocess

    milliDAQ = 'MilliDAQ.tar.gz'
    milliqanOffline = 'milliqanOffline_v35.tar.gz'
    site = args.site

    if not os.path.exists(milliDAQ):
        print("Missing the MilliDAQ.tar.gz file, please create this file first...")
        sys.exit(0)
    if not os.path.exists(milliqanOffline):
        print("Missing the milliqanOffline_vX.tar.gz file, please create this file first...")
        sys.exit(0)

    logDir = '/data/users/milliqan/log/reprocess/' + d.strftime('%m_%d_%H')

    if not os.path.exists('condorLogs/'):
        os.mkdir('condorLogs/')

    if(not os.path.isdir(logDir)): os.mkdir(logDir)
    else:
        index = 2
        newLogDir = logDir + '_v' + str(index) + '/'
        while os.path.isdir(newLogDir):
            index += 1
            newLogDir = logDir + '_v' + str(index) + '/'
        os.mkdir(newLogDir)
        logDir = newLogDir
    if not logDir.endswith('/'): logDir += '/'

    #get a list of runs that need to be matched
    runsToProcess = getRunsToMatch()

    #get the lists of runs that are still being processed by other condor jobs
    running_jobs = sortJobs()
    processingRuns = getProcessingRuns(running_jobs)

    print("Debugging Processing", processingRuns)

    merged = pd.concat([runsToProcess, processingRuns])
    runsToProcess = merged.drop_duplicates(subset='run', keep=False)

    print("Debugging", runsToProcess)

    if not os.path.exists(os.getcwd() + '/matchLists'):
        print("Making directory {} to save match lists".format(os.getcwd() + '/matchLists'))
        os.mkdir(os.getcwd() + '/matchLists')
    filelist = '{0}/matchLists/matchlist_update_{1}.txt'.format(os.getcwd(), d.strftime('%m_%d_%H'))

    runsToProcess.to_csv(filelist, sep='\t', index=False, header=False)

    if not os.path.exists(os.getcwd() + '/subs'):
        print("Making directory {} to save condor sub files".format(os.getcwd() + '/subs'))
        os.mkdir(os.getcwd() + '/subs')
    condorFile = 'subs/run_update_{}.sub'.format(d.strftime('%m_%d_%H'))

    f = open(condorFile, 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    Rank = TARGET.IsLocalSlot
    request_disk = 5000MB
    request_memory = 500MB
    request_cpus = 1
    executable              = update.sh
    arguments               = $(PROCESS) {1} {5}
    log                     = {2}log_$(PROCESS).log
    output                  = {2}out_$(PROCESS).txt
    error                   = {2}error_$(PROCESS).txt
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {1}, {3}, {4}, update_wrapper.py, update.sh
    getenv = true
    queue {0}
    """.format(len(runsToProcess),filelist,logDir,milliDAQ,milliqanOffline,site)

    f.write(submitLines)
    f.close()

    os.system('condor_submit {} >& condorLogs/condor_log_{}.log'.format(condorFile, d.strftime('%m_%d_%H')))
