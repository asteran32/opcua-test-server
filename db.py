import time
import config

from pymongo import MongoClient

class mongoDB:
    def __init__(self):
        self.client = None
        self.dir = config.DBConfig.CSV_PATH
        self.connect()

    def connect(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        return

    def commit(self, fname):
        if self.client is None:
            return
        db = self.client['plc']
        collection = db['fs300']

        timestamp = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        csv = self.dir + fname
        result = collection.find_one({"name":fname})
        if result :
            data = collection.update_one(
                {"name":fname}, {"$set":{"date": timestamp}}
            )
        else:
            data = collection.insert_one({
                "name": fname,
                "path": csv,
                "date": timestamp
            })

        return
        

