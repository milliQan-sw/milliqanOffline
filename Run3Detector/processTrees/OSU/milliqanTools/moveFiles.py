import os
import sys
import shutil
import subprocess
from datetime import datetime

sys.path.append('/share/scratch0/milliqan/milliqanOffline/Run3Detector/scripts/')
sys.path.append('/share/scratch0/milliqan/processTrees/')

from mongoConnect import mongoConnect
from changeLocation import getFileDetails

if __name__ == "__main__":

    print("Starting to run moveFiles python script")

    directories = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

    dataDir = '/store/user/milliqan/run3/'

    site = 'OSU'

    db = mongoConnect()


    if db.milliQanRawDatasets.count_documents({"site" : site}, limit=1)==0:
        print("Site: {0} is not a valid site".format(site))
        sys.exit(1)

    for filename in os.listdir(dataDir):
        print(filename)
        if not filename.endswith(".root"): continue

        try:
            runNum = int(filename.split('Run')[-1].split('.')[0])
        except:
            print("File {} does not have the correct name format to find the run number".format(filename))
            continue

        runNumber, fileNumber, fileType = getFileDetails(filename)

        if fileType == 'MilliQan' or fileType == 'TriggerBoard': outputDir = dataDir + '/bar/'
        elif fileType == 'MilliQanSlab' or fileType == 'TriggerBoardSlab': outputDir = dataDir + '/slab/'

        subdir1 = str((runNum // 100) * 100)
        outputDir += subdir1
        if not os.path.exists(outputDir): os.mkdir(outputDir)

        subdir2 = directories[(runNum % 100) // 10]
        outputDir += '/' + subdir2 + '/'
        if not os.path.exists(outputDir): os.mkdir(outputDir)

        ctime = datetime.fromtimestamp(os.path.getctime(dataDir+filename))

        db.milliQanRawDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType},
                                          { '$set': {"location" : outputDir, "date" : ctime}})

        print("Moving file {0} to directory {1}".format(dataDir+filename, outputDir+filename))

        shutil.move(dataDir+filename, outputDir+filename) 
        if fileType != 'MilliQan': continue
        cmd = 'python3 /share/scratch0/milliqan/processTrees/run_processTrees.py -S {0}.{1} -r {2} -s {3}'.format(runNumber, fileNumber, subdir1, subdir2)
        wd = os.getcwd()
        p = subprocess.run([cmd], shell=True, cwd='/share/scratch0/milliqan/processTrees/')
                
