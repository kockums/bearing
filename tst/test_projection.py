# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Projection Tests
==================================

Web Mercator forward/inverse and tile math against known EPSG:3857 anchors.
"""


# =============================================================================
# Imports
# =============================================================================

import pytest

from bearing.projection import mercator


# =============================================================================
# Web Mercator
# =============================================================================

class TestWebMercator:

    def test_origin_maps_to_zero(self):
        x, y = mercator.lonlat_to_meters(0.0, 0.0)
        assert x == pytest.approx(0.0, abs=1e-6)
        assert y == pytest.approx(0.0, abs=1e-6)

    def test_antimeridian_is_world_extent(self):
        x, _ = mercator.lonlat_to_meters(180.0, 0.0)
        assert x == pytest.approx(mercator.ORIGIN_SHIFT, rel=1e-12)

    def test_meters_round_trip(self):
        lon, lat = 4.899431, 52.379189  # Amsterdam
        x, y = mercator.lonlat_to_meters(lon, lat)
        blon, blat = mercator.meters_to_lonlat(x, y)
        assert blon == pytest.approx(lon, abs=1e-9)
        assert blat == pytest.approx(lat, abs=1e-9)

    def test_latitude_clamped_at_limit(self):
        # Beyond the Mercator limit the projection clamps rather than diverging.
        _, y_hi = mercator.lonlat_to_meters(0.0, 89.0)
        _, y_lim = mercator.lonlat_to_meters(0.0, mercator.MAX_LATITUDE)
        assert y_hi == pytest.approx(y_lim, rel=1e-9)

    def test_known_amsterdam_meters(self):
        # EPSG:3857 of Amsterdam (spherical Mercator y = R*ln(tan(pi/4+lat/2))).
        x, y = mercator.lonlat_to_meters(4.899431, 52.379189)
        assert x == pytest.approx(545402.16, abs=1.0)
        assert y == pytest.approx(6868980.23, abs=1.0)


class TestTiles:

    def test_zoom0_single_tile(self):
        assert mercator.lonlat_to_tile(-179.0, 85.0, 0) == (0, 0)
        assert mercator.lonlat_to_tile(179.0, -85.0, 0) == (0, 0)

    def test_greenwich_equator_tile_z1(self):
        # Just west/north of (0,0) lands in the NW quadrant tile (0,0) at z1;
        # just east/south lands in (1,1).
        assert mercator.lonlat_to_tile(-0.001, 0.001, 1) == (0, 0)
        assert mercator.lonlat_to_tile(0.001, -0.001, 1) == (1, 1)

    def test_tile_bounds_cover_world_at_z0(self):
        w, s, e, n = mercator.tile_bounds(0, 0, 0)
        assert w == pytest.approx(-180.0)
        assert e == pytest.approx(180.0)
        assert n == pytest.approx(mercator.MAX_LATITUDE, abs=1e-6)
        assert s == pytest.approx(-mercator.MAX_LATITUDE, abs=1e-6)

    def test_pixels_round_trip(self):
        lon, lat = -73.9857, 40.7484  # NYC
        px, py = mercator.lonlat_to_pixels(lon, lat, 12)
        blon, blat = mercator.pixels_to_lonlat(px, py, 12)
        assert blon == pytest.approx(lon, abs=1e-6)
        assert blat == pytest.approx(lat, abs=1e-6)

    def test_tile_contains_its_own_center(self):
        # The center of a tile's bounds must map back to that tile.
        x, y, z = 2412, 3079, 13
        w, s, e, n = mercator.tile_bounds(x, y, z)
        cx, cy = (w + e) / 2.0, (s + n) / 2.0
        assert mercator.lonlat_to_tile(cx, cy, z) == (x, y)
