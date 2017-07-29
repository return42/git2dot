#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=bad-continuation,invalid-name

import cgi
import time
import git
from fspath import FSPath
from graphviz import Digraph


class GitFormatter(object):

    SHA_SHORT_LENGTH  = 6
    DATE_TIME_FORMAT  = '%Y-%m-%d %H:%M:%S'

    # LABELS will be evaluated in the context of self (see cls.__getitem__)
    LABELS = dict(
        commit   = r'<%(hexsha:short)s:<B>%(message:short)s</B><BR/> %(author.name)s %(committed_date)s>'
        , ref    = r'<%(path)s>'
        , head   = r'<<B>HEAD<BR/>%(name)s</B>>'
        , branch = r'<<B>branch<BR/>%(name)s</B>>')

    # NODE_ATTRS's values will be evaluated in the context of
    # self.styles.base_style (see cls.getAttrs)
    NODE_ATTRS = dict(
        commit   = {}
        , ref    = {'fillcolor': '%(REF_COLOR)s'}
        , head   = {'fillcolor': '%(HEAD_COLOR)s'}
        , branch = {'fillcolor': '%(BRANCH_COLOR)s'})

    def __init__(self, git_item, styles):
        self.git_item = git_item
        self.git      = git_item.repo
        self.styles   = styles

    @property
    def __dict__(self):
        return self

    @property
    def type(self):
        retVal = None
        if isinstance(self.git_item, git.refs.reference.Reference):
            retVal = 'ref'
            if self.git.head.object == self.git_item.object:
                retVal = 'head'
            elif self.git_item in self.git.branches:
                retVal = 'branch'
        elif isinstance(self.git_item, git.objects.base.Object):
            retVal = self.git_item.type
        return retVal

    def dumpNode(self, graph):
        graph.node(self.getID(), self.getLabel(), self.getAttrs())

    def getID(self):
        if self.type in ('ref','head', 'branch'):
            return self.git_item.path
        else:
            return self.git_item.hexsha

    def getLabel(self):
        return self.LABELS[self.type] % self

    def getAttrs(self):
        retVal = dict()
        attrs = self.NODE_ATTRS[self.type]
        for k,v in attrs.items():
            retVal[k] = v % self.styles.base_style
        return retVal

    def __getitem__(self, attr):
        attr, modifier = (attr.split(':') + [None])[:2]

        obj = self.git_item
        for name in attr.split("."):
            obj = getattr(obj, name)
            if obj is None:
                break

        retVal = obj
        if attr in ('committed_date', ):
            retVal = time.strftime(self.DATE_TIME_FORMAT, time.gmtime(retVal))
        if modifier == 'short':
            if attr in ('hexsha', ):
                retVal = retVal[:self.SHA_SHORT_LENGTH]
            elif attr in ('message', ):
                retVal = retVal.splitlines()[0]
        return cgi.escape(retVal)


    #     self.node_id        = git_obj.hexsha
    #     self.node_shape     = self.node_shape[self.git_obj.type]
    #     self.node_style     = self.node_style[self.git_obj.type]
    #     self.node_fillcolor = self.node_fillcolor[self.git_obj.type]

    # @property
    # def node_label(self):
    #     fmt = self.node_label_format[self.git_obj.type]
    #     return fmt % self

    # @property
    # def node_attrs(self):
    #     return dict(
    #         shape       = self.node_shape
    #         , style     = self.node_style
    #         , fillcolor = self.node_fillcolor
    #         )


class GitDigraph(Digraph):

    def __init__(self, *args, **kwargs):
        super(GitDigraph, self).__init__(*args, **kwargs)

        self.git_objs   = dict()
        self.git_refs   = dict()
        self.git_edges  = dict()
        self.ref_rank   = set()

        # ToDo: facilitate for customizing
        self.fmtClass   = GitFormatter
        self.styleFunc  = buildStyles

    def addGitRef(self, gitRef, traverse=False):
        """Add a git-ref node to the graph

        :param git.refs.reference.Reference gitRef: git-ref
        :param bool tarverse: if ``True`` do traverse (default: ``False``)

        The git-ref (*node*), the object (*node*) it points to and the *edge*
        will be added. If the git-ref is already added, nothing happens.  The
        node ID is the *path* (e.g. ``refs/heads/master``) of the git-ref
        (:py:meth:`GitFormatter.getID`).

        The bool argument 'traverse' can be used to control whether a traversal
        should be carried out.

        """
        if self.git_refs.get(gitRef.path, None) is None:
            self.git_refs[gitRef.path] = gitRef
            self.addGitObj(gitRef.object)
            self.addGitEdge(gitRef.object.hexsha, gitRef.path, dir='back')
            if traverse:
                for obj in gitRef.object.traverse():
                    self.addGitObj(obj)

    def addGitObj(self, gitObj):
        """Add a git-obj node.

        :param git.objects.base.Object gitObj: git-object
        :param bool tarverse: if ``True`` do traverse (default: ``False``)

        The object (*node*) and all it's edges to parents will be added.  If the
        git-obj is already added, nothing happens. The node ID is taken from the
        *hexsha* of the git-obj (:py:meth:`GitFormatter.getID`)

        """
        if self.git_objs.get(gitObj.hexsha, None) is None:
            self.git_objs[gitObj.hexsha] = gitObj
            for p in gitObj.parents:
                self.addGitEdge(p.hexsha, gitObj.hexsha)

    def addGitEdge(self, parent, child, **kwargs):
        """Add a 'parent' --> 'child' edge.

        :param str parent: label (ID) of the parent
        :param str child: label (ID) of the parent

        If the 'parent' --> 'child' edge is already added, nothing happens.

        """
        if self.git_edges.get((parent, child), None) is None:
            self.git_edges[(parent, child)] = kwargs

    def save(self, *args, **kwargs):
        self.dumpGraph()
        return super(GitDigraph, self).save(*args, **kwargs)

    def pipe(self, *args, **kwargs):
        self.dumpGraph()
        return super(GitDigraph, self).pipe(*args, **kwargs)

    def dumpGraph(self):
        styles = self.styleFunc()
        self.graph_attr.update(styles['graph'])
        self.node_attr.update(styles['node'])
        self.edge_attr.update(styles['edge'])

        for gitObj in self.git_objs.values():
            obj = self.fmtClass(gitObj, styles)
            obj.dumpNode(self)
        self.git_objs = dict()

        for gitRef in self.git_refs.values():
            ref = self.fmtClass(gitRef, styles)
            ref.dumpNode(self)
            self.ref_rank.add(ref.getID())
        self.git_refs = dict()

        # rank all refs
        self.body.append('{rank = same; "' + '"; "'.join(self.ref_rank) + '";}')
        self.ref_rank = set()

        for (parent, child), kwargs in self.git_edges.items():
            self.edge(parent, child, **kwargs)
        self.git_edges = dict()



    # def node(self, name, label=None, _attributes=None, **attrs):
    #     """Create a node.

    #     Args:
    #         name: Unique identifier for the node inside the source.
    #         label: Caption to be displayed (defaults to the node name).
    #         attrs: Any additional node attributes (must be strings).
    #     """
    #     name = self._quote(name)
    #     attr_list = self._attr_list(label, attrs, _attributes)
    #     line = self._node % (name, attr_list)
    #     self.body.append(line)

    # def edge(self, tail_name, head_name, label=None, _attributes=None, **attrs):
    #     """Create an edge between two nodes.

    #     Args:
    #         tail_name: Start node identifier.
    #         head_name: End node identifier.
    #         label: Caption to be displayed near the edge.
    #         attrs: Any additional edge attributes (must be strings).
    #     """
