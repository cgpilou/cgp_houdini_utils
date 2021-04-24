"""
houdini file object library
"""

# imports third-parties
import cgp_generic_utils.files
import cgp_generic_utils.constants


# HOUDINI FILE OBJECTS #


class HipFile(cgp_generic_utils.files.File):
    """file object that manipulate a ``.hip`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'hip'

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **__):
        """create a hip file

        :param path: path of the file to create
        :type path: str

        :param content: content to set into the created file
        :type content: any

        :return: the created file
        :rtype: :class:`cgp_houdini_utils.files.HipFile`
        """

        # return
        raise NotImplementedError('HipFile.create is not implemented yet')


class HipncFile(cgp_generic_utils.files.File):
    """file object that manipulate a ``.hipnc`` file on the file system
    """

    # ATTRIBUTES #

    _extension = 'hipnc'

    # OBJECT COMMANDS #

    @classmethod
    def create(cls, path, content=None, **__):
        """create a hipnc file

        :param path: path of the file to create
        :type path: str

        :param content: content to set into the created file
        :type content: any

        :return: the created file
        :rtype: :class:`cgp_houdini_utils.files.HipncFile`
        """

        # return
        raise NotImplementedError('HipncFile.create is not implemented yet')
