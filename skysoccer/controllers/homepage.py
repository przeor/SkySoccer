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
            "url": request.static_url,
        }

    def check_user(request):
        if request.POST.get('name') and request.POST.get('surname'):
            username = request.POST.get('name') + " " + request.POST.get('surname')
            if username in data_for_template['players']:
                return True
            else:
                data_for_template["login_status"] = "Nie ma takiego uzytkownika"
                return False
        else:
            data_for_template["login_status"] = "Nie wpisano uzytkownika/hasla"
            return False

    def get_numer_players():
        database = request.registry['mongodb']
        return database.users.find().count()

    #-------------------------------------------------------------------------
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    data_for_template["players_count"] = get_numer_players()
    if request.POST.get('submit'):
        if check_user(request):
            return HTTPFound(location="/admin.html")

    return JinjaResponse(request, 'index2.html', data_for_template)
