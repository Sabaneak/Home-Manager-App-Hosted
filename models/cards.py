from db import db
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.dialects.postgresql import JSON

class CardsModel(db.Model):
    __tablename__ = "Cards"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20))
    data = db.Column(JSON)
    added_by = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("UserModel")
    
    @classmethod
    def find_by_name(cls, name):
        ID = get_jwt_identity()
        return cls.query.filter_by(name=name, added_by=ID).first()

    @classmethod
    def find_by_id(cls, _id):
        ID = get_jwt_identity()
        return cls.query.filter_by(id=_id, added_by=ID).first()

    @classmethod
    def find_by_category(cls, category):
        ID = get_jwt_identity()
        return cls.query.filter_by(category=category, added_by=ID).all()
    
    @classmethod
    def find_all(cls):
        ID = get_jwt_identity()
        return cls.query.filter_by(added_by=ID).all()

    def save_to_data(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_data(self) -> None:
        db.session.delete(self)
        db.session.commit()