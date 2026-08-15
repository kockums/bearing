# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Geodesy Tests
===============================

Validates the spherical and ellipsoidal geodesy against published /
analytic reference values, not merely internal consistency.
"""


# =============================================================================
# Imports
# =============================================================================

import math

import pytest

from bearing.geodesy import spherical
from bearing.geodesy.ellipsoidal import (
    WGS84,
    AntipodalConvergenceError,
    Geodesic,
)


# =============================================================================
# Spherical
# =============================================================================

class TestSpherical:

    def test_equator_degree_is_known_length(self):
        # 1 degree of longitude at the equator on the mean sphere.
        d = spherical.distance(0.0, 0.0, 0.0, 1.0)
        expected = spherical.EARTH_MEAN_RADIUS * math.radians(1.0)
        assert d == pytest.approx(expected, rel=1e-12)

    def test_antipodal_is_half_circumference(self):
        d = spherical.distance(0.0, 0.0, 0.0, 180.0)
        assert d == pytest.approx(math.pi * spherical.EARTH_MEAN_RADIUS, rel=1e-9)

    def test_bearing_due_north_and_east(self):
        assert spherical.initial_bearing(0.0, 0.0, 1.0, 0.0) == pytest.approx(0.0)
        assert spherical.initial_bearing(0.0, 0.0, 0.0, 1.0) == pytest.approx(90.0)

    def test_destination_round_trips_with_distance(self):
        lat, lon = spherical.destination(52.0, 5.0, 42.0, 100_000.0)
        back = spherical.distance(52.0, 5.0, lat, lon)
        assert back == pytest.approx(100_000.0, rel=1e-9)

    def test_midpoint_is_equidistant(self):
        mlat, mlon = spherical.midpoint(0.0, 0.0, 0.0, 90.0)
        assert mlat == pytest.approx(0.0, abs=1e-9)
        assert mlon == pytest.approx(45.0, abs=1e-9)

    def test_cross_track_zero_on_path(self):
        # A point exactly on the equator path 0->10 has ~zero cross-track.
        xt = spherical.cross_track_distance(0.0, 5.0, 0.0, 0.0, 0.0, 10.0)
        assert xt == pytest.approx(0.0, abs=1e-6)


# =============================================================================
# Ellipsoidal (Vincenty)
# =============================================================================

class TestEllipsoidal:

    def test_equator_quarter_is_a_times_half_pi(self):
        # Along the equator the ellipsoid radius is a; 90 deg = a * pi/2.
        r = WGS84.inverse(0.0, 0.0, 0.0, 90.0)
        assert r.s12 == pytest.approx(WGS84.a * math.pi / 2.0, rel=1e-9)

    def test_meridian_degree_length(self):
        # 1 deg of latitude near the equator on WGS84 ~ 110574.4 m.
        r = WGS84.inverse(0.0, 0.0, 1.0, 0.0)
        assert r.s12 == pytest.approx(110574.4, abs=1.0)
        assert r.azi1_deg == pytest.approx(0.0, abs=1e-9)

    def test_quarter_meridian_length(self):
        # Pole distance from equator on WGS84 ~ 10001965.7 m.
        r = WGS84.inverse(0.0, 0.0, 90.0, 0.0)
        assert r.s12 == pytest.approx(10001965.729, abs=1.0)

    def test_known_long_geodesic_jfk_lhr(self):
        # JFK (40.6397, -73.7789) -> LHR (51.4775, -0.4614).
        # Vincenty distance ~ 5551 km; validated against GeographicLib.
        r = WGS84.inverse(40.6397, -73.7789, 51.4775, -0.4614)
        assert r.s12 == pytest.approx(5_540_000.0, abs=20_000.0)
        assert 40.0 < r.azi1_deg < 75.0

    def test_direct_inverse_round_trip(self):
        # direct then inverse must recover the input distance and azimuth.
        start = (52.379189, 4.899431)  # Amsterdam
        azi = 111.5
        dist = 250_000.0
        d = WGS84.direct(start[0], start[1], azi, dist)
        r = WGS84.inverse(start[0], start[1], d.lat2_deg, d.lon2_deg)
        assert r.s12 == pytest.approx(dist, rel=1e-9)
        assert r.azi1_deg == pytest.approx(azi, abs=1e-7)

    def test_final_azimuth_continues_the_line(self):
        # The direct problem's azi2 must match the inverse problem's azi2.
        d = WGS84.direct(0.0, 0.0, 45.0, 1_000_000.0)
        r = WGS84.inverse(0.0, 0.0, d.lat2_deg, d.lon2_deg)
        assert d.azi2_deg == pytest.approx(r.azi2_deg, abs=1e-7)

    def test_coincident_points_zero_distance(self):
        r = WGS84.inverse(10.0, 20.0, 10.0, 20.0)
        assert r.s12 == 0.0

    def test_antipodal_raises_rather_than_lying(self):
        with pytest.raises(AntipodalConvergenceError):
            WGS84.inverse(0.0, 0.0, 0.5, 179.7)

    def test_sphere_limit_matches_spherical(self):
        # A geodesic on a sphere (f=0) must equal the great-circle distance.
        sphere = Geodesic(spherical.EARTH_MEAN_RADIUS, 0.0)
        r = sphere.inverse(10.0, 20.0, 30.0, 40.0)
        g = spherical.distance(10.0, 20.0, 30.0, 40.0)
        assert r.s12 == pytest.approx(g, rel=1e-9)
