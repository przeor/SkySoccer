def make_settings(settings={}, test_config=False):
    def initialize_settings(settings):
        settings['includes'] = []
        return settings

    def import_default(settings):
        from skysoccer.settings import default
        return default.make_settings(settings)

    def import_local_without_errors(settings):
        try:
            from skysoccer.settings import local
            local.make_settings(settings)
        except ImportError:
            pass
        return settings

    def import_test(settings):
        from skysoccer.settings import tests
        tests.make_settings(settings)
        return settings

    #---------------------------------------------------------------------------
    settings = initialize_settings(settings)
    settings = import_default(settings)
    settings = import_local_without_errors(settings)
    if test_config:
        settings = import_test(settings)
    return settings
