# encoding: utf8
from pyramid.httpexceptions import HTTPFound
from .base import JinjaResponse
from skysoccer.models.user import User
from skysoccer.models.match import Match
from passlib.apps import custom_app_context as pwd_context


def index_view(request):
    def get_initial_data():
        return {
            "title": u"Strona główna",
            "login_status": u"Niezalogowany.",
        }

    def get_matches():
        return Match.objects

    def get_players():
        def get_goals(players):
            for player in players:
                for match in Match.objects():
                    player = match.get_players_scores(player)
            return players

        players = []
        player = {}
        for user in User.objects():
            player = {'scores': 0, 'own': 0}
            player['name'] = name = user.get_fullname()
            player['win_matches'] = Match.objects(
                __raw__={'win_team.username': name}).count()
            player['defeat_matches'] = Match.objects(
                __raw__={'defeat_team.username': name}).count()
            query = {'$or': [{'win_team.username': name}, {
                'defeat_team.username': name}]}
            player['matches'] = Match.objects(__raw__=query).count()
            players.append(dict(player))
        players = get_goals(players)
        players = sorted(players, key=lambda k: k['scores'], reverse= True)
        return players

    def get_number_players():
        return User.objects().count()

    def get_number_matches():
        return Match.objects().count()

    #-------------------------------------------------------------------------
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    data_for_template['matches'] = get_matches()
    data_for_template["matches_count"] = get_number_matches()
    data_for_template["players_count"] = get_number_players()

    if request.POST.get('submit_login') == "submitting":
        if singin_user(request):
            request = singin_user(request)
            data_for_template["login_status"] = u"Zalogowano"
        else:
            data_for_template["login_status"] = u"Nie ma takiego użytkownika"

    elif request.POST.get('submit_logout') == "submitting":
        data_for_template['logged'] = request.session['logged'] = 0
        data_for_template['login_status'] = u"Wylogowano"

    elif request.POST.get('submit_admin') == "submitting":
        return HTTPFound(location="/admin.html")

    elif request.POST.get('submit_game') == "submitting":
        request.session['players'] = request.POST.items()
        request.session['number_games'] = request.POST.get('number_games')
        return HTTPFound(location="/game.html")

    elif request.POST.get('submit_register') == "submitting":
        return HTTPFound(location="/register.html")

    if not 'registered' in request.session:
        request.session['registered'] = 0

    if not 'logged' in request.session:
        data_for_template['logged'] = request.session['logged'] = 0
    else:
        data_for_template['logged'] = request.session['logged']

    if request.session['logged'] or request.session['registered']:
        data_for_template['username'] = request.session['username']

    return JinjaResponse(request, 'index2_base.html', data_for_template)


def singin_user(request):
    if request.POST.get('login') and request.POST.get('password'):
        login = request.POST['login']
        password = request.POST['password']
        if User.is_user_valid(login, password):
            user = User.objects().get(login=login)
            if pwd_context.verify(password, user.get_password()):
                request.session['logged'] = 1
                request.session['username'] = user.get_fullname()
                return request
            return False
        else:
            return False
