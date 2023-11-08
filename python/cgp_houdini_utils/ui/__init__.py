"""
python objects and management functions to manipulate a variety of entities in the houdini ui
such as desktops, panels, hotkeys, viewer states...
"""


# IMPORTS #


import cgp_generic_utils.qt

from ._api import (application,
                   desktop,
                   desktops,
                   floatingPanel,
                   floatingPanels,
                   hotkey,
                   hotkeys,
                   pane,
                   panes,
                   paneTab,
                   paneTabs,
                   viewerState,
                   visualizer,
                   visualizers,
                   createParameterWidget,
                   createViewerStates,
                   createIconPixmap)

from ._type import (registerViewerStateTypes,
                    _registerDesktopTypes,
                    _registerFloatingPanelTypes,
                    _registerHotkeyTypes,
                    _registerPaneTabTypes,
                    _registerPaneTypes,
                    _registerParameterTypes,
                    _registerVisualizerCategories)

from ._application._application import HoudiniApplication

from ._misc._desktop import Desktop
from ._misc._floatingPanel import FloatingPanel
from ._misc._hotkey import (Hotkey,
                            HotkeyContext)
from ._misc._pane import Pane
from ._misc._visualizer import (Visualizer,
                                NodeVisualizer,
                                SceneVisualizer)

from ._paneTabs._generic import PaneTab
from ._paneTabs._channelEditor import ChannelEditor
from ._paneTabs._sceneViewer import SceneViewer

from ._parameters._generic import ParameterWidget
from ._parameters._misc import (MenuParameterWidget,
                                StringParameterWidget)
from ._parameters._numeric import (FloatParameterWidget,
                                   IntParameterWidget)

from ._viewerStates._base import (BaseState,
                                  BaseNodeState)
from ._viewerStates._builtIn import (BuiltInNodeState,
                                     BuiltInHdaState,
                                     BuiltInPyState)
from ._viewerStates._generic import NodeState
from ._viewerStates._sop import (SopState,
                                 StrokeState,
                                 AttributePaintState)


# COLLECT TYPES #


__desktopTypes = {cls._TYPE: cls
                  for cls in [Desktop]}

__floatingPanelTypes = {cls._TYPE: cls
                        for cls in [FloatingPanel]}

__hotkeyTypes = {cls._TYPE: cls
                 for cls in [Hotkey,
                             HotkeyContext]}

__paneTabTypes = {cls._TYPE: cls
                  for cls in [PaneTab,
                              ChannelEditor,
                              SceneViewer]}

__paneTypes = {cls._TYPE: cls
               for cls in [Pane]}

__parameterTypes = {cls._PARAMETER_TYPE: cls
                    for cls in [ParameterWidget,
                                FloatParameterWidget,
                                IntParameterWidget,
                                MenuParameterWidget,
                                StringParameterWidget]}

__specificViewerStateTypes = {cls.NAME: cls
                              for cls in [StrokeState,
                                          AttributePaintState]}

__genericViewerStateTypes = {cls._TYPE: cls
                             for cls in [BaseState,
                                         BaseNodeState,
                                         BuiltInNodeState,
                                         BuiltInHdaState,
                                         BuiltInPyState,
                                         NodeState]}

__visualizerCategories = {cls._CATEGORY: cls
                          for cls in [Visualizer,
                                      NodeVisualizer,
                                      SceneVisualizer]}


# REGISTER TYPES #


cgp_generic_utils.qt.registerApplicationType(HoudiniApplication)
_registerDesktopTypes(__desktopTypes)
_registerFloatingPanelTypes(__floatingPanelTypes)
_registerHotkeyTypes(__hotkeyTypes)
_registerPaneTabTypes(__paneTabTypes)
_registerPaneTypes(__paneTypes)
_registerParameterTypes(__parameterTypes)
_registerVisualizerCategories(__visualizerCategories)
registerViewerStateTypes(__specificViewerStateTypes)
registerViewerStateTypes(__genericViewerStateTypes)


# PUBLIC API #


__all__ = ['application',
           'desktop',
           'desktops',
           'floatingPanel',
           'floatingPanels',
           'hotkey',
           'hotkeys',
           'pane',
           'panes',
           'paneTab',
           'paneTabs',
           'viewerState',
           'visualizer',
           'visualizers',
           'createParameterWidget',
           'createViewerStates',
           'createIconPixmap',

           'registerViewerStateTypes',

           'HoudiniApplication',
           'ParameterWidget',
           'FloatParameterWidget',
           'IntParameterWidget',
           'MenuParameterWidget',
           'SopState',
           'StrokeState',
           'AttributePaintState',

           # Viewer States
           'BaseState',
           'BaseNodeState',
           'BuiltInNodeState',
           'BuiltInHdaState',
           'BuiltInPyState',
           'NodeState',
           'SopState',
           'StrokeState',
           'AttributePaintState',

           # Visualizers
           'Visualizer',
           'NodeVisualizer',
           'SceneVisualizer']
