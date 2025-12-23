# Centore Polyhedron Data Source

## Original Data

The semantic overlay polyhedra in this library are derived from Paul Centore's 2020 paper:

> Centore, P. (2020). "Beige, aqua, fuchsia, etc.: Definitions for some non-basic surface colour names".
> *Journal of the International Colour Association*, 25, 24-54.

The paper includes supplementary data in `PolyhedronFiles.zip`, which contains convex hull definitions for 30 color names:

### 20 Non-Basic Colors (Main Contribution)
aqua, beige, coral, fuchsia, gold, lavender, lilac, magenta, mauve, navy,
peach, rose, rust, sand, tan, taupe, teal, turquoise, violet, wine

### 10 Basic ISCC-NBS Colors (For Comparison)
black, blue, brown, gray, green, orange, pink, purple, red, yellow

## Data Derivation

The polyhedra were computed from ~16,000 CAUS (Color Association of the United States) fabric samples:

1. Each sample was measured with a spectrophotometer
2. Munsell coordinates (H, V, C) were computed
3. Converted to Cartesian (x, y, z) where:
   - x = chroma × cos(hue_angle)
   - y = chroma × sin(hue_angle)
   - z = value
4. Convex hull computed using Qhull algorithm
5. Vertices and faces exported as polyhedron definitions

## File Format (Original)

Each color has a file like `aqua_poly.txt`:
```
28 52          # vertices faces
-1.52 1.06 7.06    # vertex 0 (x, y, z)
-1.40 0.80 5.96    # vertex 1
...
0 6 7              # face 0 (v0, v1, v2)
6 13 7             # face 1
...
```

## Data in This Library

The polyhedron data has been converted to Rust constants in:
`src/constants/centore_polyhedra.rs`

Each color has:
- `POLYHEDRON_<NAME>_VERTICES: [(f64, f64, f64); N]`
- `POLYHEDRON_<NAME>_FACES: [(usize, usize, usize); M]`

## Centroids

Centroid coordinates from Table 1 of the paper are stored in:
`src/semantic_overlay_data.rs` as `OVERLAY_CENTROIDS`

## License and Attribution

The original paper and data are academic publications. When using this data:

1. Cite the original paper (see above)
2. Acknowledge CAUS as the source of fabric samples
3. Follow academic fair use guidelines

For commercial use, consult the journal's licensing terms.
