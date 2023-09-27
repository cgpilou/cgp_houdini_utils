"""
sop viewer state library
"""

# imports third-parties
import hou

# import local
from . import _generic


# SOP VIEWER STATE OBJECTS #


class SopState(_generic.NodeState):
    """viewer state object that manipulates a sop viewer state
    """

    # ATTRIBUTES #

    NODE_CATEGORY = hou.sopNodeTypeCategory()
