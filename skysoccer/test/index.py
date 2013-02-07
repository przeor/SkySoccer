from .base import AppTest, ControllerTest


class IndexAppTest(AppTest):

    def test_root(self):
        res = self.testapp.post('/', {'elo': 1}, status=200)
        self.failUnless('SkySoccer' in res.body)


class IndexControllerTest(ControllerTest):

    def test_index(self):
        db = self.request.registry['mongodb']
        db.users.insert({
            'name' : 's',
            'surname' : 'd',
            })
        from skysoccer.controllers.homepage import index_view
        res = index_view(self.request)

        players = res.data['players']
        self.assertEqual(1, len(players))
        self.assertEqual('s d', players[0])
