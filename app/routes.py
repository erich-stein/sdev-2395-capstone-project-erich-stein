from app import app
from flask import jsonify, request
from loguru import logger
from flask_jwt_extended import (
  jwt_required, get_jwt_identity,
  create_access_token, get_jwt
)

# mock data
USERS = {
  'admin': {
    'id': 1,
    'username': 'admin',
    'password': 'dev',
  }
}

# for testing, modify or remove later
@app.route('/api', methods=['GET'])
def hello_world():
  logger.debug('Retrieving data.')
  return jsonify({"message":"Hello, World!"})

@app.route('/api/login', methods=['POST'])
def login():
  data = request.get_json()

  if not data:
    return jsonify({'message': 'No data provided'}), 400

  username = data.get('username')
  password = data.get('password')

  if not username or not password:
    return jsonify({'message': 'Username and password required'}), 400
  
  user = USERS.get(username)

  if user and password == user['password']:
    access_token = create_access_token(
      identity=str(user['id']),
      additional_claims={'username': user['username']}
    )
    return jsonify({'token': access_token, 'user': user['username']}), 200
  else:
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/create-account', methods=['POST'])
def createAccount():
  # todo
  return jsonify({})

# needs error handling
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
  current_user_id = get_jwt_identity()
  user = get_jwt()
  username = user.get('username')
  return jsonify({
    'user_id': current_user_id,
    'username': username,
    'message': 'User info here'
  }), 200
