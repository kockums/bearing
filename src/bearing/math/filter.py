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
# […]

# Import | Local Modules
# […]




class FilterGaussian:
    """"""


    # Static Methods

    @staticmethod
    def matlab_style_gauss2D(shape=(3,3),sigma=0.5):
        """
        2D gaussian mask - should give the same result as MATLAB's
        fspecial('gaussian',[shape],[sigma])
        https://stackoverflow.com/questions/17190649/how-to-obtain-a-gaussian-filter-in-python
        """
        m,n = [(ss-1.)/2. for ss in shape]
        y,x = numpy.ogrid[-m:m+1,-n:n+1]
        h = numpy.exp( -(x*x + y*y) / (2.*sigma*sigma) )
        h[ h < numpy.finfo(h.dtype).eps*h.max() ] = 0
        sumh = h.sum()
        if sumh != 0:
            h /= sumh
        return h


    @staticmethod
    def fspecial_gauss(size, sigma):

        """Function to mimic the 'fspecial' gaussian MATLAB function
        """

        x, y = numpy.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]
        g = numpy.exp(-((x**2 + y**2)/(2.0*sigma**2)))
        return g/g.sum()


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
