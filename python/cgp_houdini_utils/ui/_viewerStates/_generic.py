"""
generic viewer state library
"""

# imports third-parties
import hou

# import local
import cgp_houdini_utils.constants
from . import _base
from . import _builtIn


# GENERIC VIEWER STATE OBJECTS #


class NodeState(_base.BaseNodeState):
    """viewer state object that manipulates any kind of node viewer state
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ViewerStateType.NODE
    BUILT_IN_STATE_NAME = None
    DESCRIPTION = None
    HUD_TEMPLATE = None
    ICON = cgp_houdini_utils.constants.BuiltInIcon.PYTHON
    LABEL = None
    NAME = NotImplemented
    NODE_CATEGORY = NotImplemented

    # INIT #

    def __init__(self, *args, **kwargs):
        """initialization of the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'state_name': str,
                           'scene_viewer': `hou.SceneViewer`}
        """

        # init
        super(NodeState, self).__init__(*args, **kwargs)
        self._houRootNode = None
        self._houNode = None
        self._builtInStateModule = None
        self._builtInState = None

        # init running state
        if self.houSceneViewer():

            # init built in state
            if self.BUILT_IN_STATE_NAME:
                builtIn = cgp_houdini_utils.ui._api.viewerState(self.BUILT_IN_STATE_NAME)
                self._builtInStateModule = builtIn._builtInModule()
                self._builtInState = builtIn.houClass()(*args, **kwargs)

            # generate hud
            self.setHudInfo(template=self.hudTemplate())

    def __getattr__(self, attribute):
        """access the base class commands if they are not overwritten

        :param attribute: the attribute to get
        :type attribute: python
        """

        # return
        if hasattr(self._builtInState, attribute):
            return getattr(self._builtInState, attribute)

        # error
        raise AttributeError('{} has no attribute \'{}\''.format(self, attribute))

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, name=None, label=None, icon=None):
        """create a NodeState

        :param name: the name of the viewer state
        :type name: str

        :param label: the label of the viewer state
        :type label: str

        :param icon: the icon of the viewer state
        :type icon: str

        :return: the NodeState
        :rtype: :class:`cgp_houdini_utils.ui.NodeState`
        """

        # init
        name = name or cls.NAME

        # error
        if hou.ui.isRegisteredViewerState(name):
            raise ValueError('Viewer state named \'{}\' already exists'.format(name))

        # register
        template = cls.houTemplate(name=name, label=label, icon=icon)
        hou.ui.registerViewerState(template)

        # return
        return cgp_houdini_utils.ui._api.viewerState(name)

    @classmethod
    def houTemplate(cls, name=None, label=None, icon=None, isFactoryBound=True):
        """get the hou.ViewerStateTemplate object of the NodeSate

        :param name: the name of the viewer state
        :type name: str

        :param label: the label of the viewer state
        :type label: str

        :param icon: the icon of the viewer state
        :type icon: str

        :param isFactoryBound: ``True`` : the template will be returned with a bound factory -
                               ``False`` : the template will be returned without a bound factory
        :type isFactoryBound: bool

        :return: the houdini viewer state template of the NodeSate
        :rtype: :class:`hou.ViewerStateTemplate`
        """

        # init
        name = name or cls.NAME
        label = label or cls.LABEL or name
        icon = icon or cls.ICON

        # get template
        if cls.BUILT_IN_STATE_NAME:
            builtInState = cgp_houdini_utils.ui._api.viewerState(cls.BUILT_IN_STATE_NAME)
            if not isinstance(builtInState, _builtIn.BuiltInNodeState):
                raise ValueError('Viewer state named \'{}\' is not a built-in state'.format(cls.BUILT_IN_STATE_NAME))
            template = builtInState.houTemplate(name=name, label=label, icon=icon, isFactoryBound=False)
        else:
            template = hou.ViewerStateTemplate(name, label, cls.NODE_CATEGORY)
            template.bindIcon(icon)

        # bind factory
        # note: only one factory can be bound to the template, future factory binding to this object will have no effect
        if isFactoryBound:
            template.bindFactory(cls)

        # return
        return template

    # COMMANDS #

    def delete(self):
        """delete (unregister) the NodeState
        """

        # execute
        hou.ui.unregisterViewerState(self.name())

    def houNode(self):
        """get the hou.Node object that is manipulated by the NodeSate

        :return: the hou.Node object that is manipulated by the NodeSate
        :rtype: :class:`hou.Node`
        """

        # return
        return self._houNode

    def houRootNode(self):
        """get the hou.Node object that triggered the the NodeSate

        :return: the hou.Node object that triggered the the NodeSate
        :rtype: :class:`hou.Node`
        """

        # return
        return self._houRootNode

    def hudTemplate(self):
        """get the HUD template of the NodeState

        :return: the HUD template of the NodeState
        :rtype: dict
        """

        # return the specific template
        if self.HUD_TEMPLATE:
            return self.HUD_TEMPLATE

        # get the default template
        template = (self._builtInState.HUD_TEMPLATE.copy()
                    if hasattr(self._builtInState, 'HUD_TEMPLATE')
                    else {'rows': []})

        # update template values
        template.update({'title': self.label(), 'desc': self.DESCRIPTION, 'icon': self.ICON})

        # return
        return template

    def icon(self):
        """get the icon of the NodeState

        :return: the icon of the NodeState
        :rtype: str
        """

        # return
        return self.ICON if self.ICON else self.houViewerState().icon()

    def label(self):
        """get the label of the NodeState

        :return: the label of the NodeState
        :rtype: str
        """

        # return based on class attribute
        if self.LABEL:
            return self.LABEL

        # return based on registered state
        description = self.houViewerState().description()
        if description:
            return description

        # return generic
        return self.name().replace('_', ' ').title()

    def onBeginHandleToState(self, kwargs):
        """callback when a handle modification has started on the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'handle': `str`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'ui_event': `hou.UIEvent`}
        """

        # execute
        self._builtInStateExecute('onBeginHandleToState', kwargs)

    def onCommand(self, kwargs):
        """callback when a custom commands is called on the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'command': `str`
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'command_args': `dict`}

        :return: the command result
        :rtype: any
        """

        # execute command from this instance
        if hasattr(self, kwargs['command']):
            return getattr(self, kwargs['command'])(kwargs['command_args'])

        # return
        return self._builtInStateExecute('onCommand', kwargs)

    def onDragTest(self, kwargs):
        """callback when data is dragged on the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}

        :return: ``True`` : accept the dragged data - ``False`` : reject the dragged data
        :rtype: bool
        """

        # return
        return self._builtInStateExecute('onDragTest', kwargs, default=True)

    def onDraw(self, kwargs):
        """callback when rendering the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'draw_handle': `int`,
                           'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onDraw', kwargs)

    def onDrawInterrupt(self, kwargs):
        """callback when the draw is interrupted on the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'draw_handle': `int`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onDrawInterrupt', kwargs)

    def onDropAccept(self, kwargs):
        """callback when data is dropped on the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'drop_selection': `str`}

        :return: ``True`` : accept the dropped data - ``False`` : reject the dropped data
        :rtype: bool
        """

        # return
        return self._builtInStateExecute('onDropAccept', kwargs, default=True)

    def onDropGetOptions(self, kwargs):
        """build a list of drop options when data is dropped on the NodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'drop_options': `dict`,
                           'state_name': `str`,
                           'state_parms': `dict`}
        """

        # execute
        self._builtInStateExecute('onDropGetOptions', kwargs)

    def onEndHandleToState(self, kwargs):
        """callback when a handle modification has ended

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'handle': `str`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'ui_event': `hou.UIEvent`}
        """

        # execute
        self._builtInStateExecute('onEndHandleToState', kwargs)

    def onEnter(self, kwargs):
        """callback when the NodeState starts

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}
        """

        # init
        self._houRootNode = kwargs['node']
        self._houNode = self._initializeHouNode()

        # execute
        self._builtInStateExecute('onEnter', kwargs)

    def onExit(self, kwargs):
        """callback when the NodeState terminates

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onExit', kwargs)

    def onGenerate(self, kwargs):
        """callback when a nodeless NodeState starts

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onGenerate', kwargs)

    def onHandleToState(self, kwargs):
        """callback when a handle is modified

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'handle': `str`,
                           'state_flags': `dict`,
                           'prev_parms': `dict`,
                           'state_parms': `dict`,
                           'mod_parms': `list`,
                           'parms': `dict`,
                           'ui_event': `hou.UIEvent`}
        """

        # execute
        self._builtInStateExecute('onHandleToState', kwargs)

    def onInterrupt(self, kwargs):
        """callback when the NodeState is interrupted (e.g when the mouse moves outside the viewport)

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'interrupt_state': `str`,
                           'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onInterrupt', kwargs)

    def onKeyEvent(self, kwargs):
        """callback when a keyboard event is triggered

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'ui_event': `hou.ViewerEvent`}

        :return: ``True`` : the event has to be consumed - ``False`` : the event has not to be consumed
        :rtype: bool
        """

        # return
        return self._builtInStateExecute('onKeyEvent', kwargs, default=False)

    def onKeyTransitEvent(self, kwargs):
        """callback when a transitory key event is triggered

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'ui_event': `hou.ViewerEvent`}

        :return: ``True`` : the event has to be consumed - ``False`` : the event has not to be consumed
        :rtype: bool
        """

        # return
        return self._builtInStateExecute('onKeyTransitEvent', kwargs, default=False)

    def onMenuAction(self, kwargs):
        """callback when a menu item has been selected

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'menu_item': `str`,
                           'state_name': `str`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'ui_event': `hou.ViewerEvent`}
        """

        # execute
        self._builtInStateExecute('onMenuAction', kwargs)

    def onMenuPreOpen(self, kwargs):
        """callback to update the menu content before it is drawn

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'menu_states': `dict`,
                           'menu': `str`,
                           'state_name': `str`,
                           'state_parms': `dict`,
                           'menu_item_states': `dict`,
                           'ui_event': `hou.ViewerEvent`}
        """

        # execute
        self._builtInStateExecute('onMenuPreOpen', kwargs)

    def onMouseEvent(self, kwargs):
        """callback when a mouse event is triggered

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'ui_event': `hou.ViewerEvent`}

        :return: ``True`` : the event has to be consumed - ``False`` : the event has not to be consumed
        :rtype: bool
        """

        # return
        return self._builtInStateExecute('onMouseEvent', kwargs, default=False)

    def onMouseWheelEvent(self, kwargs):
        """callback when a mouse wheel event is triggered

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`,
                           'ui_event': `hou.ViewerEvent`}

        :return: ``True`` : the event has to be consumed - ``False`` : the event has not to be consumed
        :rtype: bool
        """

        # return
        return self._builtInStateExecute('onMouseWheelEvent', kwargs, default=False)

    def onParmChangeEvent(self, kwargs):
        """callback when a parameter has changed

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_name': `str`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'parm_value': `str`,
                           'parm_name': `str`,
                           'ui_event': `hou.ViewerEvent`}
        """

        # execute
        self._builtInStateExecute('onParmChangeEvent', kwargs)

    def onResume(self, kwargs):
        """callback when an interrupted NodeState resumes

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'interrupt_state': `str`,
                           'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onResume', kwargs)

    def onSelection(self, kwargs):
        """callback when a selector has selected something

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'selection': `hou.GeometrySelection`,
                           'name': `str`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'state_name': `str`}

        :return: ``True`` : accept the selection - ``False`` : reject the selection
        :rtype: bool
        """

        # return
        return self._builtInStateExecute('onSelection', kwargs, default=False)

    def onStartSelection(self, kwargs):
        """callback when a bound selector has been started

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'name': `str`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onStartSelection', kwargs)

    def onStateToHandle(self, kwargs):
        """handle action callback when a state node parameter is modified

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'parms': `dict`,
                           'state_parms': `dict`,
                           'handle': `str`}
        """

        # execute
        self._builtInStateExecute('onStateToHandle', kwargs)

    def onStopSelection(self, kwargs):
        """callback when a bound selector has been terminated

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'node': `hou.Node`,
                           'state_flags': `dict`,
                           'state_parms': `dict`,
                           'name': `str`,
                           'state_name': `str`}
        """

        # execute
        self._builtInStateExecute('onStopSelection', kwargs)

    def sceneViewer(self):
        """get the scene viewer of the NodeState

        :return: the scene viewer of the NodeState
        :rtype: :class:`cgp_houdini_utils.ui.SceneViewer`
        """

        # return
        return cgp_houdini_utils.ui._api.paneTab(self.houSceneViewer())

    def setHudInfo(self, template=None, rowsValues=None):
        """set the HUD info

        :param template: the hud template - default is class hud template
        :type template: dict

        :param rowsValues: the row values - default is class rows values
        :type rowsValues: list[dict]
        """

        # init
        sceneViewer = self.houSceneViewer()

        if template is not None:
            sceneViewer.hudInfo(template=template)

        if rowsValues is not None:
            sceneViewer.hudInfo(values=rowsValues)

    # PROTECTED COMMANDS #

    def _builtInStateExecute(self, command, kwargs, default=None):
        """execute the given command according to the base state behavior

        :param command: the name of the command to execute
        :param command: str

        :param kwargs: the kwargs of the command to execute
        :param kwargs: dict

        :param default: the default result in case the base state does not have the command implemented
        :param default: any

        :return: the command result
        :rtype: any
        """

        # if built-in state process exists
        if self._builtInState and hasattr(self._builtInState, command):

            # update manipulated node
            if 'node' in kwargs:
                kwargs['node'] = self.houNode()

            # return built-in
            return getattr(self._builtInState, command)(kwargs)

        # return default
        return default

    def _builtInStateModule(self):
        """get the python module containing the built-in state of the NodeState

        :return: the python module containing the built-in state of the NodeState
        :rtype: module
        """

        # return
        return (cgp_houdini_utils.ui._api.viewerState(self.BUILT_IN_STATE_NAME)._builtInModule()
                if self.BUILT_IN_STATE_NAME
                else None)

    def _initializeHouNode(self):
        """initialize the actual houdini node manipulated by the NodeSate

        :return: the actual houdini node manipulated by the NodeSate
        :rtype: :class:`hou.Node`
        """

        # return
        return self.houRootNode()
