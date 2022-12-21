from app import app #response
from app.controller import KolamController
from app.controller import UserController
from flask import request
from flask import jsonify



@app.route("/")
def index():
  return 'word'


@app.route('/kolam', methods=['GET', 'POST'])
def kolam():
     if request.method == 'GET':
         return KolamController.show()
     else:
         return KolamController.save()



@app.route('/kolam/<id>', methods=['PUT', 'DELETE'])
def KolamDetail(id):
    if request.method == 'PUT':
        return KolamController.ubah(id)
    else:
        return KolamController.hapus(id)


@app.route('/admin', methods=['POST'])
def admins():
 return UserController.admin()

@app.route('/login', methods = ['POST'])
def logins():
    return UserController.login()