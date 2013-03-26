from mongoengine import Document, StringField, queryset, DateTimeField, IntField
import datetime


class User(Document):
    name = StringField(max_length=120)
    surname = StringField(max_length=120)
    date = DateTimeField(default=datetime.datetime.now)
    wins_point = IntField(default=0)
    match_count = IntField(default=0)

    def fullname(self):
        return "%s %s" % (self.name, self.surname)

    def get_match_count():
        pass

    def set_match_count():
        pass

    def get_match_win():
        pass

    def set_match_win():
        pass

    @classmethod
    def is_user_valid(cls, name, surname):
        try:
            cls.objects().get(name=name, surname=surname)
            return True
        except queryset.DoesNotExist:
            return False
