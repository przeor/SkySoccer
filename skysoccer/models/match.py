from mongoengine import Document, StringField, DateTimeField
import datetime


class Match(Document):
    number = StringField(max_length=5)
    score = StringField(max_length=3)
    date = DateTimeField(default=datetime.datetime.now)
