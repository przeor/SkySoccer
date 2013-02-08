from os import path


def make_settings(settings):
    def project_paths(settings):
        import skysoccer
        settings['paths'] = {
            'project': path.dirname(path.dirname(skysoccer.__file__)),
        }
        settings['paths']['data'] = path.join(
            settings['paths']['project'],
            'data',
        )
        return settings

    def database(settings):
        settings['dbhost'] = 'localhost'
        settings['dbport'] = 27017
        settings['dbname'] = 'skysoccer'
        return settings

    def baker_session(settings):
        from os import path
        settings['session.secret'] = "change me"
        settings['session.key'] = "%(project_name)s_session" % settings
        settings['session.type'] = 'file'
        settings['session.data_dir'] = path.join(settings['paths']['data'], 'baker_data')
        settings['session.lock_dir'] = path.join(settings['paths']['data'], 'baker_lock')
        settings['session.cookie_on_exception'] = True
        settings['includes'].append('pyramid_beaker')
        return settings

    def jinja2(settings):
        settings['jinja2.directories'] = 'skysoccer:templates'
        settings['includes'].append('pyramid_jinja2')
        return settings
    #---------------------------------------------------------------------------
    settings['project_name'] = 'SkySoccer'
    settings = project_paths(settings)
    settings = database(settings)
    settings = baker_session(settings)
    settings = jinja2(settings)
    return settings
