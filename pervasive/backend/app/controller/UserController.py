from os import access
from app import app, db, response
# from app.controller.DosenController import singleObject
from app.model.user import User
from app import response, app, db
from flask import request
from flask_jwt_extended import *
import datetime


def admin():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        level = 1

        users = User(name=name, email=email, level=level)
        users.setPassword(password)
        print(users)
        db.session.add(users)
        db.session.commit()
        
        return response.success('', "Sukses Menambahkan User!")
    except Exception as e:
        print(e)
        return response.success('', e)


#fungsi untuk menampilkan data user yg login
def singleObject(data):
    data = {
        'id': data.id,
        'name': data.name,
        'email': data.email
        
    }

    return data

def login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.queryfilter_by(email=email).first()

        if not user:
            return response.badRequest([], 'Email tidak terdaftar')
        
        if not user.checkPassword(password):
            return response.badRequest([], 'Password salah')
        
        data = singleObject(user)

        expires = datetime.timedelta(days=7) #token setlah login brp lama 
        expires_refresh = datetime.timedelta(days=7) #refresh token

        #untuk akses token dri lib flask jwt
        access_token = create_access_token(data, fresh=True, expires_delta=expires)#parameter def dri flask jwt
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)

        return response.success({
            "data": data,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, "Sukses Login")
    except Exception as e:
        print(e)
    
   

