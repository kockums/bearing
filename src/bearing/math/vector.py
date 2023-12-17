# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Vector Class
=====================

Todo:
-----

Links:
------

"""

# =============================================================================
# Import
# =============================================================================

# Import | Standard Library
from typing import Any, Dict, List, Iterator, Tuple
import math

# Import | Libraries

# Import | Local Modules


# =============================================================================
# Classes
# =============================================================================

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

    # __slots__ = ["_x", "_y", "_z"]
    __slots__ = ["_components"]

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        **kwargs
    ) -> None:
        """
        Constructor of the Vector object.

        """
        super(Vector, self).__init__(**kwargs)
        # self.x = x
        # self.y = y
        # self.z = z
        self._components = [x, y, z]

    # =========================================================================
    # Methods | Properties
    # =========================================================================

    # Methods | Properties | components parameter
    # -------------------------------------------------------------------------

    @property
    def components(
        self
    ) -> Tuple[float, float, float]:
        """
        Getter decorator method for x parameter.
        Gets the components of the vector as a tuple.

        Parameters
        ----------
        None

        Returns
        -------
        components : Tuple[float, float, float]
            A tuple representing the x, y, and z components of the vector.

        """

        components = tuple(self._components)
        return components

    @components.setter
    def components(self, values: Tuple[float, float, float]) -> None:

        """
        Setter decorator method for x parameter.
        Sets the components of the vector.

        Parameters
        ----------

        Returns
        -------
        None

        """
        if len(values) != 3:
            raise ValueError(
                "Components must be a tuple of three float values."
            )
        self._components = list(values)

    @components.deleter
    def components(self) -> None:
        """
        Deleter decorator method for x parameter.
        Resets the components of the vector to zero.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        self._components = [0.0, 0.0, 0.0]

    # Methods | Properties | x parameter
    # -------------------------------------------------------------------------

    @property
    def x(self) -> float:
        """
        Getter decorator method for x parameter.
        Gets the x-component of the vector.

        Parameters
        ----------
        None

        Returns
        -------
        x : float
            The x parameter.

        """
        # return self._x
        x = self._components[0]
        return x

    @x.setter
    def x(self, x: int | float):
        """
        Setter decorator method for x parameter.
        Sets the x-component of the vector.

        Parameters
        ----------
        x : int | float
            The x parameter.

        Returns
        -------
        None

        """
        assert isinstance(
            x,
            (int, float),
            msg = "x parameter must be int or float"
        )
        self._components[0] = float(x)

    @x.deleter
    def x(self):
        """
        Deleter decorator method for x parameter.
        Resets the x-component of the vector to zero.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self._components[0] = 0.0

    # Methods | Properties | y parameter
    # -------------------------------------------------------------------------

    @property
    def y(self) -> float:
        """
        Getter decorator method for y parameter.
        Gets the y-component of the vector.

        Parameters
        ----------
        None

        Returns
        -------
        y : float
            The y parameter.

        """
        y = self._components[1]
        return y

    @y.setter
    def y(self, y: int | float):
        """
        Setter decorator method for y parameter.
        Sets the y-component of the vector.

        Parameters
        ----------
        y : int | float
            The y parameter.

        Returns
        -------
        None

        """
        assert isinstance(
            y,
            (int, float),
            msg = "y parameter must be int or float"
        )
        self._components[1] = float(y)

    @y.deleter
    def y(self):
        """
        Deleter decorator method for y parameter.
        Resets the y-component of the vector to zero.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self._components[1] = 0.0

    # Methods | Properties | z parameter
    # -------------------------------------------------------------------------

    @property
    def z(self) -> float:
        """
        Getter decorator method for z parameter.
        Gets the z-component of the vector.

        Parameters
        ----------
        None

        Returns
        -------
        z : float
            The z parameter.

        """
        # return self._z
        z = self._components[2]
        return z

    @z.setter
    def z(self, z: int | float):
        """
        Setter decorator method for z parameter.
        Sets the z-component of the vector.

        Parameters
        ----------
        z : int | float
            The z parameter.

        Returns
        -------
        None

        """
        assert isinstance(
            z,
            (int, float),
            msg = "z parameter must be int or float"
        )
        self._components[2] = float(z)

    @z.deleter
    def z(self):
        """
        Deleter decorator method for z parameter.
        Resets the z-component of the vector to zero.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self._components[2] = 0.0

    # Methods | Properties | length parameter
    # -------------------------------------------------------------------------

    @property
    def length(self) -> float:
        x, y, z = self._components
        return math.sqrt(x**2 + y**2 + z**2)

    # =========================================================================
    # Methods | Magic
    # =========================================================================

    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the Vector object.

        This representation includes the class name and the values of the
        vector's components with a fixed precision.

        Returns
        -------
        str
            A string representing the Vector object.
        """
        # Can be adjusted or made a class attribute for flexibility
        precision = 3
        return f"Vector({self.x:.{precision}f}, {self.y:.{precision}f}, {self.z:.{precision}f})"  # noqa E501

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the Vector object.

        This representation is more concise and omits the class name, focusing
        on the values of the vector's components.

        Returns
        -------
        str
            A string representation of the Vector object.
        """
        return f"({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index: int) -> float:
        """
        Retrieves the value of the vector at the specified index.

        Parameters
        ----------
        index : int
            The index of the vector component to retrieve.
            Must be 0 for x, 1 for y, or 2 for z.

        Returns
        -------
        float
            The value of the vector component at the specified index.

        Raises
        ------
        IndexError
            If the index is not 0, 1, or 2.
        """
        try:
            return self._components[index]
        except IndexError:
            raise IndexError("Index must be 0 (x), 1 (y), or 2 (z).")

    def __setitem__(self, index: int, value: float) -> None:
        """
        Sets the value of the vector at the specified index.

        Parameters
        ----------
        index : int
            The index of the vector component to set.
            Must be 0 for x, 1 for y, or 2 for z.
        value : float
            The new value for the specified component.

        Raises
        ------
        IndexError
            If the index is not 0, 1, or 2.
        TypeError
            If the value is not a numeric type (int or float).
        """
        if index not in [0, 1, 2]:
            raise IndexError("Index must be 0 (x), 1 (y), or 2 (z).")
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a numeric type (int or float).")
        self._components[index] = float(value)

    # Methods | Magic | Basic
    # -------------------------------------------------------------------------

    def __len__(self) -> int:
        """
        Returns the number of components in the vector.

        Returns
        -------
        int
            The number of components in the vector.
        """
        return len(self._components)

    def __iter__(self) -> Iterator[float]:
        """
        Returns an iterator for the vector components.

        This method utilizes Python's built-in iter function to create an
        iterator over a list that contains the x, y, and z components of the
        vector.

        Returns
        -------
        Iterator[float]
            An iterator over the vector components (x, y, z).
        """
        return iter(self._components)

    # def __next__(self):
    #     """
    #     next() method in a class.

    #     """
    #     pass

    def __eq__(self, other: "Vector") -> bool:
        """
        Checks if this vector is equal to another object.

        Equality is determined based on the similarity of components. Due to
        the nature of floating-point arithmetic, a tolerance is used to
        determine if components are 'close enough' to be considered equal.

        Parameters
        ----------
        other : object
            Another object to compare against, ideally another Vector.

        Returns
        -------
        bool
            True if the other object is a Vector and all corresponding
            components are close enough within a tolerance, False otherwise.

        Notes
        -----
        The `isclose` method from the math module is used to compare
        floating-point values with a relative tolerance. This accounts for
        minor differences in floating-point arithmetic.
        """
        if not isinstance(
            other,
            Vector,
            msg = "other must be of type: Vector"
        ):
            return NotImplemented

        return all(
            math.isclose(a, b) for a, b in zip(
                self._components,
                other._components
            )
        )

    # Methods | Magic | Unary
    # -------------------------------------------------------------------------

    def __pos__(self) -> "Vector":
        """
        Returns a new vector that is the positive of this vector.

        Returns
        -------
        Vector
            A new vector with the same components as this vector.
        """
        return Vector(*self._components)

    def __neg__(self) -> "Vector":
        """
        Returns a new vector that is the negation of this vector.

        Returns
        -------
        Vector
            A new vector with each component negated.
        """
        return Vector(*[-x for x in self._components])
        # return self.scaled(-1.0)

    def __abs__(self) -> "Vector":
        """
        Returns a new vector with the absolute values of this vector's
        components.

        Returns
        -------
        Vector
            A new vector with the absolute values of each component.
        """
        return Vector(*[abs(x) for x in self._components])

    def __invert__(self) -> "Vector":
        """
        Returns a new vector that is the bitwise inverse of this vector.

        Note
        ----
        This method treats the vector's components as integers for the purpose
        of bitwise inversion. It is mainly for demonstration and may not have
        a practical application in most vector-based computations.

        Returns
        -------
        Vector
            A new vector with each component bitwise-inverted.
        """
        return Vector(*[~int(x) for x in self._components])

    # Methods | Magic | Additions
    # -------------------------------------------------------------------------

    def __add__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Adds another vector, a scalar, or an iterable with three numeric
        elements to this vector.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The other vector, scalar, or an iterable of three numeric elements
            to add.

        Returns
        -------
        Vector
            A new vector that is the sum of this vector and the other vector,
            scalar, or iterable.

        Raises
        ------
        TypeError
            If the other object is not a Vector, int, float, tuple, or list.
        ValueError
            If the iterable does not contain exactly three elements.
        """
        if isinstance(other, Vector):
            return Vector(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
            )
        elif isinstance(other, (int, float)):
            return Vector(
                self.x + other,
                self.y + other,
                self.z + other,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            return Vector(
                self.x + other[0],
                self.y + other[1],
                self.z + other[2],
            )
        else:
            raise TypeError(
                f"Addition with type {type(other).__name__} not supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )

    def __iadd__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Performs in-place addition of another vector, a scalar, or an iterable
        with three numeric elements.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The other vector, scalar, or an iterable of three numeric elements
            to add.

        Returns
        -------
        Vector
            The modified vector after in-place addition.

        Raises
        ------
        TypeError
            If the other object is not a Vector, int, float, tuple, or list.
        ValueError
            If the iterable does not contain exactly three elements.
        """
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
            self.z += other
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        else:
            raise TypeError(
                f"Addition with type {type(other).__name__} not supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )
        return self

    def __radd__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Handles addition where the vector is on the right-hand side of the '+'
        operator.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The operand on the left side of the '+' operator.

        Returns
        -------
        Vector
            A new vector that is the sum of this vector and the 'other'
            operand.

        Raises
        ------
        TypeError
            If the 'other' object is not a Vector, int, float, tuple, or list.
        ValueError
            If 'other' is an iterable and does not contain exactly three
            elements.
        """
        if isinstance(other, Vector):
            return Vector(
                other.x + self.x,
                other.y + self.y,
                other.z + self.z,
            )
        elif isinstance(other, (int, float)):
            return Vector(
                other + self.x,
                other + self.y,
                other + self.z,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            return Vector(
                other[0] + self.x,
                other[1] + self.y,
                other[2] + self.z,
            )
        else:
            raise TypeError(
                f"Addition with type {type(other).__name__} not supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )

    # Methods | Magic | Subtractions
    # -------------------------------------------------------------------------

    def __sub__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Subtracts another vector, a scalar, or an iterable with three numeric
        elements from this vector.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The other vector, scalar, or an iterable of three numeric elements
            to subtract.

        Returns
        -------
        Vector
            A new vector that is the result of subtracting 'other' from this
            vector.

        Raises
        ------
        TypeError
            If the 'other' object is not a Vector, int, float, tuple, or list.
        ValueError
            If 'other' is an iterable and does not contain exactly three
            elements.
        """
        if isinstance(other, Vector):
            return Vector(
                self.x - other.x,
                self.y - other.y,
                self.z - other.z,
            )
        elif isinstance(other, (int, float)):
            return Vector(
                self.x - other,
                self.y - other,
                self.z - other,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            return Vector(
                self.x - other[0],
                self.y - other[1],
                self.z - other[2],
            )
        else:
            raise TypeError(
                f"Subtraction with type {type(other).__name__} not supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )

    def __isub__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Performs in-place subtraction of another vector, a scalar, or an
        iterable with three numeric elements from this vector.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The other vector, scalar, or an iterable of three numeric elements
            to subtract.

        Returns
        -------
        Vector
            The modified vector after in-place subtraction.

        Raises
        ------
        TypeError
            If the 'other' object is not a Vector, int, float, tuple, or list.
        ValueError
            If 'other' is an iterable and does not contain exactly three
            elements.
        """
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
            self.z -= other
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
        else:
            raise TypeError(
                f"Subtraction with type {type(other).__name__} not supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )

        return self

    def __rsub__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Handles reverse subtraction where the vector is on the right-hand side
        of the '-' operator.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The operand on the left side of the '-' operator.

        Returns
        -------
        Vector
            A new vector that is the result of subtracting this vector from
            'other'.

        Raises
        ------
        TypeError
            If the 'other' object is not a Vector, int, float, tuple, or list.
        ValueError
            If 'other' is an iterable and does not contain exactly three
            elements.
        """
        if isinstance(other, Vector):
            return Vector(
                other.x - self.x,
                other.y - self.y,
                other.z - self.z,
            )
        elif isinstance(other, (int, float)):
            return Vector(
                other - self.x,
                other - self.y,
                other - self.z,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            return Vector(
                other[0] - self.x,
                other[1] - self.y,
                other[2] - self.z,
            )
        else:
            raise TypeError(
                f"Subtraction with type {type(other).__name__} not supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )

    # Methods | Magic | Multiplications
    # -------------------------------------------------------------------------

    def __mul__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Multiplies this vector by a scalar or performs element-wise
        multiplication with another vector.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The scalar or another vector to multiply with this vector.

        Returns
        -------
        Vector
            A new vector that is the result of the multiplication.

        Raises
        ------
        TypeError
            If 'other' is not a Vector, int, float, tuple, or list.
        """
        if isinstance(other, Vector):
            # Element-wise multiplication
            return Vector(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z,
            )
        elif isinstance(other, (int, float)):
            # Scalar multiplication
            return Vector(
                self.x * other,
                self.y * other,
                self.z * other,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            return Vector(
                self.x * other[0],
                self.y * other[1],
                self.z * other[2],
            )
        else:
            raise TypeError(
                f"Multiplication with type {type(other).__name__} not "
                "supported. Operand must be a Vector, int, or float."
            )

    def __imul__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Performs in-place multiplication of this vector by a scalar or
        element-wise multiplication with another vector.

        Parameters
        ----------
        other : Vector, int, or float
            The scalar or another vector to multiply with this vector in place.

        Returns
        -------
        Vector
            The modified vector after in-place multiplication.

        Raises
        ------
        TypeError
            If 'other' is not a Vector, int, float, tuple, or list.
        """
        if isinstance(other, Vector):
            # Element-wise multiplication
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif isinstance(other, (int, float)):
            # Scalar multiplication
            self.x *= other
            self.y *= other
            self.z *= other
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            self.x *= other[0]
            self.y *= other[1]
            self.z *= other[2]
        else:
            raise TypeError(
                f"In-place multiplication with type {type(other).__name__} "
                "not supported. "
                "Operand must be a Vector, int, float, tuple, list."
            )
        return self

    def __rmul__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Handles reverse multiplication where the vector is on the right-hand
        side of the '*' operator.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The operand on the left side of the '*' operator.

        Returns
        -------
        Vector
            A new vector that is the result of multiplying 'other' with this
            vector.

        Raises
        ------
        TypeError
            If 'other' is not a Vector, int, float, tuple, or list.
        """
        if isinstance(other, (int, float)):
            # Scalar multiplication
            return Vector(
                other * self.x,
                other * self.y,
                other * self.z,
            )
        elif isinstance(other, Vector):
            # Element-wise multiplication
            return Vector(
                other.x * self.x,
                other.y * self.y,
                other.z * self.z,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            self.x * other[0]
            self.y * other[1]
            self.z * other[2]
        else:
            raise TypeError(
                f"In-place multiplication with type {type(other).__name__} "
                "not supported. "
                "Operand must be a Vector, int, float, tuple, list."
            )

    # Methods | Magic | Subdivisions
    # -------------------------------------------------------------------------

    def __truediv__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Divides this vector by a scalar, or performs element-wise division
        with another vector or iterable.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The scalar, vector, or iterable to divide this vector by.

        Returns
        -------
        Vector
            A new vector resulting from the division.

        Raises
        ------
        TypeError
            If 'other' is not a Vector, int, float, tuple, or list.
        ZeroDivisionError
            If any component of 'other' is zero during element-wise division.
        """
        if isinstance(other, Vector):
            if 0 in [other.x, other.y, other.z]:
                raise ZeroDivisionError(
                    "Division by zero in element-wise division with a Vector."
                )
            return Vector(
                self.x / other.x,
                self.y / other.y,
                self.z / other.z,
            )
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError(
                    "Division by zero is not allowed."
                )
            return Vector(
                self.x / other,
                self.y / other,
                self.z / other,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            if 0 in other:
                raise ZeroDivisionError(
                    "Division by zero in element-wise division with an "
                    "iterable."
                )
            return Vector(
                self.x / other[0],
                self.y / other[1],
                self.z / other[2],
            )
        else:
            raise TypeError(
                f"Division with type {type(other).__name__} not supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )

    def __itruediv__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Performs in-place true division of this vector by a scalar, or
        element-wise division with another vector or iterable.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The scalar, vector, or iterable to divide this vector by in place.

        Returns
        -------
        Vector
            The modified vector after in-place division.

        Raises
        ------
        TypeError
            If 'other' is not a Vector, int, float, tuple, or list.
        ZeroDivisionError
            If any component of 'other' is zero during element-wise division.
        """
        if isinstance(other, Vector):
            if 0 in [other.x, other.y, other.z]:
                raise ZeroDivisionError(
                    "Division by zero in element-wise division with a Vector."
                )
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError(
                    "Division by zero is not allowed."
                )
            self.x /= other
            self.y /= other
            self.z /= other
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            if 0 in other:
                raise ZeroDivisionError(
                    "Division by zero in element-wise division with an "
                    "iterable."
                )
            self.x /= other[0]
            self.y /= other[1]
            self.z /= other[2]
        else:
            raise TypeError(
                f"In-place division with type {type(other).__name__} not "
                "supported. "
                "Operand must be a Vector, int, float, tuple, or list."
            )
        return self

    def __rtruediv__(self, other) -> "Vector":
        """
        Handles reverse true division where the vector is on the right-hand
        side of the '/' operator.

        This method allows division of a scalar or another vector by this
        vector. 
        Note: Division by a vector is not a standard vector operation and is
        provided for completeness.

        Parameters
        ----------
        other : int, float, or Vector
            The operand on the left side of the '/' operator.

        Returns
        -------
        Vector
            A new vector that is the result of dividing 'other' by this vector.

        Raises
        ------
        TypeError
            If 'other' is not an int, float, or Vector.
        ZeroDivisionError
            If any component of this vector is zero.
        """
        if 0 in [self.x, self.y, self.z]:
            raise ZeroDivisionError(
                "Division by zero in vector components is not allowed."
            )

        if isinstance(other, (int, float)):
            return Vector(other / self.x, other / self.y, other / self.z)
        elif isinstance(other, Vector):
            return Vector(other.x / self.x, other.y / self.y, other.z / self.z)
        else:
            raise TypeError(
                f"Division with type {type(other).__name__} not supported. "
                "Operand must be an int, float, or Vector.")

    # Methods | Magic | Powers
    # -------------------------------------------------------------------------

    def __pow__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Raises each component of the vector to the power of 'other', which can
        be a scalar, another vector, or an iterable.

        Parameters
        ----------
        other : Vector, int, float, tuple, or list
            The exponent to raise each component of the vector to. If 'other'
            is a Vector or iterable, the operation is element-wise.

        Returns
        -------
        Vector
            A new vector with each component raised to the given power.

        Raises
        ------
        TypeError
            If 'other' is not a Vector, int, float, tuple, or list.
        ValueError
            If 'other' is an iterable and does not contain exactly three
            elements.
        """
        if isinstance(other, Vector):
            return Vector(
                self.x ** other.x,
                self.y ** other.y,
                self.z ** other.z,
            )
        elif isinstance(other, (int, float)):
            return Vector(
                self.x ** other,
                self.y ** other,
                self.z ** other,
            )
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            return Vector(
                self.x ** other[0],
                self.y ** other[1],
                self.z ** other[2],
            )
        else:
            raise TypeError(
                f"Exponent must be a Vector, int, float, tuple, or list, not {type(other).__name__}.")  # noqa E501

    def __ipow__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Performs in-place exponentiation of this vector by a scalar, or
        element-wise exponentiation with another vector or iterable.

        Parameters
        ----------
        other : int, float, Vector, tuple, or list
            The exponent to raise each component of this vector to. If 'other'
            is a Vector or iterable, the operation is element-wise.

        Returns
        -------
        Vector
            The modified vector after in-place exponentiation.

        Raises
        ------
        TypeError
            If 'other' is not an int, float, Vector, tuple, or list.
        ValueError
            If 'other' is an iterable and does not contain exactly three
            elements.
        """
        if isinstance(other, Vector):
            self.x **= other.x
            self.y **= other.y
            self.z **= other.z
        elif isinstance(other, (int, float)):
            self.x **= other
            self.y **= other
            self.z **= other
        elif isinstance(other, (tuple, list)):
            if len(other) != 3:
                raise ValueError(
                    "The iterable must contain exactly three elements."
                )
            self.x **= other[0]
            self.y **= other[1]
            self.z **= other[2]
        else:
            raise TypeError(
                f"In-place exponentiation with type {type(other).__name__} "
                "not supported. "
                "Operand must be an int, float, Vector, tuple, or list."
            )

        return self

    def __rpow__(
        self,
        other: "Vector" | int | float | tuple | list
    ) -> "Vector":
        """
        Handles reverse exponentiation where the vector is on the right-hand
        side of the '**' operator.

        This method allows exponentiation of a scalar or another vector to the
        power of this vector.
        Note: This is an unconventional operation for vectors and is provided
        for completeness.

        Parameters
        ----------
        other : int, float, or Vector
            The base of the exponentiation.

        Returns
        -------
        Vector
            A new vector resulting from raising 'other' to the power of this
            vector.

        Raises
        ------
        TypeError
            If 'other' is not an int, float, or Vector.
        """
        if isinstance(other, (int, float)):
            return Vector(
                other ** self.x, other ** self.y, other ** self.z)
        elif isinstance(other, Vector):
            return Vector(
                other.x ** self.x, other.y ** self.y, other.z ** self.z)
        else:
            raise TypeError(
                f"Exponentiation with type {type(other).__name__} not "
                "supported. "
                "Base must be an int, float, or Vector."
            )

    # =========================================================================
    # Methods | Class
    # =========================================================================

    # Methods | Class | IO
    # -------------------------------------------------------------------------

    @classmethod
    def from_tuple(cls, tuple_data) -> "Vector":
        """
        Constructs a vector from a tuple.

        This method allows for the conversion of a tuple of coordinates into a
        Vector object. The tuple can have two or three numeric elements. If it
        has two elements, the z-component is assumed to be zero, making it
        suitable for 2D scenarios.

        Parameters
        ----------
        tuple_data : tuple
            A tuple of two or three numeric elements representing the x, y
            (and optionally z) components of the vector.

        Returns
        -------
        Vector
            A new instance of Vector created from the given tuple.

        Raises
        ------
        TypeError
            If the input is not a tuple.
        ValueError
            If the tuple does not contain two or three elements.

        Examples
        --------
        >>> Vector.from_tuple((1, 2))
        Vector(1.0, 2.0, 0.0)

        >>> Vector.from_tuple((1, 2, 3))
        Vector(1.0, 2.0, 3.0)

        This method is useful for converting tuple data into Vector objects,
        particularly in scenarios like data processing or interfacing with
        systems where tuples are used to represent coordinate data.
        """
        if not isinstance(tuple_data, tuple):
            raise TypeError("Input must be a tuple.")

        if len(tuple_data) == 2:
            return cls(tuple_data[0], tuple_data[1], 0.0)
        elif len(tuple_data) == 3:
            return cls(*tuple_data)
        else:
            raise ValueError(
                "Tuple must contain either two or three elements."
            )

    def to_tuple(self) -> tuple:
        """
        Converts this vector into a tuple.

        This method provides a convenient way to convert a Vector instance
        into a tuple of its components (x, y, z). This can be useful for
        serialization, logging, or interfacing with systems that use tuples
        for coordinate representation.

        Returns
        -------
        tuple
            A tuple representation of the vector (x, y, z).

        Examples
        --------
        >>> v = Vector(1, 2, 3)
        >>> v.to_tuple()
        (1, 2, 3)

        The returned tuple contains the x, y, and z components of the vector
        in that order.
        """
        return (self.x, self.y, self.z)

    @classmethod
    def from_polar(cls, magnitude, angle_degrees) -> "Vector":
        """
        Constructs a 2D vector from polar coordinates.

        This method converts polar coordinates (magnitude and angle) into a
        Cartesian vector. The angle is given in degrees and is measured from
        the positive X-axis in a counterclockwise direction. The resulting
        vector is a 2D vector (z=0) in Cartesian coordinates.

        Parameters
        ----------
        magnitude : float
            The magnitude (or length) of the vector.
        angle_degrees : float
            The angle in degrees, measured counterclockwise from the positive X-axis.

        Returns
        -------
        Vector
            A new instance of Vector representing the 2D vector in Cartesian
            coordinates.

        Examples
        --------
        >>> Vector.from_polar(5, 45)
        Vector(3.5355, 3.5355, 0)

        The method is particularly useful in scenarios involving rotations,
        circular motion, or when dealing with systems that primarily use polar
        coordinates.
        """
        angle_radians = math.radians(angle_degrees)
        return cls(
            magnitude * math.cos(angle_radians),
            magnitude * math.sin(angle_radians),
            0
        )

    # Methods | Class | Unit Axis
    # -------------------------------------------------------------------------

    @classmethod
    def zero(cls) -> "Vector":
        """
        Creates and returns a Zero Vector.

        A Zero Vector is a vector in which all the components are zero. 
        This is equivalent to the origin in a coordinate system, and it 
        often serves as an initial or default state in many vector operations.

        In 3D space, this vector is represented as (0.0, 0.0, 0.0).

        Returns
        -------
        Vector
            A new instance of Vector with all components set to zero.

        Examples
        --------
        >>> Vector.zero()
        Vector(0.0, 0.0, 0.0)

        This method is useful when a neutral or starting vector is needed,
        especially in calculations where the addition or subtraction of other
        vectors from a neutral base is required.

        It can also represent the absence of movement or direction in physical
        simulations or graphical representations.
        """
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def unit_axis(cls, axis) -> "Vector":
        """
        Creates and returns a unit vector along the specified axis.

        A unit vector is a vector that has a magnitude of 1. In Cartesian
        coordinates, it points in the direction of one of the axes and has all
        other components as zero. This method creates a unit vector along the
        specified 'x', 'y', or 'z' axis.

        Parameters
        ----------
        axis : str
            The axis along which the unit vector should be aligned.
            Valid options are 'x', 'y', or 'z'.

        Returns
        -------
        Vector
            A new instance of Vector representing the unit vector along the
            specified axis.

        Raises
        ------
        ValueError
            If the specified axis is not 'x', 'y', or 'z'.

        Examples
        --------
        >>> Vector.unit_vector('x')
        Vector(1, 0, 0)

        >>> Vector.unit_vector('y')
        Vector(0, 1, 0)

        >>> Vector.unit_vector('z')
        Vector(0, 0, 1)

        Unit vectors are fundamental in vector operations, often used to
        represent vector directions. They are crucial in 3D graphics, physics
        simulations, and various fields of engineering and mathematics.
        """
        if axis == 'x':
            return cls(1.0, 0.0, 0.0)
        elif axis == 'y':
            return cls(0.0, 1.0, 0.0)
        elif axis == 'z':
            return cls(0.0, 0.0, 1.0)
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'.")

    @classmethod
    def unit_axis_x(cls) -> "Vector":
        """
        Constructs a unit vector along the X-axis.

        A unit vector along the X-axis has a length of 1 and points in the
        positive direction of the X-axis. In Cartesian coordinates, this
        vector is represented as (1.0, 0.0, 0.0), indicating a unit distance
        along the X-axis and zero distance along the Y and Z axes.

        Returns
        -------
        Vector
            A new instance of Vector representing the unit vector along the
            X-axis.

        Examples
        --------
        >>> Vector.unit_axis_x()
        Vector(1.0, 0.0, 0.0)

        This method is useful in scenarios where a directional vector along
        the X-axis is needed, such as in 3D graphics for defining orientations,
        or in physics for specifying directional forces.
        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def unit_axis_y(cls) -> "Vector":
        """
        Constructs a unit vector along the Y-axis.

        A unit vector along the Y-axis has a length of 1 and points in the
        positive direction of the Y-axis. In Cartesian coordinates, this
        vector is represented as (0.0, 1.0, 0.0), indicating a unit distance
        along the Y-axis and zero distance along the X and Z axes.

        Returns
        -------
        Vector
            A new instance of Vector representing the unit vector along the
            Y-axis.

        Examples
        --------
        >>> Vector.unit_axis_y()
        Vector(0.0, 1.0, 0.0)

        This method is useful in scenarios where a directional vector along
        the Y-axis is needed, such as in 3D graphics for defining orientations,
        or in physics for specifying directional forces.
        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def unit_axis_z(cls) -> "Vector":
        """
        Constructs a unit vector along the Z-axis.

        A unit vector along the Z-axis has a length of 1 and points in the
        positive direction of the Z-axis. In Cartesian coordinates, this
        vector is represented as (0.0, 0.0, 1.0), indicating a unit distance
        along the Z-axis and zero distance along the X and Y axes.

        Returns
        -------
        Vector
            A new instance of Vector representing the unit vector along the
            Z-axis.

        Examples
        --------
        >>> Vector.unit_axis_z()
        Vector(0.0, 0.0, 1.0)

        This method is useful in scenarios where a directional vector along
        the Z-axis is needed, such as in 3D graphics for defining orientations,
        or in physics for specifying directional forces.
        """
        return cls(0.0, 0.0, 1.0)
