#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Colour Class

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
# […]





class Colour(object):
    """
    A class used to represent a Colour

    ...

    Attributes
    ----------


    Methods
    -------
    test()
        test method

    """


    # Magic Methods

    def __init__(
        self,
        r,
        g,
        b):
        """Constructor of the object."""
        self._r = int(r)
        self._g = int(g)
        self._b = int(b)
        self._a = 100

    def __str__(self):
        """This method returns the string representation of the object."""
        return "Color({0} {1} {2} {3})".format(self._r, self._g, self._b, self._a)


    # Static Methods

    @staticmethod
    def rgb_to_hex(rgb_tuple):
        """"""
        #hex = '#%02x%02x%02x' % (rgb_tuple)
        hex = "#{0:02x}{1:02x}{2:02x}".format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        return hex

    @staticmethod
    def rgb_to_hsv(rgb_tuple):
        """"""
        rgb = rgb_tuple
        r, g, b, a = rgb
        # Compute the H value by finding the maximum of the RGB values
        rgb_max = max(rgb)
        rgb_min = min(rgb)
        # Compute the value
        v = rgb_max
        if v == 0:
            h = s = 0
            return (h,s,v)
        # Compute the saturation value
        s = 255 * (rgb_max - rgb_min) // v
        if s == 0:
            h = 0
            return (h, s, v)
        # Compute the Hue
        if rgb_max == r:
            h = 0 + 43*(g - b)//(rgb_max - rgb_min)
        elif rgb_max == g:
            h = 85 + 43*(b - r)//(rgb_max - rgb_min)
        else: # RGB_MAX == B
            h = 171 + 43*(r - g)//(rgb_max - rgb_min)
        return (h, s, v)

    @staticmethod
    def hex_to_hsv(hex_value):
        """"""
        hex_value = hex_value.lstrip("#")
        r, g, b = (int(hex_value[i:i+2], 16) / 255.0 for i in xrange(0,5,2))
        return colorsys.rgb_to_hsv(r, g, b)



    def value(self):
        """"""
        return (self._r, self._g, self._b, self._a)



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
