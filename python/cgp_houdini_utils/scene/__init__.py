"""
python objects and management functions to manipulate a variety of entities in a houdini scene
such as nodes, parms ...
"""


# imports local
from ._api import node, parm, _registerNodeTypes, _registerParmTypes
from ._nodes._generic import Node
from ._parms._generic import Parm
from ._misc._misc import Scene


__nodeTypes = {'node': Node}
__parmTypes = {'parm': Parm}

_registerNodeTypes(__nodeTypes)
_registerParmTypes(__parmTypes)


__all__ = ['node',
           'parm',
           'Node',
           'Parm',
           'Scene']
