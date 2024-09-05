#!/usr/bin/python3

import glob
import os
import time
import socket
import sys
from ROOT import TFile
from mongoConnect import mongoConnect
from bson.objectid import ObjectId
from transferFiles import *
from changeLocation import getFileDetails
import argparse


def transferOfflineFiles(input, destination, site, version, logFile, force=False, debug=False):
    print("In transfer offline files")

    get_lock('transfer_files_offline')
    db = mongoConnect()

    nTransferred = 0
    mbytesTransferred = 0
    os.system("echo '" + time.strftime("%c") + " Attempting to transfer data files ...' >> " + logFile)
    allIds = []
    allInputs = []
    #for subdir, dirs, files in os.walk(input):
    print("LOOPING OVER OFFLINE FILES", input)
    for inputFile in sorted(glob.glob(input + "/*/*.root"), key=os.path.getmtime, reverse=True):
        file = inputFile.split('/')[-1]
        subdir = inputFile.split(file)[0]
        #for file in files:
        runNumber, fileNumber, dataType = getFileDetails(inputFile)
        _id = "{}_{}_{}_{}_{}".format(runNumber,fileNumber,version,dataType,site)
        allIds.append(_id)
        allInputs.append(os.path.join(subdir, file))

    idsOut,inputsOut,entriesInDB, currentLocations = checkMongoDB(db,allIds,allInputs,force, offline=True)
    for _id,inputFile,entryInMongo,currentLocation in zip(idsOut,inputsOut,entriesInDB, currentLocations):
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
            print(command)
            transfer = os.system(command)

            if transfer != 0:
                os.system("echo 'Transfer of {0} failed' >> {1}".format(inputFile, logFile))
            else:
                os.system("echo '\t{0}:\t {1:.2f} MB' >> {2}".format(inputFile, sizeInMB, logFile))
                runNumber,fileNumber,ver,dataType,site = _id.split("_")
                if debug: 
                    print('File: {0} \n\tRunNumber: {1} \n\tFileNumber: {2} \n\tFileType: {3} \n\tSite: {4}'.format(_id, runNumber, fileNumber, dataType, 'OSU'))            
                milliQanOfflineDataset = db.milliQanOfflineDatasets.find_one({'run' : int(runNumber), 'file' : int(fileNumber), 'type' : dataType, 'site' : 'OSU', 'version' : ver})
                if (milliQanOfflineDataset is  None):
                    print("Could not find file with id: {} ... adding to db".format(_id))
                    milliQanOfflineDataset = {}
                    milliQanOfflineDataset['_id'] = _id
                    milliQanOfflineDataset['site'] = site
                    milliQanOfflineDataset['location'] = destination.split(':')[-1]
                    milliQanOfflineDataset['type'] = dataType
                    milliQanOfflineDataset['file'] = fileNumber
                    milliQanOfflineDataset['run'] = runNumber
                    db.milliQanOfflineDatasets.insert_one(milliQanOfflineDataset)
                else:
                    milliQanOfflineDataset['_id'] = _id
                    milliQanOfflineDataset['site'] = site
                    milliQanOfflineDataset['location'] = destination.split(':')[-1]
                    db.milliQanOfflineDatasets.insert_one(milliQanOfflineDataset)

    os.system("echo 'Transferred {0:.2f} MB in {1} file(s).' >> {2}".format(mbytesTransferred, nTransferred, logFile))

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input directory of files to be transferred", type=str, default='/store/user/milliqan/trees/v35/bar/')
    parser.add_argument('-d', '--destination', help="Destination for files to be transferred to", type=str, default='milliqan@tau.physics.ucsb.edu:/net/cms18/cms18r0/milliqan/Run3Offline/v35/bar/')
    parser.add_argument('-f', '--force', help='Option to force all files to transfer even if they exist at destination', action='store_true')
    parser.add_argument('-l', '--logFile', help='Log file to save output', default='/home/milliqan/scratch0/milliqanTools/out_transferOffline.log')
    parser.add_argument('--debug', help='Option to enable debugging', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    print("In transfer script")

    args = parse_args()
    site = None

    if 'ucsb' in args.destination:
        site = 'UCSB'
    elif 'osu' in args.destination:
        site = 'OSU'
    else:
        print("Need to provide a real data site")
        sys.exit(0)

    version = args.input.split('/')[5]

    transferOfflineFiles(args.input, args.destination, site, version, args.logFile, force=args.force, debug=args.debug)
    transferOfflineFiles('/store/user/milliqan/trees/v35/slab/', 'milliqan@tau.physics.ucsb.edu:/net/cms18/cms18r0/milliqan/Run3Offline/v35/slab/', site, version, args.logFile, force=args.force, debug=args.debug)

