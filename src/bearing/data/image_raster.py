#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Raster Image Class

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
from io import StringIO
from io import BytesIO
# […]

# Import | Libraries
from PIL import Image
# […]

# Import | Local Modules
# […]



class ImageRaster(object):
    """
    A class used to represent a Raster Image.

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
        image_data =    None,
        resolution =    (512, 512),
        mode =          "RGBA",
        background =    (0, 0, 0, 0),
        ):
        """Constructor of the object."""

        # Construct | image_data parameter
        self._image_data = image_data

        # Construct | resolution parameter
        assert isinstance(resolution, tuple)
        self._resolution = resolution

        # Construct | mode parameter
        assert isinstance(mode, str)
        self._mode = mode

        # Construct | background parameter
        assert isinstance(background, tuple)
        self._background = background

        self.new()

    def __str__(self):
        """"""
        return """Image with Size: {0}, {1}
        """.format(self.resolution[0], self.resolution[1])


    # Methods | image_data parameter

    @property
    def image_data(self):
        """Getter decorator method for image_data parameter."""
        return self._image_data

    @image_data.setter
    def image_data(self, image_data):
        """Setter decorator method for image_data parameter."""
        self._image_data = image_data

    @image_data.deleter
    def image_data(self):
        """Deleter decorator method for image_data parameter."""
        del self._image_data


    # Methods | resolution parameter

    @property
    def resolution(self):
        """Getter decorator method for resolution parameter."""
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        """Setter decorator method for resolution parameter."""
        assert isinstance(resolution, tuple)
        self._resolution = resolution

    @resolution.deleter
    def center(self):
        """Deleter decorator method for resolution parameter."""
        del self._resolution


    # Methods | mode parameter

    @property
    def mode(self):
        """Getter decorator method for mode parameter."""
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Setter decorator method for mode parameter."""
        assert isinstance(mode, str)
        self._mode = mode

    @mode.deleter
    def mode(self):
        """Deleter decorator method for mode parameter."""
        del self._mode


    # Methods | background parameter

    @property
    def background(self):
        """Getter decorator method for background parameter."""
        return self._background

    @background.setter
    def background(self, background):
        """Setter decorator method for background parameter."""
        assert isinstance(background, tuple)
        self._background = background

    @background.deleter
    def background(self):
        """Deleter decorator method for background parameter."""
        del self._background


    # Methods | operations

    def new(self):
        """"""
        image_new =  Image.new(self.mode, self.resolution, self.background)
        self.image_data = image_new

    def add_layer(self, layer, offset=(0,0)):
        """"""
        # image = Image.open(self.image_data)
        # image.paste(layer, offset, mask=layer)
        # image.save(self.image_data)
                    # image_new.paste(image_data)

        # self.image_data.paste(layer, offset, mask=layer)
        self.image_data.paste(layer, offset,)

    def show(self):
        """"""
        # image = Image.open(self.image_data)
        self.image_data.show()

    def save(self, path):
        """"""
        # image = Image.open(self.image_data)
        self.image_data.save(path)


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
