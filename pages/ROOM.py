import sqlite3,datetime
from flet import *
def room_view(page:Page,theme,alert):
    def save(e):
        page.update()
    def upd_services(e,how):
        if how=='-':e.control.parent.controls.remove(e.control)
        elif how=='+':c_services.controls.append(Row([IconButton(icon=Icons.REMOVE,icon_color='red',on_click=lambda e,how='-':upd_services(e,how)),t_date,t_time,t_service,t_price,IconButton(icon=Icons.ADD,icon_color='green',on_click=lambda e,how='+':upd_services(e,how))]))
        page.update()
    floor,room=page.data['floor'],page.data['room']
    db=sqlite3.connect('db.db')
    color,price=db.execute('select STATUS,PRICE from ROOMS where FLOOR=? and ROOM=?',(floor,room,)).fetchall()
    clean=db.execute('select DATE,TIME from CLEANINGS where FLOOR=? and ROOM=?',(floor,room,)).fetchall()
    db.close()
    t_guest=TextField(label='GUEST')
    t_id=TextField(label='ID')
    t_checkin=TextField(label='CHECK-IN')
    t_nights=TextField(label='NIGHTS')
    t_bill=TextField(label='BILL')
    t_date=TextField(label='DATE',value=datetime.date.today())
    t_time=TextField(label='TIME',value=datetime.datetime.now().time())
    t_service=TextField(label='SERVICE')
    t_price=TextField(label='PRICE')
    c_services=Column([Row([t_date,t_time,t_service,t_price,IconButton(icon=Icons.ADD,icon_color='green',on_click=lambda e,how='+':upd_services(e,how))])])
    return Column([Row([Switch(on_change=theme),Text('daHotel',color='orange',size=30),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.go('/HOME'))],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([Text(f'FLOOR {str(floor)}, ROOM {str(room)}, PRICE $.{price} PER NIGHT',color=color,size=15)],alignment=MainAxisAlignment.CENTER),
                   Row([Column([Text(f'LAST CLEAN IN {clean}'),t_guest,t_id,t_checkin,t_nights,t_bill])],alignment=MainAxisAlignment.CENTER),
                   Row([c_services],alignment=MainAxisAlignment.CENTER),
                   Row([ElevatedButton('SAVE',on_click=save)],alignment=MainAxisAlignment.CENTER)])