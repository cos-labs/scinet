from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys


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
    name='crowdscholar',
    version='0.01',
    url='https://github.com/hrybacki/crowd-scholar/',
    license='MIT Software License',
    author='Harry Rybacki',
    #tests_require=['pytest'],
    install_requires=['Flask>=0.10.1',
                    'Jinja2>=2.7',
                    'MarkupSafe>=0.18',
                    'Werkzeug>=0.9.1',
                    'cssselect>=0.8',
                    'itsdangerous>=0.22',
                    'lxml>=3.2.4',
                    'nameparser>=0.2.7',
                    'pymongo>=2.5.2',
                    'pyquery>=1.2.4',
                    'python-dateutil==1.5',
                    'reppy>=0.2.2',
                    'requests>=1.2.3',
                    'url>=0.1.0',
                    'wsgiref>=0.1.2',
                    'sciparse==0.1',
                    ],
    dependency_links=['git://github.com/jmcarp/sciparse#egg=sciparse-0.1'],
    cmdclass={'test': PyTest},
    author_email='hrybacki@gmail.com.com',
    description='Crowdsourcing the academic citation graph.',
    long_description='Tools for outsourcing the academic citation graph',
    #packages=['sandman'],
    #include_package_data=True,
    platforms='any',
    #test_suite='sandman.test.test_sandman',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: MIT Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    #extras_require={
    #    'testing': ['pytest'],
    #}
)
