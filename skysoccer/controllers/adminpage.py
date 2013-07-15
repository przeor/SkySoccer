from .base import JinjaResponse
from skysoccer.models.user import User
from skysoccer.models.match import Match


def admin_view(request):
    def get_players():
        players = []
        for user in User.objects():
            player = {'name': user.get_fullname(),
                      'login': user.get_login(),
                      'admin': user.get_status()}
            players.append(player)
        return players

    def get_matches():
        return Match.objects

    def set_initial_data():
        return {
            "title": "Panel administracyjny",
        }

    def delete_user_from_db(userlogin):
        user = User.objects().get(login=userlogin)
        user.delete()

    def set_admin(userlogin, status):
        User.objects().get(login=userlogin).update(__raw__={ '$set': {'superuser': status}})

    def get_number_players():
        return User.objects().count()

    def get_number_matches():
        return Match.objects().count()

    #-------------------------------------------------------------------------
    data_for_template = set_initial_data()
    data_for_template['players'] = get_players()
    data_for_template['username'] = request.session['username']
    data_for_template['matches'] = get_matches()
    data_for_template['admin'] = request.session['admin']
    data_for_template["matches_count"] = get_number_matches()

    if 'username' in request.session:
        data_for_template['username'] = request.session['username']

    if request.POST.get('submit_delete'):
        for key, value in request.POST.items():
            login = data_for_template['players'][0]['login']
            if value in login:
                delete_user_from_db(value)

    elif request.POST.get('submit_admin_add'):
        set_admin(request.POST.items()[0][1], True)

    elif request.POST.get('submit_admin_remove'):
        set_admin(request.POST.items()[0][1], False)

    data_for_template['players'] = get_players()
    data_for_template["players_count"] = get_number_players()

    return JinjaResponse(request, 'admin_base.html', data_for_template)
