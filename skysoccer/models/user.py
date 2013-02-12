from .base import Model
from mongoengine import StringField, queryset

class User(Model):
    name = StringField(max_length=120)
    surname = StringField(max_length=120)

    def fullname(self):
        return "%s %s" % (self.name, self.surname)

    @classmethod
    def is_user_valid(cls, name, surname):
        try:
            cls.objects().get(name=name, surname=surname)
            return True
        except queryset.DoesNotExist:
            return False


