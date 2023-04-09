from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import config
import json

db = SQLAlchemy()

class BaseModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserModel(db.Model, BaseModel):
    __tablename__ = config.USERS_TABLE

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String())
    orientation = db.Column(db.String())
    diet = db.Column(db.String())
    drinks = db.Column(db.String())
    education = db.Column(db.String())
    ethnicity = db.Column(db.String())
    job = db.Column(db.String())
    location = db.Column(db.String())
    pets = db.Column(db.String())
    religion = db.Column(db.String())
    sign = db.Column(db.String())
    speaks = db.Column(db.String())
    essay0 = db.Column(db.String())
    essay1 = db.Column(db.String())
    essay2 = db.Column(db.String())
    essay3 = db.Column(db.String())
    essay4 = db.Column(db.String())
    essay5 = db.Column(db.String())
    essay6 = db.Column(db.String())
    essay7 = db.Column(db.String())
    essay8 = db.Column(db.String())
    essay9 = db.Column(db.String())
    firstname = db.Column(db.String())
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, password, name):
        self.email = email
        self.firstname = name
        self.password = password

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def __init__(self, age, sex, orientation, diet, drinks, education, ethnicity, job, location, pets, religion, sign, speaks, essay0, essay1, essay2, essay3, essay4, essay5, essay6, essay7, essay8, essay9, name, email, password):
    #     self.age = age
    #     self.sex = sex
    #     self.orientation = orientation
    #     self.diet = diet
    #     self.drinks = drinks
    #     self.education = education
    #     self.ethnicity = ethnicity
    #     self.job = job
    #     self.location = location
    #     self.pets = pets
    #     self.religion = religion
    #     self.sign = sign
    #     self.speaks = speaks
    #     self.essay0 = essay0
    #     self.essay1 = essay1
    #     self.essay2 = essay2
    #     self.essay3 = essay3
    #     self.essay4 = essay4
    #     self.essay5 = essay5
    #     self.essay6 = essay6
    #     self.essay7 = essay7
    #     self.essay8 = essay8
    #     self.essay9 = essay9
    #     self.name = name
    #     self.email = email
    #     self.password = password
    #     self.

    def fetch_users_data():
        return json.dumps([u.as_dict() for u in UserModel.query.all()], default=str)

    def fetch_users_data_as_list():
        return [u.as_dict() for u in UserModel.query.all()]

    def fetch_user_data_by_id(user_id):
        return UserModel.query.get(user_id)

class SwipeModel(db.Model):
    __tablename__ = 'swipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    swiped_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    swipe_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, swiped_user_id, swipe_type):
        self.user_id = user_id
        self.swiped_user_id = swiped_user_id
        self.swipe_type = swipe_type

class MatchModel(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user1_id': self.user1_id,
            'user2_id': self.user2_id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
