from flask_restful import Resource
from flask import request, Response, jsonify
from schemas.cards import CardsSchema
from models.cards import CardsModel
from models.users import UserModel
import arrow
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

card_schema = CardsSchema()
card_list_schema = CardsSchema(many=True)


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
            user = UserModel.find_by_id(user_id)
            body = request.get_json()

            card = card_schema.load(body)
            card.added_by = user_id
            card.save_to_data()

            if card.category == 'Meeting':
                user.send_meeting_email(card, user.get_date_time(card.data['date'],card.data['time']))
            
            if card.category == 'Reminder':
                dates = [record['date'] for record in card.data['reminderList']]
                times = [record['time'] for record in card.data['reminderList']]
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
            card = CardsModel.find_by_id(_id)
            if card:
                return card_schema.dump(card), 200
            return {'msg': "No such task exists"}, 404

        except Exception as e:
            return {'msg':str(e)}, 500

    @classmethod
    @jwt_required
    def put(cls, _id):
        try:
            card = CardsModel.find_by_id(_id)
            given_card = request.get_json()
        
            if not card:
                return {'msg': "No such card entry exists"}
            
            given_card.id = card.id
            given_card.save_to_data()
            card.delete_from_data()
            
            if given_card.category == 'Meeting':
                user.send_meeting_email(card, user.get_date_time(given_card.data['date'],given_card.data['time']))
            
            if given_card.category == 'Reminder':
                dates = [record['date'] for record in given_card.data['reminderList']]
                times = [record['time'] for record in given_card.data['reminderList']]
                unix = [] 
                for i in range(len(dates)):
                    unix[i] =unix.append(user.get_date_time(dates[i], times[i]))
                    user.send_reminder_email(card, unix[i])
            
            return {'msg': "Card has been modified"}, 200

        except Exception as e:
            return {'msg':str(e)}, 500

    @classmethod
    @fresh_jwt_required
    def delete(cls, _id):
        try:
            card = CardsModel.find_by_id(_id)
            if card:
                card.delete_from_data()
                return {'msg': "Card has been deleted"}, 200
            return {'msg': "No such card exists"}, 404
        
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
            return {category: card_list_schema.dump(CardsModel.find_by_category(category=category))}, 200
        except Exception as e:
            return {'msg':str(e)}, 500

    @classmethod
    @fresh_jwt_required
    def delete(cls, category):
        try:
            cards = card_list_schema.dump(CardsModel.find_by_category(category=category))
            if not cards:
                return {'msg': 'Category does not exist'}, 400
            cards.delete()
            return {'msg': "Category {} has been deleted".format(group)}, 200

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
            return {'Tasks': stock_list_schema.dump(StockModel.find_all())}, 200
        except Exception as e:
            return {'msg':str(e)}, 500




        
