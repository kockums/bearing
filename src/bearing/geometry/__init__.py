# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Geometry Module
========================


"""


# =============================================================================
# Imports
# =============================================================================

# Import | Future
from __future__ import annotations

# Import | Local Modules
from bearing.geometry.point_in_polygon import (
    contains,
    on_boundary,
    point_in_polygon,
    winding_number,
)
from bearing.geometry.predicates import incircle, orient2d


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "contains",
    "incircle",
    "on_boundary",
    "orient2d",
    "point_in_polygon",
    "winding_number",
]

