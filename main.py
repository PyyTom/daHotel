import flet
from db import DB
db=DB()
from ui import UI
status={'FREE':'green','OCCUPIED':'red','RESERVED':'blue','MAINTENAINCE':'orange'}
labels=['NAME','DOC','ADDRESS','PHONE','MAIL','NOTES']
def main(page:flet.Page):
    ui=UI(page)
    page.window.full_screen=True
    page.title='daHotel - PyTom - ES 2026'
    page.theme_mode='dark'
    def theme(e):
        page.theme_mode='dark' if page.theme_mode=='light' else 'light'
        page.update()
    def set_up(e):
        def check_set_up(e):
            def save_set_up(e):
                page.pop_dialog()
                db.save_set_up(int(r_rooms.controls[0].value),int(r_rooms.controls[1].value),float(r_rooms.controls[2].value),)
                page.show_dialog(ui.alert('SET UP CORRECTLY SAVED',[]))
                refresh(None)
            if all([r_rooms.controls[0].value,r_rooms.controls[1].value,r_rooms.controls[2].value]) and all([r_rooms.controls[0].value,r_rooms.controls[1].value,r_rooms.controls[2].value])!=0:
                page.show_dialog(ui.alert(f'SETTING UP {r_rooms.controls[0].value} FLOORS, {r_rooms.controls[1].value} ROOMS PER FLOOR, WITH STARTING PRICE $. {r_rooms.controls[2].value}. CONFIRM?',
                                [ui.button('YES','green',save_set_up),ui.button('NO','red',page.pop_dialog)]))
            else:page.show_dialog(ui.alert('INVALID FIELDS. CANNOT SET UP',[]))
            page.update()
        r_rooms.controls=[ui.tf('FLOORS:',0,200,'number'),
                          ui.tf('ROOMS PER FLOOR:',0,200,'number'),
                          ui.tf('PRICE PER ROOM (EDITABLE):',0.0,200,'number'),
                          ui.column([ui.button('SAVE','green',check_set_up),
                                     ui.button('CANCEL','red',refresh)],110,100,'auto')]
        page.update()
    def show_room(room):
        def update(room):
            print(room)
            if c_room.controls[1].value:db.update(room,c_room.controls[1].value,c_room.controls[2].value)
            else:page.show_dialog(ui.alert('PRICE FIELD EMPTY',[]))
            show_room(room)
        def checkin(room):
            refresh(None)
        def checkout(room):
            refresh(None)
        data=db.get_room(room)
        c_room.controls=[ui.text(f'ROOM {data[1]}, {data[2]}',20,'blue'),
                         ui.tf('PRICE PER NIGHT:',data[3],200,'number'),
                         ui.tf('NOTES:',data[4],200,''),
                         ui.button('UPDATE','green',lambda _,r=room:update(r))]
        if data[2]=='OCCUPIED' or data[2]=='RESERVED':
            guest=db.get_guest(room) or ['','','','','','']
            r_check.controls=[ui.button('CHECKOUT','green',lambda _:checkout(room))]
        else:
            guest=['','','','','','']
            r_check.controls=[ui.button('CHECKIN','green',lambda _:checkin(room))]
        c_guest.controls=[ui.tf(labels[n],guest[n],200,'') for n in range(6)]+[r_check]
        page.update()
    def refresh(e):
        if db.check_if_empty()==0:r_rooms.controls=[ui.text('PLEASE SET FLOORS AND ROOMS FOR FIRST TIME: --->',25,'blue'),
                                                    ui.button('SET UP','green',set_up)]
        else:
            r_rooms.controls=[c_rooms]
            for floor in db.get_floors():
                c_rooms.controls.append(ui.row([ui.text(f'FLOOR {floor[0]}',20,'blue')],1200,25,'center'))
                c_rooms.controls.append(ui.row([ui.button(str(room[1]),status[room[2]],lambda _,r=room[1]: show_room(r)) for room in db.get_rooms(floor)],1200,25,'center'))
        page.update()
    r_rooms=ui.row([],1200,300,'center')
    c_rooms=ui.column([],1200,300,'auto')
    c_room=ui.column([],400,275,'auto')
    c_guest=ui.column([],400,275,'auto')
    c_services=ui.column([],400,275,'auto')
    r_check=ui.row([],400,50,'center')
    refresh(None)
    page.add(ui.row([ui.switch(theme),
                     ui.text('daHotel',50,'blue'),
                     ui.iconbutton('EXIT_TO_APP',50,'red',lambda _:page.window.close())],1200,75,'center'),
             ui.divider(),
             r_rooms,
             ui.divider(),
             ui.row([c_room,ui.v_divider(),c_guest,ui.v_divider(),c_services],1200,275,'center'))
flet.run(main)
