"""
vertex library
"""

# imports third parties
import hou

# imports local
import cgp_houdini_utils.constants
from . import _generic


# VERTEX OBJECTS #


class Vertex(_generic.EditableGeometryItem):
    """geometry item object that manipulates a ``vertex`` geometry item
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.GeometryItemType.VERTEX
    _GET_ATTRIBUTE_COMMAND = 'findVertexAttrib'
    _LIST_ATTRIBUTES_COMMAND = 'vertexAttribs'

    # COMMANDS #

    def edges(self):
        """get the edges of the Vertex

        :return: the edges of the Vertex
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Edge`]
        """

        # return
        return tuple(edge
                     for edge in self.point().edges()
                     if self.primitive() in edge.primitives())

    def geometry(self):
        """get the geometry of the Vertex

        :return: the geometry of the Vertex
        :rtype: :class:`cgp_houdini_utils.scene.Geometry`
        """

        # return
        return cgp_houdini_utils.scene._api.geometry(self.houVertex().geometry())

    def houVertex(self):
        """get the hou.Vertex object of the Vertex

        :return: the hou.Vertex object of the Vertex
        :rtype: :class:`hou.Vertex`
        """

        # return
        return self.houGeometryItem()

    def index(self):
        """get the index of the Vertex - eg: the index of the first vertex of primitive 518 is '518v0'

        :return: the index of the Vertex
        :rtype: str
        """

        # return
        return "{}v{}".format(self.primitive().index(), self.houVertex().number())

    def path(self):
        """get the path of the Vertex

        :return: the path of the Vertex
        :rtype: str
        """

        # return
        return '{}/{}'.format(self.geometry().path(), self.index())
    
    def point(self):
        """get a point of the Vertex

        :return: the point of the Vertex
        :rtype: :class:`cgp_houdini_utils.scene.Point`
        """

        # return
        return cgp_houdini_utils.scene._api.point(self.houVertex().point())

    def primitive(self):
        """get a primitive of the Vertex

        :return: the primitive of the Vertex
        :rtype: :class:`cgp_houdini_utils.scene.Primitive`
        """

        # return
        return cgp_houdini_utils.scene._api.primitive(self.houVertex().prim())
