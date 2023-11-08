"""
numeric parameter library
"""

# import third-parties
import hou

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene._api
from . import _generic


# SPECIFIC PARAMETER OBJECTS #


class ButtonParameter(_generic.Parameter):
    """parameter object that manipulates a ``Button`` parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.BUTTON

    # COMMANDS #

    def execute(self, kwargs=None):
        """execute (press the action button of) the ButtonParameter

        :param kwargs: the keyword arguments for the execution process
        :type kwargs: dict
        """

        # init
        kwargs = kwargs or {}

        # execute
        self.houParm().pressButton(kwargs)


class DataParameter(_generic.Parameter):
    """parameter object that manipulates a ``Data`` parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.DATA

    # COMMANDS #

    def setValue(self, value):
        """set the value of the DataParameter

        :param value: the value to set to the DataParameter
        :type value: any
        """

        # check for geometry value
        if isinstance(value, cgp_houdini_utils.scene.GeometryItem):
            value = value.houGeometryItem()

        # execute
        super(DataParameter, self).setValue(value)

    def value(self, frame=None, isRaw=False):
        """get the value of the DataParameter

        :param frame: frame to get the value at
        :type frame: float

        :param isRaw: ``True`` : get the value of the parameter without evaluation or expansion -
                      ``False`` : get the value of the parameter when evaluated and expanded
        :type isRaw: bool

        :return: the value of the DataParameter
        :rtype: any
        """

        # execute
        value = super(DataParameter, self).value()

        # return geometry item
        if isinstance(value, (hou.Edge, hou.Geometry, hou.Point, hou.Primitive, hou.Vertex)):
            return cgp_houdini_utils.scene._api.geometryItem(value)

        # return
        return value


class FloatParameter(_generic.Parameter):
    """parameter object that manipulates a ``Float`` parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.FLOAT

    # COMMANDS #

    def value(self, frame=None, isRaw=False):
        """get the value of the FloatParameter

        :param frame: frame to get the value at
        :type frame: float

        :param isRaw: ``True`` : get the value of the parameter without evaluation or expansion -
                      ``False`` : get the value of the parameter when evaluated and expanded
        :type isRaw: bool

        :return: the value of the FloatParameter
        :rtype: float
        """

        # return the raw text value
        if isRaw:
            return self.houParm().rawValue()

        # return based on current frame
        if frame is None:
            return self.houParm().evalAsFloat()

        # return based on given frame
        return self.houParm().evalAsFloatAtFrame(frame)


class IntParameter(_generic.Parameter):
    """parameter object that manipulates a ``Int`` parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.INT

    # COMMANDS #

    def value(self, frame=None, isRaw=False):
        """get the value of the IntParameter

        :param frame: frame to get the value at
        :type frame: float

        :param isRaw: ``True`` : get the value of the parameter without evaluation or expansion -
                      ``False`` : get the value of the parameter when evaluated and expanded
        :type isRaw: bool

        :return: the value of the IntParameter
        :rtype: int
        """

        # return the raw text value
        if isRaw:
            return self.houParm().rawValue()

        # return based on current frame
        if frame is None:
            return self.houParm().evalAsInt()

        # return based on given frame
        return self.houParm().evalAsIntAtFrame(frame)


class MenuParameter(_generic.Parameter):
    """parameter object that manipulates a ``Menu`` parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.MENU

    # COMMANDS #

    def index(self, frame=None):
        """get the index of the MenuParameter

        :param frame: frame to get the value at - default is current frame
        :type frame: float

        :return: the index of the MenuParameter
        :rtype: int
        """

        # return based on current frame
        if frame is None:
            return self.houParm().evalAsInt()

        # return based on given frame
        return self.houParm().evalAsIntAtFrame(frame)

    def setIndex(self, index):
        """set the index of the MenuParameter

        :param index: the index of the MenuParameter
        :type index: int
        """

        # execute
        self.setValue(index)

    def value(self, frame=None, isRaw=False):
        """get the value of the MenuParameter

        :param frame: frame to get the value at
        :type frame: float

        :param isRaw: ``True`` : get the value of the parameter without evaluation or expansion -
                      ``False`` : get the value of the parameter when evaluated and expanded
        :type isRaw: bool

        :return: the value of the MenuParameter
        :rtype: str
        """

        # return the raw text value
        if isRaw:
            return self.houParm().rawValue()

        # return based on current frame
        if frame is None:
            return self.houParm().evalAsString()

        # return based on given frame
        return self.houParm().evalAsStringAtFrame(frame)


class StringParameter(_generic.Parameter):
    """parameter object that manipulates a ``String`` parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.STRING
    _REFERENCE_EXPRESSION_FUNCTION = 'chs'

    # COMMANDS #

    def value(self, frame=None, isRaw=False):
        """get the value of the StringParameter

        :param frame: frame to get the value at
        :type frame: float

        :param isRaw: ``True`` : get the value of the parameter without evaluation or expansion -
                      ``False`` : get the value of the parameter when evaluated and expanded
        :type isRaw: bool

        :return: the value of the StringParameter
        :rtype: str
        """

        # return the raw text value
        if isRaw:
            return self.houParm().rawValue()

        # return based on current frame
        if frame is None:
            return self.houParm().evalAsString()

        # return based on given frame
        return self.houParm().evalAsStringAtFrame(frame)


class ToggleParameter(_generic.Parameter):
    """parameter object that manipulates a ``Toggle`` parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.TOGGLE

    def value(self, frame=None, isRaw=False):
        """get the value of the ToggleParameter

        :param frame: frame to get the value at
        :type frame: float

        :param isRaw: ``True`` : get the value of the parameter without evaluation or expansion -
                      ``False`` : get the value of the parameter when evaluated and expanded
        :type isRaw: bool

        :return: the value of the ToggleParameter
        :rtype: bool
        """

        # get
        value = super(ToggleParameter, self).value(frame=frame, isRaw=False)

        # return boolean if possible
        if isinstance(value, str):
            if value == 'on':
                return True
            if value == 'off':
                return False
            return value
        return bool(value)
