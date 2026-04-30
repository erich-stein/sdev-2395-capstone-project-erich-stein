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
      'user': user.to_json(),
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
# maybe make it dynamic or add separate user route
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

@app.route('/api/create-recipe', methods=['POST'])
@jwt_required()
def createRecipe():
  data = request.get_json()

  # backup check for data
  if not data:
    return jsonify({'errorMessage': 'No data provided'}), 400

  # backup check for minimum required data
  title = data.get('title')
  short_desc = data.get('short_desc')
  ingredients = data.get('ingredients', [])
  instructions = data.get('instructions', [])

  if not title:
    return jsonify({'errorMessage': 'Recipe name is required'}), 400
  if not short_desc:
    return jsonify({'errorMessage': 'Short description is required'}), 400
  if not ingredients:
    return jsonify({'errorMessage': 'Ingredients list is required'}), 400
  if not instructions:
    return jsonify({'errorMessage': 'Instructions list is required'}), 400

  try:
    recipe = Recipe(
      title=title,
      long_desc=data.get('long_desc'),
      short_desc=short_desc,
      categories=data.get('categories', []),
      tags=data.get('tags', []),
      ingredients=ingredients,
      instructions=instructions,
      user_id=get_jwt_identity()
    )

    db.session.add(recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe created successfully'}), 201

  except Exception as err:
    db.session.rollback()
    print(f"Error creating recipe: {str(err)}")
    return jsonify({'errorMessage': 'Error creating recipe'})

@app.route('/api/recipe/<int:id>', methods=['GET'])
def recipe(id):
  recipe = db.session.scalar(sa.select(Recipe).where(Recipe.id == id))

  if not recipe:
    return jsonify({'errorMessage': 'Recipe not found'}), 404
  return jsonify(recipe.to_json()), 200

@app.route('/api/recipe/<int:id>', methods=['PUT'])
@jwt_required()
def update_recipe(id):
  recipe = db.session.scalar(sa.select(Recipe).where(Recipe.id == id))

  if not recipe:
    return jsonify({'errorMessage': 'Recipe not found'}), 404
  
  current_user_id = int(get_jwt_identity())
  if recipe.user_id != current_user_id: 
    return jsonify({'errorMessage': 'You can only edit your own recipes'}), 401
  
  data = request.get_json()

  try:
    if 'title' in data:
      recipe.title = data.get('title')
    if 'long_desc' in data:
      recipe.long_desc = data.get('long_desc')
    if 'short_desc' in data:
      recipe.short_desc = data.get('short_desc')
    if 'categories' in data:
      recipe.categories = data.get('categories')
    if 'tags' in data:
      recipe.tags = data.get('tags')
    if 'ingredients' in data:
      recipe.ingredients = data.get('ingredients')
    if 'instructions' in data:
      recipe.instructions = data.get('instructions')

    db.session.commit()
    return jsonify(recipe.to_json()), 200
  except Exception as err:
    db.session.rollback()
    print(f"Error updating recipe: {str(err)}")
    return jsonify({'errorMessage': 'Error updating recipe'})
  
@app.route('/api/recipe/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(id):
  recipe = db.session.scalar(sa.select(Recipe).where(Recipe.id == id))

  if not recipe:
    return jsonify({'errorMessage': 'Recipe not found'}), 404
  
  current_user_id = int(get_jwt_identity())
  if recipe.user_id != current_user_id: 
    return jsonify({'errorMessage': 'You can only delete your own recipes'}), 401
  
  try:
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({})
  except Exception as err:
    db.session.rollback()
    print(f"Error deleting recipe: {str(err)}")
    return jsonify({'errorMessage': 'Error deleting recipe'})