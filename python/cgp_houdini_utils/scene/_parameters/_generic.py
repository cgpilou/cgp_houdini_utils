"""
generic parameter library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.decorators
import cgp_houdini_utils.ui
import cgp_houdini_utils.scene._type
import cgp_houdini_utils.scene._api


# GENERIC PARAMETER OBJECTS #


class Parameter(cgp_generic_utils.python.BaseObject):
    """parameter object that manipulates any kind of parameter
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.GENERIC
    _REFERENCE_EXPRESSION_FUNCTION = 'ch'

    # INIT #

    def __init__(self, parameter):
        """initialization of the Parameter

        :param parameter: the houdini parameter or its path
        :type parameter: :class:`hou.Parm` or str
        """

        # init
        self._houParm = hou.parm(parameter) if isinstance(parameter, str) else parameter

    def __eq__(self, other):
        """check if an other Parameter is equal to the Parameter

        :param other: the other Parameter
        :type other: :class:`cgp_houdini_utils.scene.Parameter`

        :return: ``True`` : the two parameters are equal - ``False`` : the two parameters are not equal
        :rtype: bool
        """

        # return
        return self.houParm() == other.houParm() if isinstance(other, Parameter) else False

    def __ne__(self, other):
        """check if an other Parameter is not equal to the Parameter

        :param other: the other Parameter
        :type other: :class:`cgp_houdini_utils.scene.Parameter`

        :return: ``True`` : the two parameters are not equal - ``False`` : the two parameters are equal
        :rtype: bool
        """

        # return
        return self.houParm() != other.houParm() if isinstance(other, Parameter) else True

    def __repr__(self):
        """get the representation of the Parameter

        :return: the representation of the Parameter
        :rtype: str
        """

        # return
        return self._representationTemplate().format(parameter=self.path())

    # COMMANDS #

    def alias(self):
        """get the alias of the Parameter

        :return: the alias of the Parameter
        :rtype: str
        """

        # return
        return self.houParm().alias()

    def animationKeys(self, frames=None, isRange=False):
        """get the animations keys existing on the Parameter

        :param frames: the frames to get the key on - default is all animation keys
        :type frames: tuple[float]

        :param isRange: ``True`` : get all the animations keys between the minimum and the maximum given frames -
                        ``False`` : get the animations keys on the given frames only
        :type isRange: bool

        :return: the animations keys existing on the Parameter
        :type: tuple[:class:`hou.BaseKeyframe`]
        """

        # return animation on given frames
        if frames and not isRange:
            return tuple(animationKey
                         for animationKey in self.houParm().keyframes()
                         if animationKey.frame() in frames)

        # return all animation keys
        if not frames:
            return self.houParm().keyframes()

        # return animation keys in range starting from the only frame given
        if len(frames) == 1:
            return tuple(animationKey
                         for animationKey in self.houParm().keyframes()
                         if animationKey.frame() >= frames[0])

        # return animation keys in range between given frames
        return self.houParm().keyframesInRange(min(frames), max(frames))

    def createWidget(self, parent=None):
        """create a qt widget manipulating the Parameter

        :return: the widget
        :rtype: cgp_houdini_utils.ui.ParameterWidget
        """

        # return
        return cgp_houdini_utils.ui.createParameterWidget(self, parent=parent)

    def deleteAnimationKeys(self, frames=None, isRange=False):
        """delete an animation key on the Parameter

        :param frames: the frames to delete the key on - default is all animation keys
        :type frames: tuple[float]

        :param isRange: ``True`` : delete all the animations keys between the minimum and the maximum given frames -
                        ``False`` : delete the animations keys on the given frames only
        :type isRange: bool
        """

        # delete all keys
        if frames is None:
            self.houParm().deleteAllKeyframes()
            return

        # delete given keys
        for animationKey in self.animationKeys(frames=frames, isRange=isRange):
            self.houParm().deleteKeyframeAtFrame(animationKey.frame())

    def dependants(self):
        """get the dependants parameters (the ones driven) of the Parameter

        :return: the dependant parameters of the Parameter
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Parameter`]
        """

        # return
        return tuple(cgp_houdini_utils.scene._api.parameter(houParm)
                     for houParm in self.houParm().parmsReferencingThis())

    def execute(self, kwargs=None):
        """execute (press the action button of) the Parameter

        :param kwargs: the keyword arguments for the execution process
        :type kwargs: dict
        """

        # init
        houParameter = self.houParm()
        kwargs = kwargs or {}
        action = houParameter.parmTemplate().tags().get('script_action')

        # error
        if not action:
            raise RuntimeError('No script action defined for parameter: {}'.format(self))

        # prepare action kwargs
        houNode = self.node().houNode()
        if 'node' not in kwargs:
            kwargs['node'] = houNode
        if 'nodepath' not in kwargs:
            kwargs['nodepath'] = houNode.path()
        if 'parmtuple' not in kwargs:
            kwargs['parmtuple'] = houParameter.tuple()

        # execute action
        with cgp_houdini_utils.decorators.PaneTabsPined():
            exec(action, globals(), locals())

    def expression(self):
        """get the expression on the Parameter

        :return: the expression on the Parameter
        :rtype: str
        """

        # return
        return self.houParm().expression()

    def hasAnimationKey(self, frame=None):
        """check if an animation key exists on the Parameter

        :param frame: the frame to look at - check all the frames by default
        :type frame: float

        :return: ``True`` : The Parameter does have an animation key -
                 ``False`` : The Parameter does not have an animation key
        :rtype: bool
        """

        # return
        return (bool(self.houParm().keyframes())
                if frame is None
                else bool(self.houParm().keyframesInRange(frame, frame)))

    def hasMenu(self):
        """check if a menu exists on the Parameter

        :return: ``True`` : The Parameter does have a menu -
                 ``False`` : The Parameter does not have a menu
        :rtype: bool
        """

        # return
        try:
            self.houParm().menuItems()
            return True
        except hou.OperationFailed:
            return False

    def help(self):
        """get the help (aka 'tooltip text') of the Parameter

        :return: the help of the Parameter
        :rtype: str
        """

        # return
        return self.houParm().parmTemplate().help()

    def houParm(self):
        """get the hou.Parm object of the Parameter

        :return: the hou.Parm object of the Parameter
        :rtype: :class:`hou.Parm`
        """

        # return
        return self._houParm

    def isDisabled(self):
        """get the lock state of the Parameter

        :return: ``True`` : the parameter is disabled - ``False`` : the parameter is enabled
        :rtype: bool
        """

        # return
        return self.houParm().isDisabled()

    def isLocked(self):
        """get the lock state of the Parameter

        :return: ``True`` : the parameter is locked - ``False`` : the parameter is not locked
        :rtype: bool
        """

        # return
        return self.houParm().isLocked()

    def isVisible(self):
        """get the visibility state of the Parameter

        :return: ``True`` : the parameter is visible - ``False`` : the parameter is hidden
        :rtype: bool
        """

        # return
        return not self.houParm().isHidden()

    def label(self):
        """get the label of the Parameter

        :return: the label of the Parameter
        :rtype: str
        """

        # return
        return self.houParm().description()

    def menuItems(self):
        """get the menu items of the Parameter

        :return: the menu items of the Parameter
        :rtype: tuple[str]
        """

        # return
        return self.houParm().menuItems()

    def menuLabels(self):
        """get the menu labels of the Parameter

        :return: the menu labels of the Parameter
        :rtype: tuple[str]
        """

        # return
        return self.houParm().menuLabels()

    def menuType(self):
        """get the menu type of the Parameter

        :return: the menu type of the Parameter
        :rtype: :class:`cgp_houdini_utils.constants.MenuType`
        """

        # return None if no menu
        if not self.hasMenu():
            return None

        # get menu type
        houType = self.houParm().parmTemplate().menuType()

        # return
        return str(houType).rsplit('.', 1)[-1]

    def name(self):
        """get the name of the Parameter

        :return: the name of the Parameter
        :rtype: str
        """

        # return
        return self.houParm().name()

    def node(self):
        """get the node containing the Parameter

        :return: the node containing the Parameter
        :rtype: :class:`cgp_houdini_utils.scene.Node`
        """

        # return
        return cgp_houdini_utils.scene._api.node(self.houParm().node())

    def path(self):
        """get the path of the Parameter

        :return: the path of the Parameter
        :rtype: str
        """

        # return
        return self.houParm().path()

    def reference(self):
        """get the referenced parameter (the ones driving) of the Parameter

        :return: the referenced parameter
        :rtype: :class:`cgp_houdini_utils.scene.Parameter`
        """

        # return
        return cgp_houdini_utils.scene._api.parameter(self.houParm().getReferencedParm())

    def setAlias(self, alias):
        """set the alias of the Parameter

        :param alias: the alias to set to the Parameter
        :type alias: str
        """

        # return
        self.houParm().setAlias(alias)

    def setAnimationKey(self, frame=None, value=None):
        """set an animation key on the Parameter

        :param frame: the frame to set the key on - default is current frame
        :type frame: float

        :param value: the value to key - default is current value
        :type value: any
        """

        # init
        frame = hou.frame() if frame is None else frame
        value = self.value() if value is None else value

        # create the houdini animation key
        animationKey = hou.Keyframe()
        animationKey.setFrame(frame)
        animationKey.setValue(value)

        # set the key to the parameter
        self.houParm().setKeyframe(animationKey)

    def setDisabled(self, isDisabled):
        """set the disable state of the Parameter

        :param isDisabled: ``True`` : disable the parameter - ``False`` : enable the parameter
        :type isDisabled: bool
        """

        # execute
        self.houParm().disable(isDisabled)

    def setExpression(self, expression):
        """set an expression on the Parameter

        :param expression: the expression to set
        :type expression: str
        """

        # return
        self.houParm().setExpression(expression)

    def setLocked(self, isLocked):
        """set the lock state of the Parameter

        :param isLocked: ``True`` : lock the parameter - ``False`` : unlock the parameter
        :type isLocked: bool
        """

        # execute
        self.houParm().lock(isLocked)

    def setVisible(self, isVisible):
        """set the visibility state of the Parameter

        :param isVisible: ``True`` : show the parameter - ``False`` : hide the parameter
        :type isVisible: bool
        """

        # execute
        self.houParm().hide(not isVisible)

    def setReference(self, parameter):
        """set the referenced parameter (the ones driving) of the Parameter

        :param parameter: the parameter to reference - or None to remove the reference
        :type parameter: :class:`cgp_houdini_utils.scene.Parameter` or None
        """

        # remove reference if nothing given
        if parameter is None:
            self.deleteAnimationKeys()
            return

        # get relative path
        nodesRelativePath = self.node().path(relativeTo=parameter.node())

        # get the reference expression
        expression = "{}(\"{}/{}\")".format(self._REFERENCE_EXPRESSION_FUNCTION, nodesRelativePath, parameter.name())

        # set the expression
        self.setExpression(expression)

    def setValue(self, value):
        """set the value of the Parameter

        :param value: the value to set to the Parameter
        :type value: any
        """

        # execute
        try:
            self.houParm().set(value)
        except TypeError:
            self.setExpression(value)

    def type_(self):
        """get the type of the Parameter

        :return: the type of the Parameter
        :rtype: str
        """

        # return
        return cgp_houdini_utils.scene._type.parameterType(self.houParm())

    def value(self, frame=None, isRaw=False):
        """get the value of the Parameter

        :param frame: frame to get the value at
        :type frame: float

        :param isRaw: ``True`` : get the value of the parameter without evaluation or expansion -
                      ``False`` : get the value of the parameter when evaluated and expanded
        :type isRaw: bool

        :return: the value of the Parameter
        :rtype: any
        """

        # return the raw text value
        if isRaw:
            return self.houParm().rawValue()

        # return based on current frame
        if frame is None:
            return self.houParm().eval()

        # return based on given frame
        return self.houParm().evalAtFrame(frame)
