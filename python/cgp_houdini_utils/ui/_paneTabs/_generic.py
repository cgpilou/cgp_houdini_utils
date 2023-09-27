"""
generic paneTab library
"""

# imports rodeo
import cgp_generic_utils.python

# import local
import cgp_houdini_utils.constants


# GENERIC OBJECTS #


class PaneTab(cgp_generic_utils.python.BaseObject):
    """pane tab object that manipulates any kind of houdini pane tab
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.PaneTabType.GENERIC

    # INIT #

    def __init__(self, paneTab):
        """initialization of the PaneTab

        :param paneTab: the houdini paneTab
        :type paneTab: :class:`hou.PaneTab`
        """

        # init
        self._houPaneTab = paneTab

    def __repr__(self):
        """get the representation of the PaneTab

        :return: the representation of the PaneTab
        :rtype: str
        """

        # return
        return self._representationTemplate().format(paneTab=self.houPaneTab())

    # COMMANDS #

    def houPaneTab(self):
        """get the hou.PaneTab object of the PaneTab

        :return: the houdini pane tab of the PaneTab
        :rtype: :class:`hou.PaneTab`
        """

        # return
        return self._houPaneTab

    def isActive(self):
        """get the active state of the PaneTab

        :return: ``True`` : the PaneTab is active - ``False`` : the PaneTab is not active
        :rtype: bool
        """

        # return
        return self.houPaneTab().isCurrentTab()

    def isPinned(self):
        """get the pin state of the PaneTab

        :return: ``True`` : the PaneTab is pinned - ``False`` : the PaneTab follows the current selection
        :rtype: bool
        """

        # return
        return self.houPaneTab().isPin()

    def name(self):
        """get the name of the PaneTab

        :return: the name of the PaneTab
        :rtype: str
        """

        # return
        return self.houPaneTab().name()

    def pane(self):
        """get the pane of the PaneTab

        :return: the pane of the PaneTab
        :rtype: :class:`cgp_houdini_utils.ui.Pane`
        """

        # return
        return cgp_houdini_utils.ui._api.pane(self.houPaneTab().pane())

    def setName(self, name):
        """set the name of the PaneTab

        :param name: the name of the PaneTab
        :type name: str
        """

        # execute
        self.houPaneTab().setName(name)

    def setPinned(self, isPinned):
        """get the pin state of the PaneTab

        :param isPinned: ``True`` : pin the PaneTab - ``False`` : unpin the PaneTab
        :type isPinned: bool
        """

        # execute
        self.houPaneTab().setPin(isPinned)

    def type_(self):
        """get the type of the PaneTab

        :return: the type of the PaneTab
        :rtype: str
        """

        # return
        return cgp_houdini_utils.ui._type.paneTabType(self.houPaneTab())
