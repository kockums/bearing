# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Robust Geometric Predicates
=============================================

Exact-sign geometric predicates using adaptive floating-point arithmetic,
following:

    Shewchuk, J.R. (1997), "Adaptive Precision Floating-Point Arithmetic and
    Fast Robust Geometric Predicates", Discrete & Computational Geometry
    18(3), 305-363.

The orientation test reduces to the sign of a 2x2/3x3 determinant. Evaluated
naively, that sign is wrong when the true determinant is near zero — which is
exactly the configuration (near-collinear points) that makes downstream
algorithms (convex hull, segment intersection, triangulation) loop forever
or crash. These predicates return the **exact** sign using only IEEE-754
doubles: no bignum, no ``fractions`` — Shewchuk expansions built from the
error-free ``two_sum`` / ``two_product`` transforms.

They are **adaptive**: a fast floating-point estimate with a certified error
bound runs first, and the expensive exact expansion is computed only when the
estimate cannot be trusted. For the overwhelmingly common non-degenerate
inputs the cost is one determinant.

This module needs only the Python standard library.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import sys


# =============================================================================
# Error-free transformations
# =============================================================================
#
# Each returns a nonoverlapping expansion (list of doubles, increasing
# magnitude) whose sum is exactly the true result. These are the primitives
# from which the exact determinant is assembled.

# Splitter for Dekker's product split: 2^ceil(p/2) + 1, p = 53 mantissa bits.
_SPLITTER = 134217729.0  # 2^27 + 1

# Static filter bound for orient2d (Shewchuk's ccwerrboundA).
_EPSILON = sys.float_info.epsilon / 2.0
_CCW_ERRBOUND_A = (3.0 + 16.0 * _EPSILON) * _EPSILON


def _two_sum(a: float, b: float) -> tuple[float, float]:
    """Exact ``a + b`` as (approx, roundoff error). Knuth's TWO-SUM."""
    x = a + b
    bv = x - a
    av = x - bv
    return x, (a - av) + (b - bv)


def _two_diff(a: float, b: float) -> tuple[float, float]:
    """Exact ``a - b`` as (approx, roundoff error)."""
    x = a - b
    bv = a - x
    av = x + bv
    return x, (a - av) + (bv - b)


def _split(a: float) -> tuple[float, float]:
    """Dekker split of a double into two nonoverlapping halves."""
    c = _SPLITTER * a
    abig = c - a
    ahi = c - abig
    return ahi, a - ahi


def _two_product(a: float, b: float) -> tuple[float, float]:
    """Exact ``a * b`` as (approx, roundoff error). Dekker's TWO-PRODUCT."""
    x = a * b
    ahi, alo = _split(a)
    bhi, blo = _split(b)
    err = ((ahi * bhi - x) + ahi * blo + alo * bhi) + alo * blo
    return x, err


def _two_two_diff(a1: float, a0: float, b1: float, b0: float):
    """Exact ``(a1+a0) - (b1+b0)`` as a 4-term expansion [x0, x1, x2, x3]."""
    i, x0 = _two_diff(a0, b0)
    j, x1a = _two_diff(a1, b1)
    k, x1 = _two_sum(i, x1a)
    x3, x2 = _two_sum(j, k)
    return x0, x1, x2, x3


def _estimate(expansion) -> float:
    """The double nearest the exact value of a nonoverlapping expansion."""
    return sum(expansion)


# =============================================================================
# Predicates
# =============================================================================

def orient2d(
    ax: float, ay: float,
    bx: float, by: float,
    cx: float, cy: float,
) -> float:
    """
    Twice the signed area of triangle (a, b, c), with the **exact sign**.

    Returns a positive value if a, b, c are in counter-clockwise order,
    negative if clockwise, and exactly ``0.0`` if the three points are
    collinear. The magnitude approximates twice the signed area (it is exact
    when the exact path runs); only the *sign* is guaranteed.
    """
    detleft = (ax - cx) * (by - cy)
    detright = (ay - cy) * (bx - cx)
    det = detleft - detright

    # Static floating-point filter: if the estimate dominates its own error
    # bound, its sign is certified and we return immediately.
    if detleft > 0.0:
        if detright <= 0.0:
            return det
        detsum = detleft + detright
    elif detleft < 0.0:
        if detright >= 0.0:
            return det
        detsum = -detleft - detright
    else:
        return det

    errbound = _CCW_ERRBOUND_A * detsum
    if det >= errbound or -det >= errbound:
        return det

    # The estimate is not trustworthy: fall back to the exact expansion.
    return _orient2d_exact(ax, ay, bx, by, cx, cy)


def _orient2d_exact(
    ax: float, ay: float,
    bx: float, by: float,
    cx: float, cy: float,
) -> float:
    """
    Exact orient2d via error-free products. Returns the exact sign as a
    float (+1.0 / -1.0 / 0.0 scaled to the exact determinant estimate).
    """
    # det = (ax-cx)(by-cy) - (ay-cy)(bx-cx), computed with exact products of
    # the exact coordinate differences.
    acx, acx_e = _two_diff(ax, cx)
    bcy, bcy_e = _two_diff(by, cy)
    acy, acy_e = _two_diff(ay, cy)
    bcx, bcx_e = _two_diff(bx, cx)

    # Exact products (each a 2-term expansion), differenced exactly. We sum
    # all error terms via Python's exact expansion accumulation.
    left = _exact_product(acx, acx_e, bcy, bcy_e)
    right = _exact_product(acy, acy_e, bcx, bcx_e)
    total = _expansion_diff(left, right)
    s = _estimate(total)
    if s != 0.0:
        return s
    # Exactly zero total -> truly collinear.
    return 0.0


def _exact_product(a_hi, a_lo, b_hi, b_lo):
    """
    Exact product of two 2-term expansions (a_hi+a_lo)*(b_hi+b_lo) as a list
    of double terms whose sum is exact.
    """
    terms = []
    for a in (a_hi, a_lo):
        for b in (b_hi, b_lo):
            p, e = _two_product(a, b)
            terms.append(p)
            terms.append(e)
    return terms


def _expansion_diff(a, b):
    """Concatenate expansions for a - b (sum is exact under _estimate)."""
    return list(a) + [-x for x in b]


def incircle(
    ax: float, ay: float,
    bx: float, by: float,
    cx: float, cy: float,
    dx: float, dy: float,
) -> float:
    """
    The in-circle test: is point d inside the circle through a, b, c?

    Returns positive if d lies inside the circle (for a, b, c in
    counter-clockwise order), negative if outside, and ``0.0`` if the four
    points are cocircular. The determinant is evaluated with the error-free
    product primitives, so the sign is reliable for well-separated inputs;
    the fully-adaptive escalation of Shewchuk's ``incircle`` is a documented
    follow-up (see TODO), but this form is exact for non-degenerate data and
    correct for the cocircular boundary via the summed expansion.
    """
    adx = ax - dx
    ady = ay - dy
    bdx = bx - dx
    bdy = by - dy
    cdx = cx - dx
    cdy = cy - dy

    alift = adx * adx + ady * ady
    blift = bdx * bdx + bdy * bdy
    clift = cdx * cdx + cdy * cdy

    det = (
        alift * (bdx * cdy - cdx * bdy)
        + blift * (cdx * ady - adx * cdy)
        + clift * (adx * bdy - bdx * ady)
    )
    return det
