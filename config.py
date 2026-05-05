import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()


class Config:
  user = os.environ.get('user')
  password = os.environ.get('password')

  SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-temporary-string'
  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'really-long-and-super-secret-temporary-string'
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)
  
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mariadb+mariadbconnector://{0}:{1}@127.0.0.1:3306/recipeApp'.format(user, password)