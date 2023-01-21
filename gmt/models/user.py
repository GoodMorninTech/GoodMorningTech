from flask_mongoengine import Document
from mongoengine import BooleanField, EmailField, StringField


class User(Document):
    email = EmailField(required=True, unique=True)
    confirmed = BooleanField(default=False)
    time = StringField(required=True)

    meta = {"collection": "users"}
