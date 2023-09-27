"""
combobox sub widget library
"""

# imports third-parties
import PySide2.QtCore
import PySide2.QtWidgets
import hou


# SUB WIDGET OBJECT #


class ComboBox(PySide2.QtWidgets.QComboBox):
    """sub widget object that manipulates a ``ComboBox`` sub widget
    """

    # SIGNALS #

    editingFinished = PySide2.QtCore.Signal()
    setAnimationKeyTriggered = PySide2.QtCore.Signal()
    deleteAnimationKeyTriggered = PySide2.QtCore.Signal()
    deleteAllAnimationKeysTriggered = PySide2.QtCore.Signal()

    # INIT

    def __init__(self, parent=None):
        """initialization of the ComboBox

        :param parent: the parent widget
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # super
        super(ComboBox, self).__init__(parent=parent)

        # edit combobox size
        self.setFixedHeight(hou.ui.scaledSize(20))
        self.setSizePolicy(PySide2.QtWidgets.QSizePolicy.Expanding, PySide2.QtWidgets.QSizePolicy.Preferred)

        # setup signal connections
        self._setupConnections()

    def _setupConnections(self):
        """setup the signal connections
        """

        self.activated.connect(lambda: self.editingFinished.emit())

    # COMMANDS #

    def setValue(self, value):
        """set the value of the ComboBox

        :param value: the value of the ComboBox
        :type value: str
        """

        # execute
        self.setCurrentText(str(value))

    def value(self):
        """get the value of the ComboBox

        :return: the value of the ComboBox
        :rtype: str
        """

        # return
        return self.currentText()
