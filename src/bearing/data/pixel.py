#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Pixel Class

...

Examples:
    ...

Attributes:
    ...

Todo:

"""


# Import | Futures
# […]

# Import | Standard Library
# […]

# Import | Libraries
# […]

# Import | Local Modules
from starling.data.colour import Colour
from starling.geometry.point import Point
# […]


class Pixel(object):
    """
    A class used to represent a Pixel

    ...

    Attributes
    ----------


    Methods
    -------
    test()
        test method
    """

    def __init__(self, _oid, _name, _location, _value):
        """"""
        assert isinstance(_location, Point)
        assert isinstance(_value, Colour)
        self.oid = int(_oid)
        self.name = str(_name)
        self.location = _location
        #self.size = int(3)
        #self.shape = Rectangle...
        self.value = _value

    def __str__(self):
        """"""
        return "Pixel: Location({0} {1} {2}) Value({3} {4} {5} {6}) \n".format(self.location.x, self.location.y, self.location.z, self.value.r, self.value.g, self.value.b, self.value.a)

    def position(self):
        """"""
        return (self.location)

    def value(self):
        """"""
        return (self.value)


    # Methods | test

    def test_something(self):
        """Test Method"""
        pass


def test():
    """Test Function"""
    pass


if __name__ == '__main__':
    """Main"""
    import doctest
    doctest.testmod()
    test()
