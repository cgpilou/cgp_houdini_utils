"""
dop nodes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _node


# BASE OBJECTS #


class DopNode(_node.Node):
    """node object that manipulates a ``Dop`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.DOP
