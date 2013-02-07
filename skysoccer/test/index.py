from .base import AppTest, ControllerTest


class IndexAppTest(AppTest):

    def test_root(self):
        res = self.testapp.post('/', {'elo': 1}, status=200)
        self.failUnless('SkySoccer' in res.body)


class IndexControllerTest(ControllerTest):

    def test_index(self):
        from skysoccer.controllers.homepage import index_view

        db = self.request.registry['mongodb']
        db.users.insert({
            'name' : 's',
            'surname' : 'd',
            })
        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(1, len(players))
        self.assertEqual('s d', players[0])

        db.users.insert({
            'name' : 's2',
            'surname' : 'd2',
            })

        res = index_view(self.request)

        self.assertTrue('players' in res.data)
        players = res.data['players']
        self.assertEqual(2, len(players))
        self.assertEqual('s d', players[0])
        self.assertEqual('s2 d2', players[1])
