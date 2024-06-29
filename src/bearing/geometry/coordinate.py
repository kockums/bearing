# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Coordinate Class
=========================

...

Examples:
    ...

Attributes:
    ...

Todo:

"""


# =============================================================================
# Import
# =============================================================================

# Import | Standard Library

# Import | Libraries

# Import | Local Modules


# =============================================================================
# Classes
# =============================================================================

class Coordinate(object):
    """
    Coordinate Class
    ================

    A class used to represent a Coordinate

    ...

    Attributes
    ----------


    Methods
    -------
    test()
        test method
    """

    def __init__(
        self,
        x,
        y,
        z
    ):
        """ """
        self._x = x
        self._y = y
        self._z = z

    def __str__(self):
        """ """
        return '<' + str(self.x()) + ',' + str(self.y()) + ',' + str(self.z()) + '>'

    def __eq__(self, other):
        """ """
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        """ """
        return "Coordinate(%d, %d, %d)" % (self.x, self.y, self.z)

    @property
    def x(self):
    # Getter method for a Coordinate object's x coordinate.
        return self._x

    @x.setter
    # Setter method for a Coordinate object's x coordinate.
    def x(self, x):
        self._x = x

    @property
    def y(self):
    # Getter method for a Coordinate object's y coordinate.
        return self._y

    @y.setter
    # Setter method for a Coordinate object's y coordinate.
    def y(self, y):
        self._y = y

    @property
    def z(self):
    # Getter method for a Coordinate object's x coordinate.
        return self._z

    @z.setter
    # Setter method for a Coordinate object's x coordinate.
    def z(self, z):
        self._z = z

