import config
from flask import Flask
from random import randrange
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import request,Response
import json
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECT_URL

db = SQLAlchemy(app)
migrate = Migrate(app, db)



class JsonModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UsersModel(db.Model, JsonModel):
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

    def __init__(self, age, sex, orientation, diet, drinks, education, ethnicity, job, location, pets, religion, sign, speaks, essay0, essay1, essay2, essay3, essay4, essay5, essay6, essay7, essay8, essay9, firstname):
        self.age = age
        self.sex = sex
        self.orientation = orientation
        self.diet = diet
        self.drinks = drinks
        self.education = education
        self.ethnicity = ethnicity
        self.job = job
        self.location = location
        self.pets = pets
        self.religion = religion
        self.sign = sign
        self.speaks = speaks
        self.essay0 = essay0
        self.essay1 = essay1
        self.essay2 = essay2
        self.essay3 = essay3
        self.essay4 = essay4
        self.essay5 = essay5
        self.essay6 = essay6
        self.essay7 = essay7
        self.essay8 = essay8
        self.essay9 = essay9
        self.firstname = firstname

        db.create_all()


def fetch_users_data():
    return json.dumps([u.as_dict() for u in UsersModel.query.all()], default=str)

@app.route('/')
def index_startpage():
    return "Welcome To Our Wingman Backend Flask Application"

@app.route('/usersdata')
def get_users_data():
    response = fetch_users_data()
    return str(response)

if __name__ == "__main__":
    app.run()
