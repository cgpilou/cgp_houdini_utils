"""
generic nodes library
"""

# imports python
import ast

# imports third-parties
import hou

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.decorators
import cgp_houdini_utils.ui
import cgp_houdini_utils.scene._type
import cgp_houdini_utils.scene._api
from . import _networkItem


# NODE OBJECTS #


class Node(_networkItem.NetworkItem):
    """network item object that manipulates any kind of node
    """

    # ATTRIBUTES #

    _ITEM_TYPE = cgp_houdini_utils.constants.NetworkItemType.NODE
    _CATEGORY = NotImplemented    # is it a sop, a lop, a dop...
    _TYPE = NotImplemented    # is it a sub network, a switch, a merge...

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, parent=None, name=None, isUniqueName=False):
        """create the Node

        :param parent: the parent node of the new node - default is to use the current network level
        :type parent: :class:`hou.Node` or :class:`cgp_houdini_utils.scene.Node`

        :param name: the name of the new node
        :type name: str

        :param isUniqueName: ``True`` : the name will be suffixed by a number if it is already in use
                             ``False`` : the name will be set as is
        :type isUniqueName: bool

        :return: the created node
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # init
        parent = (cgp_houdini_utils.scene._api.node(parent.path())
                  if parent
                  else cgp_houdini_utils.scene._api.node(hou.pwd()).parent())

        # return
        return parent.createChild(cls._TYPE, name=name, isUniqueName=isUniqueName)

    # COMMANDS #

    def child(self, path):
        """get a child node of the Node

        :param path: the relative path of the node to get
        :type path: str

        :return: the child node of the Node
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # init
        childNode = self.houNode().node(path)

        # error
        if not childNode:
            raise ValueError('{} has no child matching path: {}'.format(self, path))

        # return
        return cgp_houdini_utils.scene._api.node(childNode)

    def children(self, pattern=None, nodeTypes=None, nodeTypesIncluded=True, isRecursive=False):
        """get the children nodes of the Node

        :param pattern: the relative path pattern of the children
        :type pattern: str

        :param nodeTypes: The node types to include or exclude
        :type nodeTypes: tuple[:class:`hou.NodeType`]

        :param nodeTypesIncluded: ``True`` : the given node types be the ones returned -
                                  ``False`` : the given node types will not be returned
        :type nodeTypesIncluded: bool

        :param isRecursive: ``True`` : get children recursively - ``False`` : get only direct children
        :type isRecursive: bool

        :return: the children nodes of the Node
        :rtype: tuple[:class:`cgp_houdini_utils.Node`]
        """

        # get children
        if pattern:
            nodes = self.houNode().recursiveGlob(pattern) if isRecursive else self.houNode().glob(pattern)
        else:
            nodes = self.houNode().allSubChildren() if isRecursive else self.houNode().children()

        # filter by types
        if nodeTypes:
            nodes = tuple(node
                          for node in nodes
                          if (nodeTypesIncluded
                              and cgp_houdini_utils.scene._type.nodeType(node) in nodeTypes)
                          or (not nodeTypesIncluded
                              and cgp_houdini_utils.scene._type.nodeType(node) not in nodeTypes))

        # return
        return tuple(cgp_houdini_utils.scene._api.node(node) for node in nodes)

    def category(self):
        """get the category of the Node

        :return: the category of the Node
        :rtype: str
        """

        # return
        return cgp_houdini_utils.scene._type.nodeCategory(self.houNode())

    def cook(self, frames=None):
        """cook the Node

        :param frames: the frames to cook - default is cooking all frames
        :type frames: tuple[float]
        """

        # cook every frames
        if not frames:
            self.houNode().cook(force=True)
            return

        # cook only desired frames
        for frame in frames:
            self.houNode().cook(force=True, frame_range=(frame, frame))

    def createChild(self, nodeType, name=None, isUniqueName=False):
        """create a new child of the Node

        :param nodeType: the child node type
        :type nodeType: str

        :param name: the child node name
        :type name: str

        :param isUniqueName: ``True`` : the name will be suffixed by a number if it is already in use
                             ``False`` : the name will be set as is
        :type isUniqueName: bool

        :return: the child node
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # execute
        houNode = self.houNode().createNode(nodeType, node_name=name, force_valid_node_name=isUniqueName)

        # return
        return cgp_houdini_utils.scene._api.node(houNode)

    def createEventCallback(self, eventType, callback):
        """create an event callback on the Node

        :param eventType: the event type
        :type eventType: :class:`hou.nodeEventType`

        :param callback: the callable to execute when the event is triggered
        :type callback: callable
        """

        # execute
        self.houNode().addEventCallback(eventType, callback)

    def dependents(self):
        """get the nodes referencing the Node - the result can differ depending last cook of the nodes

        :return: the nodes referencing the Node
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Node`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.node(node)
                     for node in self.houNode().dependents(True))

    def delete(self):
        """delete the Node
        """

        # execute
        self.houNode().destroy()
        self._houNetworkItem = None

    def deleteEventCallback(self, eventType, callback):
        """delete an event callback of the Node

        :param eventType: the event type
        :type eventType: :class:`hou.nodeEventType`

        :param callback: the callable executed when the event is triggered
        :type callback: callable
        """

        # execute
        self.houNode().removeEventCallback(eventType, callback)

    def duplicate(self, destination=None, name=None):
        """duplicate the Node

        :param destination: The destination node to paste the new node into - Default is current location
        :param destination: :class:`cgp_houdini_utils.scene.Node`

        :param name: the name of the newly created node - default is try to use the same name as the original
        :type name: str

        :return: the new node
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # init
        destination = destination or self.parent()

        # error
        if not destination.isNetwork():
            raise ValueError('Unable to duplicate node. '
                             'The desired destination is not a network: {}'.format(destination))

        # duplicate the node without changing the network editor location
        toPinTypes = (cgp_houdini_utils.constants.PaneTabType.NETWORK_EDITOR,)
        with cgp_houdini_utils.decorators.PaneTabsPined(types=toPinTypes):
            newNode = cgp_houdini_utils.scene._api.node(self.houNode().copyTo(destination.houNode()))

        # move the new node to ensure it will not be placed over the original one
        if newNode.parent() == self.parent():
            newNode.setPosition((10, 10), isRelative=True)

        # set the name
        if name:
            newNode.setName(name)

        # return
        return newNode

    def eventCallbacks(self):
        """get the event callbacks of the Node

        :return: the event callbacks of the Node
        :rtype: tuple[(:class:`hou.nodeEventType`, callable)]
        """

        # return
        return self.houNode().eventCallbacks()

    def hasParameter(self, name):
        """check the given parameter exists on the Node

        :param name: the name of the parameter
        :type name: str

        :return: ``True`` : the parameter exists - ``False`` : the parameter does not exist
        :rtype: bool
        """

        # return
        return self.houNode().parm(name) is not None

    def houNode(self):
        """get the hou.Node object of the Node

        :return: the hou.Node object of the Node
        :rtype: :class:`hou.Node`,
                :class:`hou.SopNode`
        """

        # return
        return self.houNetworkItem()

    def input_(self, index=0):
        """get the node connected to the specified input of the Node

        :param index: the index of the input - default is first input
        :type index: int

        :return: the input node
        :rtype: :class:`cgp_houdini_utils.scene.NetworkItem`
        """

        # init
        inputs = self.inputs()

        # return
        return inputs[index] if index < len(inputs) else None

    def inputs(self):
        """get the nodes connected to the inputs of the Node

        :return: the nodes connected to the inputs of the Node
        :rtype: tuple[:class:`cgp_houdini_utils.scene.NetworkItem`]
        """

        # init
        houNode = self.houNode()
        inputNodes = list(houNode.inputs())
        parent = houNode.parent()

        # get indirect inputs
        indirectInputs = list(houNode.parent().indirectInputs()) if parent else None

        # prefer indirect inputs
        if indirectInputs:
            for inputIndex, inputNode in enumerate(inputNodes):
                for indirectIndex, indirectInput in enumerate(indirectInputs):
                    if indirectInput.input() == inputNode:
                        inputNodes[inputIndex] = indirectInputs.pop(indirectIndex)
                        break

        # return
        return tuple(cgp_houdini_utils.scene._api.networkItem(node) for node in inputNodes)

    def isDisplayed(self):
        """get the display state of the Node

        :return: ``True`` : the node is displayed - ``False`` : the node is not displayed
        :rtype: bool
        """

        # return
        return self.houNode().isGenericFlagSet(hou.nodeFlag.Display)

    def isLocked(self):
        """get the lock state of the Node

        :return: ``True`` : the node is locked - ``False`` : the node is not locked
        :rtype: bool
        """

        # return
        return self.houNode().isGenericFlagSet(hou.nodeFlag.Lock)

    def isNetwork(self):
        """check if the Node is a network

        :return: ``True`` : the node is a network - ``False`` : the node is not a network
        :rtype: bool
        """

        # return
        return self.houNode().isNetwork()

    def isRendered(self):
        """get the render status of the Node

        :return: ``True`` : the node is rendered - ``False`` : the node is not rendered
        :rtype: bool
        """

        # return
        return self.houNode().isGenericFlagSet(hou.nodeFlag.Render)

    def layoutChildren(self, networkItems=None, horizontalSpacing=-1.0, verticalSpacing=-1.0, isRecursive=False):
        """apply the network position layout to the children of the Node

        :param networkItems: the network items to move
        :type networkItems: tuple[:class:`cgp_houdini_utils.scene.NetworkItem`]

        :param horizontalSpacing: The horizontal spacing between nodes
        :type horizontalSpacing: float

        :param verticalSpacing: The vertical spacing between nodes
        :type verticalSpacing: float

        :param isRecursive: ``True`` : layout items into the node and its children
                            ``False`` : layout items only into the node
        :type isRecursive: bool
        """

        # init
        houNetworkItems = tuple(item.houNetworkItem() for item in networkItems) if networkItems else tuple()

        # layout direct children
        self.houNode().layoutChildren(houNetworkItems, horizontalSpacing, verticalSpacing)

        # parse sub children
        if isRecursive:
            for child in self.children():

                # bypass non network children
                if not child.isNetwork():
                    continue

                # layout sub children
                child.layoutChildren(networkItems=networkItems,
                                     horizontalSpacing=horizontalSpacing,
                                     verticalSpacing=verticalSpacing,
                                     isRecursive=True)

    def output(self, index=0):
        """get a node connected to the output of the Node

        :param index: the index of the output - default is first output
        :type index: int

        :return: the node connected to the output of the Node
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # init
        outputs = self.outputs()

        # return
        return outputs[index] if index < len(outputs) else None

    def outputs(self):
        """get the nodes connected to the outputs of the Node

        :return: the nodes connected to the outputs of the Node
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Node`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.node(node)
                     for node in self.houNode().outputs())

    def parameter(self, name):
        """get a parameter of the Node

        :param name: the parameter name
        :type name: str

        :return: the parameter of the Node
        :rtype: :class:`cgp_houdini_utils.scene.Parameter`
        """

        # init
        houParm = self.houNode().parm(name)

        # return
        return cgp_houdini_utils.scene._api.parameter(houParm) if houParm else None

    def parameterFolder(self, index):
        """get a parameter folder of the Node

        :param index: the index of the parameter folder
        :type index: int

        :return: the parameter folder of the Node
        :rtype: :class:`cgp_houdini_utils.scene.ParameterFolder`
        """

        # return
        try:
            return cgp_houdini_utils.scene._api.parameterFolder(self.houNode(), index)
        except ValueError:
            return None

    def parameterFolders(self):
        """get the parameter folders of the Node

        :return: the parameter folders of the Node
        :rtype: tuple[:class:`cgp_houdini_utils.scene.ParameterFolder`]
        """

        # init
        folders = tuple()
        count = len(self.houNode().parmTemplateGroup().entries())

        # parse folders
        for index in range(count):
            folder = self.parameterFolder(index)
            if folder:
                folders += (folder, )

        # return
        return folders

    def parameters(self):
        """get the parameters of the Node

        :return: the parameters of the Node
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Parameter`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.parameter(houParm)
                     for houParm in self.houNode().parms())

    def references(self):
        """get the nodes referenced by the Node

        :return: the nodes referenced by the Node
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Node`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.node(node)
                     for node in self.houNode().references(True))

    def setDisplayed(self, isAlsoRendered=True):
        """set the display state of the node
        note: to set this state to ``False`` you need to set the display state on another node of the same graph

        :param isAlsoRendered:  ``True`` if the render state also needs to be activated - ``False`` otherwise
        :type isAlsoRendered: bool
        """

        # activate display flag
        self.houNode().setGenericFlag(hou.nodeFlag.Display, True)

        # set also the render flag
        if isAlsoRendered:
            self.setRendered()

    def setInput(self, networkItem, inputIndex=0, outputIndex=0):
        """set an input of the Node

        :param networkItem: the network item to connect - ``None`` to disconnect everything from the input
        :type networkItem: :class:`cgp_houdini_utils.scene.NetworkItem`

        :param inputIndex: the index of the input to manipulate
        :type inputIndex: int

        :param outputIndex: the index of the output of the given network item
        :type outputIndex: int
        """

        # init
        current = self.houNetworkItem()
        other = networkItem.houNetworkItem() if networkItem else None

        # error
        if other and current.parent() != other.parent():
            raise ValueError('Unable to connect nodes. Parents are different: {} and {}'.format(self, networkItem))

        # execute
        current.setInput(inputIndex, other, outputIndex)

    def setLocked(self, isLocked):
        """set the lock state of the node

        :param isLocked: ``True`` : lock the node - ``False`` : unlock the node
        :type isLocked: bool
        """

        # execute
        self.houNode().setGenericFlag(hou.nodeFlag.Lock, isLocked)

    def setOutput(self, node, outputIndex=None, inputIndex=0):
        """set an output of the Node

        :param node: the node to connect - ``None`` to disconnect everything from the input
        :type node: :class:`cgp_houdini_utils.scene.Node`

        :param outputIndex: the index of the output to manipulate
        :type outputIndex: int

        :param inputIndex:  the index of the input of the given node
        :type inputIndex: int
        """

        # connect the output
        if node:
            outputIndex = 0 if outputIndex is None else outputIndex
            node.setInput(self, inputIndex=inputIndex, outputIndex=outputIndex)
            return

        # disconnect the output
        outputNodes = self.houNode().outputs() if outputIndex is None else (self.houNode().output(outputIndex))
        for outputNode in outputNodes:
            outputNode.setInput(inputIndex, None)

    def setParent(self, node):
        """set the parent of the Node (move the node under the new parent)

        :param node: the parent node
        :type node: :class:`cgp_houdini_utils.scene.Node`
        """

        # errors
        if self.parent() == node:
            return
        if node.path().startswith(self.path()):
            raise ValueError('Unable to parent a node under itself: {}'.format(node))
        if not node.isNetwork():
            raise ValueError('Unable to parent node. The desired parent is not a network: {}'.format(node))

        # init
        originalNode = self.houNode()

        # duplicate the node under the new parent
        toPinTypes = (cgp_houdini_utils.constants.PaneTabType.NETWORK_EDITOR,)
        with cgp_houdini_utils.decorators.PaneTabsPined(types=toPinTypes):
            newNode = originalNode.copyTo(node.houNode())

        # update houdini node
        self.houNode().destroy()
        self._houNetworkItem = newNode

    def setReference(self, sourceNode, parameters=None, isForced=False):
        """set the reference (which will drive the parameters) of the Node

        :param sourceNode: the node to reference - or None to remove the reference
        :type sourceNode: :class:`cgp_houdini_utils.scene.Node` or None

        :param parameters: the parameters to reference - default is all parameters of this node
        :param parameters: tuple[:class:`cgp_houdini_utils.scene.Parameter`]

        :param isForced: ``True`` : parameters will be unreferenced before to be referenced -
                         ``False`` : only non-referenced parameters will be referenced
        :param isForced: bool
        """

        # init
        parameters = parameters or self.parameters()

        # disconnect
        if sourceNode is None:
            for parameter in parameters:
                parameter.setReference(None)
            return

        # connect
        for parameter in parameters:
            sourceParameter = sourceNode.parameter(parameter.name())
            if isForced or parameter.reference() != sourceParameter:
                parameter.setReference(sourceParameter)

    def setRendered(self):
        """set the render status of the Node
        note: to set this state to ``False`` we need to set the render state on another node of the same graph
        """

        # execute
        self.houNode().setGenericFlag(hou.nodeFlag.Render, True)

    def type_(self):
        """get the type of the Node

        :return: the type of the Node
        :rtype: str
        """

        # return
        return cgp_houdini_utils.scene._type.nodeType(self.houNode())

    def viewerState(self):
        """get the viewer state of the Node

        :return: the viewer state of the Node
        :rtype: :class:`cgp_houdini_utils.BaseNodeState`
        """

        # init
        houNodeType = self.houNode().type()

        # return based on hda definition
        viewerStateName = houNodeType.definition().sections()['DefaultState'].contents()
        if viewerStateName:
            return cgp_houdini_utils.ui.viewerState(viewerStateName)

        # return based on node type
        for viewerType in (hou.stateViewerType.Scene, hou.stateViewerType.Compositor):
            for viewerState in houNodeType.category().viewerStates(viewerType):
                if viewerState.nodeType() == houNodeType:
                    return cgp_houdini_utils.ui.viewerState(viewerState)

        # return if nothing found
        return None

    def visualizers(self):
        """get the visualizers of the Node

        :return: the visualizers of the Node
        :rtype: tuple[:class:`cgp_houdini_utils.ui.Visualizer`]
        """

        # init
        categories = (cgp_houdini_utils.constants.VisualizerCategory.NODE,)

        # return
        return cgp_houdini_utils.ui.visualizers(categories=categories, node=self.houNode())
