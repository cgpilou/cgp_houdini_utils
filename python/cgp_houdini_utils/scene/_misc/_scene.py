"""
scene library
"""

# imports third-parties
import hou
import cgp_generic_utils.files

# imports rodeo
import cgp_generic_utils.python

# imports local
import cgp_houdini_utils.constants


# SCENE OBJECTS #


class Scene(cgp_generic_utils.python.BaseObject):
    """scene object that manipulates a ``houdini`` scene
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.MiscType.SCENE

    # INIT #

    def __getattr__(self, attr):
        """override getattr method

        :param attr: the attribute to get
        :type attr: str

        :return: the attr value
        :rtype: Any
        """

        # get the entity
        entity = cgp_generic_utils.files.entity(self.path())

        # return
        return getattr(entity, attr)

    # STATIC COMMANDS #

    @staticmethod
    def path():
        """get the path of the Scene

        :return: the path of the Scene
        :rtype: str
        """

        # return
        return hou.hipFile.path()

    # COMMANDS #

    def reopen(self, isForce=False):
        """reopen the Scene

        :param isForce: ``True`` : The scene will be reopen without any warning -
                        ``False`` : A warning dialog will pop if the scene contains unsaved changes
        :type isForce: bool
        """

        # execute
        hou.hipFile.load(self.path(), suppress_save_prompt=isForce, ignore_load_warnings=False)
