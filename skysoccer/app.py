from pyramid.config import Configurator
from pymongo import MongoClient
from skysoccer.settings import make_settings
from skysoccer.routes import make_routes
from skysoccer.subscribers import subscriber


def register_jinja(config, settings):
    config.registry['jinja2'] = config.get_jinja2_environment()


def register_mongodb(config, settings):
    config.registry['mongodb_client'] = MongoClient(settings['dbhost'], settings['dbport'])
    config.registry['mongodb'] = config.registry['mongodb_client'][settings['dbname']]


def register_settings(config, settings):
    config.registry['settings'] = settings


def make_pyramid_includes(config, settings):
    for include in settings['includes']:
        config.include(include)


def create_config(settings={}, test_config=False):
    settings = make_settings(settings, test_config)
    config = Configurator(settings=settings)
    make_pyramid_includes(config, settings)
    register_settings(config, settings)
    register_jinja(config, settings)
    make_routes(config)
    register_mongodb(config, settings)
    subscriber(config)
    return config


def main(settings, test_config=False):
    config = create_config(settings, test_config)
    return config.make_wsgi_app()
