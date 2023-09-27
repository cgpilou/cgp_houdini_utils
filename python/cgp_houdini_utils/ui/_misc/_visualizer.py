"""
visualizer library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene
import cgp_houdini_utils.ui._api


# VISUALIZER OBJECTS #


class Visualizer(cgp_generic_utils.python.BaseObject):
    """visualizer object that manipulates any kind of houdini visualizer
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.VisualizerCategory.COMMON

    # INIT #

    def __init__(self, visualizer):
        """initialization of the Visualizer

        :param visualizer: the houdini visualizer
        :type visualizer: :class:`hou.ViewportVisualizer`
        """

        # init
        self._houVisualizer = visualizer

    def __repr__(self):
        """get the representation of the Visualizer

        :return: the representation of the Visualizer
        :rtype: str
        """

        # return
        return self._representationTemplate().format(visualizer=self.houVisualizer())

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, type_):
        """create the visualizer

        :param type_: the type of the visualizer to create
        :type type_: :class:`cgp_houdini_utils.constants.VisualizerType`
        """

        # init
        type_ = hou.viewportVisualizers.type(type_)
        categories = {cgp_houdini_utils.constants.VisualizerCategory.COMMON: hou.viewportVisualizerCategory.Common,
                      cgp_houdini_utils.constants.VisualizerCategory.NODE: hou.viewportVisualizerCategory.Node,
                      cgp_houdini_utils.constants.VisualizerCategory.SCENE: hou.viewportVisualizerCategory.Scene}

        # return
        return cls(hou.viewportVisualizers.createVisualizer(type_, categories[cls._CATEGORY]))

    # COMMANDS #

    def attribute(self):
        """get the attribute of the Visualizer

        :return: the attribute of the Visualizer
        :rtype: str
        """

        # return
        return self.houVisualizer().evalParmAsString('attrib')

    def category(self):
        """get the category of the Visualizer

        :return: the category of the Visualizer
        :rtype: str
        """

        # return
        return cgp_houdini_utils.ui._type.visualizerCategory(self.houVisualizer())

    def delete(self):
        """delete the Visualizer
        """

        # execute
        self.houVisualizer().destroy()
        self._houVisualizer = None

    def houVisualizer(self):
        """get the hou.Visualizer object of the Visualizer

        :return: the houdini visualizer of the Visualizer
        :rtype: :class:`hou.Visualizer`
        """

        # return
        return self._houVisualizer

    def isActive(self):
        """get the active state of the Visualizer

        :return: ``True`` : the visualizer is active - ``False`` : the visualizer is not active
        :rtype: bool
        """

        # execute
        self.houVisualizer().isActive()

    def setActive(self, isActive):
        """set the active state of the Visualizer

        :param isActive: ``True`` : activate the visualizer - ``False`` : deactivate the visualizer
        :type isActive: bool
        """

        # execute
        for paneTab in hou.ui.paneTabs():
            if paneTab.type() != hou.paneTabType.SceneViewer:
                continue
            for viewport in paneTab.viewports():
                self.houVisualizer().setIsActive(isActive, viewport=viewport)

    def setAttribute(self, attribute):
        """set the attribute of the NodeVisualizer

        :param attribute: the attribute to set to the NodeVisualizer
        :type attribute: :class:`cgp_houdini_utils.scene.Parameter` or str
        """

        # init
        attribute = attribute.name() if isinstance(attribute, cgp_houdini_utils.scene.Attribute) else attribute

        # execute
        self.houVisualizer().setParm('attrib', attribute)

    def setType(self, type_):
        """set the type of the Visualizer

        :param type_: the type to set to the Visualizer
        :type type_: :class:`cgp_houdini_utils.constants.VisualizerType`
        """

        # execute
        self.houVisualizer().setType(hou.viewportVisualizers.type(type_))

    def type_(self):
        """get the type of the Visualizer

        :return: the type of the Visualizer
        :rtype: :class:`cgp_houdini_utils.constants.VisualizerType`
        """

        # return
        return self.houVisualizer().type().name()


class NodeVisualizer(Visualizer):
    """visualizer object that manipulates a node visualizer
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.VisualizerCategory.NODE

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, type_, node):
        """create the NodeVisualizer

        :param type_: the type of the NodeVisualizer to create
        :type type_: :class:`cgp_houdini_utils.constants.VisualizerType`

        :param node: the node of the NodeVisualizer to create
        :type node: :class:`cgp_houdini_utils.scene.Node`
        """

        # init
        type_ = hou.viewportVisualizers.type(type_)
        categories = {cgp_houdini_utils.constants.VisualizerCategory.COMMON: hou.viewportVisualizerCategory.Common,
                      cgp_houdini_utils.constants.VisualizerCategory.NODE: hou.viewportVisualizerCategory.Node,
                      cgp_houdini_utils.constants.VisualizerCategory.SCENE: hou.viewportVisualizerCategory.Scene}

        # return
        return cls(hou.viewportVisualizers.createVisualizer(type_, categories[cls._CATEGORY], node=node.houNode()))

    # COMMANDS #

    def node(self):
        """get the node of the NodeVisualizer

        :return: the node of the NodeVisualizer
        :rtype: str
        """

        # return
        return self.houVisualizer().categoryNode()

    def setActive(self, isActive):
        """set the active state of the NodeVisualizer

        :param isActive: ``True`` : activate the visualizer - ``False`` : deactivate the visualizer
        :type isActive: bool
        """

        # execute
        self.houVisualizer().setIsActive(isActive)


class SceneVisualizer(Visualizer):
    """visualizer object that manipulates a scene visualizer
    """

    # ATTRIBUTES #

    _CATEGORY = cgp_houdini_utils.constants.VisualizerCategory.SCENE
