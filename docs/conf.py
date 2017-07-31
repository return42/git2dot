# -*- coding: utf-8 -*-
#
# Sphinx documentation build configuration file

import sys
import sphinx_rtd_theme

import git2dot

project   = 'git2dot'
copyright = git2dot.__copyright__
version   = git2dot.__version__
release   = git2dot.__version__
show_authors = True

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = ['_build', 'slides']


extensions = [
    'sphinx.ext.autodoc'
    , 'sphinx.ext.extlinks'
    #, 'sphinx.ext.autosummary'
    #, 'sphinx.ext.doctest'
    , 'sphinx.ext.todo'
    , 'sphinx.ext.coverage'
    #, 'sphinx.ext.pngmath'
    #, 'sphinx.ext.mathjax'
    , 'sphinx.ext.viewcode'
    , 'sphinx.ext.intersphinx'
]

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ["../utils/sphinx-static"]
html_context = {
    'css_files': [
        '_static/theme_overrides.css',
    ],
}
html_logo = 'darmarIT_logo_128.png'
intersphinx_mapping = {}
