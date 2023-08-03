import os
import sys
import shutil
import glob
import socket
import time
import numpy as np
from pymongo import MongoClient
from datetime import datetime, timedelta

#Function taken from https://github.com/milliQan-sw/milliqanOffline/blob/master/Run3Detector/scripts/mongoConnect.py
def mongoConnect(serverName="mongodb+srv://mcitron:milliqan@testcluster.ffkkz.mongodb.net/?retryWrites=true&w=majority"):
    try:
        client = MongoClient(serverName)
        db=client.milliQanData
        serverStatusResult=db.command("serverStatus")
        # Issue the serverStatus command and print the results
    except:
        print ("Could not publish as failed to connect to mongo server")
        return;
    return db

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
        self.offlinePath = ''            #Path for offline files
        self.offlineStorageTime = 7      #Amount of time to store offline files before deleting (days)

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
        return files

    #Check which files have "copies" number of entries in mongoDB
    def checkMongoDB(self):

        ids = self.getFileIDs()

        all_ids = []
        for site in self.sites:
            tmp_ids = []
            for x in (self.db.milliQanRawDatasets.find({"_id" :{"$in": ids}, "site" :site})):
                tmp_ids.append(x['_id'])
            all_ids.append(tmp_ids)

        uniqueID = np.array([])
        for site in self.sites:
            tmpIDs = np.array([x.replace('_'+site, '') for x in ids if site in x])
            uniqueID = np.concatenate((uniqueID, tmpIDs))
        uniqueID = np.unique(uniqueID)

        idCount = {}
        for thisID in uniqueID:
            idCount[thisID] = 0
            for siteIDs in all_ids:
                if any(thisID in x for x in siteIDs): idCount[thisID]+=1

        deleteFiles = []
        for _id, count in idCount.items():
            #print('ID: {0} is stored at {1} sites'.format(_id, count))
            if count >= self.copies: deleteFiles.append(_id)
        return deleteFiles
    
    #Get fileIDs for list of filenames
    def getFileIDs(self):
        filelist = self.listFiles()
        ids = []
        for filename in filelist:
            for site in self.sites:
                runNumber = int(filename.split("/")[-1].split("Run")[-1].split(".")[0])
                fileNumber = int(filename.split("/")[-1].split(".")[1].split("_")[0])   
                dataType = filename.split("/")[-1].split("_")[0]
                _id = "{}_{}_{}_{}".format(runNumber, fileNumber, dataType, site)
                ids.append(_id)
        return ids

    #Get filename for list of fileIDs
    def nameFromID(self):
        IDs = self.checkMongoDB()
        filenames = []
        for _id in IDs:
            _id = _id.split('_')
            filename = _id[2] + '_Run' + _id[0] + '.' + _id[1]
            if _id[2] == 'MilliQan': filename += '_default.root'
            elif _id[2] == 'MilliQanSlab': filename += '_default.root'
            else: filename += '.root'
            filenames.append(filename)
        return filenames

    #Delete list of files
    def deleteFiles(self):
        counter = 0
        filesToDelete = self.nameFromID()
        for filename in filesToDelete:
            file_mTime =  datetime.fromtimestamp(os.path.getmtime(self.path + filename))
            if datetime.now() < (file_mTime + timedelta(hours=24)): 
                print('skipping file {}, created within last 24 hours'.format(filename))
                continue
            #if counter > 10: break
            if os.path.exists(self.path + filename):
                print('Deleting file {}'.format(filename))
                if not self.dryRun: 
                    os.remove(self.path + filename)
                    counter += 1
            else:
                print('Error, file {} does not exist'.format(filename))

    def deleteOfflineFiles(self):
        print("In deleteOfflineFiles function", self.offlinePath)
        for filename in os.listdir(self.offlinePath):
            if not filename.endswith('.root'): continue
            m_time = os.path.getmtime(self.offlinePath+filename)
            if((time.time() - m_time) > 86400*self.offlineStorageTime):
                print("Deleting file {0}{1}".format(self.offlinePath, filename))
                os.remove(self.offlinePath+filename)



if __name__ == "__main__":

    path = '/home/milliqan/data/'
    offlinePath = '/home/milliqan/offlineFiles/'
    usageLim = 85
    sites = {"UCSB":"milliqan@cms3.physics.ucsb.edu:/net/cms26/cms26r0/milliqan/Run3/", "OSU":"milliqan@128.146.39.20:/data/users/milliqan/run3/"}
    copies = 2
    offlineStorageTime = 7 #days

    db = mongoConnect()
    get_lock('check_disk')

    myRemover = fileRemover(path, usageLim, sites, copies, db, dryRun=False)
    myRemover.offlinePath = offlinePath
    myRemover.offlineStorageTime = offlineStorageTime
    if not offlinePath == "" and os.path.exists(offlinePath):
        myRemover.deleteOfflineFiles()
    if myRemover.checkDiskSpace():
        print("Disk space usage is above threshold {0}, going to try removing files".format(myRemover.usageLim))
        myRemover.deleteFiles()
    else:
        print("Disk usage is below threshold {0}".format(myRemover.usageLim))


