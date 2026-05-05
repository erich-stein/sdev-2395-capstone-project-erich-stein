from app import app
from flask import jsonify, request
from .models import User, Recipe
from app import db
import sqlalchemy as sa
from datetime import datetime, timezone
from loguru import logger
from flask_jwt_extended import (
  jwt_required, get_jwt_identity,
  create_access_token, get_jwt
)

# for testing, modify or remove later
# just a message the persists throught the app
# also acts as a simple check for the API
@app.route('/api', methods=['GET'])
def hello_world():
  logger.debug('Retrieving data.')
  return jsonify({"message":"Welcome to the Recipe Book!"})

# authenticates credentials and creates JWT token
@app.route('/api/login', methods=['POST'])
def login():
  data = request.get_json()
  logger.debug('Retrieving login data.')

  # backup check for data
  if not data:
    logger.error('No data.')
    return jsonify({'errorMessage': 'No data provided'}), 400

  username = data.get('username')
  password = data.get('password')

  # backup check for username and password
  if not username or not password:
    logger.error('Missing username or password.')
    return jsonify({'errorMessage': 'Username and password required'}), 400
  
  user = db.session.scalar(sa.select(User).where(
    User.username == username
  ))

  if user is None or not user.check_password(password):
    logger.error('Username or password is invalid.')
    return jsonify({'errorMessage': 'Invalid username or password'}), 400

  try:
    access_token = create_access_token(
      identity=str(user.id),
      additional_claims={'username': user.username}
    )
    logger.success('Login successful.')
    return jsonify({
      'token': access_token,
      'user': user.to_json(),
      'message': 'Login successful'}), 200
  except Exception as err:
    print(f"Error creating token: {str(err)}")
    logger.error('Error logging in.')
    return jsonify({'errorMessage': 'Error logging in'})

@app.route('/api/create-account', methods=['POST'])
def createAccount():
  data = request.get_json()
  logger.debug('Retrieving account creation data.')

  # backup check for data
  if not data:
    logger.error('No data.')
    return jsonify({'errorMessage': 'No data provided'}), 400

  newUsername = data.get('username')
  newPassword = data.get('password')

  # backup check for username and password
  if not newUsername or not newPassword:
    logger.error('Missing username or password.')
    return jsonify({'errorMessage': 'Username and password required'}), 400
  
  validateUsername = db.session.scalar(sa.select(User).where(
    User.username == newUsername))
  if validateUsername is not None:
    logger.error('Username already exists.')
    return jsonify({'errorMessage': 'Username already taken'}), 409
  
  try:
    newUser = User(username=newUsername)
    newUser.set_password(newPassword)
    db.session.add(newUser)
    db.session.commit()

    logger.success('Account created.')
    return jsonify({'message': 'Accound created successfully'}), 201

  except Exception as err:
    db.session.rollback()
    print(f"Error creating account: {str(err)}")
    logger.error('Error creating account.')
    return jsonify({'errorMessage': 'Error creating account'})

# simple profile page, mostly just for showing recipes by the user
# maybe make it dynamic or add separate user route
@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
  user = get_jwt()
  user_id = int(get_jwt_identity())
  username = user.get('username')

  try:
    query = sa.select(Recipe).where(
      Recipe.user_id == user_id).order_by(Recipe.timestamp.desc())
    
    recipes = db.session.execute(query).scalars().all()
    recipes_json = [recipe.to_json() for recipe in recipes]

    return jsonify({
    'recipes': recipes_json, 'username': username }), 200
  except Exception as err:
    print(f"Error retrieving recipes: {str(err)}")
    logger.error('Error retrieving recipes.')
    return jsonify({'errorMessage': 'Error retrieving recipes'})

@app.route('/api/create-recipe', methods=['POST'])
@jwt_required()
def createRecipe():
  data = request.get_json()
  logger.debug('Retrieving recipe creation data.')

  # backup check for data
  if not data:
    logger.error('No data.')
    return jsonify({'errorMessage': 'No data provided'}), 400

  # backup check for minimum required data
  title = data.get('title')
  short_desc = data.get('short_desc')
  ingredients = data.get('ingredients', [])
  instructions = data.get('instructions', [])

  if not str(title):
    logger.error('Missing recipe name.')
    return jsonify({'errorMessage': 'Recipe name is required'}), 400
  if not str(short_desc):
    logger.error('Missing recipe short description.')
    return jsonify({'errorMessage': 'Short description is required'}), 400
  if not str(ingredients):
    logger.error('Missing recipe ingredients.')
    return jsonify({'errorMessage': 'Ingredients list is required'}), 400
  if not str(instructions):
    logger.error('Missing recipe instructions.')
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

    logger.success('Recipe created.')
    return jsonify({'message': 'Recipe created successfully'}), 201

  except Exception as err:
    db.session.rollback()
    print(f"Error creating recipe: {str(err)}")
    logger.error('Error creating recipe.')
    return jsonify({'errorMessage': 'Error creating recipe'})

@app.route('/api/recipe/<int:id>', methods=['GET'])
def recipe(id):
  recipe = db.session.scalar(sa.select(Recipe).where(Recipe.id == id))

  if not recipe:
    logger.error('Tried to retrieve non-existing recipe.')
    return jsonify({'errorMessage': 'Recipe not found'}), 404
  logger.success('Recipe retrieved.')
  return jsonify(recipe.to_json()), 200

@app.route('/api/recipe/<int:id>', methods=['PUT'])
@jwt_required()
def update_recipe(id):
  recipe = db.session.scalar(sa.select(Recipe).where(Recipe.id == id))

  if not recipe:
    logger.error('Tried to retrieve non-existing recipe.')
    return jsonify({'errorMessage': 'Recipe not found'}), 404
  
  current_user_id = int(get_jwt_identity())
  if recipe.user_id != current_user_id: 
    logger.error('User tried to edit recipe they do not own.')
    return jsonify({'errorMessage': 'You can only edit your own recipes'}), 401
  
  data = request.get_json()
  logger.debug('Retrieving single recipe data.')

  try:
    # replace only what has been edited
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

    # manually update 'updated' timestamp
    recipe.updated = datetime.now(timezone.utc)

    db.session.commit()
    logger.success('User edited their recipe.')
    return jsonify(recipe.to_json()), 200
  except Exception as err:
    db.session.rollback()
    print(f"Error updating recipe: {str(err)}")
    logger.error('Error trying to edit recipe.')
    return jsonify({'errorMessage': 'Error updating recipe'})
  
@app.route('/api/recipe/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(id):
  recipe = db.session.scalar(sa.select(Recipe).where(Recipe.id == id))

  if not recipe:
    logger.error('Tried to retrieve non-existing recipe.')
    return jsonify({'errorMessage': 'Recipe not found'}), 404
  
  current_user_id = int(get_jwt_identity())
  if recipe.user_id != current_user_id: 
    logger.error('User tried to delete recipe they do not own.')
    return jsonify({'errorMessage': 'You can only delete your own recipes'}), 401
  
  try:
    db.session.delete(recipe)
    db.session.commit()
    logger.success('User deleted a recipe.')
    return jsonify({})
  except Exception as err:
    db.session.rollback()
    print(f"Error deleting recipe: {str(err)}")
    logger.error('Error trying to delete recipe.')
    return jsonify({'errorMessage': 'Error deleting recipe'})
  
# maybe have this be the default page and replace the existing '/' route
# get all recipes for now, add pagination later
@app.route('/api/explore', methods=['GET'])
def explore():
  try:
    query = sa.select(Recipe).order_by(Recipe.timestamp.desc())
    recipes = db.session.execute(query).scalars().all()

    recipes_json = [recipe.to_json() for recipe in recipes]

    logger.success('Successfully retrieved recipes.')
    return jsonify(recipes_json), 200
  except Exception as err:
    print(f"Error retrieving recipes: {str(err)}")
    logger.error('Error trying to retrieve recipes.')
    return jsonify({'errorMessage': 'Error retrieving recipes'})

# get searchTerm, searchType (title or tags for now, can add others),
# and categories from search parameters
# checks separately for categories and search
# frontend uses encodeURIcomponent to sanitize search term
# should probably add sanitization here too, just in case
@app.route('/api/explore/search', methods=['GET', 'POST'])
def search():
  search_term = request.args.get('term', '')
  search_type = request.args.get('type', 'title')
  categories = request.args.getlist('categories')

  query = sa.select(Recipe)

  logger.info('Attempting search or filter.')
  try:
    if categories:
      # converts JSON dict to string for 'contains' operation
      category_list = []
      for category in categories:
        category_list.append(
          sa.cast(Recipe.categories, sa.String).contains(f'"{category}"'))
      
      query = query.where(sa.or_(*category_list))

    if search_type:
      # both use ilike to work with partial matches
      if search_type == 'title':
        # simple case instensitive search
        query = query.where(
          Recipe.title.ilike(f'%{search_term}%'))
      
      elif search_type == 'tags':
        # also converts JSON dict to string
        query = query.where(
          sa.cast(Recipe.tags, sa.String).ilike(f'%{search_term}%'))
      
    else:
      return jsonify({'errorMessage': 'Invalid search type'})
      
    recipes = db.session.execute(
      query.order_by(Recipe.timestamp.desc())).scalars().all()
    recipes_json = [recipe.to_json() for recipe in recipes]

    logger.success('Search or filter succeeded.')
    return jsonify(recipes_json), 200
  except Exception as err:
    print(f"Error retrieving recipes: {str(err)}")
    logger.error('Error attempting search or filter.')
    return jsonify({'errorMessage': 'Error retrieving recipes'})