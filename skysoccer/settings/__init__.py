def make_settings(settings={}):
    from skysoccer.settings import default
    settings = default.make_settings(settings)

    try:
        from skysoccer.settings import local
        local.make_settings(settings)
    except ImportError:
        pass

    return settings
