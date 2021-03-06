# encoding: utf8
from .base import AppTest, ControllerTest
from skysoccer.controllers.homepage import index_view
from skysoccer.models import User, Match
from passlib.apps import custom_app_context as pwd_context

class IndexAppTest(AppTest):

    def test_root(self):
        res = self.testapp.post('/', {'elo': 1}, status=200)
        self.failUnless('SkySoccer' in res.body)


class IndexControllerTest(ControllerTest):
    good_user = {'login': 'name',  'password': pwd_context.encrypt('password'),
                'name': 'name', 'surname': 'surname'}
    bad_user = {'login': 'name bad', 'password': 'surname bad',
                'name': 'name bad', 'surname': 'surname bad'}

    def test_index(self):
        User(name='s', surname='d', login='s', password='d').save()
        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(1, len(players))
        self.assertEqual('s d', players[0]['name'])


        User(name='s2', surname='d2', login='s', password='d').save()

        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(2, len(players))
        self.assertEqual('s d', players[0]['name'])
        self.assertEqual('s2 d2', players[1]['name'])

    def test_count_matches(self):
        Match().save()

        res = index_view(self.request)
        self.assertTrue('matches_count' in res.data)

        matches = res.data['matches_count']
        self.assertEqual(1, matches)

    def test_player_count(self):
        User(**self.good_user).save()

        res = index_view(self.request)
        self.assertTrue('players_count' in res.data)

        players = res.data['players_count']
        self.assertEqual(1, players)

    def test_redirect_admim_succ(self):
        from pyramid.httpexceptions import HTTPFound
        User(**self.good_user).save()
   
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = 'password'
        res = index_view(self.request)

        self.request.POST['submit_login'] = ''
        self.request.POST['submit_admin'] = 'submitting'
        res = index_view(self.request)

        self.assertEqual(HTTPFound, type(res))
        self.assertEqual(res.location, self.request.route_path('admin'))

    def test_redirect_admin_fail(self):

        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.bad_user['login']
        self.request.POST['password'] = self.bad_user['password']
        res = index_view(self.request)

        self.request.POST['submit_admin'] = 'submitting'
        res = index_view(self.request)

        self.assertFalse(u'Panel administracyjny' in unicode(
            res.body, 'utf-8'))


class LoginControllerTest(ControllerTest):
    good_user = {'login': 'name',  'password': pwd_context.encrypt('password'),
                'name': 'name', 'surname': 'surname'}
    bad_user = {'login': 'name bad', 'password': 'surname bad',
                'name': 'name bad', 'surname': 'surname bad'}

    def setUp(self):
        super(LoginControllerTest, self).setUp()
        User(**self.good_user).save()

    def test_no_inputed_data(self):
        self.request.POST['submit_login'] = 'submitting'
        res = index_view(self.request)
        self.assertTrue('login_status' in res.data)
        self.assertEqual(
            u"Nie ma takiego użytkownika", res.data['login_status'])

    def test_bad_data_1(self):
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.bad_user['login']
        self.request.POST['password'] = self.bad_user['password']

        res = index_view(self.request)
        self.assertTrue('login_status' in res.data)
        self.assertEqual(
            u"Nie ma takiego użytkownika", res.data['login_status'])

    def test_bad_data_2(self):
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.bad_user['login']
        self.request.POST['password'] = 'password'

        res = index_view(self.request)
        self.assertTrue('login_status' in res.data)
        self.assertEqual(
            u"Nie ma takiego użytkownika", res.data['login_status'])

    def test_bad_data_3(self):
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.bad_user['login']
        self.request.POST['password'] = self.bad_user['password']

        res = index_view(self.request)
        self.assertEqual(0, res.data['logged'])

    def test_success(self):
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = 'password'

        res = index_view(self.request)
        self.assertEqual(1, res.data['logged'])


class LogoutControllerTest(ControllerTest):
    good_user = {'login': 'name',  'password': pwd_context.encrypt('password'),
                'name': 'name', 'surname': 'surname'}

    def setUp(self):
        super(LogoutControllerTest, self).setUp()
        User(**self.good_user).save()

    def test_no_submit(self):
        res = index_view(self.request)
        self.assertEqual(u"Niezalogowany.", res.data['login_status'])

    def test_not_login(self):
        res = index_view(self.request)
        self.assertFalse('submit_logout' in res.body)

    def test_when_login(self):
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = 'password'

        res = index_view(self.request)
        self.assertTrue('submit_logout' in res.body)

    def test_logout(self):
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = 'password'

        res = index_view(self.request)
        self.request.POST['submit_login'] = ''
        self.request.POST['submit_logout'] = 'submitting'

        res = index_view(self.request)

        self.assertEqual(0, res.data['logged'])
        self.assertTrue('login_status' in res.data)
        self.assertEqual(u"Wylogowano", res.data['login_status'])


class GameControllerTest(ControllerTest):
    good_user = {'login': 'name',  'password': pwd_context.encrypt('password'),
                'name': 'name', 'surname': 'surname'}

    def setUp(self):
        super(GameControllerTest, self).setUp()
        User(**self.good_user).save()

    def test_game_redirect_succ(self):
        from pyramid.httpexceptions import HTTPFound
        self.request.POST['submit_login'] = 'submitting'
        self.request.POST['login'] = self.good_user['login']
        self.request.POST['password'] = 'password'
        res = index_view(self.request)

        self.request.POST['submit_login'] = ''
        self.request.POST['submit_game'] = 'submitting'
        self.request.session['number_games'] = 15
        res = index_view(self.request)

        self.assertEqual(HTTPFound, type(res))
        self.assertEqual(res.location, self.request.route_path('game'))


class RegisterControllerTest(ControllerTest):

    def test_redirect(self):
        from pyramid.httpexceptions import HTTPFound
        self.request.POST['submit_register'] = 'submitting'
        res = index_view(self.request)
        self.assertEqual(HTTPFound, type(res))
