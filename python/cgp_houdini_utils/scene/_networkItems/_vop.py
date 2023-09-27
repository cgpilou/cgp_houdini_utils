"""
vop nodes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _node


# BASE OBJECTS #


class VopNode(_node.Node):
    """node object that manipulates a ``Vop`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.VOP


class VopNetwork(_node.Node):
    """node object that manipulates a ``VopNet`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.VOP_NETWORK
