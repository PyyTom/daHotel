import flet
from db import DB
db=DB()
from ui import UI
status={'FREE':'green','OCCUPIED':'red','RESERVED':'blue','MAINTENAINCE':'orange'}
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
                refresh(None)
            try:page.show_dialog(ui.alert(f'SETTING UP {r_rooms.controls[0].value} FLOORS, {r_rooms.controls[1].value} ROOMS PER FLOOR, WITH STARTING PRICE $. {r_rooms.controls[2].value}. CONFIRM?',
                                [ui.button('YES','green',save_set_up),ui.button('NO','red',page.pop_dialog())]))
            except:page.show_dialog(ui.alert('EMPTY FIELDS. CANNOT SET UP',[]))
            page.update()
        r_rooms.controls=[ui.tf('FLOORS:',0,200,'number'),
                          ui.tf('ROOMS PER FLOOR:',0,200,'number'),
                          ui.tf('PRICE PER ROOM (EDITABLE):',0.0,200,'number'),
                          ui.column([ui.button('SAVE','green',check_set_up),
                                     ui.button('CANCEL','red',refresh)],100,100,'auto')]
        page.update()
    def refresh(e):
        if db.check_if_empty()==0:r_rooms.controls=[ui.text('PLEASE SET FLOORS AND ROOMS FOR FIRST TIME: --->',25,'blue'),
                                                    ui.button('SET UP','green',set_up)]
        else:r_rooms.controls=[ui.text(room,10,'grey') for room in db.get_set_up()]
        page.update()
    r_rooms=ui.row([],1200,300,'center')
    refresh(None)
    page.add(ui.row([ui.switch(theme),
                     ui.text('daHotel',50,'blue'),
                     ui.iconbutton('EXIT_TO_APP',50,'red',lambda _:page.window.close())],1200,75,'center'),
             ui.divider(),
             r_rooms,
             ui.divider())
flet.run(main)
