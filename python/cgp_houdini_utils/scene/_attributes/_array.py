"""
array attributes library
"""

# imports third parties
import hou

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene._type
from . import _generic


# ARRAY ATTRIBUTE OBJECTS #


class ArrayAttribute(_generic.Attribute):
    """attribute object that manipulates any kind of array attribute
    """

    # ATTRIBUTES #

    _ELEMENT_TYPE = None
    _HOU_TYPE = NotImplemented
    _TYPE = NotImplemented

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, geometry, geometryItemType, name, defaultValue=None):
        """create the Attribute

        :param geometry: the geometry to create the attribute on
        :type geometry: :class:`cgp_houdini_utils.scene.Geometry` or :class:`hou.Geometry`

        :param geometryItemType: the geometry item type relative to the attribute
        :type geometryItemType: :class:`cgp_houdini_utils.constants.GeometryItemType`

        :param name: the attribute name
        :type name: str

        :param defaultValue: the attribute default value
        :type defaultValue: any
        """

        # error
        if defaultValue and cls._ELEMENT_TYPE and not isinstance(defaultValue[0], cls._ELEMENT_TYPE):
            raise ValueError('Unable to create {}. '
                             'Given default value does not match attribute type.'.format(cls.__name__))

        # get global geometry
        geometry = geometry if isinstance(geometry, hou.Geometry) else geometry.houGeometryItem()

        # get houdini geometry  type
        geometryItemType = {cgp_houdini_utils.constants.GeometryItemType.GEOMETRY: hou.attribType.Global,
                            cgp_houdini_utils.constants.GeometryItemType.POINT: hou.attribType.Point,
                            cgp_houdini_utils.constants.GeometryItemType.PRIMITIVE: hou.attribType.Prim,
                            cgp_houdini_utils.constants.GeometryItemType.VERTEX: hou.attribType.Vertex
                            }[geometryItemType]

        # create the attribute
        attribute = geometry.addArrayAttrib(geometryItemType, name, cls._HOU_TYPE)

        # create our instance
        instance = cls(geometry, attribute)

        # set default value
        if defaultValue is not None:
            instance.setValue(defaultValue)

        # return
        return instance

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

        # error
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

    _ELEMENT_TYPE = dict
    _HOU_TYPE = hou.attribData.Dict
    _TYPE = cgp_houdini_utils.constants.AttributeType.DICT_ARRAY

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

    _ELEMENT_TYPE = float
    _HOU_TYPE = hou.attribData.Float
    _TYPE = cgp_houdini_utils.constants.AttributeType.FLOAT_ARRAY

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

    _ELEMENT_TYPE = int
    _HOU_TYPE = hou.attribData.Int
    _TYPE = cgp_houdini_utils.constants.AttributeType.INT_ARRAY

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

    _ELEMENT_TYPE = str
    _HOU_TYPE = hou.attribData.String
    _TYPE = cgp_houdini_utils.constants.AttributeType.STRING_ARRAY

    # COMMANDS #

    def value(self):
        """get the value of the StringArrayAttribute

        :return: the value of the StringArrayAttribute
        :rtype: tuple[string]
        """

        # return
        return self.houGeometryItem().stringListAttribValue(self.houAttrib())
