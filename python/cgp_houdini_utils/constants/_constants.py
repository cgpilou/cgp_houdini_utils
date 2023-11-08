"""
constants used to manipulate houdini data
"""

# imports rodeo
import cgp_generic_utils.python


# CONSTANT ENUMS #


class AttributeType(cgp_generic_utils.python.BaseEnum):
    """enum of attribute types
    """

    ARRAY = "Array"
    DICT = "Dict"
    DICT_ARRAY = DICT + ARRAY
    FLOAT = "Float"
    FLOAT_ARRAY = FLOAT + ARRAY
    GENERIC = 'Generic'
    INT = "Int"
    INT_ARRAY = INT + ARRAY
    STRING = "String"
    STRING_ARRAY = STRING + ARRAY
    ARRAYS = (DICT_ARRAY, FLOAT_ARRAY, INT_ARRAY, STRING_ARRAY)
    SINGLES = (DICT, FLOAT, INT, STRING)


class BuiltInState(cgp_generic_utils.python.BaseEnum):
    """enum of built-in viewer state names
    """

    ATTRIBUTE_PAINT = 'sidefx_attribpaint'
    ROTATE = 'rotate'
    SCALE = 'scale'
    SCULPT = 'sculpt'
    SHOT_SCULPT = 'sidefx_shotsculpt'
    SOP_VIEW = 'sopview'
    STROKE = 'sidefx_stroke'
    TRANSLATE = 'translate'
    VELLUM_BRUSH = 'sidefx_vellumbrush'
    VIEW = 'view'
    VIEWS = (SOP_VIEW, VIEW)


class BuiltInIcon(cgp_generic_utils.python.BaseEnum):
    """enum of built-in viewer state icons
    """

    ATTRIBUTE_PAINT = 'SOP_attribpaint'
    PYTHON = 'MISC_python'
    VELLUM_BRUSH = 'SOP_vellumbrush'


class DesktopType(cgp_generic_utils.python.BaseEnum):
    """enum of desktop types
    """

    GENERIC = 'Generic'


class FileExtension(cgp_generic_utils.python.BaseEnum):
    """enum of file extensions
    """

    GENERIC = 'hip'
    LIMITED_COMMERCIAL = 'hiplc'
    NON_COMMERCIAL = 'hipnc'


class FloatingPanelType(cgp_generic_utils.python.BaseEnum):
    """enum of floating panel types
    """

    GENERIC = 'Generic'


class FolderType(cgp_generic_utils.python.BaseEnum):
    """enum of folder types
    """

    BORDERLESS = 'Borderless'
    COLLAPSIBLE = 'Collapsible'
    IMPORT_BLOCK = 'ImportBlock'
    MULTIPARM_BLOCK = 'MultiparmBlock'
    RADIO_BUTTONS = 'RadioButtons'
    SCROLLING_MULTIPARM_BLOCK = 'ScrollingMultiparmBlock'
    SIMPLE = 'Simple'
    TABBED_MULTIPARM_BLOCK = 'TabbedMultiparmBlock'
    TABS = 'Tabs'


class GeometryItemType(cgp_generic_utils.python.BaseEnum):
    """enum of geometry item types
    """

    EDITABLE = 'EditableGeometryItem'
    EDGE = 'Edge'
    FACE = 'Face'
    GENERIC = 'GenericGeometryItem'
    GEOMETRY = 'Global'
    POINT = 'Point'
    PRIMITIVE = 'Primitive'
    VERTEX = 'Vertex'
    VOLUME = 'Volume'
    PRIMITIVES = (FACE, PRIMITIVE, VOLUME)


class HotkeyContext(cgp_generic_utils.python.BaseEnum):
    """enum of hotkey contexts
    """

    ANIMATION_EDITOR = 'h.pane.chedit'
    BUNDLE_LIST = 'h.pane.bundle'
    CHANNEL_LIST = 'h.pane.chlist'
    CHOP_VIEWER = 'h.pane.chview'
    DATA_TREE = 'h.pane.datatree'
    DETAILS_VIEW = 'h.pane.details'
    GEOMETRY_VIEWERS = 'h.pane.gview'
    GROUPS = 'h.pane.group'
    HANDLE_LIST = 'h.pane.manip'
    IMAGE_VIEWER = 'h.pane.imgui'
    IPR_VIEWER = 'h.pane.ipr'
    LINK_EDITOR = 'h.pane.linkeditor'
    MAIN_PREFERENCES = 'h.pane.preferences'
    MATERIAL_PALETTE = 'h.pane.material'
    NETWORK_EDITOR = 'h.pane.wsheet'
    OPERATOR_TREE_CONTROLS = 'h.pane.optree'
    OPERATOR_TYPE_PROPERTIES = 'h.pane.editparms'
    ORBOLT_ASSET_BROWSER = 'h.pane.projectm'
    OUTPUTS_VIEWERS = 'h.pane.outputsview'
    PARAMETER_SPREADSHEET = 'h.pane.parmsheet'
    PARAMETERS = 'h.pane.parms'
    PERFORMANCE_MONITOR = 'h.pane.perfmon'
    PYTHON_SHELL = 'h.pane.pythonshell'
    SCENE_GRAPH_TREE = 'h.pane.scenegraphtree'
    SHADER_VIEWER = 'h.pane.shopview'
    TAKE_MANAGEMENT = 'h.pane.take'
    TEXTPORT = 'h.pane.textport'


class HotkeyType(cgp_generic_utils.python.BaseEnum):
    """enum of hotkey types
    """

    CONTEXT = 'hotkeyContext'
    HOTKEY = 'hotkey'


class MenuType(cgp_generic_utils.python.BaseEnum):
    """enum of menu types
    """

    CONTROL_NEXT = 'ControlNextParameter'
    MINI = 'Mini'
    NORMAL = 'Normal'
    STRING_REPLACE = 'StringReplace'
    STRING_TOGGLE = 'StringToggle'


class MiscType(cgp_generic_utils.python.BaseEnum):
    """enum of misc types
    """

    COLOR = 'Color'
    SCENE = 'Scene'


class NetworkItemType(cgp_generic_utils.python.BaseEnum):
    """enum of network item types
    """

    CONNECTION = 'Connection'
    GENERIC = 'Generic'
    NETWORK_BOX = 'NetworkBox'
    NETWORK_DOT = 'NetworkDot'
    NODE = 'Node'
    STICKY_NOTE = 'StickyNote'
    SUB_NETWORK_INDIRECT_INPUT = 'SubnetIndirectInput'


class NodeCategory(cgp_generic_utils.python.BaseEnum):
    """enum of node categories
    """

    CHOP = 'Chop'
    CHOP_NETWORK = 'ChopNet'
    COP = 'Cop2'
    COP_NETWORK = 'CopNet'
    DIRECTOR = 'Director'
    DOP = 'Dop'
    DRIVER = 'Driver'
    LOP = 'Lop'
    MANAGER = 'Manager'
    OBJ = 'Obj'
    SHOP = 'Shop'
    SOP = 'Sop'
    TOP = 'Top'
    TOP_NETWORK = 'TopNet'
    VOP = 'Vop'
    VOP_NETWORK = 'VopNet'


class NodeType(cgp_generic_utils.python.BaseEnum):
    """enum of node types
    """

    ATTRIBUTE_PAINT = 'attribpaint'
    ATTRIBUTE_WRANGLE = 'attribwrangle'
    MAP_POINTS = 'kinefx::mappoints'
    OUTPUT = 'output'
    RIG_MATCH_POSE = 'kinefx::rigmatchpose'
    SCULPT = 'sculpt'
    SUB_NETWORK = 'subnet'
    SWITCH = 'switch'
    VELLUM_BRUSH = 'vellumbrush'


class PaneTabType(cgp_generic_utils.python.BaseEnum):
    """enum of pane tab types
    """

    ASSET_BROWSER = 'AssetBrowser'
    BUNDLE_LIST = 'BundleList'
    CHANNEL_EDITOR = 'ChannelEditor'
    CHANNEL_LIST = 'ChannelList'
    CHANNEL_VIEWER = 'ChannelViewer'
    COMPOSITOR_VIEWER = 'CompositorViewer'
    CONTEXT_VIEWER = 'ContextViewer'
    DATA_TREE = 'DataTree'
    DETAILS_VIEW = 'DetailsView'
    ENGINE_SESSION_SYNC = 'EngineSessionSync'
    GENERIC = 'Generic'
    HANDLE_LIST = 'HandleList'
    HELP_BROWSER = 'HelpBrowser'
    IPR_VIEWER = 'IPRViewer'
    LIGHT_LINKER = 'LightLinker'
    MATERIAL_PALETTE = 'MaterialPalette'
    NETWORK_EDITOR = 'NetworkEditor'
    OUTPUT_VIEWER = 'OutputViewer'
    PARAMETER = 'Parm'
    PARAMETER_SPREADSHEET = 'ParmSpreadsheet'
    PERFORMANCE_MONITOR = 'PerformanceMonitor'
    PYTHON_PANEL = 'PythonPanel'
    PYTHON_SHELL = 'PythonShell'
    RENDER_GALLERY = 'RenderGallery'
    SCENE_VIEWER = 'SceneViewer'
    SHADER_VIEWER = 'ShaderViewer'
    TAKE_LIST = 'TakeList'
    TEXT_PORT = 'Textport'
    TREE_VIEW = 'TreeView'


class PaneType(cgp_generic_utils.python.BaseEnum):
    """enum of pane types
    """

    GENERIC = 'Generic'


class ParameterType(cgp_generic_utils.python.BaseEnum):
    """enum of parameter types
    """

    BASE = 'Base'
    BUTTON = 'Button'
    DATA = 'Data'
    FLOAT = 'Float'
    FOLDER = 'Folder'
    FOLDER_SET = 'FolderSet'
    GENERIC = 'Generic'
    INT = 'Int'
    LABEL = 'Label'
    MENU = 'Menu'
    PARAMETER_FOLDER = 'ParameterFolder'
    RAMP = 'Ramp'
    SEPARATOR = 'Separator'
    STRING = 'String'
    TOGGLE = 'Toggle'
    BASES = (BASE, BUTTON, FOLDER, FOLDER_SET, LABEL, SEPARATOR)
    VALUES = (DATA, FLOAT, GENERIC, INT, MENU, RAMP, STRING, TOGGLE)


class RotateOrder(cgp_generic_utils.python.BaseEnum):
    """enum of rotate orders
    """

    XYZ = 'xyz'
    XZY = 'xzy'
    YXZ = 'yxz'
    YZX = 'yzx'
    ZXY = 'zxy'
    ZYX = 'zyx'


class TransformationType(cgp_generic_utils.python.BaseEnum):
    """enum of transformation types
    """

    ROTATE = 'rotate'
    SCALE = 'scale'
    TRANSLATE = 'translate'


class ViewerStateType(cgp_generic_utils.python.BaseEnum):
    """enum of viewer state types
    """

    BASE = 'Base'
    BASE_NODE = 'BaseNode'
    NODE = 'Node'
    NODELESS = 'Nodeless'
    BUILT_IN = 'BuiltIn'
    BUILT_IN_PY = 'BuiltInPy'
    BUILT_IN_HDA = 'BuiltInHda'


class VisualizerCategory(cgp_generic_utils.python.BaseEnum):
    """enum of visualizer categories
    """

    COMMON = 'Common'
    NODE = 'Node'
    SCENE = 'Scene'


class VisualizerType(cgp_generic_utils.python.BaseEnum):
    """enum of visualizer types
    """

    CAPTURE_WEIGHT = 'vis_captureweight'
    COLOR = 'vis_color'
    CONSTRAINTS = 'vis_constraints'
    GENERIC = 'vis_generic'
    MARKER = 'vis_marker'
    TAG = 'vis_tag'
    VOLUME = 'vis_volume'
