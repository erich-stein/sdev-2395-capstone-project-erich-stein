import os

user = 'root'
password = 'dev'

class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mariadb+mariadbconnector://{0}:{1}@127.0.0.1:3306/recipeApp'.format(user, password)