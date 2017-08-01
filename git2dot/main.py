#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""git2dot command line
"""

import sys

from fspath import CLI
from fspath import FSPath
import git
from .git2dot import GitDigraph

def find_git_root(repo):
    """find '.git' folder of folder 'repo'"""
    while repo.DIRNAME != repo:
        if (repo / ".git").ISDIR:
            break
        else:
            repo = repo.DIRNAME
    if not (repo / ".git").ISDIR:
        repo = None
    return repo

def _cli_giant(cli):
    u"""draw graph for all git refs & objs.

    Generate DOT revision graph from the entire repository.

    .. warning::

       Depending on the repository, the graph may be gigantic

    """
    repo = find_git_root(cli.repo)
    if repo is None:
        raise cli.Error(42, '%s is not a git repository' % cli.repo)

    cli.OUT.write('using: %s\n' % repo)
    repo = git.Repo(repo)
    dot  = GitDigraph(comment     = cli.repo.BASENAME
                      , format    = cli.out.SUFFIX[1:]
                      , engine    = 'dot'
                      , encoding  = 'utf-8'
                      )
    for ref in repo.refs:
        dot.addGitRef(ref, traverse=True)

    dot.render(
        filename  = cli.out.BASENAME.SKIPSUFFIX
        , directory = cli.out.DIRNAME
    )

    if cli.show:
        cli.out.startFile()

def main():
    """main command-line"""

    cli = CLI(description=main.__doc__)
    giant = cli.addCMDParser(_cli_giant, cmdName='giant')
    giant.add_argument(
        "-s", "--show"
        , action = 'store_false'
        , help = "open graph with default application")
    giant.add_argument(
        "out"
        , type = FSPath
        , help = "file name of the output")
    giant.add_argument(
        "repo"
        , type = FSPath
        , default = FSPath('.')
        , help = "path name of the git repository")
    cli()

if __name__ == '__main__':
    sys.exit(main())
