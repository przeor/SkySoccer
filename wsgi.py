from pyramid.paster import get_app, setup_logging
ini_path = 'frontend.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')