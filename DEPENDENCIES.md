# Dependencies

This guide describes the dependencies of this repository and their purpose.

## Doctrine: dependency-free

**bearing carries zero runtime dependencies.** It is the home for generic,
commercially non-sensitive geospatial Python; anything that needs
third-party packages (raster IO, tile archives, pipeline machinery) belongs
in `ortha` (the private orbio-pipelines foundation), which may depend on
bearing — never the reverse.

Status (2026-07-25): the `new/` staging directory (Django-GIS / GDAL /
`mercantile` code lifted from a WFS service) was **merged down to pure
modules and removed**: `new/crs.py` → `geospatial/crs.py` (a stdlib CRS
identity/parser, no GDAL — reprojection delegated), `new/bounding_box.py` →
`geospatial/bounding_box.py` (pure, replacing the previously-broken
duplicate), and `new/vector_layer.py` + `new/vector_tile.py` → the new
`bearing/vector/` package (the `mercantile` tile math is now
`projection.mercator.tile_bounds_meters`; the Django serving mixin was
dropped — it belongs in `ortha`). A new stdlib `bearing/exceptions.py`
supplies the `External*` errors those parsers raise. `wgs84.py`'s dangling
`CRS` reference is fixed. All of these now import under a hard block on
django/gdal/mercantile.

Earlier (2026-07-22): the declared runtime dependencies (`pillow`, `gdal`,
`rite`) were removed — nothing in `src/` imported them. The remaining
in-code violations, slated for pure rewrite or relocation to `ortha`:

| Module | Imports | Disposition |
| --- | --- | --- |
| `bearing/math/plot.py` | matplotlib, numpy | relocate (visualization is not core geo) |
| `bearing/math/distance.py` | matplotlib, numpy, scipy | split: pure distance math stays (now also in `geodesy/`), RBF/plotting relocate |
| `bearing/math/interpolation.py` | numpy | rewrite pure or relocate |
| `bearing/math/filter.py` | numpy | rewrite pure or relocate |
| `bearing/data/cell/*.py` | numpy | relocate (grid data machinery) |
| `bearing/geospatial/grid.py` | geojson, numpy | rewrite: geojson is dict-shaping, doable in stdlib |
| `bearing/geospatial/coordinate.py` | pyproj, geojson | rewrite: route transforms through `projection/` + `geodesy/`, drop pyproj |

Until the ledger clears, importing those specific modules requires the
listed packages; importing `bearing` itself must not. The `geospatial`
package `__init__` re-exports only the pure members (`CRS`, `BoundingBox`,
`WGS84`), so `import bearing.geospatial` stays clean.

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Package Dependencies](#package-dependencies)
- [Peer Dependencies](#peer-dependencies)
- [Development Dependencies](#development-dependencies)

## Package Dependencies

Package dependencies, or just regular dependencies are those packages that are needed for the
library code to run properly and so are are included as part of the library's final production bundle.

## Peer Dependencies

Peer dependencies are package dependencies that the library depends on
but are not included as part of the library's final production bundle.

Usually peer dependencies are packages that would-be users would already have or need
as part of their own applications, and hence, no need to include them as part of
the library code.

## Development Dependencies

Development dependencies are package dependencies used while developing library code
but are not part of the library's final production bundle.
