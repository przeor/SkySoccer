import logging
import os
import shutil
import mkfile
from mkfile import data_dir
from pymk.dependency import AlwaysRebuild, FileChanged
from pymk.extra import run_cmd, touch
from pymk.task import Task
from pymk.extra.template import mktemplate
from pymk.error import CommandError


logger = logging.getLogger('pymk')


class BaseSymlink(Task):
    dependencys = []
    hide_graph = True
    hide = True

    def build(self):
        def create_dir_without_errors(path):
            try:
                if os.path.islink(path):
                    path = os.path.realpath(path)
                os.mkdir(path)
            except OSError:
                pass

        source = '../%s' % (self.output_file,)
        try:
            create_dir_without_errors(source)
            os.symlink(source, self.output_file)
        except OSError:
            pass


class DataSymlink(BaseSymlink):
    output_file = 'data'


class EggsSymlink(BaseSymlink):
    output_file = 'eggs'


class DEggsSymlink(BaseSymlink):
    output_file = 'develop-eggs'


class BinSymlink(BaseSymlink):
    output_file = 'bin'


class PartsSymlink(BaseSymlink):
    output_file = 'parts'


class docbuildSymlink(BaseSymlink):
    output_file = 'docbuild'


class supervision(Task):
    help = u'Run supervisord'

    output_file = 'data/supervisor_skysoccer.ini'

    dependencys = [
        data_dir.dependency_FileExists(),
        FileChanged('pymktemplates/supervisor.conf.jinja2'),
    ]

    def build(self):
        data = {
            'project_path': os.path.dirname(mkfile.__file__),
        }
        data['data_path'] = os.path.join(data['project_path'], 'data')
        data['supervisor_path'] = os.path.join(data['data_path'], 'supervisor')
        data['output_file'] = os.path.join(data['project_path'], self.output_file)
        try:
            os.mkdir(data['supervisor_path'])
        except OSError:
            pass

        mktemplate('supervisor.conf.jinja2', self.output_file, data)
        try:
            run_cmd('supervisorctl -c %(output_file)s reread' % data, True)
        except CommandError:
            logger.warning('WARNING: Supervisord not yet started !!! Starting...')
            run_cmd('supervisord -c %(output_file)s' % data)


class sctl(Task):
    help = u'Run supervisorctl'

    dependencys = [
        supervision.dependency_FileExists(),
        AlwaysRebuild(),
    ]

    def build(self):
        try:
            run_cmd('supervisorctl -c %s avail' % supervision.output_file)
        except CommandError:
            logger.warning('WARNING: Supervisord not yet started !!! Starting...')
            run_cmd('supervisord -c %s' % (supervision.output_file))
        run_cmd('supervisorctl -c %s' % (supervision.output_file,), True)


class before_install(Task):
    hide = True
    output_file = 'data/production.flag'

    dependencys = [
        DataSymlink.dependency_FileExists(),
        EggsSymlink.dependency_FileExists(),
        DEggsSymlink.dependency_FileExists(),
        BinSymlink.dependency_FileExists(),
        PartsSymlink.dependency_FileExists(),
        docbuildSymlink.dependency_FileExists(),
    ]

    def build(self):
        def copy_local_settings():
            logger.info('Copying local settings...')
            sourc_path = '../local/settings.py'
            destination_path = './skysoccer/settings/local.py'
            shutil.copyfile(sourc_path, destination_path)
        #-----------------------------------------------------------------------
        copy_local_settings()
        touch(self.output_file)


class install(Task):
    help = u'Install on production envoritment.'

    dependencys = [
        before_install.dependency_FileExists(),
        supervision.dependency_FileExists(),
        AlwaysRebuild(),
    ]

    def build(self):
        run_cmd('supervisorctl -c %s restart skysoccer' % (supervision.output_file,), True)
