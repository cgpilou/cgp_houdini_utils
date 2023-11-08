"""
houdini scene types library
"""

# import local
import cgp_houdini_utils.constants


# GLOBALS #


ATTRIBUTE_TYPES = {}
NETWORK_ITEM_TYPES = {}
MISC_TYPES = {}
NODE_CATEGORIES = {}
NODE_TYPES = {}
PARAMETERS_TYPES = {}
WORLD_ITEM_TYPES = {}


# COMMANDS #


def attributeType(houAttrib):
    """get the type of the houdini attribute

    :param houAttrib: the houdini attribute
    :type houAttrib: :class:`hou.Attribute`

    :return: the type of the houdini attribute
    :rtype: :class:`cgp_houdini_utils.constants.AttributeType`
    """

    # init
    type_ = str(houAttrib.dataType()).rsplit('.', 1)[-1]
    type_ += cgp_houdini_utils.constants.AttributeType.ARRAY if houAttrib.size() > 1 else ''

    # return
    return type_


def geometryItemType(houGeometryItem):
    """get the type of the given houdini world item

    :param houGeometryItem: the houdini world item
    :type houGeometryItem: :class:`hou.Edge`,
                        :class:`hou.Geometry`,
                        :class:`hou.Point`,
                        :class:`hou.Primitive`,
                        :class:`hou.Vertex`,

    :return: the type of the given houdini world item
    :rtype: :class:`cgp_houdini_utils.constants.GeometryItemType`
    """

    # return for world item with attributes
    if hasattr(houGeometryItem, 'attribType'):
        return str(houGeometryItem.attribType()).rsplit('.', 1)[-1]

    # return for world item without attributes
    return houGeometryItem.__class__.__name__


def networkItemType(houNetworkItem):
    """get the type of the houdini network item

    :param houNetworkItem: the houdini network item
    :type houNetworkItem: :class:`hou.NetworkMovableItem`

    :return: the type of the houdini network item
    :rtype: :class:`cgp_houdini_utils.constants.NetworkItemType`
    """

    # return
    return str(houNetworkItem.networkItemType()).rsplit('.', 1)[-1]


def nodeCategory(houNode):
    """get the category of the houdini node

    :param houNode: the houdini node
    :type houNode: :class:`hou.Node`

    :return: the category of the houdini node
    :rtype: :class:`cgp_houdini_utils.constants.NodeCategory`
    """

    # return
    return houNode.type().category().name()


def nodeType(houNode):
    """get the type of the houdini node

    :param houNode: the houdini node
    :type houNode: :class:`hou.Node`

    :return: the type of the houdini node
    :rtype: :class:`cgp_houdini_utils.constants.NodeType`
    """

    # return
    return houNode.type().name()


def parameterType(houParm):
    """get the type of the houdini parameter

    :param houParm: the houdini parameter
    :type houParm: :class:`hou.Parameter`

    :return: the type of the houdini parameter
    :rtype: :class:`cgp_houdini_utils.constants.ParameterType`
    """

    # return
    return parameterTemplateType(houParm.parmTemplate())


def parameterTemplateType(houParmTemplate):
    """get the type of the houdini parameter

    :param houParmTemplate: the houdini parameter template
    :type houParmTemplate: :class:`hou.ParmTemplate`

    :return: the type of the houdini parameter template
    :rtype: :class:`cgp_houdini_utils.constants.ParameterType`
    """

    # return
    return str(houParmTemplate.type()).rsplit('.', 1)[-1]


# PROTECTED COMMANDS #


def _registerAttributesTypes(attributesTypes):
    """register attribute types

    :param attributesTypes: attribute types to register
    :type attributesTypes: dict
    """

    # execute
    ATTRIBUTE_TYPES.update(attributesTypes)


def _registerGeometryItemTypes(geometryItemTypes):
    """register geometry types

    :param geometryItemTypes: world item types to register
    :type geometryItemTypes: dict
    """

    # execute
    WORLD_ITEM_TYPES.update(geometryItemTypes)


def _registerItemTypes(itemTypes):
    """register item types

    :param itemTypes: item types to register
    :type itemTypes: dict
    """

    # execute
    NETWORK_ITEM_TYPES.update(itemTypes)


def _registerMiscTypes(miscTypes):
    """register misc types

    :param miscTypes: misc types to register
    :type miscTypes: dict
    """

    # execute
    MISC_TYPES.update(miscTypes)


def _registerNodeCategories(nodeCategories):
    """register node categories

    :param nodeCategories: node categories to register
    :type nodeCategories: dict
    """

    # execute
    NODE_CATEGORIES.update(nodeCategories)


def _registerNodeTypes(nodeTypes):
    """register node types

    :param nodeTypes: node types to register
    :type nodeTypes: dict
    """

    # execute
    NODE_TYPES.update(nodeTypes)


def _registerParameterTypes(parameterTypes):
    """register parameter types

    :param parameterTypes: node types to register
    :type parameterTypes: dict
    """

    # execute
    PARAMETERS_TYPES.update(parameterTypes)
