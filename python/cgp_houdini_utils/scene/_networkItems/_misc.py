"""
misc nodes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _node


# MISC NODE OBJECTS #


class DirectorNode(_node.Node):
    """node object that manipulates a ``Director`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.DIRECTOR


class DriverNode(_node.Node):
    """node object that manipulates a ``Driver`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.DRIVER


class ManagerNode(_node.Node):
    """node object that manipulates a ``Manager`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.MANAGER


class ObjNode(_node.Node):
    """node object that manipulates a ``Obj`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.OBJ
