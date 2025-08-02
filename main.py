import sqlite3
db=sqlite3.connect('db.db')
db.execute('create table if not exists ROOMS(FLOOR integer,ROOM integer,STATUS,PRICE)')
db.execute('create table if not exists CLEANINGS(FLOOR integer,ROOM integer,DATE,TIME)')
db.execute('create table if not exists GUESTS(FLOOR integer,ROOM integer,NAME,ID,CHECKIN,NIGHTS integer,BILL float)')
db.execute('create table if not exists SERVICES(FLOOR integer,ROOM integer,SERVICE,PRICE float)')
db.close()
from flet import *
from pages.HOME import home_view
from pages.EDITOR import editor_view
from pages.ROOM import room_view
def main(page: Page):
    def theme(e):
        page.theme_mode = 'LIGHT' if page.theme_mode == 'DARK' else 'DARK'
        page.update()
    def route_to(route):
        page.clean()
        if route=='/':page.add(home_view(page,theme,alert))
        elif route == '/HOME':page.add(home_view(page,theme,alert))
        elif route == '/EDITOR':page.add(editor_view(page,theme,alert))
        elif route == '/ROOM':page.add(room_view(page,theme,alert))
        page.update()
    page.theme_mode = 'DARK'
    page.window.full_screen = True
    alert=AlertDialog(title=Text(''))
    page.add(alert)
    page.on_route_change = lambda e: route_to(e.route)
    page.go('/HOME')
app(main)