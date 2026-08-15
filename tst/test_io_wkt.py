# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - WKT IO Tests
==============================

Round-trips and OGC-spec conformance for the WKT reader/writer.
"""


# =============================================================================
# Imports
# =============================================================================

import pytest

from bearing.io import wkt


# =============================================================================
# Parsing
# =============================================================================

class TestLoads:

    def test_point(self):
        assert wkt.loads("POINT (30 10)") == {
            "type": "Point", "coordinates": [30.0, 10.0]
        }

    def test_linestring(self):
        g = wkt.loads("LINESTRING (30 10, 10 30, 40 40)")
        assert g["type"] == "LineString"
        assert g["coordinates"] == [[30, 10], [10, 30], [40, 40]]

    def test_polygon_with_hole(self):
        g = wkt.loads(
            "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10),"
            " (20 30, 35 35, 30 20, 20 30))"
        )
        assert g["type"] == "Polygon"
        assert len(g["coordinates"]) == 2
        assert g["coordinates"][0][0] == [35, 10]

    def test_multipoint_both_forms(self):
        a = wkt.loads("MULTIPOINT ((10 40), (40 30), (20 20))")
        b = wkt.loads("MULTIPOINT (10 40, 40 30, 20 20)")
        assert a == b
        assert a["coordinates"] == [[10, 40], [40, 30], [20, 20]]

    def test_multipolygon(self):
        g = wkt.loads(
            "MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)),"
            " ((15 5, 40 10, 10 20, 5 10, 15 5)))"
        )
        assert g["type"] == "MultiPolygon"
        assert len(g["coordinates"]) == 2

    def test_geometry_collection(self):
        g = wkt.loads("GEOMETRYCOLLECTION (POINT (4 6), LINESTRING (4 6, 7 10))")
        assert g["type"] == "GeometryCollection"
        assert [x["type"] for x in g["geometries"]] == ["Point", "LineString"]

    def test_point_z(self):
        g = wkt.loads("POINT Z (30 10 5)")
        assert g["coordinates"] == [30, 10, 5]

    def test_empty(self):
        assert wkt.loads("POINT EMPTY") == {"type": "Point", "coordinates": []}
        assert wkt.loads("GEOMETRYCOLLECTION EMPTY") == {
            "type": "GeometryCollection", "geometries": []
        }

    def test_measured_raises(self):
        with pytest.raises(NotImplementedError):
            wkt.loads("POINT M (30 10 5)")

    def test_garbage_raises(self):
        with pytest.raises(wkt.WKTError):
            wkt.loads("TRIANGLE (0 0, 1 0, 0 1)")
        with pytest.raises(wkt.WKTError):
            wkt.loads("POINT (30 10) EXTRA")


# =============================================================================
# Writing / round-trips
# =============================================================================

class TestDumps:

    def test_point_round_trip(self):
        text = "POINT (30 10)"
        assert wkt.dumps(wkt.loads(text)) == text

    def test_polygon_round_trip(self):
        text = "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10))"
        assert wkt.dumps(wkt.loads(text)) == text

    def test_multipolygon_round_trip(self):
        text = (
            "MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)), "
            "((15 5, 40 10, 10 20, 5 10, 15 5)))"
        )
        assert wkt.dumps(wkt.loads(text)) == text

    def test_geometry_collection_round_trip(self):
        text = "GEOMETRYCOLLECTION (POINT (4 6), LINESTRING (4 6, 7 10))"
        assert wkt.dumps(wkt.loads(text)) == text

    def test_point_z_round_trip(self):
        text = "POINT Z (30 10 5)"
        assert wkt.dumps(wkt.loads(text)) == text

    def test_precision(self):
        g = {"type": "Point", "coordinates": [1.23456789, 9.87654321]}
        assert wkt.dumps(g, precision=2) == "POINT (1.23 9.88)"

    def test_empty_round_trip(self):
        assert wkt.dumps(wkt.loads("POINT EMPTY")) == "POINT EMPTY"
