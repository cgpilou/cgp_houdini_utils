"""
scene viewer paneTab library
"""

# imports third-parties
import hou

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene
import cgp_houdini_utils.ui._api
from . import _generic


# SCENE VIEWER OBJECTS #


class SceneViewer(_generic.PaneTab):
    """pane tab object that manipulates any king of houdini scene viewer
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.PaneTabType.SCENE_VIEWER

    # COMMANDS #

    def node(self):
        """get the node of the SceneViewer

        :return: the node of the SceneViewer
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # return
        return cgp_houdini_utils.scene.node(self.houPaneTab().currentNode())

    def setNode(self, node):
        """set the node of the SceneViewer

        :param node: the node of the SceneViewer
        :type node: :class:`cgp_houdini_utils.scene.Node`
        """

        # return
        return self.houPaneTab().setCurrentNode(node.houNode())

    def setViewerState(self, viewerState):
        """set the viewer state of the SceneViewer

        :param viewerState: the viewer state to set or its name
        :type viewerState: :class:`cgp_houdini_utils.ui.BaseState` or str
        """

        # init
        name = viewerState if isinstance(viewerState, str) else viewerState.name()

        # enter view state
        if name in cgp_houdini_utils.constants.BuiltInState.VIEWS:
            self.houPaneTab().enterViewState()

        # enter rotate state
        elif name == cgp_houdini_utils.constants.BuiltInState.ROTATE:
            self.houPaneTab().enterRotateToolState()

        # enter scale state
        elif name == cgp_houdini_utils.constants.BuiltInState.SCALE:
            self.houPaneTab().enterScaleToolState()

        # enter translate state
        elif name == cgp_houdini_utils.constants.BuiltInState.TRANSLATE:
            self.houPaneTab().enterTranslateToolState()

        # enter node state
        else:
            self.houPaneTab().setCurrentState(name, generate=hou.stateGenerateMode.Enter, request_new_on_generate=False)

    def viewerState(self):
        """get the viewer state of the SceneViewer

        :return: the viewer state of the SceneViewer
        :rtype: :class:`cgp_houdini_utils.ui.ViewerState`
        """

        # return
        return cgp_houdini_utils.ui._api.viewerState(self.houPaneTab().currentState())
