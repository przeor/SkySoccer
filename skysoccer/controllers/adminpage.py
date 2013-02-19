from .base import JinjaResponse
from skysoccer.models.user import User


def admin_view(request):
    def get_database(database='test'):
        return request.registry['mongodb'][database]

    def get_players():
        players = []
        for user in User.objects():
            players.append(user.fullname())
        return players

    def get_template():
        return request.registry['jinja2'].get_template('admin.html')

    def set_initial_data():
        return {
            "title": "Panel administracyjny",
            "name": "name",
            "surname": "surname"
        }

    def check_filled_inputs_register():
        if request.POST.get('add_name') and request.POST.get('add_surname'):
            return True
        else:
            data_for_template['register_status'] = "Brakuje danych"
            return False

    def insert_user_to_db():
        user = {
            'surname': request.POST.get('add_surname'),
            'name': request.POST.get('add_name')
        }
        User(name=user['name'], surname=user['surname']).save()
        data_for_template['register_status'] = "Uzytkownik dodany"

    def delete_user_from_db(username):
        username = username.split()
        user = User.objects().get(name=username[0], surname=username[1])
        user.delete()

    def get_number_players():
        return User.objects().count()

    #-------------------------------------------------------------------------
    template = get_template()
    data_for_template = set_initial_data()
    data_for_template['players'] = get_players()
    data_for_template['logged'] = request.session['logged']
    data_for_template["players_count"] = get_number_players()

    if 'username' in request.session:
        data_for_template['username'] = request.session['username']

    if request.POST.get('add_submit') == 'submitting' and check_filled_inputs_register():
        insert_user_to_db()

    if request.POST.get('submit_delete'):
        for key, value in request.POST.items():
            if value in data_for_template['players']:
                delete_user_from_db(value)
    data_for_template['players'] = get_players()

    return JinjaResponse(request, 'admin_base.html', data_for_template)
