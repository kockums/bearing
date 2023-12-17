# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Geospatial Grid Class

...

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
from array import *


# Import | Libraries
import geojson
import numpy


# Import | Local Modules
from bearing.geospatial.coordinate import GeographicCoordinate
from bearing.geospatial.area import GeographicArea





class GeographicGrid(object):
    """
    A class used to represent a Geographic Grid

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
        area =          None,
        resolution =    None,
        size =          None,
        step =          None,
        cells =         None,
        geojson_data =  None,
        ):
        """Constructor of the object."""

        # Construct | area parameter
        if area is not None:
            assert isinstance(area, GeographicArea)
        self._area = area

        # Construct | resolution parameter
        if resolution is not None:
            assert isinstance(resolution, tuple)
        self._resolution = resolution

        # Construct | size parameter
        self._size = size # move to area
        if area is not None:
            self.load_size()

        # Construct | step parameter
        self._step = step
        if area is not None:
            self.load_step()

        # Construct | cells parameter
        self._cells = cells
        if area is not None:
            self.load_cells()

        # Construct | geojson_data parameter
        self._geojson_data = geojson_data
        if area is not None:
            self.load_geojson()

    def __str__(self):
        """This method returns the string representation of the object."""
        return '<' + str(self.area) + ',' + str(self.resolution) + '>'

    def __eq__(self, other):
        """Operator to compare the instances of the class."""
        return self.area == other.area and self.resolution == other.resolution

    def __repr__(self):
        """Special method used to represent a class's objects as a string."""
        return "Coordinate(%d, %d)" % (self.area, self.resolution)


    # Methods | area parameter

    @property
    def area(self):
        """Getter decorator method for area parameter."""
        return self._area

    @area.setter
    def area(self, area):
        """Setter decorator method for area parameter."""
        assert isinstance(area, GeographicArea)
        self._area = area

    @area.deleter
    def area(self):
        """Deleter decorator method for area parameter."""
        del self._area


    # Methods | resolution parameter

    @property
    def resolution(self):
        """Getter decorator method for resolution parameter."""
        return self._resolution

    @resolution.setter
    def resolution(self, resolution):
        """Setter decorator method for resolution parameter."""
        self._resolution = resolution

    @resolution.deleter
    def resolution(self):
        """Deleter decorator method for resolution parameter."""
        del self._resolution


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

    def load_size(self):
        """Loader method for size parameter."""
        i_size = self._area.upperright.lat - self._area.lowerleft.lat
        j_size = self._area.upperright.lon - self._area.lowerleft.lon
        self._size = (i_size, j_size)


    # Methods | step parameter

    @property
    def step(self):
        """Getter decorator method for step parameter."""
        return self._step

    @step.setter
    def step(self, step):
        """Setter decorator method for step parameter."""
        self._step = step

    @step.deleter
    def step(self):
        """Deleter decorator method for step parameter."""
        del self._step

    def load_step(self):
        """Loader method for step parameter."""
        i_step = self._size[0] / self._resolution[0]
        j_step = self._size[1] / self._resolution[1]
        self._step = (i_step, j_step)


    # Methods | cells parameter

    @property
    def cells(self):
        """Getter decorator method for cells parameter."""
        return self._cells

    @cells.setter
    def cells(self, cells):
        """Setter decorator method for cells parameter."""
        # assert isinstance(cells, dict)
        self._cells = cells

    @cells.deleter
    def cells(self):
        """Deleter decorator method for cells parameter."""
        del self._cells

    def load_cells(self):
        """Loader method for cells parameter."""
        self._cells = [[0 for x in range(self._resolution[0])] for y in range(self._resolution[1])]
        for i in range(self._resolution[0]):
            ll_lat = self._area.lowerleft.lat + i * self._step[0]
            ur_lat = ll_lat + self._step[0]
            for j in range(self._resolution[1]):
                ll_lon = self._area.lowerleft.lon + i * self._step[1]
                ur_lon = ll_lon + self._step[1]
                ll = GeographicCoordinate(ll_lat, ll_lon)
                ur = GeographicCoordinate(ur_lat, ur_lon)
                cell = GeographicArea(ll, ur)
                self._cells[i][j] = cell


    # def set_cell(self, key, value):
    #     """Setter method for a single cell."""
    #     # assert isinstance(value, CellValue)
    #     self._cells[key] = value

    # def get_cell(self, key):
    #     """Getter method for a single cell."""
    #     return self._cells[key]

    # def del_cell(self, key):
    # # Deleter method for a single cell.
    #     del self._cells[key]



    # Methods | geojson_data parameter

    @property
    def geojson_data(self):
        """Getter decorator method for geojson_data parameter."""
        return self._geojson_data

    @geojson_data.setter
    def geojson_data(self, geojson_data):
        """Setter decorator method for geojson parameter."""
        # assert isinstance(geojson_data, geojson.Point)
        self._geojson_data = geojson_data

    @geojson_data.deleter
    def geojson_data(self):
        """Deleter decorator method for geojson_data parameter."""
        del self._geojson_data

    def load_geojson(self):
        """Loader method for geojson parameter."""
        feature_collection_list_columns = []
        for column in self._cells:
            feature_collection_list_rows = []
            for cell in column:
                data = cell.geojson_data
                feature_collection_list_rows.append(data)
            feature_collection_rows = geojson.FeatureCollection(feature_collection_list_rows)
            feature_collection_list_columns.append(feature_collection_rows)
        grid_feature = geojson.FeatureCollection(features=feature_collection_list_columns)
        self._geojson_data = grid_feature


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
