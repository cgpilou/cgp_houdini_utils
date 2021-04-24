"""
constants used to manipulate houdini data
"""


class RotateOrder(object):
    XYZ = 'xyz'
    XZY = 'xzy'
    YXZ = 'yxz'
    YZX = 'yzx'
    ZXY = 'zxy'
    ZYX = 'zyx'
    ALL = [XYZ, XZY, YXZ, YZX, ZXY, ZYX]
