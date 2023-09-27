"""
houdini decorators library
"""

# imports third-parties
import hou

# import rodeo
import cgp_generic_utils.decorators


# DECORATORS #


class CookingDisabled(cgp_generic_utils.decorators.Decorator):
    """decorator object that temporary disable houdini nodes cooking
    """

    # INIT #

    def __init__(self):
        """initialization of the CookingDisabled decorator
        """

        # init
        self._state = None

    def __enter__(self):
        """entering the CookingDisabled decorator
        """

        # execute
        self._state = hou.updateModeSetting()
        hou.setUpdateMode(hou.updateMode.Manual)

    def __exit__(self, *_, **__):
        """exiting the CookingDisabled decorator
        """

        # execute
        hou.setUpdateMode(self._state)


class PaneTabsPined(cgp_generic_utils.decorators.Decorator):
    """decorator object that pin the desired paneTabs to ensure they will not be altered by the decorated process
    """

    # INIT #

    def __init__(self, names=None, types=None):
        """initialization of the PaneTabsPined decorator

        :param names: the names of the paneTabs to pin
        :type names: tuple[str]

        :param types: the types of the paneTabs to pin
        :type types: tuple[:class:`cgp_houdini_utils.constants.PaneTabType`]
        """

        # init
        self._names = names
        self._types = types
        self._paneTabs = {}
        self._selectedNodes = tuple()

    def __enter__(self):
        """entering the PaneTabsPined decorator
        """

        # store selection
        self._selectedNodes = hou.selectedNodes(True)

        # pin network editors
        for panTab in hou.ui.curDesktop().paneTabs():

            # get type
            type_ = str(panTab.type()).rsplit('.', 1)[-1]

            # ignore wrong types
            if self._types and type_ not in self._types:
                continue

            # ignore wrong names
            if self._names and panTab.name() not in self._names:
                continue

            # store the pin status
            self._paneTabs[panTab] = panTab.isPin()

            # pin the tab
            panTab.setPin(True)

    def __exit__(self, *_, **__):
        """exiting the PaneTabsPined decorator
        """

        # restore selection
        for node in set(hou.selectedNodes(True) + self._selectedNodes):
            node.setSelected(node in self._selectedNodes)

        # restore pin status
        for panTab, isPinned in self._paneTabs.items():
            panTab.setPin(isPinned)
