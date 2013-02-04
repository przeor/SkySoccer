from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

#/index.html
def index_view(request):
    from jinja2 import Environment, PackageLoader
    env = Environment(loader=PackageLoader('skysoccer', 'templates'))

    template = env.get_template('index_syntax.html')

    data = {
        "title" : "Some title",
        "games_count": 100,
        "players_count": 15
    }

    #tworzenie graczy
    tmp = []
    for i in range(1,11):
        tmp.append("Gracz%s" % i)
    data["players"] = tmp

    return Response(template.render(**data))

def not_found(request):
    msg = "Keep looking on site!"
    return HTTPNotFound(msg)

def found(request):
    return HTTPFound(location="http://www.google.pl")