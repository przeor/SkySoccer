from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound


#/index.html
def index_view(request):
    def get_template():
        return request.registry['jinja2'].get_template('index_syntax.html')

    def get_players():
        players = []
        for i in range(1, 11):
            players.append("Gracz%s" % i)
        return players

    def get_initial_data():
        return {
            "title": "Some title",
            "games_count": 100,
            "players_count": 15,
            "url": request.static_url,
        }
    #---------------------------------------------------------------------------
    template = get_template()
    data_for_template = get_initial_data()
    data_for_template["players"] = get_players()
    return Response(template.render(**data_for_template))


def not_found(request):
    msg = "Keep looking on site!"
    return HTTPNotFound(msg)


def found(request):
    return HTTPFound(location="http://www.google.pl")
