import os
from decouple import config

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from resources.routes import initialize_routes
 
from db import initialize_db
from blacklist import BLACKLIST
from oa import initialize_oauth
import flask_mongoengine
from celery import make_celery

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db' : 'myDatabase',
    'host': 'mongodb://localhost/myDatabase'
}

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ["access", "refresh"]
app.secret_key = os.urandom(24)

CORS(app)
api = Api(app)
jwt = JWTManager(app)
celery = make_celery(app)

if __name__ == '__main__':
    initialize_db(app)
    initialize_routes(api)
    initialize_oauth(app)
    app.run(debug=True, use_reloader=False)  