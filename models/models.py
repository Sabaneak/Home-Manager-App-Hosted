from db import db
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
import re

class StockModel(db.Document):
    """
    Database for user to store items.
    Fields: item, count
    """
    item = db.StringField(unique=True, required=True)
    count = db.IntField(required=True)
    added_by = db.ReferenceField('UserModel')

class CardsModel(db.DynamicDocument):
    """
    Database for user to store cards of 5 different categories.
    Categories: 'Text', 'To-do list', 'Meeting', 'Reminder', 'Refill'
    Fields (Flexible structure) : category
    """
    category = db.StringField(required=True, choices=('Text', 'To-do list', 'Meeting', 'Reminder', 'Refill'))
    added_by = db.ReferenceField('UserModel')

class DiaryModel(gj.Document):
    """
    Database for user to store diary entires.
    Fields: date, time, title, text
    """
    date = db.DateTimeField(required=True, default=datetime.datetime.now())
    time = db.DateTimeField(required=True, default=datetime.datetime.now())
    title = db.StringField(required=True)
    text = db.StringField(required=True)
    added_by = db.ReferenceField('UserModel')

class UserModel(gj.Document):
    """
    Database to store users.
    The parent database of our other 3 child databases.
    Fields: username, password, profession, email, phone
    """
    username = db.StringField(unique=True, required=True)
    password = db.StringField(required=True, regex=re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=]).{6,}$'))
    profession = db.StringField()

    email = db.EmailField(unique=True)
    phone = db.StringField(unique=True)

    phone_activated = db.BooleanField(default=False)
    email_activated = db.BooleanField(default=False)
    otp = db.StringField()

    cards = db.ListField(db.ReferenceField('CardsModel', reverse_delete_rule=db.PULL))
    diary = db.ListField(db.ReferenceField('DiaryModel', reverse_delete_rule=db.PULL))
    stock = db.ListField(db.ReferenceField('StockModel', reverse_delete_rule=db.PULL))

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
        link = request.url_root[:-1] + url_for("emailconfirm", _id=self.id)
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
        UserModel.objects.get(id=self.id).update(otp=random_num)
        self.reload()
        self.save()
        return Send_SMS.send_sms(self.otp, self.phone)

#To ensure database structure is retained
UserModel.register_delete_rule(CardsModel, 'added_by', db.CASCADE)
UserModel.register_delete_rule(DiaryModel, 'added_by', db.CASCADE)
UserModel.register_delete_rule(StockModel, 'added_by', db.CASCADE)