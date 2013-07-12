from .base import AppTest, ControllerTest
from skysoccer.controllers.adminpage import admin_view
from skysoccer.models import User, Match


class AdminControllerTest(ControllerTest):

    def test_count_players(self):
        User(name='s', surname='d').save()
        self.request.session['admin'] = 1

        res = admin_view(self.request)

        self.assertTrue('players_count' in res.data)
        self.assertEqual(1, res.data['players_count'])
        self.assertTrue('s d' in res.body)

    def test_match_players(self):
        Match().save()
        self.request.session['admin'] = 1

        res = admin_view(self.request)

        self.assertTrue('matches_count' in res.data)
        self.assertEqual(1, res.data['matches_count'])
        self.assertFalse('id="match_index"' in res.body)

    def test_player_data(self):
        User(name='a', surname='a', login='a', password='a').save()
        self.request.session['admin'] = 1

        res = admin_view(self.request)

        self.assertTrue('a a' in res.body)

    def test_match_data(self):
        team1 = {'username': 'a a', 'points': {'own': '5', 'score': '10'}}
        team2 = {'username': 'b b', 'points': {'own': '5', 'score': '5'}}
        match = {'score': ['3', '1'],
                 'win_team': [team1, team1],
                 'defeat_team': [team2, team2],
                 'number_games': '5'}
        Match(**match).save()
        User(name='a', surname='a').save()
        User(name='b', surname='b').save()

        self.request.session['admin'] = 1
        res = admin_view(self.request)

        self.assertTrue('matches_count' in res.data)
        self.assertEqual(1, res.data['matches_count'])
        self.assertTrue('3 : 1' in res.body)


class DeleteControllerTest(ControllerTest):

    def setUp(self):
        super(DeleteControllerTest, self).setUp()
        User(name="B1", surname="C1", login='B1 C1').save()

    def test_if_no_players(self):
        user = User.objects().get(name='B1', surname='C1')
        user.delete()
        self.request.session['admin'] = 1
        res = admin_view(self.request)
        self.assertTrue('players' in res.data)
        self.assertEqual([], res.data['players'])

    def test_delete_succesfull(self):
        self.request.session['admin'] = 1
        res = admin_view(self.request)
        self.assertTrue(u'B1 C1' in res.data['players'][0]['name'])

        self.request.POST['submit_delete'] = u'B1 C1'
        res = admin_view(self.request)

        self.assertEqual([], res.data['players'])
