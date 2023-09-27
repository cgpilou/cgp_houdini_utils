"""
generic hotkey library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# import local
import cgp_houdini_utils.constants


# HOTKEY OBJECTS #


class BaseHotkey(cgp_generic_utils.python.BaseObject):
    """base object that manipulates any kind of houdini hotkey or hotkey context
    """

    # ATTRIBUTES #

    _DATA_COMMAND = NotImplemented
    _TYPE = NotImplemented

    # INIT #

    def __init__(self, name):
        """initialization of the BaseHotkey

        :param name: the houdini hotkey name (aka: symbol) - eg: ``'h.pane.wsheet``
        :type name: str
        """

        # init
        self._name = name

    def __repr__(self):
        """get the representation of the BaseHotkey

        :return: the representation of the BaseHotkey
        :rtype: str
        """

        # return
        return self._representationTemplate().format(name=self.name())

    # COMMANDS #

    def data(self):
        """get the data of the BaseHotkey

        :return: the data of the BaseHotkey
        :rtype: dict
        """

        # init
        name = self.name()
        parentName = self._parentName()

        # get raw data
        for data in self._DATA_COMMAND(parentName)[self.name()]:
            if data['symbol'] != name:
                continue

            # reformat data
            data['description'] = data.pop('help')
            data['name'] = data.pop('symbol')

            # return
            return data

        # error
        raise RuntimeError('No data found for: {}'.format(self))

    def description(self):
        """get the description of the BaseHotkey

        :return: the description of the BaseHotkey
        :rtype: str
        """

        # return
        return self.data()['description']

    def label(self):
        """get the label of the BaseHotkey

        :return: the label of the BaseHotkey
        :rtype: str
        """

        # return
        return self.data()['label']

    def name(self):
        """get the name (aka: symbol) of the BaseHotkey

        :return: the name (aka: symbol) of the BaseHotkey
        :rtype: str
        """

        # return
        return self._name

    def parent(self):
        """get the parent context of the BaseHotkey

        :return: the parent context of the BaseHotkey
        :rtype: :class:`cgp_houdini_utils.ui.HotkeyContext`
        """

        # return
        return HotkeyContext(self._parentName())

    # PROTECTED COMMANDS #

    def _parentName(self):
        """get the parent name of the BaseHotkey

        :return: the parent name of the BaseHotkey
        :rtype: str
        """

        # init
        name = self.name()

        # error
        if '.' in name:
            raise RuntimeError('No parent context for: {}'.format(self))

        # return
        return name.rsplit('.', 1)[0]


class Hotkey(BaseHotkey):
    """hotkey object that manipulates any kind of houdini hotkey
    """

    # ATTRIBUTES #

    _DATA_COMMAND = hou.hotkeys.commandsInContext
    _TYPE = cgp_houdini_utils.constants.HotkeyType.HOTKEY

    # COMMANDS #

    def shortcuts(self):
        """get the assigned keyboard keys of the Hotkey

        :return: the assigned keyboard keys of the Hotkey
        :rtype: tuple[str]
        """

        # return
        return hou.hotkeys.assignments(self.name())

    def setShortcuts(self, assignments):
        """set the keyboard keys to assign to the Hotkey

        :param assignments: the keyboard keys to assign to the Hotkey
        :type assignments: tuple[str] or None
        """

        # clear
        hou.hotkeys.clearAssignments(self.name())
        assignments = assignments or tuple()

        # set the keys
        for assignment in assignments:
            hou.hotkeys.addAssignment(self.name(), assignment)


class HotkeyContext(BaseHotkey):
    """hotkey context object that manipulates any kind of houdini hotkey context
    """

    # ATTRIBUTES #

    _DATA_COMMAND = hou.hotkeys.contextsInContext
    _TYPE = cgp_houdini_utils.constants.HotkeyType.CONTEXT

    # COMMANDS #

    def children(self, isRecursive=False):
        """get the children contexts of the HotkeyContext

        :param isRecursive: ``True`` : get children context recursively - ``False`` : get only direct children context
        :type isRecursive: bool

        :return: get the children contexts of the HotkeyContext
        :rtype: tuple[:class:`cgp_houdini_utils.ui.HotkeyContext`]
        """

        # init
        children = tuple(HotkeyContext(data['symbol'])
                         for data in hou.hotkeys.contextsInContext(self.name()))

        # recurse
        if isRecursive:
            for child in children:
                children += child.children(isRecursive=True)

        # return
        return children

    def hotkeys(self):
        """get the hotkeys contained in the HotkeyContext

        :return: the hotkeys contained in the HotkeyContext
        :rtype: tuple[:class:`cgp_houdini_utils.ui.Hotkey`]
        """

        # return
        return tuple(Hotkey(data['symbol'])
                     for data in hou.hotkeys.commandsInContext(self.name()))
