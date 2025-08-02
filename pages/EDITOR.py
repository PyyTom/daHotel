import sqlite3
from flet import *
def editor_view(page:Page,theme,alert):
    def save_floors(e):
        if t_floor.value=='' or t_rooms.value=='' or t_rooms.value==0:alert.title=Text('EMPTY FIELDS')
        else:
            db=sqlite3.connect('db.db')
            if db.execute('select * from ROOMS where FLOOR=?',(t_floor.value,)).fetchall()==[]:
                for r in range(1,int(t_rooms.value)+1):
                    db.execute('insert into ROOMS values(?,?,?)',(t_floor.value,r,'green'))
                    db.commit()
                    alert.title=Text(f'FLOOR {t_floor.value} SUCCESSFULLY CREATED WITH {t_rooms.value} FREE ROOMS')
                t_floor.value=0
                t_rooms.value=0
            else:alert.title=Text('FLOOR ALREADY EXISTS')
            db.close()
        page.open(alert)
        page.update()
    t_floor=TextField(label='FLOOR',keyboard_type=KeyboardType.NUMBER,value=0)
    t_rooms=TextField(label='TOTAL ROOMS',keyboard_type=KeyboardType.NUMBER,value=0)
    return Column([Row([Switch(on_change=theme),Text('daHotel',color='orange',size=30),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.go('/HOME'))],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([Column([t_floor,t_rooms,ElevatedButton('SAVE',on_click=save_floors)])],alignment=MainAxisAlignment.CENTER)])