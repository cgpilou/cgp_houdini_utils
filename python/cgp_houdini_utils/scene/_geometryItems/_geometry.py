"""
geometry library
"""

# imports third parties
import hou

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene._api
from . import _generic


# GEOMETRY OBJECTS #


class Geometry(_generic.EditableGeometryItem):
    """geometry item object that manipulates a ``geometry`` (aka ``global`` or ``detail``) geometry item
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.GeometryItemType.GEOMETRY
    _GET_ATTRIBUTE_COMMAND = 'findGlobalAttrib'
    _LIST_ATTRIBUTES_COMMAND = 'globalAttribs'

    # COMMANDS #

    def createAttribute(self, geometryItemType, attributeType, name, defaultValue=None):
        """create a new attribute to the Geometry

        :param geometryItemType: the geometry item type to create the attribute on
        :type geometryItemType: :class:`cgp_houdini_utils.constants.GeometryItemType`

        :param attributeType: the attribute type
        :type attributeType: :class:`cgp_houdini_utils.constants.AttributeType`

        :param name: the attribute name
        :type name: str

        :param defaultValue: the attribute default value
        :type defaultValue: any
        """

        # execute
        cgp_houdini_utils.scene._api.createAttribute(self,
                                                     geometryItemType,
                                                     attributeType,
                                                     name,
                                                     defaultValue=defaultValue)

    def edge(self, index):
        """get an edge of the Geometry

        :param index: the edge index
        :type index: int

        :return: the edge of the Geometry
        :rtype: :class:`cgp_houdini_utils.scene.Edge`
        """

        # init
        edges = self.houGeometry().globEdges(index)

        # error
        if len(edges) != 1:
            raise ValueError('Unable to get the edge of "{}" with index: {}'.format(self, index))

        # return
        return cgp_houdini_utils.scene._api.edge(edges[0])

    def edges(self):
        """get the edges of the Geometry

        :return: the edges of the Geometry
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Edge`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.edge(edge)
                     for edge in self.houGeometry().globEdges('*'))

    def houGeometry(self):
        """get the hou.Geometry object of the Geometry

        :return: the hou.Geometry object of the Geometry
        :rtype: :class:`hou.Geometry`
        """

        # return
        return self.houGeometryItem()

    def nearestPoints(self, position, maximum=None, radius=None):
        """get the nearest points on the Geometry

        :param position: a 3d position
        :type position: tuple[int, int, int]

        :param maximum: the maximum number of points wanted
        :type maximum: int

        :param radius: the radius around the 3d position to search in
        :type radius: float

        :return: the nearest points on the Geometry
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Point`]
        """

        # init
        maximum = maximum or len(self.points())
        kwargs = {} if radius is None else {'max_radius': radius}

        # return
        return tuple(cgp_houdini_utils.scene._api.point(point)
                     for point in self.houGeometry().nearestPoints(position, maximum, **kwargs))

    def node(self):
        """get the node of the Geometry

        :return: the node of the Geometry
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # init
        houNode = self.houGeometry().sopNode() or hou.pwd()

        # return
        return cgp_houdini_utils.scene._api.node(houNode)

    def index(self):
        """get the index of the Geometry - eg: the index of the first geometry is 0

        :return: the index of the Geometry
        :rtype: int or str
        """

        # return
        return self.houGeometry().sopNodeOutputIndex()

    def path(self):
        """get the path of the Geometry

        :return: the path of the Geometry
        :rtype: str
        """

        # return
        return '{}/{}'.format(self.node().path(), self.index())

    def point(self, index):
        """get a point of the Geometry

        :param index: the point index
        :type index: int

        :return: the point of the Geometry
        :rtype: :class:`cgp_houdini_utils.scene.Point`
        """

        # return
        return cgp_houdini_utils.scene._api.point(self.houGeometry().point(index))

    def points(self):
        """get the points of the Geometry

        :return: the points of the Geometry
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Point`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.point(point)
                     for point in self.houGeometry().points())

    def primitive(self, index):
        """get a primitive of the Geometry

        :param index: the primitive index
        :type index: int

        :return: the primitive of the Geometry
        :rtype: :class:`cgp_houdini_utils.scene.Primitive`
        """

        # return
        return cgp_houdini_utils.scene._api.primitive(self.houGeometry().prim(index))

    def primitives(self):
        """get the primitives of the Geometry

        :return: the primitives of the Geometry
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Primitive`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.primitive(primitive)
                     for primitive in self.houGeometry().prims())

    def vertex(self, index):
        """get a vertex of the Geometry

        :param index: the vertex index
        :type index: int

        :return: the vertex of the Geometry
        :rtype: :class:`cgp_houdini_utils.scene.Vertex`
        """

        # init
        vertices = self.houGeometry().globVertices(index)

        # error
        if len(vertices) > 1:
            raise ValueError('More than one vertex of {} with index: {}'.format(self, index))

        # return
        return cgp_houdini_utils.scene._api.vertex(vertices[0])

    def vertices(self):
        """get the vertices of the Geometry

        :return: the vertices of the Geometry
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Vertex`]
        """

        # return
        return tuple(vertex
                     for primitive in self.primitives()
                     for vertex in primitive.vertices())
