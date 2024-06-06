#!/usr/bin/python3

import glob
import os
import time
import socket
import sys
from mongoConnect import mongoConnect
import transferFiles
import shutil
import argparse
from utilities import fileTypes
import ROOT as r

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-m", "--move", help="Move files to new location", action='store_true')
    parser.add_argument("-u", "--update", help="Update file location", action='store_true')
    parser.add_argument("-s", "--site", help="Site where data is located", type=str, required=True)
    parser.add_argument("-i", "--input", help="Input directory with data to be moved or updated", type=str, required=True)
    parser.add_argument("-o", "--output", help="Output directory where data should be moved to", type=str)
    parser.add_argument("-r", "--raw", help="Option to run with raw data (without option will run on offline data", action='store_true')
    parser.add_argument("-d", "--debug", help="Option for debugging", action='store_true')
    args = parser.parse_args()
    return args

def getFileDetails(filename):
    runNumber = filename.split("Run")[-1].split(".")[0]
    fileNumber = filename.split(".")[1].split("_")[0]
    fileType = filename.split("_")[0]
    return int(runNumber), int(fileNumber), fileType

def goodFile(filename):
    if not filename.endswith('.root'): return False
    if len(filename.split('.')) != 3: return False
    if filename.split("_")[0] not in fileTypes: return False
    return True

def moveFiles(db, site, source, dest):
    for filename in os.listdir(source):

        if not filename.endswith(".root"): continue

        runNumber, fileNumber, fileType = getFileDetails(filename)

        newLocation = str(dest + '/' + filename)

        shutil.move(os.path.join(source, filename), os.path.join(dest, filename))
    
        db.milliQanRawDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType}, 
                                          { '$set': {"location" : newLocation}})

        print("Moved file {0} and updated entry in MongoDB".format(filename))


def updateLocations(db, directory, site, raw=True, debug=False):
    filesProcessed = 0
    tempDebug = True

    #temp
    copyFrom = db.milliQanOfflineDatasets.find_one({"_id": "1300_2_v34_MilliQan_OSU"})
    print("fopyFrom", copyFrom)
    return
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if not goodFile(filename): continue
            if filesProcessed > 1: break

            runNumber, fileNumber, fileType = getFileDetails(filename)

            if debug: print('File: {0} \n\tRunNumber: {1} \n\tFileNumber: {2} \n\tFileType: {3} \n\tDirectory: {4}'.format(filename, runNumber, fileNumber, fileType, directory))

            if raw:
                db.milliQanRawDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, "type" : fileType},
                                                  { '$set': {"location" : directory}})
            if tempDebug:
                version = directory.split('/')[5]
                _id = "{}_{}_{}_{}_{}".format(runNumber, fileNumber, version, fileType, "OSU")
                _idMod = "{}_{}_{}_{}_{}".format(runNumber, fileNumber, version, fileType, "Other")
                initialEntry = db.milliQanOfflineDatasets.find_one({"_id": _idMod})
                print("initialEntry:", initialEntry, initialEntry==True)
                if 'chanMap' not in initialEntry.keys():
                    fin = r.TFile.Open(directory + filename)
                    isMatched = fin.Get("triggerMatched_true")
                    matched=False
                    try:
                        if isMatched.GetName() == "triggerMatched_true":
                            matched=True
                            print("file is trigger Matched")
                    except:
                        print("not trigger matched")
                    fin.Close()
                    db.milliQanOfflineDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site,
                                                            "type" : fileType, "version": version},
                                                            { '$set': {"location" : directory, 
                                                                       "site": "OSU", 
                                                                        "_id": _id,
                                                                        "timingCalibrations": copyFrom['timingCalibrations'],
                                                                        "speAreas": copyFrom['speAreas'],
                                                                        "chanMap": copyFrom['chanMap'],
                                                                        "pedestals": copyFrom['pedestals'],
                                                                        "pulseParams": copyFrom['pulseParams'],
                                                                        "sampleRate": copyFrom['sampleRate'],
                                                                        "matched": matched,
                                                            }}, upsert=True)
                elif initialEntry['location'].startswith('/var/opt/'):
                    print("updating locations...")
                    success = db.milliQanOfflineDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : "Other",
                                                            "type" : fileType, "version": version},
                                                            { '$set': {"location" : directory, "site": "OSU", "_id": _id}})
                    print("updated location", success.matched_count, directory)
            else:
                version = directory.split('/')[5]
                db.milliQanOfflineDatasets.update_one({ "run" : runNumber, "file" : fileNumber, "site" : site, 
                                                        "type" : fileType, "version": version},
                                                        { '$set': {"location" : directory}}, upsert=True)
            print("Updated database for file {0}".format(filename))
            filesProcessed+=1

def main():
    
    args = parse_args()
    
    if not args.move and not args.update:
        print("Error need to either move or update file locations... exiting")
        sys.exit(0)

    if args.move:
        if not args.output:
            print("Error need to specify an output directory with -o option")
            sys.exit(0)
        if not os.path.exists(args.output):
            print("Path: {0} does not exist".format(args.output))
            sys.exit(0)

    if not os.path.exists(args.input):
        print("Path: {0} does not exist".format(args.input))
        sys.exit(0)
    
    db = mongoConnect()

    if args.raw:
        if db.milliQanRawDatasets.count_documents({"site" : args.site}, limit=1)==0:
            print("Site: {0} is not a valid site".format(args.site))
            sys.exit(0)
    else:
        if db.milliQanOfflineDatasets.count_documents({"site" : args.site}, limit=1)==0:
            print("Site: {0} is not a valid site".format(args.site))
            sys.exit(0)


    if args.move:
        moveFiles(db, args.site, args.input, args.output)

    elif args.update:
        updateLocations(db, args.input, args.site, raw=args.raw, debug=args.debug)




if __name__ == "__main__":

    main()
