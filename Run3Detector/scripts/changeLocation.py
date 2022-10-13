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
    runNumber = filename.split("Run")[-1].split(".")[0]
    fileNumber = filename.split(".")[1].split("_")[0]
    fileType = filename.split("_")[0]
    return int(runNumber), int(fileNumber), fileType

def moveFiles(db, site, source, dest):
    for filename in os.listdir(source):

        if not filename.endswith(".root"): continue

        runNumber, fileNumber, fileType = getFileDetails(filename)

        newLocation = str(dest + '/' + filename)

        shutil.move(os.path.join(source, filename), os.path.join(dest, filename))
    
        db.milliQanRawDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType}, 
                                          { '$set': {"location" : newLocation}})

        print("Moved file {0} and updated entry in MongoDB".format(filename))


def main():
    
    if len(sys.argv) < 4:
        print("Please provide site, source, and destination directories")
        return
    
    site = sys.argv[1]
    source = sys.argv[2]
    dest = sys.argv[3]

    if not os.path.exists(source):
        print("Path: {0} does not exist".format(source))
        return
    if not os.path.exists(dest):
        print("Path: {0} does not exist".format(deset))
        return
    
    db = mongoConnect()

    if db.milliQanRawDatasets.count_documents({"site" : site}, limit=1)==0:
        print("Site: {0} is not a valid site".format(site))
        return

    moveFiles(db, site, source, dest)




if __name__ == "__main__":

    main()
