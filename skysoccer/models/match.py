from mongoengine import Document, StringField


class Match(Document):
    name = StringField(max_length=120)
    surname = StringField(max_length=120)
