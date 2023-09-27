"""
desktop library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.ui._api


# DESKTOP OBJECTS #


class Desktop(cgp_generic_utils.python.BaseObject):
    """desktop object that manipulates any kind of houdini desktop
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.DesktopType.GENERIC

    # INIT #

    def __init__(self, desktop):
        """initialization of the Desktop

        :param desktop: the houdini desktop
        :type desktop: :class:`hou.Desktop`
        """

        # init
        self._houDesktop = desktop

    def __repr__(self):
        """get the representation of the Desktop

        :return: the representation of the Desktop
        :rtype: str
        """

        # return
        return self._representationTemplate().format(desktop=self.houDesktop())

    # COMMANDS #

    def floatingPanels(self):
        """get the floating panels of the Desktop

        :return: the floating panels of the Desktop
        :rtype: tuple[:class:`cgp_houdini_utils.ui.FloatingPanel`]
        """

        # return
        return tuple(cgp_houdini_utils.ui._api.floatingPanel(houFloatingPanel)
                     for houFloatingPanel in self.houDesktop().floatingPanels())

    def houDesktop(self):
        """get the hou.Desktop object of the Desktop

        :return: the houdini desktop of the Desktop
        :rtype: :class:`hou.Desktop`
        """

        # return
        return self._houDesktop

    def panes(self):
        """get the panes of the Desktop

        :return: the the panes of the Desktop
        :rtype: tuple[:class:`cgp_houdini_utils.ui.Pane`]
        """

        # return
        return tuple(cgp_houdini_utils.ui._api.pane(houPane)
                     for houPane in self.houDesktop().panes())
