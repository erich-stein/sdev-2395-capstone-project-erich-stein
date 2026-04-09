from flask import Flask, jsonify
from config import Config
from flask_cors import CORS
from loguru import logger

logger.remove(0)
logger.add('app.log', level="TRACE")

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

@app.route('/api', methods=['GET'])
def hello_world():
  logger.debug('Retrieving data.')
  return jsonify({"message":"Hello, World!"})

if __name__ == '__main__':
  app.run(debug=True)