#!/usr/bin/python3

import glob
import os
import time
import socket
import sys
from ROOT import TFile
from mongoConnect import mongoConnect
from bson.objectid import ObjectId


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

def FileIsGood(path):
    try:
        f = TFile(path, "READ")
        if not f or f.IsZombie():
            os.system("echo '{0} is not ready to be transferred' >> {1}".format(path, logFile))
            return False
        f.Close()
        return True
    except:
        return False

def checkMongoDB(db,allIds,allInputs,force,offline=False):
    nX = 0
    #Check for existing entry 
    idsOut = []
    inputsOut = []
    indicesToSkip = []
    entriesInDB = []
    locationInDb = []
    currentLocation = []
    if offline:
        mongoDB = db.milliQanOfflineDatasets
    else:
        mongoDB = db.milliQanRawDatasets
    for x in (mongoDB.find({"_id" :{"$in": allIds}})):
        indexInDb = allIds.index(x["_id"])
        indicesToSkip.append(indexInDb)
    for index in range(len(allIds)):
        if not force and index in indicesToSkip: continue
        idsOut.append(allIds[index])
        inputsOut.append(allInputs[index])
        if index in indicesToSkip:
            entriesInDB.append(1)
            for x in (monboDB.find({"_id" : allIds[index]})):
                currentLocation.append(x["location"])
        else:
            entriesInDB.append(0)
            currentLocation.append("")
    return idsOut,inputsOut,entriesInDB, currentLocation

def checkFileAtDest(inputFile,destination):
    host = destination.split(":")[0]
    filePath = os.path.join(destination.split(":")[-1],inputFile.split("/")[-1])
    fileAtDest = os.system('ssh -q {0} [ -f {1} ]'.format(host,filePath)) == 0
    #To be implemented!
    return fileAtDest

def updateMongoDB(milliQanRawDataset,db,replace):
    if replace:
        db.milliQanRawDatasets.replace_one({"_id": milliQanRawDataset["_id"]},milliQanRawDataset)
    else:
        db.milliQanRawDatasets.insert_one(milliQanRawDataset)

def transferFiles(source,destinations,logFile,force=False):
    db = mongoConnect()
    get_lock('transfer_files_TEMP')

    nTransferred = 0
    mbytesTransferred = 0
    os.system("echo '" + time.strftime("%c") + " Attempting to transfer data files ...' >> " + logFile)
    allIds = []
    allInputs = []
    for inputFile in sorted(glob.glob(source + "*.root"), key=os.path.getmtime, reverse=True):
        for site, destination in destinations.items():
            #Details for database entry
            runNumber = int(inputFile.split("/")[-1].split("Run")[-1].split(".")[0])
            fileNumber = int(inputFile.split("/")[-1].split(".")[1].split("_")[0])    
            dataType = inputFile.split("/")[-1].split("_")[0]
            _id = "{}_{}_{}_{}".format(runNumber,fileNumber,dataType,site)
            allIds.append(_id)
            allInputs.append(inputFile)
    idsOut,inputsOut,entriesInDB, currentLocations = checkMongoDB(db,allIds,allInputs,force)
    for _id,inputFile,entryInMongo,currentLocation in zip(idsOut,inputsOut,entriesInDB, currentLocations):
        site = _id.split('_')[-1]
        destination = destinations[site]
        print(_id, site ,destination)
        nTransferred += 1
        sizeInMB = os.path.getsize(inputFile) / 1024.0 / 1024.0
        mbytesTransferred += sizeInMB
        if FileIsGood(inputFile):
            if currentLocation != "":
                currentLocation = currentLocation.split(inputFile.split("/")[-1])[0]
                if currentLocation != destination.split(":")[-1]: destination = destination.split(":")[0] + ":" + currentLocation
            fileAtDestAndDB = checkFileAtDest(inputFile,destination)
            #Don't transfer files that have already been sent (unless forced)
            if fileAtDestAndDB and entryInMongo and not force:
                print (("File {0} exists at destination and database (skipping)").format(inputFile))
                continue
            command = "rsync -zh " + inputFile + " " + destination + " >> " + logFile
            transfer = os.system(command)
            if transfer != 0:
                os.system("echo 'Transfer of {0} failed' >> {1}".format(inputFile, logFile))
            else:
                os.system("echo '\t{0}:\t {1:.2f} MB' >> {2}".format(inputFile, sizeInMB, logFile))

                #Add entry to database
                runNumber,fileNumber,dataType,site = _id.split("_")
                milliQanRawDataset = {}
                milliQanRawDataset["_id"] = _id
                milliQanRawDataset["run"] = int(runNumber)
                milliQanRawDataset["file"] = int(fileNumber)
                milliQanRawDataset["type"] = dataType
                milliQanRawDataset["site"] = site
                milliQanRawDataset["location"] = os.path.join(destination.split(":")[-1],inputFile.split("/")[-1])
                updateMongoDB(milliQanRawDataset, db, replace = entryInMongo)

    os.system("echo 'Transferred {0:.2f} MB in {1} file(s).' >> {2}".format(mbytesTransferred, nTransferred, logFile))

if __name__ == "__main__":

    source = "/home/milliqan/data/"
    logFile = "/home/milliqan/MilliDAQ_FileTransfers.log"
    
    destinations = {"UCSB":"milliqan@cms3.physics.ucsb.edu:/net/cms18/cms18r0/milliqan/run3/", "OSU":"milliqan@128.146.39.20:/store/user/milliqan/run3/", "lxplus":"/eos/experiment/milliqan/run3/bar/"}

    transferFiles(source,destinations,logFile,force=False)
