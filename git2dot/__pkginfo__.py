# -*- coding: utf-8; mode: python -*-
# pylint: disable=invalid-name,redefined-builtin
"""
python package meta informations
"""

package      = 'git2dot'
version      = '20170730'
authors      = ['Markus Heiser', ]
emails       = ['markus.heiser@darmarIT.de', ]
copyright    = '2017 Markus Heiser'
url          = 'https://github.com/return42/git2dot'
description  = 'semantic path names and more'
license      = 'GPLv2'
keywords     = "git-log graphviz"

def get_entry_points():
    """get entry points of the python package"""
    return {
        'console_scripts': [
            'git2dot = git2dot.main:main'
        ]}

install_requires = [
    'six'
    , 'graphviz'
    , 'gitpython'
    , 'fspath'
]

# See https://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = [
    "Development Status :: 5 - Production/Stable"
    , "Intended Audience :: Developers"
    , "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    , "Operating System :: OS Independent"
    , "Programming Language :: Python"
    , "Programming Language :: Python :: 2"
    , "Programming Language :: Python :: 3"
    , "Topic :: Utilities"
    , "Topic :: Software Development :: Libraries"
    , "Topic :: System :: Filesystems" ]
