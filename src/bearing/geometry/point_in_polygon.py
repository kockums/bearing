# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Point-in-Polygon
==================================

The winding number, computed robustly, following:

    Hormann, K. & Agathos, A. (2001), "The point in polygon problem for
    arbitrary polygons", Computational Geometry 20(3), 131-144.

The winding number subsumes both fill rules: its parity reproduces the
**even-odd** rule and its being non-zero gives the **nonzero** rule, so a
single algorithm handles convex, concave, and self-intersecting rings. The
crossing test uses half-open vertical inequalities (a vertex on the test
ray is assigned to one side only), which structurally eliminates the
vertex-on-ray degeneracy that breaks naive ray casting — and the left/right
classification of each crossing edge is the sign of the robust
:func:`bearing.geometry.predicates.orient2d`, so near-boundary points are
classified consistently.

Rings are sequences of ``(x, y)`` pairs; the closing edge from the last
vertex back to the first is implicit (an explicitly-repeated first/last
vertex is fine — the zero-length closing edge contributes nothing).

Standard library only.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
from typing import Sequence

# Import | Local Modules
from bearing.geometry.predicates import orient2d


# =============================================================================
# Types
# =============================================================================

Point = tuple[float, float]
Ring = Sequence[Point]


# =============================================================================
# Functions
# =============================================================================

def winding_number(point: Point, ring: Ring) -> int:
    """
    The winding number of ``ring`` around ``point``: how many times the ring
    wraps the point, signed (positive counter-clockwise). ``0`` means the
    point is outside a simple ring.

    Uses the half-open crossing rule (edges count on upward crossings when
    the lower endpoint is at-or-below the point, and on downward crossings
    when the upper endpoint is at-or-below), with the robust orientation
    predicate deciding whether the crossing passes left or right of the point.
    """
    px, py = point
    n = len(ring)
    if n < 3:
        return 0
    wn = 0
    x1, y1 = ring[0]
    for i in range(1, n + 1):
        x2, y2 = ring[i % n]
        if y1 <= py:
            if y2 > py:  # upward crossing
                if orient2d(x1, y1, x2, y2, px, py) > 0.0:
                    wn += 1
        else:
            if y2 <= py:  # downward crossing
                if orient2d(x1, y1, x2, y2, px, py) < 0.0:
                    wn -= 1
        x1, y1 = x2, y2
    return wn


def contains(point: Point, ring: Ring, rule: str = "nonzero") -> bool:
    """
    Whether ``point`` lies inside ``ring`` under the given fill ``rule``:

    - ``"nonzero"`` (default): inside when the winding number is non-zero.
    - ``"even-odd"``: inside when the winding number is odd.

    A point exactly on an edge is not guaranteed a particular result (the
    boundary is measure-zero); use :func:`on_boundary` for an explicit test.
    """
    wn = winding_number(point, ring)
    if rule == "nonzero":
        return wn != 0
    if rule == "even-odd":
        return (wn % 2) != 0
    raise ValueError(f"unknown fill rule: {rule!r}")


def point_in_polygon(
    point: Point,
    exterior: Ring,
    holes: Sequence[Ring] = (),
    rule: str = "nonzero",
) -> bool:
    """
    Whether ``point`` lies inside a polygon with an ``exterior`` ring and
    zero or more ``holes``: inside the exterior and inside none of the holes.

    Ring orientation is irrelevant — containment is decided per ring by
    :func:`contains`, so callers need not pre-orient exterior CCW / holes CW.
    """
    if not contains(point, exterior, rule):
        return False
    for hole in holes:
        if contains(point, hole, rule):
            return False
    return True


def on_boundary(point: Point, ring: Ring, tol: float = 0.0) -> bool:
    """
    Whether ``point`` lies on an edge of ``ring``: collinear with an edge
    (robust orientation exactly zero, or within ``tol`` of the segment area)
    and within that edge's bounding box.
    """
    px, py = point
    n = len(ring)
    x1, y1 = ring[0]
    for i in range(1, n + 1):
        x2, y2 = ring[i % n]
        area2 = orient2d(x1, y1, x2, y2, px, py)
        if abs(area2) <= tol:
            # Collinear with the edge line: inside the segment's bbox?
            if (
                min(x1, x2) <= px <= max(x1, x2)
                and min(y1, y2) <= py <= max(y1, y2)
            ):
                return True
        x1, y1 = x2, y2
    return False
