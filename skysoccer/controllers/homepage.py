# encoding: utf8
from pyramid.httpexceptions import HTTPFound
from .base import JinjaResponse
from skysoccer.models.user import User
from skysoccer.models.match import Match


def index_view(request):
    def get_players():
        players = []
        for user in User.objects():
            players.append(user.get_fullname())
        return players

    def get_initial_data():
        return {
            "title": u"Strona główna",
            "games_count": 100,
            "login_status": u"Niezalogowany.",
        }

    def check_user(request):
        if request.POST.get('login') and request.POST.get('password'):
            login = request.POST['login']
            password = request.POST['password']
            if User.is_user_valid(login, password):
                user = User.objects().get(login=login, password=password)
                data_for_template['logged'] = request.session['logged'] = 1
                data_for_template['username'] = request.session[
                    'username'] = user.get_fullname()
                data_for_template["login_status"] = u"Zalogowano"
                return True
            else:
                data_for_template[
                    "login_status"] = u"Nie ma takiego użytkownika"
                return False
        else:
            data_for_template[
                "login_status"] = u"Nie wpisano użytkownika/hasła"
            return False

    def get_number_players():
        return User.objects().count()

    def get_number_matches():
        return Match.objects().count()

    #-------------------------------------------------------------------------
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    data_for_template["matches_count"] = get_number_matches()
    data_for_template["players_count"] = get_number_players()

    if not 'logged' in request.session:
        data_for_template['logged'] = request.session['logged'] = 0

    if request.session['logged']:
        data_for_template["login_status"] = u"Zalogowano"

    if request.POST.get('submit_login') == "submitting":
        check_user(request)
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

    return JinjaResponse(request, 'index2_base.html', data_for_template)
