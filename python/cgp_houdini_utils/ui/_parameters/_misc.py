"""
misc parameter widget library
"""

# imports local
import PySide2.QtWidgets

import cgp_houdini_utils.constants
import cgp_houdini_utils.ui._type
from . import _generic
from ._subWidgets import _comboBox


# PARAMETER WIDGET OBJECT #


class MenuParameterWidget(_generic.ParameterWidget):
    """parameter widget object that manipulates a ``Menu`` parameter widget
    """

    # ATTRIBUTES #

    _PARAMETER_TYPE = cgp_houdini_utils.constants.ParameterType.MENU
    _DATA_WIDGET_CLASS = _comboBox.ComboBox

    # INIT #

    def __init__(self, parameter, isLabelVisible=True, parent=None):
        """ParameterWidget class initialization

        :param parameter: the parameter controlled by this widget
        :type parameter: :class:`cgp_houdini_utils.scene.Parameter`

        :param isLabelVisible: ``True`` : the label is visible - ``False`` : the label is hidden
        :type isLabelVisible: :class:`PySide2.QtWidgets.QWidget`

        :param parent: the parent widget
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # super
        super(MenuParameterWidget, self).__init__(parameter, isLabelVisible=isLabelVisible, parent=parent)

        # add menu items
        self._dataWidget.addItems(self.parameter().labels())

        # setup values
        self._syncParameterToWidget()


class StringParameterWidget(_generic.ParameterWidget):
    """parameter widget object that manipulates a ``String`` parameter widget
    """

    # ATTRIBUTES #

    _PARAMETER_TYPE = cgp_houdini_utils.constants.ParameterType.STRING
