#!/usr/bin/python3

import glob
import os
import time
import socket
import sys
from mongoConnect import mongoConnect
import transferFiles
import shutil

def getFileDetails(filename):
    filename = filename.split("/")[-1]
    runNumber = filename.split("Run")[-1].split(".")[0]
    fileNumber = filename.split(".")[1].split("_")[0]
    fileType = filename.split("_")[0]
    return int(runNumber), int(fileNumber), fileType

def moveFiles(db, site, source, dest):
    #for filename in os.listdir(source):
    filename = '/data/users/milliqan/run3/MilliQan_Run307.1_default.root'
    runNumber, fileNumber, fileType = getFileDetails(filename)
    print(runNumber, fileNumber, fileType)
    
    for x in (db.milliQanRawDatasets.find({"run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType})):
        print("Found", x["_id"], x["file"])

    newLocation = str(dest + filename.split("/")[-1])
    print("newLocation", newLocation)
    
    db.milliQanRawDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType}, 
                                      { '$set': {"location" : newLocation}})


def changeLocation(runNumber, fileNumber, site, type):
    print("test")


def main():
    
    if len(sys.argv) < 4:
        print("Please provide site, source, and destination directories")
        return
    
    site = sys.argv[1]
    source = sys.argv[2]
    dest = sys.argv[3]

    #if site not in destinations:
    #    print("Site is not a valid destination")
    #    return
    if not os.path.exists(source):
        print("Path: {0} does not exist".format(source))
        return
    if not os.path.exists(dest):
        print("Path: {0} does not exist".format(deset))
        return
    
    db = mongoConnect()

    moveFiles(db, site, source, dest)




if __name__ == "__main__":

    main()
