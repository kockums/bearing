# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Vector Tests
==============================

The merged vector package: the pure VectorLayer descriptor and the pure
VectorTile addressing (formerly the mercantile/Django ``new/`` modules).
"""


# =============================================================================
# Imports
# =============================================================================

import pytest

from bearing.projection import mercator
from bearing.vector import VectorLayer, VectorTile


# =============================================================================
# VectorLayer
# =============================================================================

class TestVectorLayer:

    def test_defaults(self):
        layer = VectorLayer("roads")
        assert layer.id == "roads"
        assert layer.min_zoom == 0
        assert layer.max_zoom == 22

    def test_as_dict(self):
        layer = VectorLayer("water", description="rivers", min_zoom=4, max_zoom=14)
        d = layer.as_dict()
        assert d["id"] == "water"
        assert d["description"] == "rivers"
        assert d["minzoom"] == 4
        assert d["maxzoom"] == 14
        assert d["fields"] == {}


# =============================================================================
# VectorTile
# =============================================================================

class TestVectorTile:

    def test_bounds_match_mercator(self):
        t = VectorTile(2412, 3079, 13)
        assert t.bounds() == mercator.tile_bounds(2412, 3079, 13)
        assert t.bounds_meters() == mercator.tile_bounds_meters(2412, 3079, 13)

    def test_bounds_meters_z0_is_whole_world(self):
        left, bottom, right, top = VectorTile(0, 0, 0).bounds_meters()
        assert left == pytest.approx(-mercator.ORIGIN_SHIFT)
        assert right == pytest.approx(mercator.ORIGIN_SHIFT)
        assert top == pytest.approx(mercator.ORIGIN_SHIFT)
        assert bottom == pytest.approx(-mercator.ORIGIN_SHIFT)

    def test_containing_round_trips(self):
        # A tile's own center must resolve back to that tile.
        t = VectorTile(2412, 3079, 13)
        w, s, e, n = t.bounds()
        cx, cy = (w + e) / 2.0, (s + n) / 2.0
        got = VectorTile.containing(cx, cy, 13)
        assert (got.x, got.y, got.z) == (2412, 3079, 13)

    def test_bounding_box_is_wgs84(self):
        bb = VectorTile(0, 0, 1).bounding_box()
        assert bb.crs.srid == 4326
        assert bb.west == pytest.approx(-180.0)

    def test_default_extent_and_buffer(self):
        t = VectorTile(1, 2, 3)
        assert t.extent == 4096
        assert t.buffer == 256
