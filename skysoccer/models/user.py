from mongoengine import Document, StringField, queryset, DateTimeField, IntField
from skysoccer.models.match import Match
import datetime


class User(Document):
    name = StringField(max_length=120)
    surname = StringField(max_length=120)
    login = StringField(max_length=120)
    password = StringField(max_length=120)
    date = DateTimeField(default=datetime.datetime.now)

    def get_fullname(self):
        return "%s %s" % (self.name, self.surname)

    def get_login(self):
        return "%s" % (self.login)

    def get_password(self):
        return "%s" % (self.password)

    @classmethod
    def is_user_valid(cls, login, password):
        try:
            cls.objects().get(login=login)
            return True
        except queryset.DoesNotExist:
            return False
