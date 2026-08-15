# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Geometry Tests
================================

Robust predicates (orient2d exact sign) and the winding-number
point-in-polygon.
"""


# =============================================================================
# Imports
# =============================================================================

from bearing.geometry.point_in_polygon import (
    contains,
    on_boundary,
    point_in_polygon,
    winding_number,
)
from bearing.geometry.predicates import incircle, orient2d


# =============================================================================
# Predicates
# =============================================================================

class TestOrient2d:

    def test_counter_clockwise_positive(self):
        assert orient2d(0, 0, 1, 0, 0, 1) > 0

    def test_clockwise_negative(self):
        assert orient2d(0, 0, 0, 1, 1, 0) < 0

    def test_collinear_exactly_zero(self):
        assert orient2d(0, 0, 1, 1, 2, 2) == 0.0

    def test_robustness_near_collinear(self):
        # A configuration where the naive float determinant mis-signs but the
        # exact predicate must not. The three points are collinear on the line
        # y = x, perturbed by one ULP; the exact answer is a definite sign.
        # Classic Shewchuk stress: points on a line with tiny perturbation.
        a = (0.5, 0.5)
        b = (12.0, 12.0)
        c = (24.0, 24.0)
        assert orient2d(*a, *b, *c) == 0.0
        # Perturb c off the line by the smallest representable amount upward:
        c_off = (24.0, 24.0 + 4e-15)
        assert orient2d(*a, *b, *c_off) > 0.0

    def test_symmetry_of_sign(self):
        # Swapping two vertices flips the sign exactly.
        p = orient2d(0, 0, 3, 1, 1, 4)
        q = orient2d(0, 0, 1, 4, 3, 1)
        assert p == -q


class TestIncircle:

    def test_point_inside_circle(self):
        # Unit square CCW; centre point is inside the circumscribing circle.
        assert incircle(0, 0, 1, 0, 1, 1, 0.5, 0.5) > 0

    def test_point_outside_circle(self):
        assert incircle(0, 0, 1, 0, 1, 1, 5.0, 5.0) < 0

    def test_cocircular_zero(self):
        # Four corners of the unit square are cocircular.
        assert incircle(0, 0, 1, 0, 1, 1, 0, 1) == 0.0


# =============================================================================
# Point in polygon
# =============================================================================

SQUARE = [(0, 0), (4, 0), (4, 4), (0, 4)]


class TestPointInPolygon:

    def test_inside_square(self):
        assert winding_number((2, 2), SQUARE) == 1
        assert contains((2, 2), SQUARE)

    def test_outside_square(self):
        assert winding_number((5, 5), SQUARE) == 0
        assert not contains((5, 5), SQUARE)

    def test_orientation_independent(self):
        # A clockwise ring gives winding -1 but still "contains".
        cw = list(reversed(SQUARE))
        assert winding_number((2, 2), cw) == -1
        assert contains((2, 2), cw)

    def test_polygon_with_hole(self):
        exterior = [(0, 0), (10, 0), (10, 10), (0, 10)]
        hole = [(3, 3), (7, 3), (7, 7), (3, 7)]
        assert point_in_polygon((1, 1), exterior, [hole])       # ring, not hole
        assert not point_in_polygon((5, 5), exterior, [hole])   # inside hole
        assert not point_in_polygon((20, 20), exterior, [hole]) # outside

    def test_concave_polygon(self):
        # A U-shape: the notch is outside.
        u = [(0, 0), (6, 0), (6, 6), (4, 6), (4, 2), (2, 2), (2, 6), (0, 6)]
        assert contains((1, 3), u)
        assert not contains((3, 4), u)  # in the notch

    def test_self_intersecting_nonzero_vs_evenodd(self):
        # A pentagram (self-intersecting): the centre is inside under the
        # nonzero rule but outside under even-odd.
        import math
        star = []
        for k in range(5):
            ang = math.pi / 2 + k * 4 * math.pi / 5  # step by 2 points
            star.append((math.cos(ang), math.sin(ang)))
        centre = (0.0, 0.0)
        assert contains(centre, star, rule="nonzero")
        assert not contains(centre, star, rule="even-odd")

    def test_vertex_on_ray_is_not_a_degeneracy(self):
        # A point horizontally aligned with vertices must still classify
        # correctly (the half-open rule prevents double/zero counting).
        poly = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]
        assert contains((1, 2), poly)   # y aligned with two vertices
        assert not contains((3, 3), poly)

    def test_on_boundary(self):
        assert on_boundary((2, 0), SQUARE)     # on the bottom edge
        assert not on_boundary((2, 2), SQUARE)  # interior
