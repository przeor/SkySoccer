from .base import JinjaResponse
from skysoccer.models.user import User
from skysoccer.models.match import Match


def game_view(request):
    def set_initial_data():
        return {
            "title": "Panel gry",            
        }
    #-------------------------------------------------------------------------
    data_for_template = set_initial_data()
    data_for_template['logged'] = request.session['logged']
    print request.session['players']

    return JinjaResponse(request, 'game.html', data_for_template)
