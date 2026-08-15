# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Geospatial Tests
==================================

The merged, dependency-free CRS and BoundingBox (formerly the Django/GDAL
``new/`` modules), plus the WGS84 constant.
"""


# =============================================================================
# Imports
# =============================================================================

import pytest

from bearing.exceptions import ExternalParsingError, ExternalValueError
from bearing.geospatial import CRS, WGS84, BoundingBox


# =============================================================================
# CRS
# =============================================================================

class TestCRS:

    def test_from_srid(self):
        crs = CRS.from_srid(4326)
        assert crs.srid == 4326
        assert crs.authority == "EPSG"
        assert crs.legacy == "EPSG:4326"
        assert crs.is_geographic

    def test_from_urn(self):
        crs = CRS.from_string("urn:ogc:def:crs:EPSG::3857")
        assert crs.srid == 3857
        assert crs.authority == "EPSG"
        assert not crs.is_geographic

    def test_from_urn_crs84(self):
        crs = CRS.from_string("urn:ogc:def:crs:OGC:1.3:CRS84")
        assert crs.srid == 4326
        assert crs.authority == "OGC"
        assert crs.crsid == "CRS84"

    def test_from_legacy_epsg(self):
        assert CRS.from_string("EPSG:4326").srid == 4326

    def test_from_legacy_opengis_url(self):
        crs = CRS.from_string("http://www.opengis.net/def/crs/EPSG/0/28992")
        assert crs.srid == 28992

    def test_bare_numeric_string(self):
        assert CRS.from_string("2154").srid == 2154

    def test_crs84_not_equal_epsg4326(self):
        # Same datum, opposite axis order — must NOT compare equal.
        epsg = CRS.from_string("EPSG:4326")
        ogc = CRS.from_string("urn:ogc:def:crs:OGC:1.3:CRS84")
        assert epsg != ogc
        assert epsg.is_yx_order
        assert not ogc.is_yx_order

    def test_equal_crs_hash_together(self):
        assert CRS.from_srid(3857) == CRS.from_string("EPSG:3857")
        assert len({CRS.from_srid(3857), CRS.from_string("EPSG:3857")}) == 1

    def test_urn_round_trip(self):
        crs = CRS.from_srid(4326)
        assert CRS.from_string(crs.urn).srid == 4326

    def test_bad_uri_raises(self):
        with pytest.raises(ExternalValueError):
            CRS.from_string("not-a-crs")
        with pytest.raises(ExternalValueError):
            CRS.from_string("urn:ogc:def:crs:OGC:1.3:CRS99")

    def test_wgs84_constant(self):
        assert WGS84.srid == 4326
        assert WGS84.is_geographic


# =============================================================================
# BoundingBox
# =============================================================================

class TestBoundingBox:

    def test_from_string_four(self):
        b = BoundingBox.from_string("2,50,7,54")
        assert b.as_tuple() == (2.0, 50.0, 7.0, 54.0)
        assert b.crs is None

    def test_from_string_with_crs(self):
        b = BoundingBox.from_string("2,50,7,54,EPSG:4326")
        assert b.crs == WGS84

    def test_from_string_wrong_arity(self):
        with pytest.raises(ExternalParsingError):
            BoundingBox.from_string("2,50,7")

    def test_geographic_aliases(self):
        b = BoundingBox(2, 50, 7, 54)
        assert (b.west, b.south, b.east, b.north) == (2, 50, 7, 54)

    def test_center_and_dims(self):
        b = BoundingBox(0, 0, 10, 20)
        assert b.center == (5.0, 10.0)
        assert b.width == 10.0
        assert b.height == 20.0

    def test_from_points(self):
        b = BoundingBox.from_points([(1, 5), (3, 2), (-1, 4)])
        assert b.as_tuple() == (-1.0, 2.0, 3.0, 5.0)

    def test_extend_to(self):
        b = BoundingBox(0, 0, 1, 1)
        b.extend_to(-1, -1, 2, 0.5)
        assert b.as_tuple() == (-1.0, -1.0, 2.0, 1.0)

    def test_union(self):
        a = BoundingBox(0, 0, 1, 1)
        b = BoundingBox(2, 2, 3, 3)
        u = a + b
        assert u.as_tuple() == (0.0, 0.0, 3.0, 3.0)

    def test_union_different_crs_raises(self):
        a = BoundingBox(0, 0, 1, 1, crs=CRS.from_srid(4326))
        b = BoundingBox(0, 0, 1, 1, crs=CRS.from_srid(3857))
        with pytest.raises(ValueError):
            _ = a + b

    def test_contains(self):
        b = BoundingBox(0, 0, 10, 10)
        assert b.contains(5, 5)
        assert b.contains(0, 0)     # boundary counts
        assert not b.contains(11, 5)

    def test_intersects(self):
        a = BoundingBox(0, 0, 5, 5)
        assert a.intersects(BoundingBox(4, 4, 9, 9))     # overlap
        assert a.intersects(BoundingBox(5, 5, 9, 9))     # touching
        assert not a.intersects(BoundingBox(6, 6, 9, 9))  # disjoint

    def test_as_ring_is_closed(self):
        b = BoundingBox(0, 0, 2, 2)
        ring = b.as_ring()
        assert ring[0] == ring[-1]
        assert len(ring) == 5
