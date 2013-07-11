[app:main]
use = egg:{{project_name}}

{% if inifile_with_server -%}
[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = 6543
{%- endif %}

# Begin logging configuration

[loggers]
keys = root, {{project_name}}, beaker.container

[handlers]
keys = console, beaker, all

[formatters]
keys = generic

[logger_root]
level = DEBUG
handlers = all

[logger_{{project_name}}]
level = {{inifile_logger_module}}
handlers = console
qualname = {{project_name}}

[logger_beaker.container]
level = DEBUG
handlers = beaker
qualname = beaker.container

[logger_routes]
level = INFO
handlers = console
qualname = routes.middleware

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = DEBUG
formatter = generic

[handler_beaker]
class = FileHandler
args = ('{{beaker_log_file}}',)
level = DEBUG
formatter = generic

[handler_all]
class = FileHandler
args = ('{{all_path}}',)
level = DEBUG
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

# End logging configuration
[uwsgi]
#socket = {{remote_wsgi_socket}}
http = 127.0.0.1:8181
master = true

uid = uwsgiuser
gid = uwsgiuser

processes = 4

harakiri = 60
harakiri-verbose = true
limit-post = 65536
post-buffering = 8192

listen = 128

max-requests = 1000

reload-on-as = 128
reload-on-rss = 96
no-orphans = true

log-slow = true
plugins = python
module = {{project_name}}
#wsgi-file = {{wsgi}}

pythonpath = {{project}}/eggs/*.egg
pythonpath = {{project}}/*
pythonpath = {{project}}/skysoccer/*

