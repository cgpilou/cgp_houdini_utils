"""
line edit sub widget library
"""

# imports third-parties
import PySide2.QtCore
import PySide2.QtGui
import PySide2.QtWidgets
import hdefereval

# import local
import cgp_houdini_utils.constants


# SUB WIDGET OBJECT #


class LineEdit(PySide2.QtWidgets.QLineEdit):
    """sub widget object that manipulates a ``LineEdit`` sub widget
    """

    # SIGNALS #

    setAnimationKeyTriggered = PySide2.QtCore.Signal()
    deleteAnimationKeyTriggered = PySide2.QtCore.Signal()
    deleteAllAnimationKeysTriggered = PySide2.QtCore.Signal()
    wheelUpTriggered = PySide2.QtCore.Signal()
    wheelDownTriggered = PySide2.QtCore.Signal()

    # INIT

    def __init__(self, parent=None):
        """initialization of the LineEdit

        :param parent: the parent widget
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # init
        super(LineEdit, self).__init__(parent=parent)
        self._hotkeyAssignations = {}

        # setup context menu
        self.setContextMenuPolicy(PySide2.QtCore.Qt.CustomContextMenu)
        parent = self.parent()
        if hasattr(parent, 'contextMenu'):
            self.customContextMenuRequested.connect(lambda click: parent.contextMenu().load(self.mapToGlobal(click)))

    # COMMANDS #

    def focusInEvent(self, event):
        """process triggered when the focus enter the widget

        :param event: the focus event
        :type event: :class:`PySide2.QtGui.QFocusEvent`
        """

        # super
        super(LineEdit, self).focusInEvent(event)

        # allow editing
        self.setReadOnly(False)

        # unset enter key hotkeys
        contextName = cgp_houdini_utils.constants.HotkeyContext.NETWORK_EDITOR
        for hotkey in cgp_houdini_utils.ui._api.hotkeys(contextNames=(contextName,), shortcuts=('Enter',)):
            self._hotkeyAssignations[hotkey] = hotkey.shortcuts()
            hotkey.setShortcuts(None)

    def focusOutEvent(self, event):
        """process triggered when the focus exit the widget

        :param event: the focus event
        :type event: :class:`PySide2.QtGui.QFocusEvent`
        """

        # super
        super(LineEdit, self).focusInEvent(event)

        # ends editing
        self.setReadOnly(True)
        self.editingFinished.emit()

        # reset enter key hotkeys
        for hotkey, shortcuts in self._hotkeyAssignations.items():
            hdefereval.executeDeferred(hotkey.setShortcuts, shortcuts)

    def keyPressEvent(self, event):
        """process triggered when a keyboard key is pressed and focus is in the widget

        :param event: the focus event
        :type event: :class:`PySide2.QtGui.QKeyEvent`
        """

        # default behavior
        super(LineEdit, self).keyPressEvent(event)

        # exit focus when enter key pressed
        # execute deferred to be sure the focus event will be triggered once Qt has finished with line edit editing
        if event.key() in (PySide2.QtCore.Qt.Key_Enter, PySide2.QtCore.Qt.Key_Return):
            hdefereval.executeDeferred(self.clearFocus)

    def setValue(self, value):
        """set the value of the LineEdit

        :param value: the value of the LineEdit
        :type value: str
        """

        # execute
        self.setText(str(value))
        self.setCursorPosition(0)

    def value(self):
        """get the value of the LineEdit

        :return: the value of the LineEdit
        :rtype: str
        """

        # return
        return self.text()

    def wheelEvent(self, event):
        """process triggered when the mouse wheel is triggered on the widget

        :param event: the wheel event
        :type event: :class:`PySide2.QtGui.QWheelEvent`
        """

        # wheel up event
        if event.angleDelta().y() > 0:
            self.wheelUpTriggered.emit()

        # wheel down event
        else:
            self.wheelDownTriggered.emit()


class AnimatableLineEdit(LineEdit):
    """sub widget object that manipulates a ``LineEdit`` sub widget of an animated parameter
    """

    def mouseReleaseEvent(self, event):
        """process triggered when the mouse click is released on the widget

        :param event: the mouse released event
        :type event: :class:`PySide2.QtGui.QMouseEvent`
        """

        # execute default behavior
        super(LineEdit, self).mouseReleaseEvent(event)

        # control+click should delete the animation key
        if event.modifiers() == PySide2.QtCore.Qt.ControlModifier:
            self.deleteAnimationKeyTriggered.emit()

        # alt+click should set the animation key
        elif event.modifiers() == PySide2.QtCore.Qt.AltModifier:
            self.setAnimationKeyTriggered.emit()
