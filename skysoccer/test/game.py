from .base import AppTest, ControllerTest
from skysoccer.controllers.gamepage import game_view
from skysoccer.models import User, Match


class GamePageControllerTest(ControllerTest):
    players = [('d1g1', u'd1 d1'), ('d1g2', u'd2 d2'), (
        'd2g1', u'd3 d3'), ('d2g2', u'd4 d4')]

    def test_match_save(self):
        self.request.session['logged'] = 1
        self.request.POST['submit_end_game'] = 'submitting'
        self.request.session['players'] = self.players

        res = game_view(self.request)

        self.assertTrue(Match.objects().get(
            win_team='d3 d3', defeat_team='d1 d1'))

    def test_score_save(self):
        self.request.session['logged'] = 1
        self.request.POST['submit_end_game'] = 'submitting'
        self.request.session['players'] = self.players
        self.request.POST['big_score_team1'] = 2
        self.request.POST['big_score_team2'] = 1

        res = game_view(self.request)

        self.assertTrue(Match.objects().get(
            win_team='d1 d1', defeat_team='d3 d3'))
