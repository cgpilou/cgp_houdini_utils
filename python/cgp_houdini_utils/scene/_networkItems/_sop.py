"""
sop nodes library
"""

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene._api
from . import _node


# BASE OBJECTS #


class SopNode(_node.Node):
    """node object that manipulates a ``Sop`` node
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.NodeCategory.SOP

    # COMMANDS #

    def geometry(self, index=0, frame=None):
        """get a geometry of the SopNode

        :param index: the index of the geometry (the node output index relative to the geometry)
        :type index: int

        :param frame: the frame to evaluate - default is current frame
        :type frame: float

        :return: the geometry of the SopNode
        :rtype: :class:`cgp_houdini_utils.scene.Geometry`
        """

        # init
        houGeometry = (self.houNode().geometry(index)
                       if frame is None
                       else self.houNode().geometryAtFrame(frame, index))

        # return
        return cgp_houdini_utils.scene._api.geometry(houGeometry)

    def isBypassed(self):
        """check the bypass status of the SopNode

        :return: ``True`` : the SopNode is bypassed - ``False`` : the SopNode is not bypassed
        :rtype: bool
        """

        # return
        return self.houNode().isBypassed()

    def setBypassed(self, isBypassed):
        """set the bypass status of the SopNode

        :return: ``True`` : bypass the SopNode - ``False`` : un-bypass the SopNode
        :rtype: bool
        """

        # execute
        self.houNode().bypass(isBypassed)


# SOP OBJECTS #


class SubNetwork(SopNode):
    """node object that manipulates a ``subnet`` node
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.NodeType.SUB_NETWORK

    # COMMANDS #

    def innerInputs(self):
        """get the inner/indirect inputs of the SubNetwork

        :return: the inner/indirect inputs of the SubNetwork
        :rtype: list[:class:`cgp_houdini_utils.scene.SubNetworkIndirectInput`]
        """

        # return
        return tuple(cgp_houdini_utils.scene.networkItem(node)
                     for node in self.houNode().indirectInputs())

    def innerOutputs(self):
        """get the inner outputs of the SubNetwork

        :return: the inner outputs of the SubNetwork
        :rtype: list[:class:`cgp_houdini_utils.scene.SopNode`]
        """

        # return
        return tuple(cgp_houdini_utils.scene.node(node)
                     for node in self.houNode().subnetOutputs())


class SwitchNode(SopNode):
    """node object that manipulates a ``switch`` node
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.NodeType.SWITCH
    INPUT_PARAMETER = 'input'

    # COMMANDS #

    def input_(self, index=None):
        """get the node connected to the specified input of the SwitchNode

        :param index: the index of the input - default is the input set in the switch node parameter
        :type index: int

        :return: the node connected to the specified input of the SwitchNode
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # init
        index = self.parameter(self.INPUT_PARAMETER).value() if index is None else index

        # return
        return super(SwitchNode, self).input_(index=index)
