from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'TestUser'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    age = db.Column(db.Integer)
    sex = db.Column(db.String())
    orientation = db.Column(db.String())
    diet = db.Column(db.String())
    drinks = db.Column(db.String())
    location = db.Column(db.String())
    bio = db.Column(db.String)

    def __init__(self, name, email, password, age, sex, orientation, diet, drinks, location, bio):
        self.name = name
        self.email = email
        self.password = password
        self.age = age
        self.sex = sex
        self.orientation = orientation
        self.diet = diet
        self.drinks = drinks
        self.location = location
        self.bio = bio

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def fetch_users_data():
        return [u.as_dict() for u in UserModel.query.all()]

class SwipeModel(db.Model):
    __tablename__ = 'swipes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('TestUser.id'), nullable=False)
    swiped_user_id = db.Column(db.Integer, db.ForeignKey('TestUser.id'), nullable=False)
    swipe_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, swiped_user_id, swipe_type):
        self.user_id = user_id
        self.swiped_user_id = swiped_user_id
        self.swipe_type = swipe_type

class MatchModel(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('TestUser.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('TestUser.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
