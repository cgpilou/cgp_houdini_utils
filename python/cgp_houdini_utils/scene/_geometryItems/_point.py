"""
point library
"""

# imports third parties
import hou

# imports local
import cgp_houdini_utils.constants
from . import _generic


# POINT OBJECTS #


class Point(_generic.EditableGeometryItem):
    """geometry item object that manipulates a ``point`` geometry item
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.GeometryItemType.POINT
    _GET_ATTRIBUTE_COMMAND = 'findPointAttrib'
    _LIST_ATTRIBUTES_COMMAND = 'pointAttribs'

    # COMMANDS #

    def edges(self):
        """get the edges of the Point

        :return: the edges of the Point
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Edge`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.edge(edge)
                     for edge in self.geometry().houGeometry().globEdges('p{}'.format(self.index())))

    def geometry(self):
        """get the geometry of the Point

        :return: the geometry of the Point
        :rtype: :class:`cgp_houdini_utils.scene.Geometry`
        """

        # return
        return cgp_houdini_utils.scene._api.geometry(self.houPoint().geometry())

    def houPoint(self):
        """get the hou.Point object of the Point

        :return: the hou.Point object of the Point
        :rtype: :class:`hou.Point`
        """

        # return
        return self.houGeometryItem()

    def index(self):
        """get the index of the Point - eg: the index of the first point is 0

        :return: the index of the Point
        :rtype: int
        """
        
        # return
        return self.houPoint().number()

    def path(self):
        """get the path of the Point

        :return: the path of the Point
        :rtype: str
        """

        # return
        return '{}/{}'.format(self.geometry().path(), self.index())

    def position(self):
        """get the position of the Point

        :return: the position of the Point
        :rtype: tuple[float]
        """

        # init
        position = self.houPoint().position()

        # return
        return position.x(), position.y(), position.z()

    def primitive(self, index):
        """get a primitive of the Point

        :param index: the primitive index
        :type index: int

        :return: the primitive of the Point
        :rtype: :class:`cgp_houdini_utils.scene.Primitive`
        """

        # return based on index
        for primitive in self.primitives():
            if primitive.index() == index:
                return primitive

        # error
        raise ValueError('Unable to get the primitive of {} with index: {}'.format(self, index))

    def primitives(self):
        """get the primitives of the Point

        :return: the primitives of the Point
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Primitive`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.primitive(primitive)
                     for primitive in self.houPoint().prims())

    def setPosition(self, position):
        """set the position of the Point

        :param position: the position of the Point
        :type position: tuple[float]
        """

        # execute
        self.houPoint().setPosition(position)

    def vertex(self, index):
        """get a vertex of the Point

        :param index: the vertex index
        :type index: int

        :return: the vertex of the Point
        :rtype: :class:`cgp_houdini_utils.scene.Vertex`
        """

        # return based on index
        for vertex in self.vertices():
            currentId = vertex.index()
            if currentId == index:
                return vertex

        # error
        raise ValueError('Unable to get the vertex of {} with index: {}'.format(self, index))

    def vertices(self):
        """get the vertices of the Point

        :return: the vertices of the Point
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Vertex`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.vertex(vertex)
                     for vertex in self.houPoint().vertices())
