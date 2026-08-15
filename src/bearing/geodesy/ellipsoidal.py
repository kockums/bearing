# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Ellipsoidal Geodesy
=====================================

The geodesic direct and inverse problems on an ellipsoid of revolution,
solved with Vincenty's formulae:

    Vincenty, T. (1975), "Direct and inverse solutions of geodesics on the
    ellipsoid with application of nested equations", Survey Review 23(176),
    88-93.

Accuracy is sub-millimetre for the direct problem and for the inverse
problem away from the antipodes; both are closed-form arithmetic on
IEEE-754 doubles, no third-party dependencies. Angles at the API edge are
**degrees**; distances are metres.

Known limitation (see TODO phase 1): Vincenty's inverse iteration fails to
converge for **near-antipodal** point pairs. This module detects
non-convergence and raises :class:`AntipodalConvergenceError` rather than
returning a wrong answer silently. The roadmap upgrade to Karney's 2013
series method removes this limitation; the API here is deliberately the same
shape (``Geodesic.inverse`` / ``Geodesic.direct``) so that swap is transparent.

References
----------
- Vincenty (1975), Survey Review 23(176):88-93.
- Karney (2013), J. Geodesy 87(1):43-55 (the planned successor method).

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Standard Library
import math
from typing import NamedTuple


# =============================================================================
# Errors
# =============================================================================

class AntipodalConvergenceError(ValueError):
    """
    Raised when the inverse solution does not converge — the near-antipodal
    case Vincenty's method cannot resolve. Callers that must handle antipodes
    should fall back to the spherical approximation
    (:func:`bearing.geodesy.spherical.distance`) or await the Karney upgrade.
    """


# =============================================================================
# Results
# =============================================================================

class InverseResult(NamedTuple):
    """Outcome of the inverse problem."""

    s12: float       # geodesic distance, metres
    azi1_deg: float  # forward azimuth at point 1, degrees in [0, 360)
    azi2_deg: float  # forward azimuth at point 2, degrees in [0, 360)


class DirectResult(NamedTuple):
    """Outcome of the direct problem."""

    lat2_deg: float
    lon2_deg: float
    azi2_deg: float  # forward azimuth at the destination, degrees in [0, 360)


# =============================================================================
# Class
# =============================================================================

class Geodesic:
    """
    Geodesics on an ellipsoid of revolution defined by equatorial radius
    ``a`` (metres) and flattening ``f``.

    Attributes
    ----------
    a : float
        Equatorial radius, metres.
    f : float
        Flattening ``(a - b) / a``.
    b : float
        Polar (semi-minor) radius, metres.

    Methods
    -------
    inverse(lat1, lon1, lat2, lon2)
        Distance and forward azimuths between two points.
    direct(lat1, lon1, azi1, s12)
        Endpoint and final azimuth from a start, azimuth, and distance.
    """

    _MAX_ITER = 200
    _EPS = 1e-12

    def __init__(self, a: float, f: float) -> None:
        """Construct a geodesic model for the given ellipsoid."""
        self.a = float(a)
        self.f = float(f)
        self.b = a * (1.0 - f)
        # Second eccentricity squared, e'^2 = (a^2 - b^2) / b^2.
        self._ep2 = (self.a ** 2 - self.b ** 2) / (self.b ** 2)

    # -- Inverse problem ---------------------------------------------------

    def inverse(
        self,
        lat1_deg: float,
        lon1_deg: float,
        lat2_deg: float,
        lon2_deg: float,
    ) -> InverseResult:
        """
        The inverse problem: geodesic distance and forward azimuths between
        two points.

        Raises
        ------
        AntipodalConvergenceError
            If the iteration does not converge (near-antipodal points).
        """
        a, f, b = self.a, self.f, self.b
        phi1 = math.radians(lat1_deg)
        phi2 = math.radians(lat2_deg)
        L = math.radians(self._wrap180(lon2_deg - lon1_deg))

        # Reduced (parametric) latitudes.
        tan_u1 = (1.0 - f) * math.tan(phi1)
        tan_u2 = (1.0 - f) * math.tan(phi2)
        cos_u1 = 1.0 / math.sqrt(1.0 + tan_u1 * tan_u1)
        sin_u1 = tan_u1 * cos_u1
        cos_u2 = 1.0 / math.sqrt(1.0 + tan_u2 * tan_u2)
        sin_u2 = tan_u2 * cos_u2

        lmbda = L
        sin_sigma = cos_sigma = sigma = 0.0
        cos_sq_alpha = cos_2sigma_m = 0.0
        sin_lambda = cos_lambda = 0.0

        for _ in range(self._MAX_ITER):
            sin_lambda = math.sin(lmbda)
            cos_lambda = math.cos(lmbda)
            sin_sigma = math.sqrt(
                (cos_u2 * sin_lambda) ** 2
                + (cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lambda) ** 2
            )
            if sin_sigma == 0.0:
                # Coincident points.
                return InverseResult(0.0, 0.0, 0.0)
            cos_sigma = sin_u1 * sin_u2 + cos_u1 * cos_u2 * cos_lambda
            sigma = math.atan2(sin_sigma, cos_sigma)
            sin_alpha = cos_u1 * cos_u2 * sin_lambda / sin_sigma
            cos_sq_alpha = 1.0 - sin_alpha * sin_alpha
            if cos_sq_alpha == 0.0:
                # Equatorial line: cos(2 sigma_m) undefined, set to 0.
                cos_2sigma_m = 0.0
            else:
                cos_2sigma_m = cos_sigma - 2.0 * sin_u1 * sin_u2 / cos_sq_alpha
            c = f / 16.0 * cos_sq_alpha * (
                4.0 + f * (4.0 - 3.0 * cos_sq_alpha)
            )
            lmbda_prev = lmbda
            lmbda = L + (1.0 - c) * f * sin_alpha * (
                sigma
                + c * sin_sigma * (
                    cos_2sigma_m
                    + c * cos_sigma * (-1.0 + 2.0 * cos_2sigma_m ** 2)
                )
            )
            if abs(lmbda - lmbda_prev) < self._EPS:
                break
        else:
            raise AntipodalConvergenceError(
                "Vincenty inverse did not converge (near-antipodal points); "
                "use the spherical fallback or the Karney method."
            )

        u_sq = cos_sq_alpha * self._ep2
        big_a = 1.0 + u_sq / 16384.0 * (
            4096.0 + u_sq * (-768.0 + u_sq * (320.0 - 175.0 * u_sq))
        )
        big_b = u_sq / 1024.0 * (
            256.0 + u_sq * (-128.0 + u_sq * (74.0 - 47.0 * u_sq))
        )
        delta_sigma = big_b * sin_sigma * (
            cos_2sigma_m
            + big_b / 4.0 * (
                cos_sigma * (-1.0 + 2.0 * cos_2sigma_m ** 2)
                - big_b / 6.0 * cos_2sigma_m
                * (-3.0 + 4.0 * sin_sigma ** 2)
                * (-3.0 + 4.0 * cos_2sigma_m ** 2)
            )
        )
        s12 = b * big_a * (sigma - delta_sigma)

        azi1 = math.atan2(
            cos_u2 * sin_lambda,
            cos_u1 * sin_u2 - sin_u1 * cos_u2 * cos_lambda,
        )
        azi2 = math.atan2(
            cos_u1 * sin_lambda,
            -sin_u1 * cos_u2 + cos_u1 * sin_u2 * cos_lambda,
        )
        return InverseResult(
            s12=s12,
            azi1_deg=math.degrees(azi1) % 360.0,
            azi2_deg=math.degrees(azi2) % 360.0,
        )

    # -- Direct problem ----------------------------------------------------

    def direct(
        self,
        lat1_deg: float,
        lon1_deg: float,
        azi1_deg: float,
        s12: float,
    ) -> DirectResult:
        """
        The direct problem: the destination point and final azimuth reached
        by travelling ``s12`` metres from the start along forward azimuth
        ``azi1``. Converges everywhere (no antipodal restriction).
        """
        a, f, b = self.a, self.f, self.b
        phi1 = math.radians(lat1_deg)
        alpha1 = math.radians(azi1_deg)
        sin_alpha1 = math.sin(alpha1)
        cos_alpha1 = math.cos(alpha1)

        tan_u1 = (1.0 - f) * math.tan(phi1)
        cos_u1 = 1.0 / math.sqrt(1.0 + tan_u1 * tan_u1)
        sin_u1 = tan_u1 * cos_u1

        sigma1 = math.atan2(tan_u1, cos_alpha1)
        sin_alpha = cos_u1 * sin_alpha1
        cos_sq_alpha = 1.0 - sin_alpha * sin_alpha
        u_sq = cos_sq_alpha * self._ep2
        big_a = 1.0 + u_sq / 16384.0 * (
            4096.0 + u_sq * (-768.0 + u_sq * (320.0 - 175.0 * u_sq))
        )
        big_b = u_sq / 1024.0 * (
            256.0 + u_sq * (-128.0 + u_sq * (74.0 - 47.0 * u_sq))
        )

        sigma = s12 / (b * big_a)
        sin_sigma = cos_sigma = cos_2sigma_m = 0.0
        for _ in range(self._MAX_ITER):
            cos_2sigma_m = math.cos(2.0 * sigma1 + sigma)
            sin_sigma = math.sin(sigma)
            cos_sigma = math.cos(sigma)
            delta_sigma = big_b * sin_sigma * (
                cos_2sigma_m
                + big_b / 4.0 * (
                    cos_sigma * (-1.0 + 2.0 * cos_2sigma_m ** 2)
                    - big_b / 6.0 * cos_2sigma_m
                    * (-3.0 + 4.0 * sin_sigma ** 2)
                    * (-3.0 + 4.0 * cos_2sigma_m ** 2)
                )
            )
            sigma_prev = sigma
            sigma = s12 / (b * big_a) + delta_sigma
            if abs(sigma - sigma_prev) < self._EPS:
                break

        tmp = sin_u1 * sin_sigma - cos_u1 * cos_sigma * cos_alpha1
        phi2 = math.atan2(
            sin_u1 * cos_sigma + cos_u1 * sin_sigma * cos_alpha1,
            (1.0 - f) * math.sqrt(sin_alpha ** 2 + tmp ** 2),
        )
        lmbda = math.atan2(
            sin_sigma * sin_alpha1,
            cos_u1 * cos_sigma - sin_u1 * sin_sigma * cos_alpha1,
        )
        c = f / 16.0 * cos_sq_alpha * (4.0 + f * (4.0 - 3.0 * cos_sq_alpha))
        big_l = lmbda - (1.0 - c) * f * sin_alpha * (
            sigma
            + c * sin_sigma * (
                cos_2sigma_m
                + c * cos_sigma * (-1.0 + 2.0 * cos_2sigma_m ** 2)
            )
        )
        lon2 = self._wrap180(lon1_deg + math.degrees(big_l))
        azi2 = math.atan2(sin_alpha, -tmp)
        return DirectResult(
            lat2_deg=math.degrees(phi2),
            lon2_deg=lon2,
            azi2_deg=math.degrees(azi2) % 360.0,
        )

    # -- Helpers -----------------------------------------------------------

    @staticmethod
    def _wrap180(lon_deg: float) -> float:
        """Normalise a longitude to ``(-180, 180]``."""
        wrapped = math.fmod(lon_deg + 180.0, 360.0)
        if wrapped <= 0.0:
            wrapped += 360.0
        return wrapped - 180.0


# =============================================================================
# Standard ellipsoid
# =============================================================================

#: The WGS84 geodesic model (the default Earth).
WGS84 = Geodesic(6378137.0, 1.0 / 298.257223563)
