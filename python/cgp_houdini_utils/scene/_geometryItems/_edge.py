"""
edge library
"""

# imports third parties
import hou

# imports local
import cgp_houdini_utils.constants
from . import _generic


# EDGE OBJECTS #


class Edge(_generic.GeometryItem):
    """geometry item object that manipulates an ``edge`` geometry item
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.GeometryItemType.EDGE

    # COMMANDS #

    def geometry(self):
        """get the geometry of the Edge

        :return: the geometry of the Edge
        :rtype: :class:`cgp_houdini_utils.scene.Geometry`
        """

        # return
        return cgp_houdini_utils.scene._api.geometry(self.houEdge().geometry())

    def houEdge(self):
        """get the hou.Edge object of the Edge

        :return: the hou.Edge object of the Edge
        :rtype: :class:`hou.Edge`
        """

        # return
        return self.houGeometryItem()

    def index(self):
        """get the index of the Edge - eg: the index of the edge between point 0 and point 1 is 'p0-1'

        :return: the index of the Edge
        :rtype: str
        """

        # return
        return self.houEdge().edgeId()

    def length(self):
        """get the length of the Edge

        :return: the length of the Edge
        :rtype: float
        """

        # return
        return self.houEdge().length()

    def path(self):
        """get the path of the Edge

        :return: the path of the Edge
        :rtype: str
        """

        # return
        return '{}/{}'.format(self.geometry().path(), self.index())

    def point(self, index):
        """get a point of the Edge

        :param index: the point index
        :type index: int

        :return: the point of the Edge
        :rtype: :class:`cgp_houdini_utils.scene.Point`
        """

        # return based on index
        for point in self.points():
            if point.index() == index:
                return point

        # error
        raise ValueError('Unable to get the point of {} with index: {}'.format(self, index))

    def points(self):
        """get the points of the Edge

        :return: the points of the Edge
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Point`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.point(point)
                     for point in self.houEdge().points())

    def primitive(self, index):
        """get a primitive of the Edge

        :param index: the primitive index
        :type index: int

        :return: the primitive of the Edge
        :rtype: :class:`cgp_houdini_utils.scene.Primitive`
        """

        # return based on index
        for primitive in self.primitives():
            if primitive.index() == index:
                return primitive

        # error
        raise ValueError('Unable to get the primitive of {} with index: {}'.format(self, index))

    def primitives(self):
        """get the primitives of the Edge

        :return: the primitives of the Edge
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Primitive`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.primitive(primitive)
                     for primitive in self.houEdge().prims())

    def vertex(self, index):
        """get a vertex of the Edge

        :param index: the vertex index
        :type index: int

        :return: the vertex of the Edge
        :rtype: :class:`cgp_houdini_utils.scene.Vertex`
        """

        # return based on index
        for vertex in self.vertices():
            if vertex.index() == index:
                return vertex

        # error
        raise ValueError('Unable to get the vertex of {} with index: {}'.format(self, index))

    def vertices(self):
        """get the vertices of the Edge

        :return: the vertices of the Edge
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Vertex`]
        """

        # init
        pointVertices = [vertex for point in self.points() for vertex in point.vertices()]
        primitiveVertices = [vertex for primitive in self.primitives() for vertex in primitive.vertices()]

        # return
        return tuple(vertex for vertex in pointVertices if vertex in primitiveVertices)
