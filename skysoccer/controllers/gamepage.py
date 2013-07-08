from .base import JinjaResponse
from pyramid.httpexceptions import HTTPFound
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
        team1 = [{'username': data_for_template['team1'][0], 'points': {'score': request.POST.get('score_team1_player1'), 'own': request.POST.get('own_team1_player1')}}, {
                 'username': data_for_template['team1'][1], 'points': {'score': request.POST.get('score_team1_player2'), 'own': request.POST.get('own_team1_player2')}}]

        team2 = [{'username': data_for_template['team2'][0], 'points': {'score': request.POST.get('score_team2_player1'), 'own': request.POST.get('own_team2_player1')}}, {
                 'username': data_for_template['team2'][1], 'points': {'score': request.POST.get('score_team2_player2'), 'own': request.POST.get('own_team2_player2')}}]

        score = [request.POST.get(
            'big_score_team1'), request.POST.get('big_score_team2')]
        if score[0] > score[1]:
            win_team = team1
            defeat_team = team2
        else:
            win_team = team2
            defeat_team = team1

        Match(score=score, win_team=win_team, defeat_team=defeat_team,
              number_games=request.session['number_games']).save()

        return HTTPFound(location="/index2.html")

    #-------------------------------------------------------------------------
    data_for_template = set_initial_data()
    if request.session['logged']:
        data_for_template['logged'] = request.session['logged']
        data_for_template['team1'] = set_teams('d1', request)
        data_for_template['team2'] = set_teams('d2', request)
        data_for_template['number_games'] = request.session['number_games']

    if request.POST.get('submit_end_game') == "submitting":
        return submit_score(request)
    return JinjaResponse(request, 'game.html', data_for_template)
