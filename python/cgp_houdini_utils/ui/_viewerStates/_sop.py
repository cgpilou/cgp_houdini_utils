"""
sop viewer state library
"""

# imports third-parties
import hou

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene
from . import _generic


# SOP VIEWER STATE OBJECTS #


class SopState(_generic.NodeState):
    """viewer state object that manipulates a sop viewer state
    """

    # ATTRIBUTES #

    NODE_CATEGORY = hou.sopNodeTypeCategory()


class StrokeState(SopState):
    """viewer state object that manipulates a stroke viewer state
    """

    # ATTRIBUTES #

    BUILT_IN_STATE_NAME = cgp_houdini_utils.constants.BuiltInState.STROKE
    LABEL = 'RDO RIG Stroke'
    NAME = 'rdo_rig_stroke'


class AttributePaintState(StrokeState):
    """viewer state object that manipulates an attribute paint viewer state
    """

    # ATTRIBUTES #

    BUILT_IN_STATE_NAME = cgp_houdini_utils.constants.BuiltInState.ATTRIBUTE_PAINT
    ICON = cgp_houdini_utils.constants.BuiltInIcon.ATTRIBUTE_PAINT
    LABEL = 'RDO RIG Attribute Paint'
    NAME = 'rdo_rig_attribute_paint'
