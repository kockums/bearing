#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Box Class

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
from bearing.geometry.point import Point
# […]



class Box(object):
    """
    A class used to represent a Box

    ...

    Attributes
    ----------


    Methods
    -------
    test()
        test method
    """

    def __init__(self, pt_a, pt_b):
        assert isinstance(pt_a, Point)
        assert isinstance(pt_b, Point)
        self._a = pt_a
        self._b = pt_b

    def __str__(self):
        return "Box(({0}, {1}, {2}))".format(self.size_x, self.size_y, self.size_z)



    def size_x(self):
        if self.a.x >= self.b.x:
            return float(self.a.x - self.b.x)
        else:
            return float(self.b.x - self.a.x)

    def size_y(self):
        if self.a.y >= self.b.y:
            return float(self.a.y - self.b.y)
        else:
            return float(self.b.y - self.a.y)

    def size_z(self):
        if self.a.z >= self.b.z:
            return float(self.a.z - self.b.z)
        else:
            return float(self.b.z - self.a.z)


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
