"""
chop nodes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _node


# BASE OBJECTS #


class ChopNode(_node.Node):
    """node object that manipulates a ``Chop`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.CHOP


class ChopNetwork(_node.Node):
    """node object that manipulates a ``ChopNet`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.CHOP_NETWORK
