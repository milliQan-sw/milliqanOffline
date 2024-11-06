import os
import sys
import shutil
import glob
import socket
import numpy as np
from pymongo import MongoClient
from datetime import datetime, timedelta

sys.path.append('/home/milliqan/milliqanOffline/Run3Detector/scripts')
from mongoConnect import mongoConnect


#function taken from https://github.com/milliQan-sw/milliqanOffline/blob/master/Run3Detector/scripts/transferFiles.py
def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        get_lock._lock_socket.bind('\0' + process_name)
        print ('Acquired lock for transferFiles.py.')
    except socket.error:
        print ('Lock already exists for transferFiles.py -- it\'s already running elsewhere!')
        sys.exit()

#define class to remove files
class fileRemover:
    def __init__(self, path, usageLim, sites, copies, db, dryRun=False):
        self.path = path                 #data directory path
        self.usageLim = usageLim         #Limit on disk usage before we remove files
        self.sites = sites               #Sites to check in mongoDB
        self.copies = copies             #Required copies in mongoDB before deletion
        self.db = db                     #MongoDB
        self.dryRun = dryRun             #Bool for testing w/o removal

    #Function checks the disk space remaining
    def checkDiskSpace(self):

        shouldRemove = False
        BytesPerGB = 1024 * 1024 * 1024

        total, used, free = shutil.disk_usage('/home')
        totalGB = round(float(total)/BytesPerGB, 2)
        usedGB = round(float(used)/BytesPerGB, 2)
        pctUsed = round(usedGB/totalGB, 2)*100
        if pctUsed > self.usageLim: shouldRemove = True

        print("Total {0}GB, Used {1}GB".format(totalGB, usedGB))
        print("Percent of disk used {}%".format(pctUsed))
        return shouldRemove

    #List all root files in data directory
    def listFiles(self):
        files = list(filter(os.path.isfile, glob.glob(self.path + '*.root')))
        files.sort(key=lambda x: os.path.getmtime(x))
        self.files = files
        return files

    #Check which files have "copies" number of entries in mongoDB
    def checkMongoDB(self):

        ids = self.getFileIDs()

        all_ids = []
        for site in self.sites:
            tmp_ids = []
            for x in (self.db.milliQanRawDatasets.find({"_id" :{"$in": list(ids.keys())}, "site" :site})):
                tmp_ids.append(x['_id'])
            all_ids.append(tmp_ids)

        uniqueID = np.array([])
        for site in self.sites:
            tmpIDs = np.array([x.replace('_'+site, '') for x in list(ids.keys()) if site in x])
            uniqueID = np.concatenate((uniqueID, tmpIDs))
        uniqueID = np.unique(uniqueID)

        idCount = {}
        for thisID in uniqueID:
            idCount[thisID] = 0
            for siteIDs in all_ids:
                if any(thisID in x for x in siteIDs): idCount[thisID]+=1

        deleteFiles = []
        for _id, count in idCount.items():
            if count >= self.copies: 
                subids = [x for x in list(ids.keys()) if _id in x]
                deleteFiles.append(ids[subids[0]])

        return deleteFiles
    
    #Get fileIDs for list of filenames
    def getFileIDs(self):
        filelist = self.listFiles()
        ids = {}
        for filename in filelist:
            for site in self.sites:
                runNumber = int(filename.split("/")[-1].split("Run")[-1].split(".")[0])
                fileNumber = int(filename.split("/")[-1].split(".")[1].split("_")[0])   
                dataType = filename.split("/")[-1].split("_")[0]
                _id = "{}_{}_{}_{}".format(runNumber, fileNumber, dataType, site)
                ids[_id] = filename
        return ids

    #Delete list of files
    def deleteFiles(self):
        counter = 0
        filesToDelete = self.checkMongoDB()
        for filename in filesToDelete:
            file_mTime =  datetime.fromtimestamp(os.path.getmtime(filename))
            if datetime.now() < (file_mTime + timedelta(hours=24)): 
                print('skipping file {}, created within last 24 hours'.format(filename))
                continue
            if os.path.exists(filename):
                print('Deleting file {}'.format(filename))
                if not self.dryRun:
                    try:
                        os.remove(filename)
                        counter += 1
                    except:
                        print("Error deleting file {}".format(filename))
                        sys.exit(1) #remove this after debugging

            else:
                print('Error, file {} does not exist'.format(filename))

if __name__ == "__main__":

    path = '/home/milliqan/data/'
    usageLim = 85
    sites = {"UCSB":"milliqan@cms3.physics.ucsb.edu:/net/cms26/cms26r0/milliqan/Run3/", "OSU":"milliqan@128.146.39.20:/data/users/milliqan/run3/"}
    copies = 2

    db = mongoConnect()
    get_lock('check_disk')

    myRemover = fileRemover(path, usageLim, sites, copies, db, dryRun=False)
    if myRemover.checkDiskSpace():
        print("Disk space usage is above threshold {0}, going to try removing files".format(myRemover.usageLim))
        myRemover.deleteFiles()
    else:
        print("Disk usage is below threshold {0}".format(myRemover.usageLim))


