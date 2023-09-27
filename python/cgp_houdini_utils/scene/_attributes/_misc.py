"""
misc attributes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _generic


# MISC ATTRIBUTE OBJECTS #


class DictAttribute(_generic.Attribute):
    """attribute object that manipulates a ``dict`` attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.DICT

    # COMMANDS #

    def value(self):
        """get the value of the DictAttribute

        :return: the value of the DictAttribute
        :rtype: dict
        """
        
        # return
        return self.houGeometryItem().dictAttribValue(self.houAttrib())


class StringAttribute(_generic.Attribute):
    """attribute object that manipulates a ``string`` attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.STRING

    # COMMANDS #

    def value(self):
        """get the value of the StringAttribute

        :return: the value of the StringAttribute
        :rtype: str
        """

        # return
        return self.houGeometryItem().stringAttribValue(self.houAttrib())
