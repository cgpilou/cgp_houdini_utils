"""
package : cgp_houdini_utils.files
file : __init__.py

description: handles file operations
"""

# imports local
from ._api import registerFileTypes
from ._houdini import HipFile


__all__ = ['registerFileTypes', 'HipFile']
