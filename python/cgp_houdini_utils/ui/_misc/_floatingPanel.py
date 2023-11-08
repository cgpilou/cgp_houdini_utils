"""
floating panel library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.ui._api


# FLOATING PANEL OBJECTS #


class FloatingPanel(cgp_generic_utils.python.BaseObject):
    """floating panel object that manipulates any kind of houdini floating panel
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.FloatingPanelType.GENERIC

    # INIT #

    def __init__(self, floatingPanel):
        """initialization of the floating panel

        :param floatingPanel: the houdini floating panel
        :type floatingPanel: :class:`hou.FloatingPanel`
        """

        # init
        self._houFloatingPanel = floatingPanel

    def __repr__(self):
        """get the representation of the FloatingPanel

        :return: the representation of the FloatingPanel
        :rtype: str
        """

        # return
        return self._representationTemplate().format(floatingPanel=self.houFloatingPanel())

    # COMMANDS #

    def panes(self):
        """get the panes of the FloatingPanel

        :return: the panes of the FloatingPanel
        :rtype: tuple[:class:`cgp_houdini_utils.ui.Pane`]
        """

        # return
        return tuple(cgp_houdini_utils.ui._api.pane(houPane)
                     for houPane in self.houFloatingPanel().panes())

    def houFloatingPanel(self):
        """get the hou.FloatingPanel object of the FloatingPanel

        :return: the houdini floating panel of the FloatingPanel
        :rtype: :class:`hou.FloatingPanel`
        """

        # return
        return self._houFloatingPanel
