from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import game_of_life

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='game_of_life',
    version=sandman.__version__,
    url='http://github.com/haycpong/game_of_life/',
    license='Apache Software License',
    author='Jeff Knupp',
    tests_require=['pytest'],
    install_requires=['numpy==1.22.3',
                    'pygame==2.1.2',
                    ],
    cmdclass={'test': PyTest},
    author_email='haycpong@gmail.com',
    description='Conway''s Game of Life',
    long_description=long_description,
    packages=['game_of_life'],
    include_package_data=True,
    platforms='any',
    test_suite='game_of_life.test.test_game_of_life',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1.0.0',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
