import os
import csv
import time

class data_sheet:
    def __init__(self, tags):
        self.fname = ""
        self.dir = "data/"
        self.tag = tags
        self.row = ""
        
        # make file
        self.check_dir()
        self.create_file()

    # check directory
    def check_dir(self):
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

    # daily schedule / make new file
    def create_file(self):
        self.fname = time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".csv"
        fpath = self.dir + self.fname
        if not os.path.exists(fpath):
            with open(fpath, 'w', encoding='utf-8') as csvfile:
                w = csv.writer(csvfile)
                w.writerow(self.tag)
    
    # every minute schedule
    def wirte_data(self):
        csv_path = os.path.join(self.dir, self.fname)
        if os.path.exists(csv_path):
            with open(csv_path, 'a', encoding='utf-8', newline='') as csvfile:
                w = csv.writer(csvfile)
                w.writerow(self.row)