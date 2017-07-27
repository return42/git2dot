#!/usr/bin/env python
# -*- coding: utf-8 -*-


def find_git_root(cwd='.'):
    d = FSPath(cwd).ABSPATH
    while d.DIRNAME != d:
        if (d / ".git").ISDIR:
            break
        else:
            d = d.DIRNAME
    if d.DIRNAME != d:
        return d

def main():
    import sys
    #folder = find_git_root('/share/git-teaching')
    folder = find_git_root(sys.argv[2])
    print('using: %s' % folder)
    repo = git.Repo(folder)

    dot = GitDigraph(comment=folder.BASENAME)
    for ref in repo.refs:
        dot.addGitRef(ref, traverse=True)

    dot.format = sys.argv[1]
    dot.render('xxxxx')

main()
