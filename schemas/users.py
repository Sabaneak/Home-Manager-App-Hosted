from ma import ma
from models.users import UserModel

from models.cards import CardsModel
from schemas.cards import CardsSchema

from models.diary import DiaryModel
from schemas.diary import DiarySchema

from models.stock import StockModel
from schemas.stock import StockSchema

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class UserSchema(ma.SQLAlchemyAutoSchema):
    cards = ma.Nested(CardsSchema, many=True)
    diary = ma.Nested(DiarySchema, many=True)
    stock = ma.Nested(StockSchema, many=True)
    
    class Meta:
        model = UserModel
        load_instance = True
        dump_only = ("id","phone_activated","email_activated","otp")