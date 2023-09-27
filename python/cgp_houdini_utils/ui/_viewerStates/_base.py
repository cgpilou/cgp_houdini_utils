"""
base viewer state library
"""

# imports python
import json

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.ui._type


# BASE VIEWER STATE OBJECTS #


class BaseState(cgp_generic_utils.python.BaseObject):
    """base object that manipulates any kind of viewer state
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ViewerStateType.BASE

    # INIT #
    
    def __init__(self, *args, **kwargs):
        """initialization of the BaseState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'state_name': str,
                           'scene_viewer': `hou.SceneViewer`}
        """

        # init
        self.__name = kwargs['state_name']
        self.__houSceneViewer = kwargs['scene_viewer']

    def __repr__(self):
        """get the representation of the PaneTab

        :return: the representation of the PaneTab
        :rtype: str
        """

        # init
        template = self._representationTemplate(withVarArgs=False, withVarKwargs=False)
        kwargs = {'state_name': self.name(), 'scene_viewer': self.houSceneViewer()}

        # return
        return template.replace('()', '(**{!r})'.format(kwargs))

    # COMMANDS #

    def houSceneViewer(self):
        """get the hou.SceneViewer object of the BaseState

        :return: the scene viewer of the BaseState
        :rtype: :class:`hou.SceneViewer`
        """

        # return
        return self.__houSceneViewer

    def icon(self):
        """get the icon of the BaseState

        :return: the icon of the BaseState
        :rtype: str
        """

        # return
        return self.info()['Icon']

    def info(self):
        """get the info of the BaseState

        :return: the info of the BaseState
        :rtype: dict
        """

        # init
        name = self.name()

        # return
        return json.loads(hou.ui.viewerStateInfo([name]))[name]

    def label(self):
        """get the label of the BaseState

        :return: the label of the BaseState
        :rtype: str
        """

        # return
        return self.info()['Label']

    def name(self):
        """get the name of the BaseState

        :return: the name of the BaseState
        :rtype: str
        """

        # return
        return self.__name


class BaseNodeState(BaseState):
    """base object that manipulates any kind of node viewer state
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ViewerStateType.BASE_NODE

    # INIT #

    def __init__(self, *args, **kwargs):
        """initialization of the BaseNodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'state_name': str,
                           'scene_viewer': `hou.SceneViewer`}
        """

        # init
        super(BaseNodeState, self).__init__(*args, **kwargs)
        self.__houViewerState = self._initializeHouViewerState()

    # COMMANDS #

    def houViewerState(self):
        """get the hou.ViewerState object of the BaseNodeState

        :return: the houdini viewer state of the BaseNodeState
        :rtype: :class:`hou.ViewerState`
        """

        # return
        return self.__houViewerState

    def isActive(self):
        """check the activation status of the BaseNodeState

        :return: ``True`` : the BaseNodeState is active - ``False`` : the BaseNodeState is not active
        :rtype: bool
        """

        # init
        name = self.name()
        houSceneViewer = self.houSceneViewer()

        # collect scene viewers to query
        if houSceneViewer:
            sceneViewers = (houSceneViewer,)
        else:
            sceneViewerType = cgp_houdini_utils.constants.PaneTabType.SCENE_VIEWER
            sceneViewers = tuple(paneTab
                                 for paneTab in hou.ui.paneTabs()
                                 if cgp_houdini_utils.ui._type.paneTabType(paneTab) == sceneViewerType)

        # return
        for sceneViewer in sceneViewers:
            if sceneViewer.currentState() == name:
                return True
        return False

    def nodeType(self):
        """get the node type handled by the BaseNodeState

        :return: the node type handled by the BaseNodeState
        :rtype: :class:`hou.ViewerState`
        """

        # return
        return self.houViewerState().nodeType().name()

    def setActive(self, isActive):
        """check the activation status of the BaseNodeState

        :param isActive: ``True`` : activate the BaseNodeState - ``False`` : deactivate the BaseNodeState
        :type isActive: bool
        """

        # init
        houSceneViewer = self.houSceneViewer()

        # collect scene viewers to query
        if houSceneViewer:
            sceneViewers = (cgp_houdini_utils.ui._api.paneTab(houSceneViewer),)
        else:
            sceneViewerTypes = (cgp_houdini_utils.constants.PaneTabType.SCENE_VIEWER,)
            sceneViewers = cgp_houdini_utils.ui._api.paneTabs(types=sceneViewerTypes)

        # execute
        for sceneViewer in sceneViewers:
            if isActive:
                sceneViewer.setViewerState(self)
            else:
                sceneViewer.setViewerState(cgp_houdini_utils.constants.BuiltInState.VIEW)

    # PROTECTED COMMANDS #

    def _initializeHouViewerState(self):
        """initialize the houdini viewer state of the BaseNodeState

        :return: the houdini viewer state of the BaseNodeState
        :rtype: :class:`hou.ViewerState`
        """

        # return
        for nodeCategory in hou.nodeTypeCategories().values():
            for viewerType in (hou.stateViewerType.Scene, hou.stateViewerType.Compositor):
                for houViewerState in nodeCategory.viewerStates(viewerType):
                    if houViewerState.name() == self.name():
                        return houViewerState

        # error
        raise ValueError('No registered viewer states named: {}'.format(self.name()))
