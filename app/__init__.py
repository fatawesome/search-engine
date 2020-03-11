import os
from flask import Flask
from flask_pymongo import PyMongo
import redis

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('reuters')

application = Flask(__name__)

application.config["MONGO_URI"] = \
    'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
    '@' + \
    os.environ['MONGODB_HOSTNAME'] + ':27017/' + \
    os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db

redis_db = redis.Redis(host='redis')

from . import routes

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
