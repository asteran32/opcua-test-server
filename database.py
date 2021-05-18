import time
import sqlite3
import config
#################################
# 경량 디스크 기반 데이터베이스   #
# Schedule every a hours        #
# id : pk                       #
# name : file name              #
# path : server file location   #
# date : file upload date       #
# ubuntu command : sqlitebrowser#
#################################

class DB:
    def __init__(self):
        self.c = None
        self.cur = None
        print("light SQL version :", sqlite3.version)

    def connect(self):
        self.c = sqlite3.connect(config.DBConfig.DB_PATH)
        self.c.isolation_level = None
        self.cur = self.c.cursor()
    
    def commit(self, fname):
        self.connect()
        if self.c is None:
            print("Can not connect at database. Please check again")
            return 
        # if file is exist => modify
        csvpath = config.DBConfig.CSV_PATH + fname
        t = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
        self.cur.execute("SELECT * FROM fs300 WHERE name = ?", (fname, ))

        if self.cur.fetchone() is not None:
            self.cur.execute("UPDATE fs300 SET date = ? WHERE name = ?", (t, fname))
        # else => create
        else:
            self.cur.execute("INSERT INTO fs300(name, path, date) VALUES(?, ?, ?)", (fname, csvpath, t))
        self.c.commit()
        self.c.close()

    def close(self):
        self.c.close()

#cur.execute("INSERT INTO fs300 (name, path, date) VALUES(?, ?, ?)", ('2021-05-14-20-08.csv', '../data/2021-05-14-20-08.csv', '2021-05-14-20-08'))