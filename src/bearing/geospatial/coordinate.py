# -*- coding: utf-8 -*-


"""
Provides Geospatial Coordinate Class

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
import math
# […]

# Import | Libraries
from pyproj import Proj, Transformer
import geojson
# […]

# Import | Local Modules
# […]


class GeographicCoordinate(object):
    """
    A class used to represent a Geographic Coordinate

    ...

    Attributes
    ----------
    lat : float
        the latitude component of the Geographic Coordinate
    lon : float
        the longitude component of the Geographic Coordinate
    h : float
        the height component of the Geographic Coordinate


    Methods
    -------
    test()
        test method
    """

    # Magic Methods

    def __init__(
        self,
        lat,
        lon,
        height=0.0,
    ):
        """Constructor of the object."""

        # Construct | lat parameter
        assert isinstance(lat, float)
        self._lat = lat

        # Construct | lon parameter
        assert isinstance(lon, float)
        self._lon = lon

        # Construct | height parameter
        assert isinstance(height, float)
        self._height = height

        # Construct | geojson_data parameter
        self._geojson_data = self.load_geojson()

    # def __str__(self):
    # # This method returns the string representation of the object.
    #     return '<' + str(self.lat) + ',' + str(self.lon) + ',' + str(self.h) + '>'

    # def __eq__(self, other):
    # # Operator to compare the instances of the class
    #     return self.lat == other.lat and self.lon == other.lon and self.h == other.h

    # def __repr__(self):
    # # Special method used to represent a class's objects as a string
    #     return "Coordinate(%d, %d, %d)" % (self.lat, self.lon, self.h)

    # Class Methods

    @classmethod
    def from_tuple(cls, t):
        """Class method to create Geographic Coordinate object by tuple"."""
        assert t >= 2 and t <= 3
        if len(t) == 2:
            return cls(lat=t[0], lon=t[1])
        elif len(t) == 3:
            return cls(lat=t[0], lon=t[1], h=t[2])

    def to_tuple(self):
        """"""
        return (self._lat, self._lon, self._height)

    # Static Methods

    @staticmethod
    def rd2wgs(x, y):
        """"""
        RD2WGS = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        lon, lat = RD2WGS.transform(x, y)
        return {"lon": lon,
                "lat": lat}

    @staticmethod
    def wgs2rd(lon, lat):
        """"""
        WGS2RD = Transformer.from_crs("EPSG:4326", "EPSG:28992")
        x, y = WGS2RD.transform(lon, lat)
        return {"x": x,
                "y": y}

    @staticmethod
    def coord_offset(latIn, lonIn, dx, dy):
        """"""
        base = GeographicCoordinate.wgs2rd(lonIn, latIn)
        base["x"] += dx
        base["y"] += dy
        lonlat = GeographicCoordinate.rd2wgs(base["x"], base["y"])
        return lonlat

    @staticmethod
    def coord_offset_alt(_lat, _lon, _offset_n, _offset_e):
        """"""
        earth_radius = 6378137.0
        dif_lat = _offset_n / earth_radius
        dif_lon = _offset_e / (earth_radius * math.cos(math.pi * _lat / 180))
        lat_off = _lat + dif_lat * 180 / math.pi
        lon_off = _lon + dif_lon * 180 / math.pi
        lat_for = float("%.10f" % lat_off)
        lon_for = float("%.10f" % lon_off)
        return (lat_for, lon_for)

    # Methods | lat parameter

    @property
    def lat(self):
        """Getter decorator method for lat parameter."""
        return self._lat

    @lat.setter
    def lat(self, lat):
        """Setter decorator method for lat parameter."""
        self._lat = lat

    @lat.deleter
    def lat(self):
        """Deleter decorator method for lat parameter."""
        del self._lat

    # Methods | lon parameter

    @property
    def lon(self):
        """Getter decorator method for lon parameter."""
        return self._lon

    @lon.setter
    def lon(self, lon):
        """Setter decorator method for lon parameter."""
        self._lon = lon

    @lon.deleter
    def lon(self):
        """Deleter decorator method for lon parameter."""
        del self._lon

    # Methods | height parameter

    @property
    def height(self):
        """Getter decorator method for height parameter."""
        return self._height

    @height.setter
    def height(self, height):
        """Setter decorator method for height parameter."""
        self._height = height

    @height.deleter
    def height(self):
        """Deleter decorator method for height parameter."""
        del self._height

    # Methods | lowerleft parameter

    @property
    def geojson_data(self):
        """Getter decorator method for geojson_data parameter."""
        return self._geojson_data

    @geojson_data.setter
    def geojson_data(self, geojson_data):
        """Setter decorator method for geojson parameter."""
        assert isinstance(geojson_data, geojson.Point)
        self._geojson_data = geojson_data

    def load_geojson(self):
        """Loader method for geojson_data parameter."""
        geojson_data = geojson.Point((self.lat, self.lon))
        return geojson_data

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
