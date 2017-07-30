#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""git2dot command line
"""

import sys

from fspath import CLI
from fspath import FSPath
import git
from .git2dot import GitDigraph

def find_git_root(cwd='.'):
    """find .git (root of the repo)"""
    _d = FSPath(cwd).ABSPATH
    while _d.DIRNAME != _d:
        if (_d / ".git").ISDIR:
            break
        else:
            _d = _d.DIRNAME
    if _d.DIRNAME != _d:
        return _d


def _cli_giant(cli):
    u"""draw graph for all git refs & objs.

    Generate DOT revision graph from the entire repository.

    .. warning::

       Depending on the repository, the graph may be gigantic

    """
    #folder = find_git_root('/share/git-teaching')
    folder = find_git_root(FSPath.getCWD())

    print('using: %s' % folder)
    repo = git.Repo(folder)

    dot = GitDigraph(comment=folder.BASENAME)
    for ref in repo.refs:
        dot.addGitRef(ref, traverse=True)

    dot.format = sys.argv[1]
    dot.render('xxxxx')


def main():
    """main command-line"""

    cli = CLI(description=main.__doc__)
    giant = cli.addCMDParser(_cli_giant, cmdName='giant')

if __name__ == '__main__':
    sys.exit(main())
