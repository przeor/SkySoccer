from pyramid.response import Response


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
    #-------------------------------------------------------------------------
    template = get_template()
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    return Response(template.render(**data_for_template))
