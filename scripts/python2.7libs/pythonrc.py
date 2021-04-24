"""
package : cgp_houdini_utils
file : pythonrc.py

description : cgp_houdini_utils startup
"""

# imports local
import cgp_houdini_utils.files


# register houdini files
cgp_houdini_utils.files.registerFileTypes()


print 'cgp_houdini_utils - pythonrc.py : loaded '
