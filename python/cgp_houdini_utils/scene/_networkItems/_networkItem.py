"""
generic network items library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene._type
import cgp_houdini_utils.scene._api


# GENERIC OBJECTS #


class NetworkItem(cgp_generic_utils.python.BaseObject):
    """network item object that manipulates any kind of network item
    """

    # ATTRIBUTES #

    _ITEM_TYPE = cgp_houdini_utils.constants.NetworkItemType.GENERIC  # is it a node, a sticky note, a connection...

    # INIT #

    def __init__(self, networkItem):
        """initialization of the NetworkItem

        :param networkItem: the houdini network item
        :type networkItem: str or :class:`hou.NetworkItem`
        """

        # init
        self._houNetworkItem = hou.item(networkItem) if isinstance(networkItem, str) else networkItem

    def __eq__(self, other):
        """check if an other NetworkItem is equal to the NetworkItem

        :param other: the other NetworkItem
        :type other: :class:`cgp_houdini_utils.scene.NetworkItem`

        :return: ``True`` : the two network items are equal - ``False`` : the two network items are not equal
        :rtype: bool
        """

        # return
        return self.houNetworkItem() == other.houNetworkItem() if isinstance(other, NetworkItem) else False

    def __ne__(self, other):
        """check if an other NetworkItem is not equal to the NetworkItem

        :param other: the other NetworkItem
        :type other: :class:`cgp_houdini_utils.scene.NetworkItem`

        :return: ``True`` : the two network items are not equal - ``False`` : the two network items are equal
        :rtype: bool
        """

        # return
        return self.houNetworkItem() != other.houNetworkItem() if isinstance(other, NetworkItem) else True

    def __repr__(self):
        """get the representation of the NetworkItem

        :return: the representation of the NetworkItem
        :rtype: str
        """

        # return
        return self._representationTemplate().format(networkItem=self.path())

    # COMMANDS #

    def houNetworkItem(self):
        """get the hou.NetworkMovableItem object of the NetworkItem

        :return: the hou.NetworkMovableItem object of the NetworkItem
        :rtype: :class:`hou.NetworkMovableItem`
        """

        # return
        return self._houNetworkItem

    def isSelected(self):
        """check selection status of the NetworkItem

        :return: ``True`` : the NetworkItem is selected - ``False`` : the NetworkItem is not selected
        :rtype: bool
        """

        # return
        return self.houNetworkItem().isSelected()

    def name(self):
        """get the name of the NetworkItem

        :return: the name of the NetworkItem
        :rtype: str
        """

        # return
        return self.houNetworkItem().name()

    def networkItemType(self):
        """get the network item type of the NetworkItem

        :return: the network item type of the NetworkItem
        :rtype: :class:`cgp_houdini_utils.constants.NetworkItemType`
        """

        # return
        return cgp_houdini_utils.scene._type.networkItemType(self.houNetworkItem())

    def parent(self):
        """get the parent item of the NetworkItem

        :return: the parent item of the NetworkItem
        :rtype: :class:`cgp_houdini_utils.scene.NetworkItem`
        """

        # init
        houParent = self.houNetworkItem().parent()

        # return
        return cgp_houdini_utils.scene._api.networkItem(houParent) if houParent else None

    def path(self, relativeTo=None):
        """get the absolute or relative path of the NetworkItem

        :param relativeTo: the network item to get the relative path to
        :type relativeTo: :class:`cgp_houdini_utils.scene.NetworkItem`

        :return: the absolute or relative path of the NetworkItem
        :rtype: str
        """

        # return
        return (self.houNetworkItem().relativePathTo(relativeTo.houNetworkItem())
                if relativeTo
                else self.houNetworkItem().path())

    def position(self):
        """get the network position of the NetworkItem

        :return: the network position of the NetworkItem
        :rtype: tuple[float, float]
        """

        # return
        return tuple(self.houNetworkItem().position())

    def setName(self, name, isUnique=False):
        """set the name of the NetworkItem

        :param name: the name to set
        :type name: str

        :param isUnique: ``True`` : the name can be changed by the closest available name -
                         ``False`` : the given name will be use even if another node has the same name
        :type isUnique: bool
        """

        # execute
        self.houNetworkItem().setName(name, isUnique)

    def setPosition(self, position, isRelative=False):
        """set the network position of the NetworkItem

        :param position: the network position to set
        :type position: tuple[float, float]

        :param isRelative: ``True`` : the NetworkItem will be moved relatively to its current position
                           ``False`` : the NetworkItem will be moved at the given position
        :type isRelative: bool
        """

        # init
        houVector = hou.Vector2(*position)

        # relative move
        if isRelative:
            self.houNetworkItem().move(houVector)

        # absolute position
        else:
            self.houNetworkItem().setPosition(houVector)

    def setSelected(self, isSelected):
        """set the selection status of the NetworkItem

        :param isSelected: ``True`` : select the NetworkItem - ``False`` : unselect the NetworkItem
        :type isSelected: bool
        """

        # return
        self.houNetworkItem().setSelected(isSelected)


class Connection(NetworkItem):
    """network item object that manipulates a ``Connection`` network item
    """

    # ATTRIBUTES #

    _ITEM_TYPE = cgp_houdini_utils.constants.NetworkItemType.CONNECTION


class NetworkBox(NetworkItem):
    """network item object that manipulates a ``NetworkBox`` network item
    """

    # ATTRIBUTES #

    _ITEM_TYPE = cgp_houdini_utils.constants.NetworkItemType.NETWORK_BOX


class NetworkDot(NetworkItem):
    """network item object that manipulates a ``NetworkDot`` network item
    """

    # ATTRIBUTES #

    _ITEM_TYPE = cgp_houdini_utils.constants.NetworkItemType.NETWORK_DOT


class StickyNote(NetworkItem):
    """network item object that manipulates a ``StickyNote`` network item
    """

    # ATTRIBUTES #

    _ITEM_TYPE = cgp_houdini_utils.constants.NetworkItemType.STICKY_NOTE


class SubNetworkIndirectInput(NetworkItem):
    """network item object that manipulates a ``SubnetIndirectInput`` network item
    """

    # ATTRIBUTES #

    _ITEM_TYPE = cgp_houdini_utils.constants.NetworkItemType.SUB_NETWORK_INDIRECT_INPUT

    # COMMANDS #

    def input_(self):
        """get the network item connected to the input of the SubNetworkIndirectInput

        :return: the network item connected to the input of the SubNetworkIndirectInput
        :rtype: :class:`cgp_houdini_utils.scene.NetworkItem`
        """

        # init
        houNetworkItem = self.houNetworkItem().inputItem()

        # return
        return cgp_houdini_utils.scene._api.networkItem(houNetworkItem) if houNetworkItem else None

    def output(self, index=0):
        """get the node connected to the given output of the SubNetworkIndirectInput

        :param index: the index of the output - default is first output
        :type index: int

        :return: the node connected to the given output of the SubNetworkIndirectInput
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # return
        return self.outputs()[index]

    def outputs(self):
        """get the nodes connected to the outputs of the SubNetworkIndirectInput

        :return: the nodes connected to the outputs of the SubNetworkIndirectInput
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Node`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.node(node) for node in self.houNetworkItem().outputs())
