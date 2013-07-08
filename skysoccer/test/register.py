# encoding: utf8
from .base import AppTest, ControllerTest
from skysoccer.controllers.registerpage import register_view
from skysoccer.models import User
from pyramid.httpexceptions import HTTPFound

class RegisteringControllerTest(ControllerTest):
    good_user = {'login': 'login', 'password':
                 'password', 'name': 'name', 'surname': 'surname'}

    def test_register_succ(self):
        self.request.POST['name'] = self.good_user['name']
        self.request.POST['surname'] = self.good_user['surname']
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = self.good_user['password']
        self.request.POST['submit_register'] = 'submitting'

        res = register_view(self.request)

        self.assertEqual(HTTPFound, type(res))

    def test_register_fail_1(self):
        self.request.POST['name'] = ''
        self.request.POST['surname'] = ''
        self.request.POST['login'] = ''
        self.request.POST['password'] = ''
        self.request.POST['submit_register'] = 'submitting'

        res = register_view(self.request)

        self.assertEqual(u'Brakuje danych', res.data['status'])

    def test_register_fail_2(self):
        self.request.POST['name'] = ''
        self.request.POST['submit_register'] = 'submitting'

        res = register_view(self.request)

        self.assertEqual(u'Brakuje danych', res.data['status'])

        self.request.POST['name'] = ''
        self.request.POST['surname'] = ''

        res = register_view(self.request)

        self.assertEqual(u'Brakuje danych', res.data['status'])

        self.request.POST['name'] = ''
        self.request.POST['surname'] = ''
        self.request.POST['login'] = ''

        res = register_view(self.request)

        self.assertEqual(u'Brakuje danych', res.data['status'])

    def test_already_registered(self):
        self.request.POST['name'] = self.good_user['name']
        self.request.POST['surname'] = self.good_user['surname']
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = self.good_user['password']
        self.request.POST['submit_register'] = 'submitting'

        res = register_view(self.request)
        res = register_view(self.request)

        self.assertEqual(u'Użytkownik istnieje z tym loginem.', res.data['status'])

    def test_form_refilled(self):
        another_good_user = {'login': 'login2'}
        self.request.POST['name'] = self.good_user['name']
        self.request.POST['surname'] = self.good_user['surname']
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = self.good_user['password']
        self.request.POST['submit_register'] = 'submitting'

        res = register_view(self.request)
        res = register_view(self.request)
        self.assertEqual(u'Użytkownik istnieje z tym loginem.', res.data['status'])

        self.request.POST['login'] = another_good_user['login']

        res = register_view(self.request)
        
        self.assertEqual(HTTPFound, type(res))
