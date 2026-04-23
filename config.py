import os
from datetime import timedelta

user = 'root'
password = 'dev'

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-temporary-string'
  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'really-long-and-super-secret-temporary-string'
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
  
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mariadb+mariadbconnector://{0}:{1}@127.0.0.1:3306/recipeApp'.format(user, password)