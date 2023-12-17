# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Geospatial Area Class
==============================


Examples:
    ...

Attributes:
    ...

Todo:

"""

# =============================================================================
# Import
# =============================================================================

# Import | Standard Library

# Import | Libraries
import geojson

# Import | Local Modules
from bearing.geospatial.coordinate import GeographicCoordinate


# =============================================================================
# Classes
# =============================================================================

class GeographicArea(object):
    """

    A class used to represent a Geographic Area

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
        lowerleft = None,
        upperright = None,
        size = None,
        ):
        """Constructor of the object."""

        # Construct | lowerleft parameter
        if lowerleft is not None:
            assert isinstance(lowerleft, GeographicCoordinate)
        self._lowerleft = lowerleft

        # Construct | upperright parameter
        if upperright is not None:
            assert isinstance(upperright, GeographicCoordinate)
        self._upperright = upperright

        # Construct | lowerright and upperleft parameter
        if isinstance(lowerleft, GeographicCoordinate) and isinstance(upperright, GeographicCoordinate):
            self._lowerright = GeographicCoordinate(self._upperright.lat, self._lowerleft.lon, self._lowerleft.height)
            self._upperleft = GeographicCoordinate(self._lowerleft.lat, self._upperright.lon, self._lowerleft.height)

        # Construct | center parameter
        self._center = GeographicCoordinate(
            (upperright.lat + lowerleft.lat) / 2,
            (upperright.lon + lowerleft.lon) / 2,
        )
        # self.load_size()
        self._size = size
        self._geojson_data = self.load_geojson()


    # def __str__(self):
    #     """This method returns the string representation of the object."""
    #     return '<' + str(self.lowerleft) + ',' + str(self.upperright) + '>'

    # def __eq__(self, other):
    #     """Operator to compare the instances of the class"""
    #     return self.lowerleft == other.lowerleft and self.upperright == other.upperright

    # def __repr__(self):
    #     """Special method used to represent a class's objects as a string"""
    #     return "Area(%d, %d)" % (self.lowerleft, self.upperright)


    # Class Methods
    # =========================================================================

    @classmethod
    def from_tuple(cls, t):
        """Class method to create Geographic Coordinate object by tuple."""
        assert t == 4
        lowerleft = GeographicCoordinate.from_tuple((t[0], t[1]))
        upperright = GeographicCoordinate.from_tuple((t[2], t[3]))
        return cls(lowerleft=lowerleft, upperright=upperright)

    def to_tuple(self):
        """"""
        return (self._lowerleft.to_tuple(), self._upperright.to_tuple())


    @classmethod
    def from_center_size(cls, center, size):
        """Class method to create Geographic Coordinate object by center and size."""
        assert isinstance(center, GeographicCoordinate)
        assert isinstance(size, tuple)
        dx = size[0] / 2
        dy = size[1] / 2
        ll = GeographicCoordinate.coord_offset_alt(center.lat, center.lon, -dy, -dx)
        ur = GeographicCoordinate.coord_offset_alt(center.lat, center.lon, +dy, +dx)
        lowerleft =  GeographicCoordinate(ll[0], ll[1])
        upperright = GeographicCoordinate(ur[0], ur[1])
        return cls(lowerleft=lowerleft, upperright=upperright, size=size)

    # Methods | lowerleft parameter

    @property
    def lowerleft(self):
        """Getter decorator method for lowerleft parameter."""
        return self._lowerleft

    @lowerleft.setter
    def lowerleft(self, lowerleft):
        """Setter decorator method for lowerleft parameter."""
        assert isinstance(lowerleft, GeographicCoordinate)
        self._lowerleft = lowerleft

    @lowerleft.deleter
    def lowerleft(self):
        """Deleter decorator method for lowerleft parameter."""
        del self._lowerleft


    # Methods | upperright parameter

    @property
    def upperright(self):
        """Getter decorator method for upperright parameter."""
        return self._upperright

    @upperright.setter
    def upperright(self, upperright):
        """Setter decorator method for upperright parameter."""
        assert isinstance(upperright, GeographicCoordinate)
        self._upperright = upperright

    @upperright.deleter
    def upperright(self):
        """Deleter decorator method for upperright parameter."""
        del self._upperright


    # Methods | lowerright parameter

    @property
    def lowerright(self):
        """Getter decorator method for lowerright parameter."""
        return self._lowerright

    @lowerright.deleter
    def lowerright(self):
        """Deleter decorator method for lowerright parameter."""
        del self._lowerright


    # Methods | upperleft parameter

    @property
    def upperleft(self):
        """Getter decorator method for upperleft parameter."""
        return self._upperleft

    @upperleft.deleter
    def upperleft(self):
        """Deleter decorator method for upperleft parameter."""
        del self._upperleft


    # Methods | center parameter

    @property
    def center(self):
        """Getter decorator method for center parameter."""
        return self._center

    @center.setter
    def center(self, center):
        """Setter decorator method for center parameter."""
        assert isinstance(center, GeographicCoordinate)
        self._center = center

    @center.deleter
    def center(self):
        """Deleter decorator method for center parameter."""
        del self._center


    # Methods | size parameter

    @property
    def size(self):
        """Getter decorator method for size parameter."""
        return self._size

    @size.setter
    def size(self, size):
        """Setter decorator method for size parameter."""
        self._size = size

    @size.deleter
    def size(self):
        """Deleter decorator method for size parameter."""
        del self._size

    def load_size_deg(self):
        """Loader method for size parameter."""
        i_size = self.upperright.lat - self.lowerleft.lat
        j_size = self.upperright.lon - self.lowerleft.lon
        return (i_size, j_size)
        # self._size = (i_size, j_size)


    # Methods | geojson_data parameter

    @property
    def geojson_data(self):
        """Getter decorator method for geojson_data parameter."""
        return self._geojson_data

    @geojson_data.setter
    def geojson_data(self, geojson_data):
        """Setter decorator method for geojson_data parameter."""
        assert isinstance(geojson_data, geojson.Polygon)
        self._geojson_data = geojson_data

    @geojson_data.deleter
    def geojson_data(self):
        """Deleter decorator method for geojson_data parameter."""
        del self._geojson_data

    def load_geojson(self):
        """Loader method for geojson_data parameter."""
        area = geojson.Polygon([[
            (self.lowerleft.lat, self.lowerleft.lon),
            (self.upperleft.lat, self.upperleft.lon),
            (self.upperright.lat, self.upperright.lon),
            (self.lowerright.lat, self.lowerright.lon),
            ]])
        area_feat = geojson.Feature(geometry=area)
        vertices = geojson.FeatureCollection([
            self.lowerleft.geojson_data,
            self.upperleft.geojson_data,
            self.upperright.geojson_data,
            self.lowerright.geojson_data,
            ])
        vertices_feat = geojson.Feature(geometry=vertices)
        center = self.center.geojson_data
        center_feat = geojson.Feature(geometry=center)
        geojson_data = geojson.FeatureCollection([
            area_feat,
            vertices_feat,
            center_feat,
            ])
        return geojson_data

