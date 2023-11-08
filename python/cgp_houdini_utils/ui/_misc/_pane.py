"""
pane library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.ui._api


# PANE OBJECTS #


class Pane(cgp_generic_utils.python.BaseObject):
    """pane object that manipulates any kind of houdini pane
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.PaneType.GENERIC

    # INIT #

    def __init__(self, pane):
        """initialization of the Pane

        :param pane: the houdini pane
        :type pane: :class:`hou.Pane`
        """

        # init
        self._houPane = pane

    def __repr__(self):
        """get the representation of the Pane

        :return: the representation of the Pane
        :rtype: str
        """

        # return
        return self._representationTemplate().format(pane=self.houPane())

    # COMMANDS #

    def activeTab(self):
        """get the currently active tab of the Pane

        :return: the currently active tab of the Pane
        :rtype: :class:`cgp_houdini_utils.ui.PaneTab`
        """

        # return
        return cgp_houdini_utils.ui._api.paneTab(self.houPane().currentTab())

    def createTab(self, tabType):
        """create a new tab in the Pane

        :param tabType: the type of the tab to create
        :type tabType: :class:`cgp_houdini_utils.constants.PaneTabType` or str

        :return: the new tab
        :rtype: :class:`cgp_houdini_utils.ui.PaneTab`
        """

        # init
        tabType = getattr(hou.paneTabType, tabType)

        # return
        return self.houPane().createTab(tabType)

    def desktop(self):
        """get the desktop of the Pane

        :return: the desktop of the Pane
        :rtype: :class:`cgp_houdini_utils.ui.Desktop`
        """

        # return
        return cgp_houdini_utils.ui._api.desktop(self.houPane().desktop())

    def houPane(self):
        """get the hou.Pane object of the Pane

        :return: the houdini pane of the Pane
        :rtype: :class:`hou.Pane`
        """

        # return
        return self._houPane

    def setActiveTab(self, paneTab):
        """set the active tab of the Pane

        :param paneTab: the active tab to set to the Pane
        :type paneTab: :class:`cgp_houdini_utils.ui.PaneTab`
        """

        # error
        if paneTab.houPaneTab() not in self.houPane().tabs():
            raise ValueError('Unable to set active pane tab of pane. '
                             'The given pane tab is not a tab of the current pane')

        # execute
        paneTab.houPaneTab().setIsCurrentTab()

    def tabs(self, tabTypes=None):
        """get the tabs of the Pane

        :param tabTypes: the types of the tabs to get
        :type tabTypes: tuple[:class:`cgp_houdini_utils.constants.PaneTabType`]

        :return: the tabs of the Pane
        :rtype: tuple[:class:`cgp_houdini_utils.ui.PaneTab`]
        """

        # init
        allTabs = tuple(cgp_houdini_utils.ui._api.paneTab(tab) for tab in self.houPane().tabs())

        # return
        return tuple(tab for tab in allTabs if tab.type_() in tabTypes) if tabTypes else allTabs
