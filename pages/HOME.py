import sqlite3
from flet import *
def home_view(page:Page,theme,alert):
    def refresh(e):
        db=sqlite3.connect('db.db')
        if db.execute('select * from ROOMS').fetchall()!=[]:
            column.controls=[Row([Text(floor[0],width=100)]) for floor in db.execute('select * from ROOMS group by FLOOR').fetchall()]
            for f in range(len(column.controls)):
                data=db.execute('select * from ROOMS where FLOOR=?',(column.controls[f].controls[0].value,)).fetchall()
                for room in data:column.controls[f].controls.append(ElevatedButton(str(room[1])+'\n'+str(room[3]),color=room[2],width=50,on_click=lambda e,floor=column.controls[f].controls[0].value:show_room(e,floor)))
        db.close()
        page.update()
    def show_room(e,floor):
        page.data={'floor':floor,'room':(e.control.text).split('\n')[0],'price':(e.control.text).split('\n')[1]}
        page.go('/ROOM')
    column=Column()
    refresh('')
    return Column([Row([Switch(on_change=theme),Text('daHotel',color='orange',size=30),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.window.destroy())],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([Text('ROOMS',color='orange',size=15)],alignment=MainAxisAlignment.CENTER),
                   Row([column],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([ElevatedButton('EDITOR',on_click=lambda _:page.go('/EDITOR'))],alignment=MainAxisAlignment.CENTER)])
