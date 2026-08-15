# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Kockums Bearing - Vector Package
================================

Vector-tile addressing and layer descriptors, dependency-free. Tile-payload
*generation* (MVT/protobuf, feature querysets) is a pipeline concern and
lives downstream in ``ortha``; this package carries only the portable,
geometry-only pieces.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from bearing.vector.layer import VectorLayer
from bearing.vector.tile import VectorTile


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "VectorLayer",
    "VectorTile",
]
