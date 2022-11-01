#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Provides Vector Class

...

Todo:

Links:


"""


# Import | Futures
from __future__ import annotations
# […]

# Import | Standard Library
import math
# […]

# Import | Libraries
# import numpy
# import matplotlib.pyplot as pyplot
# from scipy.interpolate import Rbf
# […]

# Import | Local Modules
# from bearing.geometry.point import Point
# […]



class Vector(object):
    """
    A vector is defined by XYZ components and a homogenisation factor.

    Parameters
    ----------
    x : float
        The X component of the vector.
    y : float
        The Y component of the vector.
    z : float
        The Z component of the vector.

    Attributes
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float
        The Z coordinate of the point.
    length : float, read-only
        The length of this vector.

    Examples
    --------
    >>> u = Vector(1, 0, 0)
    >>> v = Vector(0, 1, 0)
    >>> u
    Vector(1.000, 0.000, 0.000)
    >>> v
    Vector(0.000, 1.000, 0.000)
    >>> u.x
    1.0
    >>> u[0]
    1.0
    >>> u.length
    1.0
    >>> u + v
    Vector(1.000, 1.000, 0.000)
    >>> u + [0.0, 1.0, 0.0]
    Vector(1.000, 1.000, 0.000)
    >>> u * 2
    Vector(2.000, 0.000, 0.000)
    >>> u.dot(v)
    0.0
    >>> u.cross(v)
    Vector(0.000, 0.000, 1.000)
    """


    # =========================================================================
    # Methods | Constructors
    # =========================================================================

    __slots__ = ["_x", "_y", "_z"]

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        **kwargs
        ) -> None:
        """Constructor of the Vector object."""
        super(Vector, self).__init__(**kwargs)
        self.x = x
        self.y = y
        self.z = z


    # =========================================================================
    # Methods | Properties
    # =========================================================================


    # Methods | Properties | x parameter
    # -------------------------------------------------------------------------

    @property
    def x(self) -> float:
        """Getter decorator method for x parameter."""
        return self._x

    @x.setter
    def x(self, x: int | float):
        """Setter decorator method for x parameter."""
        assert isinstance(x, (int, float), msg = "x must be int or float")
        self._x = float(x)

    @x.deleter
    def x(self):
        """Deleter decorator method for x parameter."""
        del self._x


    # Methods | Properties | y parameter
    # -------------------------------------------------------------------------

    @property
    def y (self) -> float:
        """Getter decorator method for y parameter."""
        return self._y

    @y.setter
    def y (self, y: int | float):
        """Setter decorator method for y parameter."""
        assert isinstance(y, (int, float), msg = "y must be int or float")
        self._y = float(y)

    @y.deleter
    def y (self):
        """Deleter decorator method for y parameter."""
        del self._y


    # Methods | Properties | z parameter
    # -------------------------------------------------------------------------

    @property
    def z (self) -> float:
        """Getter decorator method for z parameter."""
        return self._z

    @z.setter
    def z (self, z: int | float):
        """Setter decorator method for z parameter."""
        assert isinstance(z, (int, float), msg = "z must be int or float")
        self._z = float(z)

    @z.deleter
    def z (self):
        """Deleter decorator method for z parameter."""
        del self._z


    # Methods | Properties | length parameter
    # -------------------------------------------------------------------------

    @property
    def length(self) -> float:
        return length_vector(self)



    # =========================================================================
    # Methods | Magic
    # =========================================================================

    # overload []
    def __getitem__(self, index):
        """
        Returns the ith Cartesian coordinate of self.
        """

        data = [self.x, self.y, self.z]
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

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z
        raise KeyError

    def __setitem__(self, key, value):
        i = key % 3
        if i == 0:
            self.x = value
            return
        if i == 1:
            self.y = value
            return
        if i == 2:
            self.z = value
            return
        raise KeyError


    # Return a string representation of self.
    def __str__(self):
        return str(self._coords)


    def __repr__(self):
        return str(self.values)

    def __repr__(self):
        return "Vector({0:.{3}f}, {1:.{3}f}, {2:.{3}f})".format(self.x, self.y, self.z, PRECISION[:1])


    # Methods | Magic | Basic
    # -------------------------------------------------------------------------


    # Return the dimension of self.
    def __len__(self):
        return self._n

    def __len__(self):
        return len(self.values)


    def __len__(self):
        """
        """
        return 3




    def __iter__(self):
        return iter([self.x, self.y, self.z])


    def __eq__(self, other: Vector) -> bool:
        """
        Is this vector equal to the other vector?

        Two vectors are considered equal if their XYZ components are identical.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The vector to compare.

        Returns
        -------
        bool
            True if the vectors are equal.
            False otherwise.

        """
        assert isinstance(other, Vector, msg = "other must be of type: Vector")
        _ = self.x == other.x and self.y == other.y and self.z == other.z
        return _


    # Methods | Magic | Unary
    # -------------------------------------------------------------------------



    def __neg__(self):
        """
        """
        return self.scaled(-1.0)

    # __abs__(self)
    # __invert__(self)
    # __pos__(self)

    # Methods | Magic | Additions
    # -------------------------------------------------------------------------

    def __add__(self, other: Vector | int | float | tuple | list) -> Vector:
        """
        Returns the vector addition of self and other
        Return a vector that is the the sum of this vector and another vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The other to add to self.

        Returns
        -------
        :class:`~bearing.math.Vector`
            The resulting vector.

        """
        error_message = "Addition with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
        elif isinstance(other, (int, float)):
            x = self.x + other
            y = self.y + other
            z = self.z + other
        elif isinstance(other, (tuple, list)):
            x = self.x + other[0]
            y = self.y + other[1]
            z = self.z + other[2]
        else:
            raise ValueError(error_message)
        return Vector(x, y, z)

    def __iadd__(self, other: Vector | int | float | tuple | list) -> None:
        """
        Add the components of the other vector from this vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The other to add to self.

        Returns
        -------
        None

        """
        error_message = "Addition with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
            self.z += other
        elif isinstance(other, (tuple, list)):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        else:
            raise ValueError(error_message)
        return self


    def __radd__(self, other):
        """ Called if 4 + self for instance """
        return self.__add__(other)



    # Methods | Magic | Subtractions
    # -------------------------------------------------------------------------

    def __sub__(self, other: Vector | int | float | tuple | list) -> Vector:
        """
        Returns a Vector that is the the difference between this Vector and another Vector.


        """
        error_message = "Subtraction with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
        elif isinstance(other, (int, float)):
            x = self.x - other
            y = self.y - other
            z = self.z - other
        elif isinstance(other, (tuple, list)):
            x = self.x - other[0]
            y = self.y - other[1]
            z = self.z - other[2]
        else:
            raise ValueError(error_message)
        return Vector(x, y, z)

    def __isub__(self, other: Vector | int | float | tuple | list) -> None:
        """
        Subtract the components of the other vector from this vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The vector to subtract.

        Returns
        -------
        None

        """
        error_message = "Subtraction with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
            self.z -= other
        elif isinstance(other, (tuple, list)):
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
        else:
            raise ValueError(error_message)
        return self


    def __rsub__(self, other):
        """ Called if 4 - self for instance """
        return self.__sub__(other)


    # Methods | Magic | Multiplications
    # -------------------------------------------------------------------------

    def __mul__ (self, other: Vector | int | float | tuple | list) -> Vector:
        """
        Return a vector that is the scaled version of this vector.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        :class:`~bearing.math.Vector`
            The resulting new vector.

        """
        error_message = "Multiplication with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
        elif isinstance(other, (int, float)):
            x = self.x * other
            y = self.y * other
            z = self.z * other
        elif isinstance(other, (tuple, list)):
            x = self.x * other[0]
            y = self.y * other[1]
            z = self.z * other[2]
        else:
            raise ValueError(error_message)
        return Vector(x, y, z)

    def __imul__(self, other: Vector | int | float | tuple | list) -> None:
        """
        Multiply the components of this vector by the given factor.

        Parameters
        ----------
        n : float
            The multiplication factor.

        Returns
        -------
        None

        """
        error_message = "Multiplication with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
            self.z *= other
        elif isinstance(other, (tuple, list)):
            self.x *= other[0]
            self.y *= other[1]
            self.z *= other[2]
        else:
            raise ValueError(error_message)
        return self


    def __rmul__(self, other):
        """ Called if 4 * self for instance """
        return self.__mul__(other)


    # Methods | Magic | Subdivisions
    # -------------------------------------------------------------------------


    def __truediv__ (self, other: Vector | int | float | tuple | list) -> Vector:
        """
        Return a vector that is the scaled version of this vector.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        :class:`~bearing.math.Vector`
            The resulting new vector.

        """
        error_message = "Multiplication with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
        elif isinstance(other, (int, float)):
            x = self.x / other
            y = self.y / other
            z = self.z / other
        elif isinstance(other, (tuple, list)):
            x = self.x / other[0]
            y = self.y / other[1]
            z = self.z / other[2]
        else:
            raise ValueError(error_message)
        return Vector(x, y, z)

    def __itruediv__(self, other: Vector | int | float | tuple | list) -> None:
        """
        Divide the components of this vector by the given factor.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        None

        """
        error_message = "Multiplication with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif isinstance(other, (int, float)):
            self.x /= other
            self.y /= other
            self.z /= other
        elif isinstance(other, (tuple, list)):
            self.x /= other[0]
            self.y /= other[1]
            self.z /= other[2]
        else:
            raise ValueError(error_message)
        return self



    # Methods | Magic | Powers
    # -------------------------------------------------------------------------


    def __pow__ (self, other: Vector | int | float | tuple | list) -> Vector:
        """
        Create a vector from the components of the current vector raised
        to the given power.

        Parameters
        ----------
        n : float
            The power.

        Returns
        -------
        :class:`~bearing.math.Vector`
            A new point with raised coordinates.

        """
        error_message = "Multiplication with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            x = self.x ** other.x
            y = self.y ** other.y
            z = self.z ** other.z
        elif isinstance(other, (int, float)):
            x = self.x ** other
            y = self.y ** other
            z = self.z ** other
        elif isinstance(other, (tuple, list)):
            x = self.x ** other[0]
            y = self.y ** other[1]
            z = self.z ** other[2]
        else:
            raise ValueError(error_message)
        return Vector(x, y, z)


    def __ipow__(self, other: Vector | int | float | tuple | list) -> None:
        """
        Raise the components of this vector to the given power.

        Parameters
        ----------
        n : float
            The power.

        Returns
        -------
        None

        """
        error_message = "Multiplication with type {} not supported".format(type(other))
        assert isinstance(other, (Vector, int, float, tuple, list), msg = error_message)
        if isinstance(other, Vector):
            self.x **= other.x
            self.y **= other.y
            self.z **= other.z
        elif isinstance(other, (int, float)):
            self.x **= other
            self.y **= other
            self.z **= other
        elif isinstance(other, (tuple, list)):
            self.x **= other[0]
            self.y **= other[1]
            self.z **= other[2]
        else:
            raise ValueError(error_message)
        return self



    # =========================================================================
    # Methods | Class
    # =========================================================================


    @classmethod
    def unit_axis_x(cls):
        """
        Construct a unit vector along the X axis.

        Returns
        -------
        :class:`~bearing.math.Vector`
            A vector with components ``x = 1.0, y = 0.0, z = 0.0``.

        Examples
        --------
        >>> Vector.Xaxis()
        Vector(1.000, 0.000, 0.000)

        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def unit_axis_y(cls):
        """
        Construct a unit vector along the Y axis.

        Returns
        -------
        :class:`~bearing.math.Vector`
            A vector with components ``x = 0.0, y = 1.0, z = 0.0``.

        Examples
        --------
        >>> Vector.Yaxis()
        Vector(0.000, 1.000, 0.000)

        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def unit_axis_z(cls):
        """
        Construct a unit vector along the Z axis.

        Returns
        -------
        :class:`~bearing.math.Vector`
            A vector with components ``x = 0.0, y = 0.0, z = 1.0``.

        Examples
        --------
        >>> Vector.Zaxis()
        Vector(0.000, 0.000, 1.000)

        """
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def from_start_end(cls, start, end):
        """
        Construct a vector from start and end points.

        Parameters
        ----------
        start : [float, float, float] | :class:`~bearing.math.Point`
            The start point.
        end : [float, float, float] | :class:`~bearing.math.Point`
            The end point.

        Returns
        -------
        :class:`~bearing.math.Vector`
            The vector from start to end.

        Examples
        --------
        >>> Vector.from_start_end([1.0, 0.0, 0.0], [1.0, 1.0, 0.0])
        Vector(0.000, 1.000, 0.000)

        """
        v = subtract_vectors(end, start)
        return cls(*v)


    # =========================================================================
    # Methods | Static
    # =========================================================================

    @staticmethod
    def transform_collection(collection, X):
        """
        Transform a collection of vector objects.

        Parameters
        ----------
        collection : list[[float, float, float] | :class:`~bearing.math.Vector`]
            The collection of vectors.

        Returns
        -------
        None

        Examples
        --------
        >>> from bearing.math import Rotation
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), math.radians(90))
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> vectors = [u]
        >>> Vector.transform_collection(vectors, R)
        >>> v = vectors[0]
        >>> v
        Vector(0.000, 1.000, 0.000)
        >>> u is v
        True

        """
        data = transform_vectors(collection, X)
        for vector, xyz in zip(collection, data):
            vector.x = xyz[0]
            vector.y = xyz[1]
            vector.z = xyz[2]

    @staticmethod
    def transformed_collection(collection, X):
        """
        Create a collection of transformed vectors.

        Parameters
        ----------
        collection : list[[float, float, float] | :class:`~bearing.math.Vector`]
            The collection of vectors.

        Returns
        -------
        list[:class:`~bearing.math.Vector`]
            The transformed vectors.

        Examples
        --------
        >>> from bearing.math import Rotation
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), math.radians(90))
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> vectors = [u]
        >>> vectors = Vector.transformed_collection(vectors, R)
        >>> v = vectors[0]
        >>> v
        Vector(0.000, 1.000, 0.000)
        >>> u is v
        False

        """
        vectors = [vector.copy() for vector in collection]
        Vector.transform_collection(vectors, X)
        return vectors

    @staticmethod
    def length_vectors(vectors):
        """
        Compute the length of multiple vectors.

        Parameters
        ----------
        vectors : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.

        Returns
        -------
        list[float]
            A list of lengths.

        Examples
        --------
        >>> Vector.length_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        [1.0, 2.0]

        """
        return [length_vector(vector) for vector in vectors]

    @staticmethod
    def sum_vectors(vectors):
        """
        Compute the sum of multiple vectors.

        Parameters
        ----------
        vectors : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.

        Returns
        -------
        :class:`~bearing.math.Vector`
            A vector that is the sum of the vectors.

        Examples
        --------
        >>> Vector.sum_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        Vector(3.000, 0.000, 0.000)

        """
        return Vector(*[sum(axis) for axis in zip(*vectors)])

    @staticmethod
    def dot_vectors(left, right):
        """
        Compute the dot product of two lists of vectors.

        Parameters
        ----------
        left : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.
        right : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.

        Returns
        -------
        list[float]
            A list of dot products.

        Examples
        --------
        >>> Vector.dot_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        [1.0, 4.0]

        """
        return [Vector.dot(u, v) for u, v in zip(left, right)]

    @staticmethod
    def cross_vectors(left, right):
        """
        Compute the cross product of two lists of vectors.

        Parameters
        ----------
        left : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.
        right : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.

        Returns
        -------
        list[:class:`~bearing.math.Vector`]
            A list of cross products.

        Examples
        --------
        >>> Vector.cross_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        [Vector(0.000, 0.000, 1.000), Vector(0.000, -4.000, 0.000)]

        """
        return [Vector.cross(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angles_vectors(left, right):
        """
        Compute both angles between corresponding pairs of two lists of vectors.

        Parameters
        ----------
        left : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.
        right : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.

        Returns
        -------
        list[float]
            A list of angle pairs.

        Examples
        --------
        >>> Vector.angles_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        [(1.5707963267948966, 4.71238898038469), (1.5707963267948966, 4.71238898038469)]

        """
        return [angles_vectors(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angle_vectors(left, right):
        """
        Compute the smallest angle between corresponding pairs of two lists of vectors.

        Parameters
        ----------
        left : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.
        right : list[[float, float, float] | :class:`~bearing.math.Vector`]
            A list of vectors.

        Returns
        -------
        list[float]
            A list of angles.

        Examples
        --------
        >>> Vector.angle_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        [1.5707963267948966, 1.5707963267948966]

        """
        return [angle_vectors(u, v) for u, v in zip(left, right)]




    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this vector.

        Returns
        -------
        :class:`~bearing.math.Vector`
            The copy.

        Examples
        --------
        >>> u = Vector(0.0, 0.0, 0.0)
        >>> v = u.copy()
        >>> u == v
        True
        >>> u is v
        False

        """
        cls = type(self)
        return cls(self.x, self.y, self.z)

    # ==========================================================================
    # methods
    # ==========================================================================

    def unitize(self):
        """
        Scale this vector to unit length.

        Returns
        -------
        None

        Examples
        --------
        >>> u = Vector(1.0, 2.0, 3.0)
        >>> u.unitize()
        >>> u.length
        1.0

        """
        length = self.length
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length

    def unitized(self):
        """
        Returns a unitized copy of this vector.

        Returns
        -------
        :class:`~bearing.math.Vector`
            A unitized copy of the vector.

        Examples
        --------
        >>> u = Vector(1.0, 2.0, 3.0)
        >>> v = u.unitized()
        >>> u.length == 1.0
        False
        >>> v.length == 1.0
        True

        """
        v = self.copy()
        v.unitize()
        return v

    def invert(self):
        """
        Invert the direction of this vector

        Returns
        -------
        None

        Notes
        -----
        a negation of a vector is similar to inverting a vector

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = u.copy()
        >>> u.invert()
        >>> u == v
        False
        >>> u.invert()
        >>> u == v
        True
        >>> v == --v
        True

        """
        self.scale(-1.0)

    def inverted(self):
        """
        Returns a inverted copy of this vector

        Returns
        -------
        :class:`~bearing.math.Vector`

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = u.inverted()
        >>> w = u + v
        >>> w.length
        0.0

        """
        return self.scaled(-1.0)

    def scale(self, n):
        """
        Scale this vector by a factor n.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        None

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> u.scale(3.0)
        >>> u.length
        3.0

        """
        self.x *= n
        self.y *= n
        self.z *= n


    # Return the product of self and numeric object alpha.
    def scale(self, alpha):
        result = stdarray.create1D(self._n, 0)
        for i in range(self._n):
            result[i] = alpha * self._coords[i]
        return Vector(result)


    def scaled(self, n):
        """
        Returns a scaled copy of this vector.

        Parameters
        ----------
        n : float
            The scaling factor.

        Returns
        -------
        :class:`~bearing.math.Vector`
            A scaled copy of the vector.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = u.scaled(3.0)
        >>> u.length
        1.0
        >>> v.length
        3.0

        """
        v = self.copy()
        v.scale(n)
        return v



    def dot(self, other):
        """
        The dot product of this vector and another vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The other vector.

        Returns
        -------
        float
            The dot product.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.dot(v)
        0.0

        """
        return dot_vectors(self, other)



    # Return the inner product of self and Vector object other.
    def dot(self, other):
        result = 0
        for i in range(self._n):
            result += self._coords[i] * other._coords[i]
        return result


    def inner(self, vector):
        """
        Returns the dot product (inner product) of self and another vector
        """
        if not isinstance(vector, Vector):
            raise ValueError('The dot product requires another vector')
        return sum(a * b for a, b in zip(self, vector))




    def cross(self, other):
        """
        The cross product of this vector and another vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The other vector.

        Returns
        -------
        :class:`~bearing.math.Vector`
            The cross product.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.cross(v)
        Vector(0.000, 0.000, 1.000)

        """
        return Vector(*cross_vectors(self, other))


    # Return the unit vector of self.
    def direction(self):
        return self.scale(1.0 / abs(self))


    def norm(self):
        """
        Returns the norm (length, magnitude) of the vector
        """
        return math.sqrt(sum( x*x for x in self ))

    def argument(self, radians=False):
        """
        Returns the argument of the vector, the angle clockwise from +y. In degress by default,
        set radians=True to get the result in radians. This only works for 2D vectors.
        """
        arg_in_rad = math.acos(Vector(0, 1)*self/self.norm())
        if radians:
            return arg_in_rad
        arg_in_deg = math.degrees(arg_in_rad)
        if self.values[0] < 0:
            return 360 - arg_in_deg
        else:
            return arg_in_deg

    def normalize(self):
        """ Returns a normalized unit vector """
        norm = self.norm()
        normed = tuple( x / norm for x in self )
        return self.__class__(*normed)



    def angle(self, other):
        """
        Compute the smallest angle between this vector and another vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The other vector.

        Returns
        -------
        float
            The smallest angle between the two vectors.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.angle(v) == 0.5 * math.pi
        True

        """
        return angle_vectors(self, other)

    def angle_signed(self, other, normal):
        """
        Compute the signed angle between this vector and another vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The other vector.
        normal : [float, float, float] | :class:`~bearing.math.Vector`
            The plane's normal spanned by this and the other vector.

        Returns
        -------
        float
            The signed angle between the two vectors.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.angle_signed(v, Vector(0.0, 0.0, 1.0)) == 0.5 * math.pi
        True
        >>> u.angle_signed(v, Vector(0.0, 0.0, -1.0)) == -0.5 * math.pi
        True

        """
        return angle_vectors_signed(self, other, normal)

    def angles(self, other):
        """
        Compute both angles between this vector and another vector.

        Parameters
        ----------
        other : [float, float, float] | :class:`~bearing.math.Vector`
            The other vector.

        Returns
        -------
        tuple[float, float]
            The angles between the two vectors, with the smallest angle first.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.angles(v)[0] == 0.5 * math.pi
        True

        """
        return angles_vectors(self, other)

    def transform(self, T):
        """
        Transform this vector.

        Parameters
        ----------
        T : :class:`~bearing.math.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

        Examples
        --------
        >>> from bearing.math import Rotation
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], math.radians(90))
        >>> u.transform(R)
        >>> u
        Vector(0.000, 1.000, 0.000)

        """
        point = transform_vectors([self], T)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]

    def transformed(self, T):
        """
        Return a transformed copy of this vector.

        Parameters
        ----------
        T : :class:`~bearing.math.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        :class:`~bearing.math.Vector`
            The transformed copy.

        Examples
        --------
        >>> from bearing.math import Rotation
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], math.radians(90))
        >>> v = u.transformed(R)
        >>> v
        Vector(0.000, 1.000, 0.000)

        """
        vector = self.copy()
        vector.transform(T)
        return vector


    def rotate(self, theta):
        """
        Rotate this vector. If passed a number, assumes this is a
            2D vector and rotates by the passed value in degrees.  Otherwise,
            assumes the passed value is a list acting as a matrix which rotates the vector.
        """
        if isinstance(theta, (int, float)):
            # So, if rotate is passed an int or a float...
            if len(self) != 2:
                raise ValueError("Rotation axis not defined for greater than 2D vector")
            return self._rotate2D(theta)

        matrix = theta
        if not all(len(row) == len(self) for row in matrix) or not len(matrix)==len(self):
            raise ValueError("Rotation matrix must be square and same dimensions as vector")
        return self.matrix_mult(matrix)


    def _rotate2D(self, theta):
        """ Rotate this vector by theta in degrees.

            Returns a new vector.
        """
        theta = math.radians(theta)
        # Just applying the 2D rotation matrix
        dc, ds = math.cos(theta), math.sin(theta)
        x, y = self.values
        x, y = dc*x - ds*y, ds*x + dc*y
        return self.__class__(x, y)


    def matrix_mult(self, matrix):
        """ Multiply this vector by a matrix.  Assuming matrix is a list of lists.

            Example:
            mat = [[1,2,3],[-1,0,1],[3,4,5]]
            Vector(1,2,3).matrix_mult(mat) ->  (14, 2, 26)

        """
        if not all(len(row) == len(self) for row in matrix):
            raise ValueError('Matrix must match vector dimensions')

        # Grab a row from the matrix, make it a Vector, take the dot product,
        # and store it as the first component
        product = tuple(Vector(*row)*self for row in matrix)

        return self.__class__(*product)



    # =========================================================================
    # Methods | Test
    # =========================================================================

    def test_something(self):
        """Test Method"""
        pass












def test():
    """Test Function"""
    pass

def main():

    """Main"""
    import doctest
    doctest.testmod()
    test()

if __name__ == '__main__':
    main()


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
