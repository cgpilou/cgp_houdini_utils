"""
houdini scene management functions
"""


_PARM_TYPES = {}
_NODE_TYPES = {}


# COMMANDS #


def node(name):
    """the node object from a node name

    :param name: the name of the node
    :type name: str

    :return: the node object
    :rtype: `:class: rdo_houdini_utils.scene.Node`
    """

    # return
    return _NODE_TYPES['node'](name)


def parm(nodeName, parmName):
    """the parm object from an attribute full name

    :param nodeName: the name of node of the parm
    :type nodeName: str

    :param parmName: the name of the parm
    :type parmName: str

    :return: the parm object
    :rtype: `:class: rdo_houdini_utils.scene.Parm`
    """

    # return
    return _PARM_TYPES['parm'](nodeName, parmName)


# PRIVATE COMMANDS #


def _registerNodeTypes(nodeTypes):
    """register node types

    :param nodeTypes: node types to register
    :type nodeTypes: dict
    """

    # execute
    _NODE_TYPES.update(nodeTypes)


def _registerParmTypes(parmTypes):
    """register parm types

    :param parmTypes: parm types to register
    :type parmTypes: dict
    """

    # execute
    _PARM_TYPES.update(parmTypes)
