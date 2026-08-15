# TODO — the dependency-free geospatial core

Bearing is a **general-purpose, zero-runtime-dependency** (Python stdlib
only, 3.11+) geospatial library. The doctrine is in
[DEPENDENCIES.md](DEPENDENCIES.md): anything that needs numpy / GDAL /
shapely / pyproj belongs downstream in `ortha`, never here. This file is the
roadmap for *what a pure-Python core should own* and the order to build it.

The scope below is grounded in a verified research pass (2026-07-25) across
five angles. The headline result: **a stdlib-only core can legitimately own
the entire canonical algorithmic surface**, because the authoritative
algorithms are closed-form arithmetic on IEEE-754 doubles — no native
libraries are *required* for correctness. The real constraint is
*performance*, and that is exactly the line the `ortha` split draws:
correctness lives here, throughput-critical bulk operations may be delegated.

Legend: `[x]` done · `[~]` partial · `[ ]` open · sizing S/M/L/XL. Every
item cites the canonical algorithm it must implement, so "done" is checkable
against a reference, not a matter of taste.

## Doctrine gates (every item)

- **No runtime imports outside the stdlib.** `import bearing` must never pull
  a third-party package. Compute-heavy ops may ship a documented "delegate to
  `ortha` for large inputs" note, but the pure path must exist and be correct.
- **IEEE-754 doubles are the substrate.** No bignum, no rationals — the
  robust-geometry work uses Shewchuk expansions (float-only), not `fractions`.
- **Correctness is validated against published reference values**, not
  self-consistency: geodesics against GeographicLib test vectors, predicates
  against known degenerate configurations, WKT/WKB against the OGC spec.
- **Angles are radians internally, degrees at the API edge** where a name says
  `_deg`; longitude east-positive, latitude north-positive.

## Phase 1 — the correctness core (in progress)

The flagship modules: geodesy, robust predicates, point-in-polygon, the base
projection, and WKT interchange. Each is fully implementable and testable
without dependencies.

- [x] **Great-circle geodesy** (S) — `geodesy/spherical.py`: distance,
  initial/final bearing, destination, midpoint, fractional interpolation,
  cross-track and along-track distance. Exact spherical formulae (haversine /
  the numerically-stable `atan2` variants), the correct base for the sphere
  and the sanity check for the ellipsoid.
- [x] **Ellipsoidal geodesy — Vincenty** (L) — `geodesy/ellipsoidal.py`: the
  direct problem (endpoint from start + azimuth + distance) and inverse
  (distance + azimuths between two points) via Vincenty's 1975 nested
  equations, as `Geodesic.inverse` / `Geodesic.direct`. Sub-millimetre away
  from the antipodes; validated against the equator-quarter (`a·π/2`),
  quarter-meridian (10001965.7 m), and meridian-degree analytic values, the
  JFK→LHR long geodesic, direct/inverse round-trip, and the `f=0` sphere
  limit. **Near-antipodal pairs raise `AntipodalConvergenceError`** rather
  than returning a wrong answer — the honest failure mode until the Karney
  upgrade (Phase 2) removes it. The API shape is deliberately Karney-ready so
  that swap is transparent.
- [ ] **Ellipsoidal geodesy — Karney upgrade** (L) — replace the Vincenty
  core with Karney's 2013 series (*J. Geodesy* 87(1):43–55), structured as
  GeographicLib's `Geodesic` / `GeodesicLine`: converges everywhere including
  the near-antipodal region Vincenty cannot, and yields the reduced length /
  geodesic scale for free. Same public API; drops
  `AntipodalConvergenceError`. Validate against Karney's `GeodTest` vectors.
- [x] **Robust orientation predicate** (M) — `geometry/predicates.py`:
  Shewchuk adaptive-precision `orient2d` (float-only expansions via
  `two_sum` / `two_product`), the exact-sign determinant that naive floats
  mis-sign near zero. The foundation for segment intersection, hull, and
  triangulation. `incircle` is the next-in-line follow-up.
- [x] **Point-in-polygon — winding number** (M) —
  `geometry/point_in_polygon.py`: Hormann & Agathos integer-arithmetic
  winding number (no divisions; quadrant classification that structurally
  avoids the vertex-on-ray degeneracy). Handles holes and self-intersecting
  rings; even-odd and nonzero rules fall out of the winding parity.
- [x] **Web Mercator projection** (S) — `projection/mercator.py`: EPSG:3857
  forward/inverse plus the spherical-Mercator tile math (lon/lat ↔ world
  pixels ↔ XYZ tiles), the projection every slippy-map pipeline needs.
- [x] **WKT interchange** (M) — `io/wkt.py`: read/write for the OGC Simple
  Features geometry set (Point, LineString, Polygon, Multi*, and
  GeometryCollection) over GeoJSON-style geometry dicts, plus the `EMPTY`
  forms and 2D/3D (the `Z` tag). Pure recursive-descent over the stdlib.
  Measured coordinates (`M` / `ZM`) parse to their dimensionality but raise
  `NotImplementedError` on emit until the object model carries M — Phase 2.

## Phase 2 — projections & the rest of interchange

- [ ] **Transverse Mercator / UTM — Krüger series** (L) —
  `projection/transverse_mercator.py`: Karney's extended-Krüger truncated
  series (<5 nm within 3900 km of the central meridian — far tighter than
  UTM's ~333 km zone half-width, so the exact elliptic-function method is
  unnecessary). Plus the UTM zone/band machinery and MGRS.
- [ ] **WKB interchange** (M) — `io/wkb.py`: byte-order flag + type integer;
  the seven core types (Point=1 … GeometryCollection=7). **Must support both
  Z/M encodings**: ISO offsets (+1000 Z, +2000 M, +3000 ZM) *and* EWKB high
  bits (Z=0x80000000, M=0x40000000, SRID=0x20000000). A parser that assumes
  one silently corrupts the other.
- [ ] **GeoJSON (RFC 7946)** (M) — `io/geojson.py`: parse/emit against the
  stdlib `json`, honoring the normative rules — right-hand-rule winding, the
  **antimeridian split** (§3.1.9), and bbox with antimeridian-crossing.
  *Open correctness question:* the research pass could not settle the exact
  antimeridian/pole rules for emission — resolve against RFC 7946 §3.1.9 and
  §5.2 **before** shipping the emitter, with explicit crossing-case tests.
- [ ] **OGC Simple Features object model** (M) — `geometry/features.py`: the
  abstract `Geometry` hierarchy (Point, Curve/LineString/LinearRing,
  Surface/Polygon, the Multi* collections, GeometryCollection) shared by the
  WKT/WKB/GeoJSON codecs, with `is_valid` / `is_simple` predicates.

## Phase 3 — computational geometry

- [ ] **Segment intersection** (S) — on top of `orient2d`; the robust
  proper/improper-intersection classification.
- [ ] **Convex hull** (S) — Andrew's monotone chain, orientation-predicate
  based.
- [ ] **Polygon clipping** (M) — Sutherland–Hodgman (convex clip window)
  first; Weiler–Atherton / Greiner–Hormann for general polygon–polygon.
- [ ] **Ear-clipping triangulation** (M) — O(n²) with hole bridging (outer
  CCW, holes CW, oppositely-directed bridge edges). Note: do **not** rely on
  the "test only reflex vertices" O(n²) argument — the research pass refuted
  that specific justification; implement the containment test straightforwardly.
- [ ] **Line simplification** (S) — Douglas–Peucker and Visvalingam–Whyatt.
- [ ] **`incircle` predicate + Delaunay** (L) — adaptive `incircle` then
  incremental / divide-and-conquer Delaunay; the heavy one, and the first
  real candidate for an `ortha` fast-path on large inputs.

## Phase 4 — spatial indexing

Research support here was **thin** — only the S2 cell-ID structure was
independently verified; the rest is inferred by extension (all reduce to bit
manipulation and comparisons, so feasibility is not in doubt, but the
"worth-owning-in-interpreted-Python vs delegate" tradeoff is unsettled).
Treat these as a design investigation, not a settled build order.

- [ ] **Space-filling curves** (S) — Morton (Z-order) and Hilbert encode/
  decode; the primitive under the rest.
- [ ] **Geohash** (S) — encode/decode/neighbors/bbox, base-32.
- [ ] **DGGS cell IDs** (M) — S2-style 64-bit IDs (3-bit face + Hilbert
  position + level sentinel). Cross-check vocabulary with the sibling
  `gg` / `orbio-dggs` ISEA4H work — a shared cell-addressing story may be
  worth more than an isolated S2 port.
- [ ] **In-memory indexes** (M) — quadtree, k-d tree, and a bulk-loaded
  (STR) R-tree. Bench honestly against a linear scan in interpreted Python
  before claiming they earn their place; large-N indexing may belong in
  `ortha`.

## Phase 5 — clear the dependency ledger

Per DEPENDENCIES.md, the last in-code third-party imports get resolved as
their pure replacements land above:

- [x] **Merge the `new/` staging directory** (2026-07-25) — the Django-GIS /
  GDAL / `mercantile` code was folded into pure homes and `new/` deleted:
  `new/crs.py` → pure `geospatial/crs.py` (CRS identity/parser, GDAL dropped,
  reprojection delegated); `new/bounding_box.py` → pure
  `geospatial/bounding_box.py` (replacing the broken duplicate);
  `new/vector_layer.py` + `new/vector_tile.py` → the new `bearing/vector/`
  package (mercantile → `projection.mercator.tile_bounds_meters`; the Django
  serving mixin dropped to `ortha`). New stdlib `bearing/exceptions.py`.
- [x] `geospatial/wgs84.py` — dangling `CRS.from_srid` reference fixed; now a
  real `CRS` constant plus the WGS84 ellipsoid constants.
- [ ] `math/distance.py` — drop matplotlib/numpy/scipy; the pure distance
  math already lives in the geodesy modules, the RBF/plot pieces relocate to
  `ortha`.
- [ ] `math/interpolation.py`, `math/filter.py` — rewrite pure or relocate.
- [ ] `math/plot.py` — relocate (visualization is not core geo).
- [ ] `data/cell/*.py` — relocate the numpy grid machinery to `ortha`.
- [ ] `geospatial/grid.py` — rewrite (geojson is dict-shaping, stdlib-doable).
- [ ] `geospatial/coordinate.py` — drop pyproj/geojson; route transforms
  through the new `projection/` + `geodesy/` modules.

## Definition of done (per item)

- Pure stdlib imports; `import bearing` stays dependency-free.
- Validated against the cited reference (values, spec, or known degeneracy),
  not just internal consistency.
- Tests under `tst/` (`test_*.py`), green under `pytest`.
- House style: utf-8 header, the `====` section dividers, NumPy-style
  docstrings, radians-internal / degrees-at-`_deg`-edges.
