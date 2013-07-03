from pymk.task import Task
from pymk.dependency import FileChanged, AlwaysRebuild, FileDoesNotExists
from pymk.extra import find_files, run_cmd, touch, mktemplate
import os
import logging

logger = logging.getLogger('pymk')


class clear(Task):

    dependencys = [AlwaysRebuild()]

    def build(self):
        for filename in find_files('src', '*.pyc'):
            os.unlink(filename)
            logger.debug('Deleted: %s' % (filename,))


class bootstrap(Task):
    output_file = 'bin/buildout'

    dependencys = []

    url = 'http://svn.zope.org/*checkout*/zc.buildout/branches/1.4/bootstrap/bootstrap.py'

    def build(self):
        run_cmd(['wget ' + self.url], True)
        run_cmd(['python2 bootstrap.py'], True)


class data_dir(Task):
    output_file = 'data'

    paths = [
        ['logs', ],
    ]

    dependencys = [
        FileDoesNotExists('data/logs')
    ]

    def _generate_paths(self):
        paths = [self.output_file]
        for path_list in self.paths:
            paths.append(
                os.path.join(self.output_file, *path_list)
            )
        return paths

    def build(self):
        def create_dir_without_errors(path):
            try:
                os.mkdir(path)
            except OSError:
                pass
        #-----------------------------------------------------------------------
        paths = self._generate_paths()
        for path in paths:
            create_dir_without_errors(path)


class buildout(Task):
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


class frontendini(Task):
    output_file = 'data/frontend.ini'

    dependencys = [
        buildout.dependency_FileChanged(),
        FileChanged('pymktemplates/frontend.ini.tpl'),
    ]

    def build(self):
        here = os.path.dirname(__file__)
        log_dir = os.path.join(here, 'data', 'logs')
        data = {
            'project_name': 'skysoccer',
            'inifile_with_server': True,
            'inifile_logger_module': 'DEBUG',
            'beaker_log_file': os.path.join(log_dir, 'baker.log'),
            'all_path': os.path.join(log_dir, 'all.log'),
            'here': here,
        }
        mktemplate('frontend.ini.tpl', self.output_file, data)


class frontend(Task):
    dependencys = [
        frontendini.dependency_FileExists(),
        AlwaysRebuild(),
    ]

    def build(self):
        run_cmd('./bin/pserve --reload %s' % (frontendini.output_file), True)


class test(Task):
    dependencys = [
        frontendini.dependency_FileExists(),
        AlwaysRebuild()
    ]

    def build(self):
        run_cmd(['./bin/tests'], True)
