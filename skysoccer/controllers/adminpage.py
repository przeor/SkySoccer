from pyramid.response import Response


def admin_view(request):
    def get_template():
        return request.registry['jinja2'].get_template('admin.html')

    def set_initial_data():
        return {
            "title": "Panel administracyjny",
            "name" : "name",
            "surname": "surname"
                }


    #-------------------------------------------------------------------------
    template = get_template()
    data_for_template = set_initial_data()
    return Response(template.render(**data_for_template))
