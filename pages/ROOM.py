import sqlite3,datetime
from flet import *
def room_view(page:Page,theme,alert):
    def refresh(e):
        t_service.value=t_price.value=''
        db=sqlite3.connect('db.db')
        color=db.execute('select STATUS from ROOMS where FLOOR=? and ROOM=?',(floor,room,)).fetchone()[0]
        cleaning_date,cleaning_time=db.execute('select DATE,TIME from CLEANINGS where FLOOR=? and ROOM=?',(floor,room,)).fetchone()
        r_room.controls=[Text(f'FLOOR {str(floor)}, ROOM {str(room)}, PRICE $.{price} PER NIGHT',color=color,size=20)]
        r_cleaning.controls=[Text(f'LAST CLEAN IN {cleaning_date} AT {cleaning_time}'),ElevatedButton('CLEAN NOW',on_click=clean_now)]
        if color=='red' or color=='orange':
            t_name.value,t_id.value,t_checkin.value,t_nights.value,t_bill.value=db.execute('select NAME,ID,CHECKIN,NIGHTS,BILL from GUESTS where FLOOR=? and ROOM=?',(floor,room,)).fetchone()
            c_services.controls=[Divider(),
                                 Row([Text('SERVICES',size=20)],alignment=MainAxisAlignment.CENTER),
                                 Row([t_service,t_price,ElevatedButton('BUY',on_click=buy_service)],alignment=MainAxisAlignment.CENTER)]        
            if db.execute('select * from SERVICES where FLOOR=? and ROOM=?',(floor,room,)).fetchall()!=[]:
                for service in db.execute('select DATE,TIME,SERVICE,PRICE from SERVICES where FLOOR=? and ROOM=?',(floor,room,)).fetchall():c_services.controls.append(TextButton(service,on_click=remove_service))
        db.close()
        page.update()
    def checkout(e):
        db=sqlite3.connect('db.db')
        db.execute('update ROOMS set STATUS="green" where FLOOR=? and ROOM=?',(floor,room,))
        db.commit()
        db.execute('insert into BILLS select * from GUESTS where FLOOR=? and ROOM=?',(floor,room,))
        db.commit()
        db.execute('delete from GUESTS where FLOOR=? and ROOM=?',(floor,room,))
        db.commit()
        db.execute('delete from SERVICES where FLOOR=? and ROOM=?',(floor,room,))
        db.commit()
        db.close()
        alert.title=Text('CHECK-OUT CORRECTLY EXECUTED')
        page.open(alert)
        page.go('/HOME')
    def update_bill(e):
        db=sqlite3.connect('db.db')
        t_bill.value=int(t_nights.value)*int(db.execute('select PRICE from ROOMS where FLOOR=? and ROOM=?',(floor,room,)).fetchone()[0])
        db.close()
        page.update()
    def save(e):
        if t_name.value=='' or t_id.value=='' or t_checkin.value=='' or t_nights.value=='':alert.title=Text('EMPTY FIELDS')
        else:
            db=sqlite3.connect('db.db')
            if db.execute('select STATUS from ROOMS where FLOOR=? and ROOM=?',(floor,room,)).fetchone()[0]=='green':
                db.execute('update ROOMS set STATUS="red" where FLOOR=? and ROOM=?',(floor,room,))
                db.execute('insert into GUESTS values(?,?,?,?,?,?,?)',(floor,room,(t_name.value).upper(),(t_id.value).upper(),t_checkin.value,t_nights.value,t_bill.value,))
            else:db.execute('update GUESTS set NAME=?,ID=?,CHECKIN=?,NIGHTS=? where FLOOR=? and ROOM=?',((t_name.value).upper(),(t_id.value).upper(),t_checkin.value,t_nights.value,floor,room,))
            db.commit()
            db.close()
            alert.title=Text('GUEST CORRECTLY SAVED')
        page.open(alert)
        page.go('/HOME')
    def clean_now(e):
        date,time=datetime.datetime.today().strftime('%d/%m/%Y'),datetime.datetime.now().strftime('%H:%M')
        db=sqlite3.connect('db.db')
        db.execute('update CLEANINGS set DATE=?,TIME=? where FLOOR=? and ROOM=?',(date,time,floor,room,))
        db.commit()
        db.close()
        refresh('')
    def buy_service(e):
        if t_service.value=='' or t_price.value=='':
            alert.title=Text('EMPTY FIELDS')
            page.open(alert)
        else:
            db=sqlite3.connect('db.db')
            db.execute('insert into SERVICES values(?,?,?,?,?,?)',(floor,room,datetime.datetime.today().strftime('%d/%m/%Y'),datetime.datetime.now().strftime('%H:%M'),(t_service.value).upper(),t_price.value))
            db.commit()
            db.execute('update GUESTS set BILL=BILL+? where FLOOR=? and ROOM=?',(t_price.value,floor,room,))
            db.commit()
            db.close()
            refresh('')
    def remove_service(e):
        data=[floor,room]
        for i in e.control.text:data.append(i)
        db=sqlite3.connect('db.db')
        db.execute('delete from SERVICES where FLOOR=? and ROOM=? and DATE=? and TIME=? and SERVICE=? and PRICE=?',data)
        db.commit()
        db.execute('update GUESTS set BILL=BILL-? where FLOOR=? and ROOM=?',(e.control.text[3],floor,room,))
        db.commit()
        db.close()
        refresh('')
    floor,room,price=page.data['floor'],page.data['room'],page.data['price']
    r_room=Row(alignment=MainAxisAlignment.CENTER)
    r_cleaning=Row(alignment=MainAxisAlignment.CENTER)
    t_name=TextField(label='GUEST')
    t_id=TextField(label='ID')
    t_checkin=TextField(label='CHECK-IN',value=datetime.datetime.today().strftime('%d/%m/%Y'),width=200)
    t_nights=TextField(label='NIGHTS',value=1,keyboard_type=KeyboardType.NUMBER,on_change=update_bill,width=100)
    l_bill=Text('BILL:',width=50)
    t_bill=Text(0.0,width=100)
    t_service=TextField(label='SERVICE')
    t_price=TextField(label='PRICE',value=0.0)
    c_services=Column()
    column=Column([Row([t_name,t_id,t_checkin,t_nights,l_bill,t_bill],alignment=MainAxisAlignment.CENTER),
                   Row([ElevatedButton('CHECKOUT',on_click=checkout),ElevatedButton('SAVE',on_click=save)],alignment=MainAxisAlignment.CENTER),])
    refresh('')
    return Column([Row([Switch(on_change=theme),Text('daHotel',color='orange',size=30),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.go('/HOME'))],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([r_room],alignment=MainAxisAlignment.CENTER),
                   Row([r_cleaning],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([column],alignment=MainAxisAlignment.CENTER),
                   Row([c_services],alignment=MainAxisAlignment.CENTER)])
