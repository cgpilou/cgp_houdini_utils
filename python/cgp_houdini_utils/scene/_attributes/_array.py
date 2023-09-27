"""
array attributes library
"""

# imports local
import cgp_houdini_utils.constants
from . import _generic


# ARRAY ATTRIBUTE OBJECTS #


class ArrayAttribute(_generic.Attribute):
    """attribute object that manipulates any kind of array attribute
    """

    # ATTRIBUTES #

    _TYPE = NotImplemented
    _ELEMENT_TYPE = None

    # COMMANDS #

    def setSize(self, size):
        """set the size (number of elements) of the ArrayAttribute

        :param size: the size of the ArrayAttribute
        :type size: int
        """

        # return
        self.houAttrib().setSize(size)

    def setValue(self, value):
        """set the value of the ArrayAttribute

        :param value: the value to set to the ArrayAttribute
        :type value: tuple
        """

        # errors
        if len(value) != self.size():
            raise ValueError('Attribute "{}" value expect {} elements, '
                             '{} given'.format(self.name(), self.size(), len(value)))
        for element in value:
            if self._ELEMENT_TYPE and not isinstance(element, self._ELEMENT_TYPE):
                raise TypeError('Attribute "{}" expect value of type {}, '
                                '{} given'.format(self.name(), self._ELEMENT_TYPE.__name__, type(element).__name__))

        # set value
        super(ArrayAttribute, self).setValue(value)


class DictArrayAttribute(ArrayAttribute):
    """attribute object that manipulates a ``dict`` array attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.DICT_ARRAY
    _ELEMENT_TYPE = dict

    # COMMANDS #

    def value(self):
        """get the value of the DictArrayAttribute

        :return: the value of the DictArrayAttribute
        :rtype: tuple[dict]
        """

        # return
        return self.houGeometryItem().dictListAttribValue(self.houAttrib())


class FloatArrayAttribute(ArrayAttribute):
    """attribute object that manipulates a ``float`` array attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.FLOAT_ARRAY
    _ELEMENT_TYPE = float

    # COMMANDS #

    def value(self):
        """get the value of the FloatArrayAttribute

        :return: the value of the FloatArrayAttribute
        :rtype: tuple[float]
        """

        # return
        return self.houGeometryItem().floatListAttribValue(self.houAttrib())


class IntArrayAttribute(ArrayAttribute):
    """attribute object that manipulates a ``int`` array attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.INT_ARRAY
    _ELEMENT_TYPE = int

    # COMMANDS #

    def value(self):
        """get the value of the IntArrayAttribute

        :return: the value of the IntArrayAttribute
        :rtype: tuple[int]
        """

        # return
        return self.houGeometryItem().intListAttribValue(self.houAttrib())


class StringArrayAttribute(ArrayAttribute):
    """attribute object that manipulates a ``string`` array attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.STRING_ARRAY
    _ELEMENT_TYPE = str

    # COMMANDS #

    def value(self):
        """get the value of the StringArrayAttribute

        :return: the value of the StringArrayAttribute
        :rtype: tuple[string]
        """

        # return
        return self.houGeometryItem().stringListAttribValue(self.houAttrib())
