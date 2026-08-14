from flask import Flask,render_template,request,redirect
app=Flask(__name__)
from db import DB
db=DB()
import datetime
today=datetime.datetime.today().strftime('%Y-%m-%d')
last=(datetime.datetime.today()+datetime.timedelta(days=30)).strftime('%Y-%m-%d')
@app.route('/',methods=['GET'])
def main():
    return render_template('index.html',today=today,last=last,step=1)
@app.route('/search',methods=['POST'])
def search_rooms():
    checkin=request.form.get('checkin')
    nights=request.form.get('nights')
    free_rooms=db.get_free_rooms()
    return render_template('index.html',
                            today=today,
                            last=last,
                            free_rooms=free_rooms,
                            step=2,
                            data={'checkin':checkin,'nights':nights})
@app.route('/select_room',methods=['POST'])
def select_room():
    checkin=request.form.get('checkin')
    nights=request.form.get('nights')
    room=request.form.get('room')
    price=request.form.get('price')
    return render_template('index.html',
                           today=today,
                           last=last,
                           step=3,
                           selected_room=room,
                           price=price,
                           data={'checkin':checkin,'nights':nights})
@app.route('/CONFIRM',methods=['POST'])
def confirm():
    room=int(request.form.get('room'))
    price=float(request.form.get('price'))
    nights=int(request.form.get('nights'))
    name=request.form.get('name')
    guest_id=request.form.get('doc')
    date=request.form.get('checkin')
    address=request.form.get('address')
    phone=request.form.get('phone')
    mail=request.form.get('mail')
    notes=''
    bill=float(nights)*price
    db.checkin(room,name.upper(),guest_id.upper(),date,nights,bill,address.upper(),phone,mail.upper(),notes.upper(),'booking')
    return f'<h1>CONFIRMED ROOM {room}, Total $.{bill}</h1><a href="/">BACK</a>'
app.run(debug=True)
