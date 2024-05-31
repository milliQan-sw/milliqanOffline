import sys,os
import bson
from pymongo import MongoClient

#function to dump the offline and raw datasets to bson file
def dump(client):
    dump(["milliQanOfflineDatasets","milliQanRawDatasets"],db,dest)

#function to upload dataset with name (db_name) to mongoDB
def upload(client, db_name):
    db=client[db_name]
    raw = open(db_name+'.bson', 'rb+')
    db[db_name].insert_many(bson.decode_all(raw.read()), ordered=False)

if __name__ == "__main__":

    client = MongoClient("mongodb.physics.ucdavis.edu",port=27017,username='mcitron',password='!!!Phys-2024-Mongo-Citron!!!', authSource='admin', authMechanism='SCRAM-SHA-256')

    #dump(client)

    #upload(client, 'milliQanOfflineDatasets')
    #upload(client, 'milliQanRawDatasets')



