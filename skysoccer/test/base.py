import unittest
from skysoccer.app import main, create_config
from skysoccer.subscribers import add_render_globals, init_render_globals
from webtest import TestApp
from pyramid import testing
from mongoengine import Document
from mongoengine.document import DynamicDocument


class BaseTest(unittest.TestCase):

    def _clear_db(self, config):
        for model in Document.__subclasses__():
            if model == DynamicDocument:
                continue
            model.drop_collection()


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
        init_render_globals(self.request)
        self.config = testing.setUp(
            registry=config.registry, request=self.request, settings=config.registry['settings'])
        add_render_globals(self.request)

    def tearDown(self):
        testing.tearDown()
