# -*- coding: utf-8 -*-


"""
Provides Base Layer Class

...

Examples:
    ...

Attributes:
    ...

Todo:

"""


# Import | Futures


# Import | Standard Library


# Import | Libraries


# Import | Local Modules
from starling.geometry.point import Point
from starling.geometry.rectangle import Rectangle
from starling.geospatial.utils import coord_offset
from starling.math.utils import distance_1d



class Voxel_grid():
    """
    A class used to represent a Voxel Grid

    ...

    Attributes
    ----------


    Methods
    -------
    test()
        test method
    """

    def __init__(self, _center, _lat, _lon, _voxel_size, _voxel_min_x, _voxel_max_x, _voxel_min_y, _voxel_max_y, _voxel_min_z, _voxel_max_z):
        self.center = _center
        self.lat = _lat
        self.lon = _lon
        self.voxel_size = _voxel_size
        self.voxel_min_x = _voxel_min_x
        self.voxel_max_x = _voxel_max_x
        self.voxel_min_y = _voxel_min_y
        self.voxel_max_y = _voxel_max_y
        self.voxel_min_z = _voxel_min_z
        self.voxel_max_z = _voxel_max_z
        self.voxel_res_x = distance_1d(_voxel_min_x, _voxel_max_x)
        self.voxel_res_y = distance_1d(_voxel_min_y, _voxel_max_y)
        self.voxel_res_z = distance_1d(_voxel_min_z, _voxel_max_z)
        self.coordinates = self.base_coordinates()
        self.pt_list = []

    def __str__(self):
        return "voxel grid loaded!"

    def points(self):
        for z in range(self.voxel_min_z, self.voxel_max_z):
            progress = float(z) / float(self.voxel_res_z) * 100.0
            print ("voxel init progress:    {0:.2f}%...".format(progress))
            for y in range(self.voxel_min_y, self.voxel_max_y):
                for x in range(self.voxel_min_x, self.voxel_max_x):
                    if x <= 0: oid_x = "0{0:03d}".format(abs(x))
                    else: oid_x = "1{0:03d}".format(x)
                    if y <= 0: oid_y = "0{0:03d}".format(abs(y))
                    else: oid_y = "1{0:03d}".format(y)
                    if z <= 0: oid_z = "0{0:03d}".format(abs(z))
                    else: oid_z = "1{0:03d}".format(z)
                    oid = oid_x + oid_y + oid_z
                    pt_x = self.center.x + x * self.voxel_size
                    pt_y = self.center.y + y * self.voxel_size
                    pt_z = self.center.z + z * self.voxel_size

                    pt = Point(pt_x, pt_y, pt_z)
                    ll_dx = distance_1d(self.center.x, pt.x) / 1000
                    ll_dy = distance_1d(self.center.y, pt.y) / 1000
                    coord = coord_offset(self.center, self.lat, self.lon, ll_dx, ll_dy).calc()
                    com = [oid, x, y, z, pt.x, pt.y, pt.z, coord[0], coord[1], ll_dx, ll_dy]
                    self.pt_list.append(com)

    def base(self):
        ll = Point(self.center.x + self.voxel_min_x * self.voxel_size, self.center.y + self.voxel_min_y * self.voxel_size, self.center.z + self.voxel_min_z * self.voxel_size)
        ur = Point(self.center.x + self.voxel_max_x * self.voxel_size, self.center.y + self.voxel_max_y * self.voxel_size, self.center.z + self.voxel_min_z * self.voxel_size)
        return Rectangle(ll, ur)

    def boundary(self):
        ll = Point(self.center.x + self.voxel_min_x * self.voxel_size, self.center.y + self.voxel_min_y * self.voxel_size, self.center.z + self.voxel_max_z * self.voxel_size)
        ur = Point(self.center.x + self.voxel_max_x * self.voxel_size, self.center.y + self.voxel_max_y * self.voxel_size, self.center.z + self.voxel_max_z * self.voxel_size)
        bas = self.base()
        top = Rectangle(ll, ur)
        return [bas, top]

    def base_coordinates(self):
        ll_dx = self.voxel_size * self.voxel_min_x / 1000
        ll_dy = self.voxel_size * self.voxel_min_y / 1000
        coord_ll = coord_offset(self.center, self.lat, self.lon, ll_dy, ll_dx).calc()
        ur_dx = self.voxel_size * self.voxel_max_x / 1000
        ur_dy = self.voxel_size * self.voxel_max_y / 1000
        coord_ur = coord_offset(self.center, self.lat, self.lon, ur_dy, ur_dx).calc()
        return coord_ll, coord_ur


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
