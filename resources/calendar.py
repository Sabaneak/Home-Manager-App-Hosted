from flask_restful import Resource
from flask import request, Response, jsonify
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity
from decouple import config

from calendar_setup import create_service
from datetime import datetime, timedelta

class Calendar_SetUp(Resource):
    @classmethod
    @jwt_required
    def get(cls, access_token):
        """
        Method to get calendar of user's account
        """
        service = create_service(access_token)
        settings = service.calendarList().list().execute()
        return {'Calendar': settings}, 200


class Create_Event(Resource):
    @classmethod
    @jwt_required
    def post(cls, access_token):
        """
        Method to enter event into Google Calendar
        """
        service = create_service(access_token)
        bod = request.get_json()
    
        event = {
            'summary': bod['summary'],
            'description': bod['description'],
            'start': {
                'dateTime': bod['start_time'],
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': bod['end_time'],
                'timeZone': 'Asia/Kolkata',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        
        try:
            result = service.events().insert(calendarId='primary', body=event).execute()
            print(result)
        except Exception as e:
            return {'Msg': str(e)}
        return {'msg': 'Event has been added to Google Calendar'}, 200


class Delete_Events(Resource):
    @classmethod
    @jwt_required
    def delete(cls, access_token):
        """
        Method to delete event from ID
        """
        service = create_service(access_token)
        body = request.get_json()
        
        try:
            eventId = body['eventId']
        except:
            return {'msg': "ID not provided in body"}, 404

        try:    
            result = service.events().delete(calendarId='primary', eventId=eventId).execute()
        except:
            return {'msg': "No such event found"}, 404
            
        return {'msg': 'Event has been deleted from Google Calendar'}, 200


class Get_Events(Resource):    
    @classmethod
    @jwt_required
    def get(cls, access_token):
        """
        Method to get all items of calendar
        """
        service = create_service(access_token)
        result = service.events().list(calendarId='primary', timeZone="Asia/Kolkata").execute()
        return {'Events': result['items']}, 200
