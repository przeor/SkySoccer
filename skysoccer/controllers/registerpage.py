# encoding: utf8
from pyramid.httpexceptions import HTTPFound
from .base import JinjaResponse
from skysoccer.models.user import User


def register_view(request):
    def get_initial_data():
        return {
            "title": u"Rejestracja",
            "status": "",
        }

    def validate_data(request):
        user = {
            'name': request.POST.get('name'),
            'surname': request.POST.get('surname'),
            'login': request.POST.get('login'),
            'password': request.POST.get('password'),
        }
        if user['name'] == '' or user['surname'] == '' or user['login'] == '' or user['password'] == '':
            data_for_template['status'] = u'Brakuje danych'
        else:
            try:
                if User.objects().get(name=user['name'], surname=user['surname']) or User.objects().get(login=user['login'], password=user['password']):
                    data_for_template['status'] = u'Użytkownik istnieje.'
            except:
                data_for_template['status'] = u'Użytkownik nieistnieje.'
                save_user(user)

    def save_user(user):
        User(name=user['name'], surname=user[
             'surname'], login=user['login'], password=user['password']).save()
        data_for_template['status'] = u'Użytkownik dodany.'

    #-------------------------------------------------------------------------
    data_for_template = get_initial_data()

    if request.POST.get('submit_register') == 'submitting':
        validate_data(request)

    return JinjaResponse(request, 'register.html', data_for_template)
