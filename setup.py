#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests import shut_test  # noqa


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

setup(
    name='shut',
    version='0.1.0',
    description='shut (SHape Unix Time) is a tool for converting Unix time to something readable with minimal effort.',
    long_description=readme + '\n\n' + history,
    author='Andrew Duberstein',
    author_email='ajduberstein@gmail.com',
    url='https://github.com/ajduberstein/shut',
    packages=[
        'shut',
        'tests'
    ],
    package_dir={'shut': 'shut'},
    include_package_data=True,
    license='BSD',
    zip_safe=False,
    keywords='shut',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock']
)
