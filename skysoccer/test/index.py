# encoding: utf8
from .base import AppTest, ControllerTest
from skysoccer.controllers.homepage import index_view
from skysoccer.models import User, Match

class IndexAppTest(AppTest):

    def test_root(self):
        res = self.testapp.post('/', {'elo': 1}, status=200)
        self.failUnless('SkySoccer' in res.body)


class IndexControllerTest(ControllerTest):

    def test_index(self):

        User(name='s', surname='d').save()
        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(1, len(players))
        self.assertEqual('s d', players[0])

        User(name='s2', surname='d2').save()

        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(2, len(players))
        self.assertEqual('s d', players[0])
        self.assertEqual('s2 d2', players[1])

    def test_count_matches(self):
        Match().save()

        res = index_view(self.request)
        self.assertTrue('matches_count' in res.data)

        matches = res.data['matches_count']
        self.assertEqual(1, matches)

    def test_player_count(self):
        User(name='s', surname='d').save()

        res = index_view(self.request)
        self.assertTrue('players_count' in res.data)

        matches = res.data['players_count']
        self.assertEqual(1, matches)


class LoginControllerTest(ControllerTest):
    good_user = {'name': 'name', 'surname': 'surname'}
    bad_user = {'name': 'name bad', 'surname': 'surname bad'}

    def setUp(self):
        super(LoginControllerTest, self).setUp()
        User(**self.good_user).save()

    def test_no_submit(self):
        res = index_view(self.request)
        self.assertFalse('login_status' in res.data)

    def test_no_inputed_data(self):
        self.request.POST['submit_login'] = ''
        res = index_view(self.request)
        self.assertTrue('login_status' in res.data)
        self.assertEqual(u"Nie wpisano użytkownika/hasła", res.data['login_status'])

    def test_bad_data_1(self):
        self.request.POST['submit_login'] = ''
        self.request.POST['name'] = self.bad_user['name']
        self.request.POST['surname'] = self.bad_user['surname']

        res = index_view(self.request)
        self.assertTrue('login_status' in res.data)
        self.assertEqual(u"Nie ma takiego użytkownika", res.data['login_status'])

    def test_bad_data_2(self):
        self.request.POST['submit_login'] = ''
        self.request.POST['name'] = self.bad_user['name']
        self.request.POST['surname'] = self.good_user['surname']

        res = index_view(self.request)
        self.assertTrue('login_status' in res.data)
        self.assertEqual(u"Nie ma takiego użytkownika", res.data['login_status'])

    def test_bad_data_3(self):
        self.request.POST['submit_login'] = ''
        self.request.POST['name'] = self.good_user['name']
        self.request.POST['surname'] = self.bad_user['surname']

        res = index_view(self.request)
        self.assertTrue('login_status' in res.data)
        self.assertEqual(u"Nie ma takiego użytkownika", res.data['login_status'])

    def test_failed(self):
        self.request.POST['submit_login'] = ''
        self.request.POST['name'] = self.bad_user['name']
        self.request.POST['surname'] = self.bad_user['surname']

        res = index_view(self.request)
        self.assertFalse('logged' in res.data)

    def test_success(self):
        self.request.POST['submit_login'] = ''
        self.request.POST['name'] = self.good_user['name']
        self.request.POST['surname'] = self.good_user['surname']

        res = index_view(self.request)
        self.assertEqual(1, res.data['logged'])

