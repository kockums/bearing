# -*- coding: utf-8 -*-
# flake8: noqa


"""
Provides Point Class

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
from math import sqrt
# […]

# Import | Libraries
# […]

# Import | Local Modules
# […]



class Point(object):
    """
    A class used to represent a Point

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
        *args,
        **kwargs
        ):
        '''Defines x, y and z variables'''
        self._x = float(args[0])
        self._y = float(args[1])
        self._z = args[2]
        if args[2] is not None:
            self.z = float(_z)
        else:
            self.z = float(0.0)
        self._coord = (self.x, self.y, self.z)



    def __str__(self):
        return "Point({0} {1} {2})".format(self.x, self.y, self.z)

    def __repr__(self):
        return '{p.__class__.__name__}({p!s})'.format(p=self)

    def __add__(self, other):
        """
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __sub__(self, other):
        """
        """
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    @property
    def x(self):
        """
        Returns the X coordinate of the Point.
        """
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        """
        Returns the Y coordinate of the Point.
        """
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        """
        Returns the Z coordinate of the Point.
        """
        return self._z

    @z.setter
    def z(self, z):
        if z is not None:
            self._z = float(z)
        else:
            self._z = float(0.0)
        self.coord = (self._x, self._y, self._z)

    def translate(self, dx, dy, dz):
        """
        Shift the Point by adding x and y to the coordinates of the Point.
        """
        self._x += dx
        self._y += dy
        self._z += dz

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return sqrt(dx**2 + dy**2 + dz**2)


    # Methods | test

    def test_something(self):
        """Test Method"""
        pass






def test():
    p1 = Point(1, 1, 1)
    p2 = Point(2, 3, 4)

    print(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z)
    print(p1.distance(p2))

    p2.translate(5,6,7)

    print(p2)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    test()
