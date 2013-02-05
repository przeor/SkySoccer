from skysoccer.settings import make_settings
from skysoccer.controllers import homepage, pages
from jinja2 import Environment, PackageLoader
from pyramid.config import Configurator
from pymongo import MongoClient
from os.path import dirname


def make_routes(config):
    config.add_route('index', '/')
    config.add_view(homepage.index_view, route_name='index')

    config.add_notfound_view(pages.redirect_page, append_slash=True)

    config.add_static_view(name='static', path='skysoccer:static')


def register_jinja(config, settings):
    config.registry['jinja2'] = Environment(
        loader=PackageLoader('skysoccer', 'templates'))


def register_mongodb(config, settings):
    config.registry['mongodb'] = MongoClient(settings['dbhost'], settings['dbport'])


def register_settings(config, settings):
    config.registry['settings'] = make_settings(settings)


def main(settings):
    config = Configurator()
    register_settings(config, settings)
    register_jinja(config, settings)
    make_routes(config)
    register_mongodb(config, settings)
    return config.make_wsgi_app()
