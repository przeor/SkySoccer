from .base import AppTest, ControllerTest
from skysoccer.controllers.adminpage import admin_view
from skysoccer.models import User


class AdminControllerTest(ControllerTest):

    def test_count_players(self):
        User(name='s', surname='d').save()
        self.request.session['logged'] = 1

        res = admin_view(self.request)

        self.assertTrue('players_count' in res.data)

        players = res.data['players_count']
        self.assertEqual(1, players)


class RegisterControllerTest(ControllerTest):

    def test_no_inputed_data(self):
        self.request.session['logged'] = 1
        self.request.POST['add_submit'] = 'submitting'
        res = admin_view(self.request)
        self.assertTrue('register_status' in res.data)
        self.assertEqual(u"Brakuje danych", res.data['register_status'])

    def test_bad_data_1(self):
        self.request.session['logged'] = 1
        self.request.POST['add_name'] = u'S1'
        self.request.POST['add_submit'] = 'submitting'
        res = admin_view(self.request)
        self.assertTrue('register_status' in res.data)
        self.assertEqual(u"Brakuje danych", res.data['register_status'])

    def test_bad_data_2(self):
        self.request.session['logged'] = 1
        self.request.POST['add_surname'] = u'S1'
        self.request.POST['add_submit'] = 'submitting'
        res = admin_view(self.request)
        self.assertTrue('register_status' in res.data)
        self.assertEqual(u"Brakuje danych", res.data['register_status'])

    def test_add_succesfull(self):
        self.request.session['logged'] = 1
        self.request.POST['add_name'] = u'S1'
        self.request.POST['add_surname'] = u'D1'
        self.request.POST['add_submit'] = 'submitting'
        res = admin_view(self.request)
        self.assertTrue('register_status' in res.data)
        self.assertEqual(u"Uzytkownik dodany", res.data['register_status'])


class DeleteControllerTest(ControllerTest):
    pass
