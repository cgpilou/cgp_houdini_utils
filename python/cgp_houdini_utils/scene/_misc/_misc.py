"""
miscellaneous object library
"""

# imports third-parties
import hou
import cgp_generic_utils.files


class Scene(object):
    """scene object that manipulates a live scene
    """

    # INIT #

    def __getattr__(self, attribute):
        """override getattr

        :param attribute: the attribute to get
        :type attribute: str

        :return: the attr value
        :rtype: any
        """

        # return
        return getattr(self.file_(), attribute)

    # STATIC COMMANDS #

    @staticmethod
    def file_():
        """the file of the scene

        :return: the file of the scene
        :rtype: :class:`cgp_generic_utils.files.File`
        """

        # return
        return cgp_generic_utils.files.entity(hou.hipFile.path())

    # COMMANDS #

    def reopen(self, force=False):
        """reopen the scene file

        :param force: defines whether or not the command will force the reopening of the scene
        :type force: bool
        """

        # execute
        hou.hipFile.load(self.file_(), suppress_save_prompt=force, ignore_load_warnings=False)
