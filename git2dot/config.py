# -*- coding: utf-8; mode: python -*-

class Container(dict):
    @property
    def __dict__(self):
        return self
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, val):
        self[attr] = val

BASE_STYLE = Container(

    LABEL = ''

    # http://graphviz.org/doc/info/attrs.html#k:rankdir
    , RANKDIR = 'BT'

    # http://graphviz.org/doc/info/attrs.html#k:arrowType
    , ARROWHEAD = 'normal'

    # http://graphviz.org/doc/info/attrs.html#d:fontnames
    , FONTNAME  = 'Courier'
    , FONTSIZE  = '16'
    , FONTCOLOR = '#333355'

    # http://graphviz.org/doc/info/colors.html#brewer
    , BG_COLOR     = 'white'
    , LINE_COLOR   = '#505050'
    , BORDER_COLOR = '#A0A0A0'
    , NODE_SHAPE   = 'box'
    , NODE_STYLE   = 'filled,rounded'
    , EDGE_STYLE   = 'bold'

    , COMMIT_COLOR = '#fcf594'
    , HEAD_COLOR   = '#C7FFC7'
    , BRANCH_COLOR = '#EEEEEE'
    , REF_COLOR    = '#FFFFC7'

    # http://www.graphviz.org/content/attrs#dsplines

    , SPLINE      = 'ortho'
)

def buildStyles(base_style=None):
    if base_style is None:
        base_style = BASE_STYLE
    return  Container({
        'base_style'      : base_style
        , 'graph': {
            'label'       : base_style.LABEL
            , 'bgcolor'   : base_style.BG_COLOR
            , 'rankdir'   : base_style.RANKDIR
            , 'fontname'  : base_style.FONTNAME
            , 'fontsize'  : base_style.FONTSIZE
            , 'fontcolor' : base_style.FONTCOLOR
            , 'splines'   : base_style.SPLINE
        }, 'node': {
            'fillcolor'   : base_style.COMMIT_COLOR
            , 'shape'     : base_style.NODE_SHAPE
            , 'color'     : base_style.BORDER_COLOR
            , 'style'     : base_style.NODE_STYLE
            , 'fontname'  : base_style.FONTNAME
            , 'fontsize'  : str(int(base_style.FONTSIZE) - 2)
            , 'fontcolor' : base_style.FONTCOLOR
        }, 'edge': {
            'style'       : base_style.EDGE_STYLE
            , 'dir'       : 'forward'
            , 'arrowhead' : base_style.ARROWHEAD
            , 'color'     : base_style.LINE_COLOR
            , 'fontname'  : base_style.FONTNAME
            , 'fontsize'  : str(int(base_style.FONTSIZE) - 4)
            , 'fontcolor' : base_style.FONTCOLOR
        }})

