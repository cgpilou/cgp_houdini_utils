"""
channel editor paneTab library
"""

# import local
import cgp_houdini_utils.constants
import cgp_houdini_utils.scene
from . import _generic


# CHANNEL EDITOR OBJECTS #


class ChannelEditor(_generic.PaneTab):
    """pane tab object that manipulates a ``ChannelEditor`` pane tab
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.PaneTabType.CHANNEL_EDITOR

    # COMMANDS #

    def parameters(self):
        """get the parameters listed in the ChannelEditor

        :return: the parameters listed in the ChannelEditor
        :rtype: tuple[:class:`cgp_houdini_utils.scene.Parameter`]
        """

        # return
        return tuple(cgp_houdini_utils.scene.parameter(parameter)
                     for parameter in self.houPaneTab().channelList().parms())

    def setParameters(self, parameters):
        """set the parameters listed in the ChannelEditor

        :param parameters: the parameters listed in the ChannelEditor
        :type parameters: tuple[:class:`cgp_houdini_utils.scene.Parameter`]
        """

        # init
        channelList = self.houPaneTab().channelList()

        # clear channels
        channelList.clear()

        # add desired channels
        houParms = tuple(parameter.houParm() for parameter in parameters)
        channelList.addParms(houParms)

        # set the channel list
        self.houPaneTab().setChannelList(channelList)
