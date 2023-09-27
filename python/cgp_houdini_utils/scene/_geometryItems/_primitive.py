"""
primitive library
"""

# imports third parties
import hou

# imports local
import cgp_houdini_utils.constants
from . import _generic


# PRIMITIVE OBJECTS #


class Primitive(_generic.EditableGeometryItem):
    """geometry item object that manipulates a ``primitive`` geometry item
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.GeometryItemType.PRIMITIVE
    _GET_ATTRIBUTE_COMMAND = 'findPrimAttrib'
    _LIST_ATTRIBUTES_COMMAND = 'primAttribs'

    # COMMANDS #

    def edges(self):
        """get the edges of the Primitive

        :return: the edges of the Primitive
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Edge`]
        """

        # init
        points = self.points()
        edges = tuple()

        # collect edges
        for index1, point1 in enumerate(points):
            for point2 in points[index1 + 1:]:
                edge = self.geometry().houGeometry().findEdge(point1.houPoint(), point2.houPoint())
                if edge:
                    edges += (edge,)

        # return
        return tuple(cgp_houdini_utils.scene._api.edge(edge)
                     for edge in edges)

    def geometry(self):
        """get the geometry of the Primitive

        :return: the geometry of the Primitive
        :rtype: :class:`cgp_houdini_utils.scene.Geometry`
        """

        # return
        return cgp_houdini_utils.scene._api.geometry(self.houPrim().geometry())

    def houPrim(self):
        """get the hou.Prim object of the Primitive

        :return: the hou.Prim object of the Primitive
        :rtype: :class:`hou.Prim`
        """

        # return
        return self.houGeometryItem()

    def index(self):
        """get the index of the Primitive - eg: the index of the first primitive is 0

        :return: the index of the Primitive
        :rtype: int
        """

        # return
        return self.houPrim().number()

    def path(self):
        """get the path of the Primitive

        :return: the path of the Primitive
        :rtype: str
        """

        # return
        return '{}/{}'.format(self.geometry().path(), self.index())

    def point(self, index):
        """get a point of the Primitive

        :param index: the point index
        :type index: int

        :return: the point of the Primitive
        :rtype: :class:`cgp_houdini_utils.scene.Point`
        """

        # return based on index
        for point in self.points():
            if point.index() == index:
                return point

        # error
        raise ValueError('Unable to get the point of {} with index: {}'.format(self, index))

    def points(self):
        """get the points of the Primitive

        :return: the points of the Primitive
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Point`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.point(point)
                     for point in self.houPrim().points())

    def type_(self):
        """get the type of the Primitive

        :return: the type of the Primitive
        :rtype: str
        """

        # return
        return str(self.houPrim().type()).rsplit('.', 1)[-1]

    def vertex(self, index):
        """get a vertex of the Primitive

        :param index: the vertex index
        :type index: int

        :return: the vertex of the Primitive
        :rtype: :class:`cgp_houdini_utils.scene.Vertex`
        """

        # return based on index
        for vertex in self.vertices():
            currentId = vertex.index()
            if currentId == index or currentId == '{}v{}'.format(self.index(), index):
                return vertex

        # error
        raise ValueError('Unable to get the vertex of {} with index: {}'.format(self, index))

    def vertices(self):
        """get the vertices of the Primitive

        :return: the vertices of the Primitive
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Vertex`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.vertex(vertex)
                     for vertex in self.houPrim().vertices())
