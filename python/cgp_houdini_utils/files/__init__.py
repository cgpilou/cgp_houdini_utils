"""
houdini file objects and management functions
"""


# import rodeo
import cgp_generic_utils.files

# imports local
from ._files import HoudiniFile, HipFile, HiplcFile, HipncFile


def registerFileTypes():
    """register houdini file types to grant generic file management functions access to the houdini file objects
    """

    # collect file types
    fileTypes = {cls._extension: cls
                 for cls in [HipFile,
                             HiplcFile,
                             HipncFile]}

    # register
    cgp_generic_utils.files.registerFileTypes(fileTypes)


__all__ = ['registerFileTypes', 'HoudiniFile', 'HipFile', 'HiplcFile', 'HipncFile']
