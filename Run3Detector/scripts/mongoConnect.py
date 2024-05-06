from pymongo import MongoClient

def mongoConnect():
    try:
        client = MongoClient("mongodb.physics.ucdavis.edu",port=27017,username='mcitron',password='!!!Phys-2024-Mongo-Citron!!!', authSource='admin', authMechanism='SCRAM-SHA-256')
        db=client['milliQan']
    except:
        print ("Could not publish as failed to connect to mongo server")
        return
    return db

if __name__ == "__main__":

    db = mongoConnect()

    collection_stats = db.command("collstats", "milliQanRawDatasets")
    print(collection_stats)
