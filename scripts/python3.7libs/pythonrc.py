"""cgp_houdini_utils startup
"""


# imports local
import cgp_houdini_utils.files


# EXECUTE #


# register houdini files
cgp_houdini_utils.files.registerFileTypes()


print('cgp_houdini_utils - pythonrc.py : loaded')