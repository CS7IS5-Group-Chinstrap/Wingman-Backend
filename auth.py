import jwt
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models import UserModel, db
import datetime
from sqlalchemy.exc import IntegrityError

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = UserModel.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def register():
    data = request.get_json()

    user = UserModel.query.filter_by(email=data['email']).first()

    if user:
        return jsonify({'message': 'Email already exists'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = UserModel(
        email=data['email'],
        name=data['name'],
        age = 0,
        sex = 'f',
        orientation = 'straight',
        diet  = 'anything',
        drinks = 'socially',
        
        password=hashed_password
    )

    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'New user created!', 'user_id':new_user.id})
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create new user'}), 500

def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Could not verify 1', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = UserModel.query.filter_by(email=auth.username).first()

    if not user:
        return jsonify({'message': 'User not found', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'message': 'Successfully Logged In', 'token': token, 'user_id':user.id}), 200
    else:
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401 


@token_required
def logout(current_user):
    
    return jsonify({'message': f'Logged out user {current_user.email}'}), 200
