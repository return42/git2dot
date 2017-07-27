#!/usr/bin/env python
# -*- coding: utf-8; mode: python -*-

import sys
import os
import platform
from setuptools import setup, find_packages

_dir = os.path.abspath(os.path.dirname(__file__))

sys.path.append(_dir)

import git2dot

install_requires = [
    'six'
    , 'graphviz'
    , 'gitpython'
    , 'fspath'
]

setup(
    name               = 'git2dot'
    , version          = git2dot.__version__
    , description      = git2dot.__description__
    , long_description = git2dot.__doc__
    , url              = git2dot.__url__
    , author           = 'Markus Heiser'
    , author_email     = 'markus.heiser@darmarIT.de'
    , license          = git2dot.__license__
    , keywords         = 'git dot graphvis'
    , packages         = find_packages(exclude=['docs', 'tests'])
    , install_requires = install_requires
    , entry_points     = {
        'console_scripts': [
            'git2dot = git2dot.main:main'
        ]}
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    , classifiers = [
        'Development Status :: 5 - Production/Stable'
        , 'Intended Audience :: Developers'
        , 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
        , 'Operating System :: OS Independent'
        , 'Programming Language :: Python'
        , 'Programming Language :: Python :: 2'
        , 'Programming Language :: Python :: 3'
        , 'Topic :: Utilities'
        , 'Topic :: Software Development :: Libraries'
        , 'Topic :: System :: Filesystems' ]
)
