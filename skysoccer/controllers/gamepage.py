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

    def submit_score(request):
        print request.POST.get('big_score_team1'), request.POST.get('big_score_team2')
    #-------------------------------------------------------------------------
    data_for_template = set_initial_data()
    data_for_template['logged'] = request.session['logged']
    data_for_template['team1'] = set_teams('d1', request)
    data_for_template['team2'] = set_teams('d2', request)
    # print request.session['players']
    if request.POST.get('submit_end_game') == "submitting":
        submit_score(request)
    return JinjaResponse(request, 'game.html', data_for_template)
