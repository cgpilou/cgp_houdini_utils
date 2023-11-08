"""
houdini ui api
"""

# imports third-parties
import hou
import json

# imports local
import cgp_houdini_utils.constants
import cgp_generic_utils.qt
from . import _type

import os
import zipfile
import PySide2.QtCore
import PySide2.QtSvg
import PySide2.QtGui


# APPLICATION #


def application():
    """get the application

    :return: the application
    :rtype: :class:`cgp_houdini_utils.ui.HoudiniApplication`
    """

    # return
    return cgp_generic_utils.qt.application()


# DESKTOP #


def desktop(desktop_=None):
    """get a Desktop object

    :param desktop_: the desktop to get or its name - default is current desktop
    :type desktop_: :class:`hou.Desktop` or str

    :return: the Desktop object
    :rtype: :class:`cgp_houdini_utils.ui.Desktop`
    """

    # init
    houDesktop = (hou.ui.curDesktop()
                  if desktop_ is None
                  else desktop_
                  if isinstance(desktop_, hou.Desktop)
                  else hou.ui.desktop(desktop_))

    # return
    return _type.DESKTOP_TYPES[cgp_houdini_utils.constants.DesktopType.GENERIC](houDesktop)


def desktops():
    """get the Desktop objects

    :return: the Desktop objects
    :rtype: tuple[:class:`cgp_houdini_utils.ui.Desktop`]
    """

    # return
    return tuple(desktop(houDesktop) for houDesktop in hou.ui.desktops())


# FLOATING PANEL #


def floatingPanel(floatingPanel_):
    """get a FloatingPanel object

    :param floatingPanel_: the floating panel to get or its name
    :type floatingPanel_: :class:`hou.FloatingPanel` or str

    :return: the FloatingPanel object
    :rtype: :class:`cgp_houdini_utils.ui.FloatingPanel`
    """

    # init
    cls = _type.FLOATING_PANEL_TYPES[cgp_houdini_utils.constants.FloatingPanelType.GENERIC]

    # return
    if isinstance(floatingPanel_, hou.FloatingPanel):
        return cls(floatingPanel_)

    # get houdini floating panel from name
    floatingPanels_ = tuple(available
                            for available in hou.ui.floatingPanels()
                            if available.name() == floatingPanel_)

    # errors
    if not floatingPanels_:
        raise ValueError('No floating panel named: {}'.format(floatingPanel_))
    if len(floatingPanels_) > 1:
        raise ValueError('Floating panel named "{}" is not unique'.format(floatingPanel_))

    # return
    return cls(floatingPanels_[0])


def floatingPanels(desktop_=None):
    """get the floating panels

    :param desktop_: the desktop containing the floating panels - default is to get currently opened floating panels
    :type desktop_: :class:`hou.Desktop` or str

    :return: the floating panels
    :rtype: tuple[:class:`cgp_houdini_utils.ui.FloatingPanel`]
    """

    # init
    floatingPanels_ = desktop(desktop_).floatingPanels() if desktop_ else hou.ui.floatingPanels()

    # return
    return tuple(floatingPanel(floatingPanel_) for floatingPanel_ in floatingPanels_)


# HOTKEY #


def hotkey(name):
    """get an hotkey

    :param name: the name of the hotkey
    :type name: str

    :return: the hotkey
    :rtype: :class:`cgp_houdini_utils.ui.Hotkey`
    """

    # error
    if '.' not in name:
        raise ValueError('Invalid hotkey name: {}'.format(name))

    # init
    contextName = name.rsplit('.', 1)[0]
    availableNames = tuple(data['symbol'] for data in hou.hotkeys().commandsInContext(contextName))

    # error
    if name not in availableNames:
        raise ValueError('No hotkey named: {}'.format(name))

    # return
    return _type.HOTKEY_TYPES[cgp_houdini_utils.constants.HotkeyType.HOTKEY](name)


def hotkeys(contextNames=None, shortcuts=None):
    """get hotkeys

    :param contextNames: the names of the contexts to find hotkeys in
    :type contextNames: tuple[str]

    :param shortcuts: the shortcuts assigned to the desired hotkeys
    :type shortcuts: tuple[str]

    :return: the hotkeys
    :rtype: tuple(:class:`cgp_houdini_utils.ui.Hotkey`)
    """

    # init
    contextNames = contextNames or ('h',)
    contexts = set()

    # get contexts
    for contextName in contextNames:
        context = _type.HOTKEY_TYPES[cgp_houdini_utils.constants.HotkeyType.CONTEXT](contextName)
        contexts.update((context,) + context.children(isRecursive=True))

    # return
    return tuple(hotkey_
                 for context in contexts
                 for hotkey_ in context.hotkeys()
                 if shortcuts is None
                 or list(set(hotkey_.shortcuts()) & set(shortcuts)))


# PANE #


def pane(pane_):
    """get a pane

    :param pane_: the pane to get or its name
    :type pane_: :class:`hou.Pane` or str

    :return: the pane
    :rtype: :class:`cgp_houdini_utils.ui.Pane`
    """

    # init
    houPane = pane_ if isinstance(pane_, hou.Pane) else hou.ui.findPane(pane_)

    # error
    if not houPane:
        raise ValueError('No pane named: {}'.format(pane_))

    # return
    return _type.PANE_TYPES[cgp_houdini_utils.constants.PaneType.GENERIC](houPane)


def panes(desktop_=None):
    """get the panes

    :param desktop_: the desktop containing the panes - default is current desktop
    :type desktop_: :class:`hou.Desktop` or str

    :return: the panes
    :rtype: tuple[:class:`cgp_houdini_utils.ui.Pane`]
    """

    # init
    desktopPanes = tuple(pane_ for pane_ in desktop(desktop_).panes())
    floatingPanes = tuple(pane_
                          for floatingPanel_ in floatingPanels(desktop_=desktop_)
                          for pane_ in floatingPanel_.panes())

    # return
    return desktopPanes + floatingPanes


# PANE TABS #


def paneTab(paneTab_):
    """get a pane tab

    :param paneTab_: the pane tab to get or its name
    :type paneTab_: :class:`hou.PaneTab` or str

    :return: the pane tab
    :rtype: :class:`cgp_houdini_utils.ui.PaneTab`
    """

    # init
    houPaneTab = paneTab_ if isinstance(paneTab_, hou.PaneTab) else hou.ui.findPaneTab(paneTab_)

    # error
    if not houPaneTab:
        raise ValueError('No pane tab named: {}'.format(paneTab_))

    # get type
    paneTabType = _type.paneTabType(houPaneTab)
    genericType = cgp_houdini_utils.constants.PaneTabType.GENERIC

    # return
    return _type.PANE_TAB_TYPES.get(paneTabType, _type.PANE_TAB_TYPES[genericType])(houPaneTab)


def paneTabs(types=None):
    """get the pane tabs

    :param types: the types of the desired pane tabs
    :type types: tuple[:class:`cgp_houdini_utils.constants.PaneTabType`]

    :return: the pane tabs
    :rtype: tuple[:class:`cgp_houdini_utils.ui.PaneTabs`],
            tuple[:class:`cgp_houdini_utils.ui.ChannelEditor`],
            tuple[:class:`cgp_houdini_utils.ui.SceneViewer`]
    """

    # return
    return tuple(paneTab_
                 for pane_ in panes()
                 for paneTab_ in pane_.tabs()
                 if not types or paneTab_.type_() in types)


# VIEWER STATE #


def viewerState(viewerState_, sceneViewer=None):
    """get a viewer state

    :param viewerState_: the houdini viewer state to get or its name
    :type viewerState_: str or :class:`hou.ViewerState`

    :param sceneViewer: the scene viewer containing the viewer state
    :type sceneViewer: :class:`hou.SceneViewer`

    :return: the registered viewer state
    :rtype: :class:`cgp_houdini_utils.ui.RunningState`
    """

    # init
    name = viewerState_.name() if isinstance(viewerState_, hou.ViewerState) else viewerState_
    kwargs = {'state_name': name, 'scene_viewer': sceneViewer}

    # error
    if not hou.ui.isRegisteredViewerState(name):
        ValueError('Unknown viewer state named: {}'.format(name))

    # viewer states from our API
    if name in _type.VIEWER_STATE_TYPES:
        return _type.VIEWER_STATE_TYPES[name](**kwargs)

    # built-in viewer states
    stateInfo = json.loads(hou.ui.viewerStateInfo((name,)))

    if stateInfo:

        # py file based
        if stateInfo[name]['Source'].endswith('.py'):
            type_ = cgp_houdini_utils.constants.ViewerStateType.BUILT_IN_PY

        # hda embedded
        elif stateInfo[name]['Source'].endswith('.hda'):
            type_ = cgp_houdini_utils.constants.ViewerStateType.BUILT_IN_HDA

        # generic built-in state
        else:
            type_ = cgp_houdini_utils.constants.ViewerStateType.BUILT_IN

    # unknown states
    else:

        # generic node state
        if _houViewerState(name):
            type_ = cgp_houdini_utils.constants.ViewerStateType.BASE_NODE

        # generic state
        else:
            type_ = cgp_houdini_utils.constants.ViewerStateType.BASE

    # return
    return _type.VIEWER_STATE_TYPES[type_](**kwargs)


def createViewerStates(names=None, isForce=False):
    """create (register) viewer states

    :param names: the names of the viewer states to create
    :type names: tuple[str]

    :param isForce: ``True`` : only the un registered states will be registered -
                    ``False`` : the already registered states will be unregistered then re-registered
    :type isForce: bool
    """

    # init
    names = (names
             or tuple(name
                      for name in _type.VIEWER_STATE_TYPES.keys()
                      if name not in cgp_houdini_utils.constants.ViewerStateType.all()))
    viewerStateTypes = {name: cls
                        for name, cls in _type.VIEWER_STATE_TYPES.items()
                        if name in names}

    # loop over our running state types
    for name, cls in viewerStateTypes.items():

        # unregister or bypass already registered state
        if hou.ui.isRegisteredViewerState(name):
            if isForce:
                hou.ui.unregisterViewerState(name)
            else:
                continue

        # register state
        cls.create()


# VISUALIZERS #


def visualizer(visualizer_):
    """get a Visualizer object

    :param visualizer_: the visualizer to get
    :type visualizer_: :class:`hou.ViewportVisualizer`

    :return: the Visualizer object
    :rtype: :class:`cgp_houdini_utils.ui.Visualizer`
    """

    # init
    category = _type.visualizerCategory(visualizer_)

    # return
    return _type.VISUALIZER_CATEGORIES[category](visualizer_)


def visualizers(categories=None, node=None):
    """get the Visualizer objects

    :param categories: the categories of the visualizers to get - default is all categories
    :type categories: tuple[:class:`cgp_houdini_utils.constants.VisualizerCategory`]

    :param node: the node of the visualizers to get if category is ``Node`` - has to be None otherwise
    :type node: :class:`hou.Node`

    :return: the Visualizer objects
    :rtype: tuple[:class:`cgp_houdini_utils.ui.Visualizer`]
    """

    # init
    houVisualizers = tuple()
    categoryMap = {cgp_houdini_utils.constants.VisualizerCategory.COMMON: hou.viewportVisualizerCategory.Common,
                   cgp_houdini_utils.constants.VisualizerCategory.NODE: hou.viewportVisualizerCategory.Node,
                   cgp_houdini_utils.constants.VisualizerCategory.SCENE: hou.viewportVisualizerCategory.Scene}
    categories = categories or cgp_houdini_utils.constants.VisualizerCategory.all()

    # collect visualizers
    for category in categories:
        category = categoryMap[category]
        if category != hou.viewportVisualizerCategory.Node:
            houVisualizers += hou.viewportVisualizers.visualizers(category=category)
        elif node:
            houVisualizers += hou.viewportVisualizers.visualizers(category=category, node=node)

    # return
    return tuple(visualizer(houVisualizer) for houVisualizer in houVisualizers)


# PARAMETERS #


def createParameterWidget(parameter_, parent):
    """create a qt parameter widget manipulating the given parameter

    :param parameter_: the parameter associated to the qt widget
    :type parameter_: :class:`cgp_houdini_utils.scene.Parameter`

    :param parent: the parent widget
    :type parent: :class:`PySide2.QtWidgets.QWidget`

    :return : the parameter widget manipulating the given parameter
    :rtype: :class:`cgp_houdini_utils.ui.ParameterWidget`
    """

    # init
    parameterType = parameter_.type_()

    # return
    return (_type.PARAMETERS_TYPES[parameterType](parameter_, parent=parent)
            if parameterType in _type.PARAMETERS_TYPES
            else _type.PARAMETERS_TYPES[cgp_houdini_utils.constants.ParameterType.GENERIC](parameter_,
                                                                                           parent=parent))


# ICONS #


def createIconPixmap(name, size=64):
    """create an icon pixmap of an internal houdini icon

    :param name: the name of the icon
    :type name: str

    :param size: the size (in pixels) of the icon
    :type size: int

    :return: the icon pixmap of an internal houdini icon
    :rtype: :class:`PySide2.QtGui.QPixmap`
    """

    # init
    pixmap = None
    hfs = hou.getenv('HFS')
    iconLibPath = os.path.join(hfs, 'houdini', 'config', 'Icons', 'icons.zip')

    # open zip file
    iconLibFile = zipfile.ZipFile(iconLibPath, 'r')

    # parse zip file
    for iconFilePath in iconLibFile.namelist():

        # get file info
        fileName, extension = os.path.splitext(iconFilePath)

        # ignore non svg files
        if extension != '.svg':
            continue

        # ignore not matching names
        if name not in (fileName, fileName.replace(os.sep, '_')):
            continue

        # retrieve svg data
        iconSvg = PySide2.QtSvg.QSvgRenderer(PySide2.QtCore.QByteArray(iconLibFile.read(iconFilePath)))
        if not iconSvg.isValid():
            continue

        # create a transparent image
        image = PySide2.QtGui.QImage(size, size, PySide2.QtGui.QImage.Format_ARGB32)
        image.fill(PySide2.QtCore.Qt.transparent)

        # paint svg in image
        painter = PySide2.QtGui.QPainter(image)
        iconSvg.render(painter)

        # get pixmap
        pixmap = PySide2.QtGui.QPixmap.fromImage(image, PySide2.QtCore.Qt.NoFormatConversion)

        # exit loop
        break

    # close zip file
    iconLibFile.close()

    # return
    return pixmap


# PROTECTED COMMANDS #


def _houViewerState(name):
    """get a houdini viewer state

    :param name: the name of the viewer state to get
    :type name: str

    :return: the houdini viewer state
    :rtype: :class:`hou.ViewerState`
    """

    # parse every existing viewer state
    for nodeTypeCategory in hou.nodeTypeCategories().values():
        for viewerType in (hou.stateViewerType.Scene, hou.stateViewerType.Compositor):
            for houViewerState in nodeTypeCategory.viewerStates(viewerType):

                # return the viewer state matching the given name
                if houViewerState.name() == name:
                    return houViewerState

    # return None if nothing found
    return None
