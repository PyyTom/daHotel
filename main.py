import flet as fl,sqlite3,datetime,os
from datetime import date
db=sqlite3.connect('db.db')
db.execute('create table if not exists ROOMS(ROOM integer,STATUS)')
db.execute('create table if not exists SERVICES(ROOM integer,DATE,SERVICE,COST float)')
if db.execute('select COUNT(*) from ROOMS').fetchone()[0]==0:
    for n in range(1,16):
        db.execute('insert into ROOMS(ROOM,STATUS) values(?,?)',(n,'FREE'))
        db.commit()
db.close()
services={'CLEANING':0.00,'ROOM SERVICE':30.00,'LAUNDRY':10.00,'PPV':10.00,'CHECK-OUT':0.00}
def main(page:fl.Page):
    page.window_full_screen=True
    d=fl.AlertDialog(title=fl.Text('PRINT BILL?'),modal=True)
    def xit(e):
        page.window_destroy()
    def refresh():
        def edit(e):
            room.value=e.control.text
            room.update()
            db=sqlite3.connect('db.db')
            historial=db.execute('select * from SERVICES where ROOM=?',(e.control.text,)).fetchall()
            if historial!=[]:
                for h in historial:c_historial.controls.append(fl.Text('ROOM '+str(h[0])+', '+h[1]+': '+h[2]+' $.'+str(h[3])))
            c_historial.update()
            if db.execute('select * from SERVICES where ROOM=?',(room.value,)).fetchall()==[]:service.options=[fl.dropdown.Option('CHECK-IN')]
            else:service.options=[fl.dropdown.Option(s) for s in services]
            service.update()
            db.close()
            b_save.disabled=False
        room.value=''
        room.update()
        c_historial.controls.clear()
        c_historial.update()
        b_save.disabled=True
        r_floor1.controls.clear()
        r_floor2.controls.clear()
        r_floor3.controls.clear()
        for n in range(1,16):
            color=''
            db = sqlite3.connect('db.db')
            stat = db.execute('select STATUS from ROOMS where ROOM=?', (n,)).fetchone()
            db.close()
            if stat[0]=='FREE':color='green'
            elif stat[0] == 'BUSY':color = 'red'
            elif stat[0] == 'WORKING': color= 'yellow'
            elif stat[0] == 'CLEANING':color= 'blue'
            if n<=5:r_floor1.controls.append(fl.ElevatedButton(str(n),color=color,on_click=edit,width=250,height=150))
            elif n>5 and n<11:r_floor2.controls.append(fl.ElevatedButton(str(n),color=color,on_click=edit,width=250,height=150))
            elif n > 10:r_floor3.controls.append(fl.ElevatedButton(str(n),color=color,on_click=edit, width=250, height=150))
        r_floor1.update()
        r_floor2.update()
        r_floor3.update()
    def dismiss(e):
        d.open=False
        page.update()
    def print_bill(e):
        db=sqlite3.connect('db.db')
        bill=open(str(room.value)+'.txt','w')
        bill.write('ROOM n.'+str(room.value)+'\n\n')#ROOM,DATE,SERVICE,COST
        for s in db.execute('select * from SERVICES where ROOM=?',(room.value,)).fetchall():
            bill.write('      $.'+str(s[3])+', '+s[2]+' IN DATE '+s[1]+'\n')
        total=db.execute('select sum(COST) from SERVICES where ROOM=?',(room.value,)).fetchone()[0]
        bill.write('\n\nTOTAL $.'+str(total))
        os.startfile(str(room.value)+'.txt','print')
        bill.close()
        db.execute('delete from SERVICES where ROOM=?',(room.value,))
        db.commit()
        db.close()
        d.open=False
        page.update()
        refresh()
    def save(e):
        db=sqlite3.connect('db.db')
        if service.value=='CHECK-OUT':
            status='FREE'
            checkin=db.execute('select DATE from SERVICES where ROOM=? and SERVICE=?',(room.value,'CHECK-IN',)).fetchone()[0]
            checkout=datetime.datetime.today().strftime('%Y-%m-%d')
            delta1=date(int(checkin.split('-')[0]),int(checkin.split('-')[1]),int(checkin.split('-')[2]))
            delta2 = date(int(checkout.split('-')[0]), int(checkout.split('-')[1]), int(checkout.split('-')[2]))
            days=delta2-delta1
            if int(room.value)<=5:cost=40
            elif int(room.value)>=11:cost=60
            else:cost=50
            price=days.days*cost
        else:
            status='BUSY'
            if service.value=='CHECK-IN':price=0.00
            else:price=services[service.value]
        db.execute('update ROOMS set STATUS=? where ROOM=?',(status,room.value,))
        db.commit()
        db.execute('insert into SERVICES values(?,?,?,?)',(room.value,datetime.datetime.today().strftime('%Y-%m-%d'),service.value,price))
        db.commit()
        db.close()
        if service.value=='CHECK-OUT':
            page.dialog=d
            d.actions=[fl.TextButton('YES',on_click=print_bill),fl.TextButton('NO',on_click=dismiss)]
            d.open=True
            page.update()
        else:refresh()
    r_floor1=fl.Row(alignment=fl.MainAxisAlignment.CENTER)
    r_floor2=fl.Row(alignment=fl.MainAxisAlignment.CENTER)
    r_floor3=fl.Row(alignment=fl.MainAxisAlignment.CENTER)
    room=fl.TextField(label='ROOM')
    service=fl.Dropdown(label='SERVICE')
    c_historial=fl.Column(scroll=fl.ScrollMode.ALWAYS,height=100)
    b_save=fl.ElevatedButton('SAVE',on_click=save)
    r_edit=fl.Row(controls=[room,service,b_save,c_historial])
    page.add(fl.Row(controls=[fl.Text('DAHOTEL',size=30)],alignment=fl.MainAxisAlignment.CENTER),
             fl.Text('3st FLOOR',size=20),r_floor3,fl.Text('2nd FLOOR',size=20),r_floor2,fl.Text('1rd FLOOR',size=20),r_floor1,
             fl.Divider(height=9, thickness=3),
             fl.Row(controls=[fl.Text(width=450),fl.Text('ROOM',size=20),fl.Text(width=550),fl.Text('HISTORIAL',size=20)]),r_edit,
             fl.Row(controls=[fl.IconButton(icon=fl.icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=xit)],alignment=fl.MainAxisAlignment.CENTER))
    refresh()
fl.app(target=main)