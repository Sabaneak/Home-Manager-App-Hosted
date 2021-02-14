from ma import ma
from models.stock import StockModel
from models.users import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StockModel
        load_instance = True
        load_only = ("user")
        dump_only = ("added_by","id")
        include_fk = True