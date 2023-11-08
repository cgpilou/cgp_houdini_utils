"""
houdini ui types library
"""

# GLOBALS #


DESKTOP_TYPES = {}
FLOATING_PANEL_TYPES = {}
HOTKEY_TYPES = {}
PANE_TAB_TYPES = {}
PANE_TYPES = {}
PARAMETERS_TYPES = {}
VIEWER_STATE_TYPES = {}
VISUALIZER_CATEGORIES = {}


# COMMANDS #


def paneTabType(houPaneTab):
    """get the type of the PaneTab

    :param houPaneTab: the houdini pane tab
    :type houPaneTab: :class:`hou.PaneTab`

    :return: the type of the PaneTab
    :rtype: :class:`cgp_houdini_utils.constants.PaneTabType`
    """

    # return
    return str(houPaneTab.type()).rsplit('.', 1)[-1]


def visualizerCategory(houVisualizer):
    """get the category of the Visualizer

    :param houVisualizer: the houdini visualizer
    :type houVisualizer: :class:`hou.ViewportVisualizer`

    :return: the category of the Visualizer
    :rtype: :class:`cgp_houdini_utils.constants.VisualizerCategory`
    """

    # return
    return str(houVisualizer.category()).rsplit('.', 1)[-1]


def registerViewerStateTypes(types):
    """register the viewer state types

    :param types: the types to register
    :type types: dict
    """

    # execute
    VIEWER_STATE_TYPES.update(types)


# PROTECTED COMMANDS #


def _registerDesktopTypes(types):
    """register desktop types

    :param types: the types to register
    :type types: dict
    """

    # execute
    DESKTOP_TYPES.update(types)


def _registerFloatingPanelTypes(types):
    """register floating panel types

    :param types: the types to register
    :type types: dict
    """

    # execute
    FLOATING_PANEL_TYPES.update(types)


def _registerHotkeyTypes(types):
    """register hotkey types

    :param types: the types to register
    :type types: dict
    """

    # execute
    HOTKEY_TYPES.update(types)


def _registerPaneTabTypes(types):
    """register pane tab types

    :param types: the types to register
    :type types: dict
    """

    # execute
    PANE_TAB_TYPES.update(types)


def _registerPaneTypes(types):
    """register pane types

    :param types: the types to register
    :type types: dict
    """

    # execute
    PANE_TYPES.update(types)


def _registerParameterTypes(types):
    """register parameter types

    :param types: the types to register
    :type types: dict
    """

    # execute
    PARAMETERS_TYPES.update(types)


def _registerVisualizerCategories(categories):
    """register visualizer categories

    :param categories: the categories to register
    :type categories: dict
    """

    # execute
    VISUALIZER_CATEGORIES.update(categories)
