"""
houdini file library
"""

# imports third-parties
import cgp_generic_utils.files

# imports local
import cgp_houdini_utils.constants


# HOUDINI FILE OBJECTS #


class HoudiniFile(cgp_generic_utils.files.File):
    """file object that manipulates any kind of houdini file
    """

    # ATTRIBUTES #

    _extension = NotImplemented

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **kwargs):
        """create the file

        :param path: path of the file to create
        :type path: str

        :param content: content to set into the created file
        :type content: Any

        :return: the created file
        :rtype: HipFile
        """

        # return
        raise NotImplementedError('{}.create is not implemented yet'.format(cls.__name__))


class HipFile(HoudiniFile):
    """file object that manipulates a ``hip`` file
    """

    # ATTRIBUTES #

    _extension = cgp_houdini_utils.constants.FileExtension.GENERIC


class HiplcFile(HoudiniFile):
    """file object that manipulates a ``hiplc`` file
    """

    # ATTRIBUTES #

    _extension = cgp_houdini_utils.constants.FileExtension.LIMITED_COMMERCIAL


class HipncFile(HoudiniFile):
    """file object that manipulates a ``hipnc`` file
    """

    # ATTRIBUTES #

    _extension = cgp_houdini_utils.constants.FileExtension.NON_COMMERCIAL
