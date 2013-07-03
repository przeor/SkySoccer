def make_routes(config):
    config.add_route('index', '/')
    config.add_view('skysoccer.controllers.homepage.index_view', route_name='index')

    config.add_route('admin', '/admin.html')
    config.add_view('skysoccer.controllers.adminpage.admin_view', route_name='admin')

    config.add_route('game', '/game.html')
    config.add_view('skysoccer.controllers.gamepage.game_view', route_name='game')

    config.add_route('register', '/register.html')
    config.add_view('skysoccer.controllers.registerpage.register_view', route_name='register')

    config.add_notfound_view('skysoccer.controllers.pages.redirect_page', append_slash=True)

    config.add_static_view(name='static', path='skysoccer:static')
