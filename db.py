import time
import config

from pymongo import MongoClient

class mongoDB:
    def __init__(self):
        self.add = "mongodb://localhost:27017/"
        self.client = "None"

    def connect(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        if self.client is None:
            return

    def commit(self, fname):
        self.connect()
        db = self.client['plc']
        collection = db['fs300']

        result = collection.find_one({"name":fname})
        if result :
            data = collection.updateOne(
                {"name":fname}, {"date": time.strftime('%Y-%m-%d %X', time.localtime(time.time()))}
            )

        else:
            data = collection.insert_one({
                "name": fname,
                "path": config.DatabaseConfig.CSV_PATH + fname,
                "date": time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
            })

        self.close()

        def close(self):
            self.client.close()


