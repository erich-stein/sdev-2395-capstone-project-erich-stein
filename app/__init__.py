from flask import Flask
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger

logger.remove(0)
logger.add('recipeApp.log', level="TRACE")

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
