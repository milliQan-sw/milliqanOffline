#!/usr/bin/python3
import argparse
import sys
import json
from mongoConnect import mongoConnect
from transferFiles import checkMongoDB, get_lock

fileTypes = ['MilliQan', 'MilliQanSlab', 'TriggerBoard', 'TriggerBoardSlab', 'MatchedEvents', 'MatchedEventsSlab']


def updateLocation(inputFile, destination, site,dataTypeI,database="milliQan", force=False):
  
    db = mongoConnect(database)
    print(database)
    if database == "milliQan":
        coll = db.milliQanOfflineDatasets
    elif database == "formosa":
        coll = db.formosaOfflineDatasets
    else:
        raise (ValueError, "Unknown database")
    get_lock('updateLocation')
 
    allIds = []
    allInputs = []

    #Details for database entry
    runNumber = int(inputFile.split("/")[-1].split("Run")[-1].split(".")[0])
    fileNumber = int(inputFile.split("/")[-1].split(".")[1].split("_")[0])
    dataType = inputFile.split("/")[-1].split("_")[0]
    if dataTypeI == "FORMOSA":
        dataType = dataTypeI
    version = inputFile.split('/')[-1].split("_")[2].split(".")[0]
    _id = "{}_{}_{}_{}_{}".format(runNumber,fileNumber,version,dataType,site)
    allIds.append(_id)
    allInputs.append(inputFile)
    formosa = database=="formosa"
    idsOut,inputsOut,entriesInDB, currentLocations = checkMongoDB(db, allIds, allInputs, force,formosa=formosa)
    print(idsOut)

    #Add entry to database
    print(_id)
    out = coll.update_one( 
        {"_id": _id}, 
        { 
            "$set": {"location": "/".join(destination.split("/")[:-1])+"/"+inputFile.split("/")[-1]}
        }
    )
    print(out)
    
    
    print("updated")


def removeEntries(criteria, site,database="milliQan"):

    db = mongoConnect()
    get_lock('remove_entries')

    #db.milliQanOfflineDatasets.find_one("site":"OSU", "run:600")
    
    #db.milliQanOfflineDatasets.delete_many({"site":"OSU", "run":600, "file":})
    print(criteria)
    if database == "milliQan":
        coll = db.milliQanOfflineDatasets
    elif database == "formosa":
        coll = db.formosaOfflineDatasets
    else:
        raise (ValueError, "Unknown database")
    col.delete_many(criteria)


if __name__ == "__main__":
    
    parser=argparse.ArgumentParser()
    parser.add_argument("-l", "--locationUpdate", help="Option to update file location in mongoDB", type=str, default="")
    parser.add_argument("-i", "--inputFile", help="Input File", type=str, default="")
    parser.add_argument("-s", "--site", help="Site location where file is stored", type=str, default="")
    parser.add_argument("-t", "--dataType", help="Data type", type=str, default="")
    parser.add_argument("-d", "--database", help="Data base", type=str, default="milliQan")
    parser.add_argument("-r", "--remove", help="Remove entries from mongoDB matching the given list", type=str, default="")
    parser.add_argument("-f", "--force", help="force update",action="store_true",default=False)
    args = parser.parse_args()

    if args.locationUpdate != "":
        if args.inputFile == "" or args.site == "":
            print("Error need to give an input file and the site")
            sys.exit(0)
        updateLocation(args.inputFile, args.locationUpdate, args.site,args.dataType,args.database)
        

    if args.remove != "":
        if args.site == "":
            print("Error need to give input site")
            sys.exit(0)
        removeDict = json.loads(args.remove)
        removeEntries(removeDict, args.site)
