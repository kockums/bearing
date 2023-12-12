# -*- coding: utf-8 -*-


"""
Provides Grid Class

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
from bearing.geometry.rectangle import Rectangle
# […]



class Grid(object):
    """
    A class used to represent a Grid

    ...

    Attributes
    ----------


    Methods
    -------
    test()
        test method
    """

    def __init__(self, name):
        self._name = str(name)
        self._grid = []

    def __str__(self):
        return "Grid: {0}".format(self._name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def grid(self):
        return self._grid

    @name.setter
    def grid(self, grid):
        self._grid = grid


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
