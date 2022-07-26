from pymongo import MongoClient
import glob
import os
# pprint library is used to make the output look more pretty
from pprint import pprint
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient("mongodb+srv://mcitron:milliqan@testcluster.ffkkz.mongodb.net/?retryWrites=true&w=majority")
db=client.milliQanData
printRaw=False
printOffline=True
# Issue the serverStatus command and print the results
if printRaw:
    print ("RAW dataset")
    for dataset in db.milliQanRawDatasets.find({"run": {"$gt": 0}}):
        pprint(dataset)
if printOffline:
    print ("Offline dataset")
    for dataset in db.milliQanOfflineDatasets.find({"run": {"$gt": 0}}):
        pprint(dataset)

