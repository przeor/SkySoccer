def init_render_globals(config):
    config.registry['tmpl'] = {}

def add_render_globals(request):
    tmpl = request.registry['tmpl']
    tmpl['surl'] = request.static_url
    tmpl['url'] = request.route_path

def subscriber(config):
    def _add_render_globals(event):
        add_render_globals(event.request)

    config.add_subscriber(_add_render_globals, 'pyramid.events.NewRequest')
    init_render_globals(config)
