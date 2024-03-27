from mongoConnect import mongoConnect
import subprocess
import glob
import os

def addToMongoDB(source,force=True,maxNum=100):
    db = mongoConnect()

    nTransferred = 0
    mbytesTransferred = 0
    # os.system("echo '" + time.strftime("%c") + " Attempting to transfer data files ...' >> " + logFile)
    allIds = []
    allInputs = []
    allLocations = []
    iFile = -1
    for inputFile in sorted(glob.glob(os.path.join(source, "*.dat")), key=os.path.getmtime, reverse=True):
        iFile += 1
        if iFile >= maxNum: break
        #Details for database entry
        with open(inputFile,"r") as f:
            for line in f.readlines():
                if "," not in line: continue
                line = line.strip()
                runNumber = line.split(",")[1].split("run=")[1]
                fileNumber = line.split(",")[2].split("file=")[1]
                location = line.split(",")[3].split("location=")[1]
                dataType= line.split(",")[4].split("type=")[1]
                site = line.split(",")[5].split("site=")[1]
                _id = "{}_{}_{}_{}".format(runNumber,fileNumber,dataType,site)
        allLocations.append(location)
        allIds.append(_id)
        allInputs.append(inputFile)
    idsOut,inputsOut,entriesInDB, currentLocations = checkMongoDB(db,allIds,allInputs,allLocations,force,offline=False,formosa=True)
    # print(idsOut,inputsOut,entriesInDB, currentLocations)
    # exit()
    for _id,inputFile,entryInMongo,currentLocation in zip(idsOut,inputsOut,entriesInDB, currentLocations):
        runNumber,fileNumber,dataType,site = _id.split("_")
        formosaRawDataset = {}
        formosaRawDataset["_id"] = _id
        try:
            formosaRawDataset["run"] = int(runNumber)
            formosaRawDataset["file"] = int(fileNumber)
        except:
            print("Incorrect format!", runNumber,fileNumber,dataType,site,currentLocation,inputFile)
        formosaRawDataset["type"] = dataType
        formosaRawDataset["site"] = site
        formosaRawDataset["location"] = currentLocation
        try:
            updateMongoDB(formosaRawDataset, db, replace = entryInMongo)
        except Exception as error:
            print("Error occured in updating database: ",error)
            continue
        subprocess.getstatusoutput("rm {}".format(inputFile))


def updateMongoDB(formosaRawDataset,db,replace):
    if replace:
        db.formosaRawDatasets.replace_one({"_id": formosaRawDataset["_id"]},formosaRawDataset)
    else:
        db.formosaRawDatasets.insert_one(formosaRawDataset)

def checkMongoDB(db,allIds,allInputs,allLocations,force,offline=False,formosa=False):
    nX = 0
    #Check for existing entry 
    idsOut = []
    inputsOut = []
    indicesToSkip = []
    entriesInDB = []
    locationInDb = []
    currentLocation = []
    if formosa:
        if offline:
            mongoDB = db.formosaOfflineDatasets
        else:
            mongoDB = db.formosaRawDatasets
    else:
        if offline:
            mongoDB = db.milliQanOfflineDatasets
        else:
            mongoDB = db.milliQanRawDatasets
    for x in (mongoDB.find({"_id" :{"$in": allIds}})):
        indexInDb = allIds.index(x["_id"])
        indicesToSkip.append(indexInDb)
    locationsOut = []
    for index in range(len(allIds)):
        if not force and index in indicesToSkip: continue
        idsOut.append(allIds[index])
        inputsOut.append(allInputs[index])
        locationsOut.append(allLocations[index])
        if index in indicesToSkip:
            entriesInDB.append(1)
        else:
            entriesInDB.append(0)
    return idsOut,inputsOut,entriesInDB, locationsOut


if __name__ == "__main__":

    source = "/eos/experiment/formosa/infoForMongo"

    addToMongoDB(source,force=False)
