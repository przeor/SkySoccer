from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound


def index_view(request):
    def get_database(database='test'):
        return request.registry['mongodb'][database]

    def get_template():
        return request.registry['jinja2'].get_template('index_syntax.html')

    def get_players():
        players = []
        db = get_database()
        users = db.users
        for value in users.find():
            players.append("%s %s" % (value['name'], value['surname']))
        return players

    def get_initial_data():
        return {
            "title": "Some title",
            "games_count": 100,
            "players_count": 15,
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

    #-------------------------------------------------------------------------
    template = get_template()
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    if request.POST.get('submit'):
        if check_user(request):
            return HTTPFound(location="/admin.html")
        else:
            return Response(template.render(**data_for_template))
    return Response(template.render(**data_for_template))
