#from unicodedata import temp_water, ph_water, nama_device, water_status, user_id
from app import app, db, response
from app.model.kolam import Kolam
from app.model.user import User
from flask import request, json


def show():
   try:
     kolam = Kolam.query.all()
     data = formatarray(kolam)
     return response.success(data, "success")
   except Exception as e:
      print(e)

   
def formatarray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))
    return array


def singleObject(data):
    data = {
    'id': data.id, 
    'temp_water': data.temp_water,
    'ph_water': data.ph_water,
    'nama_device': data.nama_device,
    'water_status': data.water_status,
    'user_id':data.user_id,
    'Timestamp': data.Timestamp
    }
    
    return data

def detail(id): #function untuk menampilkan data detail 
    try:
        kolam = Kolam.query.filter_by(id=id).first()
        user = User.query.filter((User.user_id == id))

        if not kolam:
            return response.badRequest([], 'Tidak ada data kolam')
    
        datauser = formatUser(user)

        data = singleDetailUser(user, datauser)
    
        return response.success(data, "success")
    
    except Exception as e:
         print(e)



def singleDetailUser(kolam, user):
    data = {
         'id': data.id, 
        'temp_water': data.temp_water,
        'ph_water': data.ph_water,
        'nama_device': data.nama_device,
        'water_status': data.water_status,
        'user_id':data.user_id,
        'Timestamp': data.Timestamp,
        'user': user #bentuknya jadi nested json
    }
    
    return data

def singleUser(user):
    data = {
        'id' : user.id,
        'nim' :user.nim,
        'name' : user.name,
        'email' : user.phone,
        'created_at' : user.create_at,
        'update_at': user.update_at
    }

    return data

def formatUser(data):
    array = [] #ditampung dalam array kosong
    for i in data:
        array.append(singleUser(i)) #single mahasiswa adalah format detailnya

    return array

def save(): #untuk menambahkan data
    try:
        print(request.is_json)
        data = request.get_json()
        temp_water = (data['temp_water']) #ditampung data inputnya
        ph_water = (data['ph_water'])
        nama_device = (data['nama_device'])
        water_status = (data['water_status'])
        user_id = (data['user_id'])
        input = [{
            'temp_water': temp_water,
            'ph_water': ph_water,
            'nama_device': nama_device,
            'water_status':water_status,
        }]
        kolam = Kolam(temp_water=temp_water, ph_water=ph_water, nama_device=nama_device, water_status=water_status, user_id=user_id)
        print(kolam)
        db.session.add(kolam)
        db.session.commit()

    #     return response.success(kolam, 'Sukses Menambahkan Data Kolam')
    # except Exception as e:
    #     return e
        return response.success(input, 'Sukses update data!')
    except Exception as e:
            print(e)

#update data
def ubah(id):
    try:
        temp_water = request.form.get('temp_water') #ditampung data inputnya
        ph_water  = request.form.get('ph_water')
        nama_device = request.form.get('nama_device')
        water_status = request.form.get('water_status')
        user_id = request.form.get('user_id')

        input = [
            {
            'temp_water': 'temp_water',
            'ph_water': 'ph_water',
            'nama_device': 'nama_device',
            'water_status':'water_status',
            }
        ]

        kolam = Kolam.query.filter_by(id=id).first() 
        #data lama diganti dengan data baru
        kolam.temp_water = temp_water
        kolam.ph_water = ph_water
        kolam.nama_device = nama_device
        kolam.water_status = water_status
        kolam.user_id = user_id
        

        db.session.commit()

        return response.success(input, 'Sukses update data!')
    except Exception as e:
        print(e)

#hapus
def hapus(id):
    try:
        kolam = Kolam.query.filter_by(id=id).first()
        if not kolam:
            return response.badRequest([], 'Data Kolam Kosong!')
        db.session.delete(kolam)
        db.session.commit()

        return response.success('', 'Berhasil Menghapus Data!')

    except Exception as e:
        print(e)


def get_paginated_list(clss, url, start, limit):
    # ambil query dari tabel dosen => class yang akan dibuat paginasi
    results = clss.query.all()
    #ubah format agar serialized 
    data = formatarray(results)
    #hitung semua isi value array
    count = len(data)

    obj = {}

    if (count < start):
        obj['success'] = False
        obj['message'] = "error"
        return obj
    else:
        # make response
        obj['success'] = True
        obj['start_page'] = start
        obj['per_page'] = limit
        obj['total_data'] = count
        #ceil agar bilangan menjadi bulat ke atas
        obj['total_page'] = math.ceil(count / limit)
        # make URLs
        # make previous url
        if start == 1:
            obj['previous'] = ''
        else:
            
            start_copy = max(1, start - limit)
            limit_copy = start - 1
            obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
        if start + limit > count:
            obj['next'] = ''
        else:
            start_copy = start + limit
            obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
        obj['results'] = data[(start - 1):(start - 1 + limit)]
        return obj

#buat fungsi paginate
def paginate():
   
    start = request.args.get('start')
    limit = request.args.get('limit')

    try:
        #default display first page
        if start == None or limit == None:
            return jsonify(get_paginated_list(
            Dosen, 
            'http://127.0.0.1:5000/kolam', 
            start=request.args.get('start',1), 
            limit=request.args.get('limit',5)
            ))
            #custom parameters
        else:
            return jsonify(get_paginated_list(
            Dosen, 
            'http://127.0.0.1:5000/kolam', 
            start=int(start), 
            limit=int(limit)
            ))

    except Exception as e:
        print(e)

 