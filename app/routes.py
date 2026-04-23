from app import app
from flask import jsonify, request
from .models import User, Recipe
from app import db
import sqlalchemy as sa
from loguru import logger
from flask_jwt_extended import (
  jwt_required, get_jwt_identity,
  create_access_token, get_jwt
)

# for testing, modify or remove later
@app.route('/api', methods=['GET'])
def hello_world():
  logger.debug('Retrieving data.')
  return jsonify({"message":"Hello, World!"})

@app.route('/api/login', methods=['GET', 'POST'])
def login():
  data = request.get_json()

  # backup check
  if not data:
    return jsonify({'errorMessage': 'No data provided'}), 400

  username = data.get('username')
  password = data.get('password')

  # backup check
  if not username or not password:
    return jsonify({'errorMessage': 'Username and password required'}), 400
  
  user = db.session.scalar(sa.select(User).where(
    User.username == username
  ))

  if user is None or not user.check_password(password):
    return jsonify({'errorMessage': 'Invalid username or password'}), 400

  try:
    access_token = create_access_token(
      identity=str(user.id),
      additional_claims={'username': user.username}
    )
    return jsonify({
      'token': access_token,
      'user': user.username,
      'message': 'Login successfull'}), 200
  except Exception as err:
    print(f"Error creating token: {str(err)}")
    return jsonify({'errorMessage': 'Error logging in'})

@app.route('/api/create-account', methods=['POST'])
def createAccount():
  data = request.get_json()

  # backup check
  if not data:
    return jsonify({'errorMessage': 'No data provided'}), 400

  newUsername = data.get('username')
  newPassword = data.get('password')

  # backup check
  if not newUsername or not newPassword:
    return jsonify({'errorMessage': 'Username and password required'}), 400
  
  validateUsername = db.session.scalar(sa.select(User).where(
    User.username == newUsername))
  if validateUsername is not None:
    return jsonify({'errorMessage': 'Username already taken'}), 409
  
  try:
    newUser = User(username=newUsername)
    newUser.set_password(newPassword)
    db.session.add(newUser)
    db.session.commit()

    return jsonify({'message': 'Accound created successfully'}), 201

  except Exception as err:
    db.session.rollback()
    print(f"Error creating account: {str(err)}")
    return jsonify({'errorMessage': 'Error creating account'})

# needs error handling here and in view
# simple profile page, mostly just for showing recipes by the user
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
  current_user_id = get_jwt_identity()
  user = get_jwt()
  username = user.get('username')
  return jsonify({
    'user_id': current_user_id,
    'username': username,
    'message': 'User recipes here'
  }), 200
