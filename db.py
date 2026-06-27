import sqlite3
class DB:
    def __init__(self,path='db.db'):
        self.path=path
        with sqlite3.connect(self.path) as db:
            db.execute('create table if not exists ROOMS(FLOOR int, ROOM int, STATUS text, PRICE float, NOTES text)')
            db.execute('create table if not exists GUESTS(NAME,ID,ADDRESS,PHONE,MAIL,NOTES)')
            db.execute('create table if not exists BOOKINGS(ROOM,ID,DATE,NIGHTS,BILL,NOTES)')
            db.execute('create table if not exists SERVICES(ROOM,ID,DATE,SERVICE,PRICE,NOTES)')
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
    def get_guest(self,id):
        with sqlite3.connect(self.path) as db:return db.execute('select * from GUESTS where ID=?',(id,)).fetchall()
    def get_services(self,room):
        with sqlite3.connect(self.path) as db:return db.execute('select * from SERVICES where ROOM=?',(room,)).fetchall()
    def get_booking(self,room):
        with sqlite3.connect(self.path) as db:
            a=db.execute('select ID,NIGHTS,NOTES from BOOKINGS where ROOM=?',(room,)).fetchone()
            b=db.execute('select NAME,ADDRESS,PHONE,MAIL from GUESTS where ID=?',(a[0],)).fetchone()
            return [b[0],a[0],a[1],b[1],b[2],b[3],a[2]]
    def get_bill(self,room):
        with sqlite3.connect(self.path) as db:return db.execute('select BILL from BOOKINGS where ROOM=?',(room,)).fetchone()[0]
    def update(self,room,status,price,notes):
        with sqlite3.connect(self.path) as db:db.execute('update ROOMS set STATUS=?,PRICE=?,NOTES=? where ROOM=?',(status,price,notes.upper(),room,))
    def add_service(self,date,room,service,price,notes):
        with sqlite3.connect(self.path) as db:
            db.execute('insert into SERVICES values(?,?,?,?,?,?)',(room,'',date,service.upper(),price,notes.upper(),))
            db.execute('update BOOKINGS set BILL=BILL+? where ROOM=?',(price,room,))
    def checkin(self,room,name,guest_id,date,nights,bill,address,phone,mail,notes,how):
        if how=='booking':status='RESERVED'
        else:status='OCCUPIED'
        with sqlite3.connect(self.path) as db:
            db.execute('insert into BOOKINGS values(?,?,?,?,?,?)',(room,guest_id.upper(),date,nights,bill,notes.upper(),))
            db.execute('update ROOMS set STATUS=? where ROOM=?',(status,room,))
            if db.execute('select * from GUESTS where ID=?',(guest_id,)).fetchall():db.execute('update GUESTS set NAME=?,ADDRESS=?,PHONE=?,MAIL=?,NOTES=? where ID=?',(name.upper(),address.upper(),phone,mail.upper(),notes.upper(),guest_id.upper(),))
            else:db.execute('insert into GUESTS values(?,?,?,?,?,?)',(name.upper(),guest_id.upper(),address.upper(),phone,mail.upper(),notes.upper(),))
    def checkout(self,room):
        with sqlite3.connect(self.path) as db:
            db.execute('update ROOMS set STATUS="FREE" where ROOM=?',(room,))
            db.execute('delete from BOOKINGS where ROOM=?',(room,))
            db.execute('delete from SERVICES where ROOM=?',(room,))
    def get_free_rooms(self):
        with sqlite3.connect(self.path) as db:return db.execute('select * from ROOMS where STATUS="FREE" order by FLOOR,ROOM').fetchall()
