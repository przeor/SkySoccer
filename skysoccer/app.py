from pyramid.config import Configurator
from skysoccer.controllers import homepage, pages
from jinja2 import Environment, PackageLoader
from pymongo import MongoClient


def make_routes(config):
    config.add_route('index', '/')
    config.add_view(homepage.index_view, route_name='index')

    config.add_notfound_view(pages.redirect_page, append_slash=True)

    config.add_static_view(name='static', path='skysoccer:static')


def register_jinja(config):
    config.registry['jinja2'] = Environment(
        loader=PackageLoader('skysoccer', 'templates'))


def register_mongodb(config, host='localhost', port=27017):
    config.registry['mongodb'] = MongoClient(host, port)


def main(settings):
    config = Configurator()
    register_jinja(config)
    make_routes(config)
    register_mongodb(config)
    return config.make_wsgi_app()
