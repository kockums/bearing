#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Rectangle Class

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




class Rectangle(object):
    """
    A class used to represent a Rectangle

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
        pt_ll,
        pt_ur
        ):
        """"""
        assert isinstance(pt_ll, Point)
        assert isinstance(pt_ur, Point)
        self._ll = pt_ll
        self._ur = pt_ur
        self._lr = Point(self._ur.x, self._ll.y, self._ll.z)
        self._ul = Point(self._ll.x, self._ur.y, self._ll.z)

    def __str__(self):
        """"""
        return "Rectangle(({0} {1}, {2} {3}, {4} {5}, {6} {7}, {8} {9}))".format(self.ll.x, self.ll.y, self.ur.x, self.ur.y, self.ur.x, self.ur.y, self.ll.x, self.ur.y, self.ll.x, self.ll.y)


    def size_x(self):
        """"""
        if self.ll.x >= self.ur.x:
            return float(self.ll.x - self.ur.x)
        else:
            return float(self.ur.x - self.ll.x)

    def size_y(self):
        """"""
        if self.ll.y >= self.ur.y:
            return float(self.ll.y - self.ur.y)
        else:
            return float(self.ur.y - self.ll.y)


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
