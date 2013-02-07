# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'pyramid',
    'jinja2',
    'waitress',
    'pymongo',
    'webtest',
]

dependency_links = [
]

if __name__ == '__main__':
    setup(name='SkySoccer',
          version='0.1.1',
          author=['Dawid Fajkowski', ],
          author_email=['dawidfajkowski@gmail.com', ],
          packages=find_packages(),
          install_requires=install_requires,
          dependency_links=dependency_links,
          test_suite='skysoccer.test.get_all_test_suite',
          entry_points="""\
            [paste.app_factory]
                main = skysoccer.app:main
            [console_scripts]
                tests = skysoccer.test:run
""",
          )
