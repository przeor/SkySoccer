from pyramid.response import Response


def admin_view(request):
    def get_database(database='test'):
        return request.registry['mongodb'][database]

    def get_players():
        players = []
        database = get_database()
        for value in database.users.find():
            players.append("%s %s" % (value['name'], value['surname']))
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
        database = get_database()
        database.users.insert(user)
        data_for_template['register_status'] = "Uzytkownik dodany"

    def delete_user_from_db(username):
        username = username.split()
        database = get_database()
        database.users.remove({'name': username[0], 'surname': username[1]})

    #-------------------------------------------------------------------------
    template = get_template()
    data_for_template = set_initial_data()
    data_for_template['players'] = get_players()
    if request.POST.get('add_submit') and check_filled_inputs_register():
        insert_user_to_db()
    if request.POST.items():
        for key, value in request.POST.items():
            if key in data_for_template['players']:
                delete_user_from_db(key)
    data_for_template['players'] = get_players()

    return Response(template.render(**data_for_template))
