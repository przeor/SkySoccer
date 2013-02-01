from pymk.task import BaseTask, AddTask
from pymk.dependency import FileChanged, AlwaysRebuild
from pymk.extra import find_files, run_cmd, touch
from pymk.template import mktemplate
import os
import logging

logger = logging.getLogger('pymk')

@AddTask
class clear(BaseTask):

    dependencys = [AlwaysRebuild()]

    def build(self):
        for filename in find_files('src', '*.pyc'):
            os.unlink(filename)
            logger.debug('Deleted: %s' % (filename,))


class bootstrap(BaseTask):
    output_file = 'bin/buildout'

    dependencys = []

    url = 'http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py'

    def build(self):
        run_cmd(['wget ' + self.url ], True)
        run_cmd(['python2 bootstrap.py'], True)


class data_dir(BaseTask):
    output_file = 'data'

    dependencys = []

    def build(self):
        try:
            os.mkdir(self.output_file)
        except OSError:
            pass


@AddTask
class buildout(BaseTask):
    output_file = 'bin/py'

    dependencys = [
        data_dir.dependency_FileExists(),
        bootstrap.dependency_FileChanged(),
        FileChanged('setup.py'),
        FileChanged('eggs'),
        FileChanged('buildout.cfg'),
    ]

    def build(self):
        run_cmd(['./bin/buildout'], True)
        touch('./bin/py')


@AddTask
class frontendini(BaseTask):
    output_file = 'data/frontend.ini'

    dependencys = [
        buildout.dependency_FileChanged(),
        FileChanged('pymktemplates/frontend.ini.tpl'),
    ]

    def build(self):
        data = {
            'project_name': 'skysoccer',
            'inifile_with_server': True,
            'inifile_logger_root': 'DEBUG',
            'inifile_logger_module': 'DEBUG',
            'here': os.path.dirname(__file__),
        }
        mktemplate('frontend.ini.tpl', self.output_file, data)


@AddTask
class frontend(BaseTask):
    dependencys = [
        frontendini.dependency_FileExists(),
        AlwaysRebuild(),
    ]

    def build(self):
        run_cmd('./bin/pserve --reload %s' % (frontendini.output_file), True)
