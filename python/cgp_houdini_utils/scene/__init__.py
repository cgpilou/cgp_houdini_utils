"""
python objects and management functions to manipulate a variety of entities in a houdini scene
such as nodes, parameters, geometries, attributes...
"""


# IMPORTS #


from ._api import (attribute,
                   createNode,
                   edge,
                   geometry,
                   geometryItem,
                   point,
                   primitive,
                   networkItem,
                   node,
                   nodes,
                   parameter,
                   parameterFolder,
                   scene,
                   selectedNodes,
                   setSelectedNodes)

from ._type import (_registerAttributesTypes,
                    _registerGeometryItemTypes,
                    _registerMiscTypes,
                    _registerItemTypes,
                    _registerNodeCategories,
                    _registerNodeTypes,
                    _registerParameterTypes)

from ._attributes._generic import Attribute
from ._attributes._array import (ArrayAttribute,
                                 DictArrayAttribute,
                                 FloatArrayAttribute,
                                 IntArrayAttribute,
                                 StringArrayAttribute)
from ._attributes._misc import (DictAttribute,
                                StringAttribute)
from ._attributes._numeric import (FloatAttribute,
                                   IntAttribute)

from ._geometryItems._edge import Edge
from ._geometryItems._geometry import Geometry
from ._geometryItems._point import Point
from ._geometryItems._primitive import Primitive
from ._geometryItems._vertex import Vertex

from ._misc._scene import Scene

from ._networkItems._networkItem import (Connection,
                                         NetworkBox,
                                         NetworkDot,
                                         NetworkItem,
                                         StickyNote,
                                         SubNetworkIndirectInput)
from ._networkItems._node import Node
from ._networkItems._chop import (ChopNode,
                                  ChopNetwork)
from ._networkItems._cop import (CopNode,
                                 CopNetwork)
from ._networkItems._dop import DopNode
from ._networkItems._lop import LopNode
from ._networkItems._misc import (DirectorNode,
                                  DriverNode,
                                  ManagerNode,
                                  ObjNode)
from ._networkItems._shop import ShopNode
from ._networkItems._sop import SopNode
from ._networkItems._sop import SubNetwork
from ._networkItems._sop import SwitchNode
from ._networkItems._top import (TopNode,
                                 TopNetwork)
from ._networkItems._vop import (VopNode,
                                 VopNetwork)

from ._parameters._generic import Parameter
from ._parameters._folder import ParameterFolder
from ._parameters._specific import (FloatParameter,
                                    IntParameter,
                                    MenuParameter,
                                    StringParameter,
                                    ToggleParameter)


# COLLECT TYPES #


__attributeTypes = {cls._TYPE: cls
                    for cls in [Attribute,
                                ArrayAttribute,
                                DictAttribute,
                                DictArrayAttribute,
                                FloatAttribute,
                                FloatArrayAttribute,
                                IntAttribute,
                                IntArrayAttribute,
                                StringAttribute,
                                StringArrayAttribute]}

__geometryItemTypes = {cls._TYPE: cls
                       for cls in [Edge,
                                   Geometry,
                                   Point,
                                   Primitive,
                                   Vertex]}

__miscTypes = {cls._TYPE: cls
               for cls in [Scene]}

__networkItemTypes = {cls._ITEM_TYPE: cls
                      for cls in [Connection,
                                  NetworkBox,
                                  NetworkDot,
                                  NetworkItem,
                                  Node,
                                  StickyNote,
                                  SubNetworkIndirectInput]}

__nodeCategories = {cls._CATEGORY: cls
                    for cls in [ChopNode,
                                ChopNetwork,
                                CopNetwork,
                                CopNode,
                                DirectorNode,
                                DopNode,
                                DriverNode,
                                LopNode,
                                ManagerNode,
                                ObjNode,
                                ShopNode,
                                SopNode,
                                TopNetwork,
                                TopNode,
                                VopNetwork,
                                VopNode]}

__nodeTypes = {cls._TYPE: cls
               for cls in [SubNetwork,
                           SwitchNode]}

__parameterTypes = {cls._TYPE: cls
                    for cls in [Parameter,
                                ParameterFolder,
                                FloatParameter,
                                IntParameter,
                                MenuParameter,
                                StringParameter,
                                ToggleParameter]}


# REGISTER TYPES #


_registerAttributesTypes(__attributeTypes)
_registerGeometryItemTypes(__geometryItemTypes)
_registerMiscTypes(__miscTypes)
_registerItemTypes(__networkItemTypes)
_registerNodeCategories(__nodeCategories)
_registerNodeTypes(__nodeTypes)
_registerParameterTypes(__parameterTypes)


# PUBLIC API #


__all__ = ['attribute',
           'createNode',
           'edge',
           'geometry',
           'geometryItem',
           'point',
           'primitive',
           'networkItem',
           'node',
           'nodes',
           'parameter',
           'parameterFolder',
           'scene',
           'selectedNodes',
           'setSelectedNodes',

           # ATTRIBUTES #

           'Attribute',
           'ArrayAttribute',
           'DictArrayAttribute',
           'FloatArrayAttribute',
           'IntArrayAttribute',
           'StringArrayAttribute',
           'DictAttribute',
           'StringAttribute',
           'FloatAttribute',
           'IntAttribute',

           # GEOMETRIES #

           'Edge',
           'Geometry',
           'Point',
           'Primitive',
           'Vertex',

           # MISC #

           'Scene',

           #  NODES / NETWORK ITEMS #

           'Connection',
           'NetworkBox',
           'NetworkDot',
           'NetworkItem',
           'StickyNote',
           'SubNetworkIndirectInput',
           'Node',
           'ChopNode',
           'ChopNetwork',
           'CopNode',
           'CopNetwork',
           'DopNode',
           'LopNode',
           'DirectorNode',
           'DriverNode',
           'ManagerNode',
           'ObjNode',
           'ShopNode',
           'SopNode',
           'SubNetwork',
           'SwitchNode',
           'TopNode',
           'TopNetwork',
           'VopNode',
           'VopNetwork',

           # PARAMETERS #

           'Parameter',
           'ParameterFolder',
           'FloatParameter',
           'IntParameter',
           'MenuParameter',
           'StringParameter',
           'ToggleParameter']
