from pyramid.config import Configurator
from skysoccer.controllers import homepage

def main(settings):
    config = Configurator()

    config.add_route('index', '/')
    config.add_view(homepage.index_view,route_name='index')

    config.add_notfound_view(homepage.not_found, append_slash=True)

    config.add_static_view(name='static', path='skysoccer:static')


    return config.make_wsgi_app()
