# encoding: utf8
from pyramid.httpexceptions import HTTPFound
from .base import JinjaResponse


def index_view(request):
    def get_players():
        players = []
        database = request.registry['mongodb']
        for value in database.users.find():
            players.append("%s %s" % (value['name'], value['surname']))
        return players

    def get_initial_data():
        return {
            "title": "Some title",
            "games_count": 100,
        }

    def check_user(request):
        if request.POST.get('name') and request.POST.get('surname'):
            username = request.POST.get('name') + " " + request.POST.get('surname')
            if username in data_for_template['players']:
                data_for_template['logged'] = request.session['logged'] = 1
                data_for_template['username'] = request.session['username'] = username
                return True
            else:
                data_for_template["login_status"] = u"Nie ma takiego użytkownika"
                return False
        else:
            data_for_template["login_status"] = u"Nie wpisano użytkownika/hasła"
            return False

    def get_number_players():
        database = request.registry['mongodb']
        return database.users.find().count()

    def get_number_matches():
        database = request.registry['mongodb']
        return database.match.find().count()

    #-------------------------------------------------------------------------
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    data_for_template["matches_count"] = get_number_matches()
    data_for_template["players_count"] = get_number_players()

    if not 'logged' in request.session:
        data_for_template['logged'] = request.session['logged'] = 0

    if request.POST.get('submit_login') == "":
        check_user(request)
    if request.POST.get('submit_logout') == "":
        data_for_template['logged'] = request.session['logged'] = 0
        data_for_template['login_status'] = u"Wylogowano"
    if request.POST.get('submit_admin') == "":
        return HTTPFound(location="/admin.html")

    return JinjaResponse(request, 'index2.html', data_for_template)
