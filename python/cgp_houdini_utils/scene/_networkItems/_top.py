"""
top nodes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _node


# BASE OBJECTS #


class TopNode(_node.Node):
    """node object that manipulates a ``Top`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.TOP


class TopNetwork(_node.Node):
    """node object that manipulates a ``TopNet`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.TOP_NETWORK
