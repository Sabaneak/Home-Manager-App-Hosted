from flask_restful import Resource
from flask import request, Response, jsonify
from models.stock import StockModel
from models.cards import CardsModel
from models.users import UserModel
from schemas.stock import StockSchema
import arrow
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

stock_schema = StockSchema()
stock_list_schema = StockSchema(many=True)

class Stock_Entry(Resource):
    """
    Class to add an item to stock.
    Params required: item, count
    """
    @classmethod
    @jwt_required
    def post(cls):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            stock = stock_schema.load(body)
            stock.added_by = user_id

            if StockModel.find_by_name(stock.item):
                return {'msg': "Item already exists"}, 404

            stock.save_to_data()
            return {'msg': "Item was added to stock database"}, 200
        
        except Exception as e:
            return {'msg':str(e)}, 500


class Stock(Resource):
    """
    Class to get or delete an item by name
    Params: name of item (Obtaining by stock/all)
    Output: item is displayed/deleted
    """
    @classmethod
    @jwt_required
    def get(cls, item):
        try:
            stock = StockModel.find_by_name(item)
            if stock:
                return stock_schema.dump(stock), 200
            return {'msg': "No such item exists"}, 404

        except Exception as e:
            return {'msg':str(e)}, 500


    @classmethod
    @fresh_jwt_required
    def delete(cls, item):
        try:
            stock = StockModel.find_by_name(item)
        
            if stock:
                stock.delete_from_data()
                return {'msg': "Item has been deleted"}, 200
            return {'msg': "No such item exists"}, 404
        
        except Exception as e:
            return {'msg':str(e)}, 500


        
class StockList(Resource):
    """
    Class to display all stock items
    """
    @classmethod
    @jwt_required
    def get(cls):
        try:
            return {'Tasks': stock_list_schema.dump(StockModel.find_all())}, 200
        except Exception as e:
            return {'msg':str(e)}, 500


class Check_Refill(Resource):
    """
    Class to check if any refills are pending. 
    If stock card refilled, deletes refill card afterwards.
    """
    @classmethod
    @jwt_required
    def post(cls):
        try:
            user_id = get_jwt_identity()
            user = UserModel.find_by_id(id=user_id)
            cards = CardsModel.find_all()

            for card in cards:
                if card.category == 'Refill':
                    current_time = arrow.now()
                    
                    if current_time.timestamp < user.get_date_time(card.data['date'], card.data['time']):
                        return {'msg': "Still not time to refill"}, 200

                    else:
                        try:
                            stock_card = StockModel.find_by_name(item=card.item)
                            stock_card.count = stock_card.count + card.data['count']
                            stock_card.save_to_data()
                            card.delete_from_data()
                            return {'msg': 'Item {} has been refilled'.format(stock_card.item)}, 200
                        except:
                            return {'msg': "Item you want to refill does not exist in your stock"}, 200           
        
        except Exception as e:
            return {'msg':str(e)}, 500