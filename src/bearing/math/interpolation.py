#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Math Utils

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
from scipy.interpolate import Rbf

# […]

# Import | Local Modules
# […]


class InterpolateIWD:
    """"""


    # Static Methods

    @staticmethod
    def simple_idw(x, y, z, xi, yi):
        """ """
        dist = InterpolateIWD.distance_matrix(x,y, xi,yi)

        # In IDW, weights are 1 / distance
        weights = 1.0 / dist

        # Make weights sum to one
        weights /= weights.sum(axis=0)

        # Multiply the weights for each interpolated point by all observed Z-values
        zi = numpy.dot(weights.T, z)
        return zi


    @staticmethod
    def linear_rbf(x, y, z, xi, yi):
        """ """
        dist = InterpolateIWD.distance_matrix(x,y, xi,yi)

        # Mutual pariwise distances between observations
        internal_dist = InterpolateIWD.distance_matrix(x,y, x,y)

        # Now solve for the weights such that mistfit at the observations is minimized
        weights = numpy.linalg.solve(internal_dist, z)

        # Multiply the weights for each interpolated point by the distances
        zi =  numpy.dot(dist.T, weights)
        return zi


    @staticmethod
    def scipy_idw(x, y, z, xi, yi):
        """ """
        interp = Rbf(x, y, z, function='linear')
        return interp(xi, yi)


    @staticmethod
    def distance_matrix(x0, y0, x1, y1):
        """ """
        obs = numpy.vstack((x0, y0)).T
        interp = numpy.vstack((x1, y1)).T

        # Make a distance matrix between pairwise observations
        # Note: from <http://stackoverflow.com/questions/1871536>
        # (Yay for ufuncs!)
        d0 = numpy.subtract.outer(obs[:,0], interp[:,0])
        d1 = numpy.subtract.outer(obs[:,1], interp[:,1])

        return numpy.hypot(d0, d1)


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
