from flask_restful import Resource
from flask import request, Response, jsonify
from models.models import UserModel, CardsModel, StockModel
import arrow
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity


class Input_Cards(Resource):
    """
    Class to input a card.
    5 categories and their required params :
        1. Text: none
        2. To-do list: none
        3. Meeting: url, documents, date, time
        4. Reminder: reminderList ( list of dictionaries with keys 'date' and 'time')
        5. Refill: item, count, date, time
    """
    @classmethod
    @jwt_required
    def post(cls):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = UserModel.objects.get(id=user_id)
            card = CardsModel(**body, added_by=user)
            card.save()
            user.update(push__cards=card)
            user.save()

            if card.category == 'Meeting':
                user.send_meeting_email(card, user.get_date_time(card.date,card.time))
            
            if card.category == 'Reminder':
                dates = [record['date'] for record in card.reminderList]
                times = [record['time'] for record in card.reminderList]
                unix = [] 
                for i in range(len(dates)):
                    unix[i] =unix.append(user.get_date_time(dates[i], times[i]))
                    user.send_reminder_email(card, unix[i])
            
            return {'msg': "Card was added to database"}, 200
        
        except Exception as e:
            return {'msg':str(e)}, 500


class Cards(Resource):
    """
    Class to get, edit or delete a card by id
    Params: id of card (Obtaining by cards/all)
    Output: card is displayed/edited/deleted
    """
    @classmethod
    @jwt_required
    def get(cls, _id):
        try:
            card = CardsModel.objects(id=_id).exclude('added_by').to_json()
            if not card:
                return {'msg': 'Card does not exist'}, 400
            return Response(card, mimetype="application/json", status=200)

        except Exception as e:
            return {'msg':str(e)}, 500

    @classmethod
    @jwt_required
    def put(cls, _id):
        try:
            user_id = get_jwt_identity()
            card = CardsModel.objects.get(id=_id, added_by=user_id)
            if not card:
                return {'msg': 'Card does not exist'}, 400

            body = request.get_json()
            CardsModel.objects.get(id=_id).update(**body)
            user = UserModel.objects.get(id=user_id)
            
            if card.category == 'Meeting':
                unix = user.get_date_time(card.date_time)
                print(unix)
                user.send_meeting_email(card, unix)
            
            if card.category == 'Reminder':
                for i in range(len(date_time)):
                    unix[i] = user.get_date_time(card.date_time[i])
                    user.send_reminder_email(card, unix[i])
            
            return {'msg': "Card has been modified"}, 200

        except Exception as e:
            return {'msg':str(e)}, 500

    @classmethod
    @fresh_jwt_required
    def delete(cls, _id):
        try:
            user_id = get_jwt_identity()
            card = CardsModel.objects.get(id=_id, added_by=user_id)
            if not card:
                return {'msg': 'Card does not exist'}, 400
            card.delete()
            return {'msg': "Card has been deleted"}, 200

        except Exception as e:
            return {'msg':str(e)}, 500

        
class CategoryList(Resource):
    """
    Class to display/delete cards based on category
    """
    @classmethod
    @jwt_required
    def get(cls, category):
        try:
            user_id = get_jwt_identity()
            cards = CardsModel.objects(added_by=user_id, category=category).exclude('added_by', 'category').to_json()
            return Response(cards, mimetype="application/json", status=200)
        
        except Exception as e:
            return {'msg': str(e)}, 500

    @classmethod
    @fresh_jwt_required
    def delete(cls, category):
        try:
            user_id = get_jwt_identity()
            cards = CardsModel.objects(added_by=user_id, category=category)
            if not cards:
                return {'msg': 'Card does not exist'}, 400
            cards.delete()
            return {'msg': "Group {} has been deleted".format(group)}, 200

        except Exception as e:
            return {'msg': str(e)}, 500


class CardsList(Resource):
    """
    Class to display all cards
    """
    @classmethod
    @jwt_required
    def get(cls):
        try:
            user_id = get_jwt_identity()
            cards = CardsModel.objects(added_by=user_id).exclude('added_by').to_json()
            return Response(cards, mimetype="application/json", status=200)
        
        except Exception as e:
            return {'msg': str(e)}, 500




        
