import unittest
from skysoccer.app import main, create_config
from webtest import TestApp
from pyramid import testing


class BaseTest(unittest.TestCase):

    def _clear_db(self, config):
        client = config.registry['mongodb_client']
        dbname = config.registry['settings']['dbname']
        client.drop_database(dbname)


class AppTest(BaseTest):

    def setUp(self):
        config = main({}, True)
        self._clear_db(config)
        self.testapp = TestApp(config)


class ControllerTest(BaseTest):

    def setUp(self):
        config = create_config({}, True)

        self._clear_db(config)
        self.request = testing.DummyRequest()
        self.config = testing.setUp(registry=config.registry, request=self.request, settings=config.registry['settings'])

    def tearDown(self):
        testing.tearDown()
