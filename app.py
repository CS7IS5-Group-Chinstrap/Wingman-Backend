import config
from flask import Flask
from flask_migrate import Migrate
from models import db
import pandas as pd
import KMeans
import text_features
import json
from flask import request, Response, jsonify
from datetime import datetime
from models import UserModel, SwipeModel, MatchModel, db
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

@app.route('/')
def index_startpage():
    return "Welcome To Our Wingman Backend Flask Application"

# Gets all the users 
@app.route('/all-users')
def get_users_data():
    return str(UserModel.fetch_users_data())

# Gets all the users similar to a given user (using userID as a api query parameter) using K-means clustering
@app.route('/get-similar-users')
def get_similar_users():
    id = request.args.get('userID')
    if not id:
        response = {'message': 'Please provide a user id at the end of URL (E.g ?userID=1)'}, 400
    else:
         data = UserModel.fetch_users_data_as_list()
         df = pd.DataFrame(data)
         try:
            response = KMeans.getSimilarUsers(df,id).to_json(orient = "records")
         except:
            response = {'message': 'No Users to show at the moment'}, 404
    
    return response

@app.route('/get-ice-breakers')
def get_ice_breakers_for_user():
    id = request.args.get('userID')
    if not id:
        response = {'message': 'Please provide a user id at the end of URL (E.g ?userID=1)'}, 400
    else:
        user = UserModel.fetch_user_data_by_id(user_id=id)
        if user is not None:
            # TODO : Pass the topics to the GPT model for sentences
            response = text_features.extract_topics_per_user(user.as_dict())
        else:
            response = {'message': 'User not found.'}, 404
    return response

@app.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = UserModel.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    age = request.json.get('age')
    sex = request.json.get('sex')
    orientation = request.json.get('orientation')
    diet = request.json.get('diet')
    drinks = request.json.get('drinks')
    location = request.json.get('location')
    bio = request.json.get('bio')

    if name:
        user.name = name
    if email:
        user.email = email
    if password:
        user.password = password
    if age:
        user.age = age
    if sex:
        user.sex = sex
    if orientation:
        user.orientation = orientation
    if diet:
        user.diet = diet
    if drinks:
        user.drinks = drinks
    if location:
        user.location = location
    if bio:
        user.essay0 = bio

    db.session.commit()

    return jsonify({'message': 'User updated successfully'})

@app.route('/add-swipe', methods=['POST'])
def add_swipe():
    user_id = request.json.get('user_id')
    swiped_user_id = request.json.get('swiped_user_id')
    swipe_type = request.json.get('swipe_type')

    new_swipe = SwipeModel(user_id=user_id, swiped_user_id=swiped_user_id, swipe_type=swipe_type)
    db.session.add(new_swipe)
    db.session.commit()

    # Check for matches
    match = SwipeModel.query.filter_by(user_id=swiped_user_id, swiped_user_id=user_id, swipe_type='right').first()
    if match:
        # Create a new match object
        new_match = MatchModel(user1_id=user_id, user2_id=swiped_user_id)
        db.session.add(new_match)
        db.session.commit()

        # Notify both users of the match
        user1 = UserModel.query.get(user_id)
        user2 = UserModel.query.get(swiped_user_id)

        # Send a message or notification to both users
        send_notification(user1, user2)

    return jsonify({'message': 'Swipe submitted successfully', "match": new_match })

@app.route('/matches/<int:user_id>', methods=['GET'])
def get_matches(user_id):
    matches = MatchModel.query.filter((MatchModel.user1_id == user_id) | (MatchModel.user2_id == user_id)).all()

    matched_users = []
    for match in matches:
        if match.user1_id == user_id:
            matched_users.append(UserModel.query.get(match.user2_id))
        else:
            matched_users.append(UserModel.query.get(match.user1_id))

    return jsonify([u.as_dict() for u in matched_users])


from flask_mail import Mail, Message

mail = Mail()

def send_notification(user1, user2):
    # Get the email addresses of both users
    user1_email = user1.email
    user2_email = user2.email

    # Create the email message
    msg = Message('New Match!', recipients=[user1_email, user2_email])
    msg.body = f'Congratulations, {user1.name} and {user2.name}! You have a new match on our dating app.'

    # Send the email
    mail.send(msg)


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    app.run()
