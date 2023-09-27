"""
numeric parameter widget library
"""


# imports local
import cgp_houdini_utils.constants
from . import _generic


# PARAMETER WIDGET OBJECT #


class NumericParameterWidget(_generic.ParameterWidget):
    """parameter widget object that manipulates any kind of numeric parameter widget
    """

    # ATTRIBUTES #

    _WHEEL_INCREMENT = 1

    # INIT #

    def _setupConnections(self):
        """setup the signal connections
        """

        # init
        super(NumericParameterWidget, self)._setupConnections()

        # execute
        dataWidget = self.dataWidget()
        dataWidget.wheelUpTriggered.connect(lambda: self._increment(self._WHEEL_INCREMENT))
        dataWidget.wheelDownTriggered.connect(lambda: self._increment(-self._WHEEL_INCREMENT))

    # PROTECTED COMMANDS #

    def _increment(self, increment):
        """increment the value of the NumericParameterWidget

        :param increment: the increment amount
        :type increment: float
        """

        # execute
        self.setValue(self._DATA_TYPE(self.value()) + increment)

        # sync
        self._syncWidgetToParameter()


class FloatParameterWidget(NumericParameterWidget):
    """numeric parameter widget object that manipulates a ``float`` parameter widget
    """

    # ATTRIBUTES #

    _PARAMETER_TYPE = cgp_houdini_utils.constants.ParameterType.FLOAT
    _DATA_TYPE = float
    _WHEEL_INCREMENT = 0.1


class IntParameterWidget(NumericParameterWidget):
    """numeric parameter widget object that manipulates a ``int`` parameter widget
    """

    # ATTRIBUTES #

    _PARAMETER_TYPE = cgp_houdini_utils.constants.ParameterType.INT
    _DATA_TYPE = int
