import sqlite3
class DB:
    def __init__(self,path='db.db'):
        self.path=path
        with sqlite3.connect(self.path) as db:
            db.execute('create table if not exists ROOMS(FLOOR int, ROOM int, STATUS text, PRICE float, NOTES text)')
            db.execute('create table if not exists GUESTS(ROOM,NAME,DOC,ADDRESS,PHONE,MAIL,NOTES)')
    def check_if_empty(self):
        with sqlite3.connect(self.path) as db:return db.execute('select count(*) from ROOMS').fetchone()[0]
    def save_set_up(self,floors,rooms,price):
        with sqlite3.connect(self.path) as db:
            room=1
            for floor in range(1,floors+1):
                for r in range(rooms):
                    db.execute('insert into ROOMS values(?,?,?,?,?)',(floor,room,'FREE',price,'',))
                    room+=1
    def get_rooms(self,floor):
        with sqlite3.connect(self.path) as db:return db.execute('select * from ROOMS where FLOOR=?',(floor[0],)).fetchall()
    def get_floors(self):
        with sqlite3.connect(self.path) as db:return db.execute('select FLOOR from ROOMS group by FLOOR').fetchall()
    def get_room(self,room):
        with sqlite3.connect(self.path) as db:return db.execute('select * from ROOMS where ROOM=?',(room,)).fetchone()
    def get_guest(self,room):
        with sqlite3.connect(self.path) as db:return db.execute('select * from GUESTS where ROOM=?',(room,)).fetchall()    
    def update(self,room,price,notes):
        with sqlite3.connect(self.path) as db:db.execute('update ROOMS set PRICE=?,NOTES=? where ROOM=?',(price,notes.upper(),room,))
