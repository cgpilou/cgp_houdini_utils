"""
cop nodes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _node


# BASE OBJECTS #


class CopNode(_node.Node):
    """node object that manipulates a ``Cop2`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.COP


class CopNetwork(_node.Node):
    """node object that manipulates a ``CopNet`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.COP_NETWORK
