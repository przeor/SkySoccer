from .base import AppTest, ControllerTest
from skysoccer.controllers.homepage import index_view


class IndexAppTest(AppTest):

    def test_root(self):
        res = self.testapp.post('/', {'elo': 1}, status=200)
        self.failUnless('SkySoccer' in res.body)


class IndexControllerTest(ControllerTest):

    def test_index(self):
        db = self.request.registry['mongodb']
        db.users.insert({
            'name': 's',
            'surname': 'd',
        })
        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(1, len(players))
        self.assertEqual('s d', players[0])

        db.users.insert({
            'name': 's2',
            'surname': 'd2',
        })

        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(2, len(players))
        self.assertEqual('s d', players[0])
        self.assertEqual('s2 d2', players[1])

    def test_count_matches(self):
        db = self.request.registry['mongodb']
        db.match.insert({'one': 1})

        res = index_view(self.request)
        self.assertTrue('matches_count' in res.data)

        matches = res.data['matches_count']
        self.assertEqual(1, matches)

    def test_player_count(self):
        db = self.request.registry['mongodb']
        db.users.insert({
            'name': 's',
            'surname': 'd',
        })

        res = index_view(self.request)
        self.assertTrue('players_count' in res.data)

        matches = res.data['players_count']
        self.assertEqual(1, matches)

    def test_login(self):
        res = index_view(self.request)
        self.assertFalse('login_status' in res.data)
