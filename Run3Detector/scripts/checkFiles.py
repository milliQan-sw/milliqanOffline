import os
from pymongo import MongoClient

##########################################################
## Script checks for files missing from mongoDB and DAQ pc
###########################################################

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

def checkDB(db, ids_):
    dbFiles = []
    for x in (db.milliQanRawDatasets.find({"_id" :{"$in": ids_}})):
        dbFiles.append(x["_id"])

    missingFiles = [x for x in ids_ if x not in dbFiles]

    return missingFiles



def checkRunList(site):

    ids_ = []
    fin = open('/var/log/MilliDAQ_RunList.log', 'r')
    for line in fin.readlines():
        line = line.split()
        run = line[0]
        subrun = line[1]
        if int(run) < 600: continue
        id_ = "{}_{}_{}_{}".format(run,subrun,'MilliQan',site)
        ids_.append(id_)

    fin.close()
    fin = open('/var/log/TriggerBoard_RunList.log', 'r')
    for line in fin.readlines():
        line = line.split()
        run = line[0]
        subrun = line[1]
        if int(run) < 600: continue
        id_ = "{}_{}_{}_{}".format(run,subrun,'TriggerBoard',site)
        ids_.append(id_)

    fin.close()
    fin = open('/var/log/Matched_RunList.log', 'r')
    for line in fin.readlines():
        line = line.split()
        run = line[0]
        subrun = line[1]
        if int(run) < 600: continue
        id_ = "{}_{}_{}_{}".format(run,subrun,'MatchedEvents',site)
        ids_.append(id_)
    fin.close()

    return ids_


def checkLocal(ids_):
    missingLocal = []
    for id_ in ids_:
        id_ = id_.split('_')
        filename = ''
        if 'MilliQan' in id_:
            filename = '{0}_Run{1}.{2}_default.root'.format(id_[2], id_[0], id_[1])
        elif 'TriggerBoard' in id_ or 'MatchedEvents' in id_:
            filename = '{0}_Run{1}.{2}.root'.format(id_[2], id_[0], id_[1])

        if not os.path.exists('/home/milliqan/data/' + filename):
            print("File {0} is missing from site and local!".format(filename))


if __name__ == '__main__':
    
    db = mongoConnect()
    ids_ = checkRunList('OSU')
    missingFiles = checkDB(db, ids_)
    checkLocal(missingFiles)

    ids_ = checkRunList('UCSB')
    missingFiles = checkDB(db, ids_)
    checkLocal(missingFiles)

