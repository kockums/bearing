
class Vector:
    # ... [other parts of the Vector class]

    @classmethod
    def from_start_end(cls, start, end) -> "Vector":
        """
        Constructs a vector representing the direction and magnitude from a start point to an end point.

        This method calculates the vector that represents the displacement from 'start' to 'end'. 
        Both 'start' and 'end' can be provided as sequences of three numbers (representing x, y, z coordinates) 
        or as instances of a Point class (or any similar class with x, y, z attributes).

        Parameters
        ----------
        start : sequence of float or Point-like object
            The start point, specified as a sequence (list, tuple) of three numbers or an object with x, y, z attributes.
        end : sequence of float or Point-like object
            The end point, specified in the same manner as the start point.

        Returns
        -------
        Vector
            A new Vector instance representing the vector from 'start' to 'end'.

        Raises
        ------
        TypeError
            If 'start' or 'end' cannot be interpreted as valid points.

        Examples
        --------
        >>> Vector.from_start_end([1.0, 0.0, 0.0], [1.0, 1.0, 0.0])
        Vector(0.000, 1.000, 0.000)

        >>> start_point = Point(1.0, 0.0, 0.0) # Assuming a Point class exists
        >>> end_point = Point(1.0, 1.0, 0.0)
        >>> Vector.from_start_end(start_point, end_point)
        Vector(0.000, 1.000, 0.000)

        This method is especially useful in scenarios involving movement, displacement,
        or when it's necessary to define a directional vector between two points in space.
        """
        try:
            start_x, start_y, start_z = cls._extract_coordinates(start)
            end_x, end_y, end_z = cls._extract_coordinates(end)
            return cls(end_x - start_x, end_y - start_y, end_z - start_z)
        except TypeError:
            raise TypeError("Start and end points must be sequences of three numbers or Point-like objects.")

    @staticmethod
    def _extract_coordinates(point):
        if hasattr(point, 'x') and hasattr(point, 'y') and hasattr(point, 'z'):
            return point.x, point.y, point.z
        elif len(point) == 3:
            return point
        else:
            raise TypeError("Point must have x, y, z coordinates.")








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
        # self.invert()
        # return self
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


    def scale_vector(vector, scalar):
        """This function creates (and returns) a new vector with components equal to the original vector scaled (i.e., multiplied) by the scalar argument.
        For example, vector <1, 2, 3> scaled by 1.5 will result in vector <1.5, 3, 4.5>."""

        new_vector = data.Vector(vector.x*scalar, vector.y*scalar, vector.z*scalar)
        return new_vector

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
        """
        Returns a normalized unit vector.
        """
        norm = self.norm()
        normed = tuple( x / norm for x in self )
        return self.__class__(*normed)


    def normalize_vector(vector):
        """
        The function creates (and returns) a new vector by normalizing the input vector.
        This means that the resulting vector has the same direction but a magnitude of 1.
        In short, the new vector is the original vector scaled by its length.

        """

        length = length_vector(vector)
        normal = data.Vector(vector.x/length, vector.y/length, vector.z/length)
        return normal


    def normalized(self):
        """
        return a new instance of Vector,
        with the same angle as this instance,
        but with length 1.
        """
        ret = self.copy()
        ret.x /= self.magnitude()
        ret.y /= self.magnitude()
        return ret





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
        """
        Rotate this vector by theta in degrees.

        Returns a new vector.

        """
        theta = math.radians(theta)
        # Just applying the 2D rotation matrix
        dc, ds = math.cos(theta), math.sin(theta)
        x, y = self.values
        x, y = dc*x - ds*y, ds*x + dc*y
        return self.__class__(x, y)


    def matrix_mult(self, matrix):
        """
        Multiply this vector by a matrix.  Assuming matrix is a list of lists.

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




    def difference_vector(vector1, vector2):
        """
        This functions creates (and returns) a new vector obtained by subtracting from vector vector1 the vector vector2 (i.e., vector1 - vector2). This is computed by subtracting the corresponding x-, y-, and z-components. (Yes, this is very similar to the previous function; the types, however, are conceptually different.)

        """

        difference_vector = data.Vector(vector1.x - vector2.x, vector1.y - vector2.y, vector1.z - vector2.z)
        return difference_vector

    def translate_point(point, vector):
        """
        This function creates (and returns) a new point created by translating (i.e., moving) the argument point in the direction of and by the magnitude of the argument vector. You can think of this as the argument vector directing the new point where and how far to go from the argument point.
        For example, translating point <9, 0, 1> along vector <1, 2, 3> will result in point <10, 2, 4>.

        """

        translation = data.Point(point.x + vector.x, point.y + vector.y, point.z + vector.z)
        return translation

    def vector_from_to(from_point, to_point):
        """
        This function is simply added to improve readability (and, thereby, to reduce confusion in later assignments). A vector in the direction from one point (from_point) to another (to_point) can be found by subtracting (i.e., point difference) from_point from to_point (i.e., to_point - from_point).

        """

        travel = data.Vector(to_point.x - from_point.x, to_point.y - from_point.y, to_point.z - from_point.z)
        return travel

