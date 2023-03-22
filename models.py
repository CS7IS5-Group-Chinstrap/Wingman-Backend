from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'TestUser'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def fetch_users_data():
    return [u.as_dict() for u in UserModel.query.all()]