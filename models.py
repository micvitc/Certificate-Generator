from . import db
from flask_login import UserMixin



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True,nullable=False)
    register_number = db.Column(db.String(100))
    password = db.Column(db.String(100), nullable=False)

#Define your Event Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    event_name = db.Column(db.String(50))
    brandings = db.Column(db.String(50))
    participants = db.Column(db.String(200))
    winners = db.Column(db.String(200))