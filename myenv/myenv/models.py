from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField


class User(Document):

    fullname = StringField(required=True)
    email = StringField(required=True, max_lenght=100)
    phone = StringField(required=False)
    age = IntField(min_value=21, max_value=75, required=True)
    send_email = BooleanField(default=False)
    send_sms = BooleanField(default=False)
    send_method = StringField(required=True)
