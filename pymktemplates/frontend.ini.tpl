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
keys = root, {{project_name}}

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = {{inifile_logger_root}}
handlers = console

[logger_{{project_name}}]
level = {{inifile_logger_module}}
handlers =
qualname = {{project_name}}

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

# End logging configuration
[uwsgi]
socket = {{remote_wsgi_socket}}
master = true

uid = uwsgiuser
gid = uwsgiuser

processes = 4

harakiri = 60
harakiri-verbose = true
limit-post = 65536
post-buffering = 8192

listen = 256

max-requests = 1000

reload-on-as = 128
reload-on-rss = 96
no-orphans = true

log-slow = true
plugins = python
module = {{project_name}}
wsgi-file = {{remote_unpacked_project}}/wsgi.py

pythonpath = {{project}}/eggs/*.egg
pythonpath = {{project}}/*

