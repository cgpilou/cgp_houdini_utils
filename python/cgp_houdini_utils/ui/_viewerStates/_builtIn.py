"""
built-in viewer state library
"""

# imports python
import re
import imp
import inspect

# import third-parties
import hou

# imports rodeo
import cgp_generic_utils.files

# imports local
import cgp_houdini_utils.constants
from . import _base


# BUILT-IN VIEWER STATE OBJECTS #


class BuiltInNodeState(_base.BaseNodeState):
    """viewer state object that manipulates any kind of built-in viewer state
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ViewerStateType.BUILT_IN

    # INIT #

    def __init__(self, *args, **kwargs):
        """initialization of the BuiltInNodeState

        :param kwargs: the kwargs sent by houdini
        :type kwargs: dict{'state_name': str,
                           'scene_viewer': `hou.SceneViewer`}
        """

        # init
        super(BuiltInNodeState, self).__init__(*args, **kwargs)

    # COMMANDS #

    def houClass(self):
        """the python class that handle python state of the BuiltInNodeState

        :return: the python class that handle python state of the BuiltInNodeState
        :rtype: class
        """

        # find class name in code
        code = self._builtInCode()
        className = re.search(r'\.bindFactory\((.+)\)', code).groups()[0]

        # return
        return getattr(self._builtInModule(), className)

    def houTemplate(self, name=None, label=None, icon=None, isFactoryBound=True):
        """get the hou.ViewerStateTemplate object to generate the python state of the BuiltInNodeState

        :param name: if defined, the returned template will use the given name - default is to use the built-in name
        :type name: str

        :param label: if defined, the returned template will use the given label - default is to use the built-in label
        :type label: str

        :param icon: if defined, the returned template will use the given icon - default is to use the built-in icon
        :type icon: str

        :param isFactoryBound: ``True`` : the built-in factory will be bound to the template -
                               ``False`` : no factory will be bound to the template
        :type isFactoryBound: bool

        :return: the hou.ViewerStateTemplate object to generate the python state of the BuiltInNodeState
        :rtype: :class:`hou.ViewerStateTemplate`
        """

        # get the module with custom values
        if name or label or icon or not isFactoryBound:

            # init
            name = name or self.name()
            label = label or self.name()
            icon = icon or self.name()

            # replace parameters in code
            code = self._builtInCode()
            code = re.sub(r'(.*\.bindIcon\()(.+)(\)\n)', r'\1"{}"\3'.format(icon), code)
            code = re.sub(r'(.*hou\.ViewerStateTemplate\()([^,]+),([^,]+)(,.*)',
                          r'\1"{}", "{}"\4'.format(name, label),
                          code)

            # remove the built-in factory binding
            if not isFactoryBound:
                code = re.sub(r'\.bindFactory\((.+)\)', '', code)

            # eval the module code with needed global kwargs
            module = imp.new_module('module')
            globals_ = module.__dict__
            globals_['kwargs'] = {'type': self._houNodeType(), 'icon': self.icon()}
            exec (code, globals_)

        # get module as is
        else:
            module = self._builtInModule()

        # return
        return module.createViewerStateTemplate()

    # PROTECTED COMMANDS #

    def _builtInCode(self):
        """get the python code of the BuiltInNodeState

        :return: the code of the BuiltInNodeState
        :rtype: str
        """

        # abstract command
        raise NotImplementedError

    def _builtInModule(self):
        """get the python module of the BuiltInNodeState

        :return: the python module of the BuiltInNodeState
        :rtype: module
        """

        # abstract command
        raise NotImplementedError

    def _houNodeType(self):
        """get the node type associated to the BuiltInNodeState

        :return: the node type associated to the BuiltInNodeState
        :rtype: :class:`hou.NodeType`
        """

        # return
        return self.houViewerState().nodeType()


class BuiltInHdaState(BuiltInNodeState):
    """viewer state object that manipulates any kind of built-in viewer state stored in a ``hda``
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ViewerStateType.BUILT_IN_HDA

    # PROTECTED COMMANDS #

    def _builtInCode(self):
        """get the python code of the BuiltInHdaState

        :return: the code of the BuiltInHdaState
        :rtype: str
        """

        # init
        info = self.info()

        # get the hda definition
        definition = hou.hdaDefinition(hou.nodeTypeCategories()[info['Category']],
                                       info['Node type'],
                                       info['Source'])

        # return
        return definition.sections()['ViewerStateModule'].contents()

    def _builtInModule(self):
        """get the python module of the BuiltInHdaState

        :return: the python module of the BuiltInHdaState
        :rtype: module
        """

        # return
        return self._houNodeType().hdaViewerStateModule()

    def _houNodeType(self):
        """get the node type associated to the BuiltInHdaState

        :return: the node type associated to the BuiltInHdaState
        :rtype: :class:`hou.NodeType`
        """

        # get from the houViewerState
        nodeType = super(BuiltInHdaState, self)._houNodeType()
        if nodeType:
            return nodeType

        # get from the state info
        info = self.info()

        # return
        return hou.nodeTypeCategories()[info['Category']].nodeTypes()[info['Node type']]


class BuiltInPyState(BuiltInNodeState):
    """viewer state object that manipulates any kind of built-in viewer state stored in a ``py`` file
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ViewerStateType.BUILT_IN_PY

    # PROTECTED COMMANDS #

    def _builtInCode(self):
        """get the python code of the BuiltInPyState

        :return: the code of the BuiltInPyState
        :rtype: str
        """

        # init
        stateFile = cgp_generic_utils.files.entity(self.info()['Source'])

        # get the python module from file
        module = stateFile.importAsModule()

        # return
        return inspect.getsource(module)

    def _builtInModule(self):
        """get the python module of the BuiltInPyState

        :return: the python module of the BuiltInPyState
        :rtype: module
        """

        # init
        stateFile = cgp_generic_utils.files.entity(self.info()['Source'])

        # return
        return stateFile.importAsModule()
