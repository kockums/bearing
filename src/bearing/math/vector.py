#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Vector Class

...

Examples:
    ...

Attributes:
    ...

Todo:

Links:


"""


# Import | Futures
# […]

# Import | Standard Library
import math
# […]

# Import | Libraries
import numpy
import matplotlib.pyplot as pyplot
from scipy.interpolate import Rbf
# […]

# Import | Local Modules
from bearing.geometry.point import Point
# […]



class Vector(object):
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    # overload []
    def __getitem__(self, index):
        data = [self.x,self.y,self.z]
        return data[index]

    # overload set []
    def __setitem__(self, key, item):
        if (key == 0):
            self.x = item
        elif (key == 1):
            self.y = item
        elif (key == 2):
            self.z = item
        #TODO: Default should throw excetion


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


# def AutoFloatProperties(*props):
#     '''metaclass'''
#     class _AutoFloatProperties(type):
#         # Inspired by autoprop (http://www.python.org/download/releases/2.2.3/descrintro/#metaclass_examples)
#         def __init__(cls, name, bases, cdict):
#             super(_AutoFloatProperties, cls).__init__(name, bases, cdict)
#             for attr in props:
#                 def fget(self, _attr='_'+attr): return getattr(self, _attr)
#                 def fset(self, value, _attr='_'+attr): setattr(self, _attr, float(value))
#                 setattr(cls, attr, property(fget, fset))
#     return _AutoFloatProperties

# class Vector(object, metaclass = AutoFloatProperties):
#     '''Creates a Maya vector/triple, having x, y and z coordinates as float values'''
#     __metaclass__ = AutoFloatProperties('x','y','z')
#     def __init__(self, x=0, y=0, z=0):
#         self.x, self.y, self.z = x, y, z # values converted to float via properties

# if __name__=='__main__':
#     v=Vector(1,2,3)
#     print(v.x)
#     # 1.0
#     v.x=4
#     print(v.x)
#     # 4.0
