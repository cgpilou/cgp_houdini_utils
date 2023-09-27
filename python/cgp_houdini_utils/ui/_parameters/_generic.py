"""
generic parameter widget library
"""

# imports third-parties
import PySide2.QtCore
import PySide2.QtGui
import PySide2.QtWidgets
import hou

# imports rodeo
import cgp_generic_utils.python

# imports local
import cgp_houdini_utils.constants
import cgp_houdini_utils.decorators
from ._subWidgets import _lineEdit
from ._subWidgets import _contextMenu


# PARAMETER WIDGET OBJECT #


class ParameterWidget(cgp_generic_utils.python.BaseObject, PySide2.QtWidgets.QWidget):
    """parameter widget object that manipulates any kind of parameter widget
    """

    # ATTRIBUTES #

    _DATA_TYPE = str
    _DATA_WIDGET_CLASS = _lineEdit.AnimatableLineEdit
    _DEFAULT_HEIGHT = hou.ui.scaledSize(24)
    _LABEL_MARGIN = hou.ui.scaledSize(10)
    _LABEL_WIDTH = hou.ui.scaledSize(150)
    _PARAMETER_TYPE = cgp_houdini_utils.constants.ParameterType.GENERIC

    # SIGNALS #

    editingFinished = PySide2.QtCore.Signal(_DATA_TYPE)
    setAnimationKeyTriggered = PySide2.QtCore.Signal()
    deleteAnimationKeysTriggered = PySide2.QtCore.Signal()

    # INIT #

    def __init__(self, parameter, isLabelVisible=True, parent=None):
        """initialization of the ParameterWidget

        :param parameter: the parameter controlled by this widget
        :type parameter: :class:`cgp_houdini_utils.scene.Parameter`

        :param isLabelVisible: ``True`` : the label is visible - ``False`` : the label is hidden
        :type isLabelVisible: :class:`PySide2.QtWidgets.QWidget`

        :param parent: the parent widget
        :type parent: :class:`PySide2.QtWidgets.QWidget`
        """

        # super
        super(ParameterWidget, self).__init__(parent=parent)

        # init attributes
        self._isCallbackConnected = False
        self._parameter = parameter
        self.setFixedHeight(self._DEFAULT_HEIGHT)

        # setup context menu
        self._contextMenu = _contextMenu.ContextMenu(parameter, parent=self)
        self.setContextMenuPolicy(PySide2.QtCore.Qt.CustomContextMenu)

        # init layout
        layout = PySide2.QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # init label widget
        self._labelWidget = PySide2.QtWidgets.QLabel(parameter.label() or parameter.name(), parent=self)
        self._labelWidget.setVisible(isLabelVisible)
        self._labelWidget.setFixedWidth(self._LABEL_WIDTH)
        self._labelWidget.setAlignment(PySide2.QtCore.Qt.AlignRight)
        self._labelWidget.setStyleSheet('margin: 0px {}px 0px 0px'.format(self._LABEL_MARGIN))
        help = parameter.help()
        self._labelWidget.setToolTip('Parameter: {}{}'.format(parameter.name(), ('\n' + help) if help else ''))
        layout.addWidget(self._labelWidget)

        # init data widget
        self._dataWidget = self._DATA_WIDGET_CLASS(parent=self)
        self._dataWidget.setFixedHeight(self._DEFAULT_HEIGHT)
        layout.addWidget(self._dataWidget)

        # init menu button
        if parameter.type_() != cgp_houdini_utils.constants.ParameterType.MENU and parameter.hasMenu():

            self._groupMenuButton = PySide2.QtWidgets.QPushButton(parent=self)
            self._groupMenuButton.setFixedSize(self._dataWidget.height(), self._dataWidget.height())
            pixmap = cgp_houdini_utils.ui._api.createIconPixmap('BUTTONS_folder_expand', size=30)
            self._groupMenuButton.setIcon(PySide2.QtGui.QIcon(pixmap))
            self._groupMenuButton.setStyleSheet('QPushButton{'
                                                'margin:1px; '
                                                'border: 1px solid rgba(0, 0, 0, 1); '
                                                'border-radius: 3px; '
                                                'background: rgba(0, 0, 0, 0.15)}'
                                                'QPushButton:hover{'
                                                'background: rgba(0, 0, 0, 0)}'
                                                '}')

            self.layout().addWidget(self._groupMenuButton)

            # additional connections
            self._groupMenuButton.pressed.connect(self._showMenu)

        # init action button
        parameterTags = parameter.houParm().parmTemplate().tags()
        if 'script_action' in parameterTags:

            icon = parameterTags['script_action_icon']
            help = parameterTags['script_action_help']

            # setup group picker
            self._groupPickerButton = PySide2.QtWidgets.QPushButton(parent=self)
            pixmap = cgp_houdini_utils.ui._api.createIconPixmap(icon, size=30)
            self._groupPickerButton.setIcon(PySide2.QtGui.QIcon(pixmap))
            self._groupPickerButton.setFixedSize(self._dataWidget.height(), self._dataWidget.height())
            self._groupPickerButton.setToolTip(help)
            self.layout().addWidget(self._groupPickerButton)

            # additional connections
            self._groupPickerButton.clicked.connect(lambda: self.parameter().execute())

        # setup connections
        self._setCallbackConnected(True)
        self._setupConnections()

        # setup values
        self._syncParameterToWidget()

    def __repr__(self):
        """get the representation of the ParameterWidget

        :return: the representation of the ParameterWidget
        :rtype: str
        """

        # return
        return self._representationTemplate().format(parameter=self.parameter(),
                                                     isLabelVisible=self._labelWidget.isVisible(),
                                                     parent=self.parent())

    def _setupConnections(self):
        """setup the connections of the ParameterWidget
        """

        # init
        dataWidget = self.dataWidget()

        # data widget connections
        dataWidget.editingFinished.connect(self._syncWidgetToParameter)
        dataWidget.editingFinished.connect(lambda: self.editingFinished.emit(self.value()))
        dataWidget.setAnimationKeyTriggered.connect(self.setAnimationKey)
        dataWidget.deleteAnimationKeyTriggered.connect(lambda: self.deleteAnimationKeys(hou.frame()))
        dataWidget.deleteAllAnimationKeysTriggered.connect(lambda: self.deleteAnimationKeys())

        # context menu connections
        self._contextMenu.setAnimationKeyTriggered.connect(self.setAnimationKey)
        self._contextMenu.deleteAnimationKeyTriggered.connect(lambda: self.deleteAnimationKeys(hou.frame()))
        self._contextMenu.deleteAllAnimationKeysTriggered.connect(lambda: self.deleteAnimationKeys())
        self.customContextMenuRequested.connect(lambda click: self.contextMenu().load(self.mapToGlobal(click)))

        # remove callbacks on destroy
        self.destroyed.connect(lambda: self._setCallbackConnected(False))

    # COMMANDS #

    def contextMenu(self):
        """get the context menu of the ParameterWidget

        :return: the context menu of the ParameterWidget
        :rtype: :class:`PySide2.QtWidgets.QMenu`
        """

        # return
        return self._contextMenu

    def dataWidget(self):
        """get the data widget of the ParameterWidget

        :return: the data widget of the ParameterWidget
        :rtype: :class:`PySide2.QtWidgets.QWidget`
        """

        # return
        return self._dataWidget

    def labelWidget(self):
        """get the label widget of the ParameterWidget

        :return: the label widget of the ParameterWidget
        :rtype: :class:`PySide2.QtWidgets.QLabel`
        """

        # return
        return self._labelWidget

    def parameter(self):
        """get the parameter connected to the ParameterWidget

        :return: the parameter connected to the ParameterWidget
        :rtype: :class:`cgp_houdini_utils.scene.Parameter`
        """
        
        # return
        return self._parameter

    def mouseReleaseEvent(self, event):
        """callback when the mouse click is released on the ParameterWidget

        :param event: the mouse released event
        :type event: :class:`PySide2.QtGui.QMouseEvent`
        """

        # execute default behavior
        super(ParameterWidget, self).mouseReleaseEvent(event)

        # control+click delete the animation key
        if event.modifiers() == PySide2.QtCore.Qt.ControlModifier:
            self.deleteAnimationKey()

        # alt+click set the animation key
        elif event.modifiers() == PySide2.QtCore.Qt.AltModifier:
            self.setAnimationKey()

    def deleteAnimationKeys(self, frame=None):
        """delete an animation key on the parameter of the ParameterWidget
        """

        # init
        frames = None if frame is None else (frame,)

        # execute
        self.parameter().deleteAnimationKeys(frames=frames)

        # update ui
        self._syncParameterToWidget()

        # propagate signal
        self.deleteAnimationKeysTriggered.emit()

    def setAnimationKey(self):
        """set an animation key on the parameter of the ParameterWidget
        """

        # execute
        self.parameter().setAnimationKey()

        # update ui
        self._syncColor()

        # propagate signal
        self.setAnimationKeyTriggered.emit()

    def setContextMenu(self, contextMenu):
        """set the context menu of the ParameterWidget

        :param contextMenu: the context menu of the ParameterWidget
        :type contextMenu: :class:`PySide2.QtWidgets.QMenu`
        """

        # execute
        self._contextMenu = contextMenu

    def setValue(self, value):
        """set the value of the ParameterWidget

        :param value: the value
        :type value: any
        """

        # execute
        self.dataWidget().setValue(value)

    def value(self):
        """get the value of the ParameterWidget

        :return: the value of the ParameterWidget
        :rtype: any
        """

        # return
        return self.dataWidget().value()

    # PROTECTED COMMANDS #

    def _executeMenuAction(self, item):
        """execute a menu action of the ParameterWidget

        :param item: the menu item to set
        :type item: any
        """

        # init
        parameter = self.parameter()

        # execute default behavior
        if parameter.menuType() != cgp_houdini_utils.constants.MenuType.STRING_TOGGLE:
            parameter.setValue(item)
            return

        # get current value
        values = self.value().split(' ')

        # update value
        if item not in values:
            values.append(item)
        else:
            values.pop(values.index(item))

        # set new value
        parameter.setValue(' '.join(values))

    def _setCallbackConnected(self, isConnected):
        """connect or disconnect the callbacks of the ParameterWidget

        :param isConnected: ``True`` : connect the callbacks - ``False`` : disconnect the callbacks
        :type isConnected: bool
        """

        # init
        valueCallback = ((hou.nodeEventType.ParmTupleChanged,), self._syncParameterToWidget)
        playbarCallback = self._syncParameterToWidget

        # connect the callbacks
        if not self._isCallbackConnected and isConnected:

            # sync value
            self._syncParameterToWidget()

            # widget <- parameter connection
            self.parameter().node().createEventCallback(*valueCallback)

            # widget <- playbar connection
            hou.playbar.addEventCallback(playbarCallback)

            # update status - ensure callbacks can be connected only once
            self._isCallbackConnected = True

        # disconnect the callbacks
        elif self._isCallbackConnected and not isConnected:

            # widget <- parameter connection
            if self._isParameterStillExisting():
                if valueCallback in self.parameter().node().eventCallbacks():
                    self.parameter().node().deleteEventCallback(*valueCallback)

            # widget <- playbar connection
            hou.playbar.removeEventCallback(playbarCallback)

            # update status - ensure callbacks can be reconnected in the future
            self._isCallbackConnected = False

    def _showMenu(self):
        """generate and show the menu of the ParameterWidget
        """

        # init
        menu = PySide2.QtWidgets.QMenu(self)
        menuPosition = self._groupMenuButton.mapToGlobal(self._groupMenuButton.rect().bottomRight())
        menuItems = self.parameter().menuItems()

        # add items to menu
        for index, label in enumerate(self.parameter().menuLabels()):
            action = PySide2.QtWidgets.QAction(label, self)
            action.triggered.connect(lambda _=None, item=menuItems[index]: self._executeMenuAction(item))
            menu.addAction(action)

        # show
        menu.exec_(menuPosition)

    def _syncParameterToWidget(self, *_, **__):
        """set the Parameter's value to the data widget of the ParameterWidget
        """

        # disconnect callbacks if called while parameter or dataWidget doesn't exist anymore
        if not self._isParameterStillExisting():
            self._setCallbackConnected(False)
            return

        # execute
        self.setValue(self.parameter().value())

        # update ui
        self._syncColor()

    def _syncWidgetToParameter(self):
        """set the data widget's value to the Parameter of the ParameterWidget
        """

        # init
        value = self.value()

        # execute
        if value.startswith('='):
            self.parameter().setExpression(value)
        else:
            try:
                self.parameter().setValue(self._DATA_TYPE(value))
            except ValueError:
                self.parameter().setExpression(value)

        # update ui
        self._syncColor()

    def _syncColor(self, *_, **__):
        """set the parameter's color to the data widget of the ParameterWidget
        """

        # disconnect callbacks if called while parameter or dataWidget doesn't exist anymore
        if not self._isParameterStillExisting():
            self._setCallbackConnected(False)
            return

        # init
        styleSheet = ''
        houColor = self.parameter().houParm().uiBackgroundColor()
        color = cgp_generic_utils.python.Color(*houColor.rgb()).hex()

        # generate stylesheet
        if color == '#000000':
            color = '#ffffff'
        elif color == '#468c46':
            styleSheet = 'font-weight: bold;'
        styleSheet += 'color: {};'.format(color)

        # set stylesheet
        self.dataWidget().setStyleSheet(styleSheet)

        # update/refresh qt widgets
        self.dataWidget().update()
        self.update()

    def _isParameterStillExisting(self):
        """check the existence of the Parameter of the ParameterWidget

        :return: ``True`` : The Parameter still exists - ``False`` : The Parameter does not exist anymore
        :rtype: bool
        """

        # query the parameter's path
        try:
            self.parameter().path()

        # return
        except hou.ObjectWasDeleted:
            return False
        return True
