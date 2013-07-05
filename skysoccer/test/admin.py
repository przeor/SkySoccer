from .base import AppTest, ControllerTest
from skysoccer.controllers.adminpage import admin_view
from skysoccer.models import User, Match


class AdminControllerTest(ControllerTest):

    def test_count_players(self):
        User(name='s', surname='d').save()
        self.request.session['logged'] = 1

        res = admin_view(self.request)

        self.assertTrue('players_count' in res.data)

        players = res.data['players_count']
        self.assertEqual(1, players)

    def test_match_players(self):
        Match().save()
        self.request.session['logged'] = 1

        res = admin_view(self.request)

        self.assertTrue('matches_count' in res.data)

        matches = res.data['matches_count']
        self.assertEqual(1, matches)


class DeleteControllerTest(ControllerTest):

    def setUp(self):
        super(DeleteControllerTest, self).setUp()
        User(name="B1", surname="C1").save()

    def test_if_no_players(self):
        user = User.objects().get(name='B1', surname='C1')
        user.delete()
        self.request.session['logged'] = 1
        res = admin_view(self.request)
        self.assertTrue('players' in res.data)
        self.assertEqual([], res.data['players'])

    def test_delete_succesfull(self):
        self.request.session['logged'] = 1
        res = admin_view(self.request)
        self.assertTrue(u'B1 C1' in res.data['players'])

        self.request.POST['submit_delete'] = u'B1 C1'
        res = admin_view(self.request)
        self.assertEqual([], res.data['players'])
