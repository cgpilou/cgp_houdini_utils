"""
context menu sub widget library
"""

# imports third-parties
import PySide2.QtCore
import PySide2.QtWidgets
import hou

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.ui._api


# SUB WIDGET OBJECT #


class ContextMenu(PySide2.QtWidgets.QMenu):
    """sub widget object that manipulates a ``ContextMenu`` sub widget
    """

    # SIGNALS #

    setAnimationKeyTriggered = PySide2.QtCore.Signal()
    deleteAnimationKeyTriggered = PySide2.QtCore.Signal()
    deleteAllAnimationKeysTriggered = PySide2.QtCore.Signal()

    # INIT #

    def __init__(self, parameter, parent=None):
        """initialization of the ContextMenu

        :param parent: the parent of the ContextMenu
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(ContextMenu, self).__init__(parent=parent)
        self._parameter = parameter

        # show channel editors actor
        self._openChannelEditorAction = PySide2.QtWidgets.QAction('Open the Animation Editor', self)
        self.addAction(self._openChannelEditorAction)

        # separator
        self.addSeparator()

        # set anim key action
        self._setAnimationKeyAction = PySide2.QtWidgets.QAction('Set Animation Key', self)
        self.addAction(self._setAnimationKeyAction)

        # remove anim key action
        self._deleteAnimationKeyAction = PySide2.QtWidgets.QAction('Delete Current Animation Key', self)
        self.addAction(self._deleteAnimationKeyAction)

        # delete all anim keys action
        self._deleteAllAnimationKeysAction = PySide2.QtWidgets.QAction('Delete All Animation Keys', self)
        self.addAction(self._deleteAllAnimationKeysAction)

        # init connections
        self._setupConnections()

    def _setupConnections(self):
        """setup the connections of the ContextMenu
        """

        self._openChannelEditorAction.triggered.connect(self._openChannelEditor)
        self._setAnimationKeyAction.triggered.connect(self.setAnimationKeyTriggered.emit)
        self._deleteAnimationKeyAction.triggered.connect(self.deleteAnimationKeyTriggered.emit)
        self._deleteAllAnimationKeysAction.triggered.connect(self.deleteAllAnimationKeysTriggered.emit)

    # COMMANDS #

    def load(self, clickPosition):
        """load the ContextMenu

        :param clickPosition: the screen position of the click that queried the context menu
        :type clickPosition: :class:`PySide2.QtCore.QPoint`
        """

        # update status
        self._deleteAnimationKeyAction.setEnabled(self._parameter.hasAnimationKey(hou.frame()))
        self._deleteAllAnimationKeysAction.setEnabled(self._parameter.hasAnimationKey())

        # display the menu
        self.exec_(clickPosition)

    # PROTECTED COMMANDS #

    @staticmethod
    def _openChannelEditor():
        """open the channel editor
        """

        # get existing channel editors
        paneTabTypes = (cgp_houdini_utils.constants.PaneTabType.CHANNEL_EDITOR,)
        channelEditors = cgp_houdini_utils.ui._api.paneTabs(types=paneTabTypes)

        # create floating if none found
        if not channelEditors:
            hou.ui.curDesktop().createFloatingPaneTab(hou.paneTabType.ChannelEditor)
            return

        # show existing
        for channelEditor in channelEditors:
            channelEditor.pane().setActiveTab(channelEditor)
