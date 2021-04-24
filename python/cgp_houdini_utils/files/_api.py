"""
houdini files management functions
"""

# imports third-parties
import cgp_generic_utils.files


# COMMANDS #


def registerFileTypes():
    """register file types
    """

    # imports file modules
    from ._houdini import HipFile, HipncFile

    fileTypes = {'hip': HipFile,
                 'hipnc': HipncFile}

    # execute
    cgp_generic_utils.files.registerFileTypes(fileTypes)
