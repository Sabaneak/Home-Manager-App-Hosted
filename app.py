import os
from decouple import config

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

from resources.routes import initialize_routes
from db import db
from ma import ma
from blacklist import BLACKLIST
from oa import initialize_oauth


app = Flask(__name__)
load_dotenv(".env")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ["access", "refresh"]
app.secret_key = os.urandom(24)

CORS(app)
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def table():
    db.create_all()

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    initialize_routes(api)
    initialize_oauth(app)
    app.run(debug=True, use_reloader=False)  