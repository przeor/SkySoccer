from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pymongo import MongoClient


def index_view(request):
    def connect_database():
        connection = MongoClient()
        return connection['test']

    def get_template():
        return request.registry['jinja2'].get_template('index_syntax.html')

    def get_players():
        players = []
        db = connect_database()
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
