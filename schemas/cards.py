from ma import ma
from models.cards import CardsModel
from models.users import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class CardsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CardsModel
        load_instance = True
        load_only = ("user")
        dump_only = ("added_by","id")
        include_fk = True