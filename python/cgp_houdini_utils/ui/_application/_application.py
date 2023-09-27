"""
houdini application object library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.qt


# HOUDINI APPLICATION OBJECT #


class HoudiniApplication(cgp_generic_utils.qt.Application):
    """application object that manipulates an ``houdini`` application
    """

    # COMMANDS #

    def mainWindow(self):
        """get the main window of the HoudiniApplication

        :return: the main window of the HoudiniApplication
        :rtype: :class:`PySide2.QtWidgets.QtWidget`
        """

        # return
        return hou.qt.mainWindow()

    def name(self):
        """get the name of the HoudiniApplication

        :return: the name of the HoudiniApplication
        :rtype: str
        """

        # return
        return hou.applicationName()

    def version(self, asTuple=False):
        """get the semantic version of the HoudiniApplication

        :param asTuple: ``True`` : get the version as a tuple - ``False`` get the version as a str
        :type asTuple: bool

        :return: the semantic version of the HoudiniApplication
        :rtype: str or tuple
        """

        # return
        return hou.applicationVersion() if asTuple else hou.applicationVersionString()
