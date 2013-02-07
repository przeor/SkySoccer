from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound


def index_view(request):
    def get_database(database='test'):
        return request.registry['mongodb'][database]

    def get_template():
        return request.registry['jinja2'].get_template('index2.html')

    def get_players():
        players = []
        database = get_database()
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
        database = get_database()
        return database.users.find().count()

    #-------------------------------------------------------------------------
    template = get_template()
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    data_for_template["players_count"] = get_numer_players()
    if request.POST.get('submit'):
        if check_user(request):
            return HTTPFound(location="/admin.html")
    return Response(template.render(**data_for_template))
