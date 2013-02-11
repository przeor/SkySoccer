from .base import Model
from mongoengine import StringField

class Match(Model):
    name = StringField(max_length=120)
    surname = StringField(max_length=120)
