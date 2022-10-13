#!/usr/bin/python3

import glob
import os
import time
import socket
import sys
from ROOT import TFile
from mongoConnect import mongoConnect


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
    f = TFile.Open(path, "READ")
    if not f or f.IsZombie():
        os.system("echo '{0} is not ready to be transferred' >> {1}".format(path, logFile))
        return False
    f.Close()
    return True

def checkMongoDB(db,_id):
    nX = 0
    #Check for existing entry 
    for x in (db.milliQanRawDatasets.find({"_id" : _id})):
        nX +=1
        currentLocation = x["location"]

    return nX, currentLocation

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
    get_lock('transfer_files_osu')

    nTransferred = 0
    mbytesTransferred = 0
    os.system("echo '" + time.strftime("%c") + " Attempting to transfer data files to cms2.physics.ucsb.edu...' >> " + logFile)

    for inputFile in sorted(glob.glob(source + "*.root"), key=os.path.getmtime):
        if FileIsGood(inputFile):
            nTransferred += 1
            sizeInMB = os.path.getsize(inputFile) / 1024.0 / 1024.0
            mbytesTransferred += sizeInMB
            for site, destination in destinations.items():
                #Details for database entry
                runNumber = int(inputFile.split("/")[-1].split("Run")[-1].split(".")[0])
                fileNumber = int(inputFile.split("/")[-1].split(".")[1].split("_")[0])    
                dataType = inputFile.split("/")[-1].split("_")[0]
                _id = "{}_{}_{}_{}".format(runNumber,fileNumber,dataType,site)
                entryInMongo, currentLocation = checkMongoDB(db,_id)
                currentLocation = currentLocation.split(inputFile.split("/")[-1])[0]
                if currentLocation != destination.split(":")[-1]: destination = destination.split(":")[0] + ":" + currentLocation
                fileAtDestAndDB = entryInMongo and checkFileAtDest(inputFile,destination)
                #Don't transfer files that have already been sent (unless forced)
                if fileAtDestAndDB and not force:
                    print (("File {0} exists at destination and database (skipping)").format(inputFile))
                    continue
                command = "rsync --bwlimit=20000 -zh " + inputFile + " " + destination + " >> " + logFile
                transfer = os.system(command)
                if transfer != 0:
                    os.system("echo 'Transfer of {0} failed' >> {1}".format(inputFile, logFile))
                else:
                    os.system("echo '\t{0}:\t {1:.2f} MB' >> {2}".format(inputFile, sizeInMB, logFile))

                    #Add entry to database
                    milliQanRawDataset = {}
                    milliQanRawDataset["_id"] = _id
                    milliQanRawDataset["run"] = runNumber
                    milliQanRawDataset["file"] = fileNumber
                    milliQanRawDataset["site"] = site
                    milliQanRawDataset["type"] = dataType
                    milliQanRawDataset["location"] = os.path.join(destination.split(":")[-1],inputFile.split("/")[-1])
                    updateMongoDB(milliQanRawDataset, db, replace = entryInMongo)

    os.system("echo 'Transferred {0:.2f} MB in {1} file(s).' >> {2}".format(mbytesTransferred, nTransferred, logFile))

if __name__ == "__main__":
    source = "/home/milliqan/data/"
    logFile = "/home/milliqan/MilliDAQ_FileTransfersOSU.log"

    #destinations = {"UCSB":"milliqan@cms26.physics.ucsb.edu:/net/cms26/cms26r0/milliqan/Run3/", "OSU":"milliqan@cms-t3.mps.ohio-state.edu:/data/users/milliqan/run3/"}
    destinations = {"OSU":"milliqan@128.146.39.20:/data/users/milliqan/run3/"}
    transferFiles(source,destinations,logFile,force=False)

