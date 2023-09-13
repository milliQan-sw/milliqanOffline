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
        moveFile(db, site, source+filename, dest)

        '''runNumber, fileNumber, fileType = getFileDetails(filename)

        newLocation = str(dest + '/' + filename)

        shutil.move(os.path.join(source, filename), os.path.join(dest, filename))
    
        db.milliQanRawDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType}, 
                                          { '$set': {"location" : newLocation}})

        print("Moved file {0} and updated entry in MongoDB".format(filename))'''


def moveFile(db, site, source, dest):
    filename = source.split('/')[-1]

    runNumber, fileNumber, fileType = getFileDetails(filename)

    if dest.endswith('.root'): newLocation = dest
    else:
        newLocation = str(dest + '/' + filename)

    shutil.move(source, newLocation)

    db.milliQanRawDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType},
                                      { '$set': {"location" : newLocation}})

    print("Moved file {0} and updated entry in MongoDB".format(filename))

def main(site='', source='', dest=''):
    
    if len(sys.argv) >= 4:
        site = sys.argv[1]
        source = sys.argv[2]
        dest = sys.argv[3]
    else:
        if site == '' or source == '' or dest == '':
             print("Please provide site, source and destination directories")
             return

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

    if source.endswith('.root'):
        moveFile(db, site, source, dest)
    else:
        moveFiles(db, site, source, dest)




if __name__ == "__main__":

    main()
