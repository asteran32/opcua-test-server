import os
import csv
import time
import config
import db

class data_sheet:
    def __init__(self):
        self.fname = ""
        self.dir = "./data/"
        self.row = ""
        # make file
        self.check_dir()
        self.createCSV()

    # check directory
    def check_dir(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    # daily schedule
    def createCSV(self):
        # make new file
        self.fname = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time())) + ".csv"
        f = open(os.path.join(self.dir, self.fname), 'w', encoding='utf-8')
        f.close()
        return
    
    # every minute schedule
    def wirteCSV(self):
        csv_path = os.path.join(self.dir, self.fname)
        if os.path.exists(csv_path):
            f = open(csv_path, 'a', encoding='utf-8', newline='')
            w = csv.writer(f)
            w.writerow(self.row)
            f.close()
        else:
            self.createCSV()

    def uploadCSV(self):
        db = db.mongoDB()
        csv_path = os.path.join(self.dir, self.fname)
        if os.path.exists(csv_path):
            db.commit(self.fname)
        return

            

            


