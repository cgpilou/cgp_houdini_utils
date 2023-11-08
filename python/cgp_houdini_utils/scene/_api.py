"""
houdini scene api
"""

# imports third-parties
import hou

# imports local
import cgp_houdini_utils.constants
from . import _type


# ATTRIBUTE COMMANDS #


def attribute(geometryItem_, attribute_):
    """get an Attribute object

    :param geometryItem_: the world item to containing the attribute
    :type geometryItem_: :class:`hou.Geometry` or :class:`hou.Point` or :class:`hou.Prim` or :class:`hou.Vertex`

    :param attribute_: the houdini attribute or its name
    :type attribute_: :class:`hou.Attrib` or str

    :return: the Attribute object
    :rtype: :class:`cgp_houdini_utils.scene.Attribute`
    """

    # get the hou.Attrib if a name has been given
    if isinstance(attribute_, str):

        # init
        name = attribute_
        geometryItemType = _type.geometryItemType(geometryItem_)

        # get the hou.Attrib based on the world item type
        if geometryItemType == cgp_houdini_utils.constants.GeometryItemType.GEOMETRY:
            attribute_ = geometryItem_.findGlobalAttrib(attribute_)
        elif geometryItemType == cgp_houdini_utils.constants.GeometryItemType.POINT:
            attribute_ = geometryItem_.geometry().findPointAttrib(attribute_)
        elif geometryItemType == cgp_houdini_utils.constants.GeometryItemType.VERTEX:
            attribute_ = geometryItem_.geometry().findVertexAttrib(attribute_)
        else:
            attribute_ = geometryItem_.geometry().findPrimAttrib(attribute_)

        # raise error if nothing found
        if not attribute:
            raise ValueError('No attribute named \'{}\' on: {}'.format(name, geometryItem_))

    # find attribute type
    attributeType = _type.attributeType(attribute_)
    attributeSize = attribute_.size()

    # return based on type
    if attributeType in _type.ATTRIBUTE_TYPES:
        return _type.ATTRIBUTE_TYPES[attributeType](geometryItem_, attribute_)

    # return array
    if attributeSize > 1:
        return _type.ATTRIBUTE_TYPES[cgp_houdini_utils.constants.AttributeType.ARRAY](geometryItem_, attribute_)

    # return generic
    return _type.ATTRIBUTE_TYPES[cgp_houdini_utils.constants.AttributeType.GENERIC](geometryItem_, attribute_)


def createAttribute(geometry_, geometryItemType, attributeType, name, defaultValue=None):
    """create an attribute

    :param geometry_: the geometry to create the attribute on
    :type geometry_: :class:`cgp_houdini_utils.scene.Geometry` or :class:`hou.Geometry`

    :param geometryItemType: the geometry item type relative to the attribute
    :type geometryItemType: :class:`cgp_houdini_utils.constants.GeometryItemType`

    :param attributeType: the attribute type
    :type attributeType: :class:`cgp_houdini_utils.constants.AttributeType`

    :param name: the attribute name
    :type name: str

    :param defaultValue: the attribute default value
    :type defaultValue: any
    """

    # get correct class
    attributeClass = _type.ATTRIBUTE_TYPES.get(attributeType, cgp_houdini_utils.constants.AttributeType.GENERIC)

    # return
    return attributeClass.create(geometry_, geometryItemType, name, defaultValue=defaultValue)


# GEOMETRY COMMANDS #


def edge(edge_):
    """get an Edge object

    :param edge_: the houdini edge object or its path
    :type edge_: str or :class:`hou.Point`

    :return: the Edge object
    :rtype: :class:`cgp_houdini_utils.scene.Edge`
    """

    # return based on hou.Edge
    if isinstance(edge_, hou.Edge):
        return _type.WORLD_ITEM_TYPES[cgp_houdini_utils.constants.GeometryItemType.EDGE](edge_)

    # return based on path
    pathData = edge_.rsplit('/', 2)
    return node(pathData[0]).geometry(int(pathData[1])).edge(pathData[2])


def geometry(geometry_):
    """get a Geometry object

    :param geometry_: the hou.Geometry object or its path
    :type geometry_: :class:`hou.Geometry`, str

    :return: the Geometry object
    :rtype: :class:`cgp_houdini_utils.scene.Geometry`
    """

    # return based on hou.Geometry
    if isinstance(geometry_, hou.Geometry):
        return _type.WORLD_ITEM_TYPES[cgp_houdini_utils.constants.GeometryItemType.GEOMETRY](geometry_)

    # return based on path
    pathData = geometry_.rsplit('/', 1)
    return node(pathData[0]).geometry(int(pathData[1]))


def geometryItem(geometryItem_, type_=None):
    """get a GeometryItem object

    :param geometryItem_: the houdini world item or its path
    :type geometryItem_: :class:`hou.Edge`,
                         :class:`hou.Geometry`,
                         :class:`hou.Point`,
                         :class:`hou.Primitive`,
                         :class:`hou.Vertex`,
                         str

    :param type_: the type of the geometry item (when a path have been given as first parameter)
    :type type_: :class:`cgp_houdini_utils.constants.GeometryItemType`

    :return: the GeometryItem object
    :rtype: :class:`cgp_houdini_utils.scene.Geometry`
    """

    # init
    type_ = type_ if isinstance(geometryItem_, str) else _type.geometryItemType(geometryItem_)

    # return edge
    if type_ == cgp_houdini_utils.constants.GeometryItemType.EDGE:
        return edge(geometryItem_)

    # return geometry
    elif type_ == cgp_houdini_utils.constants.GeometryItemType.GEOMETRY:
        return geometry(geometryItem_)

    # return point
    elif type_ == cgp_houdini_utils.constants.GeometryItemType.POINT:
        return point(geometryItem_)

    # return primitive
    elif type_ in cgp_houdini_utils.constants.GeometryItemType.PRIMITIVES:
        return primitive(geometryItem_)

    # return vertex
    elif type_ == cgp_houdini_utils.constants.GeometryItemType.VERTEX:
        return vertex(geometryItem_)

    # error
    else:
        ValueError('Unknown geometry type: {}'.format(type_))


def point(point_):
    """get a Point object

    :param point_: the houdini point object or its path
    :type point_: str or :class:`hou.Point`

    :return: the Point object
    :rtype: :class:`cgp_houdini_utils.scene.Point`
    """

    # return based on hou.Point
    if isinstance(point_, hou.Point):
        return _type.WORLD_ITEM_TYPES[cgp_houdini_utils.constants.GeometryItemType.POINT](point_)

    # return based on path
    pathData = point_.rsplit('/', 2)
    return node(pathData[0]).geometry(int(pathData[1])).point(int(pathData[2]))


def primitive(primitive_):
    """get a Primitive object

    :param primitive_: the houdini primitive object or its path
    :type primitive_: str or :class:`hou.Point`

    :return: the Primitive object
    :rtype: :class:`cgp_houdini_utils.scene.Primitive`
    """

    # return based on hou.Prim
    if isinstance(primitive_, hou.Prim):
        primitiveType = str(primitive_.type()).rsplit('.', 1)[-1]
        if primitiveType in _type.WORLD_ITEM_TYPES:
            return _type.WORLD_ITEM_TYPES[primitiveType](primitive_)
        return _type.WORLD_ITEM_TYPES[cgp_houdini_utils.constants.GeometryItemType.PRIMITIVE](primitive_)

    # return based on path
    pathData = primitive_.rsplit('/', 2)
    return node(pathData[0]).geometry(int(pathData[1])).primitive(int(pathData[2]))


def vertex(vertex_):
    """get a Vertex object

    :param vertex_: the houdini vertex object or its path
    :type vertex_: str or :class:`hou.Vertex`

    :return: the Vertex object
    :rtype: :class:`cgp_houdini_utils.scene.Vertex`
    """

    # return based on hou.Vertex
    if isinstance(vertex_, hou.Vertex):
        return _type.WORLD_ITEM_TYPES[cgp_houdini_utils.constants.GeometryItemType.VERTEX](vertex_)

    # return based on path
    pathData = vertex_.rsplit('/', 2)
    return node(pathData[0]).geometry(int(pathData[1])).vertex(pathData[2])


# NETWORK ITEMS COMMANDS #


def createNode(nodeType, parent=None, name=None, isUniqueName=False):
    """create a new node

    :param nodeType: the type of the node to create
    :type nodeType: :class:`cgp_houdini_utils.constants.`

    :param parent: the parent node of the new node
    :type parent: :class:`hou.Node` or str

    :param name: the name of the new node
    :type name: str

    :param isUniqueName: ``True`` : the name will be suffixed by a number if it is already in use
                         ``False`` : the name will be set as is
    :type isUniqueName: bool

    :return: the new node
    :rtype: :class:`cgp_houdini_utils.scene.Node`
    """

    # for implemented types execute create command
    if nodeType in _type.NODE_TYPES:
        return _type.NODE_TYPES[nodeType].create(name=name, parent=parent, isUniqueName=isUniqueName)

    # init
    parent = node(parent) if parent else (node(hou.pwd()).parent() or hou.node('/'))

    # return
    return parent.createChild(nodeType, name=name, isUniqueName=isUniqueName)


def networkItem(networkItem_):
    """get the NetworkItem object

    :param networkItem_: the network item to instantiate or its path
    :type networkItem_: str or :class:`hou.NetworkMovableItem`

    :return: the NetworkItem object
    :rtype: :class:`cgp_houdini_utils.scene.NetworkItem`
    """

    # init
    networkItem_ = networkItem_ if isinstance(networkItem_, hou.NetworkMovableItem) else hou.item(networkItem_)

    # error
    if not networkItem_:
        raise ValueError('The network item does not exist: {}'.format(networkItem_))

    # return a node
    if isinstance(networkItem_, hou.Node):
        return node(networkItem_)

    # return based on type
    itemType = _type.networkItemType(networkItem_)
    if itemType and itemType in _type.NETWORK_ITEM_TYPES:
        return _type.NETWORK_ITEM_TYPES[itemType](networkItem_)

    # return generic
    return _type.NETWORK_ITEM_TYPES[cgp_houdini_utils.constants.NetworkItemType.GENERIC](networkItem_)


def node(node_):
    """get a Node object

    :param node_: the houdini node object or its path
    :type node_: str or :class:`hou.Node`

    :return: the Node object
    :rtype: :class:`cgp_houdini_utils.scene.Node`,
            :class:`cgp_houdini_utils.scene.SopNode`
    """

    # init
    node_ = node_ if isinstance(node_, hou.Node) else hou.node(node_)

    # error
    if not node_:
        raise ValueError('The node does not exist: {}'.format(node_))

    # return based on type
    nodeType = _type.nodeType(node_)
    if nodeType in _type.NODE_TYPES:
        return _type.NODE_TYPES[nodeType](node_)

    # return based on category
    nodeCategory = _type.nodeCategory(node_)
    if nodeCategory in _type.NODE_CATEGORIES:
        return _type.NODE_CATEGORIES[nodeCategory](node_)

    # return generic
    return _type.NETWORK_ITEM_TYPES[cgp_houdini_utils.constants.NetworkItemType.NODE](node_)


def nodes(parent=None, pattern=None, nodeTypes=None, nodeTypesIncluded=True):
    """get nodes in the scene

    :param parent: parent node to search the nodes under
    :type parent: str or :class:`hou.Node`

    :param pattern: name pattern of the nodes to get - ex : '*_suffix'
    :type pattern: str

    :param nodeTypes: the types of the nodes to get or exclude
    :type nodeTypes: tuple[:class:`hou.NodeType`]

    :param nodeTypesIncluded: ``True`` : only specified node types are returned -
                              ``False`` : specified node types are excluded from the return
    :type nodeTypesIncluded: bool

    :return: the nodes
    :rtype: tuple[:class:`cgp_houdini_utils.Node`]
    """

    # init
    parent = parent or '/'

    # return
    return node(parent).children(pattern=pattern,
                                 nodeTypes=nodeTypes,
                                 nodeTypesIncluded=nodeTypesIncluded,
                                 isRecursive=True)


def selectedNodes():
    """get the selected nodes

    :return: the selected nodes
    :rtype: tuple[:class:`cgp_houdini_utils.scene.Node`]
    """

    # return
    return tuple(node(item) for item in hou.selectedNodes(True))


def setSelectedNodes(nodes_=None):
    """set the selected nodes

    :param nodes_: the nodes to select
    :type nodes_: tuple[:class:`cgp_houdini_utils.scene.Node`]
    """

    # init
    nodes_ = nodes_ or tuple()

    # unselect undesired
    for node_ in selectedNodes():
        if node_ not in nodes_:
            node_.setSelected(False)

    # select desired
    for node_ in nodes_:
        node_.setSelected(True)


# PARAMETER COMMANDS #


def parameter(parameter_):
    """get a Parameter object

    :param parameter_: the houdini parameter or its path
    :type parameter_: :class:`hou.Parm` or str

    :return: the Parameter object
    :rtype: :class:`cgp_houdini_utils.scene.Parameter`
    """

    # init
    parameter_ = parameter_ if isinstance(parameter_, hou.Parm) else hou.parm(parameter_)

    # error
    if not parameter_:
        raise ValueError('The parameter does not exist: {}'.format(parameter_))

    # return based on type
    parameterType = _type.parameterType(parameter_)
    if parameterType in _type.PARAMETERS_TYPES:
        return _type.PARAMETERS_TYPES[parameterType](parameter_)

    # return generic
    return _type.PARAMETERS_TYPES[cgp_houdini_utils.constants.ParameterType.GENERIC](parameter_)


def parameterFolder(node_, index):
    """get a ParameterFolder object

    :param node_: the houdini node or its path
    :type node_: :class:`hou.Node` or str

    :param index: the index of the folder to get
    :type index: int

    :return: the ParameterFolder object
    :rtype: :class:`cgp_houdini_utils.scene.ParameterFolder`
    """

    # init
    currentIndex = -1

    # parse templates on node
    for template in node_.parmTemplateGroup().entries():
        templateType = cgp_houdini_utils.scene._type.parameterTemplateType(template)
        if templateType == cgp_houdini_utils.constants.ParameterType.FOLDER:
            currentIndex += 1

            # return
            if currentIndex == index:
                type_ = cgp_houdini_utils.constants.ParameterType.PARAMETER_FOLDER
                return _type.PARAMETERS_TYPES[type_](node_, index)

    # error
    raise ValueError('No parameter folder at index {} on node: {}'.format(index, node_))


# MISC COMMANDS #


def scene():
    """get the current scene

    :return: the current scene
    :rtype: :class:`cgp_houdini_utils.scene.Scene`
    """

    # return
    return _type.MISC_TYPES[cgp_houdini_utils.constants.MiscType.SCENE]()
