import sqlite3
from flet import *
def editor_view(page:Page,theme,alert):
    def add_to_config(e):
        def remove(e):
            e.control.parent.controls.remove(e.control)
            page.update()
        if t_floor.value=='' or t_rooms.value=='' or t_price.value=='':
            alert.title=Text('EMPTY FIELDS')
            page.open(alert)
        else:
            c_config.controls.append(Container(content=Row([Text(str(t_floor.value),width=100),Text(str(t_rooms.value),width=100),Text(str(t_price.value),width=100)],alignment=MainAxisAlignment.CENTER),on_click=remove))
            t_floor.value,t_rooms.value,t_price.value=0,0,0.0
        page.update()
    def save(e):    
        db=sqlite3.connect('db.db')
        for c in c_config.controls:
            print(c)
            for t in c.content.controls:print(t)
            data=[t.value for t in c.content.controls]
            data.insert(2,'green')
            db.execute('insert into ROOMS values(?,?,?,?)',data)
            db.commit()
            alert.title=Text(f'FLOOR {data[0]} SUCCESSFULLY: {data[1]} FREE ROOMS FOR $.{data[2]} PER NIGHT')
        db.close()
        page.open(alert)
        page.update()
    t_floor=TextField(label='FLOOR',keyboard_type=KeyboardType.NUMBER,value=0,width=100)
    t_rooms=TextField(label='ROOMS',keyboard_type=KeyboardType.NUMBER,value=0,width=100)
    t_price=TextField(label='PRICE',keyboard_type=KeyboardType.NUMBER,value=0.0,width=100)
    c_config=Column()
    return Column([Row([Switch(on_change=theme),Text('daHotel',color='orange',size=30),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.go('/HOME'))],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([t_floor,t_rooms,t_price,ElevatedButton('ADD TO CONFIGURATION',on_click=add_to_config)],alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([Text('ROOMS CONFIGURATION',size=20,color='orange')],alignment=MainAxisAlignment.CENTER),
                   Row([Text('FLOOR',width=100),Text('ROOMS',width=100),Text('PRICE',width=100)],alignment=MainAxisAlignment.CENTER),
                   Row([c_config],alignment=MainAxisAlignment.CENTER),
                   Row([ElevatedButton('SAVE',on_click=save)],alignment=MainAxisAlignment.CENTER)])