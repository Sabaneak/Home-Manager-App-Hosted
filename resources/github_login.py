from flask import g, request, url_for, jsonify, Response
import requests
import json
from flask_restful import Resource
from oa import github
from flask_jwt_extended import create_access_token, create_refresh_token
import random
import string
from flask_bcrypt import generate_password_hash
from decouple import config

from models.models import UserModel

class GithubLogin(Resource):
    @classmethod
    def get(cls):
        """
        Redirects user to login. If already in, redirects to authorize endpoint
        """
        return github.authorize(url_for("github.authorize", _external=True)), 200


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        """
        Accesses user data and logs user in with email
        Output: Access and Refresh token
        """
        try:
            response = github.authorized_response()
        except:
             return { "msg": request.args["error"]}        
        
        g.access_token = response['access_token']
        github_user = github.get('user', token=g.access_token)

        try:
            github_username = github_user.data['login']
            github_email = github_user.data['email']
            
            if github_email is None:
                return {'msg': "Your email has not been linked to your Github account. Cannot login"}, 400
            
        except:
            return {'msg': "User of this account does not exist in database"}, 400

        user = UserModel.objects.get(email=github_email)
        access_token = create_access_token(identity=str(user.id), fresh=True)
        refresh_token = create_refresh_token(str(user.id))

        return {'access_token': access_token, 'refresh_token': refresh_token}, 200

        