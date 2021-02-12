from models.models import UserModel

from flask import request, redirect, url_for
from flask_restful import Resource

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    fresh_jwt_required
)
from blacklist import BLACKLIST

class UserRegister(Resource):
    """
    Class to register a new user to the database. Sends confirmational Email and SMS.
    Params(Required) : username, password, email, phone, profession
    Output: Confimration user has been added to db without verification
    """
    @classmethod
    def post(cls):
        try:
            body = request.get_json()
            
            if 'email' not in body:
                return {'msg': 'Email has not been provided'}, 400

            if 'phone' not in body:
                return {'msg': 'Phone Number has not been provided'}, 400

            if 'profession' not in body:
                return {'msg': 'Profession has not been provided'}, 400

            user = UserModel(**body)
            user.save()
            user.send_confirmation_email()
            user.sms()
            return {'msg': 'User has been added to database. Verification pending.'}, 200

        except Exception as e:
            return {'msg':str(e)}, 500

class EmailConfirm(Resource):
    """
    Class to confirm email user when they receive link from email
    """
    @classmethod
    def get(cls, _id):
        try:
            user = UserModel.objects.get(id=_id)

            if not user:
                return {'msg': "User does not exist"}, 400

            if user.email_activated:
                return {'msg': "Already confirmed"}, 400

            UserModel.objects.get(id=_id).update(email_activated=True)
            user.reload()
            user.save()
            return {'msg': "Registration has been confirmed for email {}".format(user.email)}, 200

        except Exception as e:
            return {'msg':str(e)}, 500


class OTPConfirm(Resource):
    """
    Class to confirm phone number when OTP received is entered
    """
    @classmethod
    def get(cls, otp):
        try:
            user = UserModel.objects.get(otp=otp)
            
            if user.phone_activated:
                return {'msg': "Already confirmed"}, 400

            user.update(phone_activated=True)
            user.reload()
            user.save()
            return {'msg': "Registration has been confirmed for phone {}".format(user.phone)}, 200

        except:
            return {'msg': "Invalid OTP"}, 400

class UserLogin(Resource):
    """
    Class to login user.
    Params : username, password
    Output: Access and refresh token
    """
    @classmethod
    def post(cls):
        try:
            body = request.get_json()
            user = UserModel.objects.get(username=body.get('username'))
            check = (body.get('password') == user.password)

            if not check:
                return {'msg': 'Credentials are not matching. Please try again'}, 400

            if not user.email_activated:
                return {'msg': 'Email has not been confirmed'}, 400

            if not user.phone_activated:
                return {'msg': 'Phone has not been confirmed'}, 400
                
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(str(user.id))
            return { 'access_token': access_token, 'refresh_token': refresh_token}, 200
        
        except Exception as e:
            return {'msg':str(e)}, 500
         

class UserLogout(Resource):
    """
    Class to logout user
    """
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {'msg': 'User ID {} has been logged out'.format(user_id)}, 200


class TokenRefresh(Resource):
    """
    Class to generate a new access token
    """
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class CheckUsername(Resource):
    """
    Class to verify if username is available
    """
    @classmethod
    def get(cls, username):
        try:
            user = UserModel.objects.get(username=username)
            return {'msg': "Username already exists"}, 200
        except:
            return {'msg': "Username does not exist"}, 400


class ChangePassword(Resource):
    """
    Class that replaces your existing password with a new one
    """
    @classmethod
    @jwt_refresh_token_required
    def post(cls, password):
        try:
            user_id = get_jwt_identity()
            UserModel.objects.get(id=user_id).update(password=password)
            user = UserModel.objects.get(id=user_id)
            
            if not user:
                return {'msg': 'User does not exist'}, 400

            user.save()
            return {'msg': "Password has been updated"}, 200
        
        except Exception as e:
            return {'msg':str(e)}, 500



            

        
        
      

