"""
generic object library
"""

# import python
import ast

# imports third-parties
import hou

# import local
import cgp_houdini_utils.scene._api


# GENERIC OBJECTS #


class Parm(object):
    """node object that manipulates any kind of parm
    """

    # INIT #

    def __init__(self, node, parm):
        """Parm class initialization

        :param node: node on which the parm exists
        :type node: str

        :param parm: name of the parm
        ;param parm: str
        """

        # init
        self._houParm = hou.node(node).parm(parm)

    def __getattr__(self, attribute):
        """override getattr

        :param attribute: the attribute to get
        :type attribute: any
        """

        # return
        return getattr(self.houParm(), attribute)

    def __repr__(self):
        """the representation of the parm

        :return: the representation of the parm
        :rtype: str
        """

        # return
        return '{0}({1!r}, {2!r})'.format(self.__class__.__name__, self.node().path(), self.name())

    # COMMANDS #

    def evalAsLiteral(self):
        """eval the attribute raw value as a literal

        :return: the evaluated literal
        :rtype: literal
        """

        # return
        return ast.literal_eval(self.rawValue())

    def houParm(self):
        """the houParm of the parm

        :return: the houParm
        :rtype: :class:`hou.Parm`
        """

        # return
        return self._houParm

    def node(self):
        """the node of the parm

        :return: the node of the parm
        :rtype: `:class: rdo_houdini_rig_utils.scene.Node`
        """

        # return
        return cgp_houdini_utils.scene._api.node(self.houParm().node().path())
