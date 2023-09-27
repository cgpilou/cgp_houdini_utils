"""
generic geometry item library
"""

# imports third parties
import hou

# imports rodeo
import cgp_generic_utils.python

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene._type
import cgp_houdini_utils.scene._api


# GENERIC WORLD ITEM OBJECTS #


class GeometryItem(cgp_generic_utils.python.BaseObject):
    """geometry item object that manipulates any kind of geometry item
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.GeometryItemType.GENERIC

    # INIT #

    def __init__(self, geometryItem):
        """initialization of the GeometryItem

        :param geometryItem: the houdini geometry item
        :type geometryItem: :class:`hou.Edge`,
                        :class:`hou.Geometry`,
                        :class:`hou.Point`,
                        :class:`hou.Prim`,
                        :class:`hou.Vertex`
        """

        # init
        self._houGeometryItem = geometryItem

    def __repr__(self):
        """get the representation of the GeometryItem

        :return: the representation of the GeometryItem
        :rtype: str
        """

        # return
        return self._representationTemplate().format(geometryItem=self.houGeometryItem())

    # COMMANDS #

    def houGeometryItem(self):
        """get the hou geometry item object of the GeometryItem

        :return: the hou geometry item object of the GeometryItem
        :rtype: :class:`hou.Edge`,
                :class:`hou.Geometry`,
                :class:`hou.Point`,
                :class:`hou.Prim`,
                :class:`hou.Vertex`
        """

        # return
        return self._houGeometryItem

    def index(self):
        """get the index of the GeometryItem

        :return: the index of the GeometryItem
        :rtype: int or str
        """

        # abstract
        raise NotImplementedError

    def path(self):
        """get the path of the GeometryItem

        :return: the path of the GeometryItem
        :rtype: str
        """

        # abstract
        raise NotImplementedError

    def type_(self):
        """get the type of the GeometryItem

        :return: the type of the GeometryItem
        :rtype: str
        """

        # return
        return cgp_houdini_utils.scene._type.geometryItemType(self.houGeometryItem())


class EditableGeometryItem(GeometryItem):
    """geometry item object that manipulates any kind of editable (aka with attributes) geometry item
    """

    # ATTRIBUTES #

    _GET_ATTRIBUTE_COMMAND = NotImplemented
    _LIST_ATTRIBUTES_COMMAND = NotImplemented
    _TYPE = cgp_houdini_utils.constants.GeometryItemType.EDITABLE

    # COMMANDS #

    def attribute(self, name):
        """get an attribute of the EditableGeometryItem

        :param name: the attribute name
        :type name: str

        :return: the attribute of the EditableGeometryItem
        :rtype: :class:`cgp_houdini_utils.scene.Attribute`
        """

        # get the geometry
        houGeometryItem = self.houGeometryItem()
        geometry = houGeometryItem if isinstance(houGeometryItem, hou.Geometry) else houGeometryItem.geometry()

        # get the attribute
        attribute = getattr(geometry, self._GET_ATTRIBUTE_COMMAND)(name)

        # return
        return cgp_houdini_utils.scene._api.attribute(houGeometryItem, attribute)

    def attributes(self):
        """get the attributes of the EditableGeometryItem

        :return: the attributes of the EditableGeometryItem
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Attribute`]
        """

        # get the geometry
        houGeometryItem = self.houGeometryItem()
        geometry = houGeometryItem if isinstance(houGeometryItem, hou.Geometry) else houGeometryItem.geometry()

        # get the attribute
        attributes = getattr(geometry, self._LIST_ATTRIBUTES_COMMAND)(True)

        # return
        return tuple(cgp_houdini_utils.scene._api.attribute(houGeometryItem, attribute) for attribute in attributes)

    def edge(self, index):
        """get an edge of the EditableGeometryItem

        :param index: the edge index
        :type index: int

        :return: the edge of the EditableGeometryItem
        :rtype: :class:`cgp_houdini_utils.scene.Edge`
        """

        # return based on index
        for edge in self.edges():
            if edge.index() == index:
                return edge

        # error
        raise ValueError('Unable to get the edge of {} with index: {}'.format(self, index))

    def edges(self):
        """get the edges of the EditableGeometryItem

        :return: the edges of the EditableGeometryItem
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Edge`]
        """

        # abstract
        raise NotImplementedError

    def hasAttribute(self, name):
        """check if an attribute exists on the GeometryComponent

        :param name: the attribute name
        :type name: str

        :return: ``True`` : the attribute exists - ``False`` : the attribute does not exist
        :rtype: bool
        """

        # get the geometry
        houGeometryItem = self.houGeometryItem()
        geometry = houGeometryItem if isinstance(houGeometryItem, hou.Geometry) else houGeometryItem.geometry()

        # get the attribute
        attribute = getattr(geometry, self._GET_ATTRIBUTE_COMMAND)(name)

        # return
        return bool(attribute)

    def isReadOnly(self):
        """check the read-only status of the EditableGeometryItem

        :return: ``True`` : the GeometryComponent is read-only - ``False`` : the GeometryComponent is not read-only
        :rtype: bool
        """

        # init
        houGeometryItem = self.houGeometryItem()
        geometry = houGeometryItem if isinstance(houGeometryItem, hou.Geometry) else houGeometryItem.geometry()

        # return
        return geometry.isReadOnly()
