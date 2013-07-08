# encoding: utf8
from pyramid.httpexceptions import HTTPFound
from .base import JinjaResponse
from .homepage import singin_user
from skysoccer.models.user import User
from passlib.apps import custom_app_context as pwd_context

def register_view(request):
    def get_initial_data():
        return {
            "title": u"Rejestracja",
            "status": "",
            "name": "",
            "surname": ""
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
            user['password'] = pwd_context.encrypt(request.POST.get('password'))
            try:
                data_for_template[
                    'status'] = u'Użytkownik istnieje z tym loginem.'
                User.objects().get(login=user['login'])
            except:
                save_user(user)
                request.session['registered'] = 1
                data_for_template['status'] = u'Użytkownik nieistnieje.'
                return True
            finally:
                data_for_template['name'] = user['name']
                data_for_template['surname'] = user['surname']

    def save_user(user):
        User(name=user['name'], surname=user[
             'surname'], login=user['login'], password=user['password']).save()
        data_for_template['status'] = u'Użytkownik dodany.'

    #-------------------------------------------------------------------------
    data_for_template = get_initial_data()

    if request.POST.get('submit_register') == 'submitting':
        if validate_data(request):
            singin_user(request)
            return HTTPFound(location="/index2.html")

    return JinjaResponse(request, 'register.html', data_for_template)
