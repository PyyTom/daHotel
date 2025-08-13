import sqlite3
from flet import *
def editor_view(page:Page,theme,alert):
    def refresh(e):
        def remove(e):
            db=sqlite3.connect('db.db')
            floor,price=e.control.content.controls[0].value,e.control.content.controls[2].value
            db.execute('delete from ROOMS where FLOOR=? and PRICE=?',(floor,price,))
            db.commit()
            db.close()
            refresh('')
        column.controls=[]
        db=sqlite3.connect('db.db')
        for data in db.execute('select FLOOR,count(ROOM),PRICE from ROOMS group by FLOOR,PRICE order by FLOOR,PRICE').fetchall():
            column.controls.append(Container(content=Row([Text(data[0],width=100),Text(data[1],width=100),Text(data[2],width=100)],alignment=MainAxisAlignment.CENTER),on_click=remove))
        db.close()
        page.update()
    def save(e):
        db=sqlite3.connect('db.db')
        if db.execute('select * from ROOMS where FLOOR=?',(t_floor.value,)).fetchall()==[]:start=1
        else:start=len(db.execute('select * from ROOMS where FLOOR=?',(t_floor.value,)).fetchall())+1
        for room in range(start,start+int(t_rooms.value)):
            db.execute('insert into ROOMS values(?,?,?,?)',(t_floor.value,room,'green',t_price.value,))
            db.commit()
            db.execute('insert into CLEANINGS values(?,?,?,?)',(t_floor.value,room,0,0,))
            db.commit()
        alert.title=Text('FLOORS CORRECTLY UPDATED')
        db.close()
        page.open(alert)
        t_floor.value=t_rooms.value=t_price.value=0
        refresh('')
    t_floor=TextField(label='FLOOR',keyboard_type=KeyboardType.NUMBER,value=0,width=100)
    t_rooms=TextField(label='ROOMS',keyboard_type=KeyboardType.NUMBER,value=0,width=100)
    t_price=TextField(label='PRICE',keyboard_type=KeyboardType.NUMBER,value=0,width=100)
    column=Column()
    try:refresh('')
    except:pass
    return Column([Row([Switch(on_change=theme),Text('daHotel',color='orange',size=30),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.go('/HOME'))],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([t_floor,t_rooms,t_price,ElevatedButton('SAVE',on_click=save)],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([Text('ROOMS CONFIGURATION',size=20,color='orange')],alignment=MainAxisAlignment.CENTER),
                   Row([Text('FLOOR',width=100),Text('ROOMS',width=100),Text('PRICE',width=100)],alignment=MainAxisAlignment.CENTER),
                   Row([column],alignment=MainAxisAlignment.CENTER)])
