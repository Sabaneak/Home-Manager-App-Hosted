from flask_restful import Resource
from flask import request, Response, jsonify
from models.models import UserModel, StockModel, CardsModel
import arrow
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity

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
            user = UserModel.objects.get(id=user_id)
            stock = StockModel(**body, added_by=user)
            stock.save()
            user.update(push__stock=stock)
            user.save()
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
            user_id = get_jwt_identity()
            stock = StockModel.objects(item=item).exclude('added_by').to_json()
            if not stock:
                return {'msg': 'Item does not exist'}, 400
            return Response(stock, mimetype="application/json", status=200)

        except Exception as e:
            return {'msg':str(e)}, 500


    @classmethod
    @fresh_jwt_required
    def delete(cls, item):
        try:
            user_id = get_jwt_identity()
            stock = StockModel.objects.get(id=_id, added_by=user_id)
            if not stock:
                return {'msg': 'Item does not exist'}, 400
            stock.delete()
            return {'msg': "Item has been deleted"}, 200

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
            user_id = get_jwt_identity()
            stock = StockModel.objects(added_by=user_id).exclude('added_by').to_json()
            return Response(stock, mimetype="application/json", status=200)
        
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
            user = UserModel.objects.get(id=user_id)
            cards = CardsModel.objects(added_by=user_id)
            for card in cards:
                if card.category == 'Refill':
                    current_time = arrow.now()
                    
                    if current_time.timestamp < user.get_date_time(card.date, card.time):
                        return {'msg': "Still not time to refill"}, 200

                    else:
                        try:
                            stock_card = StockModel.objects.get(added_by=user_id, item=card.item)
                            stock_card.count = stock_card.count + card.count
                            stock_card.save()
                            card.delete()
                            return {'msg': 'Item {} has been refilled'.format(stock_card.item)}, 200
                        except:
                            return {'msg': "Item you want to refill does not exist in your stock"}, 200           
        
        except Exception as e:
            return {'msg':str(e)}, 500