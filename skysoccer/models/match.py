from mongoengine import Document, StringField


class Match(Document):
    number = StringField(max_length=5)
    name = StringField(max_length=120)
    surname = StringField(max_length=120)
