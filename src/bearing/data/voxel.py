#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Voxel Class

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
from starling.geometry.point import Point
# […]


class Voxel(object):
    '''
    '''

    def __init__(self, _oid, _name, _location, _value):
        assert isinstance(_location, Point)
        assert isinstance(_value, Color)
        self.oid = int(_oid)
        self.name = str(_name)
        self.location = _location
        self.value = _value

    def __str__(self):
        return "Voxel({0} {1} {2}) Parameters({3} {4} {5})".format(self.x, self.y, self.z, self.a, self.b, self.c)


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
