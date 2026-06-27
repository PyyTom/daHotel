import flet,datetime
date=datetime.datetime.today().strftime('%Y-%m-%d')
from db import DB
db=DB()
from ui import UI
status={'FREE':'green','OCCUPIED':'red','RESERVED':'blue','MAINTENAINCE':'orange'}
labels=['NAME','ID','NIGHTS','ADDRESS','PHONE','MAIL','NOTES']
widths=[200,150,100,200,150,200,175]
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
            if r_room.controls[2].value:
                try:value=r_room.controls[1]._value
                except:value=r_room.controls[1].text
                db.update(room,value,r_room.controls[2].value,r_room.controls[3].value)
                page.show_dialog(ui.alert('ROOM CORRECTLY UPDATED',[]))
            else:page.show_dialog(ui.alert('PRICE FIELD EMPTY',[]))
            refresh(None)
        def checkin(room):
            name,guest_id,nights,address,phone,mail,notes=[i.value for i in r_guest.controls[:7]]
            if all([name,guest_id,nights,address,phone,mail,notes]):
                bill=float(nights)*db.get_room(room)[3]
                db.checkin(room,name,guest_id,date,nights,bill,address,phone,mail,notes)
                page.show_dialog(ui.alert('CHECKIN CORRECTLY SAVED',[]))
            else:page.show_dialog(ui.alert('EMPTY FIELDS',[]))
            show_room(room)
        def checkout(room):
            db.checkout(room)
            page.show_dialog(ui.alert('CHECKOUT CORRECTLY SAVED',[]))
            refresh(None)
        def add_service(e):
            service,price,notes=[i.value for i in r_service.controls[:3]]
            if all([service,price,notes]):
                db.add_service(date,room,service,price,notes)
                page.show_dialog(ui.alert('SERVICE CORRECTLY SAVED',[]))
            else:page.show_dialog(ui.alert('EMPTY FIELDS',[]))
            show_room(room)
        data=db.get_room(room)
        if data[2]=='FREE':x_widget=ui.dd('STATUS',data[2],['MAINTENAINCE'],'orange')
        elif data[2]=='MAINTENAINCE':x_widget=ui.dd('STATUS',data[2],['FREE'],'green')
        else:x_widget=ui.text(data[2],20,status[data[2]])
        r_room.controls=[ui.text(f'ROOM {data[1]}, ',20,'blue'),
                         x_widget,
                         ui.tf('PRICE PER NIGHT $.:',data[3],200,'number'),
                         ui.tf('NOTES:',data[4],200,''),
                         ui.button('UPDATE','green',lambda _,r=room:update(r))]
        if data[2]=='OCCUPIED' or data[2]=='RESERVED':
            guest=db.get_booking(room)
            r_check.controls=[ui.button('CHECKOUT','green',lambda _:checkout(room)),ui.text(f'BILL $. {db.get_bill(room)}',15,'green')]
            r_service.controls=[ui.tf('SERVICE:','',200,''),
                                ui.tf('PRICE $.:',0.0,100,''),
                                ui.tf('NOTES:','',200,''),
                                ui.iconbutton('ADD',25,'green',add_service)]
            c_services.controls=[ui.row([ui.text(service[2:],15,'blue')],1200,30,'center','auto') for service in db.get_services(room)] or []
        else:
            guest=['','','','','','','']
            r_check.controls=[ui.button('CHECKIN','green',lambda _:checkin(room))]
            r_service.controls.clear()
            c_services.controls.clear()
        r_guest.controls=[ui.tf(labels[n],guest[n],widths[n],'') for n in range(7)]+[r_check]
        page.update()
    def refresh(e):
        r_room.controls.clear()
        r_guest.controls.clear()
        r_service.controls.clear()
        c_services.controls.clear()
        if db.check_if_empty()==0:r_rooms.controls=[ui.text('PLEASE SET FLOORS AND ROOMS FOR FIRST TIME: --->',25,'blue'),
                                                    ui.button('SET UP','green',set_up)]
        else:
            c_rooms.controls.clear()
            r_rooms.controls=[c_rooms]
            for floor in db.get_floors():
                c_rooms.controls.append(ui.row([ui.text(f'FLOOR {floor[0]}',20,'blue')],1200,25,'center','auto'))
                c_rooms.controls.append(ui.row([ui.button(str(room[1]),status[room[2]],lambda _,r=room[1]: show_room(r)) for room in db.get_rooms(floor)],1200,25,'center','auto'))
        page.update()
    r_rooms=ui.row([],1200,250,'center','auto')
    c_rooms=ui.column([],1200,250,'auto')
    r_room=ui.row([],1200,60,'center','auto')
    r_guest=ui.row([],1200,80,'center','auto')
    r_check=ui.row([],250,50,'center','auto')
    r_service=ui.row([],1200,60,'center','auto')
    c_services=ui.column([],1200,100,'auto')
    refresh(None)
    page.add(ui.row([ui.switch(theme),
                     ui.text('daHotel',50,'blue'),
                     ui.iconbutton('EXIT_TO_APP',50,'red',lambda _:page.window.close())],1200,75,'center','auto'),
             ui.divider(),
             r_rooms,
             ui.divider(),
             r_room,
             r_guest,
             r_service,
             c_services)
flet.run(main)
