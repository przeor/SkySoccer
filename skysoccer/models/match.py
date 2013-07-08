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

    def get_defeat_team(self):
        return list(self.defeat_team)

    def get_score(self):
        return self.score

    def get_players_scores(self, player):
        team = list(self.defeat_team)
        team.extend(list(self.win_team))

        def update_scores(number):
            player['scores'] += int(team[number]['points']['score'])
            player['own'] += int(team[number]['points']['own'])

        for i in range(0, 4):
            if player['name'] in team[i].values():
                update_scores(i)
                break

        return player
