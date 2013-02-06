from pyramid.response import Response


def admin_view(request):
    def get_database(database='test'):
        return request.registry['mongodb'][database]

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

    def check_filled_input_delete():
        if request.POST.get('delete_name') and request.POST.get('delete_surname'):
            return True
        else:
            data_for_template['delete_status'] = "Brakuje danych"
            return False

    def insert_user_to_db():
        user = {
            'surname': request.POST.get('add_surname'),
            'name': request.POST.get('add_name')
        }
        database = get_database()
        database.users.insert(user)
        data_for_template['register_status'] = "Uzytkownik dodany"

    def delete_user_from_db():
        database = get_database()
        database.users.remove({'name': request.POST.get('delete_name'), 'surname': request.POST.get('delete_surname')})
        data_for_template['delete_status'] = "Uzytkownik usuniety jezeli istnial"

    #-------------------------------------------------------------------------
    template = get_template()
    data_for_template = set_initial_data()
    if request.POST.get('add_submit') and check_filled_inputs_register():
        insert_user_to_db()
    elif request.POST.get('delete_submit') and check_filled_input_delete():
        delete_user_from_db()
    return Response(template.render(**data_for_template))
