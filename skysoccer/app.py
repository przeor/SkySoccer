from pyramid.config import Configurator
from skysoccer.controllers import homepage
from jinja2 import Environment, PackageLoader


def make_routes(config):
    config.add_route('index', '/')
    config.add_view(homepage.index_view, route_name='index')

    config.add_notfound_view(homepage.not_found, append_slash=True)

    config.add_static_view(name='static', path='skysoccer:static')


def register_jinja(config):
    config.registry['jinja2'] = Environment(loader=PackageLoader('skysoccer', 'templates'))


def main(settings):
    config = Configurator()
    register_jinja(config)
    make_routes(config)
    return config.make_wsgi_app()
