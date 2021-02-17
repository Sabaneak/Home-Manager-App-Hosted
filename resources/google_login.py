from flask import g, request, url_for, jsonify, Response
import requests
import json
from flask_restful import Resource
from oa import google
from flask_jwt_extended import create_access_token, create_refresh_token
import random
import string
from flask_bcrypt import generate_password_hash
from decouple import config

from models.users import UserModel

class GoogleLogin(Resource):
    @classmethod
    def get(cls):
        """
        Redirects user to login. If already in, redirects to authorize endpoint
        """
        return google.authorize(url_for("google.authorize", _external=True))


class GoogleAuthorize(Resource):
    @classmethod
    def get(cls):
        """
        Accesses user data and logs user in with email
        Output: Access and Refresh token and Calendar Access token
        """
        try:
            response = google.authorized_response()
            print(response)
        except:
             return { "msg": request.args["error"]}        
        
        token_access = response['access_token']
        user = google.get('userinfo', token=token_access)  

        try:
            google_email = user.data['email']
        except:
            return {'msg': "User of this account does not exist in database"}, 400

        user = UserModel.find_by_email(email=google_email)
        access_token = create_access_token(identity=str(user.id), fresh=True)
        refresh_token = create_refresh_token(str(user.id))

        return {'access_token': access_token, 'refresh_token': refresh_token, 'calendar_access': token_access}, 200