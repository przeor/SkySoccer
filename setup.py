# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires=[
    'pyramid',
    'jinja2',
]

dependency_links = [
]

if __name__ == '__main__':
    setup(name='SkySoccer',
        version='0.1.0',
        author=['Dominik "Socek" Długajczyk',],
        author_email=['msocek@gmail.com',],
        packages=find_packages(),
        install_requires=install_requires,
        dependency_links=dependency_links,
        entry_points="""\
            [paste.app_factory]
                main = skysoccer.app:main
""",
    )
