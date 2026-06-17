import sqlite3
class DB:
    def __init__(self,path='db.db'):
        self.path=path
        with sqlite3.connect(self.path) as db:db.execute('create table if not exists ROOMS(FLOOR int, ROOM int, STATUS text, PRICE float, NOTES text)')
    def check_if_empty(self):
        with sqlite3.connect(self.path) as db:return db.execute('select count(*) from ROOMS').fetchone()[0]
    def get_set_up(self):
        with sqlite3.connect(self.path) as db:return db.execute('select * from ROOMS').fetchall()
