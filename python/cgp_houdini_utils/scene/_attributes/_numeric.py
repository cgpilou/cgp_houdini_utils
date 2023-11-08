"""
numeric attributes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _generic


# NUMERIC ATTRIBUTE OBJECTS #


class FloatAttribute(_generic.Attribute):
    """attribute object that manipulates a ``float`` attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.FLOAT

    # COMMANDS #

    def value(self):
        """get the value of the FloatAttribute

        :return: the value of the FloatAttribute
        :rtype: float
        """

        # return
        return self.houGeometryItem().floatAttribValue(self.houAttrib())


class IntAttribute(_generic.Attribute):
    """attribute object that manipulates a ``int`` attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.INT

    # COMMANDS #

    def value(self):
        """get the value of the IntAttribute

        :return: the value of the IntAttribute
        :rtype: int
        """

        # return
        return self.houGeometryItem().intAttribValue(self.houAttrib())
