from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response('Hello !')


def main(settings):
    config = Configurator()
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    return config.make_wsgi_app()
