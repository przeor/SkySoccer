from .base import JinjaResponse
from skysoccer.models.user import User
from skysoccer.models.match import Match


def game_view(request):
    def set_initial_data():
        return {
            "title": "Panel gry",
        }

    def set_teams(team, request):
        players = request.session['players']
        players_in_team = []
        for player in players:
            if team in player[0]:
                players_in_team.append(player[1])
        return players_in_team
    #-------------------------------------------------------------------------
    data_for_template = set_initial_data()
    data_for_template['logged'] = request.session['logged']
    data_for_template['team1'] = set_teams('d1', request)
    data_for_template['team2'] = set_teams('d2', request)
    # print request.session['players']

    return JinjaResponse(request, 'game.html', data_for_template)
