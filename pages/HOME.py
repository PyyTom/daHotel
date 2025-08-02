import sqlite3
from flet import *
def home_view(page:Page,theme,alert):
    def refresh(e):
        db=sqlite3.connect('db.db')
        if db.execute('select * from ROOMS').fetchall()!=[]:
            n=0
            for floor in db.execute('select FLOOR from ROOMS group by FLOOR order by FLOOR').fetchall():
                if n==0:c_rooms.controls=[Row([Text('FLOOR '+str(floor[0]),width=100)])]
                else:c_rooms.controls.append(Row([Text('FLOOR '+str(floor[0]),width=100)]))
                for room in range(1,db.execute('select count(*) from ROOMS where FLOOR=?',(floor[0],)).fetchone()[0]+1):
                    color=db.execute('select STATUS from ROOMS where FLOOR=? and ROOM=?',(floor[0],room,)).fetchone()[0]
                    c_rooms.controls[n].controls.append(ElevatedButton(room,color=color,on_click=lambda e,floor=floor[0]:view_room(e,floor)))
                n+=1
        db.close()
    def view_room(e,floor):
        page.data={'floor':floor,'room':e.control.text}
        page.go('/ROOM')
    c_rooms=Column()
    refresh('')
    return Column([Row([Switch(on_change=theme),Text('daHotel',color='orange',size=30),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.window.destroy())],alignment=MainAxisAlignment.CENTER),
                   Row([ElevatedButton('EDITOR',on_click=lambda _:page.go('/EDITOR'))],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([Text('ROOMS',color='orange',size=15)],alignment=MainAxisAlignment.CENTER),
                   Row([c_rooms],alignment=MainAxisAlignment.CENTER),
                   Divider()])