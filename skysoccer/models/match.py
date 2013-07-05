from mongoengine import Document, StringField, DateTimeField, ListField, DictField
import datetime


class Match(Document):
    number = StringField(max_length=3)
    score = ListField()
    date = DateTimeField(default=datetime.datetime.now)
    win_team = ListField()
    defeat_team = ListField()
    number_games = StringField()

    def get_win_team(self):
        return list(self.win_team)

    def get_score(self):
        return self.score

    def get_scores(self, player):
        team = list(self.defeat_team)
        team.extend(list(self.win_team))
        if player['name'] in team[0].values():
            player['scores'] += int(team[0]['points']['score'])
            player['own'] += int(team[0]['points']['own'])
        elif player['name'] in team[1].values():
            player['scores'] += int(team[1]['points']['score'])
            player['own'] += int(team[1]['points']['own'])
        elif player['name'] in team[2].values():
            player['scores'] += int(team[2]['points']['score'])
            player['own'] += int(team[2]['points']['own'])
        elif player['name'] in team[3].values():
            player['scores'] += int(team[3]['points']['score'])
            player['own'] += int(team[3]['points']['own'])

        return player

