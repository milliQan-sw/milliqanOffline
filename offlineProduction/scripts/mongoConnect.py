from pymongo import MongoClient

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


