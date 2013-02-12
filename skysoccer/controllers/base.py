from pyramid.response import Response


class JinjaResponse(Response):

    def __init__(self, request, template_name, data):
        self.template_name = template_name
        self.data = request.registry['tmpl']
        self.data.update(data)
        template = request.registry['jinja2'].get_template(template_name)
        super(JinjaResponse, self).__init__(template.render(**self.data))
