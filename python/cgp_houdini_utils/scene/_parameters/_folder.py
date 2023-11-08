"""
parameter folder library
"""

# imports third-parties
import hou

# imports rodeo
import cgp_generic_utils.python

# import local
import cgp_houdini_utils.constants


# PARAMETER FOLDER OBJECTS #


class ParameterFolder(cgp_generic_utils.python.BaseObject):
    """parameter folder object that manipulates any kind of parameter folder
    """

    # ATTRIBUTES #

    _TYPE = cgp_houdini_utils.constants.ParameterType.PARAMETER_FOLDER

    # INIT #

    def __init__(self, node, index):
        """initialization of the ParameterFolder

        :param node: the houdini node containing the folder or its path
        :type node: :class:`hou.Node` or str

        :param index: the folder index
        :type index: int
        """

        # init
        self._houNode = node if isinstance(node, hou.Node) else hou.node(node)
        self._index = index

    def __eq__(self, other):
        """check if an other ParameterFolder is equal to the ParameterFolder

        :param other: the other Parameter
        :type other: :class:`cgp_houdini_utils.scene.Parameter`

        :return: ``True`` : the two parameters are equal - ``False`` : the two parameters are not equal
        :rtype: bool
        """

        # return
        return ((self._houNode == other._houNode and self._index == other._index)
                if isinstance(other, ParameterFolder)
                else False)

    def __ne__(self, other):
        """check if an other ParameterFolder is not equal to the ParameterFolder

        :param other: the other Parameter
        :type other: :class:`cgp_houdini_utils.scene.Parameter`

        :return: ``True`` : the two parameters are not equal - ``False`` : the two parameters are equal
        :rtype: bool
        """

        # return
        return ((self._houNode != other._houNode or self._index != other._index)
                if isinstance(other, ParameterFolder)
                else True)

    def __repr__(self):
        """get the representation of the ParameterFolder

        :return: the representation of the ParameterFolder
        :rtype: str
        """

        # return
        return self._representationTemplate().format(node=self._houNode.path(), index=self._index)

    # COMMANDS #

    def folderType(self):
        """get the folder type of the ParameterFolder

        :return: the folder type of the ParameterFolder
        :rtype: str
        """

        # return
        return str(self._parameterTemplate().folderType()).rsplit('.', 1)[-1]

    def isEndingTabGroup(self):
        """get the end tab state of the ParameterFolder

        :return: ``True`` : the parameter is the last tab - ``False`` : the parameter is not the last tab
        :rtype: bool
        """

        # return
        return self._parameterTemplate().endsTabGroup()

    def isVisible(self):
        """get the visibility state of the ParameterFolder

        :return: ``True`` : the parameter is visible - ``False`` : the parameter is hidden
        :rtype: bool
        """

        # return
        return not self._parameterTemplate().isHidden()

    def label(self):
        """get the label of the ParameterFolder

        :return: the label of the ParameterFolder
        :rtype: str
        """

        # return
        return self._parameterTemplate().label()

    def setFolderType(self, folderType):
        """set the folder type of the ParameterFolder

        :param folderType: the folder type to set
        :type folderType: :class:`cgp_houdini_utils.constants.FolderType`
        """

        # init
        template = self._parameterTemplate().clone()
        folderTypes = cgp_houdini_utils.constants.FolderType

        # handle borderless
        if folderType == folderTypes.BORDERLESS:
            tags = template.tags()
            tags['group_type'] = 'simple'
            tags['sidefx::look'] = 'blank'
            template.setTags(tags)
            folderType = folderTypes.SIMPLE
        else:
            tags = {key: value
                    for key, value
                    in template.tags().items()
                    if key not in ('group_type', 'sidefx::look')}
            template.setTags(tags)

        # get houdini folder type
        typesMap = {folderTypes.COLLAPSIBLE: hou.folderType.Collapsible,
                    folderTypes.IMPORT_BLOCK: hou.folderType.ImportBlock,
                    folderTypes.MULTIPARM_BLOCK: hou.folderType.MultiparmBlock,
                    folderTypes.RADIO_BUTTONS: hou.folderType.RadioButtons,
                    folderTypes.SCROLLING_MULTIPARM_BLOCK: hou.folderType.ScrollingMultiparmBlock,
                    folderTypes.SIMPLE: hou.folderType.Simple,
                    folderTypes.TABBED_MULTIPARM_BLOCK: hou.folderType.TabbedMultiparmBlock,
                    folderTypes.TABS: hou.folderType.Tabs}
        folderType = typesMap[folderType]

        # execute
        template.setFolderType(folderType)
        self._replaceParameterTemplate(template)

    def setVisible(self, isVisible):
        """set the visibility state of the ParameterFolder

        :param isVisible: ``True`` : show the parameter folder - ``False`` : hide the parameter folder
        :type isVisible: bool
        """

        # init
        template = self._parameterTemplate().clone()

        # execute
        template.hide(not isVisible)
        self._replaceParameterTemplate(template)

    # PROTECTED COMMANDS #

    def _parameterTemplate(self):
        """get the parameter template of the ParameterFolder

        :return: the parameter template of the ParameterFolder
        :rtype: :class:`hou.ParmTemplate`
        """

        # init
        index = -1

        # parse templates on node
        for template in self._houNode.parmTemplateGroup().entries():
            templateType = cgp_houdini_utils.scene._type.parameterTemplateType(template)
            if templateType == cgp_houdini_utils.constants.ParameterType.FOLDER:
                index += 1

                # return
                if index == self._index:
                    return template

    def _replaceParameterTemplate(self, parameterTemplate):
        """replace the parameter template of the ParameterFolder

        :param parameterTemplate: the parameter template to set instead of the current one
        :type parameterTemplate: :class:`hou.ParmTemplate`
        """

        # init
        index = -1
        templateGroup = self._houNode.parmTemplateGroup()

        # parse templates on node
        for template in templateGroup.entries():
            templateType = cgp_houdini_utils.scene._type.parameterTemplateType(template)
            if templateType == cgp_houdini_utils.constants.ParameterType.FOLDER:
                index += 1

                # return
                if index == self._index:
                    templateGroup.replace(template, parameterTemplate)
                    self._houNode.setParmTemplateGroup(templateGroup)
                    return
