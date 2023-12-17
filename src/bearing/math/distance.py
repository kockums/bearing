# -*- coding: utf-8 -*-


"""
Provides Math Utils
===================

...

Examples:
    ...

Attributes:
    ...

Todo:

Links:


"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
import math


# Import | Libraries
import numpy
import matplotlib.pyplot as pyplot
from scipy.interpolate import Rbf


# Import | Local Modules
from bearing.geometry.point import Point
from bearing.math.vector import Vector




class Distance(Vector):
    """"""


    # Static Methods

    @staticmethod
    def distance_1d(_u, _v):
        """ """
        return math.abs(_u - _v)

    @staticmethod
    def distance_2d(_pt1, _pt2):
        """ """
        assert isinstance(_pt1, Point)
        assert isinstance(_pt2, Point)
        p1 = (_pt1.x, _pt1.y)
        p2 = (_pt2.x, _pt2.y)
        result = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        return result

    @staticmethod
    def distance_3d(_pt1, _pt2):
        """ """
        assert isinstance(_pt1, Point)
        assert isinstance(_pt2, Point)
        xd = _pt2.x - _pt1.x
        yd = _pt2.y - _pt1.y
        zd = _pt2.z - _pt1.z
        result = math.sqrt(xd * xd + yd * yd + zd * zd)
        return result

