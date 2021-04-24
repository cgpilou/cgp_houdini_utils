"""
generic object library
"""

# imports third-parties
import hou

# import local
import cgp_houdini_utils.scene._api


# GENERIC OBJECTS #


class Node(object):
    """node object that manipulates any kind of node
    """

    # INIT #

    def __init__(self, name):
        """Node class initialization

        :param name: name of the node
        :type name: str
        """

        # init
        self._houNode = hou.node(name)

    def __getattr__(self, attribute):
        """override getattr

        :param attribute: the attribute to get
        :type attribute: classAttribute
        """

        # return
        return getattr(self.houNode(), attribute)

    # COMMANDS #

    def houNode(self):
        """the houNode of the node

        :return: the houNode
        :rtype: :class:`hou.Node`
        """

        # return
        return self._houNode

    def parm(self, parm_):
        """the parm of the node

        :param parm_: the parm to get
        :type: str

        :return: the parm of the node
        :rtype: `:class: rdo_houdini_utils.scene.Parm`
        """

        # return
        return cgp_houdini_utils.scene._api.parm(self.path(), parm_)
