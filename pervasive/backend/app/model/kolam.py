from sqlite3 import Timestamp
from app import db
from datetime import datetime
from app.model.user import User
import json


class Kolam(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    temp_water = db.Column(db.Float(30), nullable=False)
    ph_water = db.Column(db.Float(50), nullable=False)
    nama_device = db.Column(db.String(13), nullable=False)
    water_status = db.Column(db.String(100),nullable=False)
    Timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.id, ondelete='CASCADE'))
    

    # def __repr__(self):
    #     return '<Kolam {}>'.format(self.name)

    