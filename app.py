import config
from flask import Flask
from flask_migrate import Migrate
from models import db
import pandas as pd
import KMeans
import text_features
import json
from flask import request, Response
from auth import (
    register,
    login,
    logout
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECT_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = config.SECRET_KEY

db.init_app(app)
migrate = Migrate(app, db)

# add the routes for the new endpoints
app.route('/register', methods=['POST'])(register)
app.route('/login', methods=['POST'])(login)
app.route('/logout', methods=['POST'])(logout)

class BaseModel(object):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UsersModel(db.Model, BaseModel):
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

def fetch_users_data():
    return json.dumps([u.as_dict() for u in UsersModel.query.all()], default=str)

def fetch_users_data_as_list():
    return [u.as_dict() for u in UsersModel.query.all()]

def fetch_user_data_by_id(user_id):
    return UsersModel.query.get(user_id)

@app.route('/')
def index_startpage():
    return "Welcome To Our Wingman Backend Flask Application"

# Gets all the users 
@app.route('/usersdata')
def get_users_data():
    return str(fetch_users_data())

# Gets all the users similar to a given user (using userID as a api query parameter) using K-means clustering
@app.route('/getSimilarUsers')
def get_similar_users():
    id = request.args.get('userID')
    if not id:
        response = {'message': 'Please provide a user id at the end of URL (E.g ?userID=1)'}, 400
    else:
         data = fetch_users_data_as_list()
         df = pd.DataFrame(data)
         try:
            response = KMeans.getSimilarUsers(df,id).to_json(orient = "records")
         except:
            response = {'message': 'No Users to show at the moment'}, 404
    
    return response

@app.route('/getIceBreakers')
def get_ice_breakers_for_user():
    id = request.args.get('userID')
    if not id:
        response = {'message': 'Please provide a user id at the end of URL (E.g ?userID=1)'}, 400
    else:
        user = fetch_user_data_by_id(user_id=id)
        if user is not None:
            # TODO : Pass the topics to the GPT model for sentences
            response = text_features.extract_topics_per_user(user.as_dict())
        else:
            response = {'message': 'User not found.'}, 404
    return response

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    app.run()
