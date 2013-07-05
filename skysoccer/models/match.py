from mongoengine import Document, StringField, DateTimeField, ListField
import datetime


class Match(Document):
    number = StringField(max_length=3)
    score = ListField()
    date = DateTimeField(default=datetime.datetime.now)
    win_team = ListField()
    defeat_team = ListField()
    number_games = StringField()

    def get_last_match_number(self):
        pass
