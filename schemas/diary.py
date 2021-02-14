from ma import ma
from models.cards import CardsModel
from models.diary import DiaryModel
from models.stock import StockModel
from models.users import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class DiarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DiaryModel
        load_instance = True
        load_only = ("user")
        dump_only = ("added_by","id")
        include_fk = True