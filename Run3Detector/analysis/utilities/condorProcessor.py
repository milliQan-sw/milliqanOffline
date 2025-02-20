import os
import shutil
import pandas as pd
import math
import json
import tarfile
import argparse
import ROOT as r
import sys

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-r", "--resubmit", help="Argument to automatically resubmit any jobs that failed", action='store_true')
    parser.add_argument("-m", "--merge", help="Argument to merge all successful root files", action='store_true')
    parser.add_argument("-o", "--outputDir", help="Optionally pass the name of output directory", type=str)
    parser.add_argument("-t", "--tarFile", help="Recreate tar file", action='store_true')
    parser.add_argument("--dryRun", help="Option to run without submitting", action='store_true')
    args = parser.parse_args()
    return args

def writeCondorSub(exe, script, nJobs, filelist, outDir, includeDirs, requirements):
    f = open('run.sub', 'w')
    submitLines = """
    Universe = vanilla
    +IsLocalJob = true
    run_as_owner = true
    Rank = TARGET.IsLocalSlot
    +IsSmallJob = true
    request_disk = {8}
    request_memory = {7}
    request_cpus = {6}
    executable              = {1}
    arguments               = {2} {3} $(PROCESS) {4} {5}
    log                     = {4}/log_$(PROCESS).log
    output                  = {4}/out_$(PROCESS).out
    error                   = {4}/error_$(PROCESS).err
    should_transfer_files   = Yes
    when_to_transfer_output = ON_EXIT
    transfer_input_files = {4}/{1}, {4}/{2}, {4}/{3}, {4}/milliqanProcessing.tar.gz, {4}/mqLumis.json, {4}/goodRunsList.json
    transfer_output_files = ""
    getenv = true
    queue {0}
    """.format(nJobs,exe,script,filelist,outDir,includeDirs,requirements[0],requirements[1],requirements[2])

    f.write(submitLines)
    f.close()

def createTarFile():
    with tarfile.open('milliqanProcessing.tar.gz', 'w:gz') as tar:
        tar.add('../utilities/', arcname='.')
        tar.add('../../configuration/', arcname='.')

def getRunFile(filename):
    run = int(filename.split('Run')[1].split('.')[0])
    file = int(filename.split('.')[1].split('_')[0])
    return run, file

def getSimFilesLocal(dataDir='/', debug=False):

    runList = []
        
    for filename in os.listdir(dataDir):

        if debug and len(runList) > 10: break

        if not filename.endswith('.root'): continue
        
        runList.append('{}/{}:t'.format(dataDir, filename))

    return runList

def getFilesLocal(startRun=-1, stopRun=10e9, beam=None, goodRun=None, dataDir='/store/user/milliqan/trees/v35/bar/', debug=False, sim=False):

    runList = []

    mqLumis = pd.read_json('mqLumis.json', orient = 'split', compression = 'infer')
    goodRuns = pd.read_json('goodRunsList.json', orient = 'split', compression = 'infer')

    for root, dirs, files in os.walk(dataDir):

        for directory in dirs:

            print("Checking for files in {}{}".format(root, directory))
            
            for filename in os.listdir(root+directory):

                if debug and len(runList) > 10: break

                if not filename.endswith('.root'): continue
                
                if not sim:
                    run, file = getRunFile(filename)

                    #check if the run is in the range desired
                    inRange = False
                    if stopRun is None:
                        if run == startRun: inRange = True
                    else:
                        if run >= startRun and run < stopRun: inRange = True

                    #print("File {} in range {}".format(filename, inRange))

                    if not inRange: continue

                    #check if there is beam if desired
                    if beam is not None:
                        beamOn = checkBeam(mqLumis, run, file, branch='beamInFill')
                        if beamOn == None: continue
                        if (beam and not beamOn) or (not beam and beamOn): continue

                    #check good runs list
                    if goodRun is not None:
                        isGoodRun = checkGoodRun(goodRuns, run, file, branch=goodRun)

                        if not isGoodRun: continue

                #add file to runlist
                runList.append('{}{}/{}:t'.format(root, directory, filename))

    return runList

def checkGoodRun(goodRuns, run, file, branch='goodRunTight'):
    goodRun = goodRuns[branch].loc[(goodRuns['run'] == run) & (goodRuns['file'] == file)].values
    if len(goodRun) == 1:
        return goodRun[0]
    return False

def checkBeam(mqLumis, run, file, branch='beam'):
    #print("check beam run {} file {}".format(run, file))
    beam = mqLumis[branch].loc[(mqLumis['run'] == run) & (mqLumis['file'] == file)]
    if beam.size == 0: return None
    beam = beam.values[0]
    return beam

def copyConfigs():
    try:
        shutil.copy('/eos/experiment/milliqan/Configs/mqLumis.json', os.getcwd())
        shutil.copy('/eos/experiment/milliqan/Configs/goodRunsList.json', os.getcwd())
    except:
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            shutil.copy(script_dir+'/../../configuration/barConfigs/mqLumis.json', os.getcwd())
            shutil.copy(script_dir+'/../../configuration/barConfigs/goodRunsList.json', os.getcwd())
        except:
            print("Could not find the lumi/good runs files on eos or locally")
            sys.exit(1)

def createRunList(files, name='filelist.json', nFilesPerJob=100):
    
    runList = {}
    
    nfiles = len(files)
    jobs = math.ceil(nfiles / nFilesPerJob)

    iJob = 0
    thisJob = []
    for ifile, filename in enumerate(files):
        if ifile % nFilesPerJob == 0 and ifile > 0:
            runList[iJob] = thisJob
            thisJob = []
            iJob += 1
        thisJob.append(filename)

    with open(name, 'w') as fout:
        json.dump(runList, fout)

    return jobs

def checkZombie(filename):
    try:
        fin = r.TFile.Open(filename)
        zombie = fin.IsZombie()
        if zombie: print("File {} is a zombie".format(filename))
        return zombie
    except:
        print("Unable to open file {}".format(filename))
        return False

def checkFailures(outputDir, sim=False):

    totalFiles = []
    filesToMerge = []
    goodFiles = []

    for filename in os.listdir(outputDir):
        if filename.endswith('.root'):
            if 'merge' in filename: continue
            if checkZombie(outputDir+'/'+filename): continue
            filesToMerge.append(filename)
            #goodFiles.append(int(filename.split('_')[-1].split('.')[0]))
            if not sim:
                goodFiles.append(int(filename.split('_')[-2].split('.')[0]))
            else:
                goodFiles.append(int(filename.split('_')[-1].split('.')[0]))

        if not filename.endswith('.err'):
            continue
        
        totalFiles.append(int(filename.split('_')[-1].split('.err')[0]))

    totalFiles.sort()
    goodFiles.sort()

    filesToResubmit = set(totalFiles)
    goodFiles = set(goodFiles)

    filesToResubmit = list(filesToResubmit - goodFiles)

    if len(filesToResubmit) == 0:
        print("There are no files to resubmit!")
    else:
        print("Files to resubmit {}".format(", ".join(map(str, filesToResubmit))))
    if len(filesToMerge) == 0:
        print("There are no files to merge!")
    else:
        print("Files to merge ({}): \n {}".format(len(filesToMerge), "\t\n ".join(filesToMerge)))

    return filesToResubmit, filesToMerge

def mergeFiles(outputDir, filesToMerge, includeDirs, name='mergedOutput.root'):

    filesToMerge = [outputDir+'/'+f for f in filesToMerge]
    files = ' '.join(filesToMerge)

    with open('mergeScript.sh', 'w') as fout:
        fout.write('#!/usr/bin/bash\n')
        fout.write('source /root/bin/thisroot.sh\n')
        fout.write('hadd -f -j 4 {} {}\n'.format(outputDir+'/'+name, files))
    os.system('chmod a+x mergeScript.sh')
    cmd = './mergeScript.sh'
    if not args.dryRun:
        os.system('singularity run -B {} /cvmfs/unpacked.cern.ch/registry.hub.docker.com/carriganm95/milliqan_uproot\:latest/ {}'.format(includeDirs, cmd))

def resubmit(outputDir, filesToResubmit):

    resubmitScript = outputDir + '/resubmit.sub'
    shutil.copy(outputDir + '/run.sub', resubmitScript)
    
    with open(resubmitScript, 'r') as file:
        lines = file.readlines()

    # Modify the last line
    for i, line in enumerate(lines):
        if line.strip().startswith('queue'):
            # Change the line to the new queue value
            lines[i] = '    queue Process in {}\n'.format(' '.join(map(str, filesToResubmit)))
            break

    # Write the modified lines back to the file
    with open(resubmitScript, 'w') as file:
        file.writelines(lines)

    cmd = 'condor_submit {}'.format(resubmitScript)
    if not args.dryRun:
        os.system(cmd)

if __name__ == "__main__":

    args = parse_args()

    r.gErrorIgnoreLevel = r.kBreak

    nFilesPerJob = 1
    sim = True
    script_dir = '../backgroundEstimation/'
    script = 'backgroundCutFlowCondor.py'
    singularity_image = ''
    exe = 'condor_exe.sh'
    fileListName = 'filelist.json'
    outputDir = '/data/user/mcarrigan/milliqan/backgroundCutFlow_signalSimTest/'
    requirements = ['4', '4000MB', '3000MB'] #CPU, Memory, Disk
    includeDirs = '/data/'

    if args.tarFile:
        createTarFile()
        sys.exit(0)
    
    if args.outputDir:
        outputDir = args.outputDir

    if args.resubmit or args.merge:
        filesToResubmit, filesToMerge = checkFailures(outputDir, sim)
        print("There are {} file to resubmit and {} files available to merge".format(len(filesToResubmit), len(filesToMerge)))
        if args.merge:
            mergeFiles(outputDir, filesToMerge, includeDirs)
        if args.resubmit:
            resubmit(outputDir, filesToResubmit)
        sys.exit(0)

    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
        os.system(f'chmod -R a+rwx {outputDir}')

    copyConfigs()

    createTarFile()

    if sim:
        filesList = getSimFilesLocal(dataDir='/data/user/mcarrigan/milliqan/pulseInjectedSim_v3/trees/', debug=False)
    else:
        filesList = getFilesLocal()

    nJobs = createRunList(filesList, name=fileListName, nFilesPerJob=nFilesPerJob)

    print("There are {} files and {} jobs".format(len(filesList), nJobs))

    writeCondorSub(exe, script, nJobs, fileListName, outputDir, includeDirs, requirements)

    shutil.copy(exe, outputDir)
    shutil.copy('run.sub', outputDir)
    shutil.copy(fileListName, outputDir)
    shutil.copy('milliqanProcessing.tar.gz', outputDir)
    shutil.copy('mqLumis.json', outputDir)
    shutil.copy('goodRunsList.json', outputDir)
    shutil.copy(script_dir+script, outputDir)


    if not args.dryRun:
        os.system('condor_submit run.sub')

