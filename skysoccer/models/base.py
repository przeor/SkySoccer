from mongoengine import Document

class Model(Document):
    meta = {'allow_inheritance': True}
