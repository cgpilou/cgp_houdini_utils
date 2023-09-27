"""
generic attributes library
"""

# imports third parties
import hou

# imports rodeo
import cgp_generic_utils.python

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene._type
import cgp_houdini_utils.scene._api


# GENERIC ATTRIBUTE OBJECTS #


class Attribute(cgp_generic_utils.python.BaseObject):
    """attribute object that manipulates any kind of attribute
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.AttributeType.GENERIC

    # INIT #

    def __init__(self, geometryItem, attribute):
        """initialization of the Attribute

        :param geometryItem: the world item containing this object
        :type geometryItem: :class:`hou.Geometry` or :class:`hou.Point` or :class:`hou.Prim` or :class:`hou.Vertex`

        :param attribute: the houdini attribute
        :type attribute: :class:`hou.Attrib`
        """

        # init
        self._houGeometryItem = geometryItem
        self._houAttrib = attribute

    def __repr__(self):
        """get the representation of the Attribute

        :return: the representation of the Attribute
        :rtype: str
        """

        # return
        return self._representationTemplate().format(geometryItem=self.houGeometryItem(), attribute=self.houAttrib())

    # COMMANDS #

    def defaultValue(self):
        """get the default value of the Attribute

        :return: the default value of the Attribute
        :rtype: any
        """

        # return
        return self.houAttrib().defaultValue()

    def delete(self):
        """delete the Attribute (remove it from the geometry)
        """

        # execute
        self.houAttrib().destroy()
        self._houAttrib = None
        self._houGeometryItem = None

    def houAttrib(self):
        """get the hou.Attrib object of the Attribute

        :return: the hou.Attrib object of the Attribute
        :rtype: :class:`hou.Attrib`
        """

        # return
        return self._houAttrib

    def houGeometryItem(self):
        """get the hou world item object of the Attribute

        :return: the hou world item object of the Attribute
        :rtype: :class:`hou.Geometry`, :class:`hou.Point`, :class:`hou.Prim`, :class:`hou.Vertex`
        """

        # return
        return self._houGeometryItem

    def isPrivate(self):
        """check the privacy status of the Attribute

        :return: ``True`` : the Attribute is private - ``False`` : the Attribute is public
        :rtype: bool
        """

        # init
        houGeometryItem = self.houGeometryItem()

        # collect public attributes attributes
        if isinstance(houGeometryItem, hou.Geometry):
            publicAttributes = houGeometryItem.globalAttribs(False)
        elif isinstance(houGeometryItem, hou.Point):
            publicAttributes = houGeometryItem.geometryItem().pointAttribs(False)
        elif isinstance(houGeometryItem, hou.Vertex):
            publicAttributes = houGeometryItem.geometryItem().vertexAttribs(False)
        else:
            publicAttributes = houGeometryItem.geometryItem().primAttribs(False)

        # return
        return self.houAttrib() not in publicAttributes

    def name(self):
        """get the name of the Attribute

        :return: the name of the Attribute
        :rtype: str
        """

        # return
        return self.houAttrib().name()

    def setName(self, name):
        """set the name of the Attribute

        :param name: the name
        :type name: str
        """

        # init
        houGeometryItem = self.houGeometryItem()

        # global attribute rename
        if isinstance(houGeometryItem, hou.Geometry):
            houGeometryItem.renameGlobalAttrib(self.name(), name)

        # point attributes rename
        elif isinstance(houGeometryItem, hou.Point):
            houGeometryItem.geometryItem().renamePointAttrib(self.name(), name)

        # vertex attributes rename
        elif isinstance(houGeometryItem, hou.Vertex):
            houGeometryItem.geometryItem().renameVertexAttrib(self.name(), name)

        # primitive attributes rename
        else:
            houGeometryItem.geometryItem().renamePrimAttrib(self.name(), name)

    def setValue(self, value):
        """set the value of the Attribute

        :param value: the value to set to the Attribute
        :type value: any
        """

        # init
        houGeometryItem = self.houGeometryItem()

        # execute
        if isinstance(houGeometryItem, hou.Geometry):
            houGeometryItem.setGlobalAttribValue(self.houAttrib(), value)
        else:
            houGeometryItem.setAttribValue(self.houAttrib(), value)

    def size(self):
        """get the size (number of elements) of the Attribute

        :return: the size of the Attribute
        :rtype: int
        """

        # return
        return self.houAttrib().size()

    def type_(self):
        """get the type of the Attribute

        :return: the type of the Attribute
        :rtype: str
        """

        # return
        return cgp_houdini_utils.scene._type.attributeType(self.houAttrib())

    def value(self):
        """get the value of the Attribute

        :return: the value of the Attribute
        :rtype: any
        """

        # return
        return self.houGeometryItem().attribValue(self.houAttrib())
