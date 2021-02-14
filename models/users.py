from flask import request, url_for, jsonify
import random
import datetime
import mongoengine
import mongoengine_goodjson as gj
from flask_bcrypt import generate_password_hash, check_password_hash
from libs.mail import Send_Email
from libs.phone import Send_SMS
import datetime
import arrow
from db import db

class UserModel(db.Model):
    __tablename__ = "Users"
    # __table_args__ = (CheckConstraint("regexp_like(password,'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=]).{6,}$')", name='emailcheck'),)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=False, unique=True)
    phone_activated = db.Column(db.Boolean, default=True)
    email_activated = db.Column(db.Boolean, default=True)
    otp = db.Column(db.String(10))

    cards = db.relationship("CardsModel")
    diary = db.relationship("DiaryModel")
    stock = db.relationship("StockModel")

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls, ID):
        return cls.query.filter_by(id = ID).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def find_by_otp(cls, otp):
        return cls.query.filter_by(otp = otp).first()

    def save_to_data(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_data(self):
        db.session.delete(self)
        db.session.commit()
    
    def get_date_time(self, date, time): 
        """
        Helper function to convert date time entered by user into unix timestamp
        Params : date, time (datetime strings)
        Output : unix timestamp
        """  
        date_obj = arrow.get(date).date()
        time_obj = arrow.get(time).time()
        new_date_time = datetime.datetime.combine(date_obj, time_obj)
        unix = int(new_date_time.timestamp())
        return unix

    def send_confirmation_email(self):
        """
        Helper function to pass parameters for confirmation email to be sent
        Params : none
        Output : redirect to mail library
        """  
        link = request.url_root[:-1] + url_for("emailconfirm", user_id=self.id)
        html = f'<html>Please click the link to join your meeting: <a href={link}>{link}</a></html>'
        return Send_Email.send_email(self.email, html=html)

    def send_meeting_email(self, card, unix):
        """
        Helper function to pass parameters for meeting email to be sent
        Params : none
        Output : redirect to mail library
        """  
        link = card.url
        html = f'<html><p> <a href={link}>{link}</a><br>Remember to bring your {card.documents}</p></html>'
        return Send_Email.send_reminder(self.email, html=html, unix=unix)

    def send_reminder_email(self, card, unix):
        """
        Helper function to pass parameters for reminder email to be sent
        Params : none
        Output : redirect to mail library
        """  
        html = f'<html><p>You asked for a reminder</p></html>'
        return Send_Email.send_reminder(self.email, html=html, unix=unix)

    def sms(self):
        """
        Helper function to generate OTP to be sent
        Params : none
        Output : redirect to phone library
        """  
        random_num = str(random.randrange(100000, 999999, 1))
        self.otp=random_num
        self.save_to_data()
        return Send_SMS.send_sms(self.otp, self.phone)
    
    